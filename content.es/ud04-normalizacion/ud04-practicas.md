---
title: "Normalización - Prácticas"
weight: 2
bookToc: true
math: true
---

# UD04 · Prácticas

{{< ra "RA6:b,c,e,g,h" >}}

| Práctica | Tipo | Nivel | CE principales |
|---|---|---|---|
| [4.1 Normalizar las facturas de un taller](#práctica-41--normalizar-las-facturas-de-un-taller) | Guiada | ●○○ | RA6.b, RA6.c, RA6.g |
| [4.2 Dependencias, cierres y claves](#práctica-42--dependencias-cierres-y-claves) | Guiada | ●●○ | RA6.e, RA6.g |
| [4.3 ¿En qué forma normal está?](#práctica-43--en-qué-forma-normal-está) | Autónoma | ●●○ | RA6.g |
| [4.4 Reservas de un hotel rural](#práctica-44--reservas-de-un-hotel-rural) | Autónoma | ●●○ | RA6.b, RA6.c, RA6.e, RA6.g |
| [4.5 FNBC y dependencias perdidas](#práctica-45--fnbc-y-dependencias-perdidas) | Reto | ●●● | RA6.g, RA6.h |
| [4.6 ¿Normalizar o desnormalizar?](#práctica-46--normalizar-o-desnormalizar) | Reto | ●●● | RA6.g |
| [Proyecto EduGest · UD04](#proyecto-edugest--ud04-informe-de-normalización) | Proyecto | ●●○ | RA6.b, RA6.c, RA6.e, RA6.g, RA6.h |

---

## Práctica 4.1 · Normalizar las facturas de un taller

{{< practica num="4.1" tipo="Guiada" duracion="2 sesiones" nivel="1" ra="RA6: b, c, g" sgbd="Hoja de cálculo o papel" entrega="Documento con cada paso de la normalización" >}}

#### Objetivo

Seguir el procedimiento completo de normalización sobre un documento real (una factura) hasta obtener un esquema en 3FN.

#### Contexto

Un taller mecánico guarda sus facturas en una hoja de cálculo. Cada fila es una línea de factura:

| num_factura | fecha | matricula | modelo | dni_cliente | cliente | telefonos_cliente | cod_servicio | servicio | precio_actual | precio_aplicado | cantidad | mecanico | especialidad_mecanico |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F-101 | 03/10/2026 | 1234-LMN | Seat Ibiza | 11111111H | Pedro Ruiz | 600100200 | S01 | Cambio de aceite | 45 | 40 | 1 | Ana | Motor |
| F-101 | 03/10/2026 | 1234-LMN | Seat Ibiza | 11111111H | Pedro Ruiz | 600100200 | S07 | Filtro de aire | 18 | 18 | 1 | Ana | Motor |
| F-102 | 04/10/2026 | 5678-PQR | Kia Ceed | 22222222J | Laura Gil | 611200300, 966123456 | S01 | Cambio de aceite | 45 | 45 | 1 | Luis | Motor |
| F-102 | 04/10/2026 | 5678-PQR | Kia Ceed | 22222222J | Laura Gil | 611200300, 966123456 | S12 | Neumático | 80 | 75 | 4 | Marta | Ruedas |

Reglas del negocio (confirmadas con el taller):

- Cada factura corresponde a **un** vehículo y a **un** cliente, en una fecha.
- Cada vehículo pertenece a un único cliente; un cliente puede tener varios vehículos.
- `precio_actual` es el precio de catálogo del servicio; `precio_aplicado` es el que se cobró en esa factura (puede haber descuento).
- En una factura, cada servicio aparece en una sola línea y lo realiza un mecánico. Cada mecánico tiene una especialidad.

#### Desarrollo

{{% steps %}}

1. **Dependencias funcionales.** A partir de las reglas, escribe:
    - `num_factura → fecha, matricula`
    - `matricula → modelo, dni_cliente`
    - `dni_cliente → cliente` (y los teléfonos, que son multivaluados)
    - `cod_servicio → servicio, precio_actual`
    - `num_factura, cod_servicio → precio_aplicado, cantidad, mecanico`
    - `mecanico → especialidad_mecanico`

2. **Clave candidata.** `num_factura` y `cod_servicio` no aparecen a la derecha de ninguna dependencia. Calcula $\{num\_factura, cod\_servicio\}^+$ y comprueba que contiene todos los atributos (salvo los teléfonos, que se tratan en 1FN).

3. **1FN.** Saca `telefonos_cliente` a TELEFONO_CLIENTE(<u>*dni_cliente*, telefono</u>).

4. **2FN.** Elimina las dependencias parciales respecto a la clave (num_factura, cod_servicio):
    - FACTURA_2(<u>num_factura</u>, fecha, matricula, modelo, dni_cliente, cliente)
    - SERVICIO(<u>cod_servicio</u>, servicio, precio_actual)
    - LINEA(<u>*num_factura*, *cod_servicio*</u>, precio_aplicado, cantidad, mecanico, especialidad_mecanico)

5. **3FN.** Elimina las dependencias transitivas:
    - En FACTURA_2: `num_factura → matricula → modelo, dni_cliente → cliente`.
    - En LINEA: `(num_factura, cod_servicio) → mecanico → especialidad_mecanico`.

6. **Verifica** que con las tablas finales desaparecen las anomalías del principio.

{{% /steps %}}

{{< solucion id="ud04-001" title="Solución: esquema en 3FN" />}}

#### Comprobación

{{% comprobacion %}}
- [ ] Obtienes 7 tablas y todas tienen clave primaria.
- [ ] Ninguna tabla contiene a la vez `cliente` y `num_factura`.
- [ ] El cliente de una factura se obtiene a través del vehículo (factura → vehículo → cliente).
- [ ] Explicas por qué `precio_actual` y `precio_aplicado` están en tablas distintas.
{{% /comprobacion %}}

#### Errores habituales

> [!WARNING]
> - Guardar `dni_cliente` también en FACTURA «para no tener que pasar por el vehículo». Sería una dependencia transitiva: si el vehículo cambia de dueño, las facturas antiguas mostrarían datos contradictorios. Ojo: si el negocio exige conservar quién pagó cada factura aunque el coche cambie de dueño, entonces **sí** es un dato propio de la factura. Pregunta al cliente.
> - Borrar `precio_aplicado` por pensar que es redundante con `precio_actual`.

#### Ampliación

Comprueba en tu solución que la descomposición es **sin pérdida**: para cada par de tablas que se combinan, indica el atributo común y de qué tabla es clave. Cuando termines la UD07, escribe el `JOIN` que reconstruye la hoja original.

---

## Práctica 4.2 · Dependencias, cierres y claves

{{< practica num="4.2" tipo="Guiada" duracion="1 sesión" nivel="2" ra="RA6: e, g" sgbd="Papel" entrega="Hoja de ejercicios" >}}

#### Objetivo

Dominar el cálculo del cierre de atributos para encontrar todas las claves candidatas de una relación.

#### Enunciado

Para cada relación, calcula las claves candidatas indicando los cierres que has calculado. Después indica la forma normal más alta que cumple.

| # | Relación | Dependencias |
|---|---|---|
| a | R(A, B, C, D) | A → B, B → C, C → D |
| b | R(A, B, C, D) | AB → C, C → D, D → A |
| c | R(A, B, C, D, E) | A → BC, CD → E, B → D, E → A |
| d | CURSO(cod_curso, aula, hora, profesor) | cod_curso → profesor; aula, hora → cod_curso; profesor, hora → aula |

{{< solucion id="ud04-002" title="Soluciones" />}}

---

## Práctica 4.3 · ¿En qué forma normal está?

{{< practica num="4.3" tipo="Autónoma" duracion="1 sesión" nivel="2" ra="RA6: g" sgbd="Papel" entrega="Tabla de respuestas justificadas" >}}

#### Enunciado

Indica la forma normal más alta de cada relación (la clave primaria está subrayada) y, si no está en 3FN, normalízala.

1. ALUMNO(<u>nia</u>, nombre, idiomas) donde `idiomas` = «inglés, francés».
2. PRESTAMO(<u>isbn, num_socio, fecha</u>, titulo, nombre_socio, fecha_devolucion).
3. EMPLEADO(<u>id_emp</u>, nombre, cod_postal, poblacion), con `cod_postal → poblacion`.
4. VUELO(<u>num_vuelo, fecha</u>, avion, plazas_avion, piloto), con `avion → plazas_avion`.
5. PRODUCTO(<u>id_producto</u>, nombre, precio, iva), donde todos dependen solo de `id_producto`.
6. NOTA(<u>id_alumno, id_modulo, evaluacion</u>, nota, nombre_modulo).

#### Comprobación

{{% comprobacion %}}
- [ ] La relación 1 no está en 1FN.
- [ ] Las relaciones 2 y 6 están en 1FN (dependencias parciales).
- [ ] Las relaciones 3 y 4 están en 2FN (dependencias transitivas).
- [ ] La relación 5 está en FNBC.

{{% details title="Pista para la relación 4" %}}
La clave es compuesta (num_vuelo, fecha). `avion` depende de toda la clave (el mismo número de vuelo puede usar aviones distintos en días distintos), pero `plazas_avion` depende de `avion`, que no es clave: dependencia transitiva.
{{% /details %}}
{{% /comprobacion %}}

---

## Práctica 4.4 · Reservas de un hotel rural

{{< practica num="4.4" tipo="Autónoma" duracion="2 sesiones" nivel="2" ra="RA6: b, c, e, g" sgbd="Papel o Data Modeler" entrega="Informe de normalización completo" >}}

#### Contexto

Un hotel rural gestiona las reservas con este formulario en papel, que han pasado a una hoja de cálculo:

| cod_reserva | fecha_reserva | dni_cliente | nombre_cliente | email | num_hab | tipo_hab | precio_noche_tipo | fecha_entrada | fecha_salida | extras | importe_extras |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R1 | 01/09 | 33333333P | Elena Sanz | elena@mail.es | 3 | Doble | 85 | 10/10 | 12/10 | Desayuno, Parking | 30 |
| R1 | 01/09 | 33333333P | Elena Sanz | elena@mail.es | 4 | Doble | 85 | 10/10 | 12/10 | Desayuno | 20 |
| R2 | 05/09 | 44444444A | Iván Mora | ivan@mail.es | 1 | Suite | 140 | 15/10 | 16/10 | | 0 |

Una reserva puede incluir varias habitaciones, cada una con sus propios extras. El precio por noche depende del tipo de habitación. Cada extra tiene un precio por noche fijo.

#### Enunciado

1. Lista las anomalías que observas.
2. Escribe las dependencias funcionales y justifica las que no sean evidentes.
3. Determina la clave candidata.
4. Normaliza hasta 3FN mostrando el resultado de cada forma normal.
5. Decide qué hacer con `importe_extras`: ¿es un atributo derivado? ¿Debe guardarse?
6. Escribe al menos dos restricciones que no queden recogidas (por ejemplo, que una habitación no tenga dos reservas solapadas).

#### Comprobación

{{% comprobacion %}}
- [ ] `extras` se trata como multivaluado en 1FN y termina en una tabla con su propia clave.
- [ ] El precio por noche se asocia al **tipo** de habitación, no a la reserva.
- [ ] El esquema final tiene entre 6 y 8 tablas, y todas están en 3FN.
{{% /comprobacion %}}

---

## Práctica 4.5 · FNBC y dependencias perdidas

{{< practica num="4.5" tipo="Reto" duracion="1 sesión" nivel="3" ra="RA6: g, h" sgbd="Papel" entrega="Análisis razonado" >}}

#### Contexto

En una autoescuela, cada **profesor** da clase en **una sola** sede. Un alumno, en cada sede a la que acude, tiene asignado **un único** profesor.

CLASE(alumno, sede, profesor) con `alumno, sede → profesor` y `profesor → sede`.

#### Enunciado

1. Calcula las claves candidatas.
2. Demuestra que la relación está en 3FN pero no en FNBC.
3. Descomponla en FNBC y comprueba que la descomposición es sin pérdida.
4. ¿Qué dependencia se pierde? Escribe un ejemplo de datos que la incumpla y que las nuevas tablas aceptarían.
5. Recomienda una solución para la autoescuela y explica cómo garantizarías la regla perdida (adelanta lo que harías en la UD09).

{{% details title="Pista" %}}
Las claves son (alumno, sede) y (alumno, profesor). La descomposición en FNBC es PROFESOR_SEDE(<u>profesor</u>, sede) y ALUMNO_PROFESOR(<u>alumno, profesor</u>). Prueba a asignar al mismo alumno dos profesores de la misma sede.
{{% /details %}}

---

## Práctica 4.6 · ¿Normalizar o desnormalizar?

{{< practica num="4.6" tipo="Reto" duracion="1 sesión" nivel="3" ra="RA6: g" sgbd="Documento" entrega="Informe de decisión (1 página por caso)" >}}

#### Enunciado

Para cada propuesta de un compañero, decide si la aceptas, la rechazas o la aceptas con condiciones. Justifica la decisión con argumentos de integridad, rendimiento y mantenimiento.

1. «Guardemos el `nombre_ciclo` en cada fila de MATRICULA para que los informes de secretaría no necesiten tres JOIN».
2. «Añadamos `num_alumnos` a la tabla GRUPO, porque el panel de jefatura lo consulta cada vez que se abre».
3. «En la tabla de pedidos de la tienda online guardemos la dirección de envío completa, aunque ya esté en CLIENTE».
4. «Para el cuadro de mando de la dirección, creemos una tabla con una fila por ciclo, curso y año con la nota media y el número de aprobados, que se recalcula cada noche».

#### Comprobación

{{% comprobacion %}}
- [ ] El caso 3 se identifica como un dato **histórico** (la dirección puede cambiar después del pedido).
- [ ] El caso 4 se relaciona con los sistemas OLAP de la UD01.
- [ ] Cuando aceptas una redundancia, explicas **cómo** se mantiene sincronizada.
{{% /comprobacion %}}

---

## Proyecto EduGest · UD04: informe de normalización

{{< practica num="EduGest-4" tipo="Proyecto" duracion="Trabajo transversal (1 semana)" nivel="2" ra="RA6: b, c, e, g, h" sgbd="Documento Markdown" entrega="edugest/docs/04-normalizacion.md" >}}

#### Enunciado

1. **Migración de la hoja heredada.** Normaliza la hoja MATRICULA_HOJA de la [teoría](/ud04-normalizacion/ud04-teoria#1-por-qué-normalizar-las-anomalías) añadiéndole estas columnas: `email_tutor`, `departamento_tutor`, `faltas_totales`. Indica cómo encaja el resultado en tu modelo de EduGest.
2. **Verificación de tu esquema.** Para cada tabla de tu modelo relacional (EduGest-3), escribe sus dependencias funcionales y justifica que está en 3FN (o en FNBC).
3. **Comparación con la solución de referencia.** Ya puedes consultar el [modelo de referencia](/guia/proyecto-edugest#3-modelo-de-referencia). Escribe una tabla con las diferencias y, para cada una, si tu decisión era también válida o si la corriges.
4. **Catálogo de restricciones actualizado** con las que hayan aparecido al normalizar.

#### Comprobación

{{% comprobacion %}}
- [ ] `faltas_totales` se identifica como un atributo **derivado** y se justifica si se guarda o se calcula.
- [ ] Ninguna tabla del esquema final tiene dependencias parciales ni transitivas.
- [ ] Las diferencias con la referencia están argumentadas, no solo listadas.

> [!TIP]
> A partir de la UD05 todo el grupo trabajará con el esquema de referencia para que los resultados de las consultas coincidan. Si tu diseño era distinto pero correcto, menciónalo en tu documentación: esa capacidad de justificar alternativas es exactamente lo que evalúa RA6.
{{% /comprobacion %}}
