---
title: "Teoría · Guiones de sentencias"
weight: 20
bookToc: true
---

# Tema 5 · Guiones de sentencias

## Resumen del tema

Hasta ahora, cada modificación se ha escrito como una sentencia suelta. Pero las tareas reales del centro (dar de alta al alumnado nuevo, pasar de curso, cargar notas) son **secuencias de sentencias** que hay que ejecutar en orden, que no deben dejar la base de datos a medias si algo falla y que se repiten cada curso. Esas tareas se escriben como **guiones** (*scripts*): ficheros que se pueden leer, revisar, repetir y auditar.

Cuando el guion necesita **decidir** (¿tiene el alumno faltas suficientes para perder la evaluación continua?), **repetir** (recorrer todos los alumnos de un grupo) o **reaccionar a un error** (¿qué hago si el módulo no existe?), SQL por sí solo no basta. Oracle ofrece para ello **PL/SQL** (*Procedural Language / SQL*): SQL más variables, condiciones, bucles y excepciones, organizado en **bloques** que se incluyen dentro del guion.

El tema avanza en cuatro pasos: primero qué formas hay de automatizar y con qué herramientas se trabaja (§1 y §2); después el bloque PL/SQL, las variables y el control de flujo (§3 a §5); a continuación el tratamiento de errores con excepciones (§6); y por último cómo se diseña un **guion de mantenimiento** profesional: transaccional, repetible y comprobable (§7).

