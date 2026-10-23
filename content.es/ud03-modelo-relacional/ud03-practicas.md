---
title: "Modelo relacional - Prácticas"
weight: 2
bookToc: true
math: true
---

# UD03 · Prácticas

{{< ra "RA6:a,b,c,d,e,f,h" "RA2:a,d,e" >}}

| Práctica | Tipo | Nivel | CE principales |
|---|---|---|---|
| [3.1 Biblioteca: del E/R a las tablas](#práctica-31--biblioteca-del-er-a-las-tablas) | Guiada | ●○○ | RA6.b, RA6.c, RA6.d, RA6.e |
| [3.2 Simulador de integridad referencial](#práctica-32--simulador-de-integridad-referencial) | Guiada | ●●○ | RA6.f, RA2.e |
| [3.3 Tres formas de transformar una jerarquía](#práctica-33--tres-formas-de-transformar-una-jerarquía) | Autónoma | ●●○ | RA6.b, RA6.d, RA6.e |
| [3.4 Ingeniería inversa de un esquema](#práctica-34--ingeniería-inversa-de-un-esquema) | Reto | ●●● | RA6.a, RA6.d |
| [3.5 Catálogo de restricciones de un hotel](#práctica-35--catálogo-de-restricciones-de-un-hotel) | Autónoma | ●●○ | RA6.h |
| [Proyecto EduGest · UD03](#proyecto-edugest--ud03-modelo-lógico) | Proyecto | ●●○ | RA6.a-f, RA6.h |
| [3.6 Entender un esquema relacional](#práctica-36--entender-un-esquema-relacional) | Guiada | ●○○ | RA6.b, RA6.c, RA6.d |
| [Tarea 1 · Naviera](#tarea-1--naviera-capitanes-contenedores-puertos-y-barcos) | Guiada | ●○○ | RA6.b-e |
| [Tarea 2 · Instituto](#tarea-2--instituto-módulos-matrículas-delegados-y-casilleros) | Autónoma | ●●○ | RA6.b-e, RA6.h |
| [Tarea 3 · Concesionario](#tarea-3--concesionario-ventas-revisiones-y-mecánicos) | Autónoma | ●●○ | RA6.b-e |
| [Tarea 4 · Casas rurales](#tarea-4--casas-rurales) | Autónoma | ●●○ | RA6.b-e |
| [Tarea 5 · Esquema abstracto 1](#tarea-5--esquema-abstracto-1-ternaria-11n-y-agregación) | Reto | ●●● | RA6.b-e, RA6.h |
| [Tarea 6 · Esquema abstracto 2](#tarea-6--esquema-abstracto-2-agregación-con-relación-11-y-existencia) | Reto | ●●● | RA6.b-e, RA6.h |
| [Tarea 7 · Esquema abstracto 3](#tarea-7--esquema-abstracto-3-ternaria-con-una-entidad-repetida) | Reto | ●●● | RA6.b-e, RA6.h |
| [Banco de ejercicios](#banco-de-ejercicios) | Autónoma | ●○○ a ●●● | RA6, RA2 |

> [!TIP]
> Para escribir esquemas relacionales usa siempre la misma notación: `TABLA(`<u>clave_primaria</u>`, atributo, `*clave_ajena*`)`, y debajo de cada tabla, las claves ajenas con la tabla a la que apuntan, las claves alternativas y los atributos que **admiten nulos**.

---

## Práctica 3.1 · Biblioteca: del E/R a las tablas

{{< practica num="3.1" tipo="Guiada" duracion="2 sesiones" nivel="1" ra="RA6: b, c, d, e" sgbd="Papel o herramienta de modelado" entrega="Esquema relacional + diagrama relacional" >}}

#### Objetivo

Aplicar una a una las reglas de transformación al modelo conceptual de la práctica 2.1 y obtener un esquema relacional completo y justificado.

#### Contexto

Partimos del diagrama de la biblioteca municipal de la [práctica 2.1](/ud02-modelo-er/ud02-practicas#práctica-21--biblioteca-municipal-del-enunciado-al-diagrama):

{{< diagrama src="chen-biblioteca.svg" caption="Diagrama de Chen de la biblioteca: autores, libros y ejemplares" >}}

#### Desarrollo

{{% steps %}}

1. **Entidades fuertes → tablas.** Cada entidad fuerte da una tabla con sus atributos; el identificador pasa a ser la clave primaria.

    - AUTOR(<u>cod_autor</u>, nombre, nacionalidad)
    - LIBRO(<u>isbn</u>, titulo, anio, editorial)
    - SOCIO(<u>num_socio</u>, dni, nombre, telefono) · `dni` UK

2. **Entidad débil → tabla con la clave del propietario.** La clave primaria de `EJEMPLAR` combina la clave de `LIBRO` y su discriminador. Esa parte de la clave también es clave ajena.

    - EJEMPLAR(<u>*isbn*, num_ejemplar</u>, estado) · FK isbn → LIBRO

3. **Relación N:M → tabla nueva.** `ESCRIBE` se convierte en una tabla con las claves de las dos entidades.

    - ESCRIBE(<u>*cod_autor*, *isbn*</u>) · FK cod_autor → AUTOR, FK isbn → LIBRO

4. **Relación N:M con atributos y repetible → tabla nueva con la fecha en la clave.** Como un socio puede llevarse el mismo ejemplar en ocasiones distintas, la clave incluye la fecha de salida.

    - PRESTAMO(<u>*num_socio*, *isbn*, *num_ejemplar*, fecha_salida</u>, fecha_prevista, fecha_devolucion)
    - FK num_socio → SOCIO; FK (isbn, num_ejemplar) → EJEMPLAR · `fecha_devolucion` admite NULL

5. **Revisa las claves ajenas compuestas.** Una clave ajena apunta a la clave primaria **completa** de la tabla referenciada: (isbn, num_ejemplar) → EJEMPLAR(isbn, num_ejemplar), no cada columna por separado.

6. **Dibuja el diagrama relacional** en una herramienta de modelado (por ejemplo, draw.io) o en papel.

{{% /steps %}}

{{< solucion id="ud03-001" title="Diagrama relacional resultante" />}}

#### Comprobación

{{% comprobacion %}}
- [ ] Hay **6** tablas: 4 por las entidades y 2 por las relaciones N:M.
- [ ] La clave primaria de `PRESTAMO` tiene 4 columnas, o has justificado una clave artificial con una clave alternativa (UK) sobre esas 4 columnas.
- [ ] La clave ajena de `PRESTAMO` a `EJEMPLAR` es **compuesta**.
- [ ] Has indicado qué columnas admiten nulos.
{{% /comprobacion %}}

#### Errores habituales

> [!WARNING]
> - Crear dos claves ajenas separadas `isbn → LIBRO` y `num_ejemplar → EJEMPLAR`. `num_ejemplar` por sí solo no identifica nada.
> - Olvidar la restricción «un libro tiene al menos un autor». La participación mínima 1 de `LIBRO` en `ESCRIBE` **no** se puede garantizar con una clave ajena: hay que documentarla (RA6.h).

#### Ampliación

Sustituye la clave compuesta de `PRESTAMO` por un identificador artificial `id_prestamo`. ¿Qué restricción de clave alternativa (UK) necesitas para no perder información? ¿Qué ventajas e inconvenientes tiene cada opción?

---

## Práctica 3.2 · Simulador de integridad referencial

{{< practica num="3.2" tipo="Guiada" duracion="1 sesión" nivel="2" ra="RA6: f · RA2: e" sgbd="Papel" entrega="Hoja de respuestas" >}}

#### Objetivo

Predecir el efecto de las operaciones de borrado y modificación según la política de integridad referencial de cada clave ajena.

#### Contexto

Un fragmento de EduGest con estos datos:

**GRUPO**

| cod_grupo | cod_ciclo | id_tutor |
|---|---|---|
| 1DAM | DAM | 103 |
| 1DAW | DAW | 106 |
| 2ASIR | ASIR | NULL |

**ALUMNO**

| id_alumno | nombre | cod_grupo |
|---|---|---|
| 1 | Adrián | 1DAM |
| 2 | Rubén | 1DAM |
| 14 | Carla | 1DAW |
| 30 | Zoe | NULL |

**MATRICULA**

| id_matricula | id_alumno | id_modulo |
|---|---|---|
| 10001 | 1 | 2 |
| 10002 | 1 | 3 |
| 10050 | 14 | 12 |

Claves ajenas: `ALUMNO.cod_grupo → GRUPO` y `MATRICULA.id_alumno → ALUMNO`.

#### Enunciado

Para cada escenario, indica si la operación **se ejecuta o se rechaza** y, si se ejecuta, cómo quedan las tres tablas.

| # | Política de la clave ajena alumno → grupo | Política de la clave ajena matrícula → alumno | Operación |
|---|---|---|---|
| A | Restringido | En cascada | Borrar el grupo 1DAM |
| B | Puesta a nulos | En cascada | Borrar el grupo 1DAM |
| C | En cascada | Restringido | Borrar el grupo 1DAM |
| D | En cascada | En cascada | Borrar el grupo 1DAM |
| E | cualquiera | cualquiera | Borrar el grupo 2ASIR |
| F | cualquiera | cualquiera | Añadir el alumno 40, Eva, al grupo 3DAM |

{{< solucion id="ud03-002" title="Soluciones" />}}

#### Ampliación

¿Qué política elegirías para cada clave ajena de EduGest? Justifica al menos tres decisiones. Recuerda que en un centro educativo las matrículas y las notas son **documentos oficiales**.

> [!CAUTION]
> El borrado en cascada es cómodo, pero convierte un error humano (borrar el grupo equivocado) en una pérdida masiva de datos. Úsalo solo cuando las filas hijas no tengan sentido sin la fila padre **y** no tengan valor por sí mismas.

---

## Práctica 3.3 · Tres formas de transformar una jerarquía

{{< practica num="3.3" tipo="Autónoma" duracion="2 sesiones" nivel="2" ra="RA6: b, d, e" sgbd="Papel o Data Modeler" entrega="Tres esquemas + tabla comparativa" >}}

#### Objetivo

Comparar las alternativas de transformación de una jerarquía y elegir la más adecuada según el caso.

#### Enunciado

Usa la jerarquía de empleados de la clínica veterinaria de la [práctica 2.4](/ud02-modelo-er/ud02-practicas#práctica-24--clínica-veterinaria-con-jerarquías): `EMPLEADO` (total y disyunta) con `VETERINARIO`, `AUXILIAR` y `ADMINISTRATIVO`.

{{< diagrama src="chen-jerarquia-empleados.svg" caption="Jerarquía de especialización en notación de Chen" >}}

1. **Opción 1. Una sola tabla** con todos los atributos y un discriminador `tipo`.
2. **Opción 2. Una tabla para la superclase y una por subclase**, cada una con la clave primaria de la superclase como clave ajena.
3. **Opción 3. Solo tablas para las subclases**, cada una con los atributos comunes repetidos.

Para cada opción, escribe el esquema relacional y responde:

| Pregunta | Opción 1 | Opción 2 | Opción 3 |
|---|---|---|---|
| ¿Cuántos nulos aparecen? | | | |
| ¿Cómo se obtiene un listado de **todos** los empleados? | | | |
| ¿Cómo se garantiza que la jerarquía es **disyunta**? | | | |
| ¿Cómo se garantiza que es **total**? | | | |
| ¿Qué pasa con la relación «un veterinario realiza consultas»? | | | |

Termina recomendando una opción para la clínica.

#### Comprobación

- [ ] En la opción 1 propones una restricción de fila que obliga a rellenar `num_colegiado` cuando `tipo = 'VET'`.
- [ ] En la opción 2 identificas que la disyunción **no** se garantiza solo con claves ajenas.
- [ ] En la opción 3 detectas que la relación con `CONSULTA` solo afecta a `VETERINARIO` y que el DNI podría repetirse entre subclases.

{{% details title="Pista: la regla de fila de la opción 1" %}}
Hazte tres preguntas por cada opción: ¿qué atributos son obligatorios **solo** para un tipo de empleado? ¿Cómo sabe el SGBD qué tipo es cada fila? ¿Qué combinaciones de «tipo» y «atributos rellenos» son válidas? La regla de fila de la opción 1 debe aceptar solo esas combinaciones: veterinario con número de colegiado, auxiliar con titulación y administrativo sin ninguno de los dos.
{{% /details %}}

---

## Práctica 3.4 · Ingeniería inversa de un esquema

{{< practica num="3.4" tipo="Reto" duracion="1 sesión" nivel="3" ra="RA6: a, d" sgbd="Papel o draw.io" entrega="Diagrama E/R reconstruido + informe" >}}

#### Objetivo

Interpretar un esquema relacional existente, reconstruir el modelo conceptual del que procede y detectar decisiones de diseño discutibles.

#### Contexto

Heredas la base de datos de un **club de pádel**. No hay documentación, solo este esquema:

```text
JUGADOR(id_jugador, nombre, telefono, nivel, id_pareja_habitual*)
    FK id_pareja_habitual → JUGADOR
PISTA(num_pista, tipo, cubierta)
RESERVA(num_pista*, fecha, hora_inicio, id_jugador*, precio)
    FK num_pista → PISTA, FK id_jugador → JUGADOR
PARTICIPA(num_pista*, fecha*, hora_inicio*, id_jugador*)
    FK (num_pista, fecha, hora_inicio) → RESERVA, FK id_jugador → JUGADOR
TORNEO(id_torneo, nombre, fecha_inicio)
INSCRIPCION(id_torneo*, id_jugador1*, id_jugador2*, categoria)
    FK id_torneo → TORNEO, FK id_jugador1 → JUGADOR, FK id_jugador2 → JUGADOR
```

#### Enunciado

1. Subraya las claves primarias que deduces y justifícalas.
2. Dibuja el diagrama E/R del que procede: entidades, relaciones (incluida la reflexiva), cardinalidades y entidades débiles.
3. ¿Qué significa `RESERVA.id_jugador` y qué significa `PARTICIPA`? ¿Son redundantes?
4. Detecta al menos **dos problemas**. Por ejemplo, ¿qué impide inscribir la misma pareja dos veces cambiando el orden de los jugadores?
5. Propón las restricciones (clave alternativa, regla de fila o textuales) que los resuelven.

{{% details title="Pista para el punto 4" %}}
Con `INSCRIPCION(id_torneo, id_jugador1, id_jugador2)` como clave, las filas (T1, 5, 8) y (T1, 8, 5) son distintas para el SGBD pero representan la misma pareja. Una regla de fila («`id_jugador1` menor que `id_jugador2`») obliga a guardar siempre la pareja en el mismo orden. ¿Qué impide que un jugador se inscriba con él mismo?
{{% /details %}}

---

## Práctica 3.5 · Catálogo de restricciones de un hotel

{{< practica num="3.5" tipo="Autónoma" duracion="1 sesión" nivel="2" ra="RA6: h · RA2: e" sgbd="Documento de texto" entrega="Catálogo de restricciones" >}}

#### Objetivo

Clasificar las reglas de negocio según dónde pueden implementarse y documentar las que el modelo lógico no recoge.

#### Contexto

Esquema simplificado de un hotel:

```text
HABITACION(num_hab, tipo, capacidad, precio_noche)
CLIENTE(id_cliente, dni, nombre, fecha_nacimiento)
RESERVA(id_reserva, id_cliente*, num_hab*, fecha_entrada, fecha_salida, num_personas, importe)
```

#### Enunciado

Clasifica cada regla en una de estas categorías: **PK / clave alternativa**, **FK**, **atributo obligatorio**, **regla de fila** o **no representable** (documentar e implementar en la UD09). En el último caso, usa el formato de documentación de la teoría.

1. Dos clientes no pueden tener el mismo DNI.
2. La fecha de salida es posterior a la de entrada.
3. El número de personas no supera la capacidad de la habitación.
4. Una habitación no puede tener dos reservas que se solapen en fechas.
5. El tipo de habitación es «individual», «doble» o «suite».
6. El cliente que reserva debe ser mayor de edad en la fecha de entrada.
7. El importe es el precio por noche multiplicado por el número de noches.
8. Toda reserva corresponde a un cliente existente.

#### Comprobación

{{% comprobacion %}}
- [ ] Las reglas 3, 4, 6 y 7 están clasificadas como no representables o justificadas como tales.
- [ ] La regla 2 es una regla de fila: `fecha_salida` posterior a `fecha_entrada`.
- [ ] Para la regla 7 se discute si conviene **guardar** el importe o **calcularlo**.
{{% /comprobacion %}}

---

## Proyecto EduGest · UD03: modelo lógico

{{< practica num="EduGest-3" tipo="Proyecto" duracion="Trabajo transversal (2 semanas)" nivel="2" ra="RA6: a, b, c, d, e, f, h" sgbd="draw.io u otra herramienta de modelado" entrega="edugest/docs/03-modelo-relacional.md + diagrama" >}}

#### Enunciado

Transforma **tu** modelo E/R de EduGest (práctica EduGest-2) en un modelo relacional:

1. Esquema relacional completo con claves primarias, ajenas y alternativas, y las columnas que admiten nulos.
2. Tabla de trazabilidad: elemento del E/R → regla aplicada → tabla o columna resultante (como la del [caso guiado](/ud03-modelo-relacional/ud03-teoria#8-caso-guiado-edugest-del-modelo-er-al-relacional)).
3. Política de borrado de cada clave ajena, justificada.
4. Diagrama relacional hecho con una herramienta gráfica.
5. Catálogo de restricciones no representables (como mínimo las cinco del enunciado del proyecto).

#### Comprobación

{{% comprobacion %}}
- [ ] Todas las relaciones N:M del E/R se han convertido en tablas.
- [ ] La relación «imparte» conserva la información de profesor, módulo, grupo y curso académico.
- [ ] Ninguna clave ajena de matrículas o notas usa el borrado en cascada sin justificarlo.
{{% /comprobacion %}}

---

## Tareas de transformación: del E/R al modelo relacional

Las tareas de este apartado parten de un **diagrama EER ya hecho**, dibujado con la misma notación que el [banco de ejercicios de la UD02](/ud02-modelo-er/ud02-practicas#banco-de-ejercicios). Hay que obtener el **esquema relacional** y anotar las **pérdidas semánticas**: lo que el diagrama dice y las tablas no pueden garantizar por sí solas.

A diferencia del diagrama E/R, donde caben varias soluciones, la transformación de un diagrama dado es casi única. Los nombres de las claves ajenas pueden variar (`cod_emp`, `codigo_empleado`…), pero las **PK, FK, UK y VNN** tienen que ser las mismas.

### Notación del esquema

Cada tabla se escribe con sus columnas y, debajo, sus restricciones:

```text
CONTENEDOR (cod_contenedor, descripcion, dni_capitan, cod_puerto)
   PK:  cod_contenedor
   FK:  dni_capitan → CAPITAN
   FK:  cod_puerto  → PUERTO
   VNN: dni_capitan, cod_puerto
```

| Marca | Nombre | ¿Admite duplicados? | ¿Admite nulos? |
|---|---|---|---|
| **PK** | Clave primaria | No | No |
| **UK** | Clave alternativa (*unique key*) | No | No, si es clave candidata (se añade VNN) |
| **FK** | Clave ajena | Sí\* | Sí\* |
| **VNN** | Valor no nulo (*valor obligatorio*) | — | No |

\* Salvo que la columna forme parte también de una PK o UK, o tenga VNN.

> [!TIP]
> Es la misma información que la notación `TABLA(`<u>clave</u>`, columna, `*clave_ajena*`)` de las prácticas anteriores, pero en forma de lista. Con ella es más fácil revisar que no falta ninguna restricción y, en la UD05, cada línea se convierte casi directamente en una tabla de la base de datos.

### Reglas de transformación (resumen)

| Elemento del E/R | Resultado en el modelo relacional |
|---|---|
| Entidad fuerte | Tabla. El identificador pasa a PK; las claves alternativas, a UK. |
| Entidad débil por identificación (**ID**) | Tabla. PK = PK de la entidad propietaria + discriminador. La parte heredada es también FK. |
| Entidad débil por existencia (**E**) | Tabla con PK propia. La FK hacia la propietaria lleva **VNN**. |
| Relación 1:N | La PK del lado 1 viaja como **FK** a la tabla del lado N, con los atributos de la relación. Si el lado N no puede existir sin el otro (mínimo 1), la FK lleva **VNN**. |
| Relación N:M | **Tabla nueva**. PK = las dos claves (más el atributo que permita repetir la pareja, si lo hay). Cada clave es FK. |
| 1:1 con (0,1) y (0,1) | **Tabla nueva**: PK = clave de una entidad; UK = clave de la otra. |
| 1:1 con (0,1) y (1,1) | Se propaga la clave a la tabla de la entidad que participa obligatoriamente, con **UK** y **VNN**. |
| 1:1 con (1,1) y (1,1) | **Una sola tabla**: PK = clave de una entidad; UK = clave de la otra. |
| Reflexiva | Igual que la binaria del mismo tipo, con la misma tabla en los dos extremos (columnas renombradas). |
| Ternaria N:N:N | Tabla con las tres claves como PK. |
| Ternaria 1:N:N | PK = claves de los dos lados N; la del lado 1, con **VNN**. |
| Ternaria 1:1:N | PK = clave del lado N + una de las de lado 1; la otra combinación, **UK**. |
| Generalización | Tabla para la superclase y una por subclase, con la PK de la superclase como PK y FK. Total y disjunta **no se pueden** expresar: son pérdidas. |
| Agregación | La relación agregada se trata como una tabla más; su clave es la que la identifica. |
| Atributo multivaluado | Tabla nueva con la PK de la entidad y el valor. |

> [!IMPORTANT]
> **Pérdidas semánticas habituales.** Las claves no pueden garantizar: el mínimo 1 del lado 1 de una relación 1:N («todo profesor imparte al menos un módulo»), la existencia de una entidad respecto a una relación cuando están en tablas distintas, las generalizaciones totales o disjuntas y las restricciones entre relaciones («C solo se relaciona con D si lo está con B»). Se anotan y se resuelven en la implementación con reglas de fila, disparadores (UD09) o procedimientos.

---

## Práctica 3.6 · Entender un esquema relacional

{{< practica num="3.6" tipo="Guiada" duracion="1 sesión" nivel="1" ra="RA6: b, c, d" sgbd="Papel" entrega="Hoja de respuestas" >}}

#### Objetivo

Hacer el camino inverso: a partir de unas tablas con sus restricciones, **deducir las cardinalidades** de la relación que representan.

#### Contexto

Antes de transformar diagramas conviene saber «leer» un esquema. Cada restricción (PK, UK, FK, VNN) responde a una pregunta sobre la relación: ¿puede repetirse?, ¿puede faltar?

#### Desarrollo

El juego consiste en responder a cuatro preguntas usando la tabla de la notación (duplicados y nulos). Primero, un caso abstracto:

```text
T1 (A, B, C)          T2 (E, F)
   PK: A                 PK: E
                         FK: F → T1
```

- ¿Con cuántas filas de `T2` puede relacionarse una fila de `T1`? El valor de `A` puede aparecer en la columna `F` de **muchas** filas de `T2` (una FK admite duplicados), o de ninguna: **(0,N)**.
- ¿Con cuántas filas de `T1` se relaciona una fila de `T2`? `F` guarda **un único** valor y puede ser nulo (la FK admite nulos): **(0,1)**.

Ahora, la relación entre alumnos y asignaturas («los alumnos se matriculan de asignaturas»). Para cada esquema responde a:

1. ¿De cuántas asignaturas puede matricularse un alumno?
2. ¿Está obligado el alumno a matricularse de alguna asignatura?
3. ¿Cuántos alumnos puede tener una asignatura?
4. ¿Es necesario que las asignaturas tengan alumnos?

| Caso | Esquema |
|---|---|
| A | `ASIGNATURA (codigo, nombre, curso)` PK: codigo · `ALUMNO (dni, nombre, asig)` PK: dni · FK: asig → ASIGNATURA |
| B | Igual que A, añadiendo **VNN: asig** |
| C | `ALUMNO (dni, nombre)` PK: dni · `ASIGNATURA (codigo, nombre, curso, dni)` PK: codigo · UK: dni · FK: dni → ALUMNO |
| D | `ALUMNO (dni, nombre)` PK: dni · `ASIGNATURA (codigo, nombre, curso)` PK: codigo · `MATRICULA (dni, asig)` PK: (dni, asig) · FK: dni → ALUMNO · FK: asig → ASIGNATURA |
| E | Igual que D, pero con **PK: dni** en `MATRICULA` |
| F | `ASIGNATURA (codigo, nombre, curso, dni, nombre_alumno)` PK: codigo · UK: dni · VNN: dni (no hay tabla `ALUMNO`) |

{{< solucion id="ud03-003" title="Solución (inténtalo antes de abrirla)" />}}

#### Comprobación

{{% comprobacion %}}
- [ ] Para cada caso has escrito las cuatro respuestas y la cardinalidad (mín, máx) de cada lado.
- [ ] Has relacionado cada respuesta con una restricción concreta (PK, UK, FK o VNN).
{{% /comprobacion %}}

#### Errores habituales

> [!WARNING]
> - Pensar que una FK no admite duplicados. Lo que no se repite es la **PK** de la tabla referenciada, no la columna que la referencia.
> - Confundir el caso E con el D: una tabla intermedia no implica siempre N:M; depende de su clave primaria.

#### Ampliación

Escribe el esquema que corresponde a «un alumno se matricula de **una o varias** asignaturas y una asignatura tiene **como máximo 30** alumnos». ¿Qué parte puedes expresar con PK, UK, FK y VNN y qué parte queda como pérdida semántica?

---

### Tarea 1 · Naviera: capitanes, contenedores, puertos y barcos

{{< practica num="1" etiqueta="Tarea" tipo="Guiada" duracion="1 sesión" nivel="1" ra="RA6: b, c, d, e" sgbd="Papel" entrega="Esquema relacional + pérdidas semánticas" >}}

#### Objetivo

Transformar relaciones 1:N con participación obligatoria y una N:M que guarda un histórico.

#### Contexto

Es el diagrama del [ejercicio 4 de la UD02](/ud02-modelo-er/ud02-practicas#ejercicio-4--naviera-capitanes-contenedores-puertos-y-barcos).

{{< figura src="ud02/ej04.svg" alt="CAPITÁN transporta CONTENEDOR (1:N), CONTENEDOR llega a PUERTO (N:1), CAPITÁN gobierna BARCO (N:M con fecha_inicio y fecha_fin)" caption="Diagrama de partida: naviera" >}}

#### Enunciado

Obtén el esquema relacional del diagrama, indicando para cada tabla su PK, sus FK, sus UK y las columnas con VNN. Anota las pérdidas semánticas.

#### Tareas

1. Escribe una tabla por entidad.
2. Decide dónde van las claves de *transporta* y *llega a*. ¿Llevan VNN?
3. Convierte *gobierna* en tabla. ¿Qué columnas forman su PK? ¿Por qué no basta con (capitán, barco)?
4. Lista las pérdidas semánticas.

#### Comprobación

{{% comprobacion %}}
- [ ] Hay 5 tablas.
- [ ] `CONTENEDOR` tiene dos FK, ambas con VNN.
- [ ] La PK de `GOBIERNA` incluye `fecha_inicio`.
{{% /comprobacion %}}

#### Errores habituales

> [!WARNING]
> - Crear una tabla para cada relación 1:N. Solo las N:M (y algunas 1:1) generan tabla nueva.
> - Dejar la PK de `GOBIERNA` en (dni, matrícula): impediría que un capitán vuelva a gobernar el mismo barco.

{{< solucion id="ud03-004" title="Solución" />}}

#### Ampliación

La naviera quiere saber en qué **barco** viaja cada contenedor. Añade la relación al diagrama y transforma solo la parte que cambia.

---

### Tarea 2 · Instituto: módulos, matrículas, delegados y casilleros

{{< practica num="2" etiqueta="Tarea" tipo="Autónoma" duracion="1 sesión" nivel="2" ra="RA6: b, c, d, e, h" sgbd="Papel" entrega="Esquema relacional + pérdidas semánticas" >}}

#### Objetivo

Transformar dos relaciones reflexivas (1:N y N:M) y una 1:1 con mínimos 0 en los dos lados.

#### Contexto

Es el diagrama del [ejercicio 6 de la UD02](/ud02-modelo-er/ud02-practicas#ejercicio-6--instituto-módulos-matrículas-delegados-y-casilleros).

{{< figura src="ud02/ej06.svg" alt="PROFESOR imparte MÓDULO; MÓDULO es requisito de MÓDULO; ALUMNO se matricula en MÓDULO; ALUMNO es delegado de ALUMNO; ALUMNO tiene CASILLERO" caption="Diagrama de partida: instituto" >}}

#### Enunciado

Obtén el esquema relacional completo con PK, FK, UK y VNN, y anota las pérdidas semánticas.

#### Tareas

1. Transforma las entidades y la relación *imparte*.
2. Transforma las dos reflexivas. ¿Cuál necesita tabla propia y cuál no?
3. Transforma *tiene* aplicando la regla de la 1:1 con (0,1) y (0,1).
4. Lista las pérdidas semánticas.

#### Comprobación

{{% comprobacion %}}
- [ ] Hay 7 tablas.
- [ ] El delegado es una FK de `ALUMNO` a la propia tabla `ALUMNO`.
- [ ] `TIENE` tiene una PK y una UK.
{{% /comprobacion %}}

#### Errores habituales

> [!WARNING]
> - Poner `fecha_matricula` en `ALUMNO` (en la solución antigua aparecía en las dos tablas). Solo va en `MATRICULA`.
> - Usar el mismo nombre de columna para los dos módulos de `ES_REQUISITO`.

{{< solucion id="ud03-005" title="Solución" />}}

#### Ampliación

Un alumno puede repetir y matricularse **dos veces** del mismo módulo en cursos distintos. ¿Qué cambia en `MATRICULA`?

---

### Tarea 3 · Concesionario: ventas, revisiones y mecánicos

{{< practica num="3" etiqueta="Tarea" tipo="Autónoma" duracion="1 sesión" nivel="2" ra="RA6: b, c, d, e" sgbd="Papel" entrega="Esquema relacional + pérdidas semánticas" >}}

#### Objetivo

Transformar una entidad débil por identificación, una reflexiva 1:N y claves alternativas.

#### Contexto

Es el diagrama del [ejercicio 10 de la UD02](/ud02-modelo-er/ud02-practicas#ejercicio-10--concesionario-ventas-revisiones-y-mecánicos).

{{< figura src="ud02/ej10.svg" alt="CLIENTE compra COCHE (1:N), COCHE pasa REVISIÓN (débil, identificadora), MECÁNICO realiza REVISIÓN, MECÁNICO supervisa a MECÁNICO" caption="Diagrama de partida: concesionario" >}}

#### Enunciado

Obtén el esquema relacional con PK, FK, UK y VNN. Indica qué columnas de `REVISION` son a la vez PK y FK.

#### Comprobación

{{% comprobacion %}}
- [ ] La PK de `REVISION` es compuesta e incluye la matrícula.
- [ ] `nif` y `dni` son UK.
- [ ] La FK del cliente en `COCHE` admite nulos (coche sin vender).
{{% /comprobacion %}}

#### Errores habituales

> [!WARNING]
> - Escribir `PK (codigo, matricula)` sin marcar `matricula` como FK.
> - Poner VNN en `cod_cliente` de `COCHE`: el diagrama dice (0,1), un coche puede estar sin vender.

{{< solucion id="ud03-006" title="Solución" />}}

#### Ampliación

El taller guarda **qué piezas** se cambian en cada revisión y cuántas. Añade la entidad `PIEZA` y transforma la nueva relación. ¿Cuántas columnas tiene la PK de la tabla nueva?

---

### Tarea 4 · Casas rurales

{{< practica num="4" etiqueta="Tarea" tipo="Autónoma" duracion="1-2 sesiones" nivel="2" ra="RA6: b, c, d, e" sgbd="Papel" entrega="Dos esquemas relacionales + pérdidas semánticas" >}}

#### Objetivo

Transformar una cadena de entidades débiles con **claves ajenas compuestas** y distinguir la dependencia en identificación (identificadora) de la dependencia en existencia (E).

#### Contexto

El primer diagrama es el del [ejercicio 11 de la UD02](/ud02-modelo-er/ud02-practicas#ejercicio-11--casas-rurales-provincias-ciudades-y-habitaciones). El segundo es la variante de su ampliación.

{{< figura src="ud02/ej11.svg" alt="PROVINCIA tiene CIUDAD (débil). CASA_RURAL está en CIUDAD. CASA_RURAL dispone de HABITACIÓN (débil). CLIENTE se aloja en HABITACIÓN." caption="Diagrama 4.1: casas rurales" >}}

{{< figura src="ud03/tarea-rurales-b.svg" alt="PROVINCIA tiene CIUDAD (débil, identificadora). CASA depende en existencia de CIUDAD (E). PERSONA vive en CASA. PERSONA posee CASA con fecha de compra." caption="Diagrama 4.2: variante con residentes y propietarios" >}}

#### Enunciado

Obtén el esquema relacional de los dos diagramas.

#### Tareas

1. Escribe la PK de `CIUDAD`. ¿Cuántas columnas tiene la FK que la referencia desde `CASA_RURAL`?
2. Transforma `HABITACION` y la relación *se aloja*.
3. En el diagrama 4.2, ¿qué diferencia hay en el esquema entre la dependencia **ID** de `CIUDAD` y la **E** de `CASA`?

#### Comprobación

{{% comprobacion %}}
- [ ] Todas las FK que apuntan a `CIUDAD` tienen **dos** columnas.
- [ ] La PK de `SE_ALOJA` incluye la fecha de entrada.
- [ ] En 4.2, `CASA` tiene PK propia y su FK a `CIUDAD` lleva VNN.
{{% /comprobacion %}}

#### Errores habituales

> [!WARNING]
> - Escribir `FK: nombre_ciudad → CIUDAD` con una sola columna. La FK debe apuntar a la PK **completa** (era el error de la solución antigua).
> - Incluir la ciudad en la PK de `CASA` en el diagrama 4.2: la dependencia es de existencia, no de identificación.

{{< solucion id="ud03-007" title="Solución" />}}

#### Ampliación

Un cliente quiere reservar **varias habitaciones** con una sola reserva (número de reserva, fecha y forma de pago). Rediseña la parte del E/R afectada y transfórmala.

---

### Tarea 5 · Esquema abstracto 1: ternaria 1:1:N y agregación

{{< practica num="5" etiqueta="Tarea" tipo="Reto" duracion="1 sesión" nivel="3" ra="RA6: b, c, d, e, h" sgbd="Papel" entrega="Esquema relacional + pérdidas semánticas" >}}

#### Objetivo

Aplicar las reglas a un esquema sin significado (letras), donde solo cuentan la estructura y las cardinalidades.

#### Contexto

Los esquemas abstractos obligan a aplicar las reglas sin apoyarse en el sentido común del enunciado. Los atributos subrayados son identificadores; `a0` es el discriminador de la entidad débil `A`.

{{< figura src="ud03/tarea-abstracto-1.svg" alt="A débil de C por R1 (identificadora), reflexiva R3 sobre A, F y G especializan A (parcial, disjunta), ternaria R2 entre A, D y E (1:1:N), agregación de C-R4-B relacionada con D por R5" caption="Esquema abstracto 1" >}}

#### Enunciado

Obtén el esquema lógico relacional y enuncia las **pérdidas semánticas**.

#### Tareas

1. ¿Cuál es la PK de `A`? ¿Y la de `F` y `G`?
2. ¿Qué clave identifica a la agregación? Transforma *R5*.
3. Transforma la ternaria *R2* (1 junto a `A`, 1 junto a `D`, N junto a `E`): PK y UK.
4. Enuncia las pérdidas.

#### Comprobación

- [ ] Todas las FK hacia `A` tienen dos columnas.
- [ ] `R2` tiene PK y UK distintas.
- [ ] Has anotado que no se capta que la generalización sea disjunta.

{{< solucion id="ud03-008" title="Solución" />}}

---

### Tarea 6 · Esquema abstracto 2: agregación con relación 1:1 y existencia

{{< practica num="6" etiqueta="Tarea" tipo="Reto" duracion="1 sesión" nivel="3" ra="RA6: b, c, d, e, h" sgbd="Papel" entrega="Esquema relacional + pérdidas semánticas" >}}

#### Objetivo

Transformar una agregación de una N:M, una 1:1 con atributo y dependencia en existencia, una ternaria 1:N:N y una reflexiva sobre una subclase.

{{< figura src="ud03/tarea-abstracto-2.svg" alt="A débil de C (R1, identificadora); F y E especializan A (parcial, disjunta); R2 reflexiva 1:N sobre F; R3 N:M entre F y E; agregación de C-R4-D (N:M, D depende en existencia de R4) relacionada 1:1 con A por R5 (atributo m, E); ternaria R6 entre C, D y B (1:N:N)" caption="Esquema abstracto 2" >}}

#### Enunciado

Obtén el esquema lógico relacional y enuncia las pérdidas semánticas.

#### Tareas

1. Transforma la agregación: como *R4* es N:M, su tabla es la que representa la agregación.
2. Coloca *R5* (1:1, atributo `m`, la agregación depende en existencia de *R5*).
3. Transforma *R6* (1 junto a `C`).

#### Comprobación

- [ ] La tabla `R4` lleva la clave de `A`, el atributo `m`, una UK y VNN.
- [ ] `R6` tiene PK de dos columnas y la tercera con VNN.

{{< solucion id="ud03-009" title="Solución" />}}

---

### Tarea 7 · Esquema abstracto 3: ternaria con una entidad repetida

{{< practica num="7" etiqueta="Tarea" tipo="Reto" duracion="1-2 sesiones" nivel="3" ra="RA6: b, c, d, e, h" sgbd="Papel" entrega="Esquema relacional + pérdidas semánticas" >}}

#### Objetivo

Transformar una ternaria en la que una entidad participa dos veces, una 1:1 con (0,1) en los dos lados y una generalización total y solapada.

{{< figura src="ud03/tarea-abstracto-3.svg" alt="G débil de B (R5, identificadora); R6 1:1 G-H; agregación C-R4-D (C N, D 1) relacionada con G por R3 (atributo m, E) y N:M con F por R2; F y E especializan A (T,S); R1 ternaria F-F-E" caption="Esquema abstracto 3" >}}

#### Enunciado

Obtén el esquema lógico relacional y enuncia las pérdidas semánticas. En *R1*, `F` aparece dos veces: llama **F1** al extremo con N y **F2** al extremo con 1.

#### Tareas

1. ¿Qué clave identifica a la agregación si *R4* es 1:N?
2. Transforma *R3* (G con 1, la agregación con N y dependencia en existencia).
3. Transforma *R6* con la regla de la 1:1 con mínimos 0.
4. Transforma *R1* (F1: N, F2: 1, E: 1).

#### Comprobación

- [ ] La agregación queda representada por la tabla `C`.
- [ ] `R6` tiene PK de una columna y UK de dos.
- [ ] `R1` tiene PK (F1, F2) y UK (F1, E).

{{< solucion id="ud03-010" title="Solución" />}}

---


## Banco de ejercicios

> [!NOTE]
> Los ejercicios del banco piden el esquema relacional y, en algunos casos, las restricciones y políticas de borrado que lo acompañan. Todo se resuelve sobre el papel: la implementación en un gestor la harás cuando llegues a la [UD05](/ud05-ddl-dcl).

### Bloque 1: Ejercicios de Transformación de Relaciones Binarias y Claves

#### Ejercicio 1: Transformación de Relación Binaria 1:N (Clientes y Pedidos)

**Enunciado:**
Un cliente realiza varios pedidos en una tienda online, pero cada pedido es realizado por un único cliente. De los clientes se conoce su `id_cliente`, `nombre`, `email` y `telefono`. De los pedidos se conoce `num_pedido`, `fecha_pedido` e `importe_total`.

- a) Exprese el **Esquema Relacional Formal** derivado de esta relación $1:N$.
- b) Indique las **restricciones** que acompañan al esquema (claves alternativas, atributos obligatorios, reglas de dominio) y la **política de borrado** de cada clave foránea, justificándola.

---

#### Ejercicio 2: Transformación de Relación Binaria N:M (Médicos y Pacientes)

**Enunciado:**
Un médico atiende a múltiples pacientes en un centro hospitalario y un paciente puede ser atendido por diferentes médicos especialistas. De los médicos se conoce `num_colegiado`, `nombre` y `especialidad`. De los pacientes se registra `id_paciente`, `dni`, `nombre` y `fecha_nacimiento`. De cada atención médica realizada se guarda la `fecha_atencion` y el `diagnostico`.

- a) Exprese el **Esquema Relacional Formal** resultante para la relación $N:M$.
- b) Indique las **restricciones** que acompañan al esquema (claves alternativas, atributos obligatorios, reglas de dominio) y la **política de borrado** de cada clave foránea, justificándola.

---

#### Ejercicio 3: Transformación de Relación 1:1 Opcional (Empleados y Vehículos de Empresa)

**Enunciado:**
Una empresa asigna un coche de empresa a ciertos empleados clave. Un empleado solo puede tener asignado como máximo un coche, y un coche pertenece como máximo a un único empleado. Algunos empleados no tienen coche asignado. De los empleados se conoce `id_empleado` y `nombre`. De los vehículos se conoce `matricula`, `modelo` y `color`.

- a) Indique qué estrategia de propagación de clave es la más adecuada para evitar la presencia innecesaria de valores nulos.
- b) Indique las **restricciones** que acompañan al esquema (claves alternativas, atributos obligatorios, reglas de dominio) y la **política de borrado** de cada clave foránea, justificándola.

---

#### Ejercicio 4: Entidad Débil por Identificación (Edificios y Aulas)

**Enunciado:**
Un campus universitario organiza sus aulas dentro de edificios. De cada edificio se conoce `cod_edificio` y `nombre_edificio`. De las aulas se conoce `num_aula` (101, 102, 201...) y `capacidad_puestos`. El número de aula no es único en todo el campus, sino únicamente dentro de cada edificio determinado.

- a) Exprese el **Esquema Relacional Formal** especificando la clave primaria compuesta de la tabla `AULA`.
- b) Indique las **restricciones** que acompañan al esquema (claves alternativas, atributos obligatorios, reglas de dominio) y la **política de borrado** de cada clave foránea, justificándola.

---

#### Ejercicio 5: Entidad Débil por Existencia e Identificación (Pacientes e Ingresos)

**Enunciado:**
En un hospital, un paciente puede realizar múltiples ingresos a lo largo del tiempo. De cada paciente se almacena `id_paciente`, `dni` y `nombre`. De cada ingreso se registra `num_ingreso` (1, 2, 3... secuencial para cada paciente), `fecha_ingreso` y `habitacion`. El ingreso no puede existir ni identificarse sin el paciente al que pertenece.

- a) Exprese el esquema relacional formal para `PACIENTE` e `INGRESO`.
- b) Indique las **restricciones** que acompañan al esquema (claves alternativas, atributos obligatorios, reglas de dominio) y la **política de borrado** de cada clave foránea, justificándola.

---

### Bloque 2: Ejercicios de Relaciones Reflexivas, Atributos Especiales y Jerarquías

#### Ejercicio 6: Relación Reflexiva 1:N (Organigrama de Empleados)

**Enunciado:**
En una empresa, cada empleado tiene un único jefe directo, que es a su vez otro empleado de la plantilla. De cada empleado se conoce `id_empleado`, `nombre`, `puesto` y `salario`.

- a) Exprese el **Esquema Relacional Formal** indicando cómo se implementa la autorreferencia.
- b) Indique las **restricciones** que acompañan al esquema (claves alternativas, atributos obligatorios, reglas de dominio) y la **política de borrado** de cada clave foránea, justificándola.

---

#### Ejercicio 7: Relación Reflexiva N:M (Estructura Compuesta de Piezas / BOM)

**Enunciado:**
Una fábrica de maquinaria registra piezas industriales. De cada pieza se almacena `cod_pieza`, `nombre_pieza` y `precio`. Una pieza puede estar compuesta por varias subpiezas componentes, y a su vez una subpieza forma parte de la fabricación de múltiples piezas superiores. En cada ensamblaje se indica la `cantidad_unidades`.

- a) Exprese el **Esquema Relacional Formal** definiendo la tabla intermedia de ensamblaje.
- b) Indique las **restricciones** que acompañan al esquema (claves alternativas, atributos obligatorios, reglas de dominio) y la **política de borrado** de cada clave foránea, justificándola.

---

#### Ejercicio 8: Atributo Multivaluado (Teléfonos de Contacto de Clientes)

**Enunciado:**
De cada cliente de un banco se conoce `id_cliente`, `nombre` y `email`. Un cliente puede disponer de varios números de teléfono de contacto (`telefono`).

- a) Indique por qué no se pueden guardar los teléfonos como una lista separada por comas dentro de la misma celda de la tabla `CLIENTE`.
- b) Exprese el esquema relacional formal transformando el atributo multivaluado en una tabla independiente.
- c) Indique las **restricciones** que acompañan al esquema (claves alternativas, atributos obligatorios, reglas de dominio) y la **política de borrado** de cada clave foránea, justificándola.

---

#### Ejercicio 9: Atributo Compuesto (Dirección Estructurada)

**Enunciado:**
De cada proveedor se conoce su `nif`, `nombre_empresa` y el atributo compuesto `direccion` (formado por `calle`, `numero`, `piso`, `codigo_postal` y `ciudad`).

- a) Muestre cómo se transforma el atributo compuesto al modelo relacional lógico.
- b) Indique las **restricciones** que acompañan al esquema (claves alternativas, atributos obligatorios, reglas de dominio) y la **política de borrado** de cada clave foránea, justificándola.

---

#### Ejercicio 10: Transformación de Jerarquía EER (Opción de Tabla Única con Discriminador)

**Enunciado:**
Una empresa clasifica a sus empleados en dos tipos exclusivos: `PROGRAMADOR` (con el atributo `lenguaje_principal`) y `ADMINISTRATIVO` (con el atributo `nivel_ofimatica`). Los atributos comunes a todos los empleados son `id_empleado`, `nombre` y `salario`.

- a) Muestre el esquema relacional aplicando la estrategia de **Tabla Única** con una columna discriminadora `tipo_empleado`.
- b) Indique las **restricciones** que acompañan al esquema (claves alternativas, atributos obligatorios, reglas de dominio) y la **política de borrado** de cada clave foránea, justificándola.

---

#### Ejercicio 11: Transformación de Jerarquía EER (Opción de Tabla por Categoría con Claves Foráneas)

**Enunciado:**
Considere la misma jerarquía de empleados del Ejercicio 10, pero aplique la estrategia de **Tabla para el Supertipo y Tablas para cada Subtipo**.

- a) Exprese el **Esquema Relacional Formal** para las 3 tablas resultantes (`EMPLEADO`, `PROGRAMADOR`, `ADMINISTRATIVO`).
- b) Indique las **restricciones** que acompañan al esquema (claves alternativas, atributos obligatorios, reglas de dominio) y la **política de borrado** de cada clave foránea, justificándola.

---

### Bloque 3: Casos Integradores Complejos (3 a 5 Entidades)

#### Ejercicio 12: Sistema de Gestión de Concesionario de Vehículos

**Enunciado:**
Diseñe el esquema relacional para un concesionario a partir de los siguientes requisitos:

- **Clientes:** `id_cliente` (PK), `nif`, `nombre` y `telefono`.
- **Coches:** `matricula` (PK), `modelo`, `precio_venta` y el cliente comprador (`id_cliente`). Un cliente puede comprar varios coches.
- **Revisiones:** Cada coche pasa revisiones en el taller. La revisión se identifica de forma débil por `num_revision` (1, 2, 3...) dentro de cada coche (`matricula`), registrando `fecha_revision` y `coste`.
- **Mecánicos:** Cada revisión es realizada por un único mecánico (`id_mecanico` [PK], `nombre`, `especialidad`). Un mecánico supervisa a otros mecánicos (relación reflexiva $1:N$).

- a) Redacte el **Esquema Relacional Formal Completo** de todas las tablas con sus PKs y FKs.
- b) Indique las **restricciones** que acompañan al esquema (claves alternativas, atributos obligatorios, reglas de dominio) y la **política de borrado** de cada clave foránea, justificándola.

