---
title: "Bases de datos NoSQL - Prácticas"
weight: 2
bookToc: true
---

# UD10 · Prácticas

{{< ra "RA7:a,b,c,d,e" "RA1:b" >}}

| Práctica | Tipo | Nivel | CE principales |
|---|---|---|---|
| [10.1 Puesta en marcha de MongoDB](#práctica-101--puesta-en-marcha-de-mongodb) | Guiada | ●○○ | RA7.c, RA7.e |
| [10.2 CRUD sobre los expedientes](#práctica-102--crud-sobre-los-expedientes) | Guiada | ●○○ | RA7.d, RA7.e |
| [10.3 Consultas con operadores, subdocumentos y arrays](#práctica-103--consultas-con-operadores-subdocumentos-y-arrays) | Autónoma | ●●○ | RA7.d, RA7.e |
| [10.4 Agregaciones: el mismo informe en SQL y en MongoDB](#práctica-104--agregaciones-el-mismo-informe-en-sql-y-en-mongodb) | Guiada | ●●○ | RA7.d, RA7.e |
| [10.5 Modelado documental de un catálogo](#práctica-105--modelado-documental-de-un-catálogo) | Autónoma | ●●● | RA7.c, RA7.d |
| [10.6 Otros modelos: clave-valor y grafos](#práctica-106--otros-modelos-clave-valor-y-grafos) | Autónoma | ●●○ | RA7.a, RA7.b |
| [10.7 Reto: ¿relacional o NoSQL?](#práctica-107--reto-relacional-o-nosql) | Reto | ●●● | RA7.a, RA7.b, RA1.b |
| [Proyecto EduGest · UD10](#proyecto-edugest--ud10-el-expediente-documental) | Proyecto | ●●● | RA7 completo |

> [!IMPORTANT]
> Usaremos **MongoDB Community Server 8.0** en Docker, `mongosh` y **MongoDB Compass**. Los resultados indicados suponen que has cargado [edugest_mongo.js](recursos/nosql/edugest_mongo.js) y no has modificado los datos (repite la carga antes de cada práctica: el script borra y recrea las colecciones).

---

## Práctica 10.1 · Puesta en marcha de MongoDB

{{< practica num="10.1" tipo="Guiada" duracion="1 sesión" nivel="1" ra="RA7: c, e" sgbd="MongoDB 8.0 · Docker · mongosh · Compass" entrega="Capturas + respuestas" >}}

#### Objetivo

Instalar el servidor, conectar con las dos herramientas cliente y reconocer los elementos de una base de datos documental.

#### Desarrollo

{{% steps %}}

1. **Arranca el servidor** (si no lo hiciste en la guía del entorno):

    ```bash
    docker run -d --name mongo8 -p 27017:27017 -v mongo-data:/data/db mongodb/mongodb-community-server:8.0-ubi9
    docker exec -it mongo8 mongosh --eval "db.version()"
    ```

2. **Carga los datos de EduGest**:

    ```bash
    docker exec -i mongo8 mongosh < edugest_mongo.js
    # ciclos: 4 · profesores: 12 · expedientes: 32
    ```

3. **Explora con `mongosh`**:

    ```javascript
    show dbs
    use edugest
    show collections
    db.expedientes.findOne({ _id: 1 })
    db.expedientes.findOne({ _id: 30 })
    db.ciclos.findOne({ _id: "SMR" })
    db.expedientes.stats().size          // tamaño en bytes
    db.expedientes.getIndexes()
    ```

4. **Explora con Compass.** Conecta con `mongodb://localhost:27017`. Abre `edugest.expedientes`, cambia entre las vistas *Lista*, *JSON* y *Tabla* y usa la pestaña **Schema** (*Analyze*) para ver qué campos tiene la colección y en qué porcentaje de documentos aparece cada uno.

{{% /steps %}}

#### Preguntas

1. Compara los documentos con `_id` 1 y 30. ¿Qué campos tiene uno y no el otro? ¿Cómo se representaría esa diferencia en Oracle?
2. ¿Qué índices tiene la colección? ¿Quién los ha creado?
3. Según la pestaña *Schema* de Compass, ¿en qué porcentaje de expedientes aparece el campo `dni`? ¿Y `grupo`?
4. ¿De qué tipo BSON es `fechaNacimiento`? ¿Y `nota`?

#### Comprobación

{{% comprobacion %}}
- [ ] `db.expedientes.countDocuments()` devuelve 32.
- [ ] Identificas que el único índice es el de `_id`, creado automáticamente.
- [ ] `dni` aparece en el 87,5 % de los documentos (28 de 32) y `grupo` en el 90,6 % (29 de 32).
{{% /comprobacion %}}

---

## Práctica 10.2 · CRUD sobre los expedientes

{{< practica num="10.2" tipo="Guiada" duracion="2 sesiones" nivel="1" ra="RA7: d, e" sgbd="MongoDB 8.0 · mongosh" entrega="p10_2.mongodb.js" >}}

#### Objetivo

Realizar las cuatro operaciones básicas sobre documentos con subdocumentos y arrays, y comparar cada una con su equivalente SQL.

#### Desarrollo

{{% steps %}}

1. **Crear.** Inserta a Marina López (consulta el ejemplo de la [teoría](/ud10-nosql/ud10-teoria#51-crear-insertone-e-insertmany)) y a dos alumnos más con `insertMany`. Uno de ellos **sin** `_id`: ¿qué valor le asigna MongoDB?

2. **Leer.** Escribe y ejecuta:

    ```javascript
    db.expedientes.find({ "grupo.codigo": "1DAW" }, { _id: 0, nombre: 1, apellidos: 1 }).sort({ apellidos: 1 })
    db.expedientes.countDocuments({ localidad: "Alicante" })          // 13 (sin contar los nuevos)
    db.expedientes.find({}, { nombre: 1, fechaNacimiento: 1 }).sort({ fechaNacimiento: 1 }).limit(3)
    ```

3. **Actualizar.**

    ```javascript
    // a) Añadir un teléfono a quien no tiene (Paula, _id 4)
    db.expedientes.updateOne({ _id: 4 }, { $set: { "contacto.telefono": "612345678" } })

    // b) Marcar a todo 2DAW como «en prácticas en empresa»
    db.expedientes.updateMany({ "grupo.codigo": "2DAW" }, { $set: { enFCT: true } })   // 5

    // c) Corregir la nota de Bases de datos de Adrián (_id 1) con el operador posicional
    db.expedientes.updateOne(
      { _id: 1, "matriculas.modulo.codigo": "0484" },
      { $set: { "matriculas.$.nota": 5 } })

    // d) Añadir una falta a esa misma matrícula
    db.expedientes.updateOne(
      { _id: 1, "matriculas.modulo.codigo": "0484" },
      { $push: { "matriculas.$.faltas": { fecha: ISODate("2026-05-20"), horas: 2, justificada: false } } })

    // e) Quitar el campo enFCT de todos
    db.expedientes.updateMany({}, { $unset: { enFCT: "" } })
    ```

4. **Comprueba** cada cambio con `findOne` y una proyección adecuada, por ejemplo:

    ```javascript
    db.expedientes.findOne({ _id: 1 }, { "matriculas.modulo.codigo": 1, "matriculas.nota": 1 })
    ```

5. **Eliminar.** Borra a los alumnos que has insertado en el paso 1 con **una sola** orden. Pista: `{ _id: { $in: [...] } }` no sirve para el que no tenía `_id`. Usa el NIA.

6. **Equivalencias.** Escribe, para cada orden de los pasos 2, 3a, 3b y 5, la sentencia SQL equivalente en EduGest-Oracle. ¿Cuál de las operaciones 3c y 3d necesita **otra tabla** en SQL?

{{% /steps %}}

#### Comprobación

{{% comprobacion %}}
- [ ] El alumno insertado sin `_id` recibe un `ObjectId("...")`.
- [ ] 3b informa `matchedCount: 5, modifiedCount: 5` y 3e `modifiedCount: 5`.
- [ ] Tras el paso 3c, la matrícula de 0484 de Adrián tiene `nota: 5` y el resto de sus matrículas no ha cambiado.
- [ ] Al final, `countDocuments()` vuelve a ser 32.
{{% /comprobacion %}}

#### Errores habituales

| Error | Causa |
|---|---|
| `MongoServerError: E11000 duplicate key error` | Insertas un `_id` que ya existe |
| `Update document requires atomic operators` | Has olvidado `$set` en un `updateOne` |
| La actualización «no hace nada» (`matchedCount: 0`) | El filtro no coincide: revisa mayúsculas, tipos (`"1"` no es `1`) y la notación de punto |

---

## Práctica 10.3 · Consultas con operadores, subdocumentos y arrays

{{< practica num="10.3" tipo="Autónoma" duracion="2 sesiones" nivel="2" ra="RA7: d, e" sgbd="MongoDB 8.0 · mongosh o Compass" entrega="p10_3.mongodb.js" >}}

#### Enunciado

Resuelve cada consulta. Comprueba que obtienes el resultado indicado.

| # | Consulta | Resultado esperado |
|---|---|---|
| N1 | ¿Cuántos alumnos son de un grupo del ciclo DAM? | 13 |
| N2 | Nombre, apellidos y fecha de nacimiento del alumnado nacido antes de 2005, del mayor al menor | 10 documentos; el primero, Sara Amorós Guillem |
| N3 | Alumnado de Elche o de El Campello (usa `$in`) | 6 |
| N4 | `_id` del alumnado **sin teléfono** | 4, 10, 16, 22, 28 |
| N5 | Alumnado con **alguna** matrícula sin nota | 3, 8, 11, 17, 23, 28 |
| N6 | Alumnado con algún 10 | Aitana (_id 29) |
| N7 | Alumnado con **más de 5** matrículas (usa `$expr` y `$size`) | Nerea, Hugo y Lucía |
| N8 | Alumnado cuyo primer apellido empieza por «Ib» (usa `$regex`) | 4 documentos |
| N9 | Profesorado que imparte algún módulo en 2DAM (colección `profesores`) | Javier, Lucía, Andrés y Raúl |
| N10 | Profesorado que **no** imparte clase | `_id` 108 a 112 |
| N11 | Ciclos con algún módulo de más de 200 horas | DAM, DAW y ASIR |
| N12 | Los tres alumnos más jóvenes | Manuel, Alba y Víctor |

{{% details title="Pista: la trampa de N5" %}}
Prueba primero `db.expedientes.find({ "matriculas.nota": { $exists: false } })`. Devuelve los `_id` 30, 31 y 32: los documentos en los que **ningún** elemento del array tiene `nota` (¡porque su array está vacío!). Para «**algún** elemento sin nota» necesitas `$elemMatch`:

```javascript
db.expedientes.find({ matriculas: { $elemMatch: { nota: { $exists: false } } } }, { nombre: 1 })
```
{{% /details %}}

{{< solucion id="ud10-001" title="Solución de N7 y N9" />}}

#### Comprobación

{{% comprobacion %}}
- [ ] Las doce consultas dan el resultado esperado.
- [ ] Explicas con tus palabras la diferencia entre N5 con y sin `$elemMatch`.
- [ ] Para N4 y N10 explicas qué equivalente tendrían en SQL (`IS NULL`, `NOT EXISTS`/`LEFT JOIN`).
{{% /comprobacion %}}

---

## Práctica 10.4 · Agregaciones: el mismo informe en SQL y en MongoDB

{{< practica num="10.4" tipo="Guiada" duracion="2 sesiones" nivel="2" ra="RA7: d, e" sgbd="MongoDB 8.0 · Compass (Aggregations) · Oracle 26ai" entrega="p10_4.mongodb.js + p10_4.sql + comparación" >}}

#### Objetivo

Construir pipelines de agregación etapa a etapa y comparar su resultado y su legibilidad con la consulta SQL equivalente.

#### Desarrollo

{{% steps %}}

1. **Construye el pipeline en Compass.** Abre `expedientes` → pestaña *Aggregations*. Añade las etapas una a una y observa la vista previa de cada una:

    ```javascript
    [
      { $group: { _id: "$localidad", alumnos: { $sum: 1 } } },
      { $sort: { alumnos: -1, _id: 1 } }
    ]
    ```

    Debe coincidir con la práctica 7.1 (Alicante 13, Mutxamel 6...). Exporta el pipeline a código con el botón *Export to language*.

2. **Media de Bases de datos por ciclo** (`$unwind` + `$match` después del `$unwind`):

    ```javascript
    db.expedientes.aggregate([
      { $unwind: "$matriculas" },
      { $match: { "matriculas.modulo.codigo": "0484" } },
      { $group: { _id: "$matriculas.modulo.ciclo",
                  calificadas: { $sum: { $cond: [ { $eq: [ { $type: "$matriculas.nota" }, "missing" ] }, 0, 1 ] } },
                  media: { $avg: "$matriculas.nota" } } },
      { $project: { calificadas: 1, media: { $round: ["$media", 2] } } },
      { $sort: { _id: 1 } }
    ])
    ```

    ```text
    [ { _id: 'DAM', calificadas: 7, media: 5.93 },
      { _id: 'DAW', calificadas: 6, media: 5.92 } ]
    ```

3. **Las cinco personas con más horas de falta** (doble `$unwind`):

    ```javascript
    db.expedientes.aggregate([
      { $unwind: "$matriculas" },
      { $unwind: "$matriculas.faltas" },
      { $group: { _id: "$_id",
                  alumno: { $first: { $concat: ["$nombre", " ", "$apellidos"] } },
                  horas: { $sum: "$matriculas.faltas.horas" } } },
      { $sort: { horas: -1, _id: 1 } },
      { $limit: 5 }
    ])
    ```

    | _id | alumno | horas |
    |---|---|---|
    | 1 | Adrián Ferri Baeza | 8 |
    | 10 | Nerea Cerdá Tomás | 8 |
    | 9 | Martina Alemany Vidal | 7 |
    | 14 | Carla Valero Cerdá | 6 |
    | 7 | Valeria Quiles Marco | 5 |

4. **Matrículas suspensas por grupo.** Escríbelo tú. Resultado: 1ASIR 3, 1DAM 7, 1DAW 5, 2DAM 8, 2DAW 4.

5. **Alumnado por nombre de ciclo con `$lookup`** sobre la colección `ciclos`. Resultado: DAM 13, DAW 11, ASIR 5.

6. **Escribe en SQL (Oracle)** las consultas de los pasos 2 a 5 y compara: número de líneas, legibilidad y qué te resulta más natural en cada caso.

{{% /steps %}}

#### Comprobación

{{% comprobacion %}}
- [ ] Los cinco pipelines dan los resultados indicados, y las consultas SQL dan los mismos.
- [ ] Sabes explicar por qué el `$match` del paso 2 va **después** del `$unwind`.
- [ ] En el paso 3 explicas por qué hace falta `$sort` por `_id` además de por `horas` (hay un empate en el quinto puesto).

> [!WARNING]
> `$round` de MongoDB redondea los valores que están **exactamente** a mitad de camino hacia el número **par** (*round half to even*): `$round: [2.345, 2]` da 2.34. El `ROUND` de Oracle redondea hacia arriba (2.35). Con los datos de EduGest no hay empates de este tipo, pero tenlo en cuenta al comparar informes.
{{% /comprobacion %}}

---

## Práctica 10.5 · Modelado documental de un catálogo

{{< practica num="10.5" tipo="Autónoma" duracion="2 sesiones" nivel="3" ra="RA7: c, d" sgbd="MongoDB 8.0" entrega="Documento de diseño + script con validador, datos y consultas" >}}

#### Objetivo

Diseñar una base de datos documental a partir de los **patrones de consulta**, justificando qué se incrusta y qué se referencia.

#### Contexto

Una tienda online de material informático quiere migrar su catálogo a MongoDB. Los productos son muy diferentes entre sí:

- Portátiles: procesador, RAM, almacenamiento, pantalla, peso.
- Ratones: conexión (USB/Bluetooth), DPI, si es inalámbrico.
- Monitores: pulgadas, resolución, frecuencia, paneles.
- Todos tienen: referencia, nombre, marca, precio, stock y una o varias categorías.
- Los clientes dejan **opiniones** (puntuación de 1 a 5, texto, fecha). Algunos productos tienen miles.

Consultas más frecuentes:

1. Ficha del producto con sus características y las **5 opiniones más recientes**.
2. Listado por categoría con filtros por precio y marca.
3. Puntuación media de cada producto.

#### Enunciado

1. Diseña las colecciones y la estructura de los documentos. Justifica cada decisión de incrustar o referenciar en función de las consultas.
2. Explica cómo resolverías la «media de puntuación» sin recalcularla en cada consulta (pista: patrón de **campo calculado** actualizado en cada nueva opinión).
3. Crea la colección `productos` con un **validador** `$jsonSchema` que exija los campos comunes, `precio >= 0` y `stock` entero no negativo.
4. Inserta al menos **10 productos** de tres tipos distintos y 20 opiniones.
5. Escribe las tres consultas frecuentes y crea los índices que las aceleran. Comprueba con `explain("executionStats")` que usan `IXSCAN`.
6. Compara con un diseño relacional: ¿cuántas tablas harían falta para las características variables? (Piensa en el patrón *entidad-atributo-valor* o en una tabla por tipo de producto.)

#### Comprobación

{{% comprobacion %}}
- [ ] Las opiniones **no** están incrustadas sin límite en el producto (problema de los 16 MB); como mucho, las 5 últimas.
- [ ] El validador rechaza un producto con precio negativo.
- [ ] Las consultas usan índices.

{{% details title="Pista: patrón «subconjunto»" %}}
Guarda todas las opiniones en una colección `opiniones` (con la referencia del producto) y, además, incrusta en el producto un array `ultimasOpiniones` con las 5 más recientes. Al añadir una opinión: insértala en `opiniones` y actualiza el producto con `$push` + `$each` + `$sort` + `$slice: 5`, y `$inc` del número de opiniones y de la suma de puntuaciones.
{{% /details %}}
{{% /comprobacion %}}

---

## Práctica 10.6 · Otros modelos: clave-valor y grafos

{{< practica num="10.6" tipo="Autónoma" duracion="2 sesiones" nivel="2" ra="RA7: a, b" sgbd="Redis/Valkey (Docker) · Neo4j (Docker o Sandbox)" entrega="Informe con capturas" >}}

#### Objetivo

Experimentar brevemente con otros dos tipos de bases de datos NoSQL para evaluar sus puntos fuertes y sus limitaciones.

#### Parte A · Clave-valor con Valkey (compatible con Redis)

```bash
docker run -d --name valkey -p 6379:6379 valkey/valkey:8
docker exec -it valkey valkey-cli
```

```text
SET sesion:abc123 "id_alumno=1;rol=ALUMNO"
EXPIRE sesion:abc123 1800        # caduca en 30 minutos
TTL sesion:abc123
INCR visitas:portal              # contador atómico
HSET alumno:1 nombre "Adrián" grupo "1DAM"
HGETALL alumno:1
KEYS alumno:*                    # ¡solo en pruebas! en producción usa SCAN
```

Responde: ¿cómo buscarías «todos los alumnos de 1DAM»? ¿Qué tendrías que haber guardado para poder hacerlo?

#### Parte B · Grafos con Neo4j

Crea un pequeño grafo de EduGest (5 alumnos, 3 módulos, 2 profesores) y resuelve con Cypher:

```text
CREATE (a:Alumno {id:1, nombre:'Adrián'}), (b:Alumno {id:2, nombre:'Rubén'}),
       (bd:Modulo {codigo:'0484'}), (pr:Modulo {codigo:'0485'}),
       (marta:Profesor {nombre:'Marta'}), (lucia:Profesor {nombre:'Lucía'}),
       (a)-[:MATRICULADO {nota:4.75}]->(bd), (b)-[:MATRICULADO {nota:4.75}]->(bd),
       (a)-[:MATRICULADO {nota:7.25}]->(pr),
       (marta)-[:IMPARTE]->(bd), (lucia)-[:IMPARTE]->(pr);

MATCH (a:Alumno {nombre:'Adrián'})-[:MATRICULADO]->(m)<-[:IMPARTE]-(p) RETURN m.codigo, p.nombre;
MATCH (a:Alumno)-[:MATRICULADO]->(m)<-[:MATRICULADO]-(c:Alumno) WHERE a.nombre = 'Adrián' RETURN DISTINCT c.nombre;
```

#### Conclusión

Completa una tabla con los cuatro modelos (relacional, documental, clave-valor y grafos) y, para cada uno: estructura, lenguaje, una consulta en la que destaca y una consulta en la que sufre.

---

## Práctica 10.7 · Reto: ¿relacional o NoSQL?

{{< practica num="10.7" tipo="Reto" duracion="1 sesión + defensa" nivel="3" ra="RA7: a, b · RA1: b" sgbd="—" entrega="Informe de decisión (1 página por caso) + defensa oral" >}}

#### Enunciado

Para cada caso, recomienda el modelo (o la combinación de modelos) y justifícalo con argumentos de **estructura de los datos**, **consultas**, **consistencia**, **escalabilidad** y **coste**. Indica también qué **perderías** con la alternativa descartada.

1. **Secretaría virtual de la Conselleria:** matrículas de todos los institutos de la Comunitat, con actas oficiales y certificados.
2. **App de apuntes colaborativos** del alumnado: cada apunte tiene texto, imágenes, etiquetas variables, comentarios y versiones.
3. **Sensores de calidad del aire** en todas las aulas del centro: CO₂, temperatura y humedad cada 30 segundos, consultados por intervalos de tiempo.
4. **Recomendador de ciclos formativos**: «el alumnado que estudió lo mismo que tú y tiene tus intereses eligió...».
5. **Carrito de la compra** de la tienda de la práctica 10.5.

#### Comprobación

{{% comprobacion %}}
- [ ] Ninguna recomendación se basa en «es más moderno» o «es más rápido» sin explicar por qué.
- [ ] Al menos un caso propone **persistencia políglota** (dos modelos a la vez) y explica cómo se sincronizan.
- [ ] Usas la tabla de decisión de la teoría como punto de partida, no como regla automática.
{{% /comprobacion %}}

---

## Proyecto EduGest · UD10: el expediente documental

{{< practica num="EduGest-10" tipo="Proyecto" duracion="Trabajo transversal (2 semanas)" nivel="3" ra="RA7: a-e" sgbd="Oracle 26ai · MongoDB 8.0" entrega="edugest/10_nosql/ + docs/10-nosql.md" >}}

#### Enunciado

1. **Exportación.** Escribe una consulta en Oracle que genere, para cada alumno, su expediente en **JSON** usando las funciones SQL/JSON de Oracle (`JSON_OBJECT`, `JSON_ARRAYAGG`). Exporta el resultado a un fichero e impórtalo en MongoDB (Compass → *Add data* → *Import JSON*, o `mongoimport`).

    ```sql
    SELECT JSON_OBJECT(
             '_id'       VALUE a.id_alumno,
             'nia'       VALUE a.nia,
             'nombre'    VALUE a.nombre,
             'matriculas' VALUE (
                 SELECT JSON_ARRAYAGG(JSON_OBJECT('curso' VALUE m.curso_academico,
                                                  'modulo' VALUE mo.codigo,
                                                  'nota' VALUE m.nota_final ABSENT ON NULL))
                 FROM matricula m JOIN modulo mo ON mo.id_modulo = m.id_modulo
                 WHERE m.id_alumno = a.id_alumno)
             ABSENT ON NULL RETURNING CLOB) AS expediente
    FROM alumno a;
    ```

2. **Validación.** Añade a la colección un validador `$jsonSchema` coherente con las restricciones de Oracle (NIA de 8 dígitos, nota entre 0 y 10, convocatoria de 1 a 4).
3. **Consultas.** Reescribe en MongoDB cinco de tus informes de la UD07 y compara resultados.
4. **Índices.** Crea los índices necesarios y muestra los planes (`explain`).
5. **Informe final** (`10-nosql.md`): ventajas e inconvenientes del modelo documental para EduGest, qué partes del sistema tendrían sentido en MongoDB y cuáles deben seguir en Oracle, y cómo se mantendrían sincronizadas.

#### Comprobación

{{% comprobacion %}}
- [ ] Los 32 expedientes importados coinciden con los datos de Oracle.
- [ ] El validador rechaza una nota de 11.
- [ ] Las cinco consultas dan los mismos resultados en los dos sistemas.
- [ ] El informe final justifica las decisiones con criterios técnicos.

> [!TIP]
> Oracle 23ai y 26ai incluyen **JSON Relational Duality Views**, que permiten consultar y modificar datos relacionales **como si fueran documentos JSON**, con todas las garantías de integridad del modelo relacional. Investiga esta característica: es un buen ejemplo de que la frontera entre SQL y NoSQL es cada vez más difusa.
{{% /comprobacion %}}
