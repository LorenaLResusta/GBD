---
title: "Resultados de aprendizaje y criterios de evaluación"
weight: 1
---

# Resultados de aprendizaje y criterios de evaluación

El módulo **0372. Gestión de bases de datos** (1º de Administración de Sistemas Informáticos en Red, ASIR) se rige por el **Real Decreto 1629/2009, de 30 de octubre**, que establece el título y sus enseñanzas mínimas. El módulo tiene **6 resultados de aprendizaje (RA)** con **47 criterios de evaluación (CE)**. Estos apuntes se imparten en **160 horas de aula** (5 por semana): el RD fija 105 horas como mínimo, y el currículo de la Comunitat Valenciana amplía el módulo hasta las 160.

> [!IMPORTANT]
> Un **resultado de aprendizaje** describe lo que sabrás hacer al terminar el módulo. Un **criterio de evaluación** es una evidencia concreta que demuestra que lo has conseguido. Cada unidad, práctica y ejercicio de estos apuntes indica qué CE trabaja.

## Horas y unidades por resultado de aprendizaje

Cada RA se corresponde con una o varias unidades consecutivas, de modo que se pueda evaluar un RA al terminar su bloque.

| RA | Resultado de aprendizaje | Unidades | Horas |
|---|---|---|:-:|
| **RA1** | Reconoce los elementos de las bases de datos analizando sus funciones y valorando la utilidad de los sistemas gestores. | [UD01](/ud01-introduccion) | 10 |
| **RA2** | Diseña modelos lógicos normalizados interpretando diagramas entidad/relación. | [UD02](/ud02-modelo-er), [UD03](/ud03-modelo-relacional), [UD04](/ud04-normalizacion) | 38 |
| **RA3** | Realiza el diseño físico de bases de datos utilizando asistentes, herramientas gráficas y el lenguaje de definición de datos. | [UD05](/ud05-ddl-dcl) | 22 |
| **RA4** | Consulta la información almacenada manejando asistentes, herramientas gráficas y el lenguaje de manipulación de datos. | [UD06](/ud06-consultas-basicas), [UD07](/ud07-consultas-avanzadas) | 32 |
| **RA5** | Modifica la información almacenada utilizando asistentes, herramientas gráficas y el lenguaje de manipulación de datos. | [UD08](/ud08-dml-transacciones), [UD09](/ud09-plsql) | 31 |
| **RA6** | Ejecuta tareas de aseguramiento de la información, analizándolas y aplicando mecanismos de salvaguarda y transferencia. | [UD10](/ud10-seguridad) | 12 |
| | *Ampliación: bases de datos NoSQL* | [UD11](/ud11-nosql) | 6 |
| | *Pruebas de evaluación (3 × 3 h)* | | 9 |
| | **Total** | | **160** |

```mermaid
flowchart LR
    RA1["RA1 · Elementos de las BD y SGBD"] --- UD01
    RA2["RA2 · Diseño lógico normalizado"] --- UD02 & UD03 & UD04
    RA3["RA3 · Diseño físico (DDL)"] --- UD05
    RA4["RA4 · Consultas"] --- UD06 & UD07
    RA5["RA5 · Modificación, transacciones y guiones"] --- UD08 & UD09
    RA6["RA6 · Seguridad: copias, importación y exportación"] --- UD10
```

> [!NOTE]
> Las unidades siguen el orden de los RA (UD01 es el RA1, UD02 a UD04 son el RA2, y así hasta el RA6). Los apuntes sobre **bases de datos NoSQL** (UD11) no corresponden a ningún RA del módulo: son una ampliación que se imparte al final del curso. También se marcan como *Ampliación* las actividades sobre protección de datos, bases de datos distribuidas, Big Data y privilegios (DCL), cuyo contenido no figura entre los CE del RD 1629/2009.

## Criterios de evaluación por resultado de aprendizaje

Texto literal de las enseñanzas mínimas. La última columna indica en qué unidades se trabaja cada criterio.

## RA1. Reconoce los elementos de las bases de datos analizando sus funciones y valorando la utilidad de los sistemas gestores.