---

#### Ejercicio 13: Gestión de Hoteles, Habitaciones Débiles y Reservas de Clientes

**Enunciado:**
Una cadena hotelera administra establecimientos:

- **Hoteles:** `id_hotel` (PK), `nombre_hotel`, `ciudad`.
- **Habitaciones:** `num_habitacion` (101, 102...) identificado de forma débil respecto al `id_hotel`. Se guarda la `capacidad` y `precio_noche`.
- **Clientes:** `id_cliente` (PK), `dni`, `nombre`, `email`.
- **Reservas:** Un cliente reserva una habitación específica de un hotel para un rango de fechas (`fecha_inicio`, `fecha_fin`, `precio_total`). Un cliente realiza muchas reservas y una habitación recibe distintas reservas en fechas diferentes.

- a) Redacte el **Esquema Relacional Formal Completo**.
- b) Indique las **restricciones** que acompañan al esquema (claves alternativas, atributos obligatorios, reglas de dominio) y la **política de borrado** de cada clave foránea, justificándola.

---

#### Ejercicio 14: Sistema de Videoclub / Plataforma de Contenidos

**Enunciado:**
Se requiere estructurar la base de datos de un videoclub digital:

- **Películas:** `id_pelicula` (PK), `titulo`, `duracion`, `año`.
- **Actores:** `id_actor` (PK), `nombre`, `nacionalidad`. Una película cuenta con varios actores y un actor participa en varias películas (registrando el `papel_desempeñado`).
- **Socios:** `num_socio` (PK), `dni`, `nombre`, `fecha_alta`. Un socio apadrina o recomienda la plataforma a otros nuevos socios (relación reflexiva $1:N$ `APADRINA`).
- **Alquileres:** Un socio alquila películas registrando `fecha_alquiler` y `precio_alquiler`.

