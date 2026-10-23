---
title: "Copias de seguridad, importación y exportación"
weight: 1
bookToc: true
---

# UD06 · Copias de seguridad, importación y exportación de datos

## Resumen del tema

Hasta ahora hemos construido, consultado y programado una base de datos. Falta la pregunta que más se acuerda el día que algo falla: **¿qué pasa si perdemos los datos?** Un disco que se estropea, un `DELETE` sin `WHERE`, un ransomware o un contenedor borrado por error tienen el mismo efecto: la información desaparece. La única defensa es haber hecho **copias de seguridad** y **haber comprobado que se pueden restaurar**.

Esta parte de la UD06 es la que cubre el **RA6** del módulo: *ejecutar tareas de aseguramiento de la información, aplicando mecanismos de salvaguarda y transferencia*. Trabajaremos sobre EduGest con las herramientas de **Oracle AI Database 26ai Free** (Data Pump, SQL\*Loader, SQLcl, SQL Developer) y con las de **MongoDB 8.0** (`mongodump`, `mongorestore`, `mongoexport`, `mongoimport`).

{{< ra "RA6:a,b,c,d,e,f,g,h" >}}

### Objetivos de aprendizaje

Al terminar esta parte serás capaz de:

- Distinguir los tipos de copia de seguridad (lógica y física, completa, incremental y diferencial, en frío y en caliente) y elegir una estrategia según el tiempo de recuperación y la pérdida de datos admisibles (RA6.a).
- Hacer y restaurar una copia lógica de un esquema de Oracle con Data Pump (RA6.b, RA6.c).
- Hacer y restaurar una copia de una base de datos de MongoDB con `mongodump` y `mongorestore` (RA6.b, RA6.c).
- Identificar las herramientas de importación y exportación de cada gestor (RA6.d).
- Exportar datos a CSV, JSON y scripts SQL (RA6.e) e importar ficheros con SQL\*Loader, SQL Developer y `mongoimport` (RA6.f).
- Leer los mensajes de error y los ficheros de registro (`.log`, `.bad`) para localizar la causa de un fallo (RA6.g).
- Transferir información entre dos sistemas gestores distintos (Oracle y MongoDB) cuidando tipos, fechas, nulos y codificación (RA6.h).

### Temporalización

La unidad ocupa **18 horas de aula** (6 de teoría y 12 de práctica).

{{< sesiones unidad="UD06" horas="18" >}}
items:
  - {h: 1, tipo: T, t: "Copias de seguridad: tipos, estrategia y herramientas", ref: "§1 y §2"}
  - {h: 1, tipo: T, t: "Copia lógica con Data Pump y copias en MongoDB", ref: "§3 y §4"}
  - {h: 2, tipo: P, t: "Copia lógica de EduGest y restauración", ref: "Práctica 6.1"}
  - {h: 1, tipo: T, t: "Importar y exportar datos", ref: "§5"}
  - {h: 1, tipo: P, t: "Exportar datos a CSV, JSON y SQL", ref: "Práctica 6.2"}
  - {h: 1, tipo: P, t: "Importar con SQL*Loader y leer los errores", ref: "Práctica 6.3"}
  - {h: 1, tipo: T, t: "Transferencia entre gestores y registros de error", ref: "§6 y §7"}
  - {h: 2, tipo: P, t: "De Oracle a MongoDB y proyecto de seguridad", ref: "Práctica 6.4 · Proyecto EduGest · UD06b"}
  - {h: 2, tipo: T, t: "NoSQL, BASE y CAP, tipos de bases de datos, MongoDB y CRUD", ref: "§1 a §5 · traductor SQL ↔ MongoDB"}
  - {h: 2, tipo: P, t: "Puesta en marcha de MongoDB y CRUD sobre los expedientes", ref: "Prácticas 6.6 y 6.7"}
  - {h: 2, tipo: P, t: "Consultas, agregaciones y modelado documental", ref: "Prácticas 6.8 a 6.10"}
  - {h: 1, tipo: P, t: "Otros modelos NoSQL y proyecto del expediente documental", ref: "Prácticas 6.11 y 6.12 · Proyecto EduGest · UD06"}
