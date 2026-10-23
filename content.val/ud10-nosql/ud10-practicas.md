---
title: "Bases de dades NoSQL - Pràctiques"
weight: 2
bookToc: true
---

# UD10 · Pràctiques

{{< ra "RA7:a,b,c,d,e" "RA1:b" >}}

| Pràctica | Tipus | Nivell | CE principals |
|---|---|---|---|
| [10.1 Posada en marxa de MongoDB](#pràctica-101--posada-en-marxa-de-mongodb) | Guiada | ●○○ | RA7.c, RA7.e |
| [10.2 CRUD sobre els expedients](#pràctica-102--crud-sobre-els-expedients) | Guiada | ●○○ | RA7.d, RA7.e |
| [10.3 Consultes amb operadors, subdocuments i arrays](#pràctica-103--consultes-amb-operadors-subdocuments-i-arrays) | Autònoma | ●●○ | RA7.d, RA7.e |
| [10.4 Agregacions: el mateix informe en SQL i en MongoDB](#pràctica-104--agregacions-el-mateix-informe-en-sql-i-en-mongodb) | Guiada | ●●○ | RA7.d, RA7.e |
| [10.5 Modelatge documental d'un catàleg](#pràctica-105--modelatge-documental-dun-catàleg) | Autònoma | ●●● | RA7.c, RA7.d |
| [10.6 Altres models: clau-valor i grafs](#pràctica-106--altres-models-clau-valor-i-grafs) | Autònoma | ●●○ | RA7.a, RA7.b |
| [10.7 Repte: relacional o NoSQL?](#pràctica-107--repte-relacional-o-nosql) | Repte | ●●● | RA7.a, RA7.b, RA1.b |
| [Projecte EduGest · UD10](#projecte-edugest--ud10-lexpedient-documental) | Projecte | ●●● | RA7 complet |

> [!IMPORTANT]
> Usarem **MongoDB Community Server 8.0** en Docker, `mongosh` i **MongoDB Compass**. Els resultats indicats suposen que has carregat [edugest_mongo.js](recursos/nosql/edugest_mongo.js) i no has modificat les dades (repetix la càrrega abans de cada pràctica: l'script esborra i recrea les col·leccions).

---

## Pràctica 10.1 · Posada en marxa de MongoDB

{{< practica num="10.1" tipo="Guiada" duracion="1 sessió" nivel="1" ra="RA7: c, e" sgbd="MongoDB 8.0 · Docker · mongosh · Compass" entrega="Captures + respostes" >}}

#### Objectiu

Instal·lar el servidor, connectar amb les dues eines client i reconéixer els elements d'una base de dades documental.

#### Desenvolupament

{{% steps %}}

1. **Arrenca el servidor** (si no ho vas fer en la guia de l'entorn):

    ```bash
    docker run -d --name mongo8 -p 27017:27017 -v mongo-data:/data/db mongodb/mongodb-community-server:8.0-ubi9
    docker exec -it mongo8 mongosh --eval "db.version()"
    ```

2. **Carrega les dades d'EduGest**:

    ```bash
    docker exec -i mongo8 mongosh < edugest_mongo.js
    # cicles: 4 · professors: 12 · expedients: 32
    ```

3. **Explora amb `mongosh`**:

    ```javascript
    show dbs
    use edugest
    show collections
    db.expedientes.findOne({ _id: 1 })
    db.expedientes.findOne({ _id: 30 })
    db.ciclos.findOne({ _id: "SMR" })
    db.expedientes.stats().size          // grandària en bytes
    db.expedientes.getIndexes()
    ```

4. **Explora amb Compass.** Connecta amb `mongodb://localhost:27017`. Obri `edugest.expedientes`, canvia entre les vistes *Llista*, *JSON* i *Taula* i usa la pestanya **Schema** (*Analyze*) per a veure quins camps té la col·lecció i en quin percentatge de documents apareix cadascun.

{{% /steps %}}

#### Preguntes

1. Compara els documents amb `_id` 1 i 30. Quins camps té un i no l'altre? Com es representaria eixa diferència en Oracle?
2. Quins índexs té la col·lecció? Qui els ha creat?
3. Segons la pestanya *Schema* de Compass, en quin percentatge d'expedients apareix el camp `dni`? I `grupo`?
4. De quin tipus BSON és `fechaNacimiento`? I `nota`?

#### Comprovació

{{% comprobacion %}}
- [ ] `db.expedientes.countDocuments()` torna 32.
- [ ] Identifiques que l'únic índex és el de `_id`, creat automàticament.
- [ ] `dni` apareix en el 87,5 % dels documents (28 de 32) i `grupo` en el 90,6 % (29 de 32).
{{% /comprobacion %}}

---

## Pràctica 10.2 · CRUD sobre els expedients

{{< practica num="10.2" tipo="Guiada" duracion="2 sessions" nivel="1" ra="RA7: d, e" sgbd="MongoDB 8.0 · mongosh" entrega="p10_2.mongodb.js" >}}

#### Objectiu

Realitzar les quatre operacions bàsiques sobre documents amb subdocuments i arrays, i comparar cadascuna amb el seu equivalent SQL.

#### Desenvolupament

{{% steps %}}

1. **Crear.** Insereix Marina López (consulta l'exemple de la [teoria](/ud10-nosql/ud10-teoria#51-crear-insertone-i-insertmany)) i dos alumnes més amb `insertMany`. Un d'ells **sense** `_id`: quin valor li assigna MongoDB?

2. **Llegir.** Escriu i executa:

    ```javascript
    db.expedientes.find({ "grupo.codigo": "1DAW" }, { _id: 0, nombre: 1, apellidos: 1 }).sort({ apellidos: 1 })
    db.expedientes.countDocuments({ localidad: "Alicante" })          // 13 (sense comptar els nous)
    db.expedientes.find({}, { nombre: 1, fechaNacimiento: 1 }).sort({ fechaNacimiento: 1 }).limit(3)
    ```

3. **Actualitzar.**

    ```javascript
    // a) Afegir un telèfon a qui no en té (Paula, _id 4)
    db.expedientes.updateOne({ _id: 4 }, { $set: { "contacto.telefono": "612345678" } })

    // b) Marcar tot 2DAW com «en pràctiques en empresa»
    db.expedientes.updateMany({ "grupo.codigo": "2DAW" }, { $set: { enFCT: true } })   // 5

    // c) Corregir la nota de Bases de dades d'Adrián (_id 1) amb l'operador posicional
    db.expedientes.updateOne(
      { _id: 1, "matriculas.modulo.codigo": "0484" },
      { $set: { "matriculas.$.nota": 5 } })

    // d) Afegir una falta a eixa mateixa matrícula
    db.expedientes.updateOne(
      { _id: 1, "matriculas.modulo.codigo": "0484" },
      { $push: { "matriculas.$.faltas": { fecha: ISODate("2026-05-20"), horas: 2, justificada: false } } })

    // e) Llevar el camp enFCT de tots
    db.expedientes.updateMany({}, { $unset: { enFCT: "" } })
    ```

4. **Comprova** cada canvi amb `findOne` i una projecció adequada, per exemple:

    ```javascript
    db.expedientes.findOne({ _id: 1 }, { "matriculas.modulo.codigo": 1, "matriculas.nota": 1 })
    ```

5. **Eliminar.** Esborra els alumnes que has inserit en el pas 1 amb **una sola** ordre. Pista: `{ _id: { $in: [...] } }` no val per al que no tenia `_id`. Usa el NIA.

6. **Equivalències.** Escriu, per a cada ordre dels passos 2, 3a, 3b i 5, la sentència SQL equivalent en EduGest-Oracle. Quina de les operacions 3c i 3d necessita **una altra taula** en SQL?

{{% /steps %}}

#### Comprovació

{{% comprobacion %}}
- [ ] L'alumne inserit sense `_id` rep un `ObjectId("...")`.
- [ ] 3b informa `matchedCount: 5, modifiedCount: 5` i 3e `modifiedCount: 5`.
- [ ] Després del pas 3c, la matrícula de 0484 d'Adrián té `nota: 5` i la resta de les seues matrícules no ha canviat.
- [ ] Al final, `countDocuments()` torna a ser 32.
{{% /comprobacion %}}

#### Errors habituals

| Error | Causa |
|---|---|
| `MongoServerError: E11000 duplicate key error` | Insereix un `_id` que ja existix |
| `Update document requires atomic operators` | Has oblidat `$set` en un `updateOne` |
| L'actualització «no fa res» (`matchedCount: 0`) | El filtre no coincidix: revisa majúscules, tipus (`"1"` no és `1`) i la notació de punt |

---

## Pràctica 10.3 · Consultes amb operadors, subdocuments i arrays

{{< practica num="10.3" tipo="Autónoma" duracion="2 sessions" nivel="2" ra="RA7: d, e" sgbd="MongoDB 8.0 · mongosh o Compass" entrega="p10_3.mongodb.js" >}}

#### Enunciat

Resol cada consulta. Comprova que obtens el resultat indicat.

| # | Consulta | Resultat esperat |
|---|---|---|
| N1 | Quants alumnes són d'un grup del cicle DAM? | 13 |
| N2 | Nom, cognoms i data de naixement de l'alumnat nascut abans de 2005, del major al menor | 10 documents; el primer, Sara Amorós Guillem |
| N3 | Alumnat d'Elx o de El Campello (usa `$in`) | 6 |
| N4 | `_id` de l'alumnat **sense telèfon** | 4, 10, 16, 22, 28 |
| N5 | Alumnat amb **alguna** matrícula sense nota | 3, 8, 11, 17, 23, 28 |
| N6 | Alumnat amb algun 10 | Aitana (_id 29) |
| N7 | Alumnat amb **més de 5** matrícules (usa `$expr` i `$size`) | Nerea, Hugo i Lucía |
| N8 | Alumnat el primer cognom del qual comença per «Ib» (usa `$regex`) | 4 documents |
| N9 | Professorat que imparteix algun mòdul en 2DAM (col·lecció `profesores`) | Javier, Lucía, Andrés i Raúl |
| N10 | Professorat que **no** imparteix classe | `_id` 108 a 112 |
| N11 | Cicles amb algun mòdul de més de 200 hores | DAM, DAW i ASIR |
| N12 | Els tres alumnes més jóvens | Manuel, Alba i Víctor |

{{% details title="Pista: la trampa de N5" %}}
Prova primer `db.expedientes.find({ "matriculas.nota": { $exists: false } })`. Torna els `_id` 30, 31 i 32: els documents en què **cap** element de l'array té `nota` (perquè el seu array està buit!). Per a «**algun** element sense nota» necessites `$elemMatch`:

```javascript
db.expedientes.find({ matriculas: { $elemMatch: { nota: { $exists: false } } } }, { nombre: 1 })
```
{{% /details %}}

{{< solucion id="ud10-001" title="Solució de N7 y N9" />}}

#### Comprovació

{{% comprobacion %}}
- [ ] Les dotze consultes donen el resultat esperat.
- [ ] Expliques amb les teues paraules la diferència entre N5 amb i sense `$elemMatch`.
- [ ] Per a N4 i N10 expliques quin equivalent tindrien en SQL (`IS NULL`, `NOT EXISTS`/`LEFT JOIN`).
{{% /comprobacion %}}

---

## Pràctica 10.4 · Agregacions: el mateix informe en SQL i en MongoDB

{{< practica num="10.4" tipo="Guiada" duracion="2 sessions" nivel="2" ra="RA7: d, e" sgbd="MongoDB 8.0 · Compass (Aggregations) · Oracle 26ai" entrega="p10_4.mongodb.js + p10_4.sql + comparació" >}}

#### Objectiu

Construir pipelines d'agregació etapa a etapa i comparar el seu resultat i la seua llegibilitat amb la consulta SQL equivalent.

#### Desenvolupament

{{% steps %}}

1. **Construïx el pipeline en Compass.** Obri `expedientes` → pestanya *Aggregations*. Afig les etapes una a una i observa la vista prèvia de cadascuna:

    ```javascript
    [
      { $group: { _id: "$localidad", alumnos: { $sum: 1 } } },
      { $sort: { alumnos: -1, _id: 1 } }
    ]
    ```

    Ha de coincidir amb la pràctica 7.1 (Alicante 13, Mutxamel 6...). Exporta el pipeline a codi amb el botó *Export to language*.

2. **Mitjana de Bases de dades per cicle** (`$unwind` + `$match` després de l'`$unwind`):

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

3. **Les cinc persones amb més hores de falta** (doble `$unwind`):

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

4. **Matrícules suspeses per grup.** Escriu-ho tu. Resultat: 1ASIR 3, 1DAM 7, 1DAW 5, 2DAM 8, 2DAW 4.

5. **Alumnat per nom de cicle amb `$lookup`** sobre la col·lecció `ciclos`. Resultat: DAM 13, DAW 11, ASIR 5.

6. **Escriu en SQL (Oracle)** les consultes dels passos 2 a 5 i compara: nombre de línies, llegibilitat i què et resulta més natural en cada cas.

{{% /steps %}}

#### Comprovació

{{% comprobacion %}}
- [ ] Els cinc pipelines donen els resultats indicats, i les consultes SQL donen els mateixos.
- [ ] Saps explicar per què el `$match` del pas 2 va **després** de l'`$unwind`.
- [ ] En el pas 3 expliques per què fa falta `$sort` per `_id` a més de per `horas` (hi ha un empat en el cinqué lloc).

> [!WARNING]
> `$round` de MongoDB arredonix els valors que estan **exactament** a meitat de camí cap al nombre **parell** (*round half to even*): `$round: [2.345, 2]` dona 2.34. El `ROUND` d'Oracle arredonix cap amunt (2.35). Amb les dades d'EduGest no hi ha empats d'este tipus, però tin-ho en compte en comparar informes.
{{% /comprobacion %}}

---

## Pràctica 10.5 · Modelatge documental d'un catàleg

{{< practica num="10.5" tipo="Autónoma" duracion="2 sessions" nivel="3" ra="RA7: c, d" sgbd="MongoDB 8.0" entrega="Document de disseny + script amb validador, dades i consultes" >}}

#### Objectiu

Dissenyar una base de dades documental a partir dels **patrons de consulta**, justificant què s'incrusta i què es referencia.

#### Context

Una botiga en línia de material informàtic vol migrar el seu catàleg a MongoDB. Els productes són molt diferents entre si:

- Portàtils: processador, RAM, emmagatzematge, pantalla, pes.
- Ratolins: connexió (USB/Bluetooth), DPI, si és sense fil.
- Monitors: polzades, resolució, freqüència, panells.
- Tots tenen: referència, nom, marca, preu, estoc i una o diverses categories.
- Els clients deixen **opinions** (puntuació d'1 a 5, text, data). Alguns productes en tenen milers.

Consultes més freqüents:

1. Fitxa del producte amb les seues característiques i les **5 opinions més recents**.
2. Llistat per categoria amb filtres per preu i marca.
3. Puntuació mitjana de cada producte.

#### Enunciat

1. Dissenya les col·leccions i l'estructura dels documents. Justifica cada decisió d'incrustar o referenciar en funció de les consultes.
2. Explica com resoldries la «mitjana de puntuació» sense recalcular-la en cada consulta (pista: patró de **camp calculat** actualitzat en cada nova opinió).
3. Crea la col·lecció `productos` amb un **validador** `$jsonSchema` que exigisca els camps comuns, `precio >= 0` i `stock` enter no negatiu.
4. Inserix almenys **10 productes** de tres tipus distints i 20 opinions.
5. Escriu les tres consultes freqüents i crea els índexs que les acceleren. Comprova amb `explain("executionStats")` que usen `IXSCAN`.
6. Compara amb un disseny relacional: quantes taules farien falta per a les característiques variables? (Pensa en el patró *entitat-atribut-valor* o en una taula per tipus de producte.)

#### Comprovació

{{% comprobacion %}}
- [ ] Les opinions **no** estan incrustades sense límit en el producte (problema dels 16 MB); com a màxim, les 5 últimes.
- [ ] El validador rebutja un producte amb preu negatiu.
- [ ] Les consultes usen índexs.

{{% details title="Pista: patró «subconjunt»" %}}
Guarda totes les opinions en una col·lecció `opiniones` (amb la referència del producte) i, a més, incrusta en el producte un array `ultimasOpiniones` amb les 5 més recents. En afegir una opinió: inserix-la en `opiniones` i actualitza el producte amb `$push` + `$each` + `$sort` + `$slice: 5`, i `$inc` del nombre d'opinions i de la suma de puntuacions.
{{% /details %}}
{{% /comprobacion %}}

---

## Pràctica 10.6 · Altres models: clau-valor i grafs

{{< practica num="10.6" tipo="Autónoma" duracion="2 sessions" nivel="2" ra="RA7: a, b" sgbd="Redis/Valkey (Docker) · Neo4j (Docker o Sandbox)" entrega="Informe amb captures" >}}

#### Objectiu

Experimentar breument amb altres dos tipus de bases de dades NoSQL per a avaluar els seus punts forts i les seues limitacions.

#### Part A · Clau-valor amb Valkey (compatible amb Redis)

```bash
docker run -d --name valkey -p 6379:6379 valkey/valkey:8
docker exec -it valkey valkey-cli
```

```text
SET sesion:abc123 "id_alumno=1;rol=ALUMNO"
EXPIRE sesion:abc123 1800        # caduca en 30 minuts
TTL sesion:abc123
INCR visitas:portal              # comptador atòmic
HSET alumno:1 nombre "Adrián" grupo "1DAM"
HGETALL alumno:1
KEYS alumno:*                    # només en proves! en producció usa SCAN
```

Respon: com buscaries «tots els alumnes de 1DAM»? Què hauries d'haver guardat per a poder fer-ho?

#### Part B · Grafs amb Neo4j

Crea un xicotet graf d'EduGest (5 alumnes, 3 mòduls, 2 professors) i resol amb Cypher:

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

#### Conclusió

Completa una taula amb els quatre models (relacional, documental, clau-valor i grafs) i, per a cadascun: estructura, llenguatge, una consulta en la qual destaca i una consulta en la qual patix.

---

## Pràctica 10.7 · Repte: relacional o NoSQL?

{{< practica num="10.7" tipo="Reto" duracion="1 sessió + defensa" nivel="3" ra="RA7: a, b · RA1: b" sgbd="—" entrega="Informe de decisió (1 pàgina per cas) + defensa oral" >}}

#### Enunciat

Per a cada cas, recomana el model (o la combinació de models) i justifica'l amb arguments d'**estructura de les dades**, **consultes**, **consistència**, **escalabilitat** i **cost**. Indica també què **perdries** amb l'alternativa descartada.

1. **Secretaria virtual de la Conselleria:** matrícules de tots els instituts de la Comunitat, amb actes oficials i certificats.
2. **App d'apunts col·laboratius** de l'alumnat: cada apunt té text, imatges, etiquetes variables, comentaris i versions.
3. **Sensors de qualitat de l'aire** en totes les aules del centre: CO₂, temperatura i humitat cada 30 segons, consultats per intervals de temps.
4. **Recomanador de cicles formatius**: «l'alumnat que va estudiar el mateix que tu i té els teus interessos va triar...».
5. **Carret de la compra** de la botiga de la pràctica 10.5.

#### Comprovació

{{% comprobacion %}}
- [ ] Cap recomanació es basa en «és més modern» o «és més ràpid» sense explicar per què.
- [ ] Almenys un cas proposa **persistència políglota** (dos models alhora) i explica com se sincronitzen.
- [ ] Uses la taula de decisió de la teoria com a punt de partida, no com a regla automàtica.
{{% /comprobacion %}}

---

## Projecte EduGest · UD10: l'expedient documental

{{< practica num="EduGest-10" tipo="Proyecto" duracion="Treball transversal (2 setmanes)" nivel="3" ra="RA7: a-e" sgbd="Oracle 26ai · MongoDB 8.0" entrega="edugest/10_nosql/ + docs/10-nosql.md" >}}

#### Enunciat

1. **Exportació.** Escriu una consulta en Oracle que genere, per a cada alumne, el seu expedient en **JSON** usant les funcions SQL/JSON d'Oracle (`JSON_OBJECT`, `JSON_ARRAYAGG`). Exporta el resultat a un fitxer i importa'l en MongoDB (Compass → *Add data* → *Import JSON*, o `mongoimport`).

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

2. **Validació.** Afig a la col·lecció un validador `$jsonSchema` coherent amb les restriccions d'Oracle (NIA de 8 dígits, nota entre 0 i 10, convocatòria d'1 a 4).
3. **Consultes.** Reescriu en MongoDB cinc dels teus informes de la UD07 i compara resultats.
4. **Índexs.** Crea els índexs necessaris i mostra els plans (`explain`).
5. **Informe final** (`10-nosql.md`): avantatges i inconvenients del model documental per a EduGest, quines parts del sistema tindrien sentit en MongoDB i quines han de continuar en Oracle, i com es mantindrien sincronitzades.

#### Comprovació

{{% comprobacion %}}
- [ ] Els 32 expedients importats coincidixen amb les dades d'Oracle.
- [ ] El validador rebutja una nota d'11.
- [ ] Les cinc consultes donen els mateixos resultats en els dos sistemes.
- [ ] L'informe final justifica les decisions amb criteris tècnics.

> [!TIP]
> Oracle 23ai i 26ai inclouen **JSON Relational Duality Views**, que permeten consultar i modificar dades relacionals **com si foren documents JSON**, amb totes les garanties d'integritat del model relacional. Investiga esta característica: és un bon exemple que la frontera entre SQL i NoSQL és cada vegada més difusa.
{{% /comprobacion %}}