- a) Redacte el **Esquema Relacional Formal Completo**.
- b) Indique las **restricciones** que acompañan al esquema (claves alternativas, atributos obligatorios, reglas de dominio) y la **política de borrado** de cada clave foránea, justificándola.

---

#### Ejercicio 15: Fabricación Industrial y Control de Calidad

**Enunciado:**
Una fábrica de maquinaria de alta precisión organiza su catálogo:

- **Líneas de Montaje:** `id_linea` (PK), `denominacion`.
- **Piezas:** `cod_pieza` (PK), `nombre_pieza`, `peso`. Una pieza está compuesta por otras subpiezas componentes (relación reflexiva $N:M$ `ENSAMBLADA_CON` con atributo `cantidad`).
- **Inspecciones de Calidad:** Cada pieza fabricada en una línea pasa inspecciones. La inspección se identifica de forma débil por `num_inspeccion` relativo a la pieza (`cod_pieza`), registrando `fecha_inspeccion`, `resultado` (Aprobado/Rechazado) y la línea de montaje donde se realizó.

- a) Redacte el **Esquema Relacional Formal Completo**.
- b) Indique las **restricciones** que acompañan al esquema (claves alternativas, atributos obligatorios, reglas de dominio) y la **política de borrado** de cada clave foránea, justificándola.