autonomo:
  - "Reto 6.5 (plan de copias y simulacro de desastre)"
  - "Teoría NoSQL §6 a §14 (subdocumentos, agregaciones, modelado, índices, seguridad y SQL frente a NoSQL)"
  - "Ampliaciones de las prácticas 6.1 a 6.4 y 6.6 a 6.12, y autoevaluación"
{{< /sesiones >}}

> [!IMPORTANT]
> Una copia de seguridad **que nunca se ha restaurado no es una copia: es una esperanza**. En cada práctica de esta parte hay un paso de *restauración y comprobación*. No te lo saltes.

---

## 1. Por qué y cómo se hacen copias

### 1.1 Qué puede salir mal

| Causa | Ejemplo en EduGest | Qué lo evita |
|---|---|---|
| Error humano | Un `DELETE FROM matricula;` sin `WHERE` y con `COMMIT` | Copia reciente; auditoría; permisos mínimos |
| Fallo de hardware | El disco donde está el volumen `oracle-data` se estropea | Copia en **otro** dispositivo |
| Fallo de software | Una actualización corrompe el contenedor | Copia anterior a la actualización |
| Ataque | Ransomware que cifra el servidor | Copia desconectada de la red |
| Desastre | Incendio o robo del equipo | Copia fuera del edificio o en la nube |

### 1.2 Dos números que mandan: RPO y RTO

- **RPO** (*Recovery Point Objective*): cuántos datos podemos permitirnos perder, medido en tiempo. Si hacemos copia cada noche, el RPO es de hasta 24 horas.
- **RTO** (*Recovery Time Objective*): cuánto tiempo podemos estar sin servicio mientras restauramos.

> [!TIP]
> Antes de elegir herramientas, pregunta al "cliente" cuánto cuesta una hora parado y cuánta información puede perder. Una secretaría que graba notas durante la evaluación necesita un RPO mucho menor que el repositorio de programaciones.

### 1.3 Clasificación de las copias

| Criterio | Tipos | Idea |
|---|---|---|
| **Qué se copia** | Lógica / Física | La **lógica** guarda los objetos y los datos como sentencias o filas (`CREATE TABLE`, `INSERT`...). La **física** copia los ficheros de la base de datos tal cual. |
| **Cuánto se copia** | Completa / Incremental / Diferencial | La **completa** copia todo. La **incremental** copia lo cambiado desde la última copia (de cualquier tipo). La **diferencial** copia lo cambiado desde la última completa. |
| **Cómo está el servicio** | En frío / En caliente | En **frío** la base de datos está parada. En **caliente** sigue funcionando mientras se copia. |

Para restaurar una incremental necesitas la completa y **todas** las incrementales intermedias. Para una diferencial, la completa y la última diferencial. Por eso las incrementales ocupan menos pero tardan más en restaurarse.

### 1.4 La regla 3-2-1

> [!IMPORTANT]
> **3** copias de los datos, en **2** tipos de soporte distintos, con **1** copia fuera del lugar original. Y una cuarta regla de sentido común: **cifra** las copias que salgan de la organización, porque contienen datos personales.

## 2. Herramientas de copia

| Gestor | Herramienta | Tipo | Cuándo usarla |
|---|---|---|---|
| Oracle | **Data Pump** (`expdp` / `impdp`) | Lógica | Copiar o mover un esquema o unas tablas; trabajar en equipos distintos |
| Oracle | **RMAN** (*Recovery Manager*) | Física | Copias completas e incrementales de toda la base de datos |
| Oracle | Copia en frío del volumen | Física | Entornos de clase: parar el contenedor y copiar el volumen |
| Oracle | **SQL Developer** (*Herramientas → Exportación de base de datos*) | Lógica (asistente) | Generar scripts de DDL y datos con interfaz gráfica |
| MongoDB | **`mongodump` / `mongorestore`** | Lógica (BSON) | Copia y restauración de bases de datos o colecciones |

