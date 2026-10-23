---
title: "Consultes sobre una taula"
weight: 1
bookToc: true
---

# UD06 · Consultes sobre una taula i funcions

## Resum del tema

Consultar és l'operació més freqüent en qualsevol base de dades. En esta unitat aprendràs la sentència `SELECT` aplicada a **una sola taula**: triar columnes (projecció), filtrar files (selecció), ordenar, eliminar duplicats, tractar els valors nuls i transformar les dades amb les **funcions** que proporciona Oracle. A la UD07 combinarem diverses taules i agruparem resultats.

Tots els exemples s'executen sobre l'esquema de referència **EDUGEST** carregat amb els [scripts del projecte](/guia/proyecto-edugest#4-scripts-descarregables), i mostren el resultat que has d'obtindre.

{{< ra "RA3:a,b" "RA5:e" >}}

### Temporalització

La unitat ocupa **23 hores d'aula** (12 de teoria i 11 de pràctica). És la unitat amb més hores del curs: ací s'adquirix la destresa amb `SELECT` que s'utilitzarà fins al final del mòdul.

{{< sesiones unidad="UD06" horas="23" >}}
items:
  - {h: 2, tipo: T, t: "Eines i sentència SELECT. Projecció, àlies, concatenació i DISTINCT", ref: "§1 i §2"}
  - {h: 1, tipo: P, t: "Primeres consultes i eines", ref: "Pràctica 6.1"}
  - {h: 2, tipo: T, t: "Ordenació i selecció amb WHERE: comparació, LIKE i operadors lògics", ref: "§3 i §4 · laboratori de SELECT"}
  - {h: 3, tipo: P, t: "Consultes per a secretaria", ref: "Pràctica 6.2"}
  - {h: 2, tipo: T, t: "El valor NULL i la lògica de tres valors", ref: "§5 · simulador de lògica trivalent"}
  - {h: 2, tipo: P, t: "Laboratori de valors nuls", ref: "Pràctica 6.3"}
  - {h: 1, tipo: T, t: "Limitar el nombre de files", ref: "§6"}
  - {h: 3, tipo: T, t: "Funcions de fila (I): text, numèriques i de data", ref: "§7.1 a §7.3"}
  - {h: 2, tipo: T, t: "Funcions de fila (II): conversió, CASE, DECODE i expressions regulars", ref: "§7.4 a §7.6"}
  - {h: 3, tipo: P, t: "Funcions per a informes", ref: "Pràctica 6.4"}
  - {h: 1, tipo: P, t: "Validar dades amb SQL", ref: "Pràctica 6.5"}
  - {h: 1, tipo: P, t: "Consultes del dia a dia en EduGest", ref: "Projecte EduGest-6"}
autonomo:
  - "Acabar les consultes de la pràctica 6.2 que no hagen donat temps a l'aula"
  - "Ampliacions de les pràctiques 6.3, 6.4 i 6.5"
{{< /sesiones >}}

> [!IMPORTANT]
> Les consultes **s'aprenen escrivint-les**. Abans d'executar cadascuna, prediu quantes files tornarà i per què; després comprova-ho. Els laboratoris interactius simulen el comportament d'Oracle sobre les dades reals d'EduGest, però no substituïxen un SGBD.

### Objectius d'aprenentatge

En acabar esta unitat seràs capaç de:

- Identificar les eines i les clàusules de la sentència `SELECT`.
- Seleccionar columnes, calcular expressions i usar àlies.
- Filtrar files amb operadors de comparació, lògics, `BETWEEN`, `IN`, `LIKE` i `IS NULL`.
- Ordenar resultats i limitar el nombre de files.
- Raonar amb la lògica de tres valors que introduïx `NULL`.
- Usar funcions de text, numèriques, de data, de conversió i condicionals d'Oracle.

> [!TIP]
> **Prepara la teua sessió** perquè les dates i els números es vegen com en estos apunts. Executa en connectar-te:
>
> ```sql
> ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY';
> ALTER SESSION SET NLS_NUMERIC_CHARACTERS = '.,';
> ```
>
> El format de presentació **no** canvia les dades guardades, només com es mostren.

---

{{< sesion n="1" h="2" tipo="t" >}}Eines, SELECT i projecció{{< /sesion >}}

## 1. Eines i sentències per a consultar

Per a consultar una base de dades Oracle pots usar:

| Eina | Ús |
|---|---|
| **Full de treball SQL** de SQL Developer o VS Code | Escriure i executar consultes (`Ctrl+Intro`); el resultat apareix en una graella |
| **Generador de consultes** (*Query Builder*) de SQL Developer | Construir la consulta arrossegant taules i marcant columnes; genera l'SQL |
| **SQLcl / SQL\*Plus** | Línia d'ordres; ideal per a scripts i per a guardar evidències amb `SPOOL` |
| **Pestanya *Dades*** d'una taula en SQL Developer | Veure i filtrar el contingut sense escriure SQL |

La sentència per a consultar és `SELECT`. La seua forma general, amb totes les clàusules que veuràs en esta unitat i en la següent, és:

```sql
SELECT    [DISTINCT] columnes o expressions     -- 5. quines columnes
FROM      taula(es)                              -- 1. d'on
WHERE     condició sobre les files               -- 2. quines files
GROUP BY  columnes d'agrupació                   -- 3. com agrupar          (UD07)
HAVING    condició sobre els grups               -- 4. quins grups          (UD07)
ORDER BY  criteris d'ordenació                   -- 6. en quin ordre
FETCH FIRST n ROWS ONLY;                         -- 7. quantes files
```

> [!IMPORTANT]
> L'**ordre en què s'escriu** una consulta no és l'**ordre en què s'avalua**. El SGBD processa primer `FROM`, després `WHERE`, `GROUP BY`, `HAVING`, `SELECT` i finalment `ORDER BY`. Per això un àlies definit en el `SELECT` **es pot usar en `ORDER BY`** però **no en `WHERE`**.

---

## 2. Projecció: triar columnes

### 2.1 Totes les columnes o només algunes

```sql
SELECT * FROM ciclo;
```


| COD_CICLO | NOMBRE | GRADO | HORAS_TOTALES |
|---|---|---|---|
| DAM | Desarrollo de Aplicaciones Multiplataforma | SUPERIOR | 2000 |
| DAW | Desarrollo de Aplicaciones Web | SUPERIOR | 2000 |
| ASIR | Administración de Sistemas Informáticos en Red | SUPERIOR | 2000 |
| SMR | Sistemas Microinformáticos y Redes | MEDIO | 2000 |

*4 files*


`*` és útil per a explorar, però en una aplicació o un informe escriu sempre les columnes que necessites: el resultat és més clar, transferix menys dades i no canvia si algú afig una columna a la taula.

```sql
SELECT codigo, nombre, horas
FROM   modulo
WHERE  cod_ciclo = 'DAM';
```

### 2.2 Expressions i àlies

En el `SELECT` es poden calcular **expressions**. Un **àlies** dóna nom a la columna resultant; si conté espais o majúscules, va entre cometes dobles.

```sql
SELECT codigo,
       nombre,
       horas,
       horas / 32            AS horas_semana,
       ROUND(horas / 32, 1)  AS "Horas/semana"
FROM   modulo
WHERE  cod_ciclo = 'DAW' AND curso = 2;
```


| CODIGO | NOMBRE | HORAS | HORAS_SEMANA | Horas/semana |
|---|---|---|---|---|
| 0612 | Desarrollo web en entorno cliente | 140 | 4.375 | 4.4 |
| 0613 | Desarrollo web en entorno servidor | 160 | 5 | 5 |
| 0614 | Despliegue de aplicaciones web | 80 | 2.5 | 2.5 |
| 0615 | Diseño de interfaces web | 120 | 3.75 | 3.8 |

*4 files*


### 2.3 Concatenació

L'operador `||` unix cadenes:

```sql
SELECT apellidos || ', ' || nombre AS alumno, localidad
FROM   alumno
WHERE  cod_grupo = '2DAW'
ORDER  BY alumno;
```


| ALUMNO | LOCALIDAD |
|---|---|
| Amorós Guillem, Sara | Mutxamel |
| Carbonell Soriano, Elena | El Campello |
| Planelles Marco, Sofía | Elche |
| Sala Brotons, Mateo | Alicante |
| Verdú Castelló, Nicolás | Alicante |

*5 files*


### 2.4 Eliminar duplicats amb DISTINCT

```sql
SELECT DISTINCT localidad FROM alumno ORDER BY localidad;
```


| LOCALIDAD |
|---|
| Alicante |
| El Campello |
| Elche |
| Mutxamel |
| San Vicente del Raspeig |
| Sant Joan d'Alacant |

*6 files*


`DISTINCT` s'aplica a la **fila completa** del resultat: `SELECT DISTINCT localidad, cod_grupo` torna les combinacions distintes de les dues columnes.

{{% curiosidad titulo="La taula DUAL té un nom per una raó" %}}
Segons el seu creador, Chuck Weiss, `DUAL` es va dissenyar al principi amb **dues files**, per a poder duplicar files amb un join. Hui en té una sola, però conserva el nom: servix per a avaluar expressions, com `SELECT SYSDATE FROM DUAL`.
{{% /curiosidad %}}

### 2.5 La taula DUAL

`DUAL` és una taula especial d'Oracle amb una sola fila. Servix per a avaluar expressions que no depenen de cap taula:

```sql
SELECT SYSDATE, 7 * 24 AS horas_semana, UPPER('edugest') FROM dual;
```

> [!NOTE]
> Des d'**Oracle 23ai** la clàusula `FROM` és opcional en estos casos: `SELECT SYSDATE;` també funciona. En versions anteriors (i en l'examen, si uses 19c) escriu `FROM dual`.

