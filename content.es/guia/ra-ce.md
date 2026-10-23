---
title: "Resultados de aprendizaje y criterios de evaluación"
weight: 1
---

# Resultados de aprendizaje y criterios de evaluación

El módulo **0372. Gestión de bases de datos** (1º de Administración de Sistemas Informáticos en Red, ASIR) se rige por el **Real Decreto 1629/2009, de 30 de octubre**, que establece el título y sus enseñanzas mínimas. El módulo tiene **6 resultados de aprendizaje (RA)** con **47 criterios de evaluación (CE)**. Estos apuntes se imparten en **160 horas de aula** (5 por semana): el RD fija 105 horas como mínimo, y el currículo de la Comunitat Valenciana amplía el módulo hasta las 160.

> [!IMPORTANT]
> Un **resultado de aprendizaje** describe lo que sabrás hacer al terminar el módulo. Un **criterio de evaluación** es una evidencia concreta que demuestra que lo has conseguido. Cada tema, práctica y ejercicio de estos apuntes indica qué CE trabaja.

## Horas por resultado de aprendizaje

El módulo se organiza en **6 temas, uno por cada RA** (el tema 1 desarrolla el RA1, el tema 2 el RA2, y así hasta el tema 6 y el RA6). Todo el contenido de los temas se corresponde con los criterios de evaluación del RD 1629/2009.

| RA | Resultado de aprendizaje | Tema | Horas |
|---|---|---|:-:|
| **RA1** | Reconoce los elementos de las bases de datos analizando sus funciones y valorando la utilidad de los sistemas gestores. | [Tema 1](/tema1-introduccion) | 19 |
| **RA2** | Diseña modelos lógicos normalizados interpretando diagramas entidad/relación. | [Tema 2](/tema2-diseno-logico) | 29 |
| **RA3** | Realiza el diseño físico de bases de datos utilizando asistentes, herramientas gráficas y el lenguaje de definición de datos. | [Tema 3](/tema3-diseno-fisico) | 29 |
| **RA4** | Consulta la información almacenada manejando asistentes, herramientas gráficas y el lenguaje de manipulación de datos. | [Tema 4](/tema4-consultas) | 23 |
| **RA5** | Modifica la información almacenada utilizando asistentes, herramientas gráficas y el lenguaje de manipulación de datos. | [Tema 5](/tema5-modificacion) | 26 |
| **RA6** | Ejecuta tareas de aseguramiento de la información, analizándolas y aplicando mecanismos de salvaguarda y transferencia. | [Tema 6](/tema6-aseguramiento) | 25 |
| | *Pruebas de evaluación (3 × 3 h)* | | 9 |
| | **Total** | | **160** |

```mermaid
flowchart LR
    T1["Tema 1 · RA1<br/>Elementos de las BD y SGBD"] --> T2
    T2["Tema 2 · RA2<br/>Diseño lógico normalizado"] --> T3
    T3["Tema 3 · RA3<br/>Diseño físico (DDL)"] --> T4
    T4["Tema 4 · RA4<br/>Consultas"] --> T5
    T5["Tema 5 · RA5<br/>Modificación, transacciones y guiones"] --> T6
    T6["Tema 6 · RA6<br/>Seguridad: copias, importación y exportación"]
```

## Criterios de evaluación por resultado de aprendizaje

Texto literal de las enseñanzas mínimas. La última columna indica en qué tema se trabaja cada criterio.

## RA1. Reconoce los elementos de las bases de datos analizando sus funciones y valorando la utilidad de los sistemas gestores.

| CE | Criterio de evaluación | Tema |
|---|---|---|
| RA1.a | Se han analizado los distintos sistemas lógicos de almacenamiento y sus funciones. | [Tema 1](/tema1-introduccion) |
| RA1.b | Se han identificado los distintos tipos de bases de datos según el modelo de datos utilizado. | [Tema 1](/tema1-introduccion) |
| RA1.c | Se han identificado los distintos tipos de bases de datos en función de la ubicación de la información. | [Tema 1](/tema1-introduccion) |
| RA1.d | Se ha reconocido la utilidad de un sistema gestor de bases de datos. | [Tema 1](/tema1-introduccion) |
| RA1.e | Se ha descrito la función de cada uno de los elementos de un sistema gestor de bases de datos. | [Tema 1](/tema1-introduccion) |
| RA1.f | Se han clasificado los sistemas gestores de bases de datos. | [Tema 1](/tema1-introduccion) |

