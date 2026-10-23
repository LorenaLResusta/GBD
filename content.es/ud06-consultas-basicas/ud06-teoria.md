---
title: "Consultas sobre una tabla"
weight: 1
bookToc: true
---

# UD06 · Consultas sobre una tabla y funciones

## Resumen del tema

Consultar es la operación más frecuente en cualquier base de datos. En esta unidad aprenderás la sentencia `SELECT` aplicada a **una sola tabla**: elegir columnas (proyección), filtrar filas (selección), ordenar, eliminar duplicados, tratar los valores nulos y transformar los datos con las **funciones** que proporciona Oracle. En la UD07 combinaremos varias tablas y agruparemos resultados.

Todos los ejemplos se ejecutan sobre el esquema de referencia **EDUGEST** cargado con los [scripts del proyecto](/guia/proyecto-edugest#4-scripts-descargables), y muestran el resultado que debes obtener.

{{< ra "RA3:a,b" "RA5:e" >}}

### Temporalización

La unidad ocupa **23 horas de aula** (12 de teoría y 11 de práctica). Es la unidad con más horas del curso: aquí se adquiere la destreza con `SELECT` que se utilizará hasta el final del módulo.

{{< sesiones unidad="UD06" horas="23" >}}
items:
  - {h: 2, tipo: T, t: "Herramientas y sentencia SELECT. Proyección, alias, concatenación y DISTINCT", ref: "§1 y §2"}
  - {h: 1, tipo: P, t: "Primeras consultas y herramientas", ref: "Práctica 6.1"}
  - {h: 2, tipo: T, t: "Ordenación y selección con WHERE: comparación, LIKE y operadores lógicos", ref: "§3 y §4 · laboratorio de SELECT"}
  - {h: 3, tipo: P, t: "Consultas para secretaría", ref: "Práctica 6.2"}
  - {h: 2, tipo: T, t: "El valor NULL y la lógica de tres valores", ref: "§5 · simulador de lógica trivalente"}
  - {h: 2, tipo: P, t: "Laboratorio de valores nulos", ref: "Práctica 6.3"}
  - {h: 1, tipo: T, t: "Limitar el número de filas", ref: "§6"}
  - {h: 3, tipo: T, t: "Funciones de fila (I): texto, numéricas y de fecha", ref: "§7.1 a §7.3"}
  - {h: 2, tipo: T, t: "Funciones de fila (II): conversión, CASE, DECODE y expresiones regulares", ref: "§7.4 a §7.6"}
  - {h: 3, tipo: P, t: "Funciones para informes", ref: "Práctica 6.4"}
  - {h: 1, tipo: P, t: "Validar datos con SQL", ref: "Práctica 6.5"}
  - {h: 1, tipo: P, t: "Consultas del día a día en EduGest", ref: "Proyecto EduGest-6"}
autonomo:
  - "Terminar las consultas de la práctica 6.2 que no hayan dado tiempo en el aula"
  - "Ampliaciones de las prácticas 6.3, 6.4 y 6.5"
{{< /sesiones >}}

> [!IMPORTANT]
> Las consultas **se aprenden escribiéndolas**. Antes de ejecutar cada una, predice cuántas filas devolverá y por qué; después compruébalo. Los laboratorios interactivos simulan el comportamiento de Oracle sobre los datos reales de EduGest, pero no sustituyen a un SGBD.

### Objetivos de aprendizaje

Al terminar esta unidad serás capaz de:

- Identificar las herramientas y las cláusulas de la sentencia `SELECT`.
- Seleccionar columnas, calcular expresiones y usar alias.
- Filtrar filas con operadores de comparación, lógicos, `BETWEEN`, `IN`, `LIKE` e `IS NULL`.
- Ordenar resultados y limitar el número de filas.
- Razonar con la lógica de tres valores que introduce `NULL`.
- Usar funciones de texto, numéricas, de fecha, de conversión y condicionales de Oracle.

> [!TIP]
> **Prepara tu sesión** para que las fechas y los números se vean como en estos apuntes. Ejecuta al conectarte:
>
> ```sql
> ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY';
> ALTER SESSION SET NLS_NUMERIC_CHARACTERS = '.,';
> ```
>
> El formato de presentación **no** cambia los datos guardados, solo cómo se muestran.

---

{{< sesion n="1" h="2" tipo="t" >}}Herramientas, SELECT y proyección{{< /sesion >}}

## 1. Herramientas y sentencias para consultar

Para consultar una base de datos Oracle puedes usar:

| Herramienta | Uso |
|---|---|
| **Hoja de trabajo SQL** de SQL Developer o VS Code | Escribir y ejecutar consultas (`Ctrl+Intro`); el resultado aparece en una rejilla |
| **Generador de consultas** (*Query Builder*) de SQL Developer | Construir la consulta arrastrando tablas y marcando columnas; genera el SQL |
| **SQLcl / SQL\*Plus** | Línea de órdenes; ideal para scripts y para guardar evidencias con `SPOOL` |
| **Pestaña *Datos*** de una tabla en SQL Developer | Ver y filtrar el contenido sin escribir SQL |

La sentencia para consultar es `SELECT`. Su forma general, con todas las cláusulas que verás en esta unidad y en la siguiente, es:

```sql
SELECT    [DISTINCT] columnas o expresiones      -- 5. qué columnas
FROM      tabla(s)                               -- 1. de dónde
WHERE     condición sobre las filas              -- 2. qué filas
GROUP BY  columnas de agrupación                 -- 3. cómo agrupar        (UD07)
HAVING    condición sobre los grupos             -- 4. qué grupos          (UD07)
ORDER BY  criterios de ordenación                -- 6. en qué orden
FETCH FIRST n ROWS ONLY;                         -- 7. cuántas filas
```

> [!IMPORTANT]
> El **orden en que se escribe** una consulta no es el **orden en que se evalúa**. El SGBD procesa primero `FROM`, después `WHERE`, `GROUP BY`, `HAVING`, `SELECT` y finalmente `ORDER BY`. Por eso un alias definido en el `SELECT` **se puede usar en `ORDER BY`** pero **no en `WHERE`**.

---

## 2. Proyección: elegir columnas

### 2.1 Todas las columnas o solo algunas

```sql
SELECT * FROM ciclo;
```


| COD_CICLO | NOMBRE | GRADO | HORAS_TOTALES |
|---|---|---|---|
| DAM | Desarrollo de Aplicaciones Multiplataforma | SUPERIOR | 2000 |
| DAW | Desarrollo de Aplicaciones Web | SUPERIOR | 2000 |
| ASIR | Administración de Sistemas Informáticos en Red | SUPERIOR | 2000 |
| SMR | Sistemas Microinformáticos y Redes | MEDIO | 2000 |

*4 filas*


`*` es útil para explorar, pero en una aplicación o un informe escribe siempre las columnas que necesitas: el resultado es más claro, transfiere menos datos y no cambia si alguien añade una columna a la tabla.

```sql
SELECT codigo, nombre, horas
FROM   modulo
WHERE  cod_ciclo = 'DAM';
```

### 2.2 Expresiones y alias

En el `SELECT` se pueden calcular **expresiones**. Un **alias** da nombre a la columna resultante; si contiene espacios o mayúsculas, va entre comillas dobles.

```sql
SELECT codigo,
       nombre,
       horas,
       horas / 32            AS horas_semana,
       ROUND(horas / 32, 1)  AS "Horas/semana"
FROM   modulo
WHERE  cod_ciclo = 'DAW' AND curso = 2;
```


| CODIGO | NOMBRE | HORAS | HORAS_SEMANA | Horas/semana |
|---|---|---|---|---|
| 0612 | Desarrollo web en entorno cliente | 140 | 4.375 | 4.4 |
| 0613 | Desarrollo web en entorno servidor | 160 | 5 | 5 |
| 0614 | Despliegue de aplicaciones web | 80 | 2.5 | 2.5 |
| 0615 | Diseño de interfaces web | 120 | 3.75 | 3.8 |

*4 filas*


### 2.3 Concatenación

El operador `||` une cadenas:

```sql
SELECT apellidos || ', ' || nombre AS alumno, localidad
FROM   alumno
WHERE  cod_grupo = '2DAW'
ORDER  BY alumno;
```


| ALUMNO | LOCALIDAD |
|---|---|
| Amorós Guillem, Sara | Mutxamel |
| Carbonell Soriano, Elena | El Campello |
| Planelles Marco, Sofía | Elche |
| Sala Brotons, Mateo | Alicante |
| Verdú Castelló, Nicolás | Alicante |

*5 filas*


### 2.4 Eliminar duplicados con DISTINCT

```sql
SELECT DISTINCT localidad FROM alumno ORDER BY localidad;
```


| LOCALIDAD |
|---|
| Alicante |
| El Campello |
| Elche |
| Mutxamel |
| San Vicente del Raspeig |
| Sant Joan d'Alacant |

*6 filas*


`DISTINCT` se aplica a la **fila completa** del resultado: `SELECT DISTINCT localidad, cod_grupo` devuelve las combinaciones distintas de las dos columnas.

{{% curiosidad titulo="La tabla DUAL tiene un nombre por una razón" %}}
Según su creador, Chuck Weiss, `DUAL` se diseñó al principio con **dos filas**, para poder duplicar filas con un join. Hoy tiene una sola, pero conserva el nombre: sirve para evaluar expresiones, como `SELECT SYSDATE FROM DUAL`.
{{% /curiosidad %}}

### 2.5 La tabla DUAL

`DUAL` es una tabla especial de Oracle con una sola fila. Sirve para evaluar expresiones que no dependen de ninguna tabla:

```sql
SELECT SYSDATE, 7 * 24 AS horas_semana, UPPER('edugest') FROM dual;
```

> [!NOTE]
> Desde **Oracle 23ai** la cláusula `FROM` es opcional en estos casos: `SELECT SYSDATE;` también funciona. En versiones anteriores (y en el examen, si usas 19c) escribe `FROM dual`.

---

{{< quiz >}}
- q: "¿Qué devuelve `SELECT DISTINCT localidad FROM alumno`?"
  options: ["Una fila por alumno", "Cada localidad una sola vez (el `NULL` cuenta como un valor más)", "Solo las localidades sin alumnos", "Un error: falta `GROUP BY`"]
  answer: 1
  explain: "`DISTINCT` elimina filas duplicadas del resultado. Considera iguales a dos `NULL`, de modo que aparece como mucho una fila nula."
- q: "En Oracle 26ai, ¿cómo se evalúa una expresión como `1+1` sin consultar ninguna tabla?"
  options: ["Solo es posible con `FROM dual`", "Con `FROM dual` (válido en todas las versiones) o, desde 23ai, sin `FROM`", "No es posible: toda consulta necesita una tabla real", "Con `VALUES (1+1)`"]
  answer: 1
  explain: "`DUAL` es una tabla de una fila y una columna. Oracle exigía `FROM` hasta la 21c; desde 23ai se admite omitirlo, pero para código portable a versiones anteriores se usa `DUAL`."
{{< /quiz >}}

---

{{< sesion n="3" h="2" tipo="t" >}}Ordenación y selección{{< /sesion >}}

## 3. Ordenación: ORDER BY

```sql
SELECT codigo, nombre, cod_ciclo, horas
FROM   modulo
WHERE  horas > 150
ORDER  BY horas DESC, codigo;
```


| CODIGO | NOMBRE | COD_CICLO | HORAS |
|---|---|---|---|
| 0485 | Programación | DAM | 256 |
| 0485 | Programación | DAW | 256 |
| 0369 | Implantación de sistemas operativos | ASIR | 224 |
| 0370 | Planificación y administración de redes | ASIR | 192 |
| 0372 | Gestión de bases de datos | ASIR | 160 |
| 0483 | Sistemas informáticos | DAM | 160 |
| 0483 | Sistemas informáticos | DAW | 160 |
| 0484 | Bases de datos | DAM | 160 |
| 0484 | Bases de datos | DAW | 160 |
| 0613 | Desarrollo web en entorno servidor | DAW | 160 |

*10 filas*


- `ASC` (por defecto) ordena de menor a mayor y `DESC` de mayor a menor.
- Con varias columnas, la segunda solo decide cuando hay empate en la primera.
- Se puede ordenar por un **alias** o por una expresión.
- En Oracle, los `NULL` van **al final** en orden ascendente y **al principio** en descendente. Puedes cambiarlo con `NULLS FIRST` o `NULLS LAST`.

> [!WARNING]
> **Sin `ORDER BY`, el orden de las filas no está garantizado.** Aunque hoy salgan ordenadas por la clave primaria, mañana pueden salir en otro orden.
>
> Además, la ordenación de textos con tildes depende del parámetro de sesión `NLS_SORT`. Con el valor por defecto (`BINARY`), «Álex» se ordena **después** de «Zoe». Con `ALTER SESSION SET NLS_SORT = SPANISH;` se ordena como en un diccionario. Si tus resultados aparecen en otro orden que en los apuntes, revisa este parámetro.

---

{{% paso-a-paso titulo="En qué orden evalúa Oracle un SELECT sencillo" %}}
{{% etapa titulo="1. FROM" %}}
Primero decide **de dónde** salen las filas: `FROM alumno`. Por eso el alias de una columna definido en el SELECT no se puede usar todavía.
{{% /etapa %}}
{{% etapa titulo="2. WHERE" %}}
Descarta las filas que no cumplen la condición: `WHERE nota >= 5`. Aquí solo existen las columnas de la tabla.
{{% /etapa %}}
{{% etapa titulo="3. SELECT" %}}
Calcula las expresiones y los alias de las columnas que se muestran: `SELECT nombre, nota * 10 AS sobre_100`.
{{% /etapa %}}
{{% etapa titulo="4. ORDER BY" %}}
Ordena el resultado. Es la **única** cláusula que puede usar los alias del SELECT.
{{% /etapa %}}
{{% etapa titulo="5. Límite de filas" %}}
Por último se recorta con `FETCH FIRST n ROWS ONLY`. En la UD07 se añadirán `GROUP BY` y `HAVING` entre el WHERE y el SELECT.
{{% /etapa %}}
{{% /paso-a-paso %}}

## 4. Selección: filtrar filas con WHERE

### 4.1 Operadores de comparación

| Operador | Significado | Ejemplo |
|---|---|---|
| `=` | Igual | `cod_grupo = '1DAM'` |
| `<>` o `!=` | Distinto | `turno <> 'M'` |
| `<`, `>`, `<=`, `>=` | Menor, mayor... | `nota_final >= 5` |
| `BETWEEN a AND b` | Entre a y b, **ambos incluidos** | `horas BETWEEN 100 AND 160` |
| `IN (lista)` | Igual a alguno de la lista | `cod_ciclo IN ('DAM', 'DAW')` |
| `LIKE patrón` | Coincide con un patrón | `apellidos LIKE 'B%'` |
| `IS NULL` / `IS NOT NULL` | Es (o no es) nulo | `cod_grupo IS NULL` |

```sql
SELECT nombre, apellidos, localidad
FROM   alumno
WHERE  localidad = 'Mutxamel'
ORDER  BY apellidos;
```


| NOMBRE | APELLIDOS | LOCALIDAD |
|---|---|---|
| Martina | Alemany Vidal | Mutxamel |
| Sara | Amorós Guillem | Mutxamel |
| Irene | Belda Iborra | Mutxamel |
| Hugo | Brotons Iborra | Mutxamel |
| Álex | Tomás Vidal | Mutxamel |
| Alba | Torregrosa Planelles | Mutxamel |

*6 filas*


> [!WARNING]
> Las comparaciones de texto **distinguen mayúsculas y minúsculas**: `localidad = 'mutxamel'` no devuelve nada. Para comparar sin distinguirlas usa `UPPER(localidad) = 'MUTXAMEL'`.

### 4.2 Patrones con LIKE

| Comodín | Significado | Ejemplo | Coincide con |
|---|---|---|---|
| `%` | Cualquier secuencia de caracteres (incluso vacía) | `'B%'` | Belda, Brotons |
| `_` | Exactamente un carácter | `'_DAM'` | 1DAM, 2DAM |

```sql
SELECT nombre, apellidos
FROM   alumno
WHERE  apellidos LIKE 'B%'
ORDER  BY apellidos;
```


| NOMBRE | APELLIDOS |
|---|---|
| Irene | Belda Iborra |
| Lucía | Belda Quiles |
| Hugo | Brotons Iborra |
| Andrea | Brotons Soriano |

*4 filas*


Para buscar un `%` o un `_` literales se usa `ESCAPE`: `email LIKE '%\_%' ESCAPE '\'` busca correos que contengan un guion bajo.

### 4.3 Operadores lógicos y precedencia

`NOT` se evalúa antes que `AND`, y `AND` antes que `OR`. Usa **paréntesis** siempre que mezcles `AND` y `OR`.

```sql
-- Matrículas suspendidas de los módulos 2 u 8
SELECT id_matricula, id_alumno, nota_final
FROM   matricula
WHERE  nota_final < 5
AND    id_modulo IN (2, 8)
ORDER  BY id_matricula;
```


| ID_MATRICULA | ID_ALUMNO | NOTA_FINAL |
|---|---|---|
| 10002 | 1 | 4.75 |
| 10007 | 2 | 4.75 |
| 10038 | 8 | 4 |

*3 filas*


{{% details title="¿Qué devolvería `WHERE nota_final < 5 AND id_modulo = 2 OR id_modulo = 8`?" %}}
Por la precedencia, se evalúa como `(nota_final < 5 AND id_modulo = 2) OR id_modulo = 8`: devolvería los suspensos del módulo 2 **y todas** las matrículas del módulo 8, aprobadas o no. Por eso hay que poner paréntesis, o usar `IN`.
{{% /details %}}

#### Laboratorio de `SELECT`

Construye una consulta sobre la tabla `ALUMNO` eligiendo columnas, condiciones y orden. Compara el resultado con el que predijiste.

{{< select-lab >}}

> [!WARNING]
> `WHERE a OR b AND c` **no** se evalúa de izquierda a derecha: `AND` tiene mayor precedencia que `OR`. Usa paréntesis siempre que mezcles ambos.

{{< quiz >}}
- q: "`WHERE nombre LIKE 'M_ría'` ¿qué cadenas cumplen el patrón?"
  options: ["Las que empiezan por M y terminan en ría, con cualquier número de caracteres en medio", "Las que tienen exactamente un carácter entre `M` y `ría` (María, Mería...)", "Solo la cadena literal `M_ría`", "Ninguna: `_` no se admite en `LIKE`"]
  answer: 1
  explain: "`%` sustituye a cero o más caracteres y `_` a exactamente uno."
- q: "¿Cuál es la forma correcta de buscar las matrículas sin nota?"
  options: ["`WHERE nota_final = NULL`", "`WHERE nota_final IS NULL`", "`WHERE nota_final == NULL`", "`WHERE NOT nota_final`"]
  answer: 1
  explain: "Cualquier comparación con `NULL` mediante `=` da `UNKNOWN`, y `WHERE` solo conserva las filas `TRUE`. Se debe usar `IS NULL`."
{{< /quiz >}}

---

{{< sesion n="5" h="2" tipo="t" >}}El valor NULL{{< /sesion >}}

{{% curiosidad titulo="NULL no es cero ni «vacío»" %}}
`NULL` significa «valor desconocido». Por eso `NULL = NULL` no es verdadero, sino desconocido, y por eso SQL usa una lógica de **tres valores**: verdadero, falso y desconocido.
{{% /curiosidad %}}

## 5. El valor NULL

`NULL` significa **«valor desconocido o no aplicable»**. No es un cero ni una cadena vacía: es la ausencia de valor.

### 5.1 Lógica de tres valores

Cualquier comparación con `NULL` da como resultado **desconocido** (`UNKNOWN`), y `WHERE` solo devuelve las filas cuya condición es **verdadera**.

| A | B | A AND B | A OR B | NOT A |
|---|---|---|---|---|
| V | V | V | V | F |
| V | F | F | V | F |
| V | ? | ? | V | F |
| F | ? | F | ? | V |
| ? | ? | ? | ? | ? |

Consecuencias prácticas:

```sql
SELECT COUNT(*) FROM alumno WHERE cod_grupo = NULL;      -- 0 filas: ¡siempre!
SELECT COUNT(*) FROM alumno WHERE cod_grupo IS NULL;     -- 3 filas
SELECT COUNT(*) FROM alumno WHERE cod_grupo <> '1DAM';   -- 22: los 3 sin grupo NO salen
```

```sql
SELECT nia, nombre, apellidos
FROM   alumno
WHERE  cod_grupo IS NULL;
```


| NIA | NOMBRE | APELLIDOS |
|---|---|---|
| 10451110 | Zoe | Iborra Valero |
| 10451147 | Lucas | Agulló Cerdá |
| 10451184 | Irene | Belda Iborra |

*3 filas*


#### Simulador de lógica de tres valores

Combina `TRUE`, `FALSE` y `UNKNOWN` con `AND`, `OR` y `NOT`, y comprueba qué filas conserva `WHERE`.

{{< null-logic >}}

{{< quiz >}}
- q: "`TRUE AND UNKNOWN` vale…"
  options: ["`TRUE`", "`FALSE`", "`UNKNOWN`", "Error"]
  answer: 2
  explain: "Si un operando es `UNKNOWN` y el otro no decide el resultado, el resultado es `UNKNOWN`. En cambio, `FALSE AND UNKNOWN` es `FALSE`."
- q: "`WHERE nota_final NOT IN (5, NULL)` ¿qué devuelve?"
  options: ["Las notas distintas de 5", "Ninguna fila", "Solo las filas con nota nula", "Error de sintaxis"]
  answer: 1
  explain: "`x NOT IN (5, NULL)` equivale a `x <> 5 AND x <> NULL`; la segunda parte es `UNKNOWN` y la conjunción nunca llega a `TRUE`. Es una trampa clásica."
{{< /quiz >}}

### 5.2 Funciones para tratar los nulos

| Función | Devuelve | Ejemplo |
|---|---|---|
| `NVL(expr, valor)` | `valor` si `expr` es nulo; si no, `expr` | `NVL(email, '(sin correo)')` |
| `NVL2(expr, si_no_nulo, si_nulo)` | Un valor u otro según `expr` sea nulo | `NVL2(id_tutor, 'Con tutor', 'Sin tutor')` |
| `COALESCE(e1, e2, ...)` | El primer valor no nulo (estándar SQL) | `COALESCE(email, telefono, 'sin contacto')` |
| `NULLIF(a, b)` | `NULL` si a = b; si no, a | `NULLIF(horas, 0)` evita dividir por cero |

```sql
SELECT id_alumno, nombre, NVL(email, '(sin correo)') AS email
FROM   alumno
WHERE  email IS NULL OR telefono IS NULL
ORDER  BY id_alumno;
```


| ID_ALUMNO | NOMBRE | EMAIL |
|---|---|---|
| 4 | Paula | paulaferri4@alu.edugest.es |
| 8 | Iván | (sin correo) |
| 10 | Nerea | nereacerda10@alu.edugest.es |
| 16 | Julia | juliaespi16@alu.edugest.es |
| 19 | Alba | (sin correo) |
| 22 | Sofía | sofiaplanelles22@alu.edugest.es |
| 28 | Pablo | pabloamoros28@alu.edugest.es |
| 30 | Zoe | (sin correo) |

*8 filas*


> [!CAUTION]
> Cualquier operación aritmética con `NULL` da `NULL`: `nota_final + 1` es `NULL` si no hay nota. Y en Oracle, `''` **es** `NULL`. Compruébalo con `SELECT NVL('', 'era nulo') FROM dual;`.

---

{{< sesion n="7" h="1" tipo="t" >}}Limitar el número de filas{{< /sesion >}}

## 6. Limitar el número de filas

```sql
-- Las cinco mejores notas (con desempate por id_matricula)
SELECT id_matricula, id_alumno, id_modulo, nota_final
FROM   matricula
WHERE  nota_final IS NOT NULL
ORDER  BY nota_final DESC, id_matricula
FETCH FIRST 5 ROWS ONLY;
```


| ID_MATRICULA | ID_ALUMNO | ID_MODULO | NOTA_FINAL |
|---|---|---|---|
| 10143 | 29 | 24 | 10 |
| 10045 | 9 | 10 | 9.75 |
| 10132 | 27 | 23 | 9.75 |
| 10020 | 4 | 5 | 9.5 |
| 10048 | 10 | 8 | 9.25 |

*5 filas*


| Variante | Efecto |
|---|---|
| `FETCH FIRST 5 ROWS ONLY` | Las 5 primeras filas |
| `FETCH FIRST 5 ROWS WITH TIES` | Las 5 primeras y las empatadas con la quinta |
| `OFFSET 10 ROWS FETCH NEXT 10 ROWS ONLY` | Filas 11 a 20 (paginación) |
| `FETCH FIRST 10 PERCENT ROWS ONLY` | El 10 % de las filas |

> [!NOTE]
> `FETCH FIRST` es SQL estándar y está en Oracle desde la versión 12c. En código antiguo verás la pseudocolumna `ROWNUM` (`WHERE ROWNUM <= 5`), que se evalúa **antes** del `ORDER BY` y produce errores si no se usa con una subconsulta. MySQL y PostgreSQL usan `LIMIT 5`.

---

{{< sesion n="8" h="3" tipo="t" >}}Funciones de fila: texto, numéricas y de fecha{{< /sesion >}}

## 7. Funciones de fila

Las **funciones de fila** se aplican a cada fila y devuelven un valor por fila. Forman parte de las funciones que proporciona el sistema gestor (RA5.e). Las **funciones de grupo** (`COUNT`, `SUM`, `AVG`...), que resumen varias filas, se estudian en la UD07.

### 7.1 Funciones de texto

| Función | Resultado de ejemplo |
|---|---|
| `UPPER('Bases de Datos')` / `LOWER(...)` | `BASES DE DATOS` / `bases de datos` |
| `INITCAP('marta soler')` | `Marta Soler` |
| `LENGTH('Oracle')` | `6` |
| `SUBSTR('10450037', 1, 4)` | `1045` (desde la posición 1, 4 caracteres) |
| `INSTR('msoler@edugest.es', '@')` | `7` (posición de la primera @) |
| `TRIM('  hola  ')`, `LTRIM`, `RTRIM` | `hola` |
| `LPAD('7', 3, '0')` / `RPAD('7', 3, '*')` | `007` / `7**` |
| `REPLACE('1DAM', 'DAM', 'DAW')` | `1DAW` |
| `CONCAT('a', 'b')` | `ab` (solo dos argumentos; mejor `\|\|`) |

```sql
-- Usuario del correo del profesorado (lo que va antes de la @)
SELECT nombre, email, SUBSTR(email, 1, INSTR(email, '@') - 1) AS usuario
FROM   profesor
WHERE  id_departamento = 2;
```

| NOMBRE | EMAIL | USUARIO |
|---|---|---|
| Carmen | cortiz@edugest.es | cortiz |
| Sergio | sramos@edugest.es | sramos |

```sql
SELECT UPPER(apellidos) || ', ' || nombre AS alumno, LENGTH(nombre) AS letras
FROM   alumno
WHERE  cod_grupo = '1ASIR'
ORDER  BY apellidos;
```

| ALUMNO | LETRAS |
|---|---|
| AMORÓS CARBONELL, Pablo | 5 |
| IBORRA TORREGROSA, Diego | 5 |
| PASCUAL BROTONS, Aitana | 6 |
| TOMÁS GUILLEM, Víctor | 6 |
| TOMÁS VIDAL, Álex | 4 |

### 7.2 Funciones numéricas

| Función | Resultado |
|---|---|
| `ROUND(7.256, 2)` / `ROUND(7.5)` | `7.26` / `8` |
| `TRUNC(7.256, 1)` / `TRUNC(7.9)` | `7.2` / `7` |
| `CEIL(4.1)` / `FLOOR(4.9)` | `5` / `4` |
| `MOD(17, 5)` | `2` (resto) |
| `ABS(-3)`, `POWER(2, 10)`, `SQRT(81)` | `3`, `1024`, `9` |

```sql
-- Notas redondeadas al entero, como aparecen en el boletín
SELECT id_matricula, nota_final, ROUND(nota_final) AS nota_boletin, TRUNC(nota_final) AS nota_truncada
FROM   matricula
WHERE  id_alumno = 1
ORDER  BY id_matricula;
```

| ID_MATRICULA | NOTA_FINAL | NOTA_BOLETIN | NOTA_TRUNCADA |
|---|---|---|---|
| 10001 | 8.75 | 9 | 8 |
| 10002 | 4.75 | 5 | 4 |
| 10003 | 7.25 | 7 | 7 |
| 10004 | 4.75 | 5 | 4 |
| 10005 | 6.75 | 7 | 6 |

> [!WARNING]
> Fíjate en la matrícula 10002: con `ROUND`, un 4,75 aparece como **5** en el boletín, pero el módulo está **suspendido**. Las decisiones (aprobar o no) se toman siempre sobre el **valor real**, nunca sobre el valor formateado.

### 7.3 Funciones de fecha

En Oracle, restar dos fechas da el número de **días** entre ellas, y sumar un número a una fecha añade días.

| Función | Resultado |
|---|---|
| `SYSDATE` / `SYSTIMESTAMP` | Fecha y hora actuales del servidor |
| `ADD_MONTHS(DATE '2026-01-31', 1)` | `28/02/2026` |
| `MONTHS_BETWEEN(fecha1, fecha2)` | Meses entre dos fechas (con decimales) |
| `EXTRACT(YEAR FROM fecha)` | El año (también `MONTH`, `DAY`) |
| `TRUNC(SYSDATE)` | La fecha de hoy a las 00:00:00 |
| `LAST_DAY(DATE '2026-02-10')` | `28/02/2026` |
| `NEXT_DAY(DATE '2026-10-06', 'LUNES')` | El lunes siguiente (el nombre depende del idioma de la sesión) |

```sql
-- Edad del alumnado de 2DAW a fecha 6 de octubre de 2026
SELECT id_alumno, nombre, fecha_nacimiento,
       TRUNC(MONTHS_BETWEEN(DATE '2026-10-06', fecha_nacimiento) / 12) AS edad
FROM   alumno
WHERE  cod_grupo = '2DAW'
ORDER  BY fecha_nacimiento;
```

| ID_ALUMNO | NOMBRE | FECHA_NACIMIENTO | EDAD |
|---|---|---|---|
| 23 | Sara | 07/08/2000 | 26 |
| 20 | Mateo | 09/04/2003 | 23 |
| 22 | Sofía | 13/07/2004 | 22 |
| 24 | Nicolás | 11/05/2005 | 21 |
| 21 | Elena | 21/06/2005 | 21 |

> [!TIP]
> En una aplicación real se usaría `SYSDATE` en lugar de `DATE '2026-10-06'`. Aquí se fija la fecha para que el resultado no cambie según el día en que ejecutes la consulta. Los **literales de fecha** `DATE 'AAAA-MM-DD'` son SQL estándar y no dependen de la configuración de la sesión: úsalos siempre en lugar de cadenas como `'15/09/2025'`.

**Comparar fechas que tienen hora.** Como `DATE` guarda la hora, para buscar «lo del día 15» compara con un intervalo semiabierto:

```sql
SELECT * FROM matricula
WHERE  fecha_matricula >= DATE '2025-09-15'
AND    fecha_matricula <  DATE '2025-09-16';
```

{{< sesion n="9" h="2" tipo="t" >}}Conversión, CASE y expresiones regulares{{< /sesion >}}

### 7.4 Funciones de conversión

| Función | Uso | Ejemplo | Resultado |
|---|---|---|---|
| `TO_CHAR(fecha, formato)` | Fecha → texto | `TO_CHAR(DATE '2026-10-06', 'DD/MM/YYYY')` | `06/10/2026` |
| | | `TO_CHAR(DATE '2026-10-06', 'fmDay, DD "de" Month', 'NLS_DATE_LANGUAGE=SPANISH')` | `Martes, 6 de Octubre` |
| `TO_CHAR(número, formato)` | Número → texto | `TO_CHAR(1520.5, '9G990D00')` | `1,520.50` (según NLS) |
| `TO_DATE(texto, formato)` | Texto → fecha | `TO_DATE('15/09/2025', 'DD/MM/YYYY')` | fecha |
| `TO_NUMBER(texto)` | Texto → número | `TO_NUMBER('42')` | `42` |

Elementos de formato de fecha más usados: `DD` (día), `MM` (mes), `MON`/`MONTH` (nombre del mes), `YYYY` (año), `HH24` (hora), `MI` (minutos), `SS` (segundos), `D` (día de la semana), `Q` (trimestre).

```sql
SELECT nombre, apellidos,
       TO_CHAR(fecha_alta, 'DD/MM/YYYY') AS alta,
       EXTRACT(YEAR FROM DATE '2026-10-06') - EXTRACT(YEAR FROM fecha_alta) AS cursos_aprox
FROM   profesor
WHERE  fecha_alta < DATE '2015-01-01'
ORDER  BY fecha_alta;
```

| NOMBRE | APELLIDOS | ALTA | CURSOS_APROX |
|---|---|---|---|
| Marta | Soler Ivars | 01/09/2009 | 17 |
| Carmen | Ortiz Llorca | 01/09/2010 | 16 |
| Javier | Pastor Gil | 01/09/2012 | 14 |

> [!WARNING]
> Evita las **conversiones implícitas**: `WHERE fecha_alta < '01/01/2015'` funciona o falla según el `NLS_DATE_FORMAT` de cada sesión, y `WHERE nia = 10450037` (sin comillas) obliga a Oracle a convertir **todas** las filas de la columna, lo que impide usar su índice.

### 7.5 Funciones condicionales: CASE y DECODE

`CASE` es estándar SQL y permite elegir un valor según condiciones.

```sql
SELECT id_matricula, id_modulo, nota_final,
       CASE
           WHEN nota_final IS NULL THEN 'Sin calificar'
           WHEN nota_final < 5     THEN 'Insuficiente'
           WHEN nota_final < 6     THEN 'Suficiente'
           WHEN nota_final < 7     THEN 'Bien'
           WHEN nota_final < 9     THEN 'Notable'
           ELSE                         'Sobresaliente'
       END AS calificacion
FROM   matricula
WHERE  id_alumno = 1
ORDER  BY id_modulo;
```


| ID_MATRICULA | ID_MODULO | NOTA_FINAL | CALIFICACION |
|---|---|---|---|
| 10001 | 1 | 8.75 | Notable |
| 10002 | 2 | 4.75 | Insuficiente |
| 10003 | 3 | 7.25 | Notable |
| 10004 | 4 | 4.75 | Insuficiente |
| 10005 | 5 | 6.75 | Bien |

*5 filas*


Las condiciones se evalúan **en orden** y se usa la primera que se cumple. Por eso basta con `nota_final < 6` en la segunda rama: si fuera menor que 5, ya se habría quedado en la primera.

**CASE simple** (compara una expresión con valores) y su equivalente propio de Oracle, `DECODE`:

```sql
SELECT cod_grupo,
       CASE turno WHEN 'M' THEN 'Mañana' WHEN 'T' THEN 'Tarde' END AS turno,
       DECODE(turno, 'M', 'Mañana', 'T', 'Tarde', 'Desconocido') AS turno_decode
FROM   grupo
ORDER  BY cod_grupo;
```


| COD_GRUPO | TURNO | TURNO_DECODE |
|---|---|---|
| 1ASIR | Mañana | Mañana |
| 1DAM | Mañana | Mañana |
| 1DAW | Tarde | Tarde |
| 2ASIR | Mañana | Mañana |
| 2DAM | Mañana | Mañana |
| 2DAW | Tarde | Tarde |

*6 filas*


### 7.6 Expresiones regulares

Oracle incluye funciones de expresiones regulares para búsquedas más potentes que `LIKE`: `REGEXP_LIKE`, `REGEXP_SUBSTR`, `REGEXP_REPLACE`, `REGEXP_INSTR`, `REGEXP_COUNT`.

```sql
-- Profesorado con DNI que empieza por 2 y termina en C o E
SELECT nombre, dni FROM profesor WHERE REGEXP_LIKE(dni, '^2[0-9]{7}[CE]$') ORDER BY nombre;
```

| NOMBRE | DNI |
|---|---|
| Carmen | 21369874E |
| Marta | 21456789C |

---

## 8. Errores frecuentes

| Error | Ejemplo | Corrección |
|---|---|---|
| Comparar con `= NULL` | `WHERE email = NULL` | `WHERE email IS NULL` |
| Usar un alias del `SELECT` en el `WHERE` | `WHERE edad > 20` | Repite la expresión o usa una subconsulta (UD07) |
| Comillas dobles para textos | `WHERE turno = "M"` | Los textos van entre comillas **simples**; las dobles son para identificadores (ORA-00904) |
| Olvidar paréntesis al mezclar `AND` y `OR` | `a AND b OR c` | `a AND (b OR c)` |
| Confiar en el orden sin `ORDER BY` | — | Ordena siempre que el orden importe |
| Comparar fechas con texto | `fecha > '01/09/2025'` | `fecha > DATE '2025-09-01'` |
| `BETWEEN` con fechas con hora | `BETWEEN DATE '2025-09-15' AND DATE '2025-09-15'` | Intervalo semiabierto `>=` y `<` |

## 9. Buenas prácticas

- Escribe las palabras reservadas en mayúsculas y alinea las cláusulas: la consulta se lee mejor.
- Nombra explícitamente las columnas; usa `*` solo para explorar.
- Usa alias claros para las expresiones calculadas.
- Usa literales `DATE 'AAAA-MM-DD'` y evita las conversiones implícitas.
- Comenta las consultas que entregues: qué pregunta responden y qué decisiones has tomado.

---

{{< tarjetas titulo="Repasa los términos de la UD06" >}}
- t: "Proyección"
  d: "Elegir columnas: la lista del SELECT."
- t: "Selección"
  d: "Elegir filas: la condición del WHERE."
- t: "Alias"
  d: "Nombre alternativo para una columna o una tabla en la consulta."
- t: "DISTINCT"
  d: "Elimina del resultado las filas duplicadas."
- t: "LIKE"
  d: "Compara con un patrón: % (cualquier texto) y _ (un carácter)."
- t: "IS NULL"
  d: "Único modo correcto de comprobar si un valor es nulo."
{{< /tarjetas >}}

## 10. Resumen

- `SELECT` elige columnas (**proyección**), `WHERE` filtra filas (**selección**) y `ORDER BY` ordena.
- El SGBD evalúa `FROM` → `WHERE` → `SELECT` → `ORDER BY`.
- `NULL` introduce una lógica de tres valores: se compara con `IS NULL` y se trata con `NVL`, `COALESCE` o `NVL2`.
- `FETCH FIRST n ROWS ONLY` limita el número de filas.
- Oracle proporciona funciones de texto, numéricas, de fecha, de conversión y condicionales (`CASE`, `DECODE`).

---

## 11. Autoevaluación

{{< quiz >}}
- q: "¿Qué cláusula elimina filas duplicadas del resultado?"
  options: ["UNIQUE", "DISTINCT", "GROUP BY", "ORDER BY"]
  answer: 1
  explain: "`SELECT DISTINCT` elimina las filas repetidas del resultado, teniendo en cuenta todas las columnas seleccionadas."
- q: "La tabla ALUMNO tiene 32 filas; 3 tienen `cod_grupo` a NULL y 7 están en 1DAM. ¿Cuántas filas devuelve `WHERE cod_grupo <> '1DAM'`?"
  options: ["25", "22", "32", "29"]
  answer: 1
  explain: "Para las 3 filas con NULL la comparación es desconocida y no se devuelven: 32 − 7 − 3 = **22**."
- q: "¿Qué patrón LIKE encuentra los grupos de primer curso ('1DAM', '1DAW', '1ASIR')?"
  options: ["'1_'", "'%1'", "'1%'", "'_1%'"]
  answer: 2
  explain: "`'1%'`: empieza por 1 y sigue cualquier secuencia. `'1_'` solo coincidiría con códigos de dos caracteres."
- q: "¿Por qué falla `SELECT horas*2 AS doble FROM modulo WHERE doble > 300`?"
  options: ["Porque no se puede multiplicar en el SELECT", "Porque WHERE se evalúa antes que SELECT y el alias aún no existe", "Porque falta ORDER BY", "Porque los alias deben ir entre comillas"]
  answer: 1
  explain: "El orden lógico es FROM → WHERE → SELECT. En WHERE hay que repetir la expresión: `WHERE horas*2 > 300`."
- q: "¿Qué devuelve `NVL2(email, 'Sí', 'No')` para un alumno sin correo?"
  options: ["NULL", "'Sí'", "'No'", "Un error"]
  answer: 2
  explain: "NVL2 devuelve el segundo argumento si la expresión **no** es nula y el tercero si es nula."
- q: "¿Qué devuelve `ROUND(4.75)` y qué devuelve `TRUNC(4.75)`?"
  options: ["5 y 4", "4 y 5", "5 y 5", "4.8 y 4.7"]
  answer: 0
  explain: "ROUND redondea al entero más cercano; TRUNC elimina los decimales sin redondear."
- q: "¿Cuál es la forma más fiable de filtrar las matrículas del 15 de septiembre de 2025 si la columna es DATE?"
  options: ["`fecha_matricula = '15/09/2025'`", "`fecha_matricula = DATE '2025-09-15'`", "`fecha_matricula >= DATE '2025-09-15' AND fecha_matricula < DATE '2025-09-16'`", "`fecha_matricula LIKE '15/09/2025%'`"]
  answer: 2
  explain: "DATE incluye la hora. El intervalo semiabierto incluye cualquier hora de ese día y no depende de la configuración de la sesión."
- q: "En un CASE con varias ramas WHEN que se cumplen a la vez, ¿cuál se usa?"
  options: ["La última", "La primera que se cumple", "Todas, concatenadas", "Se produce un error"]
  answer: 1
  explain: "Las condiciones se evalúan en orden y CASE devuelve el resultado de la **primera** rama verdadera."
{{< /quiz >}}

## Referencias

- [Oracle AI Database 26ai: SQL Language Reference, *SELECT*](https://docs.oracle.com/en/database/oracle/oracle-database/26/sqlrf/SELECT.html).
- [Oracle AI Database 26ai: SQL Language Reference, *Single-Row Functions*](https://docs.oracle.com/en/database/oracle/oracle-database/26/sqlrf/Single-Row-Functions.html).
- [Oracle AI Database 26ai: *Format Models*](https://docs.oracle.com/en/database/oracle/oracle-database/26/sqlrf/Format-Models.html).