> [!NOTE]
> **RMAN** es la herramienta profesional de copia física de Oracle (`rman target /` y órdenes como `BACKUP DATABASE`). Funciona de forma muy distinta según la base de datos esté en modo `ARCHIVELOG` o `NOARCHIVELOG`: sin archivado solo permite copias con la base de datos montada pero cerrada. En el contenedor de clase no la usaremos; trabajaremos con **Data Pump**, que es lógica y funciona con la base de datos abierta.

### 2.1 Copia en frío del contenedor

Es la copia más simple y ayuda a entender qué es una copia física: se **para** el servicio para que los ficheros estén consistentes y se copian.

```bash
docker stop oracle26ai
docker run --rm -v oracle-data:/datos -v "$PWD":/copia busybox \
       tar czf /copia/oracle-data_$(date +%Y%m%d).tgz -C /datos .
docker start oracle26ai
```

{{< sgbd "Docker" >}} El volumen `oracle-data` se monta en un contenedor auxiliar que lo comprime en la carpeta actual. Para restaurar se hace la operación inversa sobre un volumen vacío. Desventaja: el servicio queda **parado** mientras se copia.

## 3. Copia lógica con Data Pump (Oracle)

**Data Pump** se compone de dos programas que se ejecutan en el **servidor**: `expdp` (exportar) e `impdp` (importar). Escriben en un **directorio** de Oracle (un objeto `DIRECTORY` que apunta a una carpeta del servidor), y generan un fichero de volcado `.dmp` y un fichero de registro `.log`.

### 3.1 Preparar el directorio

{{< sgbd "Oracle 26ai" >}} Conectado como `SYSTEM` a `FREEPDB1`:

```sql
SELECT directory_name, directory_path
FROM   dba_directories
WHERE  directory_name = 'DATA_PUMP_DIR';
```

`DATA_PUMP_DIR` es el directorio por defecto de Data Pump. Anota la ruta: ahí aparecerán los ficheros. Si no existiera, créalo con `CREATE DIRECTORY dir_copias AS '/ruta/del/servidor';` (la carpeta debe existir y ser escribible por el usuario `oracle`).

### 3.2 Exportar un esquema

```bash
docker exec -it oracle26ai expdp system/Oracle_2026@//localhost:1521/FREEPDB1 \
  schemas=EDUGEST directory=DATA_PUMP_DIR \
  dumpfile=edugest_%U.dmp logfile=edugest_exp.log
```

Cada parámetro tiene una razón:

| Parámetro | Significado |
|---|---|
| `schemas=EDUGEST` | Modo esquema: exporta todos los objetos del usuario `EDUGEST` |
| `directory=` | Objeto `DIRECTORY` donde se escriben los ficheros |
| `dumpfile=edugest_%U.dmp` | Nombre del volcado; `%U` genera `01`, `02`... si hay varios ficheros |
| `logfile=` | Fichero con el registro de la operación |
| `content=metadata_only` | (opcional) Solo estructuras, sin datos |
| `tables=ALUMNO,MATRICULA` | (opcional) Modo tabla en lugar de esquema |
| `query=ALUMNO:"WHERE cod_grupo='1DAM'"` | (opcional) Exportar solo algunas filas |
| `parfile=copia.par` | (opcional) Guardar los parámetros en un fichero |

Al final debe aparecer una línea como `Job "SYSTEM"."SYS_EXPORT_SCHEMA_01" successfully completed`. Si aparece `completed with N error(s)`, **hay que leer el log**.

### 3.3 Sacar la copia del contenedor

La copia no sirve si está dentro del mismo disco que la base de datos que protege:

```bash
docker cp oracle26ai:/opt/oracle/admin/FREE/dpdump/<ruta-anotada>/edugest_01.dmp ./copias/
docker cp oracle26ai:/opt/oracle/admin/FREE/dpdump/<ruta-anotada>/edugest_exp.log ./copias/
```

### 3.4 Importar y restaurar

`impdp` es el camino inverso. La opción `remap_schema` permite restaurar en otro usuario, que es la forma segura de **probar** una copia sin tocar los datos reales:

```sql
-- Como SYSTEM: usuario de prueba para la restauración
CREATE USER edugest_copia IDENTIFIED BY "Copia_2026"
  DEFAULT TABLESPACE users QUOTA UNLIMITED ON users;
GRANT CREATE SESSION, CREATE TABLE, CREATE SEQUENCE, CREATE VIEW,
      CREATE PROCEDURE, CREATE TRIGGER TO edugest_copia;
```

```bash
docker exec -it oracle26ai impdp system/Oracle_2026@//localhost:1521/FREEPDB1 \
  directory=DATA_PUMP_DIR dumpfile=edugest_%U.dmp logfile=edugest_imp.log \
  remap_schema=EDUGEST:EDUGEST_COPIA
```

| Opción útil | Efecto |
|---|---|
| `table_exists_action=REPLACE` | Si la tabla ya existe: `SKIP` (por defecto), `APPEND`, `TRUNCATE` o `REPLACE` |
| `remap_tablespace=` | Cambia el espacio de tablas de destino |
| `include=TABLE:"IN ('ALUMNO')"` | Importar solo algunos objetos |
| `sqlfile=estructura.sql` | No importa: escribe en un fichero el DDL que ejecutaría |

### 3.5 Comprobar la restauración

Restaurar no termina cuando `impdp` dice *completed*. Se comprueba que los datos coinciden:

```sql
SELECT 'ALUMNO' AS tabla, COUNT(*) FROM edugest.alumno
UNION ALL SELECT 'ALUMNO_COPIA', COUNT(*) FROM edugest_copia.alumno
UNION ALL SELECT 'MATRICULA', COUNT(*) FROM edugest.matricula
UNION ALL SELECT 'MATRICULA_COPIA', COUNT(*) FROM edugest_copia.matricula;

-- Filas que están en el original y no en la copia (debe devolver 0 filas)
SELECT * FROM edugest.alumno
MINUS
SELECT * FROM edugest_copia.alumno;
```

## 4. Copia y restauración en MongoDB

`mongodump` genera ficheros **BSON** (formato binario de MongoDB) y `mongorestore` los carga.

```bash
docker exec mongo8 mongodump --db=edugest --out=/tmp/copia_mongo
docker cp mongo8:/tmp/copia_mongo ./copias/mongo

# Restaurar en una base de datos de pruebas
docker exec mongo8 mongorestore --nsFrom='edugest.*' --nsTo='edugest_copia.*' /tmp/copia_mongo
```

> [!WARNING]
> Estas herramientas forman parte de las *MongoDB Database Tools*. Comprueba que están en tu imagen con `docker exec mongo8 mongodump --version`. Si no, instálalas desde la web de MongoDB y ejecútalas desde tu equipo con `--uri="mongodb://localhost:27017"`.

Para comprobar: `db.expedientes.countDocuments()` en `edugest` y en `edugest_copia` debe dar el mismo número.

## 5. Importar y exportar datos

Una copia sirve para restaurar el **mismo** gestor. La **exportación** y la **importación** de datos sirve para intercambiar información con otras aplicaciones y con otros gestores, usando formatos de texto.

### 5.1 Formatos

| Formato | Ventajas | Cuidado con |
|---|---|---|
| **CSV** | Universal; lo abre cualquier hoja de cálculo | Separador (`,` o `;`), comillas, saltos de línea dentro de campos, fechas, decimales (`.` o `,`) |
| **JSON** | Conserva la estructura anidada; natural para MongoDB y APIs | Los tipos son pocos: las fechas son texto; los `NULL` se escriben `null` o se omiten |
| **Script SQL** | Se ejecuta en el mismo gestor o en otro parecido | Dialecto propio de cada gestor |
| **XML** | Intercambio entre sistemas empresariales | Verboso |

### 5.2 Exportar en Oracle

Con **SQLcl** o con la consola de SQL Developer se pueden cambiar los formatos de salida de una consulta:

```sql
SET SQLFORMAT csv
SPOOL alumnado.csv
SELECT nia, nombre, apellidos, cod_grupo FROM alumno ORDER BY nia;
SPOOL OFF
SET SQLFORMAT default
```

{{< sgbd "SQLcl" >}} `SQLFORMAT` admite `csv`, `json`, `xml`, `insert` (genera sentencias `INSERT`) y otros. `SPOOL` escribe el resultado en un fichero. Con el **asistente gráfico** de SQL Developer: clic derecho sobre una tabla → *Exportar*, y se elige formato, columnas y destino.

También se puede generar JSON a partir de tablas con las funciones SQL/JSON de Oracle (`JSON_OBJECT`, `JSON_ARRAYAGG`), útil para llevar los datos a MongoDB.

### 5.3 Importar en Oracle con SQL\*Loader

**SQL\*Loader** (`sqlldr`) carga ficheros de texto en tablas. Necesita un **fichero de control** que dice dónde están los datos y cómo mapearlos:

```text
-- carga_alumnos.ctl
LOAD DATA
CHARACTERSET UTF8
INFILE 'alumnos_nuevos.csv'
APPEND
INTO TABLE alumno_carga
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(nia, nombre, apellidos, cod_grupo)
```

```bash
sqlldr userid=edugest/Edugest_2026@//localhost:1521/FREEPDB1 \
       control=carga_alumnos.ctl log=carga.log bad=carga.bad
```

| Fichero | Contenido |
|---|---|
| `.log` | Resumen: filas leídas, cargadas, rechazadas, errores |
| `.bad` | Las filas **rechazadas** por la base de datos (por ejemplo, violan una restricción) |
| `.dsc` | (si se pide con `discard=`) Filas descartadas por una condición `WHEN` |

`APPEND` añade filas; `TRUNCATE` vacía la tabla antes de cargar; `INSERT` exige que la tabla esté vacía.

> [!NOTE]
> En clase usaremos también el **asistente de importación** de SQL Developer (clic derecho sobre la tabla → *Importar datos*), que genera el mismo tipo de carga sin escribir el fichero de control. Los asistentes ayudan, pero hay que entender qué hacen: se necesita saber leer sus mensajes.

### 5.4 Importar y exportar en MongoDB

```bash
# Exportar una colección a JSON (un documento por línea)
docker exec mongo8 mongoexport --db=edugest --collection=expedientes --out=/tmp/expedientes.json

# Importar un fichero JSON (si es un array, añade --jsonArray)
docker exec mongo8 mongoimport --db=edugest_copia --collection=expedientes --file=/tmp/expedientes.json
```

Para CSV: `mongoexport --type=csv --fields=nia,nombre,grupo ...` y `mongoimport --type=csv --headerline ...`.

## 6. Transferir información entre gestores

Pasar datos de Oracle a MongoDB (o a PostgreSQL, o a una hoja de cálculo) es una tarea habitual. El proceso siempre tiene los mismos pasos:

1. **Origen:** definir qué datos se transfieren (consulta).
2. **Transformación:** adaptar tipos, fechas, nulos y estructura al destino.
3. **Exportación** a un formato intermedio (CSV o JSON).
4. **Importación** en el destino.
5. **Verificación:** comparar recuentos y revisar una muestra.

| Aspecto | Qué puede fallar | Cómo evitarlo |
|---|---|---|
| **Codificación** | `Ramón` se convierte en `RamÃ³n` | Exportar e importar en **UTF-8** |
| **Fechas** | `14/03/2007` se interpreta como `03/14/...` | Usar formato ISO 8601: `2007-03-14` |
| **Decimales** | `4,75` no es un número en CSV con coma como separador | Usar punto decimal o separador `;` |
| **Nulos** | Una cadena vacía no es lo mismo que `NULL` | Decidir cómo se representan y comprobar al importar |
| **Estructura** | Una relación 1:N se convierte en un array incrustado | Diseñar el documento antes (UD06) |
| **Claves ajenas** | El destino no valida la integridad | Validar con consultas después de importar |