| CE | Criterio de evaluación | Unidades |
|---|---|---|
| RA1.a | Se han analizado los distintos sistemas lógicos de almacenamiento y sus funciones. | [UD01](/ud01-introduccion) |
| RA1.b | Se han identificado los distintos tipos de bases de datos según el modelo de datos utilizado. | [UD01](/ud01-introduccion), [UD11](/ud11-nosql) |
| RA1.c | Se han identificado los distintos tipos de bases de datos en función de la ubicación de la información. | [UD01](/ud01-introduccion) |
| RA1.d | Se ha reconocido la utilidad de un sistema gestor de bases de datos. | [UD01](/ud01-introduccion) |
| RA1.e | Se ha descrito la función de cada uno de los elementos de un sistema gestor de bases de datos. | [UD01](/ud01-introduccion) |
| RA1.f | Se han clasificado los sistemas gestores de bases de datos. | [UD01](/ud01-introduccion) |

## RA2. Diseña modelos lógicos normalizados interpretando diagramas entidad/relación.

| CE | Criterio de evaluación | Unidades |
|---|---|---|
| RA2.a | Se ha identificado el significado de la simbología propia de los diagramas entidad/relación. | [UD02](/ud02-modelo-er) |
| RA2.b | Se han utilizado herramientas gráficas para representar el diseño lógico. | [UD02](/ud02-modelo-er), [UD03](/ud03-modelo-relacional), [UD05](/ud05-ddl-dcl) |
| RA2.c | Se han identificado las tablas del diseño lógico. | [UD03](/ud03-modelo-relacional), [UD04](/ud04-normalizacion) |
| RA2.d | Se han identificado los campos que forman parte de las tablas del diseño lógico. | [UD03](/ud03-modelo-relacional), [UD04](/ud04-normalizacion) |
| RA2.e | Se han identificado las relaciones entre las tablas del diseño lógico. | [UD02](/ud02-modelo-er), [UD03](/ud03-modelo-relacional) |
| RA2.f | Se han definido los campos clave. | [UD02](/ud02-modelo-er), [UD03](/ud03-modelo-relacional), [UD04](/ud04-normalizacion) |
| RA2.g | Se han aplicado las reglas de integridad. | [UD03](/ud03-modelo-relacional), [UD05](/ud05-ddl-dcl), [UD08](/ud08-dml-transacciones) |
| RA2.h | Se han aplicado las reglas de normalización hasta un nivel adecuado. | [UD04](/ud04-normalizacion) |
| RA2.i | Se han identificado y documentado las restricciones que no pueden plasmarse en el diseño lógico. | [UD01](/ud01-introduccion), [UD02](/ud02-modelo-er), [UD03](/ud03-modelo-relacional), [UD04](/ud04-normalizacion), [UD09](/ud09-plsql) |

## RA3. Realiza el diseño físico de bases de datos utilizando asistentes, herramientas gráficas y el lenguaje de definición de datos.

| CE | Criterio de evaluación | Unidades |
|---|---|---|
| RA3.a | Se han definido las estructuras físicas de almacenamiento. | [UD01](/ud01-introduccion), [UD05](/ud05-ddl-dcl) |
| RA3.b | Se han creado tablas. | [UD05](/ud05-ddl-dcl) |
| RA3.c | Se han seleccionado los tipos de datos adecuados. | [UD05](/ud05-ddl-dcl) |
| RA3.d | Se han definido los campos clave en las tablas. | [UD05](/ud05-ddl-dcl) |
| RA3.e | Se han implantado todas las restricciones reflejadas en el diseño lógico. | [UD03](/ud03-modelo-relacional), [UD05](/ud05-ddl-dcl) |
| RA3.f | Se ha verificado mediante un conjunto de datos de prueba que la implementación se ajusta al modelo. | [UD05](/ud05-ddl-dcl) |
| RA3.g | Se han utilizado asistentes y herramientas gráficas. | [UD01](/ud01-introduccion), [UD05](/ud05-ddl-dcl) |
| RA3.h | Se ha utilizado el lenguaje de definición de datos. | [UD01](/ud01-introduccion), [UD05](/ud05-ddl-dcl), [UD07](/ud07-consultas-avanzadas) |
| RA3.i | Se ha definido y documentado el diccionario de datos. | [UD05](/ud05-ddl-dcl) |

## RA4. Consulta la información almacenada manejando asistentes, herramientas gráficas y el lenguaje de manipulación de datos.