---

{{< quiz >}}
- q: "Què torna `SELECT DISTINCT localidad FROM alumno`?"
  options: ["Una fila per alumne", "Cada localitat una sola vegada (el `NULL` compta com un valor més)", "Només les localitats sense alumnes", "Un error: falta `GROUP BY`"]
  answer: 1
  explain: "`DISTINCT` elimina files duplicades del resultat. Considera iguals dos `NULL`, de manera que apareix com a màxim una fila nul·la."
- q: "En Oracle 26ai, com s'avalua una expressió com `1+1` sense consultar cap taula?"
  options: ["Només és possible amb `FROM dual`", "Amb `FROM dual` (vàlid en totes les versions) o, des de 23ai, sense `FROM`", "No és possible: tota consulta necessita una taula real", "Amb `VALUES (1+1)`"]
  answer: 1
  explain: "`DUAL` és una taula d'una fila i una columna. Oracle exigia `FROM` fins a la 21c; des de 23ai s'admet ometre'l, però per a codi portable a versions anteriors s'usa `DUAL`."
{{< /quiz >}}

---

{{< sesion n="3" h="2" tipo="t" >}}Ordenació i selecció{{< /sesion >}}

## 3. Ordenació: ORDER BY

```sql
SELECT codigo, nombre, cod_ciclo, horas
FROM   modulo
WHERE  horas > 150
ORDER  BY horas DESC, codigo;
```


