---
title: "Programación de la base de datos con PL/SQL"
weight: 1
bookToc: true
---

# UD09 · Programación de la base de datos con PL/SQL

## Resumen del tema

Hasta ahora, la lógica de nuestras tareas vivía **fuera** de la base de datos: en un guion `.sql` que lanzábamos a mano o en la aplicación que consulta Oracle. Eso funciona mientras la tarea sea una secuencia de sentencias. Deja de funcionar cuando hace falta **decidir** (¿tiene el alumno faltas suficientes para perder la evaluación continua?), **repetir** (recorrer todos los alumnos de un grupo), **reaccionar a un error** (¿qué hago si el módulo no existe?) o **garantizar una regla** que nadie pueda saltarse, entre ellas las que en la UD03 llamamos *restricciones que el modelo lógico no puede expresar*.

La solución es programar **dentro del servidor**. Oracle incorpora para ello el lenguaje **PL/SQL** (*Procedural Language / SQL*): SQL más variables, condiciones, bucles, cursores y excepciones, organizado en **bloques**. Con él se construyen los objetos que guarda la propia base de datos: **funciones**, **procedimientos**, **paquetes** y **disparadores**, y con el planificador `DBMS_SCHEDULER` se ejecutan solos a la hora que se indique.

La unidad avanza en cinco pasos: primero qué formas hay de automatizar y con qué herramientas se trabaja (§1 y §2); después el lenguaje (bloques, variables, control de flujo, funciones del gestor y cursores, §3 a §7); a continuación los subprogramas almacenados y el tratamiento de errores (§8 a §10); luego los disparadores, con la auditoría de notas, la integridad que las restricciones no alcanzan y el famoso error de la **tabla mutante** (§11); y por último las tareas programadas, los paquetes y la comparación con otros gestores (§12 a §14).