## RA2. Diseña modelos lógicos normalizados interpretando diagramas entidad/relación.

| CE | Criterio de evaluación | Tema |
|---|---|---|
| RA2.a | Se ha identificado el significado de la simbología propia de los diagramas entidad/relación. | [Tema 2](/tema2-diseno-logico) |
| RA2.b | Se han utilizado herramientas gráficas para representar el diseño lógico. | [Tema 2](/tema2-diseno-logico), [Tema 3](/tema3-diseno-fisico) |
| RA2.c | Se han identificado las tablas del diseño lógico. | [Tema 2](/tema2-diseno-logico) |
| RA2.d | Se han identificado los campos que forman parte de las tablas del diseño lógico. | [Tema 2](/tema2-diseno-logico) |
| RA2.e | Se han identificado las relaciones entre las tablas del diseño lógico. | [Tema 2](/tema2-diseno-logico) |
| RA2.f | Se han definido los campos clave. | [Tema 2](/tema2-diseno-logico) |
| RA2.g | Se han aplicado las reglas de integridad. | [Tema 2](/tema2-diseno-logico), [Tema 3](/tema3-diseno-fisico), [Tema 5](/tema5-modificacion) |
| RA2.h | Se han aplicado las reglas de normalización hasta un nivel adecuado. | [Tema 2](/tema2-diseno-logico) |
| RA2.i | Se han identificado y documentado las restricciones que no pueden plasmarse en el diseño lógico. | [Tema 2](/tema2-diseno-logico) |

## RA3. Realiza el diseño físico de bases de datos utilizando asistentes, herramientas gráficas y el lenguaje de definición de datos.

| CE | Criterio de evaluación | Tema |
|---|---|---|
| RA3.a | Se han definido las estructuras físicas de almacenamiento. | [Tema 3](/tema3-diseno-fisico) |
| RA3.b | Se han creado tablas. | [Tema 3](/tema3-diseno-fisico) |
| RA3.c | Se han seleccionado los tipos de datos adecuados. | [Tema 3](/tema3-diseno-fisico) |
| RA3.d | Se han definido los campos clave en las tablas. | [Tema 3](/tema3-diseno-fisico) |
| RA3.e | Se han implantado todas las restricciones reflejadas en el diseño lógico. | [Tema 2](/tema2-diseno-logico), [Tema 3](/tema3-diseno-fisico) |
| RA3.f | Se ha verificado mediante un conjunto de datos de prueba que la implementación se ajusta al modelo. | [Tema 3](/tema3-diseno-fisico) |
| RA3.g | Se han utilizado asistentes y herramientas gráficas. | [Tema 3](/tema3-diseno-fisico) |
| RA3.h | Se ha utilizado el lenguaje de definición de datos. | [Tema 3](/tema3-diseno-fisico) |
| RA3.i | Se ha definido y documentado el diccionario de datos. | [Tema 3](/tema3-diseno-fisico) |

## RA4. Consulta la información almacenada manejando asistentes, herramientas gráficas y el lenguaje de manipulación de datos.

| CE | Criterio de evaluación | Tema |
|---|---|---|
| RA4.a | Se han identificado las herramientas y sentencias para realizar consultas. | [Tema 4](/tema4-consultas) |
| RA4.b | Se han realizado consultas simples sobre una tabla. | [Tema 4](/tema4-consultas) |
| RA4.c | Se han realizado consultas que generan valores de resumen. | [Tema 4](/tema4-consultas) |
| RA4.d | Se han realizado consultas sobre el contenido de varias tablas mediante composiciones internas. | [Tema 4](/tema4-consultas) |
| RA4.e | Se han realizado consultas sobre el contenido de varias tablas mediante composiciones externas. | [Tema 4](/tema4-consultas) |
| RA4.f | Se han realizado consultas con subconsultas. | [Tema 4](/tema4-consultas) |
| RA4.g | Se han valorado las ventajas e inconvenientes de las distintas opciones válidas para llevar a cabo una consulta determinada. | [Tema 4](/tema4-consultas) |