---

#### Ejercicio 16: Red de Transportes Urbanos (Líneas, Paradas Débiles y Transbordos)

**Enunciado:**
Una empresa municipal de transportes gestiona autobuses:

- **Líneas:** `cod_linea` (PK), `nombre_linea`, `frecuencia`.
- **Paradas Débiles:** Cada línea realiza paradas en una secuencia ordenada `num_orden` (1, 2, 3...) relativa a la línea (`cod_linea`), registrando `calle_ubicacion`.
- **Transbordos Reflexivos:** Dos líneas pueden conectarse en puntos de transbordo (relación reflexiva $N:M$ `TRANSBORDO` entre líneas con atributo `tiempo_minutos_andando`).
- **Autobuses:** `matricula` (PK), `modelo`, adscritos a una línea.

- a) Redacte el **Esquema Relacional Formal Completo**.
- b) Indique las **restricciones** que acompañan al esquema (claves alternativas, atributos obligatorios, reglas de dominio) y la **política de borrado** de cada clave foránea, justificándola.

---

#### Ejercicio 17: Organización de Torneo Deportivo

**Enunciado:**
Una federación de baloncesto gestiona su liga:

- **Equipos:** `id_equipo` (PK), `nombre_club`, `ciudad`.
- **Jugadores:** `num_ficha` (PK), `nombre`, `dorsal`, perteneciente a un equipo. Un jugador actúa como capitán del equipo (relación $1:1$ de capitanía).
- **Partidos:** `id_partido` (PK), `fecha`, enfrentando a dos equipos distintos (uno local y otro visitante).
- **Incidencias Débiles:** Cada partido genera incidencias en el acta identificadas por `num_incidencia` secuencial relativo al partido (`id_partido`), registrando el `minuto` y el `tipo_incidencia`.

