---
title: "Manipulación de datos y transacciones - Prácticas"
weight: 2
bookToc: true
---

# UD08 · Prácticas

{{< ra "RA4:a,b,c,d,e,f,g,h" "RA6:f" >}}

| Práctica | Tipo | Nivel | CE principales |
|---|---|---|---|
| [8.1 Altas, cambios y bajas en EduGest](#práctica-81--altas-cambios-y-bajas-en-edugest) | Guiada | ●○○ | RA4.a, RA4.b |
| [8.2 Copias, históricos e INSERT … SELECT](#práctica-82--copias-históricos-e-insert--select) | Guiada | ●●○ | RA4.c |
| [8.3 Modificaciones con subconsultas](#práctica-83--modificaciones-con-subconsultas) | Autónoma | ●●○ | RA4.b, RA4.c, RA4.h |
| [8.4 Laboratorio de transacciones](#práctica-84--laboratorio-de-transacciones) | Guiada | ●●○ | RA4.e, RA4.f |
| [8.5 Dos sesiones, un dato: concurrencia y bloqueos](#práctica-85--dos-sesiones-un-dato-concurrencia-y-bloqueos) | Guiada | ●●● | RA4.g, RA4.h |
| [8.6 Carga de notas con MERGE](#práctica-86--carga-de-notas-con-merge) | Autónoma | ●●○ | RA4.b, RA4.c |
| [8.7 Reto: guion de promoción de curso](#práctica-87--reto-guion-de-promoción-de-curso) | Reto | ●●● | RA4.d, RA4.e, RA4.f, RA4.h |
| [Proyecto EduGest · UD08](#proyecto-edugest--ud08-guiones-de-mantenimiento) | Proyecto | ●●● | RA4 completo |

> [!IMPORTANT]
> Antes de **cada** práctica, restaura EduGest ejecutando los scripts 01 y 02 del [proyecto](/guia/proyecto-edugest#4-scripts-descargables). Los números de filas afectadas que se indican suponen los datos originales.

---

## Práctica 8.1 · Altas, cambios y bajas en EduGest

{{< practica num="8.1" tipo="Guiada" duracion="2 sesiones" nivel="1" ra="RA4: a, b" sgbd="Oracle 26ai · SQL Developer" entrega="p8_1.sql + capturas de la rejilla" >}}

#### Objetivo

Insertar, modificar y borrar datos con SQL y con la herramienta gráfica, comprobando en cada paso el efecto de las restricciones y la necesidad de confirmar los cambios.

#### Desarrollo

{{% steps %}}

1. **Alta de una alumna.** Fíjate en que no indicamos `id_alumno`:

    ```sql
    INSERT INTO alumno (nia, dni, nombre, apellidos, fecha_nacimiento, email, localidad, cod_grupo)
    VALUES ('10452001', '48123456J', 'Marina', 'López Ortega', DATE '2007-03-14',
            'marinalopez@alu.edugest.es', 'Alicante', '1DAM');

    SELECT id_alumno, nombre, apellidos FROM alumno WHERE nia = '10452001';
    ```

    El identificador generado debe ser **1001**, porque la columna identidad empieza en ese valor.

2. **Comprueba el aislamiento.** Abre una **segunda conexión** (otra hoja de trabajo con *Nueva sesión*, `Ctrl+Mayús+N`, o SQLcl) y busca a Marina. **No aparece**: el cambio no está confirmado. Vuelve a la primera sesión y ejecuta `COMMIT;`. Repite la consulta en la segunda: ahora sí aparece.

3. **Matricúlala** en Bases de datos de DAM para 2026-27:

    ```sql
    INSERT INTO matricula (id_alumno, id_modulo, curso_academico, fecha_matricula)
    VALUES (1001, (SELECT id_modulo FROM modulo WHERE codigo = '0484' AND cod_ciclo = 'DAM'),
            '2026-27', DATE '2026-09-10');
    ```

    ¿Qué valor ha tomado `convocatoria`? ¿Y `nota_final`? ¿Por qué?

4. **Prueba las restricciones** con estas inserciones incorrectas y anota el error de cada una:

    ```sql
    -- a) Matrícula duplicada (mismo alumno, módulo y curso)
    INSERT INTO matricula (id_alumno, id_modulo, curso_academico) VALUES (1001, 2, '2026-27');
    -- b) Curso académico con formato incorrecto
    INSERT INTO matricula (id_alumno, id_modulo, curso_academico) VALUES (1001, 3, '2026/27');
    -- c) Nota fuera de rango
    UPDATE matricula SET nota_final = 11 WHERE id_alumno = 1001;
    ```

5. **Modifica** el teléfono de Marina y el grupo de los tres alumnos sin grupo:

    ```sql
    UPDATE alumno SET telefono = '612345678' WHERE id_alumno = 1001;     -- 1 fila
    SELECT id_alumno, nombre FROM alumno WHERE cod_grupo IS NULL;       -- comprobar antes: 3 filas
    UPDATE alumno SET cod_grupo = '1DAW' WHERE cod_grupo IS NULL;       -- 3 filas
    ```

6. **Edita con la rejilla.** Abre la tabla `ALUMNO` → pestaña *Datos*, cambia la localidad de Marina a «Elche» y pulsa *Confirmar* (`F11`). Abre el *Log de sentencias* (*Ver → Log*) y observa el `UPDATE` que ha generado la herramienta.

7. **Borra** a Marina. ¿Qué pasa con su matrícula? Consulta antes las claves ajenas en `USER_CONSTRAINTS`:

    ```sql
    DELETE FROM alumno WHERE id_alumno = 1001;
    SELECT COUNT(*) FROM matricula WHERE id_alumno = 1001;   -- 0: borrada en cascada
    COMMIT;
    ```

{{% /steps %}}

#### Comprobación

{{% comprobacion %}}
- [ ] El paso 4 produce ORA-00001 (`UQ_MATRICULA`), ORA-02290 (`CK_MATRICULA_CURSO`) y ORA-02290 (`CK_MATRICULA_NOTA`).
- [ ] La matrícula del paso 3 tiene `convocatoria = 1` (valor por defecto) y `nota_final` a `NULL`.
- [ ] Tras el paso 7, `SELECT COUNT(*) FROM alumno;` devuelve 32.
{{% /comprobacion %}}

#### Errores habituales

> [!WARNING]
> - Si la segunda sesión **se queda colgada** en el paso 5 o 6, es que intenta modificar una fila bloqueada por la primera sesión, que aún no ha hecho `COMMIT`. Lo estudiarás en la práctica 8.5.
> - Cerrar SQL Developer con cambios pendientes muestra un aviso para confirmarlos o deshacerlos. **Lee el aviso.**

---

## Práctica 8.2 · Copias, históricos e INSERT … SELECT

{{< practica num="8.2" tipo="Guiada" duracion="1 sesión" nivel="2" ra="RA4: c" sgbd="Oracle 26ai · EDUGEST" entrega="p8_2.sql" >}}

#### Objetivo

Guardar en tablas el resultado de consultas: copias de seguridad rápidas, tablas de histórico y tablas de resumen.

#### Desarrollo

{{% steps %}}

1. **Copia de seguridad con CTAS** antes de un cambio delicado:

    ```sql
    CREATE TABLE bak_matricula AS SELECT * FROM matricula;
    SELECT COUNT(*) FROM bak_matricula;     -- 143
    ```

    Compara las restricciones de `MATRICULA` y de `BAK_MATRICULA` en `USER_CONSTRAINTS`. ¿Cuáles se han copiado?

2. **Tabla de histórico** con su propio diseño y carga con `INSERT ... SELECT`:

    ```sql
    CREATE TABLE historico_nota (
        curso_academico  CHAR(7),
        nia              CHAR(8),
        alumno           VARCHAR2(130),
        cod_ciclo        VARCHAR2(5),
        cod_modulo       CHAR(4),
        nota_final       NUMBER(4,2),
        fecha_archivo    DATE DEFAULT SYSDATE,
        CONSTRAINT pk_historico_nota PRIMARY KEY (curso_academico, nia, cod_ciclo, cod_modulo)
    );

    INSERT INTO historico_nota (curso_academico, nia, alumno, cod_ciclo, cod_modulo, nota_final)
    SELECT m.curso_academico, a.nia, a.apellidos || ', ' || a.nombre, mo.cod_ciclo, mo.codigo, m.nota_final
    FROM   matricula m
           JOIN alumno a  ON a.id_alumno  = m.id_alumno
           JOIN modulo mo ON mo.id_modulo = m.id_modulo
    WHERE  m.curso_academico = '2025-26';
    -- 143 filas creadas
    COMMIT;
    ```

3. **Tabla de resumen** para el cuadro de mando:

    ```sql
    CREATE TABLE resumen_grupo AS
    SELECT a.cod_grupo,
           COUNT(*)                                          AS matriculas,
           SUM(CASE WHEN m.nota_final >= 5 THEN 1 ELSE 0 END) AS aprobadas,
           ROUND(AVG(m.nota_final), 2)                       AS media,
           SYSDATE                                           AS calculado
    FROM   matricula m JOIN alumno a ON a.id_alumno = m.id_alumno
    GROUP  BY a.cod_grupo;

    SELECT cod_grupo, matriculas, aprobadas, media FROM resumen_grupo ORDER BY cod_grupo;
    ```

    | COD_GRUPO | MATRICULAS | APROBADAS | MEDIA |
    |---|---|---|---|
    | 1ASIR | 25 | 21 | 7.07 |
    | 1DAM | 35 | 27 | 6.4 |
    | 1DAW | 30 | 24 | 6.19 |
    | 2DAM | 33 | 23 | 6.17 |
    | 2DAW | 20 | 15 | 5.93 |

4. **Restaura desde la copia.** Simula un desastre y recupera los datos:

    ```sql
    UPDATE matricula SET nota_final = NULL;   -- desastre: 143 filas
    COMMIT;                                   -- ¡y además confirmado!

    UPDATE matricula m
    SET    nota_final = (SELECT b.nota_final FROM bak_matricula b WHERE b.id_matricula = m.id_matricula);
    COMMIT;

    SELECT COUNT(nota_final) FROM matricula;  -- 137 otra vez
    ```

5. **Limpia:** `DROP TABLE bak_matricula PURGE; DROP TABLE resumen_grupo PURGE;`

{{% /steps %}}

#### Comprobación

{{% comprobacion %}}
- [ ] `BAK_MATRICULA` solo conserva las restricciones `NOT NULL`.
- [ ] `HISTORICO_NOTA` tiene 143 filas y su clave primaria impide archivar dos veces el mismo curso: repite el `INSERT` y comprueba que falla con ORA-00001.
- [ ] Tras el paso 4, las notas vuelven a ser las originales.
{{% /comprobacion %}}

#### Ampliación

¿Por qué la clave primaria de `HISTORICO_NOTA` incluye `cod_ciclo`? Piensa en el módulo 0484, que existe en DAM y en DAW.

---

## Práctica 8.3 · Modificaciones con subconsultas

{{< practica num="8.3" tipo="Autónoma" duracion="2 sesiones" nivel="2" ra="RA4: b, c, h" sgbd="Oracle 26ai · EDUGEST" entrega="p8_3.sql (cada sentencia con su SELECT de comprobación)" >}}

#### Objetivo

Escribir modificaciones que dependen de datos de otras tablas, comprobando antes y después las filas afectadas.

#### Enunciado

Ejecuta las tareas **en orden** sobre los datos originales. Para cada una escribe: (1) un `SELECT` que muestre las filas que se van a modificar, (2) la sentencia de modificación y (3) un `SELECT` de verificación. El número de filas afectadas debe coincidir con el indicado.

| # | Tarea | Filas |
|---|---|---|
| M1 | Dar de alta a la alumna Marina López Ortega (NIA 10452001, nacida el 14/03/2007, de Alicante, grupo 1DAM) | 1 |
| M2 | Matricular a Marina en **todos** los módulos de 1º de DAM para el curso 2026-27 con una sola sentencia | 5 |
| M3 | Subir a 5 las notas de Bases de datos de DAM (`0484`) comprendidas entre 4,5 y 5 (sin incluir el 5) | 2 |
| M4 | Asignar el grupo 1DAW a los alumnos sin grupo nacidos en 2006 | 3 |
| M5 | Asignar como tutor de 2ASIR al único profesor del departamento de Informática que no imparte clase (sin escribir su identificador) | 1 |
| M6 | Justificar todas las faltas de la alumna Martina Alemany Vidal | 3 |
| M7 | Borrar las faltas justificadas anteriores al 1 de noviembre de 2025 | 5 |
| M8 | Aumentar un 10 % (redondeado) las horas de los módulos de 2º de DAW | 4 |
| M9 | Cambiar el dominio del correo de **todo** el profesorado de `@edugest.es` a `@iesserragelada.es` | 12 |
| M10 | Dar de baja a Adrián Ferri Baeza (id 1). Antes, cuenta cuántas filas de **cada tabla** desaparecerán | 1 + 5 + 3 |

{{% details title="Pistas" %}}
- **M2:** `INSERT INTO matricula (...) SELECT 1001, id_modulo, '2026-27', ... FROM modulo WHERE ...`. Si Marina no tiene el id 1001 en tu base de datos, obtén el id con una subconsulta por su NIA.
- **M6:** las faltas no tienen el alumno: hay que llegar a él a través de la matrícula. `WHERE id_matricula IN (SELECT m.id_matricula FROM matricula m JOIN alumno a ... )`. Martina tiene 3 faltas y una ya está justificada: sin condición adicional se modifican 3; si añades `AND justificada = 'N'`, solo 2. Las dos opciones dejan el mismo resultado.
- **M9:** `REPLACE(email, '@edugest.es', '@iesserragelada.es')`. ¿Cumple el nuevo correo el `CHECK` del email?
- **M10:** las faltas desaparecen porque `fk_falta_matricula` también tiene `ON DELETE CASCADE`.
{{% /details %}}

{{< solucion id="ud08-001" title="Solución (M3, M5 y M10)" />}}

#### Comprobación

{{% comprobacion %}}
- [ ] Las filas afectadas coinciden con la tabla. Si no coinciden, **no** confirmes: haz `ROLLBACK` y revisa la condición.
- [ ] Al final, `SELECT COUNT(*) FROM alumno;` devuelve 32 (33 con Marina menos Adrián) y `SELECT COUNT(*) FROM matricula;` devuelve 143 (+5 −5).
- [ ] Ninguna sentencia usa identificadores escritos a mano cuando el enunciado pide obtenerlos.

> [!CAUTION]
> M10 elimina documentos académicos en cascada. En un sistema real no se borraría al alumno: se marcaría como **baja** (por ejemplo, con una columna `fecha_baja`) para conservar su expediente. Escribe en tu script un comentario que proponga esta alternativa.
{{% /comprobacion %}}

---

## Práctica 8.4 · Laboratorio de transacciones

{{< practica num="8.4" tipo="Guiada" duracion="1 sesión" nivel="2" ra="RA4: e, f" sgbd="Oracle 26ai" entrega="p8_4.sql + tabla de resultados" >}}

#### Objetivo

Comprobar experimentalmente el funcionamiento de `COMMIT`, `ROLLBACK`, `SAVEPOINT`, la confirmación implícita del DDL y la atomicidad de sentencia.

#### Preparación

```sql
CREATE TABLE cuenta (
    id_cuenta  CHAR(1)       CONSTRAINT pk_cuenta PRIMARY KEY,
    titular    VARCHAR2(50)  NOT NULL,
    saldo      NUMBER(12,2)  NOT NULL CONSTRAINT ck_cuenta_saldo CHECK (saldo >= 0)
);
INSERT INTO cuenta VALUES ('A', 'Asociación de alumnado', 1000);
INSERT INTO cuenta VALUES ('B', 'Viaje de fin de curso',   200);
INSERT INTO cuenta VALUES ('C', 'Cantina',                 50);
COMMIT;
```

#### Desarrollo

Ejecuta cada experimento y **predice** los saldos finales antes de consultar `SELECT * FROM cuenta ORDER BY id_cuenta;`.

| Exp. | Sentencias | A | B | C |
|---|---|---|---|---|
| 1 | `UPDATE cuenta SET saldo = saldo - 100 WHERE id_cuenta = 'A';` `UPDATE cuenta SET saldo = saldo + 100 WHERE id_cuenta = 'B';` `ROLLBACK;` | | | |
| 2 | Las dos mismas actualizaciones y `COMMIT;` | | | |
| 3 | `UPDATE cuenta SET saldo = saldo + 10 WHERE id_cuenta = 'C';` `SAVEPOINT s1;` `UPDATE cuenta SET saldo = 0;` `ROLLBACK TO SAVEPOINT s1;` `COMMIT;` | | | |
| 4 | `UPDATE cuenta SET saldo = saldo - 50 WHERE id_cuenta = 'B';` `UPDATE cuenta SET saldo = saldo - 100 WHERE id_cuenta = 'C';` (falla) `COMMIT;` | | | |
| 5 | `UPDATE cuenta SET saldo = saldo + 1000 WHERE id_cuenta = 'A';` `CREATE TABLE prueba (x NUMBER);` `ROLLBACK;` | | | |
| 6 | `UPDATE cuenta SET saldo = saldo - 10;` y cierra la sesión **de forma anómala** (cierra la ventana de la terminal o mata el proceso). Vuelve a conectar | | | |

{{< solucion id="ud08-002" title="Resultados esperados" />}}

#### Comprobación

{{% comprobacion %}}
- [ ] Has predicho correctamente al menos 5 de los 6 experimentos. Si no, explica en qué te equivocaste.
- [ ] Puedes explicar con tus palabras la **atomicidad de sentencia** (experimento 4) y por qué es peligrosa si la aplicación confirma sin comprobar los errores.
{{% /comprobacion %}}

#### Ampliación: la transferencia segura

Escribe la transferencia de 500 € de A a C como una transacción que **no** confirme nada si alguna de las dos actualizaciones no afecta exactamente a una fila. Usa `SQL%ROWCOUNT` en un bloque anónimo (adelanto de la UD09):

```sql
BEGIN
    UPDATE cuenta SET saldo = saldo - 500 WHERE id_cuenta = 'A';
    IF SQL%ROWCOUNT <> 1 THEN ROLLBACK; RAISE_APPLICATION_ERROR(-20001, 'Cuenta origen inexistente'); END IF;
    UPDATE cuenta SET saldo = saldo + 500 WHERE id_cuenta = 'Z';     -- cuenta inexistente
    IF SQL%ROWCOUNT <> 1 THEN ROLLBACK; RAISE_APPLICATION_ERROR(-20002, 'Cuenta destino inexistente'); END IF;
    COMMIT;
END;
/
```

---

## Práctica 8.5 · Dos sesiones, un dato: concurrencia y bloqueos

{{< practica num="8.5" tipo="Guiada" duracion="2 sesiones" nivel="3" ra="RA4: g, h" sgbd="Oracle 26ai · dos sesiones simultáneas (dos hojas con sesión propia o dos terminales SQLcl) + SYSTEM" entrega="Cronogramas completados + capturas" >}}

#### Objetivo

Observar en directo los efectos de las distintas políticas de bloqueo y de los niveles de aislamiento.

#### Preparación

Usa la tabla `CUENTA` de la práctica 8.4 restaurada a A = 1000, B = 200, C = 50. Abre **dos sesiones** como `EDUGEST`: **S1** y **S2**. En SQL Developer, abre la segunda hoja con *Hoja de trabajo SQL no compartida* (`Ctrl+Mayús+N`); si no, las dos hojas comparten sesión y no verás nada.

#### Experimento 1 · Las lecturas no se bloquean

| t | S1 | S2 |
|---|---|---|
| 1 | `UPDATE cuenta SET saldo = 0 WHERE id_cuenta = 'A';` | |
| 2 | | `SELECT saldo FROM cuenta WHERE id_cuenta = 'A';` → ¿? |
| 3 | `COMMIT;` | |
| 4 | | `SELECT saldo FROM cuenta WHERE id_cuenta = 'A';` → ¿? |

{{% details title="Resultado" %}}
En t2, S2 ve **1000** sin esperar: Oracle le muestra la última versión confirmada. En t4 ve **0**. No hay lecturas sucias ni lectores bloqueados.
{{% /details %}}

#### Experimento 2 · Las escrituras sobre la misma fila esperan

| t | S1 | S2 |
|---|---|---|
| 1 | `UPDATE cuenta SET saldo = saldo + 100 WHERE id_cuenta = 'B';` | |
| 2 | | `UPDATE cuenta SET saldo = saldo + 200 WHERE id_cuenta = 'B';` → ¿? |
| 3 | Como `SYSTEM`, en una tercera sesión: `SELECT sid, username, blocking_session, event FROM v$session WHERE username = 'EDUGEST';` | |
| 4 | `COMMIT;` | → ¿qué ocurre en S2? |
| 5 | | `COMMIT;` y consulta el saldo de B |

{{% details title="Resultado" %}}
En t2, S2 se queda **esperando**. En t3 verás que la sesión de S2 tiene `blocking_session` igual al SID de S1 y el evento `enq: TX - row lock contention`. En t4 S2 continúa. El saldo final de B es 200 + 100 + 200 = **500**: no se pierde ninguna actualización porque cada `UPDATE` lee el valor **actual** al ejecutarse.
{{% /details %}}

#### Experimento 3 · La actualización perdida (en la aplicación)

Simulamos dos aplicaciones que **leen** el saldo, calculan el nuevo valor **fuera** de la base de datos y lo escriben:

| t | S1 | S2 |
|---|---|---|
| 1 | `SELECT saldo FROM cuenta WHERE id_cuenta = 'C';` → 50 | |
| 2 | | `SELECT saldo FROM cuenta WHERE id_cuenta = 'C';` → 50 |
| 3 | `UPDATE cuenta SET saldo = 80 WHERE id_cuenta = 'C';` (50 + 30) | |
| 4 | `COMMIT;` | |
| 5 | | `UPDATE cuenta SET saldo = 70 WHERE id_cuenta = 'C';` (50 + 20) |
| 6 | | `COMMIT;` |

El saldo final es **70**: se ha perdido el ingreso de 30 de S1. Repite el experimento con las dos soluciones y comprueba que el saldo final es 100:

{{< tabs >}}
{{% tab "Pesimista: FOR UPDATE" %}}
En t1 y t2, ambas sesiones leen con `SELECT saldo FROM cuenta WHERE id_cuenta = 'C' FOR UPDATE;`. S2 **espera** en t2 hasta que S1 confirma en t4, y entonces lee 80. Escribe 80 + 20 = 100.
{{% /tab %}}
{{% tab "Optimista: comprobar al escribir" %}}
En t5, S2 escribe `UPDATE cuenta SET saldo = 70 WHERE id_cuenta = 'C' AND saldo = 50;` → **0 filas**: el saldo ya no es el que leyó. La aplicación vuelve a leer (80) y escribe `... SET saldo = 100 WHERE id_cuenta = 'C' AND saldo = 80;` → 1 fila.
{{% /tab %}}
{{< /tabs >}}

#### Experimento 4 · NOWAIT y WAIT

| t | S1 | S2 |
|---|---|---|
| 1 | `SELECT * FROM cuenta WHERE id_cuenta = 'A' FOR UPDATE;` | |
| 2 | | `SELECT * FROM cuenta WHERE id_cuenta = 'A' FOR UPDATE NOWAIT;` → ¿? |
| 3 | | `SELECT * FROM cuenta WHERE id_cuenta = 'A' FOR UPDATE WAIT 3;` → ¿? |
| 4 | `ROLLBACK;` | |

{{% details title="Resultado" %}}
t2: error inmediato `ORA-00054: resource busy and acquire with NOWAIT specified or timeout expired`. t3: espera 3 segundos y da `ORA-30006: resource busy; acquire with WAIT timeout expired`. Son útiles en aplicaciones que no deben quedarse colgadas.
{{% /details %}}

#### Experimento 5 · Interbloqueo

| t | S1 | S2 |
|---|---|---|
| 1 | `UPDATE cuenta SET saldo = saldo - 1 WHERE id_cuenta = 'A';` | |
| 2 | | `UPDATE cuenta SET saldo = saldo - 1 WHERE id_cuenta = 'B';` |
| 3 | `UPDATE cuenta SET saldo = saldo + 1 WHERE id_cuenta = 'B';` (espera) | |
| 4 | | `UPDATE cuenta SET saldo = saldo + 1 WHERE id_cuenta = 'A';` |
| 5 | → ¿? | |

{{% details title="Resultado" %}}
A los pocos segundos, Oracle detecta el ciclo y una de las sesiones (normalmente la que esperaba primero, S1) recibe `ORA-00060: deadlock detected while waiting for resource`. Solo se deshace **esa sentencia**: la sesión sigue teniendo bloqueada la fila A y debe hacer `ROLLBACK`. Repite el experimento haciendo que **las dos** sesiones actualicen primero A y después B: el interbloqueo desaparece (S2 simplemente espera).
{{% /details %}}

#### Experimento 6 · Informe consistente con READ ONLY

| t | S1 (jefatura, informe) | S2 (secretaría) |
|---|---|---|
| 1 | `SET TRANSACTION READ ONLY;` `SELECT SUM(saldo) FROM cuenta;` | |
| 2 | | `UPDATE cuenta SET saldo = saldo + 1000 WHERE id_cuenta = 'A';` `COMMIT;` |
| 3 | `SELECT SUM(saldo) FROM cuenta;` → ¿mismo valor que en t1? | |
| 4 | `COMMIT;` y repite la suma | |

#### Comprobación

{{% comprobacion %}}
- [ ] Has completado los seis cronogramas con los resultados obtenidos.
- [ ] Has capturado la consulta de `v$session` del experimento 2 mostrando la sesión bloqueada.
- [ ] Explicas, para cada experimento, qué problema de concurrencia aparece o se evita.
{{% /comprobacion %}}

---

## Práctica 8.6 · Carga de notas con MERGE

{{< practica num="8.6" tipo="Autónoma" duracion="1 sesión" nivel="2" ra="RA4: b, c" sgbd="Oracle 26ai · asistente de importación de SQL Developer" entrega="p8_6.sql + notas_0484_dam.csv" >}}

#### Contexto

El profesor de Bases de datos de DAM entrega las notas finales en un CSV. Algunas matrículas ya tenían nota (hay que actualizarla si ha cambiado) y se ha incorporado una alumna nueva que no estaba matriculada.

#### Enunciado

1. Crea el fichero `notas_0484_dam.csv` con este contenido:

    ```text
    NIA,NOTA
    10450037,5.25
    10450074,5
    10450111,8
    10450148,7
    10452001,6.5
    ```

2. Crea la tabla de carga `carga_notas_0484 (nia CHAR(8), nota NUMBER(4,2))` e **impórtala** con el asistente de SQL Developer (clic derecho → *Importar datos*).
3. Escribe un `MERGE` que, para cada fila del CSV, actualice la nota de la matrícula del curso 2025-26 en el módulo 0484 de DAM **solo si es distinta**.
4. Para el NIA 10452001, que no tiene matrícula de 2025-26, el `MERGE` no debe hacer nada: escribe una consulta que lo detecte como **incidencia**.
5. Ejecuta el `MERGE` dos veces. ¿Cuántas filas se fusionan cada vez?

#### Comprobación

- [ ] La primera ejecución fusiona **3** filas (la de 10450111 ya tenía un 8) y la segunda, **0**.
- [ ] La consulta de incidencias devuelve el NIA 10452001.

{{% details title="Pista: el MERGE" %}}
```sql
MERGE INTO matricula m
USING (SELECT c.nota, mt.id_matricula
       FROM   carga_notas_0484 c
              JOIN alumno a     ON a.nia = c.nia
              JOIN matricula mt ON mt.id_alumno = a.id_alumno
              JOIN modulo mo    ON mo.id_modulo = mt.id_modulo
       WHERE  mo.codigo = '0484' AND mo.cod_ciclo = 'DAM' AND mt.curso_academico = '2025-26') o
ON (m.id_matricula = o.id_matricula)
WHEN MATCHED THEN UPDATE SET m.nota_final = o.nota
                  WHERE m.nota_final IS NULL OR m.nota_final <> o.nota;
```
{{% /details %}}

---

## Práctica 8.7 · Reto: guion de promoción de curso

{{< practica num="8.7" tipo="Reto" duracion="3 sesiones" nivel="3" ra="RA4: d, e, f, h" sgbd="Oracle 26ai · SQLcl" entrega="promocion_2026_27.sql + salida (SPOOL) + defensa oral" >}}

#### Objetivo

Diseñar un guion transaccional que realiza una tarea compleja de forma segura, verificable y repetible.

#### Contexto

Ha terminado el curso 2025-26 y jefatura de estudios debe preparar el curso 2026-27 para el alumnado de **primer curso**. Las reglas son:

1. **Promociona** a segundo el alumnado de primero con **como máximo un** módulo pendiente. Un módulo está pendiente si su nota de 2025-26 es menor que 5 o está sin calificar.
2. Al alumnado que promociona se le cambia el grupo al de segundo de su ciclo (1DAM → 2DAM...) y se le matricula en **todos** los módulos de segundo de su ciclo, en primera convocatoria.
3. **Todo** el alumnado de primero (promocione o no) se matricula en 2026-27 de sus módulos **pendientes**, con la convocatoria siguiente a la que tenía.
4. Fecha de matrícula: 10 de septiembre de 2026.

#### Enunciado

Escribe `promocion_2026_27.sql` con esta estructura:

```sql
WHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK
SPOOL promocion_2026_27.log

-- 0. Comprobaciones previas (no modifican nada)
--    · ¿Ya existen matrículas de 2026-27? Si existen, el guion no debe ejecutarse.
--    · Listado del alumnado que promociona y del que no.

-- 1. Matrículas de módulos pendientes (regla 3)
-- 2. Matrículas de segundo curso (regla 2) — ¡antes de cambiar el grupo!
-- 3. Cambio de grupo (regla 2)

-- 4. Verificaciones: recuentos esperados
-- 5. COMMIT
SPOOL OFF
```

#### Comprobación

Con los datos originales de EduGest, tu guion debe obtener exactamente:

| Comprobación | Valor esperado |
|---|---|
| Alumnado de primero que promociona | 12 (4 de 1DAM, 4 de 1DAW, 4 de 1ASIR) |
| Matrículas de pendientes insertadas | 18 |
| Matrículas de segundo insertadas | 36 (20 de DAM y 16 de DAW) |
| Filas de `ALUMNO` con el grupo cambiado | 12 |
| Total de matrículas de 2026-27 | 54 |
| Alumnado por grupo tras el guion | 1ASIR 1 · 1DAM 3 · 1DAW 2 · 2ASIR 4 · 2DAM 10 · 2DAW 9 · sin grupo 3 |

- [ ] Ejecutar el guion **por segunda vez** no cambia nada (se detiene en las comprobaciones previas).
- [ ] Si provocas un error a mitad (por ejemplo, cambiando el nombre de una tabla), **no** queda ningún cambio aplicado.
- [ ] Explicas por qué el alumnado de 1ASIR que promociona no recibe matrículas de segundo (pista: consulta qué módulos de ASIR existen) y qué debería hacer el centro.

{{% details title="Pista: el orden importa" %}}
Si cambias el grupo **antes** de insertar las matrículas, ya no sabrás quién estaba en primero ni podrás distinguir al alumnado que promociona del que ya estaba en segundo. Otra opción profesional es calcular primero la lista de alumnos que promocionan y guardarla en una **tabla temporal global** (`CREATE GLOBAL TEMPORARY TABLE ... ON COMMIT PRESERVE ROWS`) creada **fuera** del guion.
{{% /details %}}

{{% details title="Pista: detener el guion si ya se ejecutó" %}}
```sql
DECLARE
    v_n NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_n FROM matricula WHERE curso_academico = '2026-27';
    IF v_n > 0 THEN
        RAISE_APPLICATION_ERROR(-20100, 'Ya existen ' || v_n || ' matrículas de 2026-27');
    END IF;
END;
/
```
Con `WHENEVER SQLERROR EXIT`, el error termina el guion.
{{% /details %}}

---

## Proyecto EduGest · UD08: guiones de mantenimiento

{{< practica num="EduGest-8" tipo="Proyecto" duracion="Trabajo transversal (1 semana)" nivel="3" ra="RA4: a-h" sgbd="Oracle 26ai · SQLcl" entrega="edugest/08_mantenimiento/*.sql + docs/08-transacciones.md" >}}

#### Enunciado

1. **Datos de 2026-27.** Ejecuta tu guion de promoción (práctica 8.7) y añade un guion `alta_nuevo_alumnado.sql` que dé de alta a **diez** alumnos nuevos de primero con sus matrículas, en una sola transacción.
2. **Baja lógica.** Añade a `ALUMNO` una columna `fecha_baja` y escribe el guion que da de baja a un alumno **sin borrar** su expediente. Modifica las vistas de la UD05 para que no muestren al alumnado dado de baja.
3. **Política de concurrencia.** En `08-transacciones.md`, decide y justifica la estrategia de bloqueo (pesimista u optimista) para tres operaciones de la aplicación: poner notas, matricular y registrar faltas.
4. **Integridad.** Revisa tu catálogo de restricciones (UD03-UD05): ¿alguna puede implementarse con una restricción diferida o con un guion transaccional? Documenta qué queda para la UD09.

#### Comprobación

{{% comprobacion %}}
- [ ] Todos los guiones son transaccionales: un error deja la base de datos como estaba.
- [ ] Ningún guion contiene DDL entre sentencias DML de la misma transacción.
- [ ] La estrategia de concurrencia está justificada con argumentos de la práctica 8.5.
{{% /comprobacion %}}