Todos los ejemplos se ejecutan sobre el esquema de referencia **EDUGEST** con los [scripts del proyecto](/guia/proyecto-edugest#4-scripts-descargables) cargados (32 alumnos, 143 matrículas, 46 faltas) y usan la sintaxis de **Oracle AI Database 26ai Free**. Cada ejemplo indica la salida que debes obtener. Cuando algo es propio de un gestor concreto se señala con una etiqueta o una nota.

{{< ra "RA5:a,b,c,d,e,f,g,h,i,j" "RA4:d,h" "RA6:h" >}}

### Objetivos de aprendizaje

Al terminar esta unidad serás capaz de:

- Distinguir una consulta, un guion, un bloque anónimo, una función, un procedimiento, un paquete, un disparador y una tarea programada, y elegir la forma de automatización adecuada para cada necesidad (RA5.a).
- Editar y ejecutar guiones con SQL Developer, SQLcl o SQL\*Plus, usando variables de sustitución y la salida de `DBMS_OUTPUT` (RA5.b, RA5.c).
- Escribir bloques PL/SQL con variables, constantes y tipos `%TYPE` y `%ROWTYPE`, y distinguir las variables de sustitución del cliente de las variables PL/SQL del servidor.
- Aplicar estructuras de control de flujo (`IF`, `CASE`, `LOOP`, `WHILE`, `FOR`) y las funciones predefinidas del gestor (RA5.e, RA5.g).
- Recorrer conjuntos de filas con cursores implícitos, explícitos, de bucle `FOR` y con parámetros (RA5.i).
- Definir funciones y procedimientos de usuario con parámetros `IN`, `OUT` e `IN OUT` (RA5.f).
- Tratar errores con excepciones predefinidas y propias, `PRAGMA EXCEPTION_INIT` y `RAISE_APPLICATION_ERROR` (RA5.j).
- Implementar con disparadores la auditoría de cambios y las reglas de integridad que el modelo lógico no puede declarar, y resolver el error de tabla mutante con un disparador compuesto (RA5.h, RA4.h, RA6.h).
- Programar tareas periódicas con `DBMS_SCHEDULER`, agrupar subprogramas en paquetes y reconocer los equivalentes en MySQL/MariaDB, PostgreSQL y SQL Server (RA5.a, RA5.d, RA4.d).

### Temporalización

La unidad ocupa **7 horas de aula** (4 de teoría y 3 de práctica). Es la unidad con más código del curso: conviene escribirlo a mano y recompilarlo, no copiarlo y pegarlo. Las prácticas largas (la tabla mutante, las tareas programadas, el paquete de secretaría y el proyecto) se completan fuera del horario de aula.

{{< sesiones unidad="UD09" horas="7" >}}
items:
  - {h: 1, tipo: T, t: "Formas de automatizar, herramientas, estructura del bloque, variables, tipos y `DBMS_OUTPUT`", ref: "§1 a §4"}
  - {h: 1, tipo: P, t: "Primeros bloques: el expediente de un alumno", ref: "Práctica 9.1"}
  - {h: 1, tipo: T, t: "Control de flujo, funciones del gestor, cursores y funciones de usuario", ref: "§5 a §8 · laboratorio de bloques"}
  - {h: 1, tipo: P, t: "Biblioteca de funciones de EduGest", ref: "Práctica 9.2"}
  - {h: 1, tipo: T, t: "Excepciones y procedimientos almacenados", ref: "§9 y §10"}
  - {h: 1, tipo: P, t: "Matrícula con excepciones (la 9.4, boletines con cursores, se termina en casa)", ref: "Prácticas 9.3 y 9.4"}
  - {h: 1, tipo: T, t: "Disparadores, tareas programadas con `DBMS_SCHEDULER` y paquetes", ref: "§11 a §14 · simulador de disparadores"}
autonomo:
  - "Práctica 9.4 (cursores: boletines e informes), si no se ha terminado en el aula"
  - "Práctica 9.5 (disparadores de integridad y auditoría)"
  - "Práctica 9.6 (reto: la tabla mutante)"
  - "Práctica 9.7 (tareas programadas)"
  - "Práctica 9.8 (reto: el paquete de secretaría)"
  - "Proyecto EduGest · UD09 (lógica en el servidor)"
{{< /sesiones >}}

> [!IMPORTANT]
> Trabaja siempre conectado como `EDUGEST` y con la salida activada (`SET SERVEROUTPUT ON`). Todo el código de esta unidad se prueba con un método fijo:
>
> 1. **Predice** qué debe mostrar o devolver antes de ejecutarlo.
> 2. Ejecuta y compara con la salida que figura en los apuntes.
> 3. Si falla, lee el error **de arriba abajo**: el primer mensaje (`PLS-` en compilación, `ORA-` en ejecución) es la causa; los siguientes solo dicen dónde ocurrió.
> 4. Guarda cada subprograma en su propio fichero `.sql` terminado en `/`: así se recompila y se versiona.

---

{{< sesion n="1" h="1" tipo="t" >}}Formas de automatizar, herramientas, bloques y variables{{< /sesion >}}

## 1. Programar dentro del servidor

### 1.1 Qué problema resuelve

SQL es un lenguaje **declarativo**: dices *qué* quieres, no *cómo* obtenerlo. Es excelente para consultar y modificar conjuntos de filas, pero no tiene variables, ni condiciones, ni bucles, ni forma de reaccionar a un error. En cuanto una tarea necesita alguna de esas cosas, hay dos opciones: sacar los datos a una aplicación y programar allí la lógica, o **programarla dentro de la base de datos**.

Piensa en la matrícula de un alumno en EduGest. Antes de insertar la fila hay que comprobar que el alumno existe y tiene grupo, que el módulo es de su ciclo, que no está ya matriculado ese curso y que no ha agotado las cuatro convocatorias. Son cuatro consultas, tres decisiones y un `INSERT`, y esas reglas deben cumplirse **siempre**, venga la matrícula de la aplicación web, de un script de la secretaría o de una herramienta gráfica.

La UD03 ya identificó las reglas de negocio de EduGest que el modelo lógico no puede expresar. Esta unidad las implementa:

| Código | Regla de negocio | Por qué no basta una restricción declarativa | Dónde se implementa |
|---|---|---|---|
| R1 | El jefe de un departamento pertenece a ese departamento | Compara una fila de `DEPARTAMENTO` con una de `PROFESOR` | Disparador (§11.3) |
| R2 | Un alumno solo se matricula en módulos del ciclo de su grupo, hasta 4 convocatorias | Implica `ALUMNO`, `GRUPO`, `MODULO` y `MATRICULA` | Procedimiento de matrícula (§10.5) |
| R3 | No hay faltas anteriores a la fecha de matrícula | Compara dos tablas | Disparador (práctica 9.5) |
| R4 | Un profesor no supera 20 horas lectivas semanales | Es una **suma** sobre varias filas | Disparador compuesto (práctica 9.6) |
| R5 | Un grupo no supera 30 alumnos | Es un **recuento** sobre varias filas | Disparador compuesto (§11.6) |
| R6 | La nota va en múltiplos de 0,25 | Es una regla de **una fila** | `CHECK` (UD05): no necesita PL/SQL |

> [!NOTE]
> La regla R6 está en la tabla a propósito: **no todo se resuelve con un disparador**. Si una restricción declarativa (`CHECK`, `UNIQUE`, clave ajena) puede expresar la regla, es siempre preferible: es más rápida, más clara y el optimizador la conoce.

### 1.2 Formas de automatizar tareas

El criterio RA5.a pide identificar las formas de automatizar una tarea en un gestor. En Oracle son estas:

| Forma | Qué es | Cuándo se ejecuta | Ejemplo en EduGest |
|---|---|---|---|
| **Guion** (*script*) | Fichero de texto con sentencias SQL y órdenes del cliente | Cuando alguien lo lanza (`@fichero.sql`) | `edugest_01_esquema.sql` |
| **Bloque anónimo** | Bloque PL/SQL sin nombre que el cliente envía al servidor | Cuando el cliente lo envía; no se guarda | Un cálculo puntual de comprobación |
| **Función almacenada** | Subprograma con nombre que **devuelve un valor** | Cuando se invoca desde SQL o PL/SQL | `fn_calificacion` |
| **Procedimiento almacenado** | Subprograma con nombre que **realiza una acción** | Cuando se invoca (`EXEC`, `CALL`, otro bloque) | `pr_matricular` |
| **Paquete** | Agrupación de subprogramas, constantes y variables | Cuando se invoca uno de sus elementos | `pkg_secretaria` |
| **Disparador** (*trigger*) | Bloque PL/SQL asociado a un **evento** | **Automáticamente** al ocurrir el evento (un `UPDATE`, un `CREATE`, una conexión) | `trg_auditoria_nota` |
| **Tarea programada** (*job*) | Ejecución de un subprograma o bloque según un calendario | A la hora indicada, sin intervención humana | `JOB_RESUMEN_NOCTURNO` |

Fuera del servidor existen otras formas de automatizar, también válidas: el programador de tareas del sistema operativo (`cron`, Programador de tareas de Windows) lanzando SQLcl, o la propia aplicación. La diferencia es **dónde vive la lógica**: dentro, viaja con la base de datos y la protegen sus privilegios; fuera, depende de otro sistema.

### 1.3 Consulta, guion, bloque, función, procedimiento, paquete y disparador

Es la confusión más frecuente al empezar. Esta tabla las separa por sus propiedades:

| | Consulta | Guion | Bloque anónimo | Función | Procedimiento | Paquete | Disparador |
|---|---|---|---|---|---|---|---|
| **Contenido** | Una sentencia SQL | Varias sentencias y órdenes del cliente | Un bloque PL/SQL | Un bloque PL/SQL con `RETURN` | Un bloque PL/SQL | Especificación + cuerpo | Un bloque PL/SQL + evento |
| **¿Se guarda en la BD?** | No (salvo como vista) | No: vive en un fichero | No | **Sí** | **Sí** | **Sí** | **Sí** |
| **¿Tiene nombre?** | No | El del fichero | No | Sí | Sí | Sí | Sí |
| **¿Quién lo ejecuta?** | El cliente | El cliente | El cliente | El que lo llama | El que lo llama | El que lo llama | **El propio Oracle** |
| **¿Devuelve valor?** | Un conjunto de filas | No | No | **Un valor** | No (usa parámetros `OUT`) | Según el elemento | No |
| **¿Se usa dentro de un `SELECT`?** | Como subconsulta | No | No | **Sí** | No | Sus funciones, sí | No |
| **Se compila** | En cada ejecución | En cada ejecución | En cada ejecución | **Una vez**, al crearla | **Una vez** | **Una vez** | **Una vez** |

Tres ideas para quedarse con la tabla:

1. **Lo que se guarda en la base de datos se compila una sola vez** y se ejecuta muchas. Un guion o un bloque anónimo se analizan cada vez que se envían.
2. **Una función devuelve un valor y se puede usar en una consulta; un procedimiento hace algo.** Si necesitas llamarla desde un `SELECT`, es una función.
3. **Un disparador nadie lo llama:** se ejecuta cuando ocurre su evento. Por eso hay que escribirlos con mucho cuidado.

### 1.4 Cliente o servidor: dónde poner la lógica

Cada vez que una aplicación lanza una sentencia SQL hay un **viaje de ida y vuelta** por la red. Si la matrícula de un alumno en cinco módulos se programa en la aplicación, son decenas de viajes; si se programa en un procedimiento almacenado, es **una** llamada.

```text
 Lógica en la aplicación                       Lógica en el servidor
 ───────────────────────                       ──────────────────────
 App ──SELECT alumno──────────► Oracle         App ──pr_matricular(1, 2, '2026-27')──► Oracle
 App ◄─────────────filas──────  Oracle                                                  │ valida
 App ──SELECT módulo──────────► Oracle                                                  │ calcula
 App ◄─────────────filas──────  Oracle                                                  │ inserta
 App ──INSERT matricula───────► Oracle         App ◄──────────────────────OK / error─────┘
 App ◄──────────────filas─────  Oracle
 (3 viajes como mínimo)                        (1 viaje)
```

| A favor de programar en el servidor | En contra |
|---|---|
| **Menos tráfico de red**: una llamada en lugar de muchas | **Portabilidad**: PL/SQL solo funciona en Oracle; cambiar de gestor obliga a reescribir |
| **Una única implementación** de la regla, válida para todas las aplicaciones | Más difícil de **probar, depurar y versionar** que el código de una aplicación |
| **Seguridad**: se puede conceder `EXECUTE` sobre un procedimiento sin dar acceso a las tablas | Consume **CPU del servidor**, que es el recurso más caro de escalar |
| **Integridad**: la regla no se puede saltar insertando por otra vía | La lógica queda **repartida** entre base de datos y aplicación |
| **Rendimiento**: el código ya está compilado y las sentencias SQL, analizadas | Un disparador mal pensado es una **lógica oculta** que sorprende a todo el mundo |

> [!TIP]
> Regla práctica: pon en el servidor lo que protege la **integridad** de los datos y lo que es una **operación atómica de negocio** (matricular, promocionar, anular). Deja en la aplicación la presentación, los flujos de usuario y todo lo que no afecte a la corrección de los datos.

### 1.5 Qué es PL/SQL

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

Cada paso de un motor al otro (*context switch*) tiene un coste pequeño pero medible. Por eso, cuando una tarea se puede escribir como **una sola sentencia SQL**, esa es casi siempre la mejor versión (§7.7).

{{< sgbd "Oracle 26ai" >}}

PL/SQL es propio de Oracle. Cada gestor tiene su lenguaje: PostgreSQL usa **PL/pgSQL**, MySQL y MariaDB usan el lenguaje de rutinas almacenadas **SQL/PSM**, SQL Server usa **Transact-SQL (T-SQL)**. Los conceptos (variables, condiciones, bucles, cursores, excepciones, disparadores) son los mismos; la sintaxis cambia. El apartado 14 los compara.

---

## 2. Herramientas y ejecución de guiones

### 2.1 Herramientas para editar guiones

El criterio RA5.c pide identificar las herramientas disponibles. Un guion PL/SQL es texto: se puede escribir en cualquier editor, pero las herramientas especializadas aportan resaltado, ejecución directa y acceso al diccionario de datos.

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

El criterio RA5.b pide reconocer los métodos de ejecución de guiones. Un guion puede ejecutarse de varias maneras:

| Método | Dónde | Qué hace |
|---|---|---|
| `@ruta/fichero.sql` | SQLcl, SQL\*Plus | Ejecuta el guion. La ruta es relativa al directorio actual |
| `@@fichero.sql` | SQLcl, SQL\*Plus | Ejecuta el guion **relativo al guion que lo llama**: útil en un guion maestro que invoca otros |
| `START fichero.sql` | SQLcl, SQL\*Plus | Sinónimo de `@` |
| `sql edugest@servicio @fichero.sql` | Terminal | Se conecta y ejecuta el guion en modo *batch* (sin interacción) |
| `F5` (*Ejecutar script*) | SQL Developer | Ejecuta **todo** el guion tal cual; `Ctrl+Intro` ejecuta solo la sentencia bajo el cursor |
| Tarea programada | `DBMS_SCHEDULER` | Ejecuta un procedimiento o bloque a la hora indicada (§12) |

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
| Bloque PL/SQL anónimo, `CREATE PROCEDURE`, `CREATE FUNCTION`, `CREATE TRIGGER`, `CREATE PACKAGE` | `;` **y** `/` en una línea sola | Dentro del bloque hay muchos `;`, así que el `;` ya no sirve para saber dónde acaba. La `/` dice «el bloque termina aquí, envíalo» |

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
> `DBMS_OUTPUT` es una herramienta de **depuración y de prácticas**, no un mecanismo de producción: el texto solo existe mientras dura la ejecución, se muestra al final (no mientras el bloque trabaja) y un procedimiento que se ejecuta desde una aplicación o una tarea programada no tiene a nadie delante para leerlo. Para dejar constancia hay que escribir en una **tabla de registro** (práctica 9.7).

### 2.5 Errores de compilación

Un procedimiento, función o disparador se **compila al crearlo**. Si hay errores, Oracle lo crea igualmente pero en estado `INVALID` y avisa con `Warning: Procedure created with compilation errors.` Los errores de compilación empiezan por `PLS-`:

```sql
SHOW ERRORS
-- o, desde cualquier cliente:
SELECT line, position, text
FROM   user_errors
WHERE  name = 'FN_EDAD'
ORDER  BY sequence;
```

| Mensaje | Causa habitual |
|---|---|
| `PLS-00103: Encountered the symbol "..." when expecting one of the following` | Error de sintaxis: un `;` olvidado, un `END IF` sin cerrar, una coma sobrante |
| `PLS-00201: identifier 'X' must be declared` | Nombre mal escrito, variable no declarada, o falta de privilegio sobre el objeto |
| `PLS-00302: component 'X' must be declared` | Se usa una columna o un campo que no existe (`r_alumno.telefon`) |
| `PLS-00306: wrong number or types of arguments in call to 'X'` | Llamada con más, menos o distintos parámetros de los declarados |
| `PLS-00428: an INTO clause is expected in this SELECT statement` | Un `SELECT` dentro de un bloque sin `INTO` (ni cursor) |
| `PLS-00363: expression 'X' cannot be used as an assignment target` | Se asigna a una constante, a un parámetro `IN` o al índice de un bucle `FOR` |

---

{{% curiosidad titulo="PL/SQL se parece a Ada" %}}
La sintaxis de PL/SQL (`BEGIN … END;`, `:=`, `IF … THEN … END IF;`, las excepciones) está inspirada en el lenguaje **Ada**. Apareció a finales de los años ochenta, para poder meter lógica de programa dentro del servidor y no solo sentencias sueltas.
{{% /curiosidad %}}

## 3. Estructura de un bloque PL/SQL

### 3.1 Las cuatro secciones

Todo programa PL/SQL se construye con **bloques**. Un bloque tiene hasta cuatro secciones, y solo `BEGIN ... END` es obligatoria:

```text
DECLARE        -- 1. Declaraciones (opcional): variables, constantes, cursores, excepciones
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
| `SELECT` | Sí, **con `INTO`** o dentro de un cursor | `SELECT` sin `INTO` da `PLS-00428` |
| `COMMIT`, `ROLLBACK`, `SAVEPOINT` | Sí | El control de la transacción (UD08) funciona igual |
| `CREATE`, `ALTER`, `DROP` (DDL) | **No directamente** | Hay que usar SQL dinámico: `EXECUTE IMMEDIATE 'CREATE TABLE ...'` |
| `GRANT`, `REVOKE` (DCL) | **No directamente** | También con `EXECUTE IMMEDIATE` |
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

Los bloques anidados no sirven solo para organizar el código: son la herramienta para **limitar el alcance de una excepción** (§9.7).

### 3.4 Comentarios, mayúsculas y convenciones de nombres

PL/SQL no distingue mayúsculas de minúsculas en el código (`begin` es `BEGIN`), pero sí en los **literales de texto** (`'EduGest'` y `'EDUGEST'` son distintos). Los comentarios son de línea (`-- texto`) o de varias líneas (`/* texto */`).

Un prefijo en cada nombre evita el error más común: que una variable se llame igual que una columna. Si en `WHERE id_alumno = id_alumno` ambos son la columna, la condición es siempre verdadera. EduGest usa estas convenciones:

| Elemento | Prefijo | Ejemplo |
|---|---|---|
| Variable local | `v_` | `v_media` |
| Constante | `c_` | `c_max_convocatorias` |
| Parámetro | `p_` | `p_id_alumno` |
| Registro (*record*) | `r_` | `r_alumno` |
| Cursor | `c_` o `cur_` | `c_notas` |
| Excepción propia | `e_` | `e_sin_grupo` |
| Tipo definido por el usuario | `t_` | `t_grupos` |
| Función / procedimiento | `fn_` / `pr_` | `fn_edad`, `pr_matricular` |
| Disparador | `trg_` | `trg_auditoria_nota` |
| Paquete | `pkg_` | `pkg_secretaria` |

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
| `cursor%ROWTYPE` | Un registro con las columnas del cursor | `r_nota c_notas%ROWTYPE;` |

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

Es la confusión más frecuente de la unidad. Observa este bloque:

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
| **¿Existe en un procedimiento almacenado?** | **No**: se resolvería una vez al crearlo | Sí |
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
| `SQLCODE`, `SQLERRM` | Código y mensaje del último error (solo dentro de un manejador, §9.3) |
| `SQL%ROWCOUNT` | Filas afectadas por la última sentencia DML (§7.1) |

Estas funciones son las que permiten registrar **quién** hizo un cambio y **desde dónde**: se usan en la auditoría (§11.2).

{{< quiz >}}
- q: "En el bloque `BEGIN DBMS_OUTPUT.PUT_LINE('Hola'); END;` no aparece nada por pantalla, pero tampoco hay error. ¿Qué falta?"
  options: ["Un `COMMIT` antes del `END`", "`SET SERVEROUTPUT ON` en el cliente", "Declarar una variable de tipo texto", "Cambiar `PUT_LINE` por `PRINT`"]
  answer: 1
  explain: "`DBMS_OUTPUT` escribe en un búfer del servidor y es el cliente quien lo muestra, solo si se le ha pedido con `SET SERVEROUTPUT ON`. Sin esa orden el bloque se ejecuta correctamente, pero no se ve nada."
- q: "Un bloque contiene `WHERE cod_grupo = '&g'` y se ejecuta en SQLcl. ¿Quién sustituye `&g` y cuándo?"
  options: ["Oracle, durante la ejecución del bloque", "El cliente, antes de enviar el bloque al servidor", "El motor PL/SQL, cuando lee la variable `g`", "Nadie: es una variable PL/SQL que vale `NULL`"]
  answer: 1
  explain: "`&g` es una variable de **sustitución**: el cliente (SQLcl, SQL*Plus, SQL Developer) reemplaza el texto antes de enviar nada. El servidor recibe ya el valor y no sabe que existió un `&`. Por eso no existe dentro de un procedimiento almacenado."
- q: "¿Qué ocurre con `SELECT nombre INTO v_nombre FROM alumno WHERE nia LIKE '104507%';` si el patrón coincide con tres alumnos?"
  options: ["Se asigna el primero y se ignoran los demás", "Se asigna el último", "Se lanza `TOO_MANY_ROWS` y no se asigna ningún valor", "Se lanza `NO_DATA_FOUND`"]
  answer: 2
  explain: "`SELECT ... INTO` exige exactamente una fila. Con varias se lanza `TOO_MANY_ROWS` (`ORA-01422`). Para recorrer varias filas hace falta un cursor (§7)."
- q: "¿Qué ventaja tiene declarar `v_nia alumno.nia%TYPE` en lugar de `v_nia CHAR(8)`?"
  options: ["La variable es más rápida", "La variable hereda el tipo de la columna y sigue siendo correcta si la columna cambia", "Permite almacenar valores nulos", "Hace que la variable sea una constante"]
  answer: 1
  explain: "`%TYPE` consulta el diccionario de datos: si se amplía o cambia la columna, el código sigue siendo coherente sin tocarlo. Una longitud escrita a mano se queda anticuada."
{{< /quiz >}}


---

{{< sesion n="3" h="1" tipo="t" >}}Control de flujo, funciones del gestor, cursores y funciones de usuario{{< /sesion >}}

## 5. Estructuras de control de flujo

El criterio RA5.g pide utilizar estructuras de control. PL/SQL tiene las tres familias habituales: **condicionales** (`IF`, `CASE`), **repetitivas** (`LOOP`, `WHILE`, `FOR`) y de **salto** (`EXIT`, `CONTINUE`, `GOTO`).

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
> **Una condición con `NULL` no es verdadera ni falsa: es desconocida** (*lógica trivaluada*, UD06), y `IF` solo ejecuta la rama `THEN` cuando la condición es **verdadera**. Con `v_nota` a `NULL`, `IF v_nota >= 5 THEN ... ELSE` ejecutaría el `ELSE` y marcaría como suspenso a quien no se ha presentado. Por eso en el ejemplo la primera pregunta es `IS NULL`. Y nunca se escribe `v_nota = NULL`: no es verdadera jamás.

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
| **`FOR` de cursor** | Recorrer las filas de una consulta (§7.3) | `FOR r IN (SELECT ...) LOOP ... END LOOP;` |

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
| `SELECT ... INTO` dentro de un bucle sobre filas | Una consulta por vuelta y `NO_DATA_FOUND` posible | Usa un cursor `FOR` (§7.3) |

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

## 6. Funciones proporcionadas por el sistema gestor

El criterio RA5.e pide hacer uso de las funciones del gestor. Ya las conoces de SQL (UD06); en PL/SQL son las mismas y se usan igual en las expresiones.

### 6.1 Catálogo de funciones útiles

{{< sgbd "Oracle 26ai" >}}

| Categoría | Función | Ejemplo | Resultado |
|---|---|---|---|
| **Texto** | `UPPER`, `LOWER` | `UPPER('Sala Brotons')` | `SALA BROTONS` |
| | `INITCAP` | `INITCAP('sala BROTONS')` | `Sala Brotons` |
| | `SUBSTR(t, inicio, n)` | `SUBSTR('10450740', 1, 4)` | `1045` |
| | `INSTR(t, buscado)` | `INSTR('mateosala20@alu.edugest.es', '@')` | `12` |
| | `LENGTH` | `LENGTH('Bases de datos')` | `14` |
| | `LPAD`, `RPAD` | `LPAD(7, 3, '0')` | `007` |
| | `TRIM` | `TRIM('  hola  ')` | `hola` |
| | `REPLACE` | `REPLACE('2025-26', '-', '/')` | `2025/26` |
| **Numéricas** | `ROUND(n, d)` | `ROUND(7.125, 2)` | `7.13` |
| | `TRUNC(n, d)` | `TRUNC(7.125, 1)` | `7.1` |
| | `MOD`, `CEIL`, `FLOOR`, `ABS` | `MOD(10, 3)`, `CEIL(4.2)` | `1`, `5` |
| **Fecha** | `SYSDATE` | `TRUNC(SYSDATE)` | Hoy a las 00:00 |
| | `ADD_MONTHS` | `ADD_MONTHS(DATE '2026-09-09', 9)` | `09/06/2027` |
| | `MONTHS_BETWEEN` | `MONTHS_BETWEEN(DATE '2027-06-09', DATE '2026-09-09')` | `9` |
| | `LAST_DAY` | `LAST_DAY(DATE '2027-02-10')` | `28/02/2027` |
| | `EXTRACT` | `EXTRACT(YEAR FROM DATE '2027-05-14')` | `2027` |
| **Conversión** | `TO_CHAR(fecha, formato)` | `TO_CHAR(DATE '2027-05-14', 'DD/MM/YYYY')` | `14/05/2027` |
| | `TO_DATE(texto, formato)` | `TO_DATE('14/05/2027', 'DD/MM/YYYY')` | `14/05/2027` |
| **Nulos** | `NVL(x, y)` | `NVL(NULL, 0)` | `0` |
| | `NVL2(x, si, no)` | `NVL2(nota, 'con nota', 'NC')` | `con nota` si `nota` no es nula |
| | `COALESCE(a, b, c...)` | `COALESCE(NULL, NULL, 5)` | `5` |
| | `NULLIF(a, b)` | `NULLIF(5, 5)` | `NULL` |

Un bloque que las combina sobre un alumno real:

```sql
DECLARE
    r_alu  alumno%ROWTYPE;
BEGIN
    SELECT * INTO r_alu FROM alumno WHERE id_alumno = 20;

    DBMS_OUTPUT.PUT_LINE('Ficha:     ' || UPPER(r_alu.apellidos) || ', ' || r_alu.nombre);
    DBMS_OUTPUT.PUT_LINE('Iniciales: ' || SUBSTR(r_alu.nombre, 1, 1) || SUBSTR(r_alu.apellidos, 1, 1));
    DBMS_OUTPUT.PUT_LINE('Nació:     ' ||
        TO_CHAR(r_alu.fecha_nacimiento, 'fmDD "de" month "de" YYYY', 'NLS_DATE_LANGUAGE=SPANISH'));
    DBMS_OUTPUT.PUT_LINE('Edad:      ' ||
        TRUNC(MONTHS_BETWEEN(DATE '2026-10-06', r_alu.fecha_nacimiento) / 12) || ' años');
    DBMS_OUTPUT.PUT_LINE('Dominio:   ' ||
        SUBSTR(r_alu.email, INSTR(r_alu.email, '@') + 1));
END;
/
```

```text
Ficha:     SALA BROTONS, Mateo
Iniciales: MS
Nació:     9 de abril de 2003
Edad:      23 años
Dominio:   alu.edugest.es
```

> [!TIP]
> Fíjate en que la edad se calcula con `MONTHS_BETWEEN(...) / 12` y `TRUNC`, no con `(fecha1 - fecha2) / 365`. Restar fechas da días y los años bisiestos desajustan el resultado. Esa expresión es el núcleo de la función `fn_edad` (§8.3).

### 6.2 Qué funciones son de Oracle y cuáles estándar

No todas las funciones existen en otros gestores. Si el código debe ser portable, conviene saberlo:

| Necesidad | Función de Oracle | Equivalente estándar o portable |
|---|---|---|
| Sustituir un nulo | `NVL(x, y)` (Oracle) | `COALESCE(x, y)` (estándar SQL) |
| Condicional | `DECODE(x, a, r1, r2)` (Oracle) | `CASE WHEN ... END` (estándar) |
| Fecha y hora actuales | `SYSDATE` (Oracle) | `CURRENT_DATE`, `CURRENT_TIMESTAMP` (estándar) |
| Subcadena | `SUBSTR`, `INSTR` (Oracle, también en MySQL) | `SUBSTRING`, `POSITION` (estándar) |
| Convertir a texto con formato | `TO_CHAR(f, 'DD/MM/YYYY')` (Oracle y PostgreSQL) | `CAST` + formato propio de cada gestor |
| Concatenar | `\|\|` (estándar; MySQL usa `CONCAT`) | `CONCAT` |

> [!NOTE]
> Las funciones de **agregado** (`SUM`, `AVG`, `COUNT`...), las **analíticas** y `DECODE` solo pueden usarse dentro de una sentencia SQL; no en una instrucción procedimental. Para obtener un total, hay que escribirlo en un `SELECT ... INTO`; para decidir, usa `CASE`.

### 6.3 Funciones propias de PL/SQL

Además de las de SQL, PL/SQL ofrece funciones y atributos que solo existen en el lenguaje procedimental:

| Elemento | Qué hace | Apartado |
|---|---|---|
| `SQLCODE`, `SQLERRM` | Código y texto del error que se está tratando | §9.3 |
| `SQL%ROWCOUNT`, `SQL%FOUND`, `SQL%NOTFOUND` | Resultado de la última sentencia DML | §7.1 |
| `c%FOUND`, `c%NOTFOUND`, `c%ROWCOUNT`, `c%ISOPEN` | Estado de un cursor explícito | §7.2 |
| `COUNT`, `FIRST`, `LAST`, `NEXT`, `EXISTS`... | Métodos de las colecciones | §11.6 |
| `DBMS_OUTPUT`, `DBMS_SCHEDULER`, `DBMS_UTILITY`... | Paquetes que Oracle suministra | §2.4, §12 |

---

## 7. Cursores

### 7.1 Qué es un cursor y cuál es el implícito

Cuando Oracle ejecuta una sentencia SQL reserva una zona de memoria privada (el **área de contexto**) con la sentencia analizada y las filas del resultado. Un **cursor** es el puntero a esa zona. `SELECT ... INTO` solo puede traer **una fila**; para recorrer un resultado de varias filas hace falta un cursor.

| Tipo | Quién lo gestiona | Se usa para |
|---|---|---|
| **Implícito** | Oracle, automáticamente, para cada sentencia SQL del bloque | Conocer el resultado de la última sentencia DML (`SQL%ROWCOUNT`) |
| **Explícito** | El programador: `CURSOR`, `OPEN`, `FETCH`, `CLOSE` | Recorrer consultas de varias filas con control total |
| **Cursor `FOR`** | El programador declara la consulta; Oracle abre, lee y cierra | La forma habitual de recorrer filas |
| **`REF CURSOR`** | El programador; la consulta se decide en ejecución | Devolver un resultado a una aplicación (JDBC, Python...) |

Tras cada `INSERT`, `UPDATE`, `DELETE` o `MERGE`, el cursor implícito `SQL` informa de lo que ha pasado:

| Atributo | Significado |
|---|---|
| `SQL%ROWCOUNT` | Número de filas afectadas por la última sentencia |
| `SQL%FOUND` | `TRUE` si la sentencia afectó al menos a una fila |
| `SQL%NOTFOUND` | `TRUE` si no afectó a ninguna |
| `SQL%ISOPEN` | Siempre `FALSE`: Oracle ya lo ha cerrado |

```sql
BEGIN
    UPDATE falta_asistencia
    SET    justificada = 'S'
    WHERE  justificada = 'N' AND fecha < DATE '2025-11-01';

    DBMS_OUTPUT.PUT_LINE('Faltas justificadas: ' || SQL%ROWCOUNT);   -- hay que leerlo YA

    IF SQL%NOTFOUND THEN
        DBMS_OUTPUT.PUT_LINE('No había ninguna falta que justificar');
    END IF;
    ROLLBACK;                                                         -- es una prueba
END;
/
```

```text
Faltas justificadas: 7
```

> [!WARNING]
> `SQL%ROWCOUNT` se **sobrescribe con cada sentencia SQL** que se ejecute después, incluido un `SELECT INTO`. Léelo en la instrucción inmediatamente posterior al DML, o guárdalo en una variable. Y recuerda: un `UPDATE` que no encuentra filas **no lanza error** (`SQL%NOTFOUND` vale `TRUE`); solo `SELECT ... INTO` lanza `NO_DATA_FOUND`.

### 7.2 Cursores explícitos

Un cursor explícito sigue cuatro pasos:

| Paso | Instrucción | Qué ocurre |
|---|---|---|
| 1. Declarar | `CURSOR c_notas IS SELECT ...;` | Se da nombre a una consulta. **No se ejecuta** |
| 2. Abrir | `OPEN c_notas;` | Oracle ejecuta la consulta y deja el cursor **antes de la primera fila** |
| 3. Leer | `FETCH c_notas INTO variables;` | Copia la fila actual en las variables y avanza una fila |
| 4. Cerrar | `CLOSE c_notas;` | Libera los recursos |

```sql
DECLARE
    CURSOR c_notas IS
        SELECT mo.codigo, m.nota_final
        FROM   matricula m JOIN modulo mo ON mo.id_modulo = m.id_modulo
        WHERE  m.id_alumno = 20
        ORDER  BY mo.codigo;
    v_codigo  modulo.codigo%TYPE;
    v_nota    matricula.nota_final%TYPE;
    v_filas   PLS_INTEGER := 0;
BEGIN
    OPEN c_notas;
    LOOP
        FETCH c_notas INTO v_codigo, v_nota;
        EXIT WHEN c_notas%NOTFOUND;                  -- justo después del FETCH
        v_filas := v_filas + 1;
        DBMS_OUTPUT.PUT_LINE(v_codigo || '  ' || v_nota);
    END LOOP;
    CLOSE c_notas;
    DBMS_OUTPUT.PUT_LINE('Módulos leídos: ' || v_filas);
END;
/
```

```text
0612  6.5
0613  5.25
0614  7.5
0615  9.25
Módulos leídos: 4
```

Los atributos del cursor permiten saber en qué punto está:

| Atributo | Antes de `OPEN` | Tras `OPEN` | Tras un `FETCH` con fila | Tras un `FETCH` sin fila | Tras `CLOSE` |
|---|---|---|---|---|---|
| `%ISOPEN` | `FALSE` | `TRUE` | `TRUE` | `TRUE` | `FALSE` |
| `%FOUND` | `ORA-01001` | `NULL` | `TRUE` | `FALSE` | `ORA-01001` |
| `%NOTFOUND` | `ORA-01001` | `NULL` | `FALSE` | `TRUE` | `ORA-01001` |
| `%ROWCOUNT` | `ORA-01001` | `0` | n.º de filas leídas | n.º de filas leídas | `ORA-01001` |

> [!CAUTION]
> Dos errores clásicos: (1) poner el `EXIT WHEN c%NOTFOUND` **después** de usar las variables. El último `FETCH`, el que no encuentra fila, **no cambia las variables**, y la última fila se procesaría dos veces. (2) Olvidar el `CLOSE`: el cursor queda abierto hasta el final de la sesión y, en un bucle que lo abre una y otra vez, se alcanza el límite `OPEN_CURSORS` (`ORA-01000`).

### 7.3 Cursor `FOR`: la forma habitual

El bucle `FOR` de cursor **hace los cuatro pasos por ti**: abre el cursor, lee fila a fila, declara el registro y cierra el cursor al terminar, incluso si se sale por una excepción. Es más corto, más seguro y se debe preferir salvo que se necesite el control fino del cursor explícito.

```sql
BEGIN
    FOR r IN (SELECT g.cod_grupo, COUNT(a.id_alumno) AS alumnos
              FROM   grupo g
                     LEFT JOIN alumno a ON a.cod_grupo = g.cod_grupo
              GROUP  BY g.cod_grupo
              ORDER  BY g.cod_grupo) LOOP
        DBMS_OUTPUT.PUT_LINE(RPAD(r.cod_grupo, 7) || LPAD(r.alumnos, 2) || ' alumnos');
    END LOOP;
END;
/
```

```text
1ASIR   5 alumnos
1DAM    7 alumnos
1DAW    6 alumnos
2ASIR   0 alumnos
2DAM    6 alumnos
2DAW    5 alumnos
```

Compara con el apartado anterior: ya no hay `OPEN`, `FETCH`, `CLOSE`, ni variables que declarar, ni `EXIT WHEN`. El registro `r` tiene un campo por cada columna del `SELECT` (`r.cod_grupo`, `r.alumnos`) y **solo existe dentro del bucle**. Observa también que el `LEFT JOIN` conserva el grupo 2ASIR, que no tiene alumnado (UD07).

Si la consulta es larga o se reutiliza, puede declararse con nombre y usarse en el `FOR`:

```sql
DECLARE
    CURSOR c_grupos IS SELECT cod_grupo, turno FROM grupo ORDER BY cod_grupo;
BEGIN
    FOR r IN c_grupos LOOP
        DBMS_OUTPUT.PUT_LINE(r.cod_grupo || ' · ' || r.turno);
    END LOOP;
END;
/
```

### 7.4 Cursores con parámetros

Un cursor puede recibir parámetros para reutilizar la misma consulta con valores distintos. Los parámetros se declaran **sin longitud** y se pasan al abrir el cursor:

```sql
DECLARE
    CURSOR c_modulos (p_ciclo  modulo.cod_ciclo%TYPE,
                      p_curso  modulo.curso%TYPE) IS
        SELECT codigo, nombre, horas
        FROM   modulo
        WHERE  cod_ciclo = p_ciclo AND curso = p_curso
        ORDER  BY codigo;
    v_total  PLS_INTEGER := 0;
BEGIN
    DBMS_OUTPUT.PUT_LINE('Módulos de DAW · segundo curso');
    FOR r IN c_modulos('DAW', 2) LOOP
        DBMS_OUTPUT.PUT_LINE(r.codigo || '  ' || RPAD(r.nombre, 36) || LPAD(r.horas, 4) || ' h');
        v_total := v_total + r.horas;
    END LOOP;
    DBMS_OUTPUT.PUT_LINE('Total: ' || v_total || ' h');
END;
/
```

```text
Módulos de DAW · segundo curso
0612  Desarrollo web en entorno cliente     140 h
0613  Desarrollo web en entorno servidor    160 h
0614  Despliegue de aplicaciones web         80 h
0615  Diseño de interfaces web              120 h
Total: 500 h
```

Con un cursor explícito se escribiría `OPEN c_modulos('DAW', 2);`. Dentro de la consulta, el parámetro se usa como cualquier valor; el prefijo `p_` evita que se confunda con una columna.

### 7.5 `FOR UPDATE`, `WHERE CURRENT OF` y `REF CURSOR`

Cuando el recorrido va a **modificar** las filas que lee, se bloquean con `FOR UPDATE` (bloqueo pesimista, UD08 §8.5) y se actualiza la fila actual con `WHERE CURRENT OF`:

```sql
-- Ejemplo de sintaxis: sube 0,25 puntos a las notas del módulo 16 (con tope 10)
DECLARE
    CURSOR c_notas IS
        SELECT id_matricula, nota_final
        FROM   matricula
        WHERE  id_modulo = 16 AND nota_final IS NOT NULL
        FOR UPDATE OF nota_final;
BEGIN
    FOR r IN c_notas LOOP
        UPDATE matricula
        SET    nota_final = LEAST(r.nota_final + 0.25, 10)
        WHERE CURRENT OF c_notas;
    END LOOP;
    ROLLBACK;                                      -- es solo una demostración
END;
/
```

Un **`REF CURSOR`** (`SYS_REFCURSOR`) es un cursor cuya consulta se decide en ejecución y que se puede **devolver** a quien llama. Es el mecanismo para entregar un resultado a una aplicación:

```sql
CREATE OR REPLACE FUNCTION fn_alumnos_grupo (p_cod_grupo IN grupo.cod_grupo%TYPE)
RETURN SYS_REFCURSOR
IS
    c_res  SYS_REFCURSOR;
BEGIN
    OPEN c_res FOR
        SELECT nia, apellidos, nombre
        FROM   alumno
        WHERE  cod_grupo = p_cod_grupo
        ORDER  BY apellidos;
    RETURN c_res;                  -- quien llama es responsable de leerlo y cerrarlo
END fn_alumnos_grupo;
/
```

### 7.6 Laboratorio: depurar bloques paso a paso

El siguiente depurador reproduce, línea a línea, tres de los bloques de esta unidad sobre datos reales de EduGest. Muestra la **línea en ejecución**, el valor de cada **variable** (resaltada cuando cambia) y el contenido del **búfer de `DBMS_OUTPUT`**. Las trazas están precalculadas: es una simulación didáctica, no un intérprete de PL/SQL.

{{< plsql-trace >}}

**Experimento 1 · Una consulta, tres desenlaces.** Elige el bloque «`SELECT … INTO` y la sección `EXCEPTION`» y ejecútalo con sus tres entradas:

1. Con el NIA `10450740` avanza hasta el final. Comprueba que `INTO` copia los dos valores y que la sección `EXCEPTION` **no** llega a ejecutarse.
2. Con `10459999` (un NIA que no existe) observa a qué línea salta la ejecución cuando la consulta no devuelve filas, y qué valen entonces `v_nia` y `v_nombre`.
3. Con `104507%` la consulta coincide con tres alumnos. Fíjate en que Oracle no asigna **ni siquiera la primera fila**, y en que se salta el manejador de `NO_DATA_FOUND`.

{{% details title="Qué deberías haber observado" %}}
Sin filas se lanza `NO_DATA_FOUND`, la ejecución abandona el cuerpo del bloque y se salta al manejador; las dos variables siguen a `NULL` porque `INTO` no llegó a asignar nada. Con tres filas se lanza `TOO_MANY_ROWS` y tampoco se asigna nada. En ambos casos el bloque termina sin error **porque la excepción se trata**; si se quitara la sección `EXCEPTION`, el error llegaría al cliente (`ORA-01403` u `ORA-01422`) y el bloque habría fallado.
{{% /details %}}

**Experimento 2 · ¿Cuándo se entera el cursor de que no quedan filas?** Cambia al bloque «Cursor explícito: `OPEN`, `FETCH`, `CLOSE`» y avanza paso a paso hasta el quinto `FETCH`:

1. Después de `OPEN`, ¿cuánto valen `%ROWCOUNT` y `%NOTFOUND`? ¿Se ha leído ya alguna fila?
2. En el quinto `FETCH`, observa qué le pasa a `%NOTFOUND`, a `%ROWCOUNT` y a `v_codigo`/`v_nota`.
3. Cambia ahora al bloque 1 («Bucle `FOR`») y compáralo: ¿qué instrucciones del cursor explícito han desaparecido y quién las hace?

{{% details title="Qué deberías haber observado" %}}
Tras `OPEN`, `%ROWCOUNT` es 0 y `%NOTFOUND` es `NULL`: el cursor está antes de la primera fila y no ha leído nada. El quinto `FETCH` no encuentra fila: `%NOTFOUND` pasa a `TRUE`, `%ROWCOUNT` se queda en 4 y las variables **conservan** los valores de la última fila (0615 y 9,25). Si el `EXIT WHEN` estuviera después del `PUT_LINE`, esa última fila se escribiría dos veces. En el bloque `FOR` desaparecen `OPEN`, `FETCH`, `CLOSE` y la declaración de variables: las hace el propio bucle.
{{% /details %}}

### 7.7 Cuándo no usar un cursor

Un cursor procesa **fila a fila**, y cada vuelta cuesta un cambio de contexto entre el motor PL/SQL y el motor SQL. Si la tarea se puede escribir como una sola sentencia, el motor SQL la hace en conjunto y mucho más rápido:

```sql
-- Lento y largo: una sentencia UPDATE por cada fila
BEGIN
    FOR r IN (SELECT id_falta FROM falta_asistencia
              WHERE justificada = 'N' AND fecha < DATE '2025-11-01') LOOP
        UPDATE falta_asistencia SET justificada = 'S' WHERE id_falta = r.id_falta;
    END LOOP;
END;
/

-- Mejor: una sola sentencia SQL que hace lo mismo
UPDATE falta_asistencia
SET    justificada = 'S'
WHERE  justificada = 'N' AND fecha < DATE '2025-11-01';
```

> [!TIP]
> Un cursor es la herramienta adecuada cuando, **para cada fila, hay que hacer algo que SQL no puede hacer en conjunto**: escribir un informe, llamar a un procedimiento, aplicar una lógica con varias decisiones, tratar cada fila con su propio control de errores. Cuando de verdad hay que procesar muchas filas con PL/SQL, `BULK COLLECT` lee un lote de golpe en una colección y `FORALL` envía todas sus modificaciones al motor SQL en una sola llamada; son optimizaciones que conviene conocer, no un punto de partida.

{{< quiz >}}
- q: "Al leer un cursor explícito en un bucle, el `EXIT WHEN c%NOTFOUND;` se escribe…"
  options: ["Antes del `FETCH`", "Inmediatamente después del `FETCH`, antes de usar las variables", "Después de usar las variables", "Dentro de la sección `EXCEPTION`"]
  answer: 1
  explain: "El `FETCH` que no encuentra fila no cambia las variables. Si se usan antes de comprobar `%NOTFOUND`, la última fila se procesa dos veces."
- q: "¿Qué diferencia hay entre un cursor explícito y un cursor `FOR`?"
  options: ["El cursor `FOR` no puede tener parámetros", "El cursor `FOR` abre, lee, declara el registro y cierra por sí mismo", "El cursor explícito no admite `ORDER BY`", "No hay ninguna: son sinónimos"]
  answer: 1
  explain: "El bucle `FOR` hace `OPEN`, `FETCH`, `CLOSE` y la declaración del registro automáticamente, incluso si el bucle termina por una excepción. Ambos admiten parámetros y cualquier consulta."
- q: "Tras `UPDATE matricula SET nota_final = 5 WHERE id_alumno = 999;` (no existe ese alumno), ¿qué ocurre?"
  options: ["`NO_DATA_FOUND`", "`TOO_MANY_ROWS`", "No hay error: `SQL%ROWCOUNT` vale 0 y `SQL%NOTFOUND` es `TRUE`", "`ORA-02291`"]
  answer: 2
  explain: "Un `UPDATE` o `DELETE` que no encuentra filas es una operación correcta que afecta a cero. Solo `SELECT ... INTO` lanza `NO_DATA_FOUND`."
- q: "Hay que subir un punto la nota de las 5 000 matrículas de un módulo. ¿Cuál es la mejor solución?"
  options: ["Un cursor `FOR` con un `UPDATE` por fila", "Un bucle `WHILE` con `SELECT INTO`", "Una única sentencia `UPDATE ... SET nota_final = nota_final + 1 WHERE ...`", "Un `REF CURSOR`"]
  answer: 2
  explain: "Si la tarea se puede expresar como una sola sentencia SQL, el motor SQL la ejecuta en conjunto, sin cambios de contexto por fila. El cursor se reserva para lo que SQL no puede hacer en conjunto."
{{< /quiz >}}

---

## 8. Funciones de usuario

### 8.1 Qué es una función y cuándo crearla

Una **función de usuario** es un subprograma almacenado en la base de datos que **recibe parámetros y devuelve un único valor**. El criterio RA5.f pide definirlas. Se crea una función cuando hay un cálculo que se repite y que se quiere escribir **una sola vez**: la calificación en texto de una nota, la edad a partir de una fecha, la media de un alumno.

Su gran ventaja sobre un procedimiento es que **se puede usar dentro de una consulta SQL**, como cualquier función del gestor:

```sql
SELECT nia, fn_edad(fecha_nacimiento) FROM alumno WHERE cod_grupo = '2DAW';
```

### 8.2 Sintaxis

```text
CREATE [OR REPLACE] FUNCTION nombre
    [(parámetro [IN] tipo [DEFAULT valor], ...)]
RETURN tipo_devuelto
[DETERMINISTIC]
IS | AS
    -- declaraciones locales
BEGIN
    ...
    RETURN valor;
[EXCEPTION
    ...]
END [nombre];
```

| Elemento | Significado |
|---|---|
| `CREATE OR REPLACE` | Crea la función o, si ya existe, la **sustituye conservando sus privilegios**. Es la forma de recompilar sin perder los `GRANT` |
| `parámetro [IN] tipo` | Parámetros de entrada. **Sin longitud** en el tipo: `VARCHAR2`, no `VARCHAR2(20)`. En una función se recomienda usar solo `IN` |
| `RETURN tipo` | Tipo del valor devuelto (en la cabecera, sin longitud) |
| `DETERMINISTIC` | Promete que con los mismos argumentos devuelve siempre el mismo valor; el optimizador puede reutilizar resultados. Solo si es cierto |
| `RETURN valor;` | Instrucción que devuelve el valor y **termina** la función. Debe ejecutarse en todos los caminos |
| `IS` / `AS` | Equivalentes: separan la cabecera de las declaraciones |

### 8.3 Dos funciones de EduGest: `fn_calificacion` y `fn_edad`

La primera convierte una nota en su calificación en texto. Es la regla que ya vimos en la vista `v_acta` (UD07), ahora escrita **una sola vez**:

{{< sgbd "Oracle 26ai" >}}

```sql
CREATE OR REPLACE FUNCTION fn_calificacion (p_nota IN NUMBER)
RETURN VARCHAR2
DETERMINISTIC
IS
BEGIN
    RETURN CASE
               WHEN p_nota IS NULL THEN 'NC'
               WHEN p_nota < 5     THEN 'Insuficiente'
               WHEN p_nota < 6     THEN 'Suficiente'
               WHEN p_nota < 7     THEN 'Bien'
               WHEN p_nota < 9     THEN 'Notable'
               ELSE                     'Sobresaliente'
           END;
END fn_calificacion;
/
```

La segunda calcula los años cumplidos. Tiene un parámetro con valor por defecto: si no se indica la fecha de referencia, usa la de hoy.

```sql
CREATE OR REPLACE FUNCTION fn_edad (
    p_fecha_nacimiento  IN DATE,
    p_fecha_ref         IN DATE DEFAULT SYSDATE
) RETURN NUMBER
IS
BEGIN
    IF p_fecha_nacimiento IS NULL THEN
        RETURN NULL;
    END IF;
    RETURN TRUNC(MONTHS_BETWEEN(p_fecha_ref, p_fecha_nacimiento) / 12);
END fn_edad;
/
```

Si todo va bien, SQLcl responde `Function FN_CALIFICACION compiled`. Si hay errores de compilación, los muestra con `SHOW ERRORS` (§2.5).

### 8.4 Usar una función

Desde **SQL**, en el `SELECT`, el `WHERE` o el `ORDER BY`:

```sql
SELECT a.nia,
       fn_edad(a.fecha_nacimiento, DATE '2026-10-06')  AS edad,
       ROUND(AVG(m.nota_final), 2)                      AS media,
       fn_calificacion(ROUND(AVG(m.nota_final), 2))     AS calificacion
FROM   alumno a
       JOIN matricula m ON m.id_alumno = a.id_alumno
WHERE  a.cod_grupo = '2DAW'
GROUP  BY a.nia, a.fecha_nacimiento
ORDER  BY a.nia;
```

| NIA | EDAD | MEDIA | CALIFICACION |
|---|---|---|---|
| 10450740 | 23 | 7.13 | Notable |
| 10450777 | 21 | 5.44 | Suficiente |
| 10450814 | 22 | 5.56 | Suficiente |
| 10450851 | 26 | 5.42 | Suficiente |
| 10450888 | 21 | 6 | Bien |

*5 filas*

Desde **PL/SQL**, en una asignación o una expresión:

```sql
DECLARE
    v_nota  NUMBER := 9.25;
BEGIN
    DBMS_OUTPUT.PUT_LINE(v_nota || ' = ' || fn_calificacion(v_nota));
    DBMS_OUTPUT.PUT_LINE('Edad de Mateo en 2027: ' ||
                         fn_edad(DATE '2003-04-09', DATE '2027-04-09'));
END;
/
```

```text
9.25 = Sobresaliente
Edad de Mateo en 2027: 24
```

Los argumentos se pueden pasar por **posición** (en el orden de la declaración) o por **nombre** con `=>`, que permite saltarse los opcionales y mejora la legibilidad:

```sql
SELECT fn_edad(p_fecha_ref => DATE '2026-10-06',
               p_fecha_nacimiento => DATE '2003-04-09') AS edad
FROM   dual;
```

### 8.5 Una función con consulta: `fn_nombre_modulo`

Una función puede leer de las tablas. Esta devuelve el nombre de un módulo, o `NULL` si no existe, en lugar de propagar el error al llamador:

```sql
CREATE OR REPLACE FUNCTION fn_nombre_modulo (p_id_modulo IN modulo.id_modulo%TYPE)
RETURN modulo.nombre%TYPE
IS
    v_nombre  modulo.nombre%TYPE;
BEGIN
    SELECT nombre INTO v_nombre FROM modulo WHERE id_modulo = p_id_modulo;
    RETURN v_nombre;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN NULL;                       -- decisión de diseño: «no existe» no es un error
END fn_nombre_modulo;
/
```

```sql
SELECT fn_nombre_modulo(2) AS existe, fn_nombre_modulo(999) AS no_existe FROM dual;
```

| EXISTE | NO_EXISTE |
|---|---|
| Bases de datos | *(null)* |

*1 fila*

> [!NOTE]
> Decidir qué hace una función cuando no encuentra el dato es una **decisión de diseño** que debes documentar: devolver `NULL` (cómodo en una consulta) o lanzar un error (obliga al llamador a tratarlo). En la práctica 9.2, `fn_nombre_completo` devuelve `NULL`; en el procedimiento de matrícula (§10.5), un alumno inexistente es un error.

### 8.6 Restricciones de las funciones llamadas desde SQL

Una función que se ejecuta dentro de un `SELECT` está sujeta a reglas, porque Oracle debe poder evaluarla muchas veces y en el orden que más le convenga:

| Regla | Si se incumple |
|---|---|
| No puede hacer `INSERT`, `UPDATE` ni `DELETE` (en una consulta) | `ORA-14551: cannot perform a DML operation inside a query` |
| No puede hacer `COMMIT`, `ROLLBACK` ni cambiar la sesión | `ORA-14552: cannot perform a DDL, commit or rollback inside a query or DML` |
| No debería depender de datos que cambien durante la propia sentencia | Resultados impredecibles o `ORA-04091` si lee la tabla que se modifica |
| Cada llamada es un cambio de contexto entre el motor SQL y el motor PL/SQL | Una función llamada 500 000 veces en un `SELECT` puede ser lenta: si es posible, expresa el cálculo en SQL |

> [!TIP]
> Marca con `DETERMINISTIC` las funciones puras como `fn_calificacion`; así Oracle puede reutilizar el resultado para argumentos repetidos y, además, es requisito para usarlas en un índice basado en funciones.

### 8.7 Gestionar las funciones

```sql
-- ¿Qué funciones tengo y en qué estado están?
SELECT object_name, status FROM user_objects WHERE object_type = 'FUNCTION' ORDER BY object_name;

-- Ver el código fuente almacenado
SELECT text FROM user_source WHERE name = 'FN_EDAD' ORDER BY line;

-- Eliminarla
DROP FUNCTION fn_edad;
```

Si una función depende de una tabla y ésta cambia (por ejemplo, `ALTER TABLE`), Oracle la marca `INVALID` y la recompila sola en el siguiente uso; para forzarlo: `ALTER FUNCTION fn_edad COMPILE;`.


---

{{< sesion n="5" h="1" tipo="t" >}}Excepciones y procedimientos almacenados{{< /sesion >}}

## 9. Excepciones

### 9.1 Qué es una excepción

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

El criterio RA5.j pide utilizar excepciones. Existen tres clases:

| Clase | Quién la lanza | Ejemplo |
|---|---|---|
| **Predefinida** | Oracle, con nombre ya asignado | `NO_DATA_FOUND`, `ZERO_DIVIDE` |
| **Oracle sin nombre** | Oracle, con código `ORA-` pero sin nombre en el lenguaje | `ORA-02292` (borrar un padre con hijos) |
| **Definida por el usuario** | El programador, con `RAISE` o `RAISE_APPLICATION_ERROR` | «El alumno no tiene grupo» |

### 9.2 Excepciones predefinidas

| Excepción | Código | Se lanza cuando… |
|---|---|---|
| `NO_DATA_FOUND` | `ORA-01403` | Un `SELECT ... INTO` no devuelve filas |
| `TOO_MANY_ROWS` | `ORA-01422` | Un `SELECT ... INTO` devuelve más de una fila |
| `DUP_VAL_ON_INDEX` | `ORA-00001` | Se viola una clave primaria o una restricción `UNIQUE` |
| `ZERO_DIVIDE` | `ORA-01476` | División por cero |
| `INVALID_NUMBER` | `ORA-01722` | Conversión de texto a número imposible dentro de una sentencia SQL |
| `VALUE_ERROR` | `ORA-06502` | Error de conversión o de tamaño en una asignación PL/SQL (`VARCHAR2(3) := 'Sala'`) |
| `CURSOR_ALREADY_OPEN` | `ORA-06511` | Se abre un cursor que ya está abierto |
| `INVALID_CURSOR` | `ORA-01001` | Operación no permitida sobre un cursor (leer uno cerrado) |
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

### 9.3 `OTHERS`, `SQLCODE` y `SQLERRM`

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

### 9.4 Excepciones definidas por el usuario

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

Una excepción declarada así solo existe dentro de su bloque. Si no se trata, al llegar al cliente se muestra como `ORA-06510: PL/SQL: unhandled user-defined exception`, un mensaje que no ayuda a nadie: por eso, para errores que deben llegar a la aplicación, se prefiere `RAISE_APPLICATION_ERROR` (§9.6).

### 9.5 `PRAGMA EXCEPTION_INIT`: ponerle nombre a un error de Oracle

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
| `-54` | `ORA-00054`: recurso ocupado (`FOR UPDATE NOWAIT`, UD08) | `e_ocupado` |

### 9.6 `RAISE_APPLICATION_ERROR`: errores de negocio hacia el cliente

`RAISE_APPLICATION_ERROR(código, mensaje)` detiene el subprograma y devuelve al llamador un error con el **código** y el **mensaje** que tú decidas. Es la forma estándar de comunicar a una aplicación que se ha incumplido una regla de negocio.

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
| Desde un disparador | Aborta la sentencia DML que lo disparó (§11) |

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

### 9.7 Bloques anidados: limitar el alcance de un error

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

### 9.8 Excepciones y transacciones

Un error **no** hace `ROLLBACK` de la transacción. Lo que ocurre depende de si se trata o no:

| Situación | Qué pasa con los cambios |
|---|---|
| La excepción **no se trata** y llega al cliente | Oracle deshace los cambios de **la llamada que ha fallado** (atomicidad de sentencia, UD08). Lo hecho antes en la transacción permanece, sin confirmar |
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
> No dependas del comportamiento implícito. Un subprograma que hace varias modificaciones y trata sus propios errores debe decidir **explícitamente** qué se conserva y qué se deshace, y quien lo llama debe saberlo. En la práctica 9.8 el paquete de secretaría usa exactamente esta técnica.

---

## 10. Procedimientos almacenados

### 10.1 Qué es un procedimiento

Un **procedimiento almacenado** es un subprograma con nombre, guardado y compilado en la base de datos, que **realiza una acción** y no devuelve valor (la información de salida viaja por los parámetros `OUT`). Se invoca desde un cliente, desde otro subprograma o desde una tarea programada.

```text
CREATE [OR REPLACE] PROCEDURE nombre
    [(parámetro [IN | OUT | IN OUT] tipo [DEFAULT valor], ...)]
[AUTHID DEFINER | CURRENT_USER]
IS | AS
    -- declaraciones locales
BEGIN
    -- instrucciones
[EXCEPTION
    -- manejadores]
END [nombre];
```

La estructura es la del bloque anónimo, con la cabecera `CREATE PROCEDURE` en lugar de `DECLARE`: las declaraciones locales se escriben **entre `IS` y `BEGIN`**, sin la palabra `DECLARE`.

| Función | Procedimiento |
|---|---|
| Devuelve **un valor** con `RETURN` | No devuelve valor |
| Se puede usar **dentro de un `SELECT`** | Se invoca con `EXEC`, `CALL` o desde otro bloque |
| Calcula | **Hace**: inserta, modifica, valida, registra |
| Parámetros normalmente solo `IN` | Parámetros `IN`, `OUT` e `IN OUT` |

### 10.2 Parámetros `IN`, `OUT` e `IN OUT`

| Modo | Dirección | Dentro del procedimiento | Al llamar se pasa |
|---|---|---|---|
| `IN` (por defecto) | Entrada | Solo lectura | Un valor, una variable o una expresión |
| `OUT` | Salida | Empieza a `NULL`; se le asigna un valor | **Una variable** que recibirá el resultado |
| `IN OUT` | Entrada y salida | Se lee y se modifica | **Una variable** con valor inicial |

Un procedimiento que devuelve datos de un módulo mediante parámetros `OUT`:

```sql
CREATE OR REPLACE PROCEDURE pr_datos_modulo (
    p_id_modulo  IN  modulo.id_modulo%TYPE,
    p_codigo     OUT modulo.codigo%TYPE,
    p_nombre     OUT modulo.nombre%TYPE,
    p_horas      OUT modulo.horas%TYPE
)
IS
BEGIN
    SELECT codigo, nombre, horas
    INTO   p_codigo, p_nombre, p_horas
    FROM   modulo
    WHERE  id_modulo = p_id_modulo;
END pr_datos_modulo;
/
```

Para llamarlo hace falta una variable por cada parámetro `OUT`:

```sql
DECLARE
    v_codigo  modulo.codigo%TYPE;
    v_nombre  modulo.nombre%TYPE;
    v_horas   modulo.horas%TYPE;
BEGIN
    pr_datos_modulo(2, v_codigo, v_nombre, v_horas);               -- notación posicional
    DBMS_OUTPUT.PUT_LINE(v_codigo || ' ' || v_nombre || ': ' || v_horas || ' h');
END;
/
```

```text
0484 Bases de datos: 160 h
```

Un parámetro `IN OUT` entra con un valor y sale transformado:

```sql
CREATE OR REPLACE PROCEDURE pr_normalizar_nombre (p_texto IN OUT VARCHAR2)
IS
BEGIN
    p_texto := INITCAP(TRIM(p_texto));
END pr_normalizar_nombre;
/

DECLARE
    v_nombre  VARCHAR2(40) := '  mateo SALA  ';
BEGIN
    pr_normalizar_nombre(v_nombre);
    DBMS_OUTPUT.PUT_LINE('[' || v_nombre || ']');
END;
/
```

```text
[Mateo Sala]
```

**Notación posicional y nombrada.** Los argumentos se pueden pasar en el orden de la declaración o por nombre con `=>`; esta segunda es más legible y permite omitir los parámetros con `DEFAULT`:

```sql
pr_datos_modulo(2, v_codigo, v_nombre, v_horas);                                       -- posicional
pr_datos_modulo(p_id_modulo => 2, p_horas => v_horas, p_nombre => v_nombre, p_codigo => v_codigo);   -- nombrada
```

> [!WARNING]
> Tres errores habituales con los parámetros: (1) **darles el nombre de una columna** (`id_alumno`): dentro de un `WHERE id_alumno = id_alumno` ambos son la columna y la condición es siempre verdadera. Por eso el prefijo `p_`. (2) **Indicar longitud** en el tipo (`p_texto VARCHAR2(40)`): es un error de sintaxis; el parámetro toma la longitud del argumento. (3) Pasar un **literal** a un parámetro `OUT` (`PLS-00363`): necesita una variable.

### 10.3 Invocar un procedimiento

| Forma | Dónde | Ejemplo |
|---|---|---|
| Desde un bloque PL/SQL | Cualquier cliente | `BEGIN pr_matricular(1, 2, '2026-27'); END;` |
| `EXEC` / `EXECUTE` | SQLcl, SQL\*Plus, SQL Developer | `EXEC pr_matricular(1, 2, '2026-27')` (es una abreviatura del bloque anterior; sin `;` ni `/`) |
| `CALL` | Cualquier cliente SQL | `CALL pr_matricular(1, 2, '2026-27');` (los paréntesis son obligatorios, incluso sin parámetros) |
| Desde otro subprograma o un disparador | PL/SQL | `pr_matricular(...);` |
| Desde una tarea programada | `DBMS_SCHEDULER` | `job_type => 'STORED_PROCEDURE'` (§12) |

### 10.4 Procedimientos, transacciones y privilegios

**¿Quién confirma la transacción?** Un procedimiento que modifica datos **no debería hacer `COMMIT`**: quien lo llama puede estar encadenando varias operaciones que deben confirmarse juntas (UD08). La regla práctica:

| Tipo de subprograma | `COMMIT` |
|---|---|
| Operación de negocio **llamada desde la aplicación o desde otro subprograma** (`pr_matricular`) | **No**: lo decide el llamador |
| Tarea **desatendida** sin nadie por encima (un procedimiento que ejecuta una tarea programada) | Sí: nadie más lo hará |

**¿Con qué privilegios se ejecuta?** Por defecto un procedimiento se ejecuta con los privilegios de su **propietario** (`AUTHID DEFINER`), no con los de quien lo llama:

| | `AUTHID DEFINER` (por defecto) | `AUTHID CURRENT_USER` |
|---|---|---|
| Privilegios usados | Los del propietario | Los de quien ejecuta |
| Roles del que lo usa | No intervienen | Se aplican |
| Para qué sirve | Dar un **acceso controlado**: `EXECUTE` sobre el procedimiento sin dar acceso a las tablas | Utilidades genéricas que deben respetar los permisos de cada usuario |

Esta es la base de la seguridad del proyecto de la unidad: la secretaría puede matricular **solo a través de** `pr_matricular`, sin permiso `INSERT` sobre `MATRICULA`:

```sql
GRANT EXECUTE ON pr_matricular TO rol_secretaria;
```

> [!NOTE]
> En un procedimiento de derechos del propietario, los privilegios que necesita sobre las tablas deben estar concedidos **directamente** a su dueño; los recibidos a través de un rol no cuentan en tiempo de compilación (el síntoma es un `PLS-00201` o un `ORA-00942` sobre una tabla que sí «ves» desde SQL). Si el propietario es el mismo esquema que las tablas, como en `EDUGEST`, no hay problema.

### 10.5 Ejemplo completo: procedimiento de matrícula

`pr_matricular` implementa la regla R2 del catálogo de restricciones (UD03) y las reglas de convocatoria. Recibe el alumno, el módulo y el curso académico, valida y, si todo es correcto, inserta la matrícula calculando la convocatoria. Reúne todo lo visto: parámetros, `SELECT INTO`, bloques anidados, excepciones y `RAISE_APPLICATION_ERROR`.

{{< sgbd "Oracle 26ai" >}}

```sql
CREATE OR REPLACE PROCEDURE pr_matricular (
    p_id_alumno  IN alumno.id_alumno%TYPE,
    p_id_modulo  IN modulo.id_modulo%TYPE,
    p_curso      IN matricula.curso_academico%TYPE
)
IS
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
        WHERE  a.id_alumno = p_id_alumno;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RAISE_APPLICATION_ERROR(-20012, 'El alumno ' || p_id_alumno || ' no existe o no tiene grupo asignado');
    END;

    -- 2. El módulo existe
    BEGIN
        SELECT cod_ciclo INTO v_ciclo_modulo FROM modulo WHERE id_modulo = p_id_modulo;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RAISE_APPLICATION_ERROR(-20012, 'El módulo ' || p_id_modulo || ' no existe');
    END;

    -- 3. R2: el módulo es del ciclo del grupo del alumno
    IF v_ciclo_modulo <> v_ciclo_alumno THEN
        RAISE_APPLICATION_ERROR(-20010, 'El módulo ' || p_id_modulo || ' (' || v_ciclo_modulo || ') no es del ciclo del alumno ' || p_id_alumno || ' (' || v_ciclo_alumno || ')');
    END IF;

    -- 4. No está ya matriculado en ese curso académico
    SELECT COUNT(*)
    INTO   v_ya_matriculado
    FROM   matricula
    WHERE  id_alumno = p_id_alumno AND id_modulo = p_id_modulo AND curso_academico = p_curso;

    IF v_ya_matriculado > 0 THEN
        RAISE_APPLICATION_ERROR(-20013, 'El alumno ' || p_id_alumno || ' ya está matriculado del módulo ' || p_id_modulo || ' en ' || p_curso);
    END IF;

    -- 5. Convocatoria: una más que la última matrícula del módulo (máximo 4)
    SELECT NVL(MAX(convocatoria), 0) + 1
    INTO   v_convocatoria
    FROM   matricula
    WHERE  id_alumno = p_id_alumno AND id_modulo = p_id_modulo;

    IF v_convocatoria > c_max_convocatorias THEN
        RAISE_APPLICATION_ERROR(-20011, 'El alumno ' || p_id_alumno || ' ha agotado las ' || c_max_convocatorias || ' convocatorias del módulo ' || p_id_modulo);
    END IF;

    -- 6. Todo correcto: se inserta. No hay COMMIT: lo decide quien llama
    INSERT INTO matricula (id_alumno, id_modulo, curso_academico, convocatoria)
    VALUES (p_id_alumno, p_id_modulo, p_curso, v_convocatoria);
END pr_matricular;
/
```

Decisiones de diseño que conviene entender:

| Decisión | Motivo |
|---|---|
| Los dos primeros `SELECT INTO` van en **bloques anidados** | Convierten `NO_DATA_FOUND` en un error de negocio con código y mensaje propios (`-20012`), en lugar de dejar pasar un `ORA-01403` incomprensible |
| La convocatoria se calcula como `MAX(convocatoria) + 1` sobre **todas** las matrículas del alumno en ese módulo | Si nunca se ha matriculado, `MAX` devuelve `NULL`, `NVL(..., 0)` lo convierte en 0 y la convocatoria es 1 |
| `RAISE_APPLICATION_ERROR` en cada regla | Un código distinto por regla: la aplicación puede reaccionar sin analizar el texto |
| **No hay `COMMIT`** | La matrícula forma parte de una transacción mayor (matricular al alumno en todo el curso, UD08); la decide quien llama |
| El curso académico **no se valida** en el procedimiento | Lo hace la restricción `CK_MATRICULA_CURSO` de la tabla. Duplicar la validación crearía dos reglas que mantener |

**Pruebas.** Con el alumno 1 (grupo 1DAM, ciclo DAM), que ya cursó el módulo 2 en 2025-26 y lo suspendió (nota 4,75):

```sql
EXEC pr_matricular(1, 2, '2026-27')

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
EXEC pr_matricular(1, 2, '2026-27')      -- repetida
```

```text
ORA-20013: El alumno 1 ya está matriculado del módulo 2 en 2026-27
ORA-06512: at "EDUGEST.PR_MATRICULAR", line 45
ORA-06512: at line 1
```

```sql
EXEC pr_matricular(1, 12, '2026-27')     -- el módulo 12 es de DAW; el alumno 1 es de DAM
```

```text
ORA-20010: El módulo 12 (DAW) no es del ciclo del alumno 1 (DAM)
ORA-06512: at "EDUGEST.PR_MATRICULAR", line 35
ORA-06512: at line 1
```

Los números de línea de `ORA-06512` cuentan desde la línea `PROCEDURE pr_matricular` y te llevan al `RAISE_APPLICATION_ERROR` exacto (`SELECT text FROM user_source WHERE name = 'PR_MATRICULAR' ORDER BY line`). La batería completa de ocho pruebas está en la [práctica 9.3](/ud09-plsql/ud09-practicas#práctica-93--procedimiento-de-matrícula-con-excepciones). Cuando termines, `ROLLBACK;` devuelve la tabla a su estado original.

> [!TIP]
> Un procedimiento que valida siempre tiene la misma estructura: **comprobar → rechazar con un error claro → actuar**. Las comprobaciones van primero y de más barata a más cara; el `INSERT` va al final, cuando ya no puede fallar por una regla de negocio.

### 10.6 Gestionar los procedimientos

| Tarea | Sentencia |
|---|---|
| Listar los subprogramas y su estado | `SELECT object_name, object_type, status FROM user_objects WHERE object_type IN ('PROCEDURE','FUNCTION','PACKAGE','TRIGGER') ORDER BY 2, 1;` |
| Ver el código | `SELECT text FROM user_source WHERE name = 'PR_MATRICULAR' ORDER BY line;` |
| Ver los errores de compilación | `SHOW ERRORS` o `SELECT * FROM user_errors WHERE name = 'PR_MATRICULAR';` |
| Recompilar | `ALTER PROCEDURE pr_matricular COMPILE;` |
| De qué depende | `SELECT referenced_name, referenced_type FROM user_dependencies WHERE name = 'PR_MATRICULAR';` |
| Conceder su uso | `GRANT EXECUTE ON pr_matricular TO rol_secretaria;` |
| Borrar | `DROP PROCEDURE pr_matricular;` |

Un subprograma pasa a `INVALID` cuando cambia algo de lo que depende (una tabla, otra función). Oracle lo recompila automáticamente la siguiente vez que se usa, pero un cambio de estructura en producción debe seguirse de una **recompilación del esquema** y de una comprobación de que todo está `VALID`.

{{< quiz >}}
- q: "En un procedimiento, ¿qué debe pasarse como argumento a un parámetro `OUT`?"
  options: ["Un literal con el valor inicial", "Una variable que recibirá el resultado", "Una constante", "Nada: los `OUT` no se pasan"]
  answer: 1
  explain: "El parámetro `OUT` devuelve un valor al llamador, que necesita una variable donde recibirlo. Pasarle un literal da `PLS-00363`."
- q: "Un bloque tiene `WHEN OTHERS THEN NULL;` y el programa «funciona», pero faltan datos en la tabla. ¿Cuál es el problema?"
  options: ["`NULL` no es una instrucción válida", "El manejador traga cualquier error sin dejar rastro", "`OTHERS` solo se puede usar en funciones", "Falta un `COMMIT` en el manejador"]
  answer: 1
  explain: "Con `WHEN OTHERS THEN NULL` cualquier error desaparece en silencio. Un `OTHERS` solo es aceptable si registra el error y lo vuelve a lanzar con `RAISE;`."
- q: "`PRAGMA EXCEPTION_INIT(e_tiene_hijos, -2292);` sirve para…"
  options: ["Crear el error `ORA-02292`", "Dar nombre a un error de Oracle para poder tratarlo en un `WHEN`", "Evitar que se produzca el error", "Convertir el error en una advertencia"]
  answer: 1
  explain: "El pragma solo asocia un nombre del programa a un código de error de Oracle que no tiene nombre predefinido. No cambia cuándo ni por qué ocurre el error."
- q: "¿Qué códigos admite `RAISE_APPLICATION_ERROR`?"
  options: ["Cualquier código `ORA-`", "Solo de -20000 a -20999", "Solo positivos", "Solo los de la tabla `USER_ERRORS`"]
  answer: 1
  explain: "El rango de -20000 a -20999 está reservado por Oracle a las aplicaciones. Cualquier otro valor lanza `ORA-21000`."
- q: "El procedimiento `pr_matricular` no ejecuta `COMMIT`. ¿Por qué?"
  options: ["Porque Oracle no permite `COMMIT` en procedimientos", "Porque la matrícula forma parte de una transacción mayor y debe decidirlo quien llama", "Porque `INSERT` ya confirma automáticamente", "Porque lo hace el disparador de la tabla"]
  answer: 1
  explain: "Un `COMMIT` dentro de una operación de negocio impediría agrupar varias operaciones en una sola transacción. Oracle sí permite el `COMMIT` en un procedimiento; es una decisión de diseño."
{{< /quiz >}}


---

{{< sesion n="7" h="1" tipo="t" >}}Disparadores, tareas programadas y paquetes{{< /sesion >}}

{{% paso-a-paso titulo="Qué dispara un trigger y en qué orden" %}}
{{% etapa titulo="1. Llega la sentencia" %}}
Un usuario ejecuta `UPDATE empleado SET sueldo = sueldo * 1.05 WHERE id_dep = 10;` y afecta, por ejemplo, a 3 filas.
{{% /etapa %}}
{{% etapa titulo="2. BEFORE STATEMENT" %}}
Se ejecuta **una vez**, antes de tocar ninguna fila.
{{% /etapa %}}
{{% etapa titulo="3. BEFORE EACH ROW" %}}
Se ejecuta **por cada fila afectada**, justo antes de cambiarla. Aquí se puede modificar `:NEW`.
{{% /etapa %}}
{{% etapa titulo="4. Se modifica la fila" %}}
Oracle aplica el cambio a esa fila.
{{% /etapa %}}
{{% etapa titulo="5. AFTER EACH ROW" %}}
Se ejecuta por cada fila, justo después. Los pasos 3-5 se repiten para las 3 filas.
{{% /etapa %}}
{{% etapa titulo="6. AFTER STATEMENT" %}}
Se ejecuta **una vez** al final. Si algo falla en cualquier punto, se deshace toda la sentencia.
{{% /etapa %}}
{{% /paso-a-paso %}}

## 11. Disparadores (triggers)

### 11.1 Qué es un disparador y cómo se construye

Un **disparador** es un bloque PL/SQL guardado en la base de datos y asociado a un **evento**. Nadie lo llama: Oracle lo ejecuta automáticamente cuando ocurre el evento. Es la herramienta con la que se implementan las reglas de integridad que el modelo lógico no puede declarar (RA6.h), la auditoría y los valores calculados que deben aplicarse **siempre**, venga el cambio de donde venga (RA4.h).

```text
CREATE [OR REPLACE] TRIGGER nombre
{BEFORE | AFTER | INSTEAD OF}
{INSERT | UPDATE [OF columna, ...] | DELETE} [OR ...]
ON {tabla | vista}
[FOR EACH ROW]
[WHEN (condición)]
[DECLARE declaraciones]
BEGIN
    instrucciones
[EXCEPTION manejadores]
END;
```

Tres decisiones definen el comportamiento de un disparador:

| Decisión | Opciones | Efecto |
|---|---|---|
| **Momento** | `BEFORE` / `AFTER` / `INSTEAD OF` | Antes o después de que se aplique el cambio; o en lugar de él (solo vistas) |
| **Evento** | `INSERT`, `UPDATE [OF col]`, `DELETE` (combinables con `OR`) | Qué sentencia lo dispara. `UPDATE OF nota_final` solo si esa columna aparece en el `SET` |
| **Nivel** | De **sentencia** (por omisión) o de **fila** (`FOR EACH ROW`) | Una ejecución por sentencia o una por cada fila afectada |

Combinando momento y nivel resultan los cuatro puntos de disparo clásicos:

| Punto de disparo | Cuántas veces | Qué se puede hacer | Uso típico |
|---|---|---|---|
| `BEFORE STATEMENT` | 1 por sentencia | Comprobar condiciones generales | Rechazar cambios fuera de horario o sin permiso |
| `BEFORE EACH ROW` | 1 por fila, antes del cambio | **Leer y modificar `:NEW`** | Normalizar datos, rellenar valores, validar la fila |
| `AFTER EACH ROW` | 1 por fila, tras el cambio | Leer `:OLD` y `:NEW` | **Auditoría**, propagar cambios a otra tabla |
| `AFTER STATEMENT` | 1 por sentencia | Consultar el resultado completo de la sentencia | Comprobaciones sobre el conjunto de filas |

#### `:NEW`, `:OLD` y condiciones

En un disparador **de fila**, `:OLD` contiene los valores de la fila **antes** del cambio y `:NEW` los valores **después**:

| Evento | `:OLD.columna` | `:NEW.columna` |
|---|---|---|
| `INSERT` | `NULL` (no había fila) | Los valores que se insertan |
| `UPDATE` | Valores antes del cambio | Valores después del cambio |
| `DELETE` | Valores de la fila borrada | `NULL` (no queda fila) |

Reglas que conviene memorizar:

- Dentro del cuerpo se escriben **con dos puntos**: `:NEW.nota_final`. En la cláusula `WHEN` se escriben **sin ellos**: `WHEN (NEW.nota_final <> OLD.nota_final)`.
- **Solo un `BEFORE EACH ROW` puede asignar a `:NEW`**. Hacerlo en un `AFTER` produce `ORA-04084: cannot change NEW values for this trigger type`.
- Un disparador que atiende varios eventos distingue cuál ha sido con los predicados `INSERTING`, `UPDATING` (o `UPDATING('columna')`) y `DELETING`.
- `WHEN` evita ejecutar el cuerpo cuando no hace falta: es la forma más eficiente de filtrar.

Restricciones de un disparador:

| No puede… | Error | Motivo |
|---|---|---|
| Hacer `COMMIT` ni `ROLLBACK` | `ORA-04092: cannot COMMIT in a trigger` | Forma parte de la transacción de la sentencia que lo ha disparado |
| Ejecutar DDL | Confirma la transacción (y no se permite) | El DDL lleva `COMMIT` implícito |
| Consultar o modificar la tabla que está cambiando la sentencia (disparador de fila) | `ORA-04091: table is mutating` | Es el error de la **tabla mutante** (§11.6) |

> [!IMPORTANT]
> Un disparador pertenece a la transacción de la sentencia que lo dispara: si la sentencia falla o se hace `ROLLBACK`, **también se deshace lo que el disparador hizo**. Es lo que se quiere para la integridad; no lo es para un registro de intentos fallidos (§11.2, nota final).

### 11.2 Auditoría de cambios de nota

Los cambios de nota son el dato más sensible de EduGest. Un disparador `AFTER UPDATE` registra, para cada cambio, **quién** lo hizo, **cuándo**, y qué valor había **antes** y **después**. Primero, la tabla donde se guarda:

{{< sgbd "Oracle 26ai" >}}

```sql
CREATE TABLE auditoria_nota (
    id_auditoria   NUMBER(10) GENERATED BY DEFAULT ON NULL AS IDENTITY
                   CONSTRAINT pk_auditoria_nota PRIMARY KEY,
    id_matricula   NUMBER(8)     CONSTRAINT nn_auditoria_matricula NOT NULL,
    nota_anterior  NUMBER(4,2),
    nota_nueva     NUMBER(4,2),
    usuario        VARCHAR2(128) CONSTRAINT nn_auditoria_usuario NOT NULL,
    fecha_cambio   TIMESTAMP     DEFAULT SYSTIMESTAMP CONSTRAINT nn_auditoria_fecha NOT NULL
);
COMMENT ON TABLE auditoria_nota IS 'Histórico de cambios de MATRICULA.NOTA_FINAL (trg_auditoria_nota)';
```

> [!NOTE]
> La tabla de auditoría **no lleva clave ajena** a `MATRICULA`: el histórico debe sobrevivir a la fila auditada. Si se borrara una matrícula y la clave ajena lo impidiera (o lo arrastrara en cascada), la auditoría perdería su razón de ser.

Y el disparador:

```sql
CREATE OR REPLACE TRIGGER trg_auditoria_nota
AFTER UPDATE OF nota_final ON matricula
FOR EACH ROW
WHEN (NVL(NEW.nota_final, -1) <> NVL(OLD.nota_final, -1))
BEGIN
    INSERT INTO auditoria_nota (id_matricula, nota_anterior, nota_nueva, usuario)
    VALUES (:OLD.id_matricula, :OLD.nota_final, :NEW.nota_final, USER);
END trg_auditoria_nota;
/
```

| Parte | Por qué |
|---|---|
| `AFTER` | La auditoría se registra cuando el cambio ya se ha aceptado: si una restricción lo rechaza, no queda rastro de algo que no ocurrió |
| `UPDATE OF nota_final` | El disparador solo se evalúa cuando la sentencia toca esa columna |
| `FOR EACH ROW` | Hace falta `:OLD` y `:NEW`, que existen por fila |
| `WHEN (NVL(NEW.nota_final, -1) <> NVL(OLD.nota_final, -1))` | Solo se audita si la nota **realmente cambia**. `NVL` maneja los nulos: sin él, pasar de `NULL` a 6, o de 6 a `NULL`, daría un resultado desconocido y no se auditaría. El valor centinela `-1` es seguro porque una nota válida va de 0 a 10 |
| `USER` | Quién hizo el cambio |

**Prueba.** Con la matrícula `10002` (alumno 1, módulo 2, nota 4,75):

```sql
UPDATE matricula SET nota_final = 6    WHERE id_matricula = 10002;   -- cambia 4,75 → 6
UPDATE matricula SET nota_final = 6    WHERE id_matricula = 10002;   -- el valor no cambia
UPDATE matricula SET nota_final = NULL WHERE id_matricula = 10002;   -- 6 → NULL (se anula la nota)

SELECT id_matricula, nota_anterior, nota_nueva, usuario
FROM   auditoria_nota
ORDER  BY id_auditoria;
```

| ID_MATRICULA | NOTA_ANTERIOR | NOTA_NUEVA | USUARIO |
|---|---|---|---|
| 10002 | 4.75 | 6 | EDUGEST |
| 10002 | 6 | *(null)* | EDUGEST |

*2 filas*

Las tres sentencias han actualizado una fila, pero solo se han registrado **dos** cambios: la segunda no cambió el valor y el `WHEN` impidió que el cuerpo se ejecutara. Termina con `ROLLBACK;`: como el disparador pertenece a la transacción, la auditoría también se deshace y la tabla vuelve a su estado inicial.

> [!NOTE]
> Esa es justo la propiedad que se quiere para la integridad (si el cambio no se confirma, su auditoría tampoco), pero no para un **registro de intentos**: si se quiere dejar constancia de un intento aunque la transacción se deshaga, el registro debe hacerse en una **transacción autónoma** (`PRAGMA AUTONOMOUS_TRANSACTION`), que confirma por su cuenta. Es lo que se pide en la práctica 9.5 y en el proyecto.

### 11.3 R1: el jefe de un departamento pertenece a ese departamento

La regla R1 compara una fila de `DEPARTAMENTO` con una fila de `PROFESOR`: ninguna restricción declarativa puede hacerlo. Hay que vigilar **dos lados**: cuando se asigna el jefe (este disparador) y cuando un profesor jefe cambia de departamento (práctica 9.5).

```sql
CREATE OR REPLACE TRIGGER trg_jefe_departamento
BEFORE INSERT OR UPDATE OF id_jefe ON departamento
FOR EACH ROW
WHEN (NEW.id_jefe IS NOT NULL)
DECLARE
    v_dpto  profesor.id_departamento%TYPE;
BEGIN
    SELECT id_departamento INTO v_dpto FROM profesor WHERE id_profesor = :NEW.id_jefe;
    IF v_dpto <> :NEW.id_departamento THEN
        RAISE_APPLICATION_ERROR(-20020, 'El profesor ' || :NEW.id_jefe || ' pertenece al departamento ' || v_dpto || ', no al ' || :NEW.id_departamento);
    END IF;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        NULL;      -- profesor inexistente: ya lo rechazará la clave ajena
END;
/
```

Es un disparador `BEFORE` porque **rechaza** el cambio antes de aplicarlo. Consulta `PROFESOR`, no la tabla que se modifica (`DEPARTAMENTO`), así que no hay problema de tabla mutante. Pruebas:

```sql
UPDATE departamento SET id_jefe = 111 WHERE id_departamento = 1;   -- 111 es Laura Vicent, del dpto. 3
```

```text
ORA-20020: El profesor 111 pertenece al departamento 3, no al 1
ORA-06512: at "EDUGEST.TRG_JEFE_DEPARTAMENTO", line 10
ORA-04088: error during execution of trigger 'EDUGEST.TRG_JEFE_DEPARTAMENTO'
```

```sql
UPDATE departamento SET id_jefe = 102 WHERE id_departamento = 1;   -- 102 es Javier Pastor, del dpto. 1
-- 1 fila actualizada
```

Observa que el error tiene **tres líneas**: el mensaje propio (`ORA-20020`), el lugar del código donde ocurrió (`ORA-06512`, número de línea contado desde la línea `TRIGGER`) y el aviso genérico de que falló un disparador (`ORA-04088`). La causa es siempre la primera.

> [!TIP]
> Los datos de ejemplo del script 02 cumplen la regla: los jefes 101, 109, 111 y 112 pertenecen a sus departamentos (1, 2, 3 y 5). Por eso el disparador no impide recargar los datos.

### 11.4 Normalización de datos al guardar

Un `BEFORE ... FOR EACH ROW` puede **corregir** el dato antes de que se guarde. Es el sitio adecuado para que los nombres lleguen siempre con la misma forma, venga el `INSERT` de la aplicación o de una herramienta gráfica:

```sql
CREATE OR REPLACE TRIGGER trg_alumno_normaliza
BEFORE INSERT OR UPDATE OF nombre, apellidos, email ON alumno
FOR EACH ROW
BEGIN
    :NEW.nombre    := INITCAP(TRIM(:NEW.nombre));
    :NEW.apellidos := INITCAP(TRIM(:NEW.apellidos));
    :NEW.email     := LOWER(TRIM(:NEW.email));
END trg_alumno_normaliza;
/
```

```sql
INSERT INTO alumno (nia, nombre, apellidos, fecha_nacimiento, email)
VALUES ('10459999', '  marina ', 'lópez ortega', DATE '2007-01-01', ' Marina@Mail.COM ');

SELECT nombre, apellidos, email FROM alumno WHERE nia = '10459999';
```

| NOMBRE | APELLIDOS | EMAIL |
|---|---|---|
| Marina | López Ortega | marina@mail.com |

*1 fila*

Dos observaciones:

1. El disparador `BEFORE` se ejecuta **antes de comprobar** la restricción `UNIQUE` del correo. Así `Marina@Mail.COM` y `marina@mail.com` se detectan como duplicados: sin normalizar, la restricción los habría considerado distintos.
2. `INITCAP` no es perfecto: convierte `de la Cruz` en `De La Cruz`. Una normalización automática debe ser **conservadora** y documentada.

Termina con `ROLLBACK;` para no dejar el alumno de prueba.

### 11.5 Disparadores `INSTEAD OF`: vistas que se pueden modificar

Una vista construida con composiciones no siempre es actualizable. Un disparador `INSTEAD OF` se ejecuta **en lugar de** la sentencia DML sobre la vista, y decide qué hacer con las tablas reales. Es siempre de fila. Por ejemplo, una vista para que la secretaría matricule indicando el NIA y el código del módulo, en lugar de identificadores internos:

```sql
CREATE OR REPLACE VIEW v_matricula_nia AS
    SELECT a.nia, mo.codigo AS cod_modulo, mo.cod_ciclo,
           m.curso_academico, m.convocatoria, m.nota_final
    FROM   matricula m
           JOIN alumno a  ON a.id_alumno  = m.id_alumno
           JOIN modulo mo ON mo.id_modulo = m.id_modulo;

CREATE OR REPLACE TRIGGER trg_v_matricula_nia_ins
INSTEAD OF INSERT ON v_matricula_nia
FOR EACH ROW
DECLARE
    v_id_alumno  alumno.id_alumno%TYPE;
    v_id_modulo  modulo.id_modulo%TYPE;
BEGIN
    SELECT id_alumno INTO v_id_alumno FROM alumno WHERE nia = :NEW.nia;
    SELECT id_modulo INTO v_id_modulo FROM modulo
    WHERE  codigo = :NEW.cod_modulo AND cod_ciclo = :NEW.cod_ciclo;

    pr_matricular(v_id_alumno, v_id_modulo, :NEW.curso_academico);   -- reutiliza §10.5
END trg_v_matricula_nia_ins;
/
```

```sql
INSERT INTO v_matricula_nia (nia, cod_modulo, cod_ciclo, curso_academico)
VALUES ('10450037', '0484', 'DAM', '2026-27');
-- 1 fila creada (internamente: pr_matricular(1, 2, '2026-27'))
```

El `INSERT` sobre la vista no toca la vista (no almacena nada): activa el disparador, que traduce el NIA y el código a identificadores y delega en el procedimiento, **con todas sus validaciones**. Pruébalo y haz `ROLLBACK`.

### 11.6 La tabla mutante (`ORA-04091`) y el disparador compuesto

La regla R5 dice que un grupo no puede tener más de 30 alumnos. Es un **recuento sobre varias filas**: no se puede declarar. La idea obvia es un disparador `AFTER ... FOR EACH ROW` que cuente los alumnos del grupo:

```sql
CREATE OR REPLACE TRIGGER trg_grupo_max_fila               -- ¡INCORRECTO! Solo para ver el error
AFTER INSERT OR UPDATE OF cod_grupo ON alumno
FOR EACH ROW
DECLARE
    v_n  PLS_INTEGER;
BEGIN
    SELECT COUNT(*) INTO v_n FROM alumno WHERE cod_grupo = :NEW.cod_grupo;
    IF v_n > 30 THEN
        RAISE_APPLICATION_ERROR(-20040, 'El grupo ' || :NEW.cod_grupo || ' supera los 30 alumnos');
    END IF;
END;
/
```

Compila sin problemas. Falla al ejecutarse:

```sql
UPDATE alumno SET cod_grupo = '2ASIR' WHERE id_alumno = 30;
```

```text
ORA-04091: table EDUGEST.ALUMNO is mutating, trigger/function may not see it
ORA-06512: at "EDUGEST.TRG_GRUPO_MAX_FILA", line 7
ORA-04088: error during execution of trigger 'EDUGEST.TRG_GRUPO_MAX_FILA'
```

**Por qué.** Mientras una sentencia modifica una tabla, ésta se halla en un estado intermedio: unas filas ya han cambiado y otras no. Un disparador de fila que la consultase obtendría un resultado que **depende del orden** en que Oracle procese las filas. Para impedirlo, Oracle prohíbe que un disparador de fila (o una función llamada desde él) lea o modifique la tabla que se está modificando: es el error de la **tabla mutante**.

> [!NOTE]
> Hay excepciones puntuales a la restricción (por ejemplo, algunos `INSERT ... VALUES` de una sola fila), pero no deben utilizarse: el diseño correcto no depende de ellas. Los disparadores de **sentencia** no tienen esta restricción, porque se ejecutan antes o después de que la tabla cambie.

**La solución: el disparador compuesto.** Un disparador `COMPOUND` agrupa en un solo objeto las secciones de varios puntos de disparo (`BEFORE STATEMENT`, `BEFORE EACH ROW`, `AFTER EACH ROW`, `AFTER STATEMENT`) que **comparten las mismas variables mientras dura la sentencia**. La técnica tiene dos pasos:

1. En `AFTER EACH ROW` **no se consulta** la tabla: solo se *anota* en una colección qué grupos ha tocado la sentencia.
2. En `AFTER STATEMENT`, cuando la sentencia ya ha terminado y la tabla **deja de estar mutando**, se recorre la colección y se hace el recuento.

{{< sgbd "Oracle 26ai" >}}

```sql
CREATE OR REPLACE TRIGGER trg_grupo_max_alumnos
FOR INSERT OR UPDATE OF cod_grupo ON alumno
COMPOUND TRIGGER

    c_max  CONSTANT PLS_INTEGER := 30;                       -- R5: máximo de alumnos por grupo

    TYPE t_grupos IS TABLE OF PLS_INTEGER INDEX BY VARCHAR2(10);
    g_grupos  t_grupos;                                      -- grupos tocados por la sentencia
    v_grupo   grupo.cod_grupo%TYPE;
    v_n       PLS_INTEGER;

    AFTER EACH ROW IS
    BEGIN
        IF :NEW.cod_grupo IS NOT NULL THEN
            g_grupos(:NEW.cod_grupo) := 1;                   -- solo anotar: NO consultar ALUMNO
        END IF;
    END AFTER EACH ROW;

    AFTER STATEMENT IS
    BEGIN
        v_grupo := g_grupos.FIRST;
        WHILE v_grupo IS NOT NULL LOOP
            SELECT COUNT(*) INTO v_n FROM alumno WHERE cod_grupo = v_grupo;
            IF v_n > c_max THEN
                RAISE_APPLICATION_ERROR(-20040, 'El grupo ' || v_grupo || ' superaría los ' || c_max || ' alumnos (tendría ' || v_n || ')');
            END IF;
            v_grupo := g_grupos.NEXT(v_grupo);
        END LOOP;
    END AFTER STATEMENT;

END trg_grupo_max_alumnos;
/
```

| Elemento | Qué hace |
|---|---|
| `FOR INSERT OR UPDATE OF cod_grupo ON alumno` | La cabecera de un compuesto usa `FOR` en lugar de `BEFORE`/`AFTER`, y **no** lleva `FOR EACH ROW` |
| Sección declarativa (antes de las secciones) | Variables y tipos **compartidos** por todas las secciones. Se inicializan al empezar cada sentencia y se descartan al terminar |
| `TYPE t_grupos ... INDEX BY VARCHAR2(10)` | Colección asociativa indexada por el código de grupo: guarda cada grupo una sola vez, aunque la sentencia toque varias filas |
| `AFTER EACH ROW IS ... END AFTER EACH ROW;` | Se ejecuta por fila; `:NEW` está disponible. Anota el grupo |
| `AFTER STATEMENT IS ... END AFTER STATEMENT;` | Se ejecuta una vez al final; ahora sí puede consultar `ALUMNO` |
| `FIRST` / `NEXT` | Recorren las claves de la colección asociativa |

**Pruebas.** Los alumnos 30, 31 y 32 no tienen grupo, y `2ASIR` está vacío. Con `c_max = 30` la regla se cumple:

```sql
UPDATE alumno SET cod_grupo = '2ASIR' WHERE cod_grupo IS NULL;
-- 3 filas actualizadas
ROLLBACK;
```

Para provocar el error sin crear 28 alumnos, recompila el disparador con `c_max CONSTANT PLS_INTEGER := 2;`:

```sql
UPDATE alumno SET cod_grupo = '2ASIR' WHERE cod_grupo IS NULL;
```

```text
ORA-20040: El grupo 2ASIR superaría los 2 alumnos (tendría 3)
ORA-06512: at "EDUGEST.TRG_GRUPO_MAX_ALUMNOS", line 25
ORA-04088: error during execution of trigger 'EDUGEST.TRG_GRUPO_MAX_ALUMNOS'
```

La sentencia completa se deshace: las tres filas siguen sin grupo. Observa que la regla se comprueba sobre el **resultado final**, no fila a fila, y que no aparece `ORA-04091`.

> [!WARNING]
> Este disparador comprueba la regla en la **sesión que modifica**, pero no ve los cambios sin confirmar de otras sesiones (consistencia de lectura, UD08). Dos secretarias que añadan a la vez un alumno a un grupo con 29 pueden confirmar ambas y dejar 31. La solución es **serializar** el acceso: bloquear la fila del grupo (`SELECT ... FROM grupo WHERE cod_grupo = ... FOR UPDATE`) antes de contar. Es el apartado 5 de la [práctica 9.6](/ud09-plsql/ud09-practicas#práctica-96--reto-la-tabla-mutante).

Otras formas de resolver una restricción que necesita leer su propia tabla:

| Solución | Cuándo | Observaciones |
|---|---|---|
| **Disparador compuesto** | La opción general desde Oracle 11g | La de esta unidad |
| Disparador de sentencia (`AFTER STATEMENT`) simple | No hace falta saber *qué filas* cambiaron | Vuelve a comprobar toda la tabla |
| Variable de paquete + tres disparadores | Antes de Oracle 11g | Obsoleto: es lo mismo que un compuesto, con más piezas |
| Un único procedimiento de acceso (y revocar el DML directo) | Todo cambio pasa por una API (`pkg_secretaria`) | La regla vive en el procedimiento, no en la tabla |
| Rediseñar | La regla es un contador | Columna con el número de alumnos mantenida por la API, o vista materializada con restricción |
| `PRAGMA AUTONOMOUS_TRANSACTION` | **Nunca para esto** | Quitaría el error, pero leería el estado confirmado y no el de la sentencia: la regla dejaría de ser fiable |

{{% details title="Prueba tú: un disparador de fila que calcula una media" %}}
**Enunciado.** Un compañero escribe un `AFTER UPDATE OF nota_final ON matricula FOR EACH ROW` que ejecuta `SELECT AVG(nota_final) FROM matricula WHERE id_modulo = :NEW.id_modulo`. ¿Qué error obtiene al ejecutar `UPDATE matricula SET nota_final = nota_final + 0.25 WHERE id_modulo = 16;`? ¿Cómo lo corregirías?

**Solución.** Obtiene `ORA-04091` (tabla `MATRICULA` mutando): el disparador de fila lee la tabla que la sentencia está modificando. Se corrige con un disparador compuesto: `AFTER EACH ROW` anota los `id_modulo` afectados en una colección y `AFTER STATEMENT` calcula la media de cada módulo anotado. Si lo que se quiere es solo mantener una tabla de resumen, es más sencillo calcularlo en una tarea programada (§12).
{{% /details %}}

### 11.7 Laboratorio: orden de disparo y tabla mutante

Este simulador reproduce un `UPDATE` de **tres filas** de `ALUMNO` (los alumnos 30, 31 y 32, que pasan al grupo 2ASIR) y muestra, paso a paso, **cuándo se ejecuta cada punto de disparo** y en qué momento la tabla está «mutando». Es una simulación didáctica: las trazas se generan con reglas fijas, no con un gestor real.

{{< trigger-lab >}}

**Experimento 1 · El orden de disparo.** Con el escenario 1, avanza hasta el final y contesta:

1. ¿Cuántas veces se ejecutan `BEFORE STATEMENT` y `AFTER STATEMENT`? ¿Y los disparadores de fila?
2. ¿Se ejecutan los tres `BEFORE EACH ROW` seguidos y después los tres `AFTER EACH ROW`, o se intercalan?
3. ¿En qué puntos de disparo aparece la tabla como «mutando»? ¿Dónde sería seguro consultar `ALUMNO`?

**Experimento 2 · Dos formas de comprobar la regla R5.** Ejecuta el escenario 2 (el disparador de fila que cuenta) y fíjate en qué le ocurre a la fila 30 cuando salta el error. Después ejecuta el escenario 3 con el límite de 30 alumnos y con el de 2: compara **cuándo** se hace la consulta `COUNT(*)` y **qué ve** en cada caso.

{{% details title="Qué deberías haber observado" %}}
`BEFORE STATEMENT` y `AFTER STATEMENT` se ejecutan **una vez**; los de fila, **tres** (una por fila). Los disparadores de fila **se intercalan por fila** (antes–cambio–después de la fila 30, luego de la 31...) y la tabla solo es segura de consultar en `BEFORE STATEMENT` y `AFTER STATEMENT`, los dos puntos que quedan fuera del recorrido de las filas.

En el escenario 2, la consulta del disparador de fila falla en cuanto se cambia la primera fila, y Oracle deshace la sentencia entera: la fila 30 vuelve a `NULL`. En el escenario 3 la consulta se mueve al `AFTER STATEMENT`, donde ya no hay tabla mutante, y devuelve 3. Con límite 30 la sentencia termina bien; con límite 2 el disparador lanza `ORA-20040` y se deshace igualmente toda la sentencia.
{{% /details %}}

### 11.8 Gestionar los disparadores y los disparadores de sistema

| Tarea | Sentencia |
|---|---|
| Listar los disparadores | `SELECT trigger_name, trigger_type, triggering_event, table_name, status FROM user_triggers ORDER BY table_name, trigger_name;` |
| Desactivar uno | `ALTER TRIGGER trg_auditoria_nota DISABLE;` |
| Activarlo | `ALTER TRIGGER trg_auditoria_nota ENABLE;` |
| Desactivar todos los de una tabla | `ALTER TABLE matricula DISABLE ALL TRIGGERS;` (y `ENABLE ALL TRIGGERS`) |
| Ver el código | `SELECT text FROM user_source WHERE name = 'TRG_AUDITORIA_NOTA' ORDER BY line;` |
| Borrarlo | `DROP TRIGGER trg_auditoria_nota;` |

> [!WARNING]
> Desactivar un disparador **apaga la regla** que implementa. Se hace en cargas masivas controladas (y se reactiva y se **comprueba** después), nunca «para que funcione». Un disparador desactivado en producción es una restricción de integridad que ya no existe.

Los disparadores no se limitan a las sentencias DML. Oracle admite disparadores de **sistema**, que responden a eventos de la base de datos o de la sesión (RA5.h: «eventos y disparadores»):

| Categoría | Evento (ejemplo) | Uso típico |
|---|---|---|
| **DML** | `BEFORE`/`AFTER INSERT OR UPDATE OR DELETE ON tabla` | Integridad, auditoría, valores calculados |
| **Vista** | `INSTEAD OF INSERT OR UPDATE OR DELETE ON vista` | Hacer actualizable una vista compleja |
| **DDL** | `AFTER CREATE OR ALTER OR DROP ON SCHEMA` | Registrar cambios de estructura (con `ORA_SYSEVENT`, `ORA_DICT_OBJ_NAME`) |
| **Sesión** | `AFTER LOGON ON SCHEMA` | Fijar parámetros de la sesión, registrar accesos |
| **Base de datos** | `STARTUP`, `SHUTDOWN`, `SERVERERROR` | Tareas de arranque, registrar los errores del servidor |

### 11.9 Cuándo NO usar un disparador

Un disparador es lógica **invisible**: no aparece en el código de la aplicación y se ejecuta sin que nadie lo llame. Úsalo cuando no haya una alternativa declarativa:

| Necesidad | Mejor que un disparador |
|---|---|
| Valor por defecto | `DEFAULT` en la columna |
| Valor de una sola fila dentro de un rango o lista | `CHECK` |
| Unicidad | `UNIQUE` |
| Integridad referencial | `FOREIGN KEY` |
| Clave autogenerada | Columna `IDENTITY` (en lugar de secuencia + disparador) |
| Operación de negocio completa que llama la aplicación | Procedimiento almacenado (como `pr_matricular`) |

> [!TIP]
> Diseña los disparadores **cortos y de un único propósito**: uno para la auditoría, otro para cada regla. Un disparador de 200 líneas que valida, audita, recalcula y avisa es imposible de probar. Documenta en un comentario qué restricción del catálogo implementa (R1, R3...), y ten una prueba para cada una.

{{< quiz >}}
- q: "En un disparador de fila `AFTER UPDATE ... FOR EACH ROW`, ¿cuál es el contenido de `:OLD.nota_final` y `:NEW.nota_final` al cambiar la nota de 4,75 a 6?"
  options: ["`:OLD` es 6 y `:NEW` es 4,75", "`:OLD` es 4,75 y `:NEW` es 6", "Ambos valen 6", "Ambos valen `NULL`"]
  answer: 1
  explain: "`:OLD` contiene la fila antes del cambio y `:NEW` la fila después. En un `INSERT` `:OLD` es nulo; en un `DELETE`, `:NEW` es nulo."
- q: "¿Por qué `trg_auditoria_nota` usa `NVL(NEW.nota_final, -1) <> NVL(OLD.nota_final, -1)` en lugar de `NEW.nota_final <> OLD.nota_final`?"
  options: ["Porque `<>` no existe en `WHEN`", "Porque si alguna nota es `NULL` la comparación es desconocida y el cambio no se auditaría", "Porque `NVL` es más rápido", "Porque `-1` es la nota mínima"]
  answer: 1
  explain: "Una comparación con `NULL` no es verdadera ni falsa. Sin `NVL`, pasar de `NULL` a 6 (o anular una nota) no dispararía el cuerpo y el cambio quedaría sin auditar."
- q: "Un `AFTER INSERT ... FOR EACH ROW` sobre `ALUMNO` ejecuta `SELECT COUNT(*) FROM alumno ...`. ¿Qué ocurre?"
  options: ["Funciona y cuenta todas las filas", "Oracle devuelve `ORA-04091` (tabla mutante)", "El disparador no compila", "Se ejecuta pero cuenta cero filas"]
  answer: 1
  explain: "Un disparador de fila no puede leer la tabla que está modificando la sentencia: el resultado dependería del orden de proceso de las filas. Compila bien y falla al ejecutarse."
- q: "En un disparador compuesto, ¿en qué sección es seguro consultar la tabla que se está modificando?"
  options: ["`BEFORE EACH ROW`", "`AFTER EACH ROW`", "`AFTER STATEMENT`", "En ninguna"]
  answer: 2
  explain: "En `AFTER STATEMENT` la sentencia ya ha terminado y la tabla deja de estar mutando. Por eso la técnica consiste en anotar en `AFTER EACH ROW` y comprobar en `AFTER STATEMENT`."
- q: "Un `INSTEAD OF INSERT` sobre una vista…"
  options: ["Se ejecuta después del `INSERT` en la vista", "Se ejecuta en lugar del `INSERT` y decide qué hacer con las tablas reales", "Solo puede crearse sobre tablas", "Es de sentencia, no de fila"]
  answer: 1
  explain: "`INSTEAD OF` solo existe sobre vistas, es siempre de fila y sustituye a la sentencia DML: el programador decide cómo se traduce a las tablas base."
{{< /quiz >}}


---


## 12. Eventos y tareas programadas {#12-eventos-tareas-programadas}

### 12.1 Disparador, procedimiento o tarea programada

Hay tres maneras de ejecutar código sin que una persona lo lance a mano. Se distinguen por **qué las pone en marcha**:

| | Qué lo pone en marcha | Ejemplo en EduGest |
|---|---|---|
| **Disparador** | Un **evento de datos**: una sentencia DML, una conexión, un `CREATE` | Auditar un cambio de nota |
| **Procedimiento** | Una **llamada explícita** de una persona o de una aplicación | Matricular a un alumno |
| **Tarea programada** (*job*) | El **reloj**: un calendario | Recalcular cada noche el resumen por grupo |

La tarea programada sirve para trabajo periódico y desatendido: resúmenes, limpiezas, cierres, avisos. En Oracle la ofrece el paquete **`DBMS_SCHEDULER`**; otros gestores la llaman *evento* (MySQL/MariaDB) o delegan en un agente externo (§12.5).

### 12.2 Un caso: la tabla de resumen por grupo

Consultar la media de un grupo recorre muchas filas. Si la secretaría necesita ese dato constantemente, conviene tenerlo ya calculado en una **tabla de resumen** (UD08 §5.3) que se refresque de madrugada.

{{< sgbd "Oracle 26ai" >}}

```sql
CREATE TABLE resumen_grupo (
    cod_grupo    VARCHAR2(10) CONSTRAINT pk_resumen_grupo PRIMARY KEY,
    alumnos      NUMBER(3)    CONSTRAINT nn_resumen_grupo_alumnos NOT NULL,
    matriculas   NUMBER(5)    CONSTRAINT nn_resumen_grupo_matr NOT NULL,
    nota_media   NUMBER(4,2),
    horas_falta  NUMBER(5)    DEFAULT 0 CONSTRAINT nn_resumen_grupo_faltas NOT NULL,
    calculado    TIMESTAMP    DEFAULT SYSTIMESTAMP CONSTRAINT nn_resumen_grupo_calc NOT NULL,
    CONSTRAINT fk_resumen_grupo FOREIGN KEY (cod_grupo) REFERENCES grupo (cod_grupo)
);
COMMENT ON COLUMN resumen_grupo.nota_media IS 'Media de las notas no nulas del grupo';
```

El procedimiento que la rellena usa `MERGE` (UD08 §5.4): inserta los grupos nuevos y actualiza los existentes. Cada dato se calcula con una subconsulta propia para que las composiciones de `MATRICULA` y `FALTA_ASISTENCIA` no dupliquen filas:

```sql
CREATE OR REPLACE PROCEDURE pr_recalcular_resumen
IS
BEGIN
    MERGE INTO resumen_grupo r
    USING (
        SELECT g.cod_grupo,
               (SELECT COUNT(*) FROM alumno a
                WHERE  a.cod_grupo = g.cod_grupo)                          AS alumnos,
               (SELECT COUNT(*) FROM matricula m
                       JOIN alumno a ON a.id_alumno = m.id_alumno
                WHERE  a.cod_grupo = g.cod_grupo)                          AS matriculas,
               (SELECT ROUND(AVG(m.nota_final), 2) FROM matricula m
                       JOIN alumno a ON a.id_alumno = m.id_alumno
                WHERE  a.cod_grupo = g.cod_grupo)                          AS nota_media,
               (SELECT NVL(SUM(f.horas), 0) FROM falta_asistencia f
                       JOIN matricula m ON m.id_matricula = f.id_matricula
                       JOIN alumno a    ON a.id_alumno    = m.id_alumno
                WHERE  a.cod_grupo = g.cod_grupo)                          AS horas_falta
        FROM   grupo g
    ) o
    ON (r.cod_grupo = o.cod_grupo)
    WHEN MATCHED THEN
        UPDATE SET r.alumnos     = o.alumnos,
                   r.matriculas  = o.matriculas,
                   r.nota_media  = o.nota_media,
                   r.horas_falta = o.horas_falta,
                   r.calculado   = SYSTIMESTAMP
    WHEN NOT MATCHED THEN
        INSERT (cod_grupo, alumnos, matriculas, nota_media, horas_falta)
        VALUES (o.cod_grupo, o.alumnos, o.matriculas, o.nota_media, o.horas_falta);

    COMMIT;          -- tarea desatendida: nadie más confirmará (ver §10.4)
END pr_recalcular_resumen;
/
```

```sql
EXEC pr_recalcular_resumen
SELECT cod_grupo, alumnos, matriculas, nota_media, horas_falta FROM resumen_grupo ORDER BY cod_grupo;
```

| COD_GRUPO | ALUMNOS | MATRICULAS | NOTA_MEDIA | HORAS_FALTA |
|---|---|---|---|---|
| 1ASIR | 5 | 25 | 7.07 | 11 |
| 1DAM | 7 | 35 | 6.4 | 18 |
| 1DAW | 6 | 30 | 6.19 | 14 |
| 2ASIR | 0 | 0 | *(null)* | 0 |
| 2DAM | 6 | 33 | 6.17 | 25 |
| 2DAW | 5 | 20 | 5.93 | 13 |

*6 filas*

Comprobación: las matrículas suman 143 y las horas de falta 81, las del total de la base de datos. El grupo `2ASIR` no tiene alumnado: su media es `NULL`, no 0.

### 12.3 `DBMS_SCHEDULER`: crear y gobernar tareas

`DBMS_SCHEDULER` separa lo que se ejecuta (la **acción**) de cuándo se ejecuta (el **calendario**). La unidad básica es el *job*:

| Concepto | Qué es |
|---|---|
| **Job** (tarea) | Una acción más un calendario: «ejecuta esto a esta hora» |
| **Acción** (`job_type`) | `STORED_PROCEDURE` (llama a un procedimiento), `PLSQL_BLOCK` (un bloque anónimo), `EXECUTABLE` (un programa del sistema) |
| **Calendario** (`repeat_interval`) | Una cadena de calendario, p. ej. `FREQ=DAILY; BYHOUR=2` |
| **Program** y **Schedule** | Acción y calendario con nombre, reutilizables por varios jobs |
| **Chain**, **Window** | Cadenas de tareas con dependencias; ventanas de recursos. No se estudian aquí |

{{< sgbd "Oracle 26ai" >}}

```sql
BEGIN
    DBMS_SCHEDULER.CREATE_JOB(
        job_name        => 'JOB_RESUMEN_NOCTURNO',
        job_type        => 'STORED_PROCEDURE',
        job_action      => 'PR_RECALCULAR_RESUMEN',
        start_date      => SYSTIMESTAMP AT TIME ZONE 'Europe/Madrid',
        repeat_interval => 'FREQ=DAILY; BYHOUR=2; BYMINUTE=0; BYSECOND=0',
        enabled         => TRUE,
        auto_drop       => FALSE,
        comments        => 'Recalcula RESUMEN_GRUPO cada noche a las 02:00');
END;
/
```

| Parámetro | Significado |
|---|---|
| `job_name` | Nombre del job. Se guarda en mayúsculas |
| `job_type`, `job_action` | Qué se ejecuta. Con `STORED_PROCEDURE`, el nombre del procedimiento |
| `start_date` | Desde cuándo vale el calendario. Con una zona horaria con nombre (`Europe/Madrid`) el job respeta el cambio de hora de verano |
| `repeat_interval` | El calendario (ver abajo). Si se omite, la tarea se ejecuta **una vez** |
| `enabled` | `TRUE` la activa al crearla. Con `FALSE` hay que activarla con `ENABLE` |
| `auto_drop` | `TRUE` borra el job cuando termina su última ejecución (útil para tareas de una sola vez) |

> [!NOTE]
> Para crear tareas hace falta el privilegio `CREATE JOB`. Si ves `ORA-27486: insufficient privileges`, quien administra la base de datos debe ejecutar `GRANT CREATE JOB TO edugest;`. Los jobs con `DBMS_SCHEDULER` sustituyen a `DBMS_JOB`, el mecanismo antiguo que aún aparece en documentación vieja.

**Cadenas de calendario.** Siguen un formato basado en el estándar iCalendar (RFC 5545): una frecuencia (`FREQ`) y restricciones (`BY...`).

| Cadena | Cuándo se ejecuta |
|---|---|
| `FREQ=MINUTELY; INTERVAL=1` | Cada minuto (para pruebas) |
| `FREQ=HOURLY; INTERVAL=4` | Cada 4 horas |
| `FREQ=DAILY; BYHOUR=2; BYMINUTE=0` | Todos los días a las 02:00 |
| `FREQ=WEEKLY; BYDAY=MON,TUE,WED,THU,FRI; BYHOUR=7; BYMINUTE=30` | De lunes a viernes a las 07:30 |
| `FREQ=MONTHLY; BYMONTHDAY=1; BYHOUR=6` | El día 1 de cada mes a las 06:00 |
| `FREQ=YEARLY; BYMONTH=9; BYMONTHDAY=1; BYHOUR=0` | El 1 de septiembre, a medianoche |

Oracle puede **calcular cuándo se ejecutaría** un calendario sin crear nada, con `EVALUATE_CALENDAR_STRING`. Es la forma de comprobar que la cadena dice lo que crees:

```sql
DECLARE
    v_proxima  TIMESTAMP WITH TIME ZONE;
BEGIN
    DBMS_SCHEDULER.EVALUATE_CALENDAR_STRING(
        calendar_string   => 'FREQ=WEEKLY; BYDAY=MON,TUE,WED,THU,FRI; BYHOUR=7; BYMINUTE=30',
        start_date        => NULL,
        return_date_after => TO_TIMESTAMP_TZ('14/05/2027 08:00 Europe/Madrid', 'DD/MM/YYYY HH24:MI TZR'),
        next_run_date     => v_proxima);
    DBMS_OUTPUT.PUT_LINE('Siguiente ejecución: ' || TO_CHAR(v_proxima, 'DD/MM/YYYY HH24:MI'));
END;
/
```

```text
Siguiente ejecución: 17/05/2027 07:30
```

El 14 de mayo de 2027 es viernes y ya han pasado las 07:30, así que la siguiente ejecución es el lunes 17.

**Gobernar las tareas:**

| Tarea | Sentencia |
|---|---|
| Ejecutar ahora, sin esperar | `EXEC DBMS_SCHEDULER.RUN_JOB('JOB_RESUMEN_NOCTURNO')` |
| Desactivar / activar | `EXEC DBMS_SCHEDULER.DISABLE('JOB_RESUMEN_NOCTURNO')` / `ENABLE` |
| Cambiar el calendario | `EXEC DBMS_SCHEDULER.SET_ATTRIBUTE('JOB_RESUMEN_NOCTURNO', 'repeat_interval', 'FREQ=WEEKLY; BYDAY=MON,TUE,WED,THU,FRI; BYHOUR=7; BYMINUTE=30')` |
| Borrar | `EXEC DBMS_SCHEDULER.DROP_JOB('JOB_RESUMEN_NOCTURNO')` |
| Ver las tareas y su próxima ejecución | `SELECT job_name, enabled, state, last_start_date, next_run_date FROM user_scheduler_jobs;` |
| Ver el historial de ejecuciones | `SELECT log_date, job_name, status, error#, additional_info FROM user_scheduler_job_run_details ORDER BY log_date DESC;` |

El historial es la herramienta de diagnóstico: cada ejecución queda registrada con su `STATUS` (`SUCCEEDED` o `FAILED`) y, si falla, el código de error (`ERROR#`) y su texto (`ADDITIONAL_INFO`).

> [!WARNING]
> Una tarea programada se ejecuta **sin nadie delante**: no hay pantalla donde leer un `DBMS_OUTPUT` ni a quién preguntar. Tres consecuencias: el procedimiento debe hacer su propio `COMMIT` (§10.4); debe **registrar su resultado** en una tabla de log; y hay que **mirar el historial** de vez en cuando, porque un job que falla cada noche no avisa a nadie. Y no olvides borrar las tareas de prueba (`DROP_JOB`): siguen ejecutándose en tu contenedor mientras exista.

### 12.4 Tareas basadas en eventos

Además de las tareas por calendario, `DBMS_SCHEDULER` admite tareas **basadas en eventos**: se ejecutan cuando otra parte del sistema envía un mensaje a una cola (por ejemplo, cuando llega un fichero o termina una carga). Son tareas con `event_condition` y `queue_spec` en lugar de `repeat_interval`. Quedan fuera del alcance de la unidad, pero conviene saber que el planificador de Oracle es, en realidad, un sistema de reacciones a eventos, y no solo un reloj.

### 12.5 Equivalentes en otros gestores

Aquí la portabilidad es casi nula: cada gestor resuelve las tareas programadas de forma distinta, y dos de ellos ni siquiera las traen de serie.

{{< sgbd "MySQL / MariaDB" >}}

Son **eventos** (`CREATE EVENT`), ejecutados por el *event scheduler*, que debe estar activado:

```sql
SET GLOBAL event_scheduler = ON;

CREATE EVENT ev_resumen_nocturno
ON SCHEDULE EVERY 1 DAY
STARTS (TIMESTAMP(CURRENT_DATE) + INTERVAL 1 DAY + INTERVAL 2 HOUR)
DO CALL pr_recalcular_resumen();
```

{{< sgbd "PostgreSQL" >}}

**No tiene planificador interno.** Las opciones son la extensión **`pg_cron`**, el agente **pgAgent** (de pgAdmin) o el `cron` del sistema operativo:

```sql
-- Requiere instalar la extensión pg_cron y cargarla (shared_preload_libraries)
CREATE EXTENSION pg_cron;
SELECT cron.schedule('resumen-nocturno', '0 2 * * *', 'CALL pr_recalcular_resumen()');
```

{{< sgbd "SQL Server" >}}

Se programan con **SQL Server Agent** (no disponible en la edición Express) mediante procedimientos de `msdb`:

```sql
EXEC msdb.dbo.sp_add_job         @job_name = N'resumen_nocturno';
EXEC msdb.dbo.sp_add_jobstep     @job_name = N'resumen_nocturno', @step_name = N'recalcular',
                                 @subsystem = N'TSQL', @command = N'EXEC dbo.pr_recalcular_resumen;',
                                 @database_name = N'edugest';
EXEC msdb.dbo.sp_add_jobschedule @job_name = N'resumen_nocturno', @name = N'diario_2am',
                                 @freq_type = 4, @freq_interval = 1, @active_start_time = 020000;
EXEC msdb.dbo.sp_add_jobserver   @job_name = N'resumen_nocturno';
```

| | Oracle | MySQL / MariaDB | PostgreSQL | SQL Server |
|---|---|---|---|---|
| **Mecanismo** | `DBMS_SCHEDULER` (integrado) | `EVENT` (integrado) | `pg_cron` / pgAgent / `cron` (externo) | SQL Server Agent (servicio aparte) |
| **Calendario** | Cadena `FREQ=...` | `EVERY n unidad` | Expresión `cron` | Parámetros `@freq_type`... |
| **Historial** | Vistas `*_SCHEDULER_JOB_RUN_DETAILS` | No guarda historial; hay que registrarlo | Tabla `cron.job_run_details` | `msdb.dbo.sysjobhistory` |
| **Activación** | Por defecto activo | `event_scheduler = ON` | Instalar y configurar la extensión | Servicio Agent en marcha |

---

## 13. Paquetes

### 13.1 Qué es un paquete

Un **paquete** agrupa subprogramas, constantes, variables y tipos relacionados bajo un mismo nombre. Es la unidad de organización de PL/SQL (RA5.d, RA5.f): en lugar de veinte procedimientos sueltos, un `pkg_secretaria` con las operaciones de la secretaría. Se compone de dos partes:

| Parte | Qué contiene | Quién la ve |
|---|---|---|
| **Especificación** (*package specification*) | La **interfaz pública**: cabeceras de los subprogramas y constantes visibles | Todo el que tenga `EXECUTE` sobre el paquete |
| **Cuerpo** (*package body*) | La **implementación** y los elementos privados | Solo el paquete |

Ventajas: un solo `GRANT EXECUTE`; se pueden ocultar los detalles (lo que no está en la especificación es privado); las variables del paquete mantienen su valor durante la sesión; y cambiar el cuerpo no invalida a quienes lo llaman, solo cambiar la especificación.

### 13.2 Ejemplo: `pkg_informes`

{{< sgbd "Oracle 26ai" >}}

```sql
CREATE OR REPLACE PACKAGE pkg_informes AS
    c_aprobado  CONSTANT NUMBER(3,1) := 5;                       -- constante pública

    FUNCTION  alumnos_grupo (p_cod_grupo IN grupo.cod_grupo%TYPE) RETURN PLS_INTEGER;
    PROCEDURE resumen_grupo (p_cod_grupo IN grupo.cod_grupo%TYPE);
END pkg_informes;
/

CREATE OR REPLACE PACKAGE BODY pkg_informes AS

    -- Privada: no aparece en la especificación, solo la ven los subprogramas del paquete
    FUNCTION media_grupo (p_cod_grupo IN grupo.cod_grupo%TYPE) RETURN NUMBER
    IS
        v_media  NUMBER;
    BEGIN
        SELECT ROUND(AVG(m.nota_final), 2)
        INTO   v_media
        FROM   matricula m JOIN alumno a ON a.id_alumno = m.id_alumno
        WHERE  a.cod_grupo = p_cod_grupo;
        RETURN v_media;
    END media_grupo;

    FUNCTION alumnos_grupo (p_cod_grupo IN grupo.cod_grupo%TYPE) RETURN PLS_INTEGER
    IS
        v_n  PLS_INTEGER;
    BEGIN
        SELECT COUNT(*) INTO v_n FROM alumno WHERE cod_grupo = p_cod_grupo;
        RETURN v_n;
    END alumnos_grupo;

    PROCEDURE resumen_grupo (p_cod_grupo IN grupo.cod_grupo%TYPE)
    IS
    BEGIN
        DBMS_OUTPUT.PUT_LINE('Grupo ' || p_cod_grupo || ': ' ||
                             alumnos_grupo(p_cod_grupo) || ' alumnos, media ' ||
                             NVL(TO_CHAR(media_grupo(p_cod_grupo)), 'sin notas'));
    END resumen_grupo;

END pkg_informes;
/
```

```sql
EXEC pkg_informes.resumen_grupo('2DAW')
EXEC pkg_informes.resumen_grupo('2ASIR')
SELECT pkg_informes.alumnos_grupo('1DAM') AS alumnos FROM dual;
```

```text
Grupo 2DAW: 5 alumnos, media 5.93
Grupo 2ASIR: 0 alumnos, media sin notas

   ALUMNOS
----------
         7
```

Se llama con `paquete.elemento`. `media_grupo` no es accesible desde fuera (`pkg_informes.media_grupo(...)` daría `PLS-00302`); `alumnos_grupo` es pública y se puede usar incluso en una consulta SQL.

| Regla | Detalle |
|---|---|
| Orden en el cuerpo | Un subprograma privado debe estar **declarado antes** de que otro lo use (por eso `media_grupo` va primero) |
| Cuerpo y especificación | Cada cabecera pública debe coincidir **exactamente** con su implementación |
| Estado | Una variable o constante del paquete conserva su valor mientras dure la **sesión** de cada usuario |
| `ORA-04068` | Si recompilas un paquete con estado mientras otras sesiones lo están usando, esas sesiones reciben «existing state of packages has been discarded»; basta con repetir la llamada |
| Sobrecarga | Dentro de un paquete puede haber varios subprogramas con el mismo nombre y distintos parámetros |

> [!TIP]
> El reto de la [práctica 9.8](/ud09-plsql/ud09-practicas#práctica-98--reto-el-paquete-de-secretaría) consiste en construir `pkg_secretaria` con `matricular`, `matricular_curso_completo`, `promocionar` y `media`. En el proyecto, ese paquete es la **única vía** de matrícula de la secretaría: tiene `EXECUTE` sobre él pero ningún `INSERT` sobre `MATRICULA`. Así las reglas del catálogo no se pueden saltar con una sentencia directa.

---

## 14. Comparación con otros gestores

PL/SQL es de Oracle. Si mañana trabajas con otro gestor, los **conceptos** son los mismos (variables, condiciones, bucles, cursores, excepciones, disparadores); lo que cambia es la sintaxis y algunas decisiones de diseño. La tabla marca lo que es **específico de cada gestor**:

| | Oracle | PostgreSQL | MySQL / MariaDB | SQL Server |
|---|---|---|---|---|
| **Lenguaje** | PL/SQL | PL/pgSQL (y otros: PL/Python...) | SQL/PSM (rutinas almacenadas) | Transact-SQL (T-SQL) |
| **Bloque anónimo** | `DECLARE ... BEGIN ... END;` | `DO $$ ... $$;` | MariaDB: `BEGIN NOT ATOMIC ... END`; MySQL: no existe, hay que crear una rutina | Un lote T-SQL, sin necesidad de bloque |
| **Variable** | `v_x NUMBER;` en `DECLARE` | `v_x numeric;` en `DECLARE` | `DECLARE v_x DECIMAL;` dentro de `BEGIN` | `DECLARE @x DECIMAL;` |
| **Asignación** | `v_x := 1;` | `v_x := 1;` | `SET v_x = 1;` | `SET @x = 1;` |
| **Condicional** | `IF ... ELSIF ... END IF;` | `IF ... ELSIF ... END IF;` | `IF ... ELSEIF ... END IF;` | `IF ... ELSE ...` (con `BEGIN/END`) |
| **Bucles** | `LOOP`, `WHILE`, `FOR` | `LOOP`, `WHILE`, `FOR` | `LOOP`, `WHILE`, `REPEAT` | Solo `WHILE` |
| **Parámetros** | `IN`, `OUT`, `IN OUT` | `IN`, `OUT`, `INOUT` | `IN`, `OUT`, `INOUT` | `@p tipo [OUTPUT]` |
| **Llamada** | `EXEC` / `CALL` | `CALL` | `CALL` | `EXEC` |
| **Cursores** | `CURSOR`, cursor `FOR` | `FOR r IN SELECT ... LOOP` o cursor explícito | Cursor explícito con `HANDLER ... NOT FOUND` | Cursor explícito con `@@FETCH_STATUS` |
| **Capturar errores** | `EXCEPTION WHEN ...` | `EXCEPTION WHEN ...` | `DECLARE HANDLER FOR ...` | `TRY ... CATCH` |
| **Error propio** | `RAISE_APPLICATION_ERROR(-20xxx, ...)` | `RAISE EXCEPTION '...'` | `SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = ...` | `THROW 50000, '...', 1` |
| **Disparadores** | Fila y sentencia; `BEFORE`/`AFTER`/`INSTEAD OF`; `:NEW`/`:OLD`; compuestos | Fila y sentencia; función de disparador aparte; `NEW`/`OLD` | Solo de fila; `BEFORE`/`AFTER`; `NEW.`/`OLD.`; sin `INSTEAD OF` | Solo de sentencia; `AFTER`/`INSTEAD OF`; tablas `inserted` y `deleted` |
| **Tabla mutante** | Sí (`ORA-04091`) | No existe como error | Sí (error 1442) | No (el disparador ve el lote completo) |
| **Paquetes** | Sí | No (esquemas y extensiones) | No | No (esquemas) |
| **Tareas programadas** | `DBMS_SCHEDULER` | `pg_cron` / `cron` | `CREATE EVENT` | SQL Server Agent |

### 14.1 La misma función en cuatro gestores

La función `fn_calificacion` de §8.3 escrita en cada uno. Fíjate en qué cambia: la cabecera, el modo de declarar el tipo devuelto y los separadores del bloque; la lógica (`CASE`) es idéntica.

{{< sgbd "PostgreSQL 17" >}}

```sql
CREATE OR REPLACE FUNCTION fn_calificacion(p_nota NUMERIC) RETURNS TEXT
LANGUAGE plpgsql IMMUTABLE
AS $$
BEGIN
    RETURN CASE
               WHEN p_nota IS NULL THEN 'NC'
               WHEN p_nota < 5     THEN 'Insuficiente'
               WHEN p_nota < 6     THEN 'Suficiente'
               WHEN p_nota < 7     THEN 'Bien'
               WHEN p_nota < 9     THEN 'Notable'
               ELSE                     'Sobresaliente'
           END;
END;
$$;
```

{{< sgbd "MySQL / MariaDB" >}}

```sql
DELIMITER //
CREATE FUNCTION fn_calificacion(p_nota DECIMAL(4,2)) RETURNS VARCHAR(15)
DETERMINISTIC
BEGIN
    RETURN CASE
               WHEN p_nota IS NULL THEN 'NC'
               WHEN p_nota < 5     THEN 'Insuficiente'
               WHEN p_nota < 6     THEN 'Suficiente'
               WHEN p_nota < 7     THEN 'Bien'
               WHEN p_nota < 9     THEN 'Notable'
               ELSE                     'Sobresaliente'
           END;
END //
DELIMITER ;
```

`DELIMITER` es una orden del cliente `mysql`: cambia temporalmente el terminador para que el `;` interior no cierre la rutina, el mismo problema que la `/` de Oracle.

{{< sgbd "SQL Server" >}}

```sql
CREATE OR ALTER FUNCTION dbo.fn_calificacion (@nota DECIMAL(4,2))
RETURNS VARCHAR(15)
AS
BEGIN
    RETURN CASE
               WHEN @nota IS NULL THEN 'NC'
               WHEN @nota < 5     THEN 'Insuficiente'
               WHEN @nota < 6     THEN 'Suficiente'
               WHEN @nota < 7     THEN 'Bien'
               WHEN @nota < 9     THEN 'Notable'
               ELSE                    'Sobresaliente'
           END;
END;
```

### 14.2 El mismo disparador de auditoría en tres gestores

El disparador `trg_auditoria_nota` (§11.2) en los otros tres gestores. La diferencia más visible está en cómo cada uno accede a los valores antes y después del cambio.

{{< sgbd "PostgreSQL 17" >}}

```sql
-- En PostgreSQL el disparador son DOS objetos: una función y el trigger que la invoca
CREATE OR REPLACE FUNCTION fn_trg_auditoria_nota() RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.nota_final IS DISTINCT FROM OLD.nota_final THEN
        INSERT INTO auditoria_nota (id_matricula, nota_anterior, nota_nueva, usuario)
        VALUES (OLD.id_matricula, OLD.nota_final, NEW.nota_final, current_user);
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_auditoria_nota
AFTER UPDATE OF nota_final ON matricula
FOR EACH ROW EXECUTE FUNCTION fn_trg_auditoria_nota();
```

{{< sgbd "MySQL / MariaDB" >}}

```sql
-- Sin "UPDATE OF columna" ni WHEN: la condición va dentro del cuerpo.
-- "<=>" es la igualdad que trata NULL como un valor más.
DELIMITER //
CREATE TRIGGER trg_auditoria_nota
AFTER UPDATE ON matricula
FOR EACH ROW
BEGIN
    IF NOT (NEW.nota_final <=> OLD.nota_final) THEN
        INSERT INTO auditoria_nota (id_matricula, nota_anterior, nota_nueva, usuario)
        VALUES (OLD.id_matricula, OLD.nota_final, NEW.nota_final, CURRENT_USER());
    END IF;
END //
DELIMITER ;
```

{{< sgbd "SQL Server" >}}

```sql
-- Dispara una vez por SENTENCIA: no hay :NEW/:OLD sino las tablas "inserted" y "deleted",
-- con todas las filas afectadas. Se trabaja en conjunto, no fila a fila.
CREATE OR ALTER TRIGGER trg_auditoria_nota
ON matricula
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    INSERT INTO auditoria_nota (id_matricula, nota_anterior, nota_nueva, usuario)
    SELECT d.id_matricula, d.nota_final, i.nota_final, SUSER_SNAME()
    FROM   deleted d
           JOIN inserted i ON i.id_matricula = d.id_matricula
    WHERE  ISNULL(i.nota_final, -1) <> ISNULL(d.nota_final, -1);
END;
```

> [!NOTE]
> El diseño de SQL Server es un cambio de mentalidad: no existe el disparador de fila, así que **el problema de la tabla mutante no se plantea**, pero hay que pensar siempre en conjuntos de filas. Y en MySQL/MariaDB, al no existir `INSTEAD OF` ni disparadores de sentencia, las reglas de varias filas (R4, R5) se implementan normalmente con procedimientos que controlan el acceso.

---

## 15. Errores frecuentes

| Síntoma | Causa | Solución |
|---|---|---|
| El bloque «funciona» pero no muestra nada | Falta `SET SERVEROUTPUT ON` o el panel de salida está cerrado | Actívalo en cada sesión (§2.4) |
| SQLcl se queda esperando tras escribir el bloque | Falta la `/` final | Escríbela en una línea sola (§2.3) |
| `PLS-00103: Encountered the symbol ...` | `;` olvidado, `END IF` o `END LOOP` sin cerrar, coma sobrante | Revisa la línea que indica y la anterior (§2.5) |
| `PLS-00428: an INTO clause is expected` | `SELECT` en un bloque sin `INTO` ni cursor | Añade `INTO` o usa un cursor `FOR` |
| `Warning: ... created with compilation errors` | El subprograma tiene errores `PLS-` | `SHOW ERRORS` o `USER_ERRORS` |
| `ORA-01403: no data found` | `SELECT ... INTO` sin filas | Trata `NO_DATA_FOUND` o usa un agregado (§9.2) |
| `ORA-01422: exact fetch returns more than requested number of rows` | `SELECT ... INTO` con varias filas | Concreta el `WHERE` o usa un cursor (§7) |
| La condición `WHERE id_alumno = id_alumno` devuelve todas las filas | Parámetro o variable con el mismo nombre que la columna | Prefijos `p_` y `v_` (§3.4) |
| Un `IF x > 5 ... ELSE` marca como suspenso a quien no tiene nota | La comparación con `NULL` es desconocida y cae en el `ELSE` | Pregunta primero `IS NULL` (§5.1) |
| El último registro del cursor sale duplicado | `EXIT WHEN c%NOTFOUND` colocado después de usar las variables | Justo después del `FETCH` (§7.2) |
| `ORA-01000: maximum open cursors exceeded` | Cursores explícitos sin `CLOSE` | Cierra siempre, o usa cursor `FOR` |
| `ORA-14551: cannot perform a DML operation inside a query` | Función con `INSERT`/`UPDATE` llamada desde un `SELECT` | Conviértela en procedimiento (§8.6) |
| `ORA-04091: table is mutating` | Disparador de fila que lee su propia tabla | Disparador compuesto (§11.6) |
| `ORA-04092: cannot COMMIT in a trigger` | `COMMIT` o `ROLLBACK` dentro de un disparador | Quítalo; el disparador va en la transacción de la sentencia |
| `ORA-04084: cannot change NEW values for this trigger type` | Asignar `:NEW` en un `AFTER` | Usa un `BEFORE` |
| `ORA-04088` + `ORA-20xxx` | El disparador ha rechazado la sentencia a propósito | La causa es el `ORA-20xxx`: lee su mensaje |
| `ORA-06510: unhandled user-defined exception` | `RAISE` de una excepción propia sin manejador | Trátala o usa `RAISE_APPLICATION_ERROR` |
| `ORA-27486: insufficient privileges` al crear un job | Falta el privilegio `CREATE JOB` | `GRANT CREATE JOB TO edugest;` por parte de administración |
| `ORA-04068: existing state of packages has been discarded` | Se recompiló un paquete con estado mientras se usaba | Repite la llamada |
| `WHEN OTHERS THEN NULL` y datos que no cuadran | Un error se ha tragado en silencio | Registra y relanza con `RAISE;` (§9.3) |
| Los cambios del procedimiento no aparecen en otra sesión | Falta el `COMMIT` (que, por diseño, el procedimiento no hace) | Confirma desde quien lo llama (§10.4) |

---

## 16. Buenas prácticas

- **Una sentencia SQL antes que un bucle.** Si la tarea cabe en un `UPDATE` o un `INSERT ... SELECT`, no la escribas con un cursor (§7.7).
- **Usa `%TYPE` y `%ROWTYPE`** en lugar de repetir los tipos de las columnas.
- **Prefijos en los nombres** (`v_`, `p_`, `c_`, `r_`, `e_`) para no confundir variables, parámetros y columnas.
- **Escribe siempre el `ELSE`** de un `CASE` y la rama `IS NULL` de las condiciones que manejen datos que puedan faltar.
- **Un cursor `FOR` antes que uno explícito**, salvo que necesites el control fino de `OPEN`/`FETCH`/`CLOSE`.
- **Una función calcula y no modifica datos; un procedimiento hace.** Las funciones que se llaman desde SQL deben ser puras.
- **Trata solo los errores que sabes tratar.** Nada de `WHEN OTHERS THEN NULL`: registra y vuelve a lanzar con `RAISE;`.
- **Define un catálogo de errores propios** (`-20010`...), con un código por regla y un mensaje que diga qué dato falló.
- **No hagas `COMMIT` en las operaciones de negocio** que otros llaman; sí en las tareas desatendidas.
- **Si tienes que deshacer una parte, usa `SAVEPOINT`** de forma explícita; no dependas de lo que ocurra de forma implícita.
- **Una regla, un disparador; cada disparador corto.** Comenta qué restricción del catálogo implementa y escribe una prueba para cada una.
- **Antes de un disparador, pregúntate si basta un `CHECK`, un `DEFAULT`, una clave ajena o un procedimiento** (§11.9).
- **Concede `EXECUTE` sobre el procedimiento en lugar de `INSERT` sobre la tabla** cuando la regla de negocio importe.
- **Una tarea programada registra su resultado** en una tabla y se revisa su historial. No olvides borrar las de prueba.
- **Cada objeto en su propio `.sql`**, con `CREATE OR REPLACE`, terminado en `/` y bajo control de versiones.
- **Marca en la documentación lo específico de Oracle** si el código tiene que portarse a otro gestor.

---

{{< tarjetas titulo="Repasa los términos de la UD09" >}}
- t: "Bloque anónimo"
  d: "Código PL/SQL sin nombre: DECLARE, BEGIN, EXCEPTION, END."
- t: "Procedimiento"
  d: "Subprograma almacenado con nombre que realiza una acción."
- t: "Función"
  d: "Subprograma almacenado que devuelve un valor y puede usarse en SQL."
- t: "Cursor"
  d: "Puntero que recorre las filas de una consulta una a una."
- t: "Excepción"
  d: "Error controlado en la sección EXCEPTION."
- t: "Trigger"
  d: "Código que se ejecuta automáticamente ante un evento DML, DDL o de sistema."
- t: "Paquete"
  d: "Agrupación de procedimientos, funciones y variables relacionados."
{{< /tarjetas >}}

## 17. Resumen

| Concepto | Idea clave | Sintaxis esencial |
|---|---|---|
| Formas de automatizar | Guion, bloque anónimo, función, procedimiento, paquete, disparador y tarea programada: se distinguen por **dónde viven** y **qué los ejecuta** | — |
| Ejecución de guiones | Las órdenes de cliente (`SET`, `SPOOL`, `@`) no las entiende el servidor; los bloques PL/SQL terminan en `;` y `/` | `@fichero.sql`, `SET SERVEROUTPUT ON` |
| Bloque | `DECLARE` (opcional), `BEGIN` ... `EXCEPTION` (opcional) ... `END;` | `DECLARE ... BEGIN ... END;` |
| Variables | Con tipo, heredables de la tabla con `%TYPE` y `%ROWTYPE`. Distintas de las variables de **sustitución** (`&`), que resuelve el cliente | `v_x tabla.col%TYPE;`, `SELECT ... INTO` |
| Control de flujo | `IF`/`ELSIF`, `CASE`, `LOOP`/`WHILE`/`FOR`; cuidado con `NULL` | `IF ... THEN ... END IF;` |
| Funciones del gestor | Las de SQL funcionan en PL/SQL (salvo agregadas, analíticas y `DECODE`); `NVL` y `SYSDATE` son de Oracle | `NVL`, `TO_CHAR`, `MONTHS_BETWEEN` |
| Cursores | Implícito (`SQL%ROWCOUNT`), explícito (`OPEN`/`FETCH`/`CLOSE`), `FOR`, con parámetros | `FOR r IN (SELECT ...) LOOP` |
| Funciones de usuario | Devuelven un valor y se usan en SQL; sin DML si se llaman desde una consulta | `CREATE OR REPLACE FUNCTION ... RETURN` |
| Procedimientos | Hacen algo; parámetros `IN`, `OUT`, `IN OUT`; `EXECUTE` en lugar de `INSERT` directo | `CREATE OR REPLACE PROCEDURE` |
| Excepciones | Predefinidas, propias, `PRAGMA EXCEPTION_INIT`; `RAISE_APPLICATION_ERROR` entre -20000 y -20999 | `EXCEPTION WHEN ... THEN` |
| Disparadores | Se ejecutan solos ante un evento; `:NEW`/`:OLD`; `BEFORE` modifica, `AFTER` audita; `INSTEAD OF` en vistas | `CREATE TRIGGER ... FOR EACH ROW` |
| Tabla mutante | Un disparador de fila no puede leer su tabla (`ORA-04091`); se resuelve anotando en `AFTER EACH ROW` y comprobando en `AFTER STATEMENT` | `COMPOUND TRIGGER` |
| Tareas programadas | Un calendario + una acción; sin nadie delante: hay que registrar y vigilar | `DBMS_SCHEDULER.CREATE_JOB` |
| Paquetes | Especificación (interfaz) y cuerpo (implementación); elementos privados | `CREATE PACKAGE` / `PACKAGE BODY` |
| Otros gestores | Mismos conceptos, sintaxis distinta; los disparadores y las tareas programadas son lo que más cambia | PL/pgSQL, SQL/PSM, T-SQL |

Ideas que conviene llevarse grabadas:

1. **Lo que se guarda en la base de datos se compila una vez.** Lo demás se analiza cada vez.
2. **Un `&` lo resuelve el cliente; un `v_` lo resuelve el servidor.**
3. **La excepción más peligrosa es la que se traga en silencio.**
4. **Una operación de negocio no confirma; quien la llama decide.** Una tarea desatendida sí.
5. **Un disparador es una restricción que se ejecuta sola:** pequeño, con un único propósito y con su prueba.
6. **Si necesitas leer la tabla que estás modificando, no lo hagas fila a fila:** anota en la fila y comprueba al final.

---

## 18. Autoevaluación

{{< quiz >}}
- q: "¿Qué distingue a una función de un procedimiento almacenado?"
  options: ["La función no puede tener parámetros", "La función devuelve un valor y se puede usar dentro de un `SELECT`; el procedimiento realiza una acción", "El procedimiento no se guarda en la base de datos", "La función solo puede ser llamada desde un disparador"]
  answer: 1
  explain: "Ambos son subprogramas almacenados con parámetros. La función termina con `RETURN` y puede formar parte de una expresión SQL; el procedimiento se invoca como una instrucción y devuelve información, si acaso, por parámetros `OUT`."
- q: "Un script usa `WHERE cod_grupo = '&grupo'`. ¿Qué afirmación es correcta?"
  options: ["`&grupo` es una variable PL/SQL declarada en el servidor", "El cliente sustituye `&grupo` antes de enviar el texto al servidor", "El valor cambia en cada vuelta de un bucle", "Funciona igual dentro de un procedimiento almacenado"]
  answer: 1
  explain: "Una variable de sustitución es texto que el cliente pega en el código antes de enviarlo. Por eso no existe en un procedimiento almacenado ni cambia dentro de un bucle."
- q: "¿Qué hace `SELECT AVG(nota_final) INTO v_media FROM matricula WHERE id_alumno = 30;` si el alumno 30 no tiene matrículas?"
  options: ["Lanza `NO_DATA_FOUND`", "Lanza `TOO_MANY_ROWS`", "Asigna `NULL` a `v_media`, sin error", "Asigna 0 a `v_media`"]
  answer: 2
  explain: "Un agregado sin `GROUP BY` devuelve siempre exactamente una fila, aunque no haya datos de entrada. `AVG` de ningún valor es `NULL`: no hay excepción, y `v_media` queda a `NULL`."
- q: "En un bucle con un cursor explícito, ¿por qué se escribe `EXIT WHEN c%NOTFOUND` justo después del `FETCH`?"
  options: ["Porque el cursor se cierra solo", "Porque el `FETCH` sin fila no modifica las variables y se repetiría la última", "Porque `%NOTFOUND` solo vale después del `CLOSE`", "Porque es obligatorio por sintaxis"]
  answer: 1
  explain: "El `FETCH` que no encuentra fila deja las variables con los valores anteriores. Si se procesan antes de comprobar `%NOTFOUND`, la última fila se trata dos veces."
- q: "`RAISE_APPLICATION_ERROR(-20013, 'Ya matriculado')` dentro de `pr_matricular` provoca…"
  options: ["Un `COMMIT` automático", "Un error `ORA-20013` que se propaga al llamador, que puede tratarlo", "La desactivación del procedimiento", "Que el `INSERT` se confirme igualmente"]
  answer: 1
  explain: "El error detiene el procedimiento y llega al llamador con ese código y mensaje. No confirma nada; la sentencia que invocó el procedimiento se deshace si nadie lo trata."
- q: "Un procedimiento trata una excepción con `WHEN OTHERS THEN DBMS_OUTPUT.PUT_LINE('error');` y termina. ¿Qué pasa con lo que hizo antes del error?"
  options: ["Oracle lo deshace siempre", "Se queda hecho: tratar la excepción evita el rollback implícito", "Se confirma con `COMMIT`", "Depende del valor de `SERVEROUTPUT`"]
  answer: 1
  explain: "Si la excepción se trata y el bloque termina con normalidad, Oracle no deshace nada. Para deshacer una parte hace falta un `SAVEPOINT` y un `ROLLBACK TO` en el manejador, y normalmente relanzar el error con `RAISE;`."
- q: "¿Cuál de estos disparadores puede modificar el valor que se va a guardar?"
  options: ["`AFTER UPDATE FOR EACH ROW`", "`BEFORE INSERT FOR EACH ROW`", "`AFTER STATEMENT`", "Ninguno: `:NEW` es de solo lectura"]
  answer: 1
  explain: "Solo un disparador `BEFORE` de fila puede asignar a `:NEW`. En un `AFTER`, Oracle devuelve `ORA-04084`."
- q: "Para implementar «un grupo no puede superar los 30 alumnos» sin `ORA-04091`, la solución habitual es…"
  options: ["Un `CHECK` sobre `cod_grupo`", "`AFTER EACH ROW` con `SELECT COUNT(*)`", "Un disparador compuesto: anotar el grupo en `AFTER EACH ROW` y contar en `AFTER STATEMENT`", "Desactivar el disparador durante la carga"]
  answer: 2
  explain: "Un `CHECK` no puede mirar otras filas. El disparador de fila que cuenta provoca la tabla mutante. El compuesto anota durante la sentencia y consulta al final, cuando la tabla ya no está mutando."
- q: "¿Qué ventaja de seguridad tiene conceder `EXECUTE` sobre `pr_matricular` en lugar de `INSERT` sobre `MATRICULA`?"
  options: ["Ninguna: son equivalentes", "La única vía de matricular pasa por las validaciones del procedimiento", "El usuario puede borrar matrículas sin control", "El procedimiento se ejecuta con los privilegios de quien lo llama"]
  answer: 1
  explain: "Por defecto un procedimiento se ejecuta con los privilegios de su propietario. Así la secretaría puede matricular, pero solo a través del procedimiento, que aplica las reglas del catálogo."
- q: "Una tarea creada con `DBMS_SCHEDULER` falla cada noche. ¿Dónde se ve la causa?"
  options: ["En el búfer de `DBMS_OUTPUT`", "En `USER_SCHEDULER_JOB_RUN_DETAILS` (columnas `STATUS`, `ERROR#` y `ADDITIONAL_INFO`)", "En la pantalla de quien creó la tarea", "En ningún sitio: las tareas no guardan historial"]
  answer: 1
  explain: "El historial de ejecuciones registra el estado de cada vez y, si falla, el código y el texto del error. Como nadie mira la salida de una tarea desatendida, la revisión periódica del historial es imprescindible."
{{< /quiz >}}

## Referencias

- [Oracle AI Database 26ai: Database PL/SQL Language Reference](https://docs.oracle.com/en/database/oracle/oracle-database/26/lnpls/) — bloques, variables, control de flujo, cursores, subprogramas, paquetes, excepciones y disparadores (incluidos los compuestos y la restricción de la tabla mutante).
- [Oracle AI Database 26ai: Database PL/SQL Packages and Types Reference, *DBMS_OUTPUT*](https://docs.oracle.com/en/database/oracle/oracle-database/26/arpls/DBMS_OUTPUT.html).
- [Oracle AI Database 26ai: Database PL/SQL Packages and Types Reference, *DBMS_SCHEDULER*](https://docs.oracle.com/en/database/oracle/oracle-database/26/arpls/DBMS_SCHEDULER.html) — tareas, calendarios y `EVALUATE_CALENDAR_STRING`.
- [Oracle AI Database 26ai: Database Administrator's Guide, *Scheduling Jobs with Oracle Scheduler*](https://docs.oracle.com/en/database/oracle/oracle-database/26/admin/scheduling-jobs-with-oracle-scheduler.html).
- [Oracle AI Database 26ai: SQL*Plus User's Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/26/sqpug/) — variables de sustitución, `SET SERVEROUTPUT`, `SPOOL` y ejecución de guiones.
- [Oracle SQLcl: documentación](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/) y [Oracle SQL Developer](https://docs.oracle.com/en/database/oracle/sql-developer/).
- [Oracle AI Database 26ai: Database Error Messages](https://docs.oracle.com/en/error-help/db/) — `ORA-04091`, `ORA-04088`, `ORA-01403`, `ORA-02292`, `ORA-27486`...
- [Oracle AI Database 26ai: Database Concepts, *Data Concurrency and Consistency*](https://docs.oracle.com/en/database/oracle/oracle-database/26/cncpt/data-concurrency-and-consistency.html) — consistencia de lectura, relevante para los disparadores.
- [PostgreSQL: PL/pgSQL](https://www.postgresql.org/docs/current/plpgsql.html) y [`pg_cron`](https://github.com/citusdata/pg_cron).
- [MySQL: Stored Objects](https://dev.mysql.com/doc/refman/8.4/en/stored-objects.html) y [MariaDB: Events](https://mariadb.com/kb/en/events/).
- [Microsoft: Transact-SQL, disparadores y SQL Server Agent](https://learn.microsoft.com/sql/t-sql/).
- [Real Decreto 405/2023, de 29 de mayo](https://www.boe.es/buscar/act.php?id=BOE-A-2023-13221) — enseñanzas mínimas del módulo 0484 Bases de datos (RA5, y los criterios RA4.d, RA4.h y RA6.h).