| CODIGO | NOMBRE | COD_CICLO | HORAS |
|---|---|---|---|
| 0485 | Programación | DAM | 256 |
| 0485 | Programación | DAW | 256 |
| 0369 | Implantación de sistemas operativos | ASIR | 224 |
| 0370 | Planificación y administración de redes | ASIR | 192 |
| 0372 | Gestión de bases de datos | ASIR | 160 |
| 0483 | Sistemas informáticos | DAM | 160 |
| 0483 | Sistemas informáticos | DAW | 160 |
| 0484 | Bases de datos | DAM | 160 |
| 0484 | Bases de datos | DAW | 160 |
| 0613 | Desarrollo web en entorno servidor | DAW | 160 |

*10 files*


- `ASC` (per defecte) ordena de menor a major i `DESC` de major a menor.
- Amb diverses columnes, la segona només decidix quan hi ha empat en la primera.
- Es pot ordenar per un **àlies** o per una expressió.
- En Oracle, els `NULL` van **al final** en ordre ascendent i **al principi** en descendent. Pots canviar-ho amb `NULLS FIRST` o `NULLS LAST`.

> [!WARNING]
> **Sense `ORDER BY`, l'ordre de les files no està garantit.** Encara que hui isquen ordenades per la clau primària, demà poden eixir en un altre ordre.
>
> A més, l'ordenació de textos amb accents depén del paràmetre de sessió `NLS_SORT`. Amb el valor per defecte (`BINARY`), «Álex» s'ordena **després** de «Zoe». Amb `ALTER SESSION SET NLS_SORT = SPANISH;` s'ordena com en un diccionari. Si els teus resultats apareixen en un altre ordre que en els apunts, revisa este paràmetre.

---

{{% paso-a-paso titulo="En qué orden evalúa Oracle un SELECT sencillo" %}}
{{% etapa titulo="1. FROM" %}}
Primer decidix **d'on** ixen les files: `FROM alumno`. Per això l'àlies d'una columna definit en el SELECT no es pot usar encara.
{{% /etapa %}}
{{% etapa titulo="2. WHERE" %}}
Descarta les files que no complixen la condició: `WHERE nota >= 5`. Ací només existixen les columnes de la taula.
{{% /etapa %}}
{{% etapa titulo="3. SELECT" %}}
Calcula les expressions i els àlies de les columnes que es mostren: `SELECT nombre, nota * 10 AS sobre_100`.
{{% /etapa %}}
{{% etapa titulo="4. ORDER BY" %}}
Ordena el resultat. És l'**única** clàusula que pot usar els àlies del SELECT.
{{% /etapa %}}
{{% etapa titulo="5. Límit de files" %}}
Finalment es retalla amb `FETCH FIRST n ROWS ONLY`. A la UD07 s'afegiran `GROUP BY` i `HAVING` entre el WHERE i el SELECT.
{{% /etapa %}}
{{% /paso-a-paso %}}

## 4. Selecció: filtrar files amb WHERE

### 4.1 Operadors de comparació

| Operador | Significat | Exemple |
|---|---|---|
| `=` | Igual | `cod_grupo = '1DAM'` |
| `<>` o `!=` | Distint | `turno <> 'M'` |
| `<`, `>`, `<=`, `>=` | Menor, major... | `nota_final >= 5` |
| `BETWEEN a AND b` | Entre a i b, **tots dos inclosos** | `horas BETWEEN 100 AND 160` |
| `IN (lista)` | Igual a algun de la llista | `cod_ciclo IN ('DAM', 'DAW')` |
| `LIKE patrón` | Coincidix amb un patró | `apellidos LIKE 'B%'` |
| `IS NULL` / `IS NOT NULL` | És (o no és) nul | `cod_grupo IS NULL` |

```sql
SELECT nombre, apellidos, localidad
FROM   alumno
WHERE  localidad = 'Mutxamel'
ORDER  BY apellidos;
```


| NOMBRE | APELLIDOS | LOCALIDAD |
|---|---|---|
| Martina | Alemany Vidal | Mutxamel |
| Sara | Amorós Guillem | Mutxamel |
| Irene | Belda Iborra | Mutxamel |
| Hugo | Brotons Iborra | Mutxamel |
| Álex | Tomás Vidal | Mutxamel |
| Alba | Torregrosa Planelles | Mutxamel |

*6 files*


> [!WARNING]
> Les comparacions de text **distingeixen majúscules i minúscules**: `localidad = 'mutxamel'` no torna res. Per a comparar sense distingir-les usa `UPPER(localidad) = 'MUTXAMEL'`.

### 4.2 Patrons amb LIKE

| Comodí | Significat | Exemple | Coincidix amb |
|---|---|---|---|
| `%` | Qualsevol seqüència de caràcters (inclús buida) | `'B%'` | Belda, Brotons |
| `_` | Exactament un caràcter | `'_DAM'` | 1DAM, 2DAM |

```sql
SELECT nombre, apellidos
FROM   alumno
WHERE  apellidos LIKE 'B%'
ORDER  BY apellidos;
```