## RA5. Modifica la información almacenada utilizando asistentes, herramientas gráficas y el lenguaje de manipulación de datos.

| CE | Criterio de evaluación | Tema |
|---|---|---|
| RA5.a | Se han identificado las herramientas y sentencias para modificar el contenido de la base de datos. | [Tema 5](/tema5-modificacion) |
| RA5.b | Se han insertado, borrado y actualizado datos en las tablas. | [Tema 5](/tema5-modificacion) |
| RA5.c | Se ha incluido en una tabla la información resultante de la ejecución de una consulta. | [Tema 5](/tema5-modificacion) |
| RA5.d | Se han adoptado medidas para mantener la integridad y consistencia de la información. | [Tema 5](/tema5-modificacion) |
| RA5.e | Se han diseñado guiones de sentencias para llevar a cabo tareas complejas. | [Tema 5](/tema5-modificacion) |
| RA5.f | Se ha reconocido el funcionamiento de las transacciones. | [Tema 5](/tema5-modificacion) |
| RA5.g | Se han anulado parcial o totalmente los cambios producidos por una transacción. | [Tema 5](/tema5-modificacion) |
| RA5.h | Se han identificado los efectos de las distintas políticas de bloqueo de registros. | [Tema 5](/tema5-modificacion) |

## RA6. Ejecuta tareas de aseguramiento de la información, analizándolas y aplicando mecanismos de salvaguarda y transferencia.

| CE | Criterio de evaluación | Tema |
|---|---|---|
| RA6.a | Se han identificado herramientas gráficas y en línea de comandos para la administración de copias de seguridad. | [Tema 6](/tema6-aseguramiento) |
| RA6.b | Se han realizado copias de seguridad. | [Tema 6](/tema6-aseguramiento) |
| RA6.c | Se han restaurado copias de seguridad. | [Tema 6](/tema6-aseguramiento) |
| RA6.d | Se han identificado las herramientas para importar y exportar datos. | [Tema 6](/tema6-aseguramiento) |
| RA6.e | Se han exportado datos a diversos formatos. | [Tema 6](/tema6-aseguramiento) |
| RA6.f | Se han importado datos con distintos formatos. | [Tema 6](/tema6-aseguramiento) |
| RA6.g | Se ha interpretado correctamente la información suministrada por los mensajes de error y los ficheros de registro. | [Tema 6](/tema6-aseguramiento) |
| RA6.h | Se ha transferido información entre sistemas gestores. | [Tema 6](/tema6-aseguramiento) |

## Evidencias de aprendizaje

Para cada criterio de evaluación se recogen evidencias de distintos tipos:

| Tipo de evidencia | Ejemplos | CE en los que se usa sobre todo |
|---|---|---|
| Cuestionarios y preguntas de razonamiento | Autoevaluaciones de cada tema, preguntas de justificación | RA1 |
| Diagramas y documentos de diseño | Diagrama E/R, esquema relacional, informe de normalización | RA2 |
| Scripts SQL ejecutables | Scripts DDL, de consulta y de modificación | RA3, RA4, RA5 |
| Guiones PL/SQL con pruebas | Bloques con variables, control de flujo y excepciones con su batería de pruebas | RA5.e |
| Capturas y registros de ejecución | Planes de ejecución, sesiones concurrentes, ficheros `.log` de Data Pump y SQL*Loader | RA4.g, RA5.h, RA6.g |
| Entregas del proyecto EduGest | Una tarea de proyecto al final de cada tema | Todos |

## Fuente

- [Real Decreto 1629/2009, de 30 de octubre, por el que se establece el título de Técnico Superior en Administración de Sistemas Informáticos en Red](https://www.boe.es/eli/es/rd/2009/10/30/1629).