| CE | Criterio de evaluación | Unidades |
|---|---|---|
| RA4.a | Se han identificado las herramientas y sentencias para realizar consultas. | [UD06](/ud06-consultas-basicas), [UD07](/ud07-consultas-avanzadas) |
| RA4.b | Se han realizado consultas simples sobre una tabla. | [UD06](/ud06-consultas-basicas), [UD07](/ud07-consultas-avanzadas) |
| RA4.c | Se han realizado consultas que generan valores de resumen. | [UD07](/ud07-consultas-avanzadas) |
| RA4.d | Se han realizado consultas sobre el contenido de varias tablas mediante composiciones internas. | [UD07](/ud07-consultas-avanzadas) |
| RA4.e | Se han realizado consultas sobre el contenido de varias tablas mediante composiciones externas. | [UD07](/ud07-consultas-avanzadas) |
| RA4.f | Se han realizado consultas con subconsultas. | [UD07](/ud07-consultas-avanzadas) |
| RA4.g | Se han valorado las ventajas e inconvenientes de las distintas opciones válidas para llevar a cabo una consulta determinada. | [UD07](/ud07-consultas-avanzadas) |

## RA5. Modifica la información almacenada utilizando asistentes, herramientas gráficas y el lenguaje de manipulación de datos.

| CE | Criterio de evaluación | Unidades |
|---|---|---|
| RA5.a | Se han identificado las herramientas y sentencias para modificar el contenido de la base de datos. | [UD08](/ud08-dml-transacciones) |
| RA5.b | Se han insertado, borrado y actualizado datos en las tablas. | [UD08](/ud08-dml-transacciones) |
| RA5.c | Se ha incluido en una tabla la información resultante de la ejecución de una consulta. | [UD08](/ud08-dml-transacciones) |
| RA5.d | Se han adoptado medidas para mantener la integridad y consistencia de la información. | [UD08](/ud08-dml-transacciones), [UD09](/ud09-plsql) |
| RA5.e | Se han diseñado guiones de sentencias para llevar a cabo tareas complejas. | [UD06](/ud06-consultas-basicas), [UD08](/ud08-dml-transacciones), [UD09](/ud09-plsql) |
| RA5.f | Se ha reconocido el funcionamiento de las transacciones. | [UD08](/ud08-dml-transacciones) |
| RA5.g | Se han anulado parcial o totalmente los cambios producidos por una transacción. | [UD08](/ud08-dml-transacciones) |
| RA5.h | Se han identificado los efectos de las distintas políticas de bloqueo de registros. | [UD08](/ud08-dml-transacciones) |

## RA6. Ejecuta tareas de aseguramiento de la información, analizándolas y aplicando mecanismos de salvaguarda y transferencia.

| CE | Criterio de evaluación | Unidades |
|---|---|---|
| RA6.a | Se han identificado herramientas gráficas y en línea de comandos para la administración de copias de seguridad. | [UD10](/ud10-seguridad) |
| RA6.b | Se han realizado copias de seguridad. | [UD10](/ud10-seguridad) |
| RA6.c | Se han restaurado copias de seguridad. | [UD10](/ud10-seguridad) |
| RA6.d | Se han identificado las herramientas para importar y exportar datos. | [UD10](/ud10-seguridad) |
| RA6.e | Se han exportado datos a diversos formatos. | [UD10](/ud10-seguridad) |
| RA6.f | Se han importado datos con distintos formatos. | [UD10](/ud10-seguridad) |
| RA6.g | Se ha interpretado correctamente la información suministrada por los mensajes de error y los ficheros de registro. | [UD10](/ud10-seguridad) |
| RA6.h | Se ha transferido información entre sistemas gestores. | [UD10](/ud10-seguridad) |

## Evidencias de aprendizaje

Para cada criterio de evaluación se recogen evidencias de distintos tipos:

| Tipo de evidencia | Ejemplos | CE en los que se usa sobre todo |
|---|---|---|
| Cuestionarios y preguntas de razonamiento | Autoevaluaciones de cada unidad, preguntas de justificación | RA1 |
| Diagramas y documentos de diseño | Diagrama E/R, esquema relacional, informe de normalización | RA2 |
| Scripts SQL ejecutables | Scripts DDL y DCL, de consulta y de modificación | RA3, RA4, RA5 |
| Código PL/SQL con pruebas | Procedimientos, funciones y triggers con su batería de pruebas | RA5.e |
| Capturas y registros de ejecución | Planes de ejecución, sesiones concurrentes, ficheros `.log` de Data Pump y SQL*Loader | RA4.g, RA5.h, RA6.g |
| Entregas del proyecto EduGest | Una tarea de proyecto al final de cada unidad | Todos |

## Fuente

- [Real Decreto 1629/2009, de 30 de octubre, por el que se establece el título de Técnico Superior en Administración de Sistemas Informáticos en Red](https://www.boe.es/eli/es/rd/2009/10/30/1629).