| NOMBRE | APELLIDOS |
|---|---|
| Irene | Belda Iborra |
| Lucía | Belda Quiles |
| Hugo | Brotons Iborra |
| Andrea | Brotons Soriano |

*4 files*


Per a buscar un `%` o un `_` literals s'usa `ESCAPE`: `email LIKE '%\_%' ESCAPE '\'` busca correus que continguen un guió baix.

### 4.3 Operadors lògics i precedència

`NOT` s'avalua abans que `AND`, i `AND` abans que `OR`. Usa **parèntesis** sempre que barreges `AND` i `OR`.

```sql
-- Matrícules suspeses dels mòduls 2 o 8
SELECT id_matricula, id_alumno, nota_final
FROM   matricula
WHERE  nota_final < 5
AND    id_modulo IN (2, 8)
ORDER  BY id_matricula;
```


| ID_MATRICULA | ID_ALUMNO | NOTA_FINAL |
|---|---|---|
| 10002 | 1 | 4.75 |
| 10007 | 2 | 4.75 |
| 10038 | 8 | 4 |

*3 files*


{{% details title="Què tornaria `WHERE nota_final < 5 AND id_modulo = 2 OR id_modulo = 8`?" %}}
Per la precedència, s'avalua com `(nota_final < 5 AND id_modulo = 2) OR id_modulo = 8`: tornaria els suspensos del mòdul 2 **i totes** les matrícules del mòdul 8, aprovades o no. Per això cal posar parèntesis, o usar `IN`.
{{% /details %}}

#### Laboratori de `SELECT`

Construïx una consulta sobre la taula `ALUMNO` triant columnes, condicions i ordre. Compara el resultat amb el que vas predir.

{{< select-lab >}}

> [!WARNING]
> `WHERE a OR b AND c` **no** s'avalua d'esquerra a dreta: `AND` té major precedència que `OR`. Usa parèntesis sempre que barreges ambdós.

{{< quiz >}}
- q: "`WHERE nombre LIKE 'M_ría'` quines cadenes complixen el patró?"
  options: ["Les que comencen per M i acaben en ría, amb qualsevol nombre de caràcters pel mig", "Les que tenen exactament un caràcter entre `M` i `ría` (María, Mería...)", "Només la cadena literal `M_ría`", "Cap: `_` no s'admet en `LIKE`"]
  answer: 1
  explain: "`%` substituïx zero o més caràcters i `_` exactament un."
- q: "Quina és la forma correcta de buscar les matrícules sense nota?"
  options: ["`WHERE nota_final = NULL`", "`WHERE nota_final IS NULL`", "`WHERE nota_final == NULL`", "`WHERE NOT nota_final`"]
  answer: 1
  explain: "Qualsevol comparació amb `NULL` mitjançant `=` dóna `UNKNOWN`, i `WHERE` només conserva les files `TRUE`. S'ha d'usar `IS NULL`."
{{< /quiz >}}

---

{{< sesion n="5" h="2" tipo="t" >}}El valor NULL{{< /sesion >}}

{{% curiosidad titulo="NULL no és zero ni «buit»" %}}
`NULL` significa «valor desconegut». Per això `NULL = NULL` no és vertader, sinó desconegut, i per això SQL usa una lògica de **tres valors**: vertader, fals i desconegut.
{{% /curiosidad %}}

## 5. El valor NULL

`NULL` significa **«valor desconegut o no aplicable»**. No és un zero ni una cadena buida: és l'absència de valor.

### 5.1 Lògica de tres valors

Qualsevol comparació amb `NULL` dóna com a resultat **desconegut** (`UNKNOWN`), i `WHERE` només torna les files la condició de les quals és **vertadera**.

| A | B | A AND B | A OR B | NOT A |
|---|---|---|---|---|
| V | V | V | V | F |
| V | F | F | V | F |
| V | ? | ? | V | F |
| F | ? | F | ? | V |
| ? | ? | ? | ? | ? |

Conseqüències pràctiques:

```sql
SELECT COUNT(*) FROM alumno WHERE cod_grupo = NULL;      -- 0 files: sempre!
SELECT COUNT(*) FROM alumno WHERE cod_grupo IS NULL;     -- 3 files
SELECT COUNT(*) FROM alumno WHERE cod_grupo <> '1DAM';   -- 22: els 3 sense grup NO ixen
```

```sql
SELECT nia, nombre, apellidos
FROM   alumno
WHERE  cod_grupo IS NULL;
```


| NIA | NOMBRE | APELLIDOS |
|---|---|---|
| 10451110 | Zoe | Iborra Valero |
| 10451147 | Lucas | Agulló Cerdá |
| 10451184 | Irene | Belda Iborra |

*3 files*


#### Simulador de lògica de tres valors

Combina `TRUE`, `FALSE` i `UNKNOWN` amb `AND`, `OR` i `NOT`, i comprova quines files conserva `WHERE`.

{{< null-logic >}}

{{< quiz >}}
- q: "`TRUE AND UNKNOWN` val…"
  options: ["`TRUE`", "`FALSE`", "`UNKNOWN`", "Error"]
  answer: 2
  explain: "Si un operand és `UNKNOWN` i l'altre no decidix el resultat, el resultat és `UNKNOWN`. En canvi, `FALSE AND UNKNOWN` és `FALSE`."
