---
title: "Consultas avanzadas - Prácticas"
weight: 2
bookToc: true
---

# UD07 · Prácticas

{{< ra "RA3:a,c,d,e,f,g,h" "RA2:f" >}}

| Práctica | Tipo | Nivel | CE principales |
|---|---|---|---|
| [7.1 Consultas resumen](#práctica-71--consultas-resumen) | Guiada | ●○○ | RA3.e |
| [7.2 Composiciones paso a paso](#práctica-72--composiciones-paso-a-paso) | Guiada | ●●○ | RA3.c, RA3.d |
| [7.3 Informes para jefatura](#práctica-73--informes-para-jefatura) | Autónoma | ●●○ | RA3.c, RA3.d, RA3.e |
| [7.4 Subconsultas](#práctica-74--subconsultas) | Autónoma | ●●○ | RA3.f |
| [7.5 Múltiples selecciones y vistas](#práctica-75--múltiples-selecciones-y-vistas) | Autónoma | ●●○ | RA3.g, RA2.f |
| [7.6 Optimización: medir antes y después](#práctica-76--optimización-medir-antes-y-después) | Guiada | ●●● | RA3.h |
| [7.7 Reto: el cuadro de mando](#práctica-77--reto-el-cuadro-de-mando) | Reto | ●●● | RA3.c-h |
| [Proyecto EduGest · UD07](#proyecto-edugest--ud07-informes) | Proyecto | ●●● | RA3 completo |

> [!IMPORTANT]
> Trabaja sobre **EDUGEST con los datos originales** (scripts 01 y 02) y con `ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY';`. Intenta cada consulta antes de abrir la solución; como mínimo, comprueba que obtienes el **mismo número de filas**.

---

## Práctica 7.1 · Consultas resumen

{{< practica num="7.1" tipo="Guiada" duracion="2 sesiones" nivel="1" ra="RA3: e" sgbd="Oracle 26ai · EDUGEST" entrega="p7_1.sql" >}}

#### Objetivo

Usar funciones de agregado, `GROUP BY` y `HAVING`, y entender cómo influyen los valores nulos en los resultados.

#### Desarrollo

{{% steps %}}

1. **Totales generales.** ¿Cuántos alumnos hay, cuántos tienen grupo y en cuántos grupos distintos están?

    ```sql
    SELECT COUNT(*) AS alumnos, COUNT(cod_grupo) AS con_grupo, COUNT(DISTINCT cod_grupo) AS grupos
    FROM   alumno;
    ```

    | ALUMNOS | CON_GRUPO | GRUPOS |
    |---|---|---|
    | 32 | 29 | 5 |

    *1 fila*


2. **Agrupar por una columna.** Número de alumnos por localidad, de más a menos.

    ```sql
    SELECT localidad, COUNT(*) AS alumnos
    FROM   alumno
    GROUP  BY localidad
    ORDER  BY alumnos DESC, localidad;
    ```

    | LOCALIDAD | ALUMNOS |
    |---|---|
    | Alicante | 13 |
    | Mutxamel | 6 |
    | Sant Joan d'Alacant | 4 |
    | El Campello | 3 |
    | Elche | 3 |
    | San Vicente del Raspeig | 3 |

    *6 filas*


3. **Agrupar por varias columnas.** Faltas y horas de falta por mes y por tipo (justificada o no).

    ```sql
    SELECT TO_CHAR(fecha, 'YYYY-MM') AS mes, justificada,
           COUNT(*) AS faltas, SUM(horas) AS horas
    FROM   falta_asistencia
    GROUP  BY TO_CHAR(fecha, 'YYYY-MM'), justificada
    ORDER  BY mes, justificada;
    ```

    | MES | JUSTIFICADA | FALTAS | HORAS |
    |---|---|---|---|
    | 2025-09 | N | 3 | 5 |
    | 2025-09 | S | 2 | 2 |
    | 2025-10 | N | 4 | 6 |
    | 2025-10 | S | 3 | 4 |
    | 2025-11 | N | 2 | 5 |
    | 2025-11 | S | 2 | 4 |
    | 2025-12 | N | 2 | 2 |
    | 2026-01 | N | 5 | 10 |
    | 2026-02 | N | 3 | 5 |
    | 2026-02 | S | 5 | 11 |
    | 2026-03 | N | 5 | 11 |
    | 2026-03 | S | 4 | 5 |
    | 2026-04 | N | 3 | 6 |
    | 2026-04 | S | 1 | 1 |
    | 2026-05 | S | 2 | 4 |

    *15 filas*


4. **Filtrar grupos.** Módulos (por `id_modulo`) con al menos un suspenso y su número de suspensos, solo si hay **dos o más**.

    ```sql
    SELECT id_modulo, COUNT(*) AS suspensos
    FROM   matricula
    WHERE  nota_final < 5
    GROUP  BY id_modulo
    HAVING COUNT(*) >= 2
    ORDER  BY suspensos DESC, id_modulo;
    ```

    | ID_MODULO | SUSPENSOS |
    |---|---|
    | 3 | 4 |
    | 18 | 3 |
    | 2 | 2 |
    | 6 | 2 |
    | 7 | 2 |
    | 10 | 2 |
    | 11 | 2 |
    | 13 | 2 |

    *8 filas*


5. **Contar condiciones.** Para cada convocatoria: matrículas, aprobadas, suspensas y sin calificar.

    ```sql
    SELECT convocatoria,
           COUNT(*) AS total,
           SUM(CASE WHEN nota_final >= 5 THEN 1 ELSE 0 END) AS aprobadas,
           SUM(CASE WHEN nota_final <  5 THEN 1 ELSE 0 END) AS suspensas,
           COUNT(*) - COUNT(nota_final)                    AS sin_calificar
    FROM   matricula
    GROUP  BY convocatoria
    ORDER  BY convocatoria;
    ```

    | CONVOCATORIA | TOTAL | APROBADAS | SUSPENSAS | SIN_CALIFICAR |
    |---|---|---|---|---|
    | 1 | 140 | 108 | 26 | 6 |
    | 2 | 3 | 2 | 1 | 0 |

    *2 filas*


6. **Provoca los errores típicos** y anota el mensaje:

    ```sql
    SELECT localidad, nombre, COUNT(*) FROM alumno GROUP BY localidad;   -- ORA-00979
    SELECT localidad, COUNT(*) FROM alumno;                              -- ORA-00937
    SELECT localidad FROM alumno WHERE COUNT(*) > 3 GROUP BY localidad;  -- ORA-00934
    ```

{{% /steps %}}

#### Comprobación

{{% comprobacion %}}
- [ ] En el paso 1 entiendes por qué `COUNT(*)` y `COUNT(cod_grupo)` dan resultados distintos.
- [ ] En el paso 5, la suma de aprobadas, suspensas y sin calificar coincide con el total de cada convocatoria.
- [ ] Sabes corregir cada uno de los tres errores del paso 6.
{{% /comprobacion %}}

#### Ampliación

Repite el paso 2 añadiendo `ROLLUP`: `GROUP BY ROLLUP(localidad)`. ¿Qué fila nueva aparece? ¿Qué valor tiene `localidad` en ella?

---

## Práctica 7.2 · Composiciones paso a paso

{{< practica num="7.2" tipo="Guiada" duracion="2 sesiones" nivel="2" ra="RA3: c, d" sgbd="Oracle 26ai · EDUGEST" entrega="p7_2.sql + respuestas" >}}

#### Objetivo

Construir composiciones de varias tablas siguiendo el camino de claves ajenas, y decidir cuándo hace falta una composición externa.

#### Desarrollo

{{% steps %}}

1. **Traza el camino.** Queremos, para cada falta de asistencia, el nombre del alumno, el nombre del módulo y el ciclo. Sobre el diagrama relacional de EduGest, el camino es:

    ```mermaid
    flowchart LR
        F[FALTA_ASISTENCIA] -- id_matricula --> M[MATRICULA]
        M -- id_alumno --> A[ALUMNO]
        M -- id_modulo --> MO[MODULO]
        MO -- cod_ciclo --> C[CICLO]
    ```

2. **Añade las tablas una a una** y comprueba el número de filas en cada paso. Si el número **aumenta** de forma inesperada, falta una condición o la composición no sigue una clave ajena.

    ```sql
    -- Paso a: solo faltas
    SELECT COUNT(*) FROM falta_asistencia f;                                  -- 46
    -- Paso b: + matrícula
    SELECT COUNT(*) FROM falta_asistencia f
           JOIN matricula m ON m.id_matricula = f.id_matricula;              -- 46
    -- Paso c: + alumno y módulo
    SELECT COUNT(*) FROM falta_asistencia f
           JOIN matricula m ON m.id_matricula = f.id_matricula
           JOIN alumno a    ON a.id_alumno    = m.id_alumno
           JOIN modulo mo   ON mo.id_modulo   = m.id_modulo;                 -- 46
    ```

3. **Escribe la consulta final**, limitada a las faltas no justificadas de 3 horas:

    ```sql
    SELECT f.fecha, a.apellidos || ', ' || a.nombre AS alumno,
           mo.nombre AS modulo, c.cod_ciclo, f.horas
    FROM   falta_asistencia f
           JOIN matricula m ON m.id_matricula = f.id_matricula
           JOIN alumno a    ON a.id_alumno    = m.id_alumno
           JOIN modulo mo   ON mo.id_modulo   = m.id_modulo
           JOIN ciclo c     ON c.cod_ciclo    = mo.cod_ciclo
    WHERE  f.justificada = 'N' AND f.horas = 3
    ORDER  BY f.fecha;
    ```

    | FECHA | ALUMNO | MODULO | COD_CICLO | HORAS |
    |---|---|---|---|---|
    | 22/09/2025 | Quiles Marco, Valeria | Entornos de desarrollo | DAM | 3 |
    | 21/10/2025 | Ripoll Agulló, Iván | Sistemas de gestión empresarial | DAM | 3 |
    | 25/11/2025 | Cerdá Tomás, Nerea | Sistemas informáticos | DAM | 3 |
    | 06/01/2026 | Amorós Guillem, Sara | Diseño de interfaces web | DAW | 3 |
    | 21/01/2026 | Tomás Vidal, Álex | Lenguajes de marcas y sistemas de gestión de información | ASIR | 3 |
    | 25/02/2026 | Alemany Vidal, Martina | Sistemas de gestión empresarial | DAM | 3 |
    | 10/03/2026 | Cerdá Pérez, Tomás | Programación | DAM | 3 |
    | 19/03/2026 | Ferri Baeza, Adrián | Programación | DAM | 3 |
    | 25/03/2026 | Alemany Pérez, Daniel | Entornos de desarrollo | DAW | 3 |
    | 29/04/2026 | Alemany Vidal, Martina | Programación de servicios y procesos | DAM | 3 |

    *10 filas*


4. **Provoca un producto cartesiano** quitando la condición `ON` de `MODULO` (en Oracle, sustituye `JOIN modulo mo ON ...` por `CROSS JOIN modulo mo`). ¿Cuántas filas salen ahora en el paso c? ¿Por qué?

5. **Interna frente a externa.** Ejecuta las dos consultas y explica la diferencia:

    ```sql
    -- (a) Interna
    SELECT c.cod_ciclo, COUNT(g.cod_grupo) AS grupos
    FROM   ciclo c JOIN grupo g ON g.cod_ciclo = c.cod_ciclo
    GROUP  BY c.cod_ciclo ORDER BY c.cod_ciclo;

    -- (b) Externa
    SELECT c.cod_ciclo, COUNT(g.cod_grupo) AS grupos
    FROM   ciclo c LEFT JOIN grupo g ON g.cod_ciclo = c.cod_ciclo
    GROUP  BY c.cod_ciclo ORDER BY c.cod_ciclo;
    ```

    | (a) Interna | | (b) Externa | |
    |---|---|---|---|
    | ASIR | 2 | ASIR | 2 |
    | DAM | 2 | DAM | 2 |
    | DAW | 2 | DAW | 2 |
    | | | **SMR** | **0** |

6. **La trampa del WHERE.** Queremos todos los profesores y las horas que imparten **en 2DAM** (0 si no imparten allí). Compara:

    ```sql
    -- (a) Incorrecta: el WHERE elimina a quien no imparte en 2DAM
    SELECT p.nombre, NVL(SUM(i.horas_semanales), 0) AS horas_2dam
    FROM   profesor p LEFT JOIN imparte i ON i.id_profesor = p.id_profesor
    WHERE  i.cod_grupo = '2DAM'
    GROUP  BY p.id_profesor, p.nombre ORDER BY p.id_profesor;     -- 4 filas

    -- (b) Correcta: la condición sobre la tabla opcional va en el ON
    SELECT p.nombre, NVL(SUM(i.horas_semanales), 0) AS horas_2dam
    FROM   profesor p LEFT JOIN imparte i
           ON i.id_profesor = p.id_profesor AND i.cod_grupo = '2DAM'
    GROUP  BY p.id_profesor, p.nombre ORDER BY p.id_profesor;     -- 12 filas
    ```

    | NOMBRE | HORAS_2DAM |
    |---|---|
    | Marta | 0 |
    | Javier | 3 |
    | Lucía | 6 |
    | Andrés | 4 |
    | Elena | 0 |
    | Raúl | 3 |
    | Nuria | 0 |
    | Pablo | 0 |
    | Carmen | 0 |
    | Sergio | 0 |
    | Laura | 0 |
    | David | 0 |

    *12 filas*


{{% /steps %}}

#### Comprobación

{{% comprobacion %}}
- [ ] Las tres consultas del paso 2 devuelven 46 filas.
- [ ] En el paso 4 obtienes 46 × 24 = 1104 filas y sabes explicarlo.
- [ ] Sabes explicar por qué SMR solo aparece con `LEFT JOIN` y por qué el `COUNT` da 0 y no 1.
- [ ] En el paso 6, la versión (b) devuelve los 12 profesores.
{{% /comprobacion %}}

---

## Práctica 7.3 · Informes para jefatura

{{< practica num="7.3" tipo="Autónoma" duracion="3 sesiones" nivel="2" ra="RA3: c, d, e" sgbd="Oracle 26ai · EDUGEST" entrega="p7_3.sql comentado" >}}

#### Objetivo

Resolver de forma autónoma consultas de varias tablas, decidiendo el tipo de composición y combinándolas con agrupamientos.

#### Enunciado

**J1.** Listado de módulos con el nombre completo de su ciclo, solo de 2º curso.

{{< solucion id="ud07-001" title="Solución J1" />}}

**J2.** Profesorado con el nombre de su departamento y, si es jefe de algún departamento, el nombre de ese departamento (si no, vacío).

{{< solucion id="ud07-002" title="Solución J2" />}}

**J3.** Carga docente: para cada profesor que imparte clase, número de módulos, número de grupos distintos y horas semanales totales, de más a menos horas.

{{< solucion id="ud07-003" title="Solución J3" />}}

**J4.** Todos los grupos con su número de alumnos y su tutor; deben aparecer los grupos sin alumnos y sin tutor.

{{< solucion id="ud07-004" title="Solución J4" />}}

**J5.** Porcentaje de aprobados por módulo de DAM (código, nombre, matrículas calificadas y porcentaje con un decimal), del peor al mejor porcentaje.

{{< solucion id="ud07-005" title="Solución J5" />}}

**J6.** Alumnado con más de 3 horas de faltas **no justificadas** en total (nombre, grupo y horas).

{{< solucion id="ud07-006" title="Solución J6" />}}

**J7.** Profesorado del departamento de Informática y Comunicaciones que **no** es tutor de ningún grupo.

{{< solucion id="ud07-007" title="Solución J7" />}}

**J8.** Para cada alumno de 1DAM, su nota en *Bases de datos* (0484) y en *Programación* (0485) en la misma fila.

{{< solucion id="ud07-008" title="Solución J8" />}}

#### Comprobación

{{% comprobacion %}}
- [ ] Has elegido composición interna o externa según la pregunta y lo justificas en un comentario.
- [ ] J4 muestra 2ASIR con 0 alumnos y «(sin tutor)».
- [ ] J5 no divide entre las matrículas sin calificar.
{{% /comprobacion %}}

---

## Práctica 7.4 · Subconsultas

{{< practica num="7.4" tipo="Autónoma" duracion="2 sesiones" nivel="2" ra="RA3: f" sgbd="Oracle 26ai · EDUGEST" entrega="p7_4.sql" >}}

#### Enunciado

**S1.** Alumnado de mayor edad (puede haber empates).

{{< solucion id="ud07-009" title="Solución S1" />}}

**S2.** Módulos de DAW con más horas que **cualquier** módulo de 2º de DAM.

{{< solucion id="ud07-010" title="Solución S2" />}}

**S3.** Alumnos que tienen **alguna** falta de asistencia (usa `EXISTS`).

{{< solucion id="ud07-011" title="Solución S3" />}}

**S4.** Alumnos con grupo que **no** tienen ninguna falta.

{{< solucion id="ud07-012" title="Solución S4" />}}

**S5.** Para cada alumno de 2DAW, su nota media y la diferencia con la media de **su grupo** (subconsulta correlacionada).

{{< solucion id="ud07-013" title="Solución S5" />}}

**S6.** El grupo (o grupos) con más alumnos. Resuélvelo con una subconsulta en el `HAVING`.

{{< solucion id="ud07-014" title="Solución S6" />}}

**S7.** Explica por qué esta consulta no devuelve filas y corrígela de dos formas:

```sql
SELECT nombre FROM profesor WHERE id_profesor NOT IN (SELECT id_tutor FROM grupo);
```

{{< solucion id="ud07-015" title="Solución S7" />}}

---

## Práctica 7.5 · Múltiples selecciones y vistas

{{< practica num="7.5" tipo="Autónoma" duracion="1 sesión" nivel="2" ra="RA3: g · RA2: f" sgbd="Oracle 26ai · EDUGEST" entrega="p7_5.sql" >}}

#### Enunciado

**U1.** Lista única de todas las **localidades** en las que vive alumnado de DAM o de DAW (sin repetir).

{{< solucion id="ud07-016" title="Solución U1" />}}

**U2.** Localidades con alumnado **tanto** de DAM **como** de DAW.

{{< solucion id="ud07-017" title="Solución U2" />}}

**U3.** Códigos de módulo oficiales que están en DAM pero **no** en DAW.

{{< solucion id="ud07-018" title="Solución U3" />}}

**U4.** Crea la vista `v_acta` de la [teoría](/ud07-consultas-avanzadas/ud07-teoria#7-vistas-con-composiciones) y úsala para obtener el número de APTOS, NO APTOS y NC de cada módulo de 1DAW.

{{< solucion id="ud07-019" title="Solución U4" />}}

---

## Práctica 7.6 · Optimización: medir antes y después

{{< practica num="7.6" tipo="Guiada" duracion="2 sesiones" nivel="3" ra="RA3: h" sgbd="Oracle 26ai · SQL Developer (Explicar plan, Autotrace) o SQLcl" entrega="p7_6.sql + tabla de mediciones + capturas de los planes" >}}

#### Objetivo

Comprobar con mediciones reales cómo afectan los índices y la forma de escribir una consulta a su plan de ejecución y a su rendimiento.

#### Contexto

EduGest tiene muy pocos datos para notar diferencias. Simularemos el **histórico de accesos** del portal del alumnado durante varios cursos: medio millón de filas.

#### Desarrollo

{{% steps %}}

1. **Crea y llena la tabla** (conectado como `EDUGEST`). `CONNECT BY LEVEL` es un truco de Oracle para generar filas:

    ```sql
    CREATE TABLE acceso_portal (
        id_acceso   NUMBER(10)   CONSTRAINT pk_acceso_portal PRIMARY KEY,
        id_alumno   NUMBER(6)    NOT NULL,
        fecha_hora  DATE         NOT NULL,
        ip          VARCHAR2(15) NOT NULL,
        seccion     VARCHAR2(20) NOT NULL
    );

    INSERT INTO acceso_portal
    SELECT LEVEL,
           MOD(LEVEL * 7, 5000) + 1,
           DATE '2022-09-01' + MOD(LEVEL * 13, 1460) + MOD(LEVEL, 86400) / 86400,
           '10.0.' || MOD(LEVEL, 256) || '.' || MOD(LEVEL * 3, 256),
           CASE MOD(LEVEL, 5) WHEN 0 THEN 'NOTAS' WHEN 1 THEN 'FALTAS' WHEN 2 THEN 'HORARIO'
                              WHEN 3 THEN 'MENSAJES' ELSE 'PERFIL' END
    FROM   dual
    CONNECT BY LEVEL <= 500000;
    COMMIT;

    EXEC DBMS_STATS.GATHER_TABLE_STATS(USER, 'ACCESO_PORTAL');
    SET TIMING ON
    ```

2. **Consulta 1: buscar por alumno sin índice.**

    ```sql
    SELECT COUNT(*) FROM acceso_portal WHERE id_alumno = 1234;
    ```

    Obtén el plan (F10 en SQL Developer, o `EXPLAIN PLAN FOR ...` + `SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);`). Anota la operación, el coste y el tiempo. Debe aparecer `TABLE ACCESS FULL`.

3. **Crea un índice** y repite la medición:

    ```sql
    CREATE INDEX ix_acceso_alumno ON acceso_portal (id_alumno);
    ```

    El plan debe cambiar a `INDEX RANGE SCAN`, con un coste mucho menor. Como solo se pide `COUNT(*)`, Oracle ni siquiera necesita leer la tabla.

4. **Consulta 2: función sobre la columna.** Compara estas dos consultas equivalentes:

    ```sql
    -- (a) Función sobre la columna fecha_hora
    SELECT COUNT(*) FROM acceso_portal WHERE TRUNC(fecha_hora) = DATE '2024-03-15';
    -- (b) Rango sobre la columna sin modificarla
    SELECT COUNT(*) FROM acceso_portal
    WHERE  fecha_hora >= DATE '2024-03-15' AND fecha_hora < DATE '2024-03-16';
    ```

    Crea `CREATE INDEX ix_acceso_fecha ON acceso_portal (fecha_hora);` y compara los planes de (a) y (b). Solo (b) puede usar el índice.

5. **Consulta 3: selectividad.** Con un índice sobre `seccion`, ¿usa Oracle el índice para `WHERE seccion = 'NOTAS'`? Esa condición devuelve el 20 % de la tabla: lo más probable es que el optimizador prefiera `TABLE ACCESS FULL`. Compruébalo y explica por qué es la decisión correcta.

6. **Consulta 4: composición.** Mide la composición con `ALUMNO` antes y después de que exista el índice `ix_acceso_alumno`:

    ```sql
    SELECT a.cod_grupo, COUNT(*) AS accesos
    FROM   acceso_portal ap JOIN alumno a ON a.id_alumno = ap.id_alumno
    GROUP  BY a.cod_grupo;
    ```

7. **Limpia** al terminar: `DROP TABLE acceso_portal PURGE;`

{{% /steps %}}

#### Comprobación

{{% comprobacion %}}
Completa la tabla de mediciones con tus datos (los valores exactos dependen de tu equipo):

| Consulta | Sin índice: operación / coste / tiempo | Con índice: operación / coste / tiempo |
|---|---|---|
| 1 · `id_alumno = 1234` | `TABLE ACCESS FULL` / … / … | `INDEX RANGE SCAN` / … / … |
| 2a · `TRUNC(fecha_hora) = ...` | | |
| 2b · rango de fechas | | |
| 3 · `seccion = 'NOTAS'` | | |
| 4 · composición con `ALUMNO` | | |

- [ ] La consulta 1 devuelve 100 accesos y su coste baja de forma clara con el índice.
- [ ] Explicas por qué 2a no usa el índice y cómo lo conseguirías sin reescribirla (índice basado en función sobre `TRUNC(fecha_hora)`).
- [ ] Explicas por qué en la consulta 3 un acceso completo puede ser mejor que el índice.

> [!WARNING]
> Las mediciones de tiempo varían entre ejecuciones porque Oracle guarda en caché los bloques leídos. Ejecuta cada consulta **dos o tres veces** y anota el tiempo de las últimas. El **coste** del plan es una estimación del optimizador, no un tiempo.
{{% /comprobacion %}}

#### Ampliación

Añade `/*+ FULL(ap) */` justo después de `SELECT` en la consulta 1 con índice y compara. Las *hints* obligan al optimizador a usar un plan concreto; en producción solo se usan cuando se ha demostrado que el optimizador se equivoca.

---

## Práctica 7.7 · Reto: el cuadro de mando

{{< practica num="7.7" tipo="Reto" duracion="2 sesiones" nivel="3" ra="RA3: c, d, e, f, g, h" sgbd="Oracle 26ai · EDUGEST" entrega="p7_7.sql + defensa oral" >}}

#### Enunciado

La dirección quiere un **cuadro de mando** con una sola consulta por indicador. Resuelve cada uno con la técnica que consideres más adecuada y justifica la elección:

1. Para cada ciclo (incluido SMR): número de grupos, de alumnos, de matrículas y nota media.
2. Los **dos** mejores alumnos de cada grupo según su nota media (pista: `RANK()` o `ROW_NUMBER()` con `PARTITION BY`).
3. Para cada profesor que imparte clase: la nota media de sus alumnos en los módulos que imparte **en los grupos en los que los imparte**. (Cuidado: la composición entre `IMPARTE` y `MATRICULA` debe usar el módulo **y** el grupo del alumno.)
4. Alumnos que han suspendido **todos** los módulos en los que están calificados.
5. Porcentaje de horas de falta justificadas sobre el total, por grupo.
6. Escribe una de las consultas anteriores de dos formas distintas (por ejemplo, subconsulta frente a composición) y compara sus planes de ejecución.

#### Comprobación

{{% comprobacion %}}
- [ ] El indicador 1 tiene 4 filas y SMR aparece con ceros.
- [ ] El indicador 3 no mezcla alumnos de otros grupos con el mismo módulo.
- [ ] Puedes defender cada consulta y explicar su plan de ejecución.

{{% details title="Pista para el indicador 4" %}}
«Todos suspendidos» equivale a «no existe ninguno aprobado» y «tiene al menos uno calificado»: `NOT EXISTS (... nota_final >= 5)` y `EXISTS (... nota_final IS NOT NULL)`. Otra forma: `GROUP BY` alumno con `HAVING MAX(nota_final) < 5`.
{{% /details %}}
{{% /comprobacion %}}

---

## Proyecto EduGest · UD07: informes

{{< practica num="EduGest-7" tipo="Proyecto" duracion="Trabajo transversal (2 semanas)" nivel="3" ra="RA3: a-h · RA2: f" sgbd="Oracle 26ai · EDUGEST" entrega="edugest/06_informes.sql + 07_vistas_informes.sql + docs/07-optimizacion.md" >}}

#### Enunciado

1. Escribe **diez informes** para EduGest que en conjunto usen: composiciones internas y externas (al menos tres tablas en alguno), consultas resumen con `HAVING`, subconsultas (una correlacionada y una con `EXISTS`), un operador de conjuntos y una función analítica.
2. Convierte los tres informes más usados en **vistas** y concede `SELECT` sobre ellas al rol adecuado de la práctica 5.7.
3. **Optimización:** elige dos de tus informes, obtén su plan de ejecución, propón una mejora (índice o reescritura) y documenta el antes y el después en `07-optimizacion.md`. Si EduGest tiene pocos datos para notar la diferencia, explícalo y apóyate en la práctica 7.6.

#### Comprobación

{{% comprobacion %}}
- [ ] Cada informe tiene un comentario con el perfil que lo usa, la pregunta que responde y el número de filas.
- [ ] Las vistas se pueden consultar desde el usuario del rol correspondiente.
- [ ] El documento de optimización incluye los planes antes y después.
{{% /comprobacion %}}