- a) Redacte el **Esquema Relacional Formal Completo**.
- b) Indique las **restricciones** que acompañan al esquema (claves alternativas, atributos obligatorios, reglas de dominio) y la **política de borrado** de cada clave foránea, justificándola.

---

#### Ejercicio 18: Análisis de Inconsistencias en Tablas Relacionales

**Enunciado:**
Dada la siguiente tabla `PEDIDO_DESNORMALIZADO`:

| `num_pedido` | `fecha` | `id_cliente` | `nombre_cliente` | `id_producto` | `precio` | `cantidad` |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `5001` | `'2026-10-01'` | `10` | `'Juan'` | `'P1'` | `15.00` | `2` |
| `5001` | `'2026-10-01'` | `10` | `'Juan'` | `'P2'` | `30.00` | `1` |
| `5002` | `'2026-10-02'` | `10` | `'Juan Perez'` | `'P1'` | `15.00` | `5` |

- a) Identifique qué problemas de redundancia e inconsistencia presenta esta tabla plana.
- b) Rediseñe la estructura descomponiéndola en un esquema de 4 tablas relacionales bien definidas con sus respectivas claves primarias y foráneas (`CLIENTE`, `PRODUCTO`, `PEDIDO`, `LINEA_PEDIDO`).

---

#### Ejercicio 19: Definición de Acciones de Integridad Referencial