- q: "`WHERE nota_final NOT IN (5, NULL)` què torna?"
  options: ["Les notes distintes de 5", "Cap fila", "Només les files amb nota nul·la", "Error de sintaxi"]
  answer: 1
  explain: "`x NOT IN (5, NULL)` equival a `x <> 5 AND x <> NULL`; la segona part és `UNKNOWN` i la conjunció mai no arriba a `TRUE`. És una trampa clàssica."
{{< /quiz >}}

### 5.2 Funcions per a tractar els nuls

| Funció | Torna | Exemple |
|---|---|---|
| `NVL(expr, valor)` | `valor` si `expr` és nul; si no, `expr` | `NVL(email, '(sin correo)')` |
| `NVL2(expr, si_no_nulo, si_nulo)` | Un valor o un altre segons `expr` siga nul | `NVL2(id_tutor, 'Con tutor', 'Sin tutor')` |
| `COALESCE(e1, e2, ...)` | El primer valor no nul (estàndard SQL) | `COALESCE(email, telefono, 'sin contacto')` |
| `NULLIF(a, b)` | `NULL` si a = b; si no, a | `NULLIF(horas, 0)` evita dividir per zero |

```sql
SELECT id_alumno, nombre, NVL(email, '(sin correo)') AS email
FROM   alumno
WHERE  email IS NULL OR telefono IS NULL
ORDER  BY id_alumno;
```


| ID_ALUMNO | NOMBRE | EMAIL |
|---|---|---|
| 4 | Paula | paulaferri4@alu.edugest.es |
| 8 | Iván | (sin correo) |
| 10 | Nerea | nereacerda10@alu.edugest.es |
| 16 | Julia | juliaespi16@alu.edugest.es |
| 19 | Alba | (sin correo) |
| 22 | Sofía | sofiaplanelles22@alu.edugest.es |
| 28 | Pablo | pabloamoros28@alu.edugest.es |
| 30 | Zoe | (sin correo) |

*8 files*


> [!CAUTION]
> Qualsevol operació aritmètica amb `NULL` dóna `NULL`: `nota_final + 1` és `NULL` si no hi ha nota. I en Oracle, `''` **és** `NULL`. Comprova-ho amb `SELECT NVL('', 'era nulo') FROM dual;`.

---

{{< sesion n="7" h="1" tipo="t" >}}Limitar el nombre de files{{< /sesion >}}

## 6. Limitar el nombre de files

```sql
-- Les cinc millors notes (amb desempat per id_matricula)
SELECT id_matricula, id_alumno, id_modulo, nota_final
FROM   matricula
WHERE  nota_final IS NOT NULL
ORDER  BY nota_final DESC, id_matricula
FETCH FIRST 5 ROWS ONLY;
```


| ID_MATRICULA | ID_ALUMNO | ID_MODULO | NOTA_FINAL |
|---|---|---|---|
| 10143 | 29 | 24 | 10 |
| 10045 | 9 | 10 | 9.75 |
| 10132 | 27 | 23 | 9.75 |
| 10020 | 4 | 5 | 9.5 |
| 10048 | 10 | 8 | 9.25 |

*5 files*


| Variant | Efecte |
|---|---|
| `FETCH FIRST 5 ROWS ONLY` | Les 5 primeres files |
| `FETCH FIRST 5 ROWS WITH TIES` | Les 5 primeres i les empatades amb la cinquena |
| `OFFSET 10 ROWS FETCH NEXT 10 ROWS ONLY` | Files 11 a 20 (paginació) |
| `FETCH FIRST 10 PERCENT ROWS ONLY` | El 10 % de les files |

> [!NOTE]
> `FETCH FIRST` és SQL estàndard i està en Oracle des de la versió 12c. En codi antic veuràs la pseudocolumna `ROWNUM` (`WHERE ROWNUM <= 5`), que s'avalua **abans** de l'`ORDER BY` i produïx errors si no s'usa amb una subconsulta. MySQL i PostgreSQL usen `LIMIT 5`.

---

{{< sesion n="8" h="3" tipo="t" >}}Funcions de fila: text, numèriques i de data{{< /sesion >}}

## 7. Funcions de fila

Les **funcions de fila** s'apliquen a cada fila i tornen un valor per fila. Formen part de les funcions que proporciona el sistema gestor (RA5.e). Les **funcions de grup** (`COUNT`, `SUM`, `AVG`...), que resumixen diverses files, s'estudien a la UD07.

### 7.1 Funcions de text

| Funció | Resultat d'exemple |
|---|---|
| `UPPER('Bases de Datos')` / `LOWER(...)` | `BASES DE DATOS` / `bases de datos` |
| `INITCAP('marta soler')` | `Marta Soler` |
| `LENGTH('Oracle')` | `6` |
| `SUBSTR('10450037', 1, 4)` | `1045` (des de la posició 1, 4 caràcters) |
| `INSTR('msoler@edugest.es', '@')` | `7` (posició de la primera @) |
| `TRIM('  hola  ')`, `LTRIM`, `RTRIM` | `hola` |
| `LPAD('7', 3, '0')` / `RPAD('7', 3, '*')` | `007` / `7**` |
| `REPLACE('1DAM', 'DAM', 'DAW')` | `1DAW` |
| `CONCAT('a', 'b')` | `ab` (només dos arguments; millor `\|\|`) |

```sql
-- Usuari del correu del professorat (allò que va abans de la @)
SELECT nombre, email, SUBSTR(email, 1, INSTR(email, '@') - 1) AS usuario
FROM   profesor
WHERE  id_departamento = 2;
```