Todos los ejemplos se ejecutan sobre el esquema de referencia **EDUGEST** con los [scripts del proyecto](/guia/proyecto-edugest#4-scripts-descargables) cargados (32 alumnos, 143 matrículas, 46 faltas) y usan la sintaxis de **Oracle AI Database 26ai Free**. Cada ejemplo indica la salida que debes obtener. Cuando algo es propio de un gestor concreto se señala con una etiqueta o una nota.

{{< ra "RA5:e" >}}

### Objetivos de aprendizaje

Al terminar este tema serás capaz de:

- Distinguir un guion de un bloque anónimo y elegir la forma de automatización adecuada para cada tarea.
- Editar y ejecutar guiones con SQL Developer, SQLcl o SQL\*Plus, usando variables de sustitución y la salida de `DBMS_OUTPUT`.
- Escribir bloques PL/SQL con variables, constantes y tipos `%TYPE` y `%ROWTYPE`, y distinguir las variables de sustitución del cliente de las variables PL/SQL del servidor.
- Aplicar estructuras de control de flujo (`IF`, `CASE`, `LOOP`, `WHILE`, `FOR`).
- Tratar errores con excepciones predefinidas y propias, `PRAGMA EXCEPTION_INIT` y `RAISE_APPLICATION_ERROR`.
- Diseñar guiones de mantenimiento transaccionales, repetibles y verificables.

### Temporalización

Esta parte del tema ocupa **8 horas de aula** (5 de teoría y 3 de práctica). Desarrolla el criterio RA5.e (*diseñar guiones de sentencias para llevar a cabo tareas complejas*) y se apoya en lo visto en el tema 5. Las prácticas largas y el proyecto se completan fuera del horario de aula.

{{< sesiones unidad="T5" horas="8" parte="Guiones de sentencias" >}}
items:
  - {h: 1, tipo: T, t: "Formas de automatizar, herramientas y ejecución de guiones", ref: "§1 y §2"}
  - {h: 1, tipo: T, t: "Bloque PL/SQL, variables y tipos", ref: "§3 y §4"}
  - {h: 1, tipo: T, t: "Estructuras de control de flujo", ref: "§5"}
  - {h: 1, tipo: T, t: "Excepciones", ref: "§6"}
  - {h: 1, tipo: P, t: "Matrícula con excepciones", ref: "Práctica 5.8"}
  - {h: 1, tipo: T, t: "Guiones de mantenimiento: estructura, idempotencia y pruebas", ref: "§7"}
  - {h: 1, tipo: P, t: "Reto: guion de promoción de curso", ref: "Práctica 5.9"}
  - {h: 1, tipo: P, t: "Guiones de mantenimiento de EduGest", ref: "Proyecto EduGest-5"}
autonomo:
  - "Primeros bloques: el expediente de un alumno (Práctica 5.7)"
  - "Terminar en casa lo que no haya dado tiempo de las prácticas 5.7 y 5.8"
  - "Ejercicios resueltos y autoevaluación"
{{< /sesiones >}}

> [!IMPORTANT]
> Trabaja siempre conectado como `EDUGEST` y con la salida activada (`SET SERVEROUTPUT ON`). Todo el código de este tema se prueba con un método fijo:
>
> 1. **Predice** qué debe mostrar o devolver antes de ejecutarlo.
> 2. Ejecuta y compara con la salida que figura en los apuntes.
> 3. Si falla, lee el error **de arriba abajo**: el primer mensaje (`PLS-` en compilación, `ORA-` en ejecución) es la causa; los siguientes solo dicen dónde ocurrió.
> 4. Guarda cada guion en su propio fichero `.sql`: así se repite y se versiona.

---


{{< sesion n="1" h="1" tipo="t" >}}Formas de automatizar, herramientas y ejecución de guiones{{< /sesion >}}

## 1. Programar dentro del servidor

### 1.1 Qué problema resuelve

SQL es un lenguaje **declarativo**: dices *qué* quieres, no *cómo* obtenerlo. Es excelente para consultar y modificar conjuntos de filas, pero no tiene variables, ni condiciones, ni bucles, ni forma de reaccionar a un error. En cuanto una tarea necesita alguna de esas cosas, hay dos opciones: sacar los datos a una aplicación y programar allí la lógica, o **programarla dentro de la base de datos**.

Piensa en la matrícula de un alumno en EduGest. Antes de insertar la fila hay que comprobar que el alumno existe y tiene grupo, que el módulo es de su ciclo, que no está ya matriculado ese curso y que no ha agotado las cuatro convocatorias. Son cuatro consultas, tres decisiones y un `INSERT`: eso ya no es una sentencia, es un pequeño programa.

### 1.2 Formas de automatizar tareas

El criterio RA5.e pide diseñar **guiones** que automaticen tareas complejas. En Oracle hay dos formas de escribirlos:

| Forma | Qué es | Cuándo se ejecuta | Ejemplo en EduGest |
|---|---|---|---|
| **Guion** (*script*) | Fichero de texto con sentencias SQL y órdenes del cliente | Cuando alguien lo lanza (`@fichero.sql`) | `edugest_01_esquema.sql` |
| **Bloque anónimo** | Bloque PL/SQL sin nombre que el cliente envía al servidor | Cuando el cliente lo envía; no se guarda | Un cálculo puntual de comprobación |

Un guion puede contener bloques anónimos. Fuera del servidor existen otras formas de lanzarlos, también válidas: el programador de tareas del sistema operativo (`cron`, Programador de tareas de Windows) ejecutando SQLcl, o la propia aplicación.

### 1.3 Qué es PL/SQL

**PL/SQL** es la extensión procedimental de SQL de Oracle. Un programa PL/SQL se envía al servidor y lo ejecuta el **motor PL/SQL**, que se encarga de las instrucciones procedimentales (asignaciones, condiciones, bucles) y entrega al **motor SQL** las sentencias SQL que encuentra (`SELECT`, `INSERT`, `UPDATE`...).

```text
       Cliente (SQL Developer, SQLcl, aplicación)
                       │  bloque PL/SQL
                       ▼
        ┌─────────────────────────────────┐
        │          SERVIDOR ORACLE        │
        │   Motor PL/SQL  ──sentencias──► Motor SQL ──► Datos
        │   (variables, IF, bucles,      │  (SELECT, INSERT...)
        │    excepciones)  ◄──resultado──┘
        └─────────────────────────────────┘
```

Cada paso de un motor al otro (*context switch*) tiene un coste pequeño pero medible. Por eso, cuando una tarea se puede escribir como **una sola sentencia SQL**, esa es casi siempre la mejor versión.

{{< sgbd "Oracle 26ai" >}}

PL/SQL es propio de Oracle. Cada gestor tiene su lenguaje: PostgreSQL usa **PL/pgSQL**, MySQL y MariaDB usan el lenguaje de rutinas almacenadas **SQL/PSM**, SQL Server usa **Transact-SQL (T-SQL)**. Los conceptos (variables, condiciones, bucles, excepciones) son los mismos; la sintaxis cambia.

---

## 2. Herramientas y ejecución de guiones

### 2.1 Herramientas para editar guiones

El criterio RA5.e pide identificar las herramientas disponibles. Un guion PL/SQL es texto: se puede escribir en cualquier editor, pero las herramientas especializadas aportan resaltado, ejecución directa y acceso al diccionario de datos.

| Herramienta | Tipo | Qué aporta | Cuándo usarla |
|---|---|---|---|
| **Oracle SQL Developer** | Gráfica, gratuita | Editor con autocompletado, árbol de objetos, depurador PL/SQL, panel *Salida de DBMS* | Desarrollo y depuración diaria |
| **Extensión SQL Developer para VS Code** | Gráfica (extensión de VS Code) | Lo mismo dentro del editor del que ya trabajas, con control de versiones integrado | Si el resto del proyecto se edita en VS Code |
| **SQLcl** (`sql`) | Línea de órdenes | SQL\*Plus moderno: historial, autocompletado, formato de resultados (`SET SQLFORMAT`) | Automatización y trabajo remoto |
| **SQL\*Plus** (`sqlplus`) | Línea de órdenes | La herramienta clásica, presente en todas las instalaciones | Servidores donde solo hay esto |
| **Editor de texto + Git** | Texto | Guiones versionados y revisables | Siempre: **el guion en Git es la fuente de verdad** |

> [!NOTE]
> En el contenedor *Oracle AI Database 26ai Free* el servicio al que se conecta el alumnado es `FREEPDB1`: `sql edugest@localhost:1521/FREEPDB1`.

### 2.2 Métodos de ejecución de guiones

El criterio RA5.e pide reconocer los métodos de ejecución de guiones. Un guion puede ejecutarse de varias maneras:

| Método | Dónde | Qué hace |
|---|---|---|
| `@ruta/fichero.sql` | SQLcl, SQL\*Plus | Ejecuta el guion. La ruta es relativa al directorio actual |
| `@@fichero.sql` | SQLcl, SQL\*Plus | Ejecuta el guion **relativo al guion que lo llama**: útil en un guion maestro que invoca otros |
| `START fichero.sql` | SQLcl, SQL\*Plus | Sinónimo de `@` |
| `sql edugest@servicio @fichero.sql` | Terminal | Se conecta y ejecuta el guion en modo *batch* (sin interacción) |
| `F5` (*Ejecutar script*) | SQL Developer | Ejecuta **todo** el guion tal cual; `Ctrl+Intro` ejecuta solo la sentencia bajo el cursor |


Un guion puede recibir **parámetros posicionales** (`&1`, `&2`...), que son sustituidos por el cliente antes de enviar nada al servidor:

```sql
-- informe_grupo.sql · Uso: @informe_grupo.sql 2DAW
SET VERIFY OFF
WHENEVER SQLERROR EXIT FAILURE ROLLBACK
SPOOL informe_&1..txt

SELECT nia, apellidos, nombre
FROM   alumno
WHERE  cod_grupo = '&1'
ORDER  BY apellidos;

SPOOL OFF
```

{{< sgbd "Oracle 26ai" >}}

Al lanzar `@informe_grupo.sql 2DAW` se crea el fichero `informe_2DAW.txt` (el segundo punto de `&1..txt` es el literal; el primero termina el nombre de la variable) con:

| NIA | APELLIDOS | NOMBRE |
|---|---|---|
| 10450851 | Amorós Guillem | Sara |
| 10450777 | Carbonell Soriano | Elena |
| 10450814 | Planelles Marco | Sofía |
| 10450740 | Sala Brotons | Mateo |
| 10450888 | Verdú Castelló | Nicolás |

*5 filas*

Las órdenes de un guion son de dos clases que conviene no confundir:

| Clase | Ejemplos | Quién las entiende |
|---|---|---|
| **Sentencias SQL y bloques PL/SQL** | `SELECT`, `INSERT`, `CREATE TABLE`, `BEGIN ... END;` | El **servidor** Oracle |
| **Órdenes del cliente** | `SET SERVEROUTPUT ON`, `SET VERIFY OFF`, `SPOOL`, `DEFINE`, `ACCEPT`, `WHENEVER`, `@` | Solo **SQLcl y SQL\*Plus** (SQL Developer entiende la mayoría). El servidor no las conoce |

### 2.3 Cómo se termina cada cosa: `;` y `/`

El cliente necesita saber dónde acaba cada sentencia para enviarla al servidor. La regla es simple pero es la causa de muchos errores de principiante:

| Se escribe | Terminador | Motivo |
|---|---|---|
| Sentencia SQL (`SELECT`, `UPDATE`...) | `;` | El punto y coma es del cliente: le dice «envía esto» |
| Orden del cliente (`SET`, `SPOOL`...) | Nada (fin de línea) | No es SQL |
| Bloque PL/SQL anónimo | `;` **y** `/` en una línea sola | Dentro del bloque hay muchos `;`, así que el `;` ya no sirve para saber dónde acaba. La `/` dice «el bloque termina aquí, envíalo» |

```sql
BEGIN
    DBMS_OUTPUT.PUT_LINE('Hola');   -- este ; cierra la instrucción PL/SQL
END;                                 -- este ; cierra el bloque
/                                    -- esta / lo envía al servidor
```

> [!WARNING]
> Si olvidas la `/`, SQLcl se queda esperando sin ejecutar nada (a veces muestra un número de línea, `2  3  4...`). Si la escribes de más, ejecutas **otra vez** el último bloque. Un `CREATE OR REPLACE` repetido es inofensivo; un bloque con un `INSERT`, no.

### 2.4 La salida del servidor: `DBMS_OUTPUT`

PL/SQL no tiene una instrucción `PRINT`. El paquete `DBMS_OUTPUT` escribe texto en un **búfer del servidor**, y es el cliente quien lo vuelca por pantalla cuando el bloque termina, **si se le ha pedido**:

```sql
SET SERVEROUTPUT ON
```

| Elemento | Qué hace |
|---|---|
| `SET SERVEROUTPUT ON` | Pide al cliente que muestre el búfer al terminar cada bloque. Sin esta orden el bloque funciona, pero **no se ve nada** |
| `SET SERVEROUTPUT ON SIZE UNLIMITED` | Igual, sin límite de tamaño del búfer |
| `DBMS_OUTPUT.PUT_LINE(texto)` | Añade una línea al búfer |
| `DBMS_OUTPUT.PUT(texto)` y `NEW_LINE` | Añaden texto sin salto de línea y el salto, respectivamente |

En SQL Developer, además de `SET SERVEROUTPUT ON`, debe estar abierto el panel *Ver → Salida de DBMS* y habilitada la conexión con el botón **+**.

> [!WARNING]
> `DBMS_OUTPUT` es una herramienta de **depuración y de prácticas**, no un mecanismo de producción: el texto solo existe mientras dura la ejecución, se muestra al final (no mientras el bloque trabaja) y un procedimiento que se ejecuta desde una aplicación o una tarea programada no tiene a nadie delante para leerlo. Para dejar constancia hay que escribir en una **tabla de registro** (práctica 5.13).

### 2.5 Errores de compilación

Un bloque PL/SQL se **compila al enviarse** al servidor. Si hay errores, no se ejecuta: Oracle devuelve un `ORA-06550` con la línea y la columna y, a continuación, el mensaje `PLS-` que explica la causa:

```text
ORA-06550: line 4, column 5:
PLS-00201: identifier 'V_NOTA' must be declared
ORA-06550: line 4, column 5:
PL/SQL: Statement ignored
```

| Mensaje | Causa habitual |
|---|---|
| `PLS-00103: Encountered the symbol "..." when expecting one of the following` | Error de sintaxis: un `;` olvidado, un `END IF` sin cerrar, una coma sobrante |
| `PLS-00201: identifier 'X' must be declared` | Nombre mal escrito o variable no declarada |
| `PLS-00302: component 'X' must be declared` | Se usa una columna o un campo que no existe (`r_alumno.telefon`) |
| `PLS-00306: wrong number or types of arguments in call to 'X'` | Llamada con más, menos o distintos parámetros de los declarados |
| `PLS-00428: an INTO clause is expected in this SELECT statement` | Un `SELECT` dentro de un bloque sin `INTO` |
| `PLS-00363: expression 'X' cannot be used as an assignment target` | Se asigna a una constante, a un parámetro `IN` o al índice de un bucle `FOR` |

---

{{% curiosidad titulo="PL/SQL se parece a Ada" %}}
La sintaxis de PL/SQL (`BEGIN … END;`, `:=`, `IF … THEN … END IF;`, las excepciones) está inspirada en el lenguaje **Ada**. Apareció a finales de los años ochenta, para poder meter lógica de programa dentro del servidor y no solo sentencias sueltas.
{{% /curiosidad %}}

{{< sesion n="2" h="1" tipo="t" >}}Bloque PL/SQL, variables y tipos{{< /sesion >}}

## 3. Estructura de un bloque PL/SQL

### 3.1 Las cuatro secciones

Todo programa PL/SQL se construye con **bloques**. Un bloque tiene hasta cuatro secciones, y solo `BEGIN ... END` es obligatoria:

```text
DECLARE        -- 1. Declaraciones (opcional): variables, constantes, excepciones
    ...
BEGIN          -- 2. Instrucciones (obligatoria): el programa en sí
    ...
EXCEPTION      -- 3. Tratamiento de errores (opcional)
    ...
END;           -- 4. Fin del bloque
```

{{< sgbd "Oracle 26ai" >}}

```sql
SET SERVEROUTPUT ON
DECLARE
    c_centro  CONSTANT VARCHAR2(20) := 'EduGest';      -- constante
    v_hoy     DATE := SYSDATE;                          -- variable inicializada
BEGIN
    DBMS_OUTPUT.PUT_LINE('Centro:  ' || c_centro);
    DBMS_OUTPUT.PUT_LINE('Usuario: ' || USER);
    DBMS_OUTPUT.PUT_LINE('Fecha:   ' || TO_CHAR(v_hoy, 'DD/MM/YYYY'));
END;
/
```

```text
Centro:  EduGest
Usuario: EDUGEST
Fecha:   07/10/2026

PL/SQL procedure successfully completed.
```

La fecha es la de tu sistema. La última línea la escribe el cliente, no el bloque: confirma que el servidor lo ha ejecutado sin errores.

| Parte | Qué hace |
|---|---|
| `DECLARE` | Reserva nombre y tipo para los datos que usará el bloque. Si no hay nada que declarar, se omite |
| `CONSTANT` | El valor no puede cambiar después de la declaración |
| `:=` | Operador de asignación. (La igualdad se escribe `=`) |
| `BEGIN ... END;` | Las instrucciones, terminadas cada una en `;` |
| `\|\|` | Concatenación de texto. Convierte números y fechas a texto de forma implícita |
| `USER` | Función del sistema: el usuario conectado |

### 3.2 Qué se puede escribir dentro de un bloque

| Instrucción | ¿Permitida directamente? | Observaciones |
|---|---|---|
| `INSERT`, `UPDATE`, `DELETE`, `MERGE` | Sí | Se escriben igual que en SQL |
| `SELECT` | Sí, **con `INTO`** o dentro de un bucle `FOR` | `SELECT` sin `INTO` da `PLS-00428` |
| `COMMIT`, `ROLLBACK`, `SAVEPOINT` | Sí | El control de la transacción (Tema 5) funciona igual |
| `CREATE`, `ALTER`, `DROP` (DDL) | **No directamente** | Hay que usar SQL dinámico: `EXECUTE IMMEDIATE 'CREATE TABLE ...'` |
| Órdenes de cliente (`SET`, `SPOOL`, `DEFINE`...) | **No** | Son del cliente, no del servidor |

### 3.3 Bloques anidados y ámbito

Un bloque puede contener otros bloques en su sección ejecutable o en la de excepciones. Una variable es visible en el bloque donde se declara y en los bloques que contiene; si un bloque interior declara una con el mismo nombre, **oculta** a la exterior mientras dura.

```sql
DECLARE
    v_x  NUMBER := 1;                                    -- bloque exterior
BEGIN
    DECLARE
        v_x  NUMBER := 2;                                -- oculta a la exterior
        v_y  NUMBER := 10;
    BEGIN
        DBMS_OUTPUT.PUT_LINE('Interior: x=' || v_x || ' y=' || v_y);
    END;
    DBMS_OUTPUT.PUT_LINE('Exterior: x=' || v_x);
    -- DBMS_OUTPUT.PUT_LINE(v_y);   -- PLS-00201: v_y no existe fuera de su bloque
END;
/
```

```text
Interior: x=2 y=10
Exterior: x=1
```

Los bloques anidados no sirven solo para organizar el código: son la herramienta para **limitar el alcance de una excepción** (§6.7).

### 3.4 Comentarios, mayúsculas y convenciones de nombres

PL/SQL no distingue mayúsculas de minúsculas en el código (`begin` es `BEGIN`), pero sí en los **literales de texto** (`'EduGest'` y `'EDUGEST'` son distintos). Los comentarios son de línea (`-- texto`) o de varias líneas (`/* texto */`).

Un prefijo en cada nombre evita el error más común: que una variable se llame igual que una columna. Si en `WHERE id_alumno = id_alumno` ambos son la columna, la condición es siempre verdadera. EduGest usa estas convenciones:

| Elemento | Prefijo | Ejemplo |
|---|---|---|
| Variable local | `v_` | `v_media` |
| Constante | `c_` | `c_max_convocatorias` |
| Parámetro | `p_` | `p_id_alumno` |
| Registro (*record*) | `r_` | `r_alumno` |
| Excepción propia | `e_` | `e_sin_grupo` |
| Tipo definido por el usuario | `t_` | `t_grupos` |

---

## 4. Variables, constantes y tipos

### 4.1 Declaración

```text
nombre  [CONSTANT]  tipo  [NOT NULL]  [:= valor_inicial | DEFAULT valor_inicial];
```

| Tipo | Se usa para | Observaciones |
|---|---|---|
| `VARCHAR2(n)` | Texto de longitud variable | **La longitud es obligatoria** en variables. En PL/SQL admite hasta 32 767 bytes; en una columna, 4000 |
| `NUMBER(p,s)` | Números exactos | Igual que en las tablas. `NUMBER` sin parámetros admite cualquier valor |
| `PLS_INTEGER` | Enteros (contadores, índices) | Aritmética entera más rápida que `NUMBER` |
| `DATE` | Fechas con hora hasta el segundo | `SYSDATE`, `DATE '2027-05-14'` |
| `TIMESTAMP` | Fecha y hora con fracciones de segundo | `SYSTIMESTAMP` |
| `BOOLEAN` | `TRUE`, `FALSE`, `NULL` | Siempre existió en PL/SQL; desde Oracle 23ai también en SQL (columnas y expresiones) |

Dos reglas valen para todos: una variable sin valor inicial vale `NULL`, y una constante **debe** tener valor inicial.

### 4.2 Asignar valores: `:=` y `SELECT ... INTO`

Una variable recibe valor de dos formas: con el operador `:=` o leyendo de una consulta con `INTO`.

```sql
DECLARE
    v_nia     alumno.nia%TYPE;
    v_nombre  VARCHAR2(130);
BEGIN
    SELECT nia, apellidos || ', ' || nombre
    INTO   v_nia, v_nombre
    FROM   alumno
    WHERE  id_alumno = 20;

    DBMS_OUTPUT.PUT_LINE(v_nia || ' · ' || v_nombre);
END;
/
```

```text
10450740 · Sala Brotons, Mateo
```

`SELECT ... INTO` exige que la consulta devuelva **exactamente una fila**:

| La consulta devuelve | Resultado |
|---|---|
| Una fila | Correcto: las columnas se copian a las variables, **en orden** |
| Ninguna fila | Excepción `NO_DATA_FOUND` (`ORA-01403`) |
| Más de una fila | Excepción `TOO_MANY_ROWS` (`ORA-01422`), y no se asigna nada |

El laboratorio del apartado 7.6 permite verlo paso a paso con los tres casos.

> [!CAUTION]
> Un `SELECT ... INTO` con una función de agregado **sin `GROUP BY`** devuelve siempre una fila, aunque no haya datos: `SELECT AVG(nota_final) INTO v_media FROM matricula WHERE id_alumno = 30;` no lanza `NO_DATA_FOUND`; `v_media` queda a `NULL`. Es una diferencia importante entre «la consulta no encuentra nada» y «el agregado de nada».

### 4.3 `%TYPE` y `%ROWTYPE`: heredar el tipo de la tabla

Escribir `v_nia CHAR(8)` funciona hasta el día en que alguien amplía la columna. Los atributos `%TYPE` y `%ROWTYPE` hacen que la variable **herede el tipo directamente del diccionario de datos**:

| Atributo | Declara | Ejemplo |
|---|---|---|
| `tabla.columna%TYPE` | Una variable con el tipo exacto de esa columna | `v_nia alumno.nia%TYPE;` |
| `variable%TYPE` | Una variable del mismo tipo que otra | `v_otra v_nia%TYPE;` |
| `tabla%ROWTYPE` | Un **registro** con un campo por cada columna de la tabla | `r_mod modulo%ROWTYPE;` |

```sql
DECLARE
    r_mod  modulo%ROWTYPE;                              -- un campo por columna de MODULO
BEGIN
    SELECT * INTO r_mod FROM modulo WHERE id_modulo = 2;

    DBMS_OUTPUT.PUT_LINE(r_mod.codigo || ' ' || r_mod.nombre ||
                         ' (' || r_mod.cod_ciclo || ', curso ' || r_mod.curso ||
                         ', ' || r_mod.horas || ' h)');
END;
/
```

```text
0484 Bases de datos (DAM, curso 1, 160 h)
```

Se accede a cada campo con `registro.columna`. Ventajas de `%ROWTYPE`: el `SELECT *` no necesita una variable por columna, y si se añade una columna a `MODULO` el bloque sigue compilando. Su inconveniente: **trae todas las columnas**, aunque solo uses dos.

Cuando interesa un registro con campos elegidos, se define un tipo propio con `RECORD`:

```sql
DECLARE
    TYPE t_resumen IS RECORD (
        nia     alumno.nia%TYPE,
        nombre  VARCHAR2(130),
        media   NUMBER(4,2)
    );
    r  t_resumen;
BEGIN
    SELECT a.nia, a.apellidos || ', ' || a.nombre, ROUND(AVG(m.nota_final), 2)
    INTO   r
    FROM   alumno a
           JOIN matricula m ON m.id_alumno = a.id_alumno
    WHERE  a.id_alumno = 20
    GROUP  BY a.nia, a.apellidos, a.nombre;

    DBMS_OUTPUT.PUT_LINE(r.nia || ' · ' || r.nombre || ' · media ' || r.media);
END;
/
```

```text
10450740 · Sala Brotons, Mateo · media 7.13
```

> [!NOTE]
> Los números se convierten a texto con el separador decimal de la sesión (`NLS_NUMERIC_CHARACTERS`). En el contenedor de prácticas es el punto, como en las salidas de estos apuntes; con una configuración regional española verías `7,13`. Para controlarlo, usa `TO_CHAR(x, '990D00')`.

### 4.4 Variables de sustitución frente a variables PL/SQL

Es la confusión más frecuente del tema. Observa este bloque:

```sql
SET VERIFY ON
DEFINE g_grupo = 2DAW
BEGIN
    DBMS_OUTPUT.PUT_LINE('Grupo: &g_grupo');
END;
/
```

```text
old   2:     DBMS_OUTPUT.PUT_LINE('Grupo: &g_grupo');
new   2:     DBMS_OUTPUT.PUT_LINE('Grupo: 2DAW');
Grupo: 2DAW
```

Las dos líneas `old` y `new` las escribe el **cliente** (SQLcl, SQL\*Plus, SQL Developer): ha **sustituido** `&g_grupo` por `2DAW` en el texto del bloque y solo después se lo ha enviado a Oracle. El servidor jamás ha visto el `&`. Una variable de sustitución no es una variable: es un **marcador de «buscar y reemplazar» del cliente**.

| | Variable de sustitución (`&nombre`) | Variable PL/SQL (`v_nombre`) |
|---|---|---|
| **¿Quién la resuelve?** | El **cliente**, antes de enviar el texto | El **servidor**, mientras se ejecuta |
| **¿Cuándo?** | Antes de que el bloque exista | En tiempo de ejecución |
| **¿Qué es?** | Texto que se pega en el código | Un valor con tipo, dentro de la memoria del bloque |
| **Declaración** | `DEFINE`, `ACCEPT` o se pregunta al ejecutar | `DECLARE v_nombre tipo;` |
| **¿Cambia dentro de un bucle?** | **No**: ya es texto fijo | Sí |
| **Propia de** | SQL\*Plus / SQLcl / SQL Developer | PL/SQL |

| Orden | Efecto |
|---|---|
| `DEFINE nombre = valor` | Crea la variable de sustitución con ese valor (sin comillas: se pega literalmente) |
| `ACCEPT nombre PROMPT 'texto'` | Pide el valor por teclado |
| `&nombre` | Se sustituye. Si no está definida, el cliente **pregunta** |
| `&&nombre` | Como `&`, pero además la deja definida: no vuelve a preguntar |
| `SET VERIFY ON \| OFF` | Muestra (o no) las líneas `old` y `new` |
| `SET DEFINE OFF` | Desactiva la sustitución: el `&` pasa a ser un carácter normal |

> [!WARNING]
> Como `&variable` es texto pegado en el código, **escribir `&id_alumno` en un guion que recibe datos de una persona es una vía de inyección de código**. Sirve para prácticas con un guion que ejecutas tú; en una aplicación se usan siempre **variables de enlace** (`:nombre`) o parámetros de un procedimiento. Y al revés: si tus datos contienen un `&` (`'Gómez & Pérez'`), el cliente intentará sustituirlo y preguntará por una variable; el script de datos de EduGest empieza con `SET DEFINE OFF` por esa razón.

Las **variables de enlace** (*bind variables*) se declaran en el cliente con `VARIABLE` y se leen con `:nombre`. Sí las entiende el servidor, que las recibe como valores:

```sql
VARIABLE v_total NUMBER
BEGIN
    SELECT COUNT(*) INTO :v_total FROM alumno WHERE cod_grupo = '2DAW';
END;
/
PRINT v_total
```

```text
   V_TOTAL
----------
         5
```

### 4.5 Variables del sistema y del contexto de la sesión

PL/SQL no tiene variables globales del sistema como tales: se obtienen con funciones. Estas son las más útiles:

| Expresión | Devuelve |
|---|---|
| `USER` | Usuario conectado (`EDUGEST`) |
| `SYSDATE` | Fecha y hora del servidor (tipo `DATE`) |
| `SYSTIMESTAMP` | Fecha y hora con fracciones de segundo y zona horaria |
| `SYS_CONTEXT('USERENV', 'SESSION_USER')` | Usuario de la sesión |
| `SYS_CONTEXT('USERENV', 'HOST')` | Nombre del equipo cliente |
| `SYS_CONTEXT('USERENV', 'IP_ADDRESS')` | Dirección IP del cliente |
| `SYS_CONTEXT('USERENV', 'DB_NAME')` | Nombre de la base de datos |
| `SYS_CONTEXT('USERENV', 'CON_NAME')` | Nombre de la base de datos conectable (*PDB*), p. ej. `FREEPDB1` |
| `SQLCODE`, `SQLERRM` | Código y mensaje del último error (solo dentro de un manejador, §6.3) |
| `SQL%ROWCOUNT` | Filas afectadas por la última sentencia DML |

Estas funciones son las que permiten registrar **quién** hizo un cambio y **desde dónde**: se usan, por ejemplo, para registrar quién ejecutó un guion.

{{< quiz >}}
- q: "En el bloque `BEGIN DBMS_OUTPUT.PUT_LINE('Hola'); END;` no aparece nada por pantalla, pero tampoco hay error. ¿Qué falta?"
  options: ["Un `COMMIT` antes del `END`", "`SET SERVEROUTPUT ON` en el cliente", "Declarar una variable de tipo texto", "Cambiar `PUT_LINE` por `PRINT`"]
  answer: 1
  explain: "`DBMS_OUTPUT` escribe en un búfer del servidor y es el cliente quien lo muestra, solo si se le ha pedido con `SET SERVEROUTPUT ON`. Sin esa orden el bloque se ejecuta correctamente, pero no se ve nada."
- q: "Un bloque contiene `WHERE cod_grupo = '&g'` y se ejecuta en SQLcl. ¿Quién sustituye `&g` y cuándo?"
  options: ["Oracle, durante la ejecución del bloque", "El cliente, antes de enviar el bloque al servidor", "El motor PL/SQL, cuando lee la variable `g`", "Nadie: es una variable PL/SQL que vale `NULL`"]
  answer: 1
  explain: "`&g` es una variable de **sustitución**: el cliente (SQLcl, SQL*Plus, SQL Developer) reemplaza el texto antes de enviar nada. El servidor recibe ya el valor y no sabe que existió un `&`. Por eso no cambia dentro de un bucle del bloque."
- q: "¿Qué ocurre con `SELECT nombre INTO v_nombre FROM alumno WHERE nia LIKE '104507%';` si el patrón coincide con tres alumnos?"
  options: ["Se asigna el primero y se ignoran los demás", "Se asigna el último", "Se lanza `TOO_MANY_ROWS` y no se asigna ningún valor", "Se lanza `NO_DATA_FOUND`"]
  answer: 2
  explain: "`SELECT ... INTO` exige exactamente una fila. Con varias se lanza `TOO_MANY_ROWS` (`ORA-01422`). Para recorrer varias filas hace falta un bucle `FOR r IN (SELECT ...)`."
- q: "¿Qué ventaja tiene declarar `v_nia alumno.nia%TYPE` en lugar de `v_nia CHAR(8)`?"
  options: ["La variable es más rápida", "La variable hereda el tipo de la columna y sigue siendo correcta si la columna cambia", "Permite almacenar valores nulos", "Hace que la variable sea una constante"]
  answer: 1
  explain: "`%TYPE` consulta el diccionario de datos: si se amplía o cambia la columna, el código sigue siendo coherente sin tocarlo. Una longitud escrita a mano se queda anticuada."
{{< /quiz >}}


---


{{< sesion n="3" h="1" tipo="t" >}}Estructuras de control de flujo{{< /sesion >}}

## 5. Estructuras de control de flujo

El criterio RA5.e pide utilizar estructuras de control. PL/SQL tiene las tres familias habituales: **condicionales** (`IF`, `CASE`), **repetitivas** (`LOOP`, `WHILE`, `FOR`) y de **salto** (`EXIT`, `CONTINUE`, `GOTO`).

### 5.1 `IF`, `ELSIF` y `ELSE`

```text
IF condición1 THEN
    instrucciones;
[ELSIF condición2 THEN
    instrucciones;]
[ELSE
    instrucciones;]
END IF;
```

Se escribe `ELSIF` (sin la `E` de *else if*) y se cierra con `END IF;`. Las condiciones se evalúan **en orden** y se ejecuta la primera rama verdadera.

```sql
DECLARE
    v_nota   matricula.nota_final%TYPE := 6.5;
    v_texto  VARCHAR2(15);
BEGIN
    IF v_nota IS NULL THEN
        v_texto := 'NC';
    ELSIF v_nota < 5 THEN
        v_texto := 'Insuficiente';
    ELSIF v_nota < 6 THEN
        v_texto := 'Suficiente';
    ELSIF v_nota < 7 THEN
        v_texto := 'Bien';
    ELSIF v_nota < 9 THEN
        v_texto := 'Notable';
    ELSE
        v_texto := 'Sobresaliente';
    END IF;

    DBMS_OUTPUT.PUT_LINE(v_nota || ' -> ' || v_texto);
END;
/
```

```text
6.5 -> Bien
```

> [!WARNING]
> **Una condición con `NULL` no es verdadera ni falsa: es desconocida** (*lógica trivaluada*, Tema 4), y `IF` solo ejecuta la rama `THEN` cuando la condición es **verdadera**. Con `v_nota` a `NULL`, `IF v_nota >= 5 THEN ... ELSE` ejecutaría el `ELSE` y marcaría como suspenso a quien no se ha presentado. Por eso en el ejemplo la primera pregunta es `IS NULL`. Y nunca se escribe `v_nota = NULL`: no es verdadera jamás.

| `x` | `y` | `x = y` | `x <> y` | `x IS NULL` |
|---|---|---|---|---|
| 5 | 5 | `TRUE` | `FALSE` | `FALSE` |
| 5 | 6 | `FALSE` | `TRUE` | `FALSE` |
| 5 | `NULL` | **`NULL`** | **`NULL`** | `FALSE` |
| `NULL` | `NULL` | **`NULL`** | **`NULL`** | `TRUE` |

### 5.2 `CASE`: sentencia y expresión

`CASE` es la alternativa más legible cuando hay muchas ramas. Existe en dos formas, y cada una en dos usos:

| Forma | Sintaxis | Se usa cuando |
|---|---|---|
| **Simple** | `CASE variable WHEN valor1 THEN ... WHEN valor2 THEN ... END` | Se compara **una expresión con varios valores** |
| **Con condiciones** (*searched*) | `CASE WHEN condición1 THEN ... WHEN condición2 THEN ... END` | Cada rama tiene **su propia condición** |

| Uso | Termina en | Qué produce |
|---|---|---|
| **Sentencia** `CASE` | `END CASE;` | Ejecuta instrucciones |
| **Expresión** `CASE` | `END` | **Devuelve un valor** que se asigna o se concatena |

```sql
DECLARE
    v_turno  grupo.turno%TYPE;
BEGIN
    SELECT turno INTO v_turno FROM grupo WHERE cod_grupo = '2DAW';

    -- CASE simple como sentencia
    CASE v_turno
        WHEN 'M' THEN DBMS_OUTPUT.PUT_LINE('2DAW: turno de mañana');
        WHEN 'T' THEN DBMS_OUTPUT.PUT_LINE('2DAW: turno de tarde');
        ELSE          DBMS_OUTPUT.PUT_LINE('2DAW: turno desconocido');
    END CASE;

    -- CASE con condiciones como expresión
    DBMS_OUTPUT.PUT_LINE('Hora de entrada: ' ||
        CASE WHEN v_turno = 'M' THEN '08:00' ELSE '15:00' END);
END;
/
```

```text
2DAW: turno de tarde
Hora de entrada: 15:00
```

> [!CAUTION]
> Si ninguna rama de una **sentencia** `CASE` se cumple y no hay `ELSE`, Oracle lanza `CASE_NOT_FOUND` (`ORA-06592`). La **expresión** `CASE` sin `ELSE` devuelve `NULL` en silencio. Escribe siempre el `ELSE`.

### 5.3 Bucles

| Bucle | Cuándo usarlo | Sintaxis |
|---|---|---|
| **`LOOP`** básico | No se sabe cuántas veces; la salida se decide en medio | `LOOP ... EXIT WHEN cond; ... END LOOP;` |
| **`WHILE`** | La condición se comprueba **antes** de cada vuelta (puede no ejecutarse nunca) | `WHILE cond LOOP ... END LOOP;` |
| **`FOR`** numérico | Se sabe cuántas veces | `FOR i IN 1..n LOOP ... END LOOP;` |
| **`FOR` de consulta** | Recorrer las filas de una consulta | `FOR r IN (SELECT ...) LOOP ... END LOOP;` |

Un ejemplo con cada uno, sobre las convocatorias que le quedan a un alumno que va por la segunda:

```sql
DECLARE
    v_conv  PLS_INTEGER := 2;                      -- convocatoria actual
BEGIN
    -- LOOP básico: la salida está en medio
    LOOP
        EXIT WHEN v_conv > 4;
        DBMS_OUTPUT.PUT_LINE('Queda la convocatoria ' || v_conv);
        v_conv := v_conv + 1;
    END LOOP;

    -- WHILE: equivalente, con la condición al principio
    v_conv := 2;
    WHILE v_conv <= 4 LOOP
        DBMS_OUTPUT.PUT_LINE('(while) convocatoria ' || v_conv);
        v_conv := v_conv + 1;
    END LOOP;
END;
/
```

```text
Queda la convocatoria 2
Queda la convocatoria 3
Queda la convocatoria 4
(while) convocatoria 2
(while) convocatoria 3
(while) convocatoria 4
```

El bucle `FOR` numérico declara **él mismo** su contador, que solo existe dentro del bucle y **no se puede modificar**:

```sql
DECLARE
    v_nombre  modulo.nombre%TYPE;
BEGIN
    FOR i IN 1..3 LOOP
        SELECT nombre INTO v_nombre FROM modulo WHERE id_modulo = i;
        DBMS_OUTPUT.PUT_LINE(i || '. ' || v_nombre);
    END LOOP;

    FOR i IN REVERSE 1..3 LOOP                       -- cuenta atrás
        DBMS_OUTPUT.PUT_LINE('Cuenta atrás: ' || i);
    END LOOP;
END;
/
```

```text
1. Sistemas informáticos
2. Bases de datos
3. Programación
Cuenta atrás: 3
Cuenta atrás: 2
Cuenta atrás: 1
```

### 5.4 `EXIT`, `CONTINUE`, etiquetas y `GOTO`

| Instrucción | Efecto |
|---|---|
| `EXIT;` / `EXIT WHEN cond;` | Sale del bucle más interno |
| `CONTINUE;` / `CONTINUE WHEN cond;` | Salta al principio de la siguiente vuelta |
| `<<etiqueta>>` antes de un bucle | Le da nombre; permite `EXIT etiqueta;` para salir de un bucle exterior desde uno interior |
| `GOTO etiqueta;` | Salto incondicional. **Evítalo**: rompe la lectura lineal del código |

```sql
BEGIN
    <<externo>>
    FOR g IN 1..3 LOOP
        FOR a IN 1..3 LOOP
            CONTINUE WHEN a = 2;                     -- se salta la vuelta a = 2
            EXIT externo WHEN g = 2;                 -- sale de los DOS bucles
            DBMS_OUTPUT.PUT_LINE('g=' || g || ' a=' || a);
        END LOOP;
    END LOOP externo;
END;
/
```

```text
g=1 a=1
g=1 a=3
```

### 5.5 Errores habituales con los bucles

| Error | Síntoma | Solución |
|---|---|---|
| `LOOP` sin `EXIT` alcanzable | Bucle infinito: el cliente se queda colgado | Comprueba que la variable de la condición cambia dentro del bucle |
| Asignar al contador del `FOR` | `PLS-00363: expression 'I' cannot be used as an assignment target` | Copia el valor a otra variable |
| Usar el contador fuera del `FOR` | `PLS-00201: identifier 'I' must be declared` | Es local al bucle |
| `SELECT ... INTO` dentro de un bucle sobre filas | Una consulta por vuelta y `NO_DATA_FOUND` posible | Usa un bucle `FOR r IN (SELECT ...)` |

{{% details title="Prueba tú: marcar los módulos largos" %}}
**Enunciado.** Escribe un bloque que muestre los módulos con identificador 1 a 5 y marque con un asterisco los que tengan más de 150 horas.

**Solución.**

```sql
DECLARE
    r_mod  modulo%ROWTYPE;
BEGIN
    FOR i IN 1..5 LOOP
        SELECT * INTO r_mod FROM modulo WHERE id_modulo = i;
        DBMS_OUTPUT.PUT_LINE(
            CASE WHEN r_mod.horas > 150 THEN '* ' ELSE '  ' END ||
            r_mod.codigo || ' ' || r_mod.nombre || ' (' || r_mod.horas || ' h)');
    END LOOP;
END;
/
```

```text
* 0483 Sistemas informáticos (160 h)
* 0484 Bases de datos (160 h)
* 0485 Programación (256 h)
  0487 Entornos de desarrollo (96 h)
  0373 Lenguajes de marcas y sistemas de gestión de información (128 h)
```

El `CASE` es una **expresión**: devuelve el prefijo que se concatena al texto.
{{% /details %}}

---

{{< sesion n="4" h="1" tipo="t" >}}Excepciones{{< /sesion >}}

## 6. Excepciones

### 6.1 Qué es una excepción

Una **excepción** es un error que ocurre durante la ejecución de un bloque. Cuando se produce, el flujo normal se **interrumpe**: Oracle abandona las instrucciones restantes de la sección `BEGIN` y busca un **manejador** en la sección `EXCEPTION`.

```text
BEGIN
    instrucción 1;          ← se ejecuta
    instrucción 2;          ← ¡error! se lanza una excepción
    instrucción 3;          ← NO se ejecuta
EXCEPTION
    WHEN una_excepcion THEN ← Oracle busca aquí, de arriba abajo, el primer WHEN que coincida
        tratamiento;
    WHEN OTHERS THEN        ← comodín: cualquier otra excepción
        tratamiento;
END;
```

| Situación | Resultado |
|---|---|
| Hay un manejador que coincide | Se ejecuta su código y el bloque **termina normalmente** (como si no hubiera pasado nada, salvo lo que haga el manejador) |
| No hay manejador en este bloque | La excepción **se propaga** al bloque exterior, y así sucesivamente |
| Ningún bloque la trata | El error llega al cliente: `ORA-xxxxx` |

El criterio RA5.e pide utilizar excepciones. Existen tres clases:

| Clase | Quién la lanza | Ejemplo |
|---|---|---|
| **Predefinida** | Oracle, con nombre ya asignado | `NO_DATA_FOUND`, `ZERO_DIVIDE` |
| **Oracle sin nombre** | Oracle, con código `ORA-` pero sin nombre en el lenguaje | `ORA-02292` (borrar un padre con hijos) |
| **Definida por el usuario** | El programador, con `RAISE` o `RAISE_APPLICATION_ERROR` | «El alumno no tiene grupo» |

### 6.2 Excepciones predefinidas

| Excepción | Código | Se lanza cuando… |
|---|---|---|
| `NO_DATA_FOUND` | `ORA-01403` | Un `SELECT ... INTO` no devuelve filas |
| `TOO_MANY_ROWS` | `ORA-01422` | Un `SELECT ... INTO` devuelve más de una fila |
| `DUP_VAL_ON_INDEX` | `ORA-00001` | Se viola una clave primaria o una restricción `UNIQUE` |
| `ZERO_DIVIDE` | `ORA-01476` | División por cero |
| `INVALID_NUMBER` | `ORA-01722` | Conversión de texto a número imposible dentro de una sentencia SQL |
| `VALUE_ERROR` | `ORA-06502` | Error de conversión o de tamaño en una asignación PL/SQL (`VARCHAR2(3) := 'Sala'`) |
| `CASE_NOT_FOUND` | `ORA-06592` | Ninguna rama de un `CASE` sin `ELSE` |
| `OTHERS` | cualquiera | Comodín: atrapa todo lo que no se haya tratado antes |

Un bloque que calcula las horas de falta por alumno de un grupo. El grupo 2ASIR existe, pero **no tiene alumnado**:

```sql
DECLARE
    v_alumnos  PLS_INTEGER;
    v_horas    PLS_INTEGER;
    v_media    NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_alumnos FROM alumno WHERE cod_grupo = '2ASIR';

    SELECT NVL(SUM(f.horas), 0)
    INTO   v_horas
    FROM   falta_asistencia f
           JOIN matricula m ON m.id_matricula = f.id_matricula
           JOIN alumno a    ON a.id_alumno    = m.id_alumno
    WHERE  a.cod_grupo = '2ASIR';

    v_media := v_horas / v_alumnos;                             -- 0 / 0 → ZERO_DIVIDE
    DBMS_OUTPUT.PUT_LINE('Horas de falta por alumno: ' || v_media);
EXCEPTION
    WHEN ZERO_DIVIDE THEN
        DBMS_OUTPUT.PUT_LINE('2ASIR no tiene alumnado: no se puede calcular la media');
END;
/
```

```text
2ASIR no tiene alumnado: no se puede calcular la media
```

Y un `INSERT` que viola la clave primaria de `CICLO`:

```sql
BEGIN
    INSERT INTO ciclo (cod_ciclo, nombre, grado, horas_totales)
    VALUES ('DAW', 'Desarrollo de Aplicaciones Web', 'SUPERIOR', 2000);
EXCEPTION
    WHEN DUP_VAL_ON_INDEX THEN
        DBMS_OUTPUT.PUT_LINE('El ciclo DAW ya existe');
END;
/
```

```text
El ciclo DAW ya existe
```

El caso de `NO_DATA_FOUND` y `TOO_MANY_ROWS` lo tienes paso a paso en el laboratorio del apartado 7.6.

### 6.3 `OTHERS`, `SQLCODE` y `SQLERRM`

Dentro de un manejador, dos funciones describen el error que se está tratando:

| Función | Devuelve |
|---|---|
| `SQLCODE` | Número del error. Negativo para los `ORA-` (`-1476`); `+100` para `NO_DATA_FOUND`; el de `RAISE_APPLICATION_ERROR` (`-20010`) |
| `SQLERRM` | Texto completo con el prefijo: `ORA-01476: divisor is equal to zero` |

```sql
DECLARE
    v_cero  NUMBER := 0;
BEGIN
    DBMS_OUTPUT.PUT_LINE(10 / v_cero);
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('SQLCODE = ' || SQLCODE);
        DBMS_OUTPUT.PUT_LINE('SQLERRM = ' || SQLERRM);
END;
/
```

```text
SQLCODE = -1476
SQLERRM = ORA-01476: divisor is equal to zero
```

> [!CAUTION]
> **`WHEN OTHERS THEN NULL;` es el peor código que se puede escribir en PL/SQL.** Traga cualquier error, incluso uno inesperado, y deja la base de datos en un estado incierto sin dejar rastro. Un manejador `OTHERS` solo es aceptable si **registra** el error y lo **vuelve a lanzar** con `RAISE;`:
>
> ```sql
> EXCEPTION
>     WHEN OTHERS THEN
>         DBMS_OUTPUT.PUT_LINE('Error ' || SQLCODE || ': ' || SQLERRM);   -- o, mejor, a una tabla de registro
>         RAISE;                                                          -- el MISMO error sigue su camino
> ```

`SQLERRM` está limitado a 512 bytes y no incluye *dónde* ocurrió el error. Para depurar, `DBMS_UTILITY.FORMAT_ERROR_STACK` devuelve la pila completa y `DBMS_UTILITY.FORMAT_ERROR_BACKTRACE` indica los números de línea de cada subprograma por el que pasó.

### 6.4 Excepciones definidas por el usuario

Cuando la «anomalía» es de negocio y no del gestor, se declara una excepción propia en la sección `DECLARE`, se lanza con `RAISE` y se trata como las demás:

```sql
DECLARE
    e_sin_notas  EXCEPTION;                     -- 1. se declara
    v_notas      PLS_INTEGER;
BEGIN
    SELECT COUNT(nota_final) INTO v_notas FROM matricula WHERE id_alumno = 30;

    IF v_notas = 0 THEN
        RAISE e_sin_notas;                      -- 2. se lanza
    END IF;
    DBMS_OUTPUT.PUT_LINE('El alumno 30 tiene ' || v_notas || ' notas');
EXCEPTION
    WHEN e_sin_notas THEN                       -- 3. se trata
        DBMS_OUTPUT.PUT_LINE('El alumno 30 no tiene ninguna nota');
END;
/
```

```text
El alumno 30 no tiene ninguna nota
```

Una excepción declarada así solo existe dentro de su bloque. Si no se trata, al llegar al cliente se muestra como `ORA-06510: PL/SQL: unhandled user-defined exception`, un mensaje que no ayuda a nadie: por eso, para errores que deben llegar a la aplicación, se prefiere `RAISE_APPLICATION_ERROR` (§6.6).

### 6.5 `PRAGMA EXCEPTION_INIT`: ponerle nombre a un error de Oracle

Hay muchos errores `ORA-` que no tienen nombre predefinido. `PRAGMA EXCEPTION_INIT` asocia un nombre propio a un código, para poder tratarlo en un `WHEN`. Un caso típico de EduGest: borrar un profesor que todavía imparte módulos (`ORA-02292`, clave ajena sin `ON DELETE`):

```sql
DECLARE
    e_tiene_hijos  EXCEPTION;
    PRAGMA EXCEPTION_INIT(e_tiene_hijos, -2292);        -- ORA-02292: child record found
BEGIN
    DELETE FROM profesor WHERE id_profesor = 105;
    DBMS_OUTPUT.PUT_LINE('Profesor borrado');
EXCEPTION
    WHEN e_tiene_hijos THEN
        DBMS_OUTPUT.PUT_LINE('No se puede borrar al profesor 105: imparte módulos (tabla IMPARTE)');
END;
/
```

```text
No se puede borrar al profesor 105: imparte módulos (tabla IMPARTE)
```

El segundo argumento es el código **con signo negativo** (`-2292`, no `2292`). Otros códigos que se asocian con frecuencia:

| Código | Significado | Nombre habitual |
|---|---|---|
| `-2291` | `ORA-02291`: *parent key not found* (la clave ajena apunta a una fila que no existe) | `e_padre_no_existe` |
| `-2292` | `ORA-02292`: *child record found* (se borra un padre con hijos) | `e_tiene_hijos` |
| `-1400` | `ORA-01400`: no se puede insertar `NULL` en una columna `NOT NULL` | `e_nulo_no_permitido` |
| `-2290` | `ORA-02290`: se viola una restricción `CHECK` | `e_check` |
| `-54` | `ORA-00054`: recurso ocupado (`FOR UPDATE NOWAIT`, Tema 5) | `e_ocupado` |

### 6.6 `RAISE_APPLICATION_ERROR`: errores de negocio hacia el cliente

`RAISE_APPLICATION_ERROR(código, mensaje)` detiene el bloque y devuelve al llamador un error con el **código** y el **mensaje** que tú decidas. Es la forma estándar de comunicar a una aplicación que se ha incumplido una regla de negocio.

```sql
BEGIN
    RAISE_APPLICATION_ERROR(-20010, 'El módulo 12 no pertenece al ciclo del alumno');
END;
/
```

```text
ORA-20010: El módulo 12 no pertenece al ciclo del alumno
ORA-06512: at line 2
```

| Regla | Detalle |
|---|---|
| Código | Entre **-20000 y -20999**: el rango que Oracle reserva a las aplicaciones |
| Mensaje | Hasta 2048 bytes; debe decir **qué** ha fallado y con **qué datos** |
| Efecto | La excepción se propaga; si nadie la trata, la sentencia que invocó el código se deshace |

> [!TIP]
> Reserva un **catálogo de códigos** para el proyecto y documéntalo, igual que una tabla de errores HTTP. Así la aplicación puede reaccionar al código (`-20013` → «ya estás matriculado») y no analizar el texto. EduGest usa:
>
> | Código | Significado | Dónde |
> |---|---|---|
> | `-20010` | El módulo no es del ciclo del alumno (R2) | `pr_matricular` |
> | `-20011` | Convocatorias agotadas (máximo 4) | `pr_matricular` |
> | `-20012` | Alumno o módulo inexistente, o alumno sin grupo | `pr_matricular` |
> | `-20013` | Alumno ya matriculado del módulo en ese curso | `pr_matricular` |
> | `-20020` | El jefe no pertenece al departamento (R1) | `trg_jefe_departamento` |
> | `-20021` | Profesor jefe que cambia de departamento (R1) | `trg_profesor_cambio_dpto` |
> | `-20022` | Falta anterior a la fecha de matrícula (R3) | `trg_falta_fecha` |
> | `-20030` | Un profesor supera las 20 horas semanales (R4) | `trg_imparte_max_horas` |
> | `-20040` | Un grupo supera los 30 alumnos (R5) | `trg_grupo_max_alumnos` |

### 6.7 Bloques anidados: limitar el alcance de un error

Un `SELECT ... INTO` que no encuentra datos en medio de un bucle aborta **todo** el bucle. Si lo que se quiere es tratar el caso y **continuar con la fila siguiente**, la solución es envolver la parte arriesgada en su propio bloque:

```sql
DECLARE
    TYPE t_ids IS TABLE OF PLS_INTEGER;
    v_ids     t_ids := t_ids(20, 999, 30);
    v_nombre  VARCHAR2(130);
BEGIN
    FOR i IN 1..v_ids.COUNT LOOP
        BEGIN                                              -- bloque interior, uno por vuelta
            SELECT apellidos || ', ' || nombre
            INTO   v_nombre
            FROM   alumno
            WHERE  id_alumno = v_ids(i);
            DBMS_OUTPUT.PUT_LINE(v_ids(i) || ': ' || v_nombre);
        EXCEPTION
            WHEN NO_DATA_FOUND THEN
                DBMS_OUTPUT.PUT_LINE(v_ids(i) || ': no existe');
        END;
    END LOOP;
END;
/
```

```text
20: Sala Brotons, Mateo
999: no existe
30: Iborra Valero, Zoe
```

Dos particularidades que sorprenden:

1. **Una excepción en la sección `DECLARE` no la trata el manejador del mismo bloque**, sino el del bloque exterior. Con `v_corto VARCHAR2(3) := 'Sala';` el bloque falla con `ORA-06502` aunque tenga un `WHEN VALUE_ERROR`: aún no había empezado a ejecutarse.
2. **Una excepción dentro de un manejador** tampoco la trata el mismo bloque: sube al exterior.

### 6.8 Excepciones y transacciones

Un error **no** hace `ROLLBACK` de la transacción. Lo que ocurre depende de si se trata o no:

| Situación | Qué pasa con los cambios |
|---|---|
| La excepción **no se trata** y llega al cliente | Oracle deshace los cambios de **la llamada que ha fallado** (atomicidad de sentencia, Tema 5). Lo hecho antes en la transacción permanece, sin confirmar |
| La excepción **se trata** y el bloque termina | **No se deshace nada.** Lo que el bloque ya había hecho antes del error se queda hecho |
| Se necesita deshacer solo una parte | `SAVEPOINT` al principio y `ROLLBACK TO SAVEPOINT` en el manejador |

```sql
BEGIN
    SAVEPOINT antes_de_borrar;
    DELETE FROM falta_asistencia WHERE id_matricula = 10060;
    DELETE FROM profesor WHERE id_profesor = 105;          -- ORA-02292
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK TO antes_de_borrar;                        -- deshace también el primer DELETE
        RAISE;
END;
/
```

> [!IMPORTANT]
> No dependas del comportamiento implícito. Un bloque que hace varias modificaciones y trata sus propios errores debe decidir **explícitamente** qué se conserva y qué se deshace, y quien lo llama debe saberlo.

### 6.9 Ejemplo completo: matrícula validada en un bloque

Este bloque implementa la regla R2 del catálogo de restricciones (Tema 2) y las reglas de convocatoria. Valida el alumno, el módulo y el curso académico (que se indican con `DEFINE`) y, si todo es correcto, inserta la matrícula calculando la convocatoria. Reúne todo lo visto: variables, `SELECT INTO`, bloques anidados, excepciones y `RAISE_APPLICATION_ERROR`.

{{< sgbd "Oracle 26ai" >}}

```sql
DEFINE id_alumno = 1
DEFINE id_modulo = 2
DEFINE curso     = 2026-27

DECLARE
    v_id_alumno          alumno.id_alumno%TYPE          := &id_alumno;
    v_id_modulo          modulo.id_modulo%TYPE          := &id_modulo;
    v_curso              matricula.curso_academico%TYPE := '&curso';
    c_max_convocatorias  CONSTANT PLS_INTEGER := 4;
    v_ciclo_alumno       grupo.cod_ciclo%TYPE;
    v_ciclo_modulo       modulo.cod_ciclo%TYPE;
    v_ya_matriculado     PLS_INTEGER;
    v_convocatoria       PLS_INTEGER;
BEGIN
    -- 1. El alumno existe y tiene grupo (si no, el JOIN no devuelve ninguna fila)
    BEGIN
        SELECT g.cod_ciclo
        INTO   v_ciclo_alumno
        FROM   alumno a
               JOIN grupo g ON g.cod_grupo = a.cod_grupo
        WHERE  a.id_alumno = v_id_alumno;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RAISE_APPLICATION_ERROR(-20012, 'El alumno ' || v_id_alumno || ' no existe o no tiene grupo asignado');
    END;

    -- 2. El módulo existe
    BEGIN
        SELECT cod_ciclo INTO v_ciclo_modulo FROM modulo WHERE id_modulo = v_id_modulo;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RAISE_APPLICATION_ERROR(-20012, 'El módulo ' || v_id_modulo || ' no existe');
    END;

    -- 3. R2: el módulo es del ciclo del grupo del alumno
    IF v_ciclo_modulo <> v_ciclo_alumno THEN
        RAISE_APPLICATION_ERROR(-20010, 'El módulo ' || v_id_modulo || ' (' || v_ciclo_modulo || ') no es del ciclo del alumno ' || v_id_alumno || ' (' || v_ciclo_alumno || ')');
    END IF;

    -- 4. No está ya matriculado en ese curso académico
    SELECT COUNT(*)
    INTO   v_ya_matriculado
    FROM   matricula
    WHERE  id_alumno = v_id_alumno AND id_modulo = v_id_modulo AND curso_academico = v_curso;

    IF v_ya_matriculado > 0 THEN
        RAISE_APPLICATION_ERROR(-20013, 'El alumno ' || v_id_alumno || ' ya está matriculado del módulo ' || v_id_modulo || ' en ' || v_curso);
    END IF;

    -- 5. Convocatoria: una más que la última matrícula del módulo (máximo 4)
    SELECT NVL(MAX(convocatoria), 0) + 1
    INTO   v_convocatoria
    FROM   matricula
    WHERE  id_alumno = v_id_alumno AND id_modulo = v_id_modulo;

    IF v_convocatoria > c_max_convocatorias THEN
        RAISE_APPLICATION_ERROR(-20011, 'El alumno ' || v_id_alumno || ' ha agotado las ' || c_max_convocatorias || ' convocatorias del módulo ' || v_id_modulo);
    END IF;

    -- 6. Todo correcto: se inserta. No hay COMMIT: lo decide quien llama
    INSERT INTO matricula (id_alumno, id_modulo, curso_academico, convocatoria)
    VALUES (v_id_alumno, v_id_modulo, v_curso, v_convocatoria);
END;
/
```

Decisiones de diseño que conviene entender:

| Decisión | Motivo |
|---|---|
| Los dos primeros `SELECT INTO` van en **bloques anidados** | Convierten `NO_DATA_FOUND` en un error de negocio con código y mensaje propios (`-20012`), en lugar de dejar pasar un `ORA-01403` incomprensible |
| La convocatoria se calcula como `MAX(convocatoria) + 1` sobre **todas** las matrículas del alumno en ese módulo | Si nunca se ha matriculado, `MAX` devuelve `NULL`, `NVL(..., 0)` lo convierte en 0 y la convocatoria es 1 |
| `RAISE_APPLICATION_ERROR` en cada regla | Un código distinto por regla: la aplicación puede reaccionar sin analizar el texto |
| **No hay `COMMIT`** | La matrícula forma parte de una transacción mayor (matricular al alumno en todo el curso, Tema 5); la decide quien llama |
| El curso académico **no se valida** en el bloque | Lo hace la restricción `CK_MATRICULA_CURSO` de la tabla. Duplicar la validación crearía dos reglas que mantener |

**Pruebas.** Con el alumno 1 (grupo 1DAM, ciclo DAM), que ya cursó el módulo 2 en 2025-26 y lo suspendió (nota 4,75):

```sql
DEFINE id_alumno = 1
DEFINE id_modulo = 2
DEFINE curso     = 2026-27
-- y vuelve a ejecutar el bloque

SELECT id_matricula, id_modulo, curso_academico, convocatoria
FROM   matricula
WHERE  id_alumno = 1 AND curso_academico = '2026-27';
```

| ID_MATRICULA | ID_MODULO | CURSO_ACADEMICO | CONVOCATORIA |
|---|---|---|---|
| 20001 | 2 | 2026-27 | 2 |

*1 fila* (el identificador depende de las inserciones que se hayan hecho antes en la tabla)

La matrícula se ha creado como **segunda convocatoria**. Ahora, los errores:

```sql
DEFINE id_alumno = 1
DEFINE id_modulo = 2
DEFINE curso     = 2026-27   -- repetida
-- y vuelve a ejecutar el bloque
```

```text
ORA-20013: El alumno 1 ya está matriculado del módulo 2 en 2026-27
ORA-06512: at line 43
```

```sql
DEFINE id_alumno = 1
DEFINE id_modulo = 12
DEFINE curso     = 2026-27   -- el módulo 12 es de DAW; el alumno 1 es de DAM
-- y vuelve a ejecutar el bloque
```

```text
ORA-20010: El módulo 12 (DAW) no es del ciclo del alumno 1 (DAM)
ORA-06512: at line 33
```

Los números de línea de `ORA-06512` cuentan desde la línea `DECLARE` y te llevan al `RAISE_APPLICATION_ERROR` exacto. La batería completa de ocho pruebas está en la [práctica 5.8](/tema5-modificacion/guiones-practicas#práctica-58--matrícula-con-excepciones). Cuando termines, `ROLLBACK;` devuelve la tabla a su estado original.

> [!TIP]
> Un bloque que valida siempre tiene la misma estructura: **comprobar → rechazar con un error claro → actuar**. Las comprobaciones van primero y de más barata a más cara; el `INSERT` va al final, cuando ya no puede fallar por una regla de negocio.


---

{{< sesion n="6" h="1" tipo="t" >}}Guiones de mantenimiento: estructura, idempotencia y pruebas{{< /sesion >}}

## 7. Guiones de mantenimiento

El criterio RA5.e pide **diseñar guiones de sentencias para llevar a cabo tareas complejas**. Un guion de mantenimiento es un fichero `.sql` que una persona ejecuta en un servidor real: debe poderse **leer, revisar, repetir y auditar**.

### 7.1 Estructura de un guion profesional

```sql
-- =====================================================================
-- Guion    : justificar_faltas_huelga.sql
-- Autor    : Lorena L. Resusta
-- Fecha    : 2027-05-10
-- Entorno  : FREEPDB1 · esquema EDUGEST
-- Objetivo : Justificar las faltas del 12/03/2026 (huelga de transporte)
-- Reversión: ROLLBACK antes del COMMIT final; después, restaurar desde
--            BAK_FALTA_20270510 con el guion deshacer_faltas_huelga.sql
-- Filas esperadas: 1 (según comprobación previa del 09/05/2027)
-- =====================================================================

WHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK   -- cualquier error aborta y deshace
SET ECHO ON FEEDBACK ON TIMING ON
SPOOL justificar_faltas_huelga.log

-- 0. ¿Dónde estoy? (queda en la traza)
SELECT sys_context('USERENV','DB_NAME') AS bd, user AS esquema, SYSDATE FROM dual;

-- 1. Copia de seguridad de las filas afectadas  (DDL: ANTES de la transacción)
CREATE TABLE bak_falta_20270510 AS
SELECT * FROM falta_asistencia WHERE fecha = DATE '2026-03-12';

-- 2. Comprobación previa: las filas que se van a modificar
SELECT id_falta, id_matricula, fecha, horas, justificada
FROM   falta_asistencia
WHERE  fecha = DATE '2026-03-12' AND justificada = 'N';

-- 3. Transacción
SAVEPOINT antes_de_justificar;

UPDATE falta_asistencia
SET    justificada = 'S'
WHERE  fecha = DATE '2026-03-12'
AND    justificada = 'N';

-- 4. Comprobación posterior: no debe quedar ninguna sin justificar
SELECT COUNT(*) AS pendientes
FROM   falta_asistencia
WHERE  fecha = DATE '2026-03-12' AND justificada = 'N';   -- debe ser 0

-- 5. Registro de lo hecho
INSERT INTO log_mantenimiento (guion, filas, observaciones)
VALUES ('justificar_faltas_huelga.sql', SQL%ROWCOUNT,
        'Huelga de transporte del 12/03/2026');

-- 6. Confirmación
COMMIT;

SPOOL OFF
```

| Elemento | Para qué sirve |
|---|---|
| Cabecera con autor, fecha, entorno y objetivo | Que quien lo lea en 2029 sepa qué hace y quién responde |
| `WHENEVER SQLERROR EXIT ... ROLLBACK` | Que un error **detenga** el guion y no deje medias tintas |
| `SPOOL` | Dejar traza de todo lo ejecutado y de sus resultados: es la evidencia de la intervención |
| Copia previa con CTAS | Poder volver atrás después del `COMMIT` |
| `SELECT` de comprobación previa | Verificar las filas antes de tocarlas |
| `SAVEPOINT` | Poder retroceder un paso sin perder el resto |
| `SELECT` de comprobación posterior | Confirmar que el resultado es el esperado |
| Registro en una tabla de auditoría | Saber qué se ejecutó, cuándo y con qué resultado |
| `COMMIT` **al final y una sola vez** | Que todo el guion sea una única unidad de trabajo |

```sql
-- Tabla de auditoría de los guiones de mantenimiento
CREATE TABLE log_mantenimiento (
    id_log         NUMBER(8) GENERATED BY DEFAULT ON NULL AS IDENTITY
                   CONSTRAINT pk_log_mantenimiento PRIMARY KEY,
    guion          VARCHAR2(80) CONSTRAINT nn_log_guion NOT NULL,
    ejecutado      TIMESTAMP DEFAULT SYSTIMESTAMP CONSTRAINT nn_log_fecha NOT NULL,
    usuario        VARCHAR2(30)  DEFAULT USER CONSTRAINT nn_log_usuario NOT NULL,
    filas          NUMBER(8),
    observaciones  VARCHAR2(400)
);
```

> [!WARNING]
> El `CREATE TABLE` del paso 1 es **DDL**: lleva `COMMIT` implícito. Por eso está **antes** de la transacción y nunca en medio. Si lo colocaras entre el `UPDATE` y el `COMMIT`, confirmarías el `UPDATE` sin querer y el `WHENEVER SQLERROR ... ROLLBACK` ya no podría deshacerlo.

### 7.2 Idempotencia

Un guion es **idempotente** si ejecutarlo dos veces produce el mismo resultado que ejecutarlo una. Es una propiedad valiosísima: permite relanzar sin miedo un proceso interrumpido.

| Forma de conseguirla | Ejemplo |
|---|---|
| Condición que ya no se cumple tras la primera pasada | `WHERE justificada = 'N'`: la segunda vez afecta a 0 filas |
| `MERGE` en lugar de `INSERT` | Actualiza lo que ya está y añade lo que falta (Tema 5, §5.4) |
| `INSERT … WHERE NOT EXISTS` | No duplica las filas ya insertadas |
| Clave primaria que impide el duplicado | `HISTORICO_NOTA` falla con `ORA-00001` en el segundo archivado |
| Comprobación de guarda al principio | Si ya existen matrículas de 2026-27, el guion se detiene |

```sql
-- Guarda: detener el guion si ya se ejecutó
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

### 7.3 Cómo se prueba un guion antes de ejecutarlo en producción

- [ ] Se ejecuta en un **entorno de pruebas** con una copia reciente de los datos reales.
- [ ] Se anota el número de filas afectadas de **cada** sentencia y se compara con lo previsto.
- [ ] Se ejecuta **dos veces** para comprobar la idempotencia.
- [ ] Se provoca un error a mitad (renombrando una tabla, por ejemplo) y se verifica que **no queda ningún cambio** aplicado.
- [ ] Se comprueba que existe y funciona el guion de reversión.
- [ ] Se revisa que no haya DDL dentro de la transacción.
- [ ] Se ejecuta en producción con `SPOOL` activo, y el `.log` se archiva junto al guion.


---


## 8. Errores frecuentes

| Síntoma | Causa | Solución |
|---|---|---|
| El bloque «funciona» pero no muestra nada | Falta `SET SERVEROUTPUT ON` o el panel de salida está cerrado | Actívalo en cada sesión (§2.4) |
| SQLcl se queda esperando tras escribir el bloque | Falta la `/` final | Escríbela en una línea sola (§2.3) |
| `PLS-00103: Encountered the symbol ...` | `;` olvidado, `END IF` o `END LOOP` sin cerrar, coma sobrante | Revisa la línea que indica y la anterior (§2.5) |
| `ORA-01403: no data found` | `SELECT ... INTO` sin filas | Trata `NO_DATA_FOUND` o usa un agregado (§6.2) |
| `ORA-01422: exact fetch returns more than requested number of rows` | `SELECT ... INTO` con varias filas | Concreta el `WHERE` o recorre las filas con un bucle `FOR` |
| La condición `WHERE id_alumno = id_alumno` devuelve todas las filas | Parámetro o variable con el mismo nombre que la columna | Prefijos `p_` y `v_` (§3.4) |
| Un `IF x > 5 ... ELSE` marca como suspenso a quien no tiene nota | La comparación con `NULL` es desconocida y cae en el `ELSE` | Pregunta primero `IS NULL` (§5.1) |
| `ORA-06510: unhandled user-defined exception` | `RAISE` de una excepción propia sin manejador | Trátala o usa `RAISE_APPLICATION_ERROR` |
| `WHEN OTHERS THEN NULL` y datos que no cuadran | Un error se ha tragado en silencio | Registra y relanza con `RAISE;` (§6.3) |
| Los cambios del bloque no aparecen en otra sesión | Falta el `COMMIT` (que, por diseño, el bloque no hace) | Confirma al final del guion |

---

## 9. Buenas prácticas

- **Usa `%TYPE` y `%ROWTYPE`** en lugar de repetir los tipos de las columnas.
- **Prefijos en los nombres** (`v_`, `p_`, `c_`, `r_`, `e_`) para no confundir variables, parámetros y columnas.
- **Escribe siempre el `ELSE`** de un `CASE` y la rama `IS NULL` de las condiciones que manejen datos que puedan faltar.
- **Trata solo los errores que sabes tratar.** Nada de `WHEN OTHERS THEN NULL`: registra y vuelve a lanzar con `RAISE;`.
- **Define un catálogo de errores propios** (`-20010`...), con un código por regla y un mensaje que diga qué dato falló.
- **Guiones versionados, con cabecera, `SPOOL`, comprobaciones e idempotencia.** Nada de cambios a mano en la rejilla para tareas que se repiten.
- **Un guion confirma una sola vez, al final,** y solo si las comprobaciones han salido bien.
- **Registra lo que haces** en una tabla de auditoría: fecha, usuario, guion y filas afectadas.
- **Si tienes que deshacer una parte, usa `SAVEPOINT`** de forma explícita; no dependas de lo que ocurra de forma implícita.
- **Marca en la documentación lo específico de Oracle** si el código tiene que portarse a otro gestor.

---

{{< tarjetas titulo="Repasa los términos del tema 5" >}}
- t: "Bloque anónimo"
  d: "Código PL/SQL sin nombre: DECLARE, BEGIN, EXCEPTION, END."
- t: "Excepción"
  d: "Error controlado en la sección EXCEPTION."
{{< /tarjetas >}}

## 10. Resumen

| Concepto | Idea clave | Sintaxis esencial |
|---|---|---|
| Ejecución de guiones | Las órdenes de cliente (`SET`, `SPOOL`, `@`) no las entiende el servidor; los bloques PL/SQL terminan en `;` y `/` | `@fichero.sql`, `SET SERVEROUTPUT ON` |
| Bloque | `DECLARE` (opcional), `BEGIN` ... `EXCEPTION` (opcional) ... `END;` | `DECLARE ... BEGIN ... END;` |
| Variables | Con tipo, heredables de la tabla con `%TYPE` y `%ROWTYPE`. Distintas de las variables de **sustitución** (`&`), que resuelve el cliente | `v_x tabla.col%TYPE;`, `SELECT ... INTO` |
| Control de flujo | `IF`/`ELSIF`, `CASE`, `LOOP`/`WHILE`/`FOR`; cuidado con `NULL` | `IF ... THEN ... END IF;` |
| Excepciones | Predefinidas, propias, `PRAGMA EXCEPTION_INIT`; `RAISE_APPLICATION_ERROR` entre -20000 y -20999 | `EXCEPTION WHEN ... THEN` |
| Guiones de mantenimiento | Cabecera, copia previa, comprobaciones, `SAVEPOINT`, `COMMIT` único, `SPOOL` e idempotencia | `WHENEVER SQLERROR EXIT ROLLBACK`, `SPOOL` |

Ideas que conviene llevarse grabadas:

1. **Un `&` lo resuelve el cliente; un `v_` lo resuelve el servidor.**
2. **La excepción más peligrosa es la que se traga en silencio.**
3. **Un guion bien hecho se puede ejecutar dos veces sin romper nada.**
4. **Se prueba antes en un entorno de pruebas, con copia previa y con `SPOOL` activo.**

---

## 11. Autoevaluación

{{< quiz >}}
- q: "¿Qué hace `SELECT AVG(nota_final) INTO v_media FROM matricula WHERE id_alumno = 30;` si el alumno 30 no tiene matrículas?"
  options: ["Lanza `NO_DATA_FOUND`", "Lanza `TOO_MANY_ROWS`", "Asigna `NULL` a `v_media`, sin error", "Asigna 0 a `v_media`"]
  answer: 2
  explain: "Un agregado sin `GROUP BY` devuelve siempre exactamente una fila, aunque no haya datos de entrada. `AVG` de ningún valor es `NULL`: no hay excepción, y `v_media` queda a `NULL`."
- q: "En un guion se escribe `&grupo` dentro de un bloque PL/SQL. ¿Quién sustituye el valor?"
  options: ["El servidor Oracle, al compilar el bloque", "El cliente (SQLcl, SQL*Plus, SQL Developer), antes de enviar el texto al servidor", "El bloque, en cada vuelta de un bucle", "La base de datos, al confirmar la transacción"]
  answer: 1
  explain: "Una variable de sustitución es texto que el cliente pega en el código antes de enviarlo. El servidor recibe ya el valor y no sabe que existió un `&`."
- q: "Un bloque ejecuta `SELECT nombre INTO v_nombre FROM alumno WHERE id_alumno = 999;` y el alumno no existe. ¿Qué ocurre?"
  options: ["`v_nombre` queda a `NULL` sin error", "Se lanza `NO_DATA_FOUND` (`ORA-01403`)", "Se lanza `TOO_MANY_ROWS` (`ORA-01422`)", "El bloque no compila"]
  answer: 1
  explain: "`SELECT ... INTO` exige exactamente una fila. Sin filas se lanza `NO_DATA_FOUND`; con varias, `TOO_MANY_ROWS`."
- q: "Un manejador `WHEN OTHERS THEN NULL;` tras un `UPDATE` que falla. ¿Qué problema tiene?"
  options: ["No compila", "Traga el error en silencio: el guion continúa como si todo hubiera ido bien", "Deshace automáticamente la transacción", "Convierte el error en un aviso"]
  answer: 1
  explain: "La excepción más peligrosa es la que se traga. Si no sabes tratar el error, regístralo y relánzalo con `RAISE;`."
- q: "¿Qué significa que un guion de mantenimiento sea idempotente?"
  options: ["Que se ejecuta más rápido la segunda vez", "Que ejecutarlo dos veces deja la base de datos igual que ejecutarlo una", "Que no necesita `COMMIT`", "Que solo lo puede ejecutar un usuario"]
  answer: 1
  explain: "La idempotencia permite relanzar un guion interrumpido sin duplicar ni corromper datos (por ejemplo, con `MERGE` o con comprobaciones previas)."
- q: "En mitad de un guion transaccional aparece un `CREATE TABLE`. ¿Qué consecuencia tiene?"
  options: ["Ninguna: el DDL se deshace con el `ROLLBACK`", "Confirma implícitamente la transacción en curso, y lo anterior ya no se puede deshacer", "Bloquea todas las tablas", "Solo funciona dentro de un bloque anónimo"]
  answer: 1
  explain: "Cada sentencia DDL lleva un `COMMIT` implícito. Las copias y los cambios de estructura se hacen antes de abrir la transacción."
{{< /quiz >}}

## Referencias

- [Oracle AI Database 26ai: Database PL/SQL Language Reference](https://docs.oracle.com/en/database/oracle/oracle-database/26/lnpls/) — bloques, variables, control de flujo, excepciones y disparadores (incluidos los compuestos y la restricción de la tabla mutante).
- [Oracle AI Database 26ai: SQL*Plus User's Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/26/sqpug/) — variables de sustitución, `SET SERVEROUTPUT`, `SPOOL` y ejecución de guiones.
- [Oracle SQLcl: documentación](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/) y [Oracle SQL Developer](https://docs.oracle.com/en/database/oracle/sql-developer/).
- [Oracle AI Database 26ai: Database Error Messages](https://docs.oracle.com/en/error-help/db/) — `ORA-01403`, `ORA-02292`, `ORA-06510`...
- [Real Decreto 1629/2009, de 30 de octubre](https://www.boe.es/eli/es/rd/2009/10/30/1629) — enseñanzas mínimas del módulo 0372 Gestión de bases de datos (RA5.e).
