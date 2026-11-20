---
title: "Prácticas · Modelo relacional"
weight: 21
bookToc: true
math: true
---

# Tema 2 · Prácticas: modelo relacional
{{< ra "RA2:b,c,d,e,f,g,i" >}}

| Práctica | Tipo | Nivel | CE principales |
|---|---|---|---|
| [2.5 Biblioteca: del E/R a las tablas](#práctica-25--biblioteca-del-er-a-las-tablas) | Guiada | ●○○ | RA2.c-f |
| [2.6 Simulador de integridad referencial](#práctica-26--simulador-de-integridad-referencial) | Guiada | ●●○ | RA2.g, RA3.e |
| [2.7 Tres formas de transformar una jerarquía](#práctica-27--tres-formas-de-transformar-una-jerarquía) | Autónoma | ●●○ | RA2.c, RA2.e, RA2.f |
| [2.8 Catálogo de restricciones de un hotel](#práctica-28--catálogo-de-restricciones-de-un-hotel) | Autónoma | ●●○ | RA2.i |
| [Proyecto EduGest · Tema 2](#proyecto-edugest--tema-2-modelo-lógico) | Proyecto | ●●○ | RA2.b-g, RA2.i |

> [!TIP]
> Para escribir esquemas relacionales usa siempre la misma notación: `TABLA(`<u>clave_primaria</u>`, atributo, `*clave_ajena*`)`, y debajo de cada tabla, las claves ajenas con la tabla a la que apuntan, las claves alternativas y los atributos que **admiten nulos**.

---

## Práctica 2.5 · Biblioteca: del E/R a las tablas

{{< practica num="2.5" tipo="Guiada" duracion="2 sesiones" nivel="1" ra="RA2: c, d, e, f" sgbd="Papel o herramienta de modelado" entrega="Esquema relacional + diagrama relacional" >}}

#### Objetivo

Aplicar una a una las reglas de transformación al modelo conceptual de la práctica 2.1 y obtener un esquema relacional completo y justificado.

#### Contexto

Partimos del diagrama de la biblioteca municipal de la [práctica 2.1](/tema2-diseno-logico/er-practicas#práctica-21--biblioteca-municipal-del-enunciado-al-diagrama):

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

{{< solucion id="tema2-052" title="Diagrama relacional resultante" />}}

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
> - Olvidar la restricción «un libro tiene al menos un autor». La participación mínima 1 de `LIBRO` en `ESCRIBE` **no** se puede garantizar con una clave ajena: hay que documentarla (RA2.i).

---

## Práctica 2.6 · Simulador de integridad referencial

{{< practica num="2.6" tipo="Guiada" duracion="1 sesión" nivel="2" ra="RA2: g · RA3: e" sgbd="Papel" entrega="Hoja de respuestas" >}}

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

{{< solucion id="tema2-053" title="Soluciones" />}}

---

## Práctica 2.7 · Tres formas de transformar una jerarquía

{{< practica num="2.7" tipo="Autónoma" duracion="2 sesiones" nivel="2" ra="RA2: c, e, f" sgbd="Papel o Data Modeler" entrega="Tres esquemas + tabla comparativa" >}}

#### Objetivo

Comparar las alternativas de transformación de una jerarquía y elegir la más adecuada según el caso.

#### Enunciado

Usa la jerarquía de empleados de la clínica veterinaria de la [práctica 2.4](/tema2-diseno-logico/er-practicas#práctica-24--clínica-veterinaria-con-jerarquías): `EMPLEADO` (total y disyunta) con `VETERINARIO`, `AUXILIAR` y `ADMINISTRATIVO`.

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

## Práctica 2.8 · Catálogo de restricciones de un hotel

{{< practica num="2.8" tipo="Autónoma" duracion="1 sesión" nivel="2" ra="RA2: i · RA3: e" sgbd="Documento de texto" entrega="Catálogo de restricciones" >}}

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

Clasifica cada regla en una de estas categorías: **PK / clave alternativa**, **FK**, **atributo obligatorio**, **regla de fila** o **no representable** (documentar e implementar en el tema 5). En el último caso, usa el formato de documentación de la teoría.

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

## Proyecto EduGest · Tema 2: modelo lógico

{{< practica num="EduGest-2" tipo="Proyecto" duracion="Trabajo transversal (2 semanas)" nivel="2" ra="RA2: b, c, d, e, f, g, i" sgbd="draw.io u otra herramienta de modelado" entrega="edugest/docs/03-modelo-relacional.md + diagrama" >}}

#### Enunciado

Transforma **tu** modelo E/R de EduGest (práctica EduGest-2) en un modelo relacional:

1. Esquema relacional completo con claves primarias, ajenas y alternativas, y las columnas que admiten nulos.
2. Tabla de trazabilidad: elemento del E/R → regla aplicada → tabla o columna resultante (como la del [caso guiado](/tema2-diseno-logico/relacional-teoria#8-caso-guiado-edugest-del-modelo-er-al-relacional)).
3. Política de borrado de cada clave ajena, justificada.
4. Diagrama relacional hecho con una herramienta gráfica.
5. Catálogo de restricciones no representables (como mínimo las cinco del enunciado del proyecto).

#### Comprobación

{{% comprobacion %}}
- [ ] Todas las relaciones N:M del E/R se han convertido en tablas.
- [ ] La relación «imparte» conserva la información de profesor, módulo, grupo y curso académico.
- [ ] Ninguna clave ajena de matrículas o notas usa el borrado en cascada sin justificarlo.
{{% /comprobacion %}}