| NOMBRE | EMAIL | USUARIO |
|---|---|---|
| Carmen | cortiz@edugest.es | cortiz |
| Sergio | sramos@edugest.es | sramos |

```sql
SELECT UPPER(apellidos) || ', ' || nombre AS alumno, LENGTH(nombre) AS letras
FROM   alumno
WHERE  cod_grupo = '1ASIR'
ORDER  BY apellidos;
```

| ALUMNO | LETRAS |
|---|---|
| AMORÓS CARBONELL, Pablo | 5 |
| IBORRA TORREGROSA, Diego | 5 |
| PASCUAL BROTONS, Aitana | 6 |
| TOMÁS GUILLEM, Víctor | 6 |
| TOMÁS VIDAL, Álex | 4 |

### 7.2 Funcions numèriques

| Funció | Resultat |
|---|---|
| `ROUND(7.256, 2)` / `ROUND(7.5)` | `7.26` / `8` |
| `TRUNC(7.256, 1)` / `TRUNC(7.9)` | `7.2` / `7` |
| `CEIL(4.1)` / `FLOOR(4.9)` | `5` / `4` |
| `MOD(17, 5)` | `2` (resta) |
| `ABS(-3)`, `POWER(2, 10)`, `SQRT(81)` | `3`, `1024`, `9` |

```sql
-- Notes arredonides a l'enter, com apareixen al butlletí
SELECT id_matricula, nota_final, ROUND(nota_final) AS nota_boletin, TRUNC(nota_final) AS nota_truncada
FROM   matricula
WHERE  id_alumno = 1
ORDER  BY id_matricula;
```

| ID_MATRICULA | NOTA_FINAL | NOTA_BOLETIN | NOTA_TRUNCADA |
|---|---|---|---|
| 10001 | 8.75 | 9 | 8 |
| 10002 | 4.75 | 5 | 4 |
| 10003 | 7.25 | 7 | 7 |
| 10004 | 4.75 | 5 | 4 |
| 10005 | 6.75 | 7 | 6 |

> [!WARNING]
> Fixa't en la matrícula 10002: amb `ROUND`, un 4,75 apareix com a **5** en el butlletí, però el mòdul està **suspés**. Les decisions (aprovar o no) es prenen sempre sobre el **valor real**, mai sobre el valor formatat.

### 7.3 Funcions de data

En Oracle, restar dues dates dóna el nombre de **dies** entre elles, i sumar un número a una data afig dies.

