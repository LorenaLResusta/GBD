---
title: "Consultas sobre una tabla - Prácticas"
weight: 2
bookToc: true
---

# UD06 · Prácticas

{{< ra "RA3:a,b" "RA5:e" >}}

| Práctica | Tipo | Nivel | CE principales |
|---|---|---|---|
| [6.1 Primeras consultas y herramientas](#práctica-61--primeras-consultas-y-herramientas) | Guiada | ●○○ | RA3.a, RA3.b |
| [6.2 Consultas para secretaría](#práctica-62--consultas-para-secretaría) | Autónoma | ●●○ | RA3.b |
| [6.3 Laboratorio de valores nulos](#práctica-63--laboratorio-de-valores-nulos) | Guiada | ●●○ | RA3.b |
| [6.4 Funciones para informes](#práctica-64--funciones-para-informes) | Autónoma | ●●○ | RA3.b, RA5.e |
| [6.5 Validar datos con SQL](#práctica-65--validar-datos-con-sql) | Reto | ●●● | RA3.b, RA5.e |
| [Proyecto EduGest · UD06](#proyecto-edugest--ud06-consultas-del-día-a-día) | Proyecto | ●●○ | RA3.a, RA3.b |

> [!IMPORTANT]
> Todas las prácticas usan el esquema de referencia **EDUGEST** con los datos del [script 02](/guia/proyecto-edugest#4-scripts-descargables). Antes de empezar, ejecuta en tu sesión:
>
> ```sql
> ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY';
> ```
>
> Si has modificado los datos en otras prácticas, vuelve a ejecutar los scripts 01 y 02 para que tus resultados coincidan con las soluciones.

---

## Práctica 6.1 · Primeras consultas y herramientas

{{< practica num="6.1" tipo="Guiada" duracion="1 sesión" nivel="1" ra="RA3: a, b" sgbd="Oracle 26ai · SQL Developer (o extensión de VS Code)" entrega="p6_1.sql + captura del generador de consultas" >}}

#### Objetivo

Conocer las herramientas de consulta (hoja de trabajo, generador de consultas, pestaña de datos) y escribir las primeras consultas sobre una tabla.

#### Desarrollo

{{% steps %}}

1. **Explora sin SQL.** En el navegador de conexiones, despliega *Tablas* → `MODULO` → pestaña *Datos*. Usa el filtro de la parte superior (escribe `cod_ciclo = 'DAW'`). Observa que la herramienta **genera** una condición SQL.

2. **Usa el generador de consultas.** Abre una hoja de trabajo, clic derecho → *Generador de consultas*. Arrastra la tabla `PROFESOR`, marca `NOMBRE`, `APELLIDOS` y `ESPECIALIDAD`, y añade el criterio `ID_DEPARTAMENTO = 1`. Pasa a la pestaña *SQL* y copia la consulta generada. Haz una captura.

3. **Escribe y ejecuta** cada consulta con `Ctrl+Intro`. Comprueba que el número de filas coincide.

    ```sql
    -- 1. Todos los grupos
    SELECT * FROM grupo;                                              -- 6 filas

    -- 2. Nombre y horas de los módulos de 2º de DAM
    SELECT nombre, horas FROM modulo WHERE cod_ciclo = 'DAM' AND curso = 2;   -- 5 filas

    -- 3. Grupos de tarde
    SELECT cod_grupo, cod_ciclo FROM grupo WHERE turno = 'T';         -- 2 filas

    -- 4. Profesorado ordenado por fecha de alta, del más antiguo al más reciente
    SELECT nombre, apellidos, fecha_alta FROM profesor ORDER BY fecha_alta;   -- 12 filas
    ```

4. **Ejecuta el script completo** con `F5` y compara: el resultado aparece como texto en la *Salida de script*, como en SQLcl.

5. **Exporta un resultado.** Clic derecho sobre la rejilla del resultado 4 → *Exportar* → formato CSV.

{{% /steps %}}

#### Comprobación

{{% comprobacion %}}
- [ ] Las cuatro consultas devuelven 6, 5, 2 y 12 filas.
- [ ] La consulta del generador es equivalente a `SELECT nombre, apellidos, especialidad FROM profesor WHERE id_departamento = 1;` y devuelve 8 filas.
- [ ] Sabes explicar la diferencia entre ejecutar con `Ctrl+Intro` y con `F5`.
{{% /comprobacion %}}

---

## Práctica 6.2 · Consultas para secretaría

{{< practica num="6.2" tipo="Autónoma" duracion="3 sesiones" nivel="2" ra="RA3: b" sgbd="Oracle 26ai · esquema EDUGEST" entrega="p6_2.sql comentado" >}}

#### Objetivo

Resolver de forma autónoma consultas reales sobre una tabla combinando proyección, selección, ordenación, operadores y eliminación de duplicados.

#### Contexto

Secretaría necesita respuestas rápidas a preguntas del día a día. Escribe una consulta para cada una. Antes de mirar la solución, comprueba que obtienes **el mismo número de filas**.

#### Enunciado

**Bloque A · Proyección y ordenación**

**A1.** Código, nombre y horas de todos los módulos de ASIR, de más a menos horas.

{{< solucion id="ud06-001" title="Solución A1" />}}

**A2.** Nombre completo del profesorado en el formato «Apellidos, Nombre», ordenado alfabéticamente, con una columna llamada `profesor`.

{{< solucion id="ud06-002" title="Solución A2" />}}

**A3.** Las distintas especialidades del profesorado, sin repetir.

{{< solucion id="ud06-003" title="Solución A3" />}}

**A4.** Los distintos pares (ciclo, curso) que existen en la tabla de módulos.

{{< solucion id="ud06-004" title="Solución A4" />}}

**Bloque B · Selección**

**B1.** Alumnado que vive en Elche o en El Campello (nombre, apellidos y localidad).

{{< solucion id="ud06-005" title="Solución B1" />}}

**B2.** Módulos que tienen entre 96 y 128 horas, ambas incluidas.

{{< solucion id="ud06-006" title="Solución B2" />}}

**B3.** Alumnado nacido antes de 2005, del mayor al menor.

{{< solucion id="ud06-007" title="Solución B3" />}}

**B4.** Profesorado del departamento 1 que **no** tiene la especialidad «Informática».

{{< solucion id="ud06-008" title="Solución B4" />}}

**B5.** Módulos cuyo nombre contiene la palabra «web» (en cualquier combinación de mayúsculas).

{{< solucion id="ud06-009" title="Solución B5" />}}

**B6.** Matrículas en segunda convocatoria o posterior (id de matrícula, alumno, módulo, convocatoria y nota).

{{< solucion id="ud06-010" title="Solución B6" />}}

**B7.** Faltas **justificadas** de 3 horas.

{{< solucion id="ud06-011" title="Solución B7" />}}

**B8.** Faltas registradas en diciembre de 2025.

{{< solucion id="ud06-012" title="Solución B8" />}}

**Bloque C · Valores nulos y límites**

**C1.** Matrículas **sin calificar**.

{{< solucion id="ud06-013" title="Solución C1" />}}

**C2.** Grupos sin tutor asignado.

{{< solucion id="ud06-014" title="Solución C2" />}}

**C3.** Las tres matrículas con peor nota (entre las calificadas), con desempate por `id_matricula`.

{{< solucion id="ud06-015" title="Solución C3" />}}

**C4.** Los dos profesores con más antigüedad en el centro.

{{< solucion id="ud06-016" title="Solución C4" />}}

#### Comprobación

{{% comprobacion %}}
- [ ] Cada consulta empieza con un comentario que repite la pregunta.
- [ ] Ninguna consulta compara con `= NULL` ni usa fechas como texto.
- [ ] Todas las consultas que devuelven listados tienen `ORDER BY`.
- [ ] El número de filas de cada consulta coincide con la solución.
{{% /comprobacion %}}

#### Errores habituales

> [!WARNING]
> - En B4, la condición `especialidad <> 'Informática'` excluye también a quien tenga la especialidad a `NULL`. En estos datos no hay ninguno, pero en una consulta real tendrías que decidir si incluirlos con `OR especialidad IS NULL`.
> - En B8, `fecha BETWEEN DATE '2025-12-01' AND DATE '2025-12-31'` no incluiría una falta del 31 a las 10:00. En estos datos todas las fechas son a las 00:00, pero acostúmbrate al intervalo semiabierto.

#### Ampliación

Escribe B5 de tres formas distintas (con `UPPER`, con `LOWER` y con `REGEXP_LIKE(nombre, 'web', 'i')`) y comprueba que dan el mismo resultado.

---

## Práctica 6.3 · Laboratorio de valores nulos

{{< practica num="6.3" tipo="Guiada" duracion="1 sesión" nivel="2" ra="RA3: b" sgbd="Oracle 26ai · esquema EDUGEST" entrega="Tabla de predicciones + resultados reales" >}}

#### Objetivo

Comprender la lógica de tres valores **prediciendo** el resultado de consultas con `NULL` antes de ejecutarlas.

#### Desarrollo

Para cada consulta, **escribe primero tu predicción** del número de filas. Después ejecútala y anota el resultado real. Si no coinciden, explica por qué.

Datos de partida: `ALUMNO` tiene 32 filas; 3 sin grupo, 4 sin DNI, 3 sin email y 5 sin teléfono. `MATRICULA` tiene 143 filas, de las que 6 están sin calificar.

| # | Consulta | Tu predicción | Real |
|---|---|---|---|
| 1 | `SELECT COUNT(*) FROM alumno WHERE dni = NULL;` | | |
| 2 | `SELECT COUNT(*) FROM alumno WHERE dni IS NULL;` | | |
| 3 | `SELECT COUNT(*) FROM alumno WHERE cod_grupo <> '1DAM';` | | |
| 4 | `SELECT COUNT(*) FROM alumno WHERE cod_grupo <> '1DAM' OR cod_grupo IS NULL;` | | |
| 5 | `SELECT COUNT(*) FROM alumno WHERE email IS NULL OR telefono IS NULL;` | | |
| 6 | `SELECT COUNT(*) FROM matricula WHERE nota_final >= 5;` | | |
| 7 | `SELECT COUNT(*) FROM matricula WHERE NOT (nota_final >= 5);` | | |
| 8 | `SELECT COUNT(*) FROM matricula WHERE NVL(nota_final, 0) < 5;` | | |
| 9 | `SELECT COUNT(*) FROM alumno WHERE cod_grupo NOT IN ('1DAM', '2DAM');` | | |
| 10 | `SELECT COUNT(*) FROM alumno WHERE cod_grupo NOT IN ('1DAM', NULL);` | | |

{{< solucion id="ud06-017" title="Resultados reales y explicación" />}}

> [!CAUTION]
> El caso 10 es una trampa clásica que aparecerá de nuevo en la UD07 con las subconsultas: `WHERE id NOT IN (SELECT ...)` no devuelve nada si la subconsulta devuelve algún `NULL`.

---

## Práctica 6.4 · Funciones para informes

{{< practica num="6.4" tipo="Autónoma" duracion="2 sesiones" nivel="2" ra="RA3: b · RA5: e" sgbd="Oracle 26ai · esquema EDUGEST" entrega="p6_4.sql comentado" >}}

#### Objetivo

Usar las funciones de fila de Oracle para transformar y presentar los datos.

#### Enunciado

**F1.** Genera la **etiqueta del casillero** de cada alumno de 1DAM: inicial del nombre, punto, primer apellido en mayúsculas y el NIA entre corchetes. Ejemplo: `A. FERRI [10450037]`.

{{< solucion id="ud06-018" title="Solución F1" />}}

**F2.** Para cada módulo de DAW, muestra el código, el nombre y una columna `duracion` con el texto «Corto» (menos de 100 horas), «Medio» (de 100 a 159) o «Largo» (160 o más).

{{< solucion id="ud06-019" title="Solución F2" />}}

**F3.** Para el profesorado, muestra el nombre, la fecha de alta con el formato «01/09/2009» y el número de **años completos** de antigüedad a fecha 1 de septiembre de 2026.

{{< solucion id="ud06-020" title="Solución F3" />}}

**F4.** Muestra el teléfono del alumnado de 2DAM de forma que, si no tiene, aparezca «Sin teléfono», y una columna `contacto` que muestre el email si existe y, si no, el teléfono.

{{< solucion id="ud06-021" title="Solución F4" />}}

**F5.** Nombre del día de la semana (en castellano) de cada falta de asistencia de la matrícula 10044.

{{< solucion id="ud06-022" title="Solución F5" />}}

**F6.** Para las matrículas del alumno 9, muestra la nota con **dos decimales** como texto (`TO_CHAR`), la nota redondeada y una columna `estado` con «Aprobado», «Suspenso» o «Pendiente».

{{< solucion id="ud06-023" title="Solución F6" />}}

#### Comprobación

{{% comprobacion %}}
- [ ] F1 funciona aunque un apellido tenga tildes.
- [ ] F3 calcula años **completos**, no la diferencia de años del calendario.
- [ ] F5 muestra los días en castellano aunque tu sesión esté en inglés.
{{% /comprobacion %}}

---

## Práctica 6.5 · Validar datos con SQL

{{< practica num="6.5" tipo="Reto" duracion="1 sesión" nivel="3" ra="RA3: b · RA5: e" sgbd="Oracle 26ai · esquema EDUGEST" entrega="p6_5.sql + informe de calidad de datos" >}}

#### Objetivo

Usar consultas y funciones del SGBD para auditar la **calidad de los datos**, una tarea profesional habitual antes de migrar o explotar una base de datos.

#### Contexto

Jefatura sospecha que hay datos mal introducidos. Te pide un informe de calidad.

#### Enunciado

1. **Letra del DNI.** La letra de un DNI es el carácter que ocupa la posición `MOD(número, 23) + 1` en la cadena `'TRWAGMYFPDXBNJZSQVHLCKE'`. Escribe una consulta que muestre el profesorado cuyo DNI tiene la letra **incorrecta**.
2. **Formato del correo.** Lista el alumnado cuyo email no cumple el patrón `texto@alu.edugest.es`.
3. **NIA.** Comprueba que todos los NIA tienen exactamente 8 dígitos numéricos.
4. **Coherencia de edades.** ¿Hay alumnado menor de 16 años a fecha 15/09/2025? ¿Y mayor de 30?
5. **Fechas de faltas.** ¿Hay faltas registradas en sábado o domingo?
6. Redacta un **informe** con los problemas encontrados y propón, para cada uno, una restricción (UD05) o un trigger (UD09) que lo habría evitado.

{{% details title="Pista para el apartado 1" %}}
```sql
SELECT nombre, apellidos, dni,
       SUBSTR('TRWAGMYFPDXBNJZSQVHLCKE', MOD(TO_NUMBER(SUBSTR(dni, 1, 8)), 23) + 1, 1) AS letra_correcta
FROM   profesor
WHERE  SUBSTR(dni, 9, 1) <> SUBSTR('TRWAGMYFPDXBNJZSQVHLCKE', MOD(TO_NUMBER(SUBSTR(dni, 1, 8)), 23) + 1, 1);
```
Debes encontrar **2** profesores con la letra incorrecta. ¿Valdría esta consulta para un NIE (que empieza por X, Y o Z)?
{{% /details %}}

{{% details title="Pista para el apartado 5" %}}
`TO_CHAR(fecha, 'D')` depende del territorio de la sesión (en unos países la semana empieza en domingo y en otros en lunes). Es más fiable `TO_CHAR(fecha, 'DY', 'NLS_DATE_LANGUAGE=ENGLISH') IN ('SAT', 'SUN')`.
{{% /details %}}

---

## Proyecto EduGest · UD06: consultas del día a día

{{< practica num="EduGest-6" tipo="Proyecto" duracion="Trabajo transversal (1 semana)" nivel="2" ra="RA3: a, b" sgbd="Oracle 26ai · esquema EDUGEST" entrega="edugest/05_consultas_basicas.sql" >}}

#### Enunciado

Entrevista (o imagina) a tres perfiles de EduGest: secretaría, tutoría y jefatura. Para cada uno, escribe **cinco preguntas** que se respondan con una consulta sobre **una sola tabla** y resuélvelas. Cada consulta debe:

1. Ir precedida de un comentario con el perfil, la pregunta y el número de filas que devuelve.
2. Usar al menos una de estas técnicas: `CASE`, una función de fecha, una función de texto, `NVL`/`COALESCE`, `FETCH FIRST`, `LIKE`, `IN` o `BETWEEN`.
3. Estar ordenada cuando devuelva un listado.

Incluye también una consulta creada con el **generador de consultas** de SQL Developer y explica qué ha generado.

#### Comprobación

{{% comprobacion %}}
- [ ] 15 consultas, todas ejecutables sin errores.
- [ ] Las técnicas indicadas aparecen al menos una vez cada una.
- [ ] Las preguntas son realistas y distintas a las de la práctica 6.2.
{{% /comprobacion %}}