**Enunciado:**
Considere las tablas `CURSO(id_curso [PK], nombre)` y `ALUMNO(id_alumno [PK], nombre, id_curso [FK])`.

- Explique qué ocurre en la tabla `ALUMNO` al borrar el curso 5 en cada uno de los siguientes escenarios de configuración de la clave foránea:
  1. Borrado en cascada
  2. Borrado restringido
  3. Puesta a nulos

---

#### Ejercicio 20: Caso Integrador de Hospital y Tarjetas de Visita Débiles

**Enunciado:**
Un centro sanitario gestiona sus pacientes e ingresos:

- **Pacientes:** `id_paciente` (PK), `dni`, `nombre`.
- **Plantas de Hospital:** `num_planta` (PK), `denominacion`.
- **Camas Débiles:** Cada planta tiene camas numeradas `num_cama` (1, 2, 3...) relativas a esa planta (`num_planta`).
- **Asignaciones / Ingresos:** Un paciente es ingresado en una cama de una planta en una `fecha_ingreso`.
- **Tarjetas de Visita Débiles:** Por cada paciente ingresado se emiten hasta 4 tarjetas de visita autorizadas, identificadas por un `num_tarjeta` (1, 2, 3, 4) relativo al paciente (`id_paciente`), con `horario_autorizado`.

- a) Redacte el **Esquema Relacional Formal Completo** identificando todas las entidades débiles y claves compuestas.
- b) Indique las **restricciones** que acompañan al esquema (claves alternativas, atributos obligatorios, reglas de dominio) y la **política de borrado** de cada clave foránea, justificándola.