| Funció | Resultat |
|---|---|
| `SYSDATE` / `SYSTIMESTAMP` | Data i hora actuals del servidor |
| `ADD_MONTHS(DATE '2026-01-31', 1)` | `28/02/2026` |
| `MONTHS_BETWEEN(fecha1, fecha2)` | Mesos entre dues dates (amb decimals) |
| `EXTRACT(YEAR FROM fecha)` | L'any (també `MONTH`, `DAY`) |
| `TRUNC(SYSDATE)` | La data d'hui a les 00:00:00 |
| `LAST_DAY(DATE '2026-02-10')` | `28/02/2026` |
| `NEXT_DAY(DATE '2026-10-06', 'LUNES')` | El dilluns següent (el nom depén de l'idioma de la sessió) |

```sql
-- Edat de l'alumnat de 2DAW a data 6 d'octubre de 2026
SELECT id_alumno, nombre, fecha_nacimiento,
       TRUNC(MONTHS_BETWEEN(DATE '2026-10-06', fecha_nacimiento) / 12) AS edad
FROM   alumno
WHERE  cod_grupo = '2DAW'
ORDER  BY fecha_nacimiento;
```

| ID_ALUMNO | NOMBRE | FECHA_NACIMIENTO | EDAD |
|---|---|---|---|
| 23 | Sara | 07/08/2000 | 26 |
| 20 | Mateo | 09/04/2003 | 23 |
| 22 | Sofía | 13/07/2004 | 22 |
| 24 | Nicolás | 11/05/2005 | 21 |
| 21 | Elena | 21/06/2005 | 21 |

> [!TIP]
> En una aplicació real s'usaria `SYSDATE` en lloc de `DATE '2026-10-06'`. Ací es fixa la data perquè el resultat no canvie segons el dia en què executes la consulta. Els **literals de data** `DATE 'AAAA-MM-DD'` són SQL estàndard i no depenen de la configuració de la sessió: usa'ls sempre en lloc de cadenes com `'15/09/2025'`.

**Comparar dates que tenen hora.** Com que `DATE` guarda l'hora, per a buscar «el del dia 15» compara amb un interval semiobert:

```sql
SELECT * FROM matricula
WHERE  fecha_matricula >= DATE '2025-09-15'
AND    fecha_matricula <  DATE '2025-09-16';
```

{{< sesion n="9" h="2" tipo="t" >}}Conversió, CASE i expressions regulars{{< /sesion >}}

### 7.4 Funcions de conversió

| Funció | Ús | Exemple | Resultat |
|---|---|---|---|
| `TO_CHAR(fecha, formato)` | Data → text | `TO_CHAR(DATE '2026-10-06', 'DD/MM/YYYY')` | `06/10/2026` |
| | | `TO_CHAR(DATE '2026-10-06', 'fmDay, DD "de" Month', 'NLS_DATE_LANGUAGE=SPANISH')` | `Martes, 6 de Octubre` |
| `TO_CHAR(número, formato)` | Número → text | `TO_CHAR(1520.5, '9G990D00')` | `1,520.50` (segons NLS) |
| `TO_DATE(texto, formato)` | Text → data | `TO_DATE('15/09/2025', 'DD/MM/YYYY')` | data |
| `TO_NUMBER(texto)` | Text → número | `TO_NUMBER('42')` | `42` |

Elements de format de data més usats: `DD` (dia), `MM` (mes), `MON`/`MONTH` (nom del mes), `YYYY` (any), `HH24` (hora), `MI` (minuts), `SS` (segons), `D` (dia de la setmana), `Q` (trimestre).

```sql
SELECT nombre, apellidos,
       TO_CHAR(fecha_alta, 'DD/MM/YYYY') AS alta,
       EXTRACT(YEAR FROM DATE '2026-10-06') - EXTRACT(YEAR FROM fecha_alta) AS cursos_aprox
FROM   profesor
WHERE  fecha_alta < DATE '2015-01-01'
ORDER  BY fecha_alta;
```

| NOMBRE | APELLIDOS | ALTA | CURSOS_APROX |
|---|---|---|---|
| Marta | Soler Ivars | 01/09/2009 | 17 |
| Carmen | Ortiz Llorca | 01/09/2010 | 16 |
| Javier | Pastor Gil | 01/09/2012 | 14 |

> [!WARNING]
> Evita les **conversions implícites**: `WHERE fecha_alta < '01/01/2015'` funciona o falla segons el `NLS_DATE_FORMAT` de cada sessió, i `WHERE nia = 10450037` (sense cometes) obliga Oracle a convertir **totes** les files de la columna, la qual cosa impedix usar el seu índex.

### 7.5 Funcions condicionals: CASE i DECODE

`CASE` és estàndard SQL i permet triar un valor segons condicions.

```sql
SELECT id_matricula, id_modulo, nota_final,
       CASE
           WHEN nota_final IS NULL THEN 'Sin calificar'
           WHEN nota_final < 5     THEN 'Insuficiente'
           WHEN nota_final < 6     THEN 'Suficiente'
           WHEN nota_final < 7     THEN 'Bien'
           WHEN nota_final < 9     THEN 'Notable'
           ELSE                         'Sobresaliente'
       END AS calificacion
FROM   matricula
WHERE  id_alumno = 1
ORDER  BY id_modulo;
```


| ID_MATRICULA | ID_MODULO | NOTA_FINAL | CALIFICACION |
|---|---|---|---|
| 10001 | 1 | 8.75 | Notable |
| 10002 | 2 | 4.75 | Insuficiente |
| 10003 | 3 | 7.25 | Notable |
| 10004 | 4 | 4.75 | Insuficiente |
| 10005 | 5 | 6.75 | Bien |

*5 files*


Les condicions s'avaluen **en ordre** i s'usa la primera que es complix. Per això basta amb `nota_final < 6` en la segona branca: si fora menor que 5, ja s'hauria quedat en la primera.

**CASE simple** (compara una expressió amb valors) i el seu equivalent propi d'Oracle, `DECODE`:

```sql
SELECT cod_grupo,
       CASE turno WHEN 'M' THEN 'Mañana' WHEN 'T' THEN 'Tarde' END AS turno,
       DECODE(turno, 'M', 'Mañana', 'T', 'Tarde', 'Desconocido') AS turno_decode
FROM   grupo
ORDER  BY cod_grupo;
```


| COD_GRUPO | TURNO | TURNO_DECODE |
|---|---|---|
| 1ASIR | Mañana | Mañana |
| 1DAM | Mañana | Mañana |
| 1DAW | Tarde | Tarde |
| 2ASIR | Mañana | Mañana |
| 2DAM | Mañana | Mañana |
| 2DAW | Tarde | Tarde |

*6 files*


### 7.6 Expressions regulars

Oracle inclou funcions d'expressions regulars per a cerques més potents que `LIKE`: `REGEXP_LIKE`, `REGEXP_SUBSTR`, `REGEXP_REPLACE`, `REGEXP_INSTR`, `REGEXP_COUNT`.

```sql
-- Professorat amb DNI que comença per 2 i acaba en C o E
SELECT nombre, dni FROM profesor WHERE REGEXP_LIKE(dni, '^2[0-9]{7}[CE]$') ORDER BY nombre;
```

| NOMBRE | DNI |
|---|---|
| Carmen | 21369874E |
| Marta | 21456789C |

---

## 8. Errors freqüents

| Error | Exemple | Correcció |
|---|---|---|
| Comparar amb `= NULL` | `WHERE email = NULL` | `WHERE email IS NULL` |
| Usar un àlies del `SELECT` en el `WHERE` | `WHERE edad > 20` | Repetix l'expressió o usa una subconsulta (UD07) |
| Cometes dobles per a textos | `WHERE turno = "M"` | Els textos van entre cometes **simples**; les dobles són per a identificadors (ORA-00904) |
| Oblidar parèntesis en barrejar `AND` i `OR` | `a AND b OR c` | `a AND (b OR c)` |
| Confiar en l'ordre sense `ORDER BY` | — | Ordena sempre que l'ordre importe |
| Comparar dates amb text | `fecha > '01/09/2025'` | `fecha > DATE '2025-09-01'` |
| `BETWEEN` amb dates amb hora | `BETWEEN DATE '2025-09-15' AND DATE '2025-09-15'` | Interval semiobert `>=` i `<` |

## 9. Bones pràctiques

- Escriu les paraules reservades en majúscules i alinea les clàusules: la consulta es llig millor.
- Anomena explícitament les columnes; usa `*` només per a explorar.
- Usa àlies clars per a les expressions calculades.
- Usa literals `DATE 'AAAA-MM-DD'` i evita les conversions implícites.
- Comenta les consultes que lliures: quina pregunta responen i quines decisions has pres.

---

{{< tarjetas titulo="Repassa els termes de la UD06" >}}
- t: "Projecció"
  d: "Triar columnes: la llista del SELECT."
- t: "Selecció"
  d: "Triar files: la condició del WHERE."
- t: "Àlies"
  d: "Nom alternatiu per a una columna o una taula en la consulta."
- t: "DISTINCT"
  d: "Elimina del resultat les files duplicades."
- t: "LIKE"
  d: "Compara amb un patró: % (qualsevol text) i _ (un caràcter)."
- t: "IS NULL"
  d: "Únic mode correcte de comprovar si un valor és nul."
{{< /tarjetas >}}

## 10. Resum

- `SELECT` tria columnes (**projecció**), `WHERE` filtra files (**selecció**) i `ORDER BY` ordena.
- El SGBD avalua `FROM` → `WHERE` → `SELECT` → `ORDER BY`.
- `NULL` introduïx una lògica de tres valors: es compara amb `IS NULL` i es tracta amb `NVL`, `COALESCE` o `NVL2`.
- `FETCH FIRST n ROWS ONLY` limita el nombre de files.
- Oracle proporciona funcions de text, numèriques, de data, de conversió i condicionals (`CASE`, `DECODE`).

---

## 11. Autoavaluació

{{< quiz >}}
- q: "Quina clàusula elimina files duplicades del resultat?"
  options: ["UNIQUE", "DISTINCT", "GROUP BY", "ORDER BY"]
  answer: 1
  explain: "`SELECT DISTINCT` elimina les files repetides del resultat, tenint en compte totes les columnes seleccionades."
- q: "La taula ALUMNO té 32 files; 3 tenen `cod_grupo` a NULL i 7 estan en 1DAM. Quantes files torna `WHERE cod_grupo <> '1DAM'`?"
  options: ["25", "22", "32", "29"]
  answer: 1
  explain: "Per a les 3 files amb NULL la comparació és desconeguda i no es tornen: 32 − 7 − 3 = **22**."
- q: "Quin patró LIKE troba els grups de primer curs ('1DAM', '1DAW', '1ASIR')?"
  options: ["'1_'", "'%1'", "'1%'", "'_1%'"]
  answer: 2
  explain: "`'1%'`: comença per 1 i continua qualsevol seqüència. `'1_'` només coincidiria amb codis de dos caràcters."
- q: "Per què falla `SELECT horas*2 AS doble FROM modulo WHERE doble > 300`?"
  options: ["Perquè no es pot multiplicar en el SELECT", "Perquè WHERE s'avalua abans que SELECT i l'àlies encara no existix", "Perquè falta ORDER BY", "Perquè els àlies han d'anar entre cometes"]
  answer: 1
  explain: "L'ordre lògic és FROM → WHERE → SELECT. En WHERE cal repetir l'expressió: `WHERE horas*2 > 300`."
- q: "Què torna `NVL2(email, 'Sí', 'No')` per a un alumne sense correu?"
  options: ["NULL", "'Sí'", "'No'", "Un error"]
  answer: 2
  explain: "NVL2 torna el segon argument si l'expressió **no** és nul·la i el tercer si és nul·la."
- q: "Què torna `ROUND(4.75)` i què torna `TRUNC(4.75)`?"
  options: ["5 y 4", "4 y 5", "5 y 5", "4.8 y 4.7"]
  answer: 0
  explain: "ROUND arredoneix a l'enter més pròxim; TRUNC elimina els decimals sense arredonir."
- q: "Quina és la forma més fiable de filtrar les matrícules del 15 de setembre de 2025 si la columna és DATE?"
  options: ["`fecha_matricula = '15/09/2025'`", "`fecha_matricula = DATE '2025-09-15'`", "`fecha_matricula >= DATE '2025-09-15' AND fecha_matricula < DATE '2025-09-16'`", "`fecha_matricula LIKE '15/09/2025%'`"]
  answer: 2
  explain: "DATE inclou l'hora. L'interval semiobert inclou qualsevol hora d'eixe dia i no depén de la configuració de la sessió."
- q: "En un CASE amb diverses branques WHEN que es complixen alhora, quina s'usa?"
  options: ["L'última", "La primera que es complix", "Totes, concatenades", "Es produïx un error"]
  answer: 1
  explain: "Les condicions s'avaluen en ordre i CASE torna el resultat de la **primera** branca vertadera."
{{< /quiz >}}

## Referències

- [Oracle AI Database 26ai: SQL Language Reference, *SELECT*](https://docs.oracle.com/en/database/oracle/oracle-database/26/sqlrf/SELECT.html).
- [Oracle AI Database 26ai: SQL Language Reference, *Single-Row Functions*](https://docs.oracle.com/en/database/oracle/oracle-database/26/sqlrf/Single-Row-Functions.html).
- [Oracle AI Database 26ai: *Format Models*](https://docs.oracle.com/en/database/oracle/oracle-database/26/sqlrf/Format-Models.html).