## 7. Mensajes de error y ficheros de registro

Aprender a leer los registros es la diferencia entre resolver un fallo en cinco minutos o en cinco horas.

### 7.1 Método

1. **Lee el log completo**, no solo la última línea.
2. Busca el **primer** error: los siguientes suelen ser consecuencia.
3. Anota el **código** (`ORA-39002`, `SQL*Loader-500`...) y el texto.
4. Busca el código en la documentación oficial ([Oracle Error Help](https://docs.oracle.com/en/error-help/db/)).
5. Corrige **una** cosa y repite.

### 7.2 Errores frecuentes en copias e importaciones

| Mensaje | Causa habitual | Solución |
|---|---|---|
| `ORA-39002: invalid operation` / `ORA-39070: Unable to open the log file` | El directorio no existe o el usuario no puede escribir | Comprobar `DBA_DIRECTORIES` y permisos |
| `ORA-39087: directory name DATA_PUMP_DIR is invalid` | El objeto `DIRECTORY` no existe en la PDB | Crearlo o conectarse a `FREEPDB1` |
| `ORA-31655: no data or metadata objects selected for job` | El filtro (`schemas`, `include`) no coincide con nada | Revisar mayúsculas y nombres |
| `ORA-31684: Object type USER:"EDUGEST_COPIA" already exists` | El usuario de destino ya existe | Es un aviso; se puede ignorar si es el esperado |
| `ORA-39151: Table "X"."Y" exists. All dependent metadata and data will be skipped` | La tabla ya existe en el destino | `table_exists_action=REPLACE` o `TRUNCATE` |
| `ORA-00001: unique constraint ... violated` (en `sqlldr`) | Clave duplicada en el fichero | Revisar el `.bad` |
| `ORA-01722: invalid number` | Un texto donde se esperaba un número | Revisar separadores y decimales |
| `SQL*Loader-350: Syntax error` | Error en el fichero `.ctl` | Revisar comas, paréntesis y nombre de columnas |
| `mongorestore: ... E11000 duplicate key error` | El documento ya existe en el destino | Usar `--drop` o restaurar en otra base de datos |

### 7.3 Otros ficheros de registro

- **Alert log** de Oracle (`alert_FREE.log`): eventos de la instancia. En el contenedor, `docker logs oracle26ai` muestra el arranque.
- **Registro de Docker** de MongoDB: `docker logs mongo8`.
- **Historial de trabajos de Data Pump**: `SELECT owner_name, job_name, state FROM dba_datapump_jobs;`

## 8. Errores frecuentes

| Error | Consecuencia | Prevención |
|---|---|---|
| Guardar la copia en el mismo disco/contenedor | Se pierde todo a la vez | Regla 3-2-1 |
| No probar nunca la restauración | La copia no sirve cuando hace falta | Simulacro periódico en otro esquema |
| Exportar sin `UTF-8` | Caracteres corruptos | Fijar la codificación |
| Dejar copias sin cifrar en un USB | Fuga de datos personales (RGPD) | Cifrar y limitar accesos |
| Restaurar encima de los datos reales | Se pierde lo ocurrido desde la copia | Restaurar primero en otro esquema |
| No registrar qué copia es cuál | No se sabe cuál restaurar | Nombres con fecha y documentación |

## 9. Buenas prácticas

- Automatiza las copias (un guion programado) y **revisa los logs**.
- Nombra los ficheros con fecha y contenido: `edugest_20271105_completa.dmp`.
- Define quién puede hacer y quién puede restaurar copias (**mínimo privilegio**).
- Documenta el procedimiento de restauración paso a paso y pruébalo.
- Conserva varias generaciones de copias, no solo la última.

## 10. Resumen

- Una copia se elige según el **RPO** y el **RTO**; la regla **3-2-1** guía dónde se guarda.
- **Data Pump** hace copias lógicas de esquemas de Oracle; **RMAN** hace copias físicas.
- **`mongodump` / `mongorestore`** hacen lo mismo en MongoDB.
- Importar y exportar usa **CSV**, **JSON** o **SQL**: cuida codificación, fechas, decimales y nulos.
- **SQL\*Loader** carga ficheros con un fichero de control y genera `.log` y `.bad`.
- Transferir entre gestores = exportar → transformar → importar → **verificar**.
- Los **logs** dicen la causa: lee el primer error.

## 11. Autoevaluación

{{< quiz >}}
- q: "Haces una copia completa el domingo y una incremental cada noche. El jueves se pierde el servidor. ¿Qué necesitas para restaurar?"
  options: ["Solo la copia del miércoles", "La completa del domingo y todas las incrementales hasta el miércoles", "Solo la completa del domingo", "Solo la incremental más reciente"]
  answer: 1
  explain: "Cada incremental guarda los cambios desde la copia anterior, así que se aplican todas en orden sobre la completa."
- q: "Si el RPO de una aplicación es de 1 hora, ¿cuál de estas estrategias sirve?"
  options: ["Una copia completa cada noche", "Una copia semanal", "Copias frecuentes (al menos cada hora) o archivado continuo", "Ninguna, el RPO no afecta a la estrategia"]
  answer: 2
  explain: "El RPO es la pérdida de datos admisible. Con 1 hora hay que copiar, como mínimo, cada hora."
- q: "¿Qué hace `impdp ... remap_schema=EDUGEST:EDUGEST_COPIA`?"
  options: ["Borra EDUGEST y crea EDUGEST_COPIA", "Importa los objetos del volcado en el esquema EDUGEST_COPIA en lugar de en EDUGEST", "Cambia la contraseña del usuario", "Exporta EDUGEST_COPIA"]
  answer: 1
  explain: "Permite restaurar en otro usuario, que es la forma segura de probar una copia sin tocar los datos reales."
- q: "Tras una carga con SQL*Loader, ¿dónde miras las filas que la base de datos rechazó?"
  options: ["En el fichero `.log` solamente", "En el fichero `.bad`", "En el alert log", "En la tabla de destino"]
  answer: 1
  explain: "El `.bad` contiene las filas rechazadas; el `.log` explica por qué."
- q: "Exportas un CSV desde Oracle y al importarlo en otro gestor `Ramón` aparece como `RamÃ³n`. ¿Cuál es la causa más probable?"
  options: ["Un error de clave primaria", "Una diferencia de codificación (UTF-8 frente a otra)", "Un problema de RPO", "Falta de privilegios"]
  answer: 1
  explain: "Es el síntoma típico de leer un fichero UTF-8 como si fuera otra codificación."
- q: "¿Qué copia es **física**?"
  options: ["Un volcado `.dmp` de Data Pump", "Un `mongodump`", "Copiar el volumen de datos con el servicio parado", "Un CSV exportado"]
  answer: 2
  explain: "Una copia física copia los ficheros de la base de datos; las otras son lógicas (objetos y datos)."
{{< /quiz >}}

## Referencias

- [Oracle AI Database 26ai: Utilities, *Oracle Data Pump*](https://docs.oracle.com/en/database/oracle/oracle-database/26/sutil/) — `expdp`, `impdp` y sus parámetros.
- [Oracle AI Database 26ai: Utilities, *SQL\*Loader*](https://docs.oracle.com/en/database/oracle/oracle-database/26/sutil/) — fichero de control, `.log` y `.bad`.
- [Oracle AI Database 26ai: Backup and Recovery User's Guide](https://docs.oracle.com/en/database/oracle/oracle-database/26/bradv/) — RMAN y estrategias de copia.
- [Oracle SQLcl: documentación](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/) — `SET SQLFORMAT`, `SPOOL`.
- [Oracle Database Error Help](https://docs.oracle.com/en/error-help/db/).
- [MongoDB Database Tools](https://www.mongodb.com/docs/database-tools/) — `mongodump`, `mongorestore`, `mongoexport` y `mongoimport`.
- [Real Decreto 1629/2009, de 30 de octubre (módulo profesional 0372 Gestión de bases de datos)](https://www.boe.es/eli/es/rd/2009/10/30/1629).
