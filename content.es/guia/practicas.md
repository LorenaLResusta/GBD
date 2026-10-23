---
title: "Cómo son las prácticas"
weight: 4
---

# Cómo son las prácticas

Cada unidad tiene una página de **prácticas**. Las prácticas son la parte principal del módulo: los criterios de evaluación de RA2 a RA7 se demuestran **haciendo**, no memorizando.

## 1. Tipos de práctica

| Tipo | Qué es | Cómo se trabaja |
|---|---|---|
| **Guiada** | Se presenta el procedimiento paso a paso. Su objetivo es aprender la técnica. | En clase. Se comprueba al final de la sesión con la lista de comprobación. |
| **Autónoma** | Se plantea un problema parecido sin el procedimiento. Su objetivo es aplicar la técnica. | Individual. Se entrega y se evalúa. |
| **Reto** | Un problema abierto o con una dificultad extra. Exige analizar y decidir. | Opcional o para subir nota. Se defiende oralmente. |
| **Proyecto** | La tarea de EduGest de la unidad. | Individual o por parejas. Forma parte del proyecto final. |

La dificultad se indica con tres puntos: ●○○ básico, ●●○ intermedio y ●●● avanzado.

## 2. Estructura de una práctica

Todas las prácticas siguen el mismo esquema. Así sabes qué se espera en cada apartado:

{{< practica num="X.Y" tipo="Guiada" duracion="Tiempo orientativo" nivel="2" ra="RAx: criterios" sgbd="Software y versión" entrega="Qué hay que entregar" >}}

1. **Objetivo.** Qué competencia o resultado se pretende desarrollar.
2. **Contexto.** La situación profesional que se plantea.
3. **Requisitos.** Software, versiones y conocimientos previos.
4. **Enunciado.** El problema que debes resolver.
5. **Desarrollo.** El procedimiento guiado (solo en prácticas guiadas).
6. **Comprobación.** Pruebas que permiten verificar que el resultado es correcto.
7. **Errores habituales.** Problemas frecuentes y cómo diagnosticarlos.
8. **Ampliación.** Una modificación que te obliga a aplicar lo aprendido por tu cuenta.

> [!TIP]
> Lee la **Comprobación** antes de empezar. Te dice exactamente qué resultado tienes que obtener y te ahorra tiempo.

## 3. Organización del repositorio

Crea un repositorio Git privado para el módulo con esta estructura:

```text
bbdd-<tu-usuario>/
├── README.md                 # nombre, grupo y estado de cada práctica
├── ud01/
│   └── p1.1-analisis.md
├── ud02/
│   ├── p2.1-biblioteca.drawio
│   └── p2.1-biblioteca.png
├── ud05/
│   ├── p5.1-tienda.sql
│   └── evidencias/p5.1-salida.txt
├── ...
└── edugest/                  # el proyecto transversal
    ├── 01_esquema.sql
    ├── 02_datos.sql
    ├── 03_seguridad.sql
    └── docs/diseno.md
```

## 4. Normas para los scripts SQL

Un script entregado debe poder **ejecutarse de principio a fin** en una base de datos limpia sin errores inesperados. Por eso:

```sql
-- =============================================================
-- Práctica 5.2 · Tienda online · Script de creación
-- Autor/a: Nombre Apellidos (1DAM)
-- SGBD: Oracle AI Database 26ai Free 23.26
-- Fecha: 2026-11-10
-- =============================================================

-- 1. Limpieza para poder relanzar el script
DROP TABLE linea_pedido CASCADE CONSTRAINTS PURGE;

-- 2. Creación de tablas (cada restricción con nombre)
CREATE TABLE cliente (
    id_cliente NUMBER(6) CONSTRAINT pk_cliente PRIMARY KEY
    -- ...
);

-- 3. Comprobaciones
SELECT constraint_name, constraint_type FROM user_constraints WHERE table_name = 'CLIENTE';
```

- Una sentencia por bloque, terminada en `;`.
- Comentarios que expliquen el **porqué**, no solo el qué.
- Restricciones con **nombre** (`pk_`, `fk_`, `uq_`, `ck_`, `nn_`).
- Identificadores en minúsculas y con guion bajo (`fecha_nacimiento`), sin tildes ni espacios.
- Las evidencias de ejecución se guardan con `SPOOL` o con capturas en la carpeta `evidencias/`.

## 5. Autoevaluación de las prácticas

Las prácticas autónomas y las de proyecto se autoevalúan con esta rúbrica común. Cada práctica indica qué criterios de evaluación (CE) trabaja.

| Aspecto | Excelente (4) | Adecuado (3) | Mejorable (2) | Insuficiente (1) |
|---|---|---|---|---|
| **Resultado** | Funciona y supera todas las comprobaciones | Errores menores que no afectan al resultado | Funciona parcialmente | No funciona o no se ejecuta |
| **Diseño y decisiones** | Justifica cada decisión y valora alternativas | Decisiones correctas con poca justificación | Decisiones discutibles sin justificar | Decisiones incorrectas |
| **Calidad del código o del diagrama** | Legible, comentado, con nombres coherentes | Legible con pocos comentarios | Difícil de seguir | Desordenado |
| **Comprobación y evidencias** | Pruebas propias además de las pedidas | Incluye las comprobaciones pedidas | Comprobaciones incompletas | Sin evidencias |

> [!WARNING]
> **Integridad académica.** Puedes consultar documentación, foros y asistentes de IA, pero debes **entender y poder defender** todo lo que entregas. En la defensa oral se te puede pedir que modifiques tu solución en directo. Indica en el `README.md` las fuentes y herramientas que hayas usado.
