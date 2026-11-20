---
title: "Prácticas"
weight: 11
bookToc: true
---

# Tema 6 · Prácticas · Copias de seguridad, importación y exportación

{{< ra "RA6:a,b,c,d,e,f,g,h" >}}

| Práctica | Tipo | Nivel | CE principales |
|---|---|---|---|
| [6.1 Copia lógica de EduGest y restauración](#práctica-61--copia-lógica-de-edugest-y-restauración) | Guiada | ●●○ | RA6.a, RA6.b, RA6.c |
| [6.2 Exportar datos a CSV, JSON y SQL](#práctica-62--exportar-datos-a-csv-json-y-sql) | Guiada | ●○○ | RA6.d, RA6.e |
| [6.3 Importar con SQL\*Loader y leer los errores](#práctica-63--importar-con-sqlloader-y-leer-los-errores) | Autónoma | ●●○ | RA6.f, RA6.g |
| [6.4 De Oracle a PostgreSQL](#práctica-64--de-oracle-a-postgresql) | Guiada | ●●○ | RA6.e, RA6.f, RA6.h |
| [6.5 Reto: plan de copias y simulacro de desastre](#práctica-65--reto-plan-de-copias-y-simulacro-de-desastre) | Reto | ●●● | RA6.a, RA6.b, RA6.c, RA6.g |
| [Proyecto EduGest · Tema 6](#proyecto-edugest--tema-6-seguridad-de-la-información) | Proyecto | ●●● | RA6 completo |

> [!IMPORTANT]
> Estas prácticas suponen que tienes EduGest cargado y los contenedores `oracle26ai` en marcha (y, para la práctica 6.4, PostgreSQL) (guía de [entorno](/guia/entorno)). Las comprobaciones de filas suponen los datos originales: 32 alumnos y 143 matrículas.

---

## Práctica 6.1 · Copia lógica de EduGest y restauración

{{< practica num="6.1" tipo="Guiada" duracion="2 sesiones" nivel="2" ra="RA6: a, b, c" sgbd="Oracle 26ai · Data Pump · Docker" entrega="edugest_exp.log + edugest_imp.log + capturas de la comprobación" >}}

#### Objetivo

Hacer una copia lógica del esquema `EDUGEST`, sacarla del contenedor y restaurarla en un esquema de pruebas, comprobando que no se ha perdido nada.

#### Desarrollo

{{% steps %}}

1. **Localiza el directorio de Data Pump.** Como `SYSTEM` en `FREEPDB1`:

    ```sql
    SELECT directory_path FROM dba_directories WHERE directory_name = 'DATA_PUMP_DIR';
    ```

    Anota la ruta. ¿Es la misma carpeta que contiene los datos de la base de datos, o una aparte?

2. **Exporta el esquema.** En una terminal de tu equipo:

    ```bash
    docker exec -it oracle26ai expdp system/Oracle_2026@//localhost:1521/FREEPDB1 \
      schemas=EDUGEST directory=DATA_PUMP_DIR dumpfile=edugest_%U.dmp logfile=edugest_exp.log
    ```

    Lee las últimas líneas. Debe aparecer `successfully completed`. Anota cuántas filas exportó de `ALUMNO` y de `MATRICULA`.

3. **Saca la copia del contenedor** y comprueba su tamaño:

    ```bash
    mkdir -p copias
    docker cp oracle26ai:<ruta-del-paso-1>/edugest_01.dmp ./copias/
    docker cp oracle26ai:<ruta-del-paso-1>/edugest_exp.log ./copias/
    ```

4. **Crea el usuario de pruebas** (como `SYSTEM`):

    ```sql
    CREATE USER edugest_copia IDENTIFIED BY "Copia_2026"
      DEFAULT TABLESPACE users QUOTA UNLIMITED ON users;
    GRANT CREATE SESSION, CREATE TABLE, CREATE SEQUENCE TO edugest_copia;
    ```

5. **Restaura en el esquema de pruebas:**

    ```bash
    docker exec -it oracle26ai impdp system/Oracle_2026@//localhost:1521/FREEPDB1 \
      directory=DATA_PUMP_DIR dumpfile=edugest_%U.dmp logfile=edugest_imp.log \
      remap_schema=EDUGEST:EDUGEST_COPIA
    ```

6. **Comprueba la restauración** comparando recuentos y diferencias:

    ```sql
    SELECT 'ALUMNO' tabla, (SELECT COUNT(*) FROM edugest.alumno) original,
                           (SELECT COUNT(*) FROM edugest_copia.alumno) copia FROM dual
    UNION ALL
    SELECT 'MATRICULA', (SELECT COUNT(*) FROM edugest.matricula),
                        (SELECT COUNT(*) FROM edugest_copia.matricula) FROM dual;

    SELECT * FROM edugest.alumno MINUS SELECT * FROM edugest_copia.alumno;
    ```

7. **Obtén solo la estructura.** Ejecuta `impdp` con `sqlfile=estructura.sql` (sin `remap_schema` y sin importar). Abre el fichero generado: ¿reconoces las sentencias `CREATE TABLE` del tema 2?

{{% /steps %}}

#### Comprobación

{{% comprobacion %}}
- [ ] `edugest_exp.log` termina con `successfully completed` y el volcado `.dmp` está fuera del contenedor.
- [ ] El paso 6 muestra 32 alumnos y 143 matrículas en el original y en la copia, y la consulta con `MINUS` devuelve 0 filas.
- [ ] Sabes explicar por qué se restaura primero en `EDUGEST_COPIA` y no encima de `EDUGEST`.
{{% /comprobacion %}}

#### Errores habituales

> [!WARNING]
> - `ORA-39087` o `ORA-39070`: el nombre del directorio es incorrecto o te has conectado a la CDB. Usa `FREEPDB1`.
> - `ORA-01918: user 'EDUGEST_COPIA' does not exist`: te saltaste el paso 4.
> - El `.dmp` no aparece al hacer `docker cp`: la ruta debe ser la del paso 1, **dentro del contenedor**.

#### Ampliación

Repite la exportación con `content=metadata_only` y con `tables=ALUMNO query=ALUMNO:"WHERE cod_grupo='1DAM'"`. Compara el tamaño de los tres volcados.

---

## Práctica 6.2 · Exportar datos a CSV, JSON y SQL

{{< practica num="6.2" tipo="Guiada" duracion="1 sesión" nivel="1" ra="RA6: d, e" sgbd="Oracle 26ai · SQLcl · SQL Developer" entrega="alumnado.csv + alumnado.json + alumnado_insert.sql" >}}

#### Objetivo

Exportar el mismo resultado a distintos formatos con herramientas de línea de comandos y con el asistente gráfico.

#### Desarrollo

{{% steps %}}

1. **CSV con SQLcl.** Conectado como `EDUGEST`:

    ```sql
    SET SQLFORMAT csv
    SPOOL alumnado.csv
    SELECT nia, nombre, apellidos, cod_grupo FROM alumno ORDER BY nia;
    SPOOL OFF
    ```

    Abre el fichero con un editor de texto y con una hoja de cálculo. ¿Se ven bien las tildes en los dos?

2. **JSON y sentencias `INSERT`:**

    ```sql
    SET SQLFORMAT json
    SPOOL alumnado.json
    SELECT nia, nombre, apellidos, cod_grupo FROM alumno ORDER BY nia;
    SPOOL OFF

    SET SQLFORMAT insert
    SPOOL alumnado_insert.sql
    SELECT nia, nombre, apellidos, cod_grupo FROM alumno ORDER BY nia;
    SPOOL OFF
    SET SQLFORMAT default
    ```

3. **Asistente gráfico.** En SQL Developer: clic derecho sobre la tabla `GRUPO` → *Exportar*. Elige formato *CSV*, marca *Cabecera* y guarda el fichero. Repite con formato *insert*.

4. **Compara las tres salidas** en una tabla: formato, tamaño del fichero y qué pasa con una columna que contenga una coma o un valor nulo.

{{% /steps %}}

#### Comprobación

{{% comprobacion %}}
- [ ] `alumnado.csv` tiene 33 líneas (cabecera y 32 alumnos).
- [ ] `alumnado_insert.sql` contiene 32 sentencias `INSERT`.
- [ ] Has localizado en el CSV un campo entre comillas y puedes explicar por qué.
{{% /comprobacion %}}

#### Errores habituales

> [!WARNING]
> Si el fichero se crea vacío, olvidaste cerrar con `SPOOL OFF` o ejecutaste la consulta antes de `SPOOL`. Si las tildes salen mal en la hoja de cálculo, es un problema de **codificación** al abrirlo, no de la exportación.

---

## Práctica 6.3 · Importar con SQL\*Loader y leer los errores

{{< practica num="6.3" tipo="Autónoma" duracion="1 sesión" nivel="2" ra="RA6: f, g" sgbd="Oracle 26ai · SQL*Loader" entrega="carga_alumnos.ctl + carga.log + carga.bad + informe" >}}

#### Objetivo

Cargar un fichero CSV en una tabla, localizar las filas rechazadas y explicar la causa de cada rechazo a partir del registro.

#### Enunciado

Crea la tabla de destino como `EDUGEST`:

```sql
CREATE TABLE alumno_carga (
  nia        CHAR(8)       CONSTRAINT pk_alumno_carga PRIMARY KEY,
  nombre     VARCHAR2(50)  NOT NULL,
  apellidos  VARCHAR2(80),
  cod_grupo  VARCHAR2(6)   CONSTRAINT ck_alumno_carga_grupo
             CHECK (cod_grupo IN ('1DAM','2DAM','1DAW','2DAW','1ASIR','2ASIR'))
);
```

Guarda este contenido como `alumnos_nuevos.csv` (UTF-8):

```text
nia,nombre,apellidos,cod_grupo
10460001,Lucía,Marín Soler,1ASIR
10460002,Pau,Giner Calvo,1ASIR
10460003,Aitana,Pérez Ruiz,1ASIR
10460004,Marc,"Vidal, Ferrando",1ASIR
10460002,Pablo,Giner Calvo,1ASIR
10460006,,Sempere Mira,1ASIR
10460007,Nuria,Beltrán Pons,3ASIR
10460008,Iván,Cano Lillo,1ASIR
```

1. Escribe el fichero de control `carga_alumnos.ctl` (usa `CHARACTERSET UTF8`, `OPTIONS (SKIP=1)` para saltar la cabecera, `APPEND` y los separadores adecuados).
2. Copia los dos ficheros al contenedor (`docker cp ... oracle26ai:/tmp/`) y ejecuta `sqlldr` con `docker exec -w /tmp`, indicando `log=` y `bad=`.
3. Abre el `.log` y el `.bad`. Rellena una tabla con una fila por cada registro rechazado: número de línea, código `ORA-` y causa.
4. Corrige el CSV (no la tabla) y vuelve a cargar **solo** las filas rechazadas.

{{% details title="Pista: estructura del fichero de control" %}}
Necesitas `OPTIONS`, `LOAD DATA`, `CHARACTERSET`, `INFILE`, `APPEND`, `INTO TABLE`, `FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'`, `TRAILING NULLCOLS` y la lista de columnas entre paréntesis. Consulta el ejemplo de la teoría §5.3.
{{% /details %}}

#### Comprobación

{{% comprobacion %}}
- [ ] Tras la primera carga, `SELECT COUNT(*) FROM alumno_carga;` devuelve **5** y el log indica 3 filas rechazadas.
- [ ] Has identificado una violación de clave primaria (`ORA-00001`), un valor nulo en columna obligatoria (`ORA-01400`) y una violación de `CHECK` (`ORA-02290`).
- [ ] Tras la corrección, la tabla tiene 8 filas sin duplicados.
{{% /comprobacion %}}

#### Errores habituales

> [!WARNING]
> - `SQL*Loader-350: Syntax error`: revisa comas y paréntesis del `.ctl`.
> - Tildes corruptas (`LucÃ­a`): falta `CHARACTERSET UTF8` o el CSV no está guardado en UTF-8.
> - `SQL*Loader-500: Unable to open file`: el CSV no está en la carpeta desde la que ejecutas (`-w /tmp`).

---

## Práctica 6.4 · De Oracle a PostgreSQL

{{< practica num="6.4" tipo="Guiada" duracion="1 sesión" nivel="2" ra="RA6: e, f, h" sgbd="Oracle 26ai · SQLcl · PostgreSQL 17" entrega="alumnado.csv + capturas de la verificación" >}}

#### Objetivo

Transferir información entre dos sistemas gestores distintos y comprobar que no se pierde ni se deforma.

#### Desarrollo

{{% steps %}}

1. **Exporta el alumnado desde Oracle** a CSV, con las fechas en ISO 8601:

    ```sql
    SET SQLFORMAT csv
    SPOOL alumnado.csv
    SELECT nia, nombre, apellidos, cod_grupo,
           TO_CHAR(fecha_nacimiento, 'YYYY-MM-DD') AS fecha_nacimiento
    FROM   alumno ORDER BY nia;
    SPOOL OFF
    ```

    Abre el fichero: debe tener una cabecera y 32 filas.

2. **Arranca PostgreSQL** y crea la tabla de destino. Los tipos de Oracle se **mapean** a los del destino (`VARCHAR2` → `VARCHAR`, `DATE` → `DATE`):

    ```bash
    docker run -d --name pg17 -e POSTGRES_PASSWORD=Postgres_2026 -p 5432:5432 postgres:17
    docker cp alumnado.csv pg17:/tmp/
    docker exec -it pg17 psql -U postgres
    ```

    ```sql
    CREATE TABLE alumnado (
        nia              VARCHAR(8)   PRIMARY KEY,
        nombre           VARCHAR(100) NOT NULL,
        apellidos        VARCHAR(100) NOT NULL,
        cod_grupo        VARCHAR(10),
        fecha_nacimiento DATE
    );
    ```

3. **Importa el CSV** con `\copy`:

    ```sql
    \copy alumnado FROM '/tmp/alumnado.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
    ```

4. **Verifica** en PostgreSQL y compara con Oracle:

    ```sql
    SELECT COUNT(*) FROM alumnado;
    SELECT * FROM alumnado WHERE nia = '10450037';
    SELECT cod_grupo, COUNT(*) FROM alumnado GROUP BY cod_grupo ORDER BY 1;
    SELECT pg_typeof(fecha_nacimiento) FROM alumnado LIMIT 1;
    ```

    En Oracle, `SELECT COUNT(*) FROM alumno;` y `SELECT cod_grupo, COUNT(*) FROM alumno GROUP BY cod_grupo ORDER BY 1;` deben dar los mismos números.

{{% /steps %}}

#### Comprobación

{{% comprobacion %}}
- [ ] El recuento de PostgreSQL es 32 y coincide con Oracle.
- [ ] El alumno de NIA 10450037 aparece como «Adrián Ferri Baeza», con la tilde bien.
- [ ] La fecha de nacimiento es de tipo `date` y los alumnos sin grupo tienen `cod_grupo` nulo.
{{% /comprobacion %}}

#### Errores habituales

> [!WARNING]
> Si `\copy` informa de `invalid byte sequence for encoding "UTF8"`, el fichero no está en UTF-8. Si dice `extra data after last expected column`, el CSV tiene más columnas que la tabla de destino: revisa que la `SELECT` y el `CREATE TABLE` coincidan.

---

## Práctica 6.5 · Reto: plan de copias y simulacro de desastre

{{< practica num="6.5" tipo="Reto" duracion="2 sesiones" nivel="3" ra="RA6: a, b, c, g" sgbd="Oracle 26ai · Data Pump · Docker" entrega="plan_copias.md + copia_edugest.sh + registro del simulacro" >}}

#### Enunciado

El instituto te pide que protejas EduGest. Tienes que entregar:

1. **Un plan de copias** (una página) con: qué se copia, tipo de copia, frecuencia, dónde se guarda (regla 3-2-1), quién puede restaurar, cuánto se conserva, RPO y RTO justificados para la secretaría durante el periodo de evaluaciones.
2. **Un guion** `copia_edugest.sh` que exporte el esquema con Data Pump, ponga la fecha en el nombre del fichero, saque el `.dmp` y el `.log` del contenedor, **compruebe** que el log contiene `successfully completed` y avise si no es así.
3. **Un simulacro de desastre** sobre `EDUGEST_COPIA`: toma una copia, borra datos con un `DELETE` sin `WHERE`, restáuralos con `impdp` (`table_exists_action=REPLACE`) y demuestra con recuentos que has vuelto al estado anterior. Registra la hora de inicio y de fin: ese es tu RTO real.

{{% details title="Pista: comprobar el log en un guion" %}}
`grep -q "successfully completed" edugest_exp.log || echo "ERROR: la copia ha fallado"`.
{{% /details %}}

#### Comprobación

{{% comprobacion %}}
- [ ] El plan cumple 3-2-1 y justifica el RPO.
- [ ] El guion genera un fichero con fecha en el nombre y detecta un fallo (pruébalo con un usuario o directorio inexistente).
- [ ] El registro del simulacro incluye los recuentos antes, tras el desastre y tras la restauración.
{{% /comprobacion %}}

---

## Proyecto EduGest · Tema 6: seguridad de la información

{{< practica num="EduGest-6" tipo="Proyecto" duracion="Trabajo transversal (1 semana)" nivel="3" ra="RA6: a, b, c, d, e, f, g, h" sgbd="Oracle 26ai · PostgreSQL 17" entrega="edugest/10_seguridad/ + docs/10-seguridad.md" >}}

#### Enunciado

1. **Procedimiento de copia y restauración** de Oracle, con los comandos exactos, los usuarios necesarios y la ubicación de los ficheros.
2. **Guion de exportación** del listado de alumnado de un grupo en CSV y JSON.
3. **Guion de importación** de un fichero de alumnado nuevo con control de rechazados y un informe de la carga.
4. **Transferencia** del alumnado de EduGest a PostgreSQL con verificación de recuentos.
5. **Tabla de errores** con al menos cinco mensajes que hayas obtenido, su causa y su solución.

#### Comprobación

{{% comprobacion %}}
- [ ] Un compañero puede restaurar EduGest siguiendo **solo** tu documento.
- [ ] Cada transferencia tiene su comprobación de recuentos.
- [ ] Las copias que salen del equipo están identificadas con fecha y se indica cómo cifrarlas.
{{% /comprobacion %}}
