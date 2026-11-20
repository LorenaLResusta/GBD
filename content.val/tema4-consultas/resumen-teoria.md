---
title: "Teoria · Resum, composicions i subconsultes"
weight: 20
bookToc: true
---

# Tema 4 · Consultes avançades: composicions, resums i subconsultes

## Resum del tema

A el tema 4 vas aprendre a consultar **una** taula. Però una base de dades ben dissenyada reparteix la informació entre moltes taules: el nom de l'alumne està a `ALUMNO`, la seua nota a `MATRICULA` i el nom del mòdul a `MODULO`. Quasi cap pregunta real del centre es respon amb una sola taula. Este tema ensenya a **tornar a juntar** el que el disseny va separar (composicions o *joins*), a **resumir** moltes files en poques (funcions d'agregat i `GROUP BY`) i a **encadenar consultes** unes dins d'altres (subconsultes).

El recorregut és acumulatiu. Primer es resumix una sola taula, perquè agrupar és més fàcil d'entendre sense composicions pel mig. Després es combinen taules, primer de forma interna (només les files que emparellen) i després externa (conservant també les que no emparellen: el grup sense tutor, el cicle sense grups). A continuació s'usen subconsultes per a preguntes que necessiten dos passos («qui està per damunt de la mitjana del seu mòdul»). Finalment s'estudia l'**optimització** de consultes amb el pla d'execució.

Este és el tema que converteix l'SQL en una eina professional: en acabar-la seràs capaç de contestar pràcticament qualsevol pregunta que secretaria, cap d'estudis o l'equip docent li puguen fer a EduGest. A el tema 5 reutilitzaràs quasi tot el d'ací, perquè `UPDATE` i `DELETE` admeten subconsultes, i a el tema 5 encapsularàs estes consultes en procediments i vistes més elaborades.

Tots els exemples s'executen sobre l'esquema de referència **EDUGEST** amb les dades del curs **2025-26** carregades amb els [scripts del projecte](/guia/proyecto-edugest#4-scripts-descarregables): 5 departaments, 12 professors, 4 cicles, 24 mòduls, 6 grups, 32 alumnes, 143 matrícules, 24 assignacions docents i 46 faltes d'assistència.

{{< ra "RA4:a,c,d,e,f,g" >}}

### Objectius d'aprenentatge

En acabar este tema seràs capaç de:

- Resumir el contingut d'una taula amb funcions d'agregat, raonant com afecten els valors nuls.
- Formar grups amb `GROUP BY` i filtrar-los amb `HAVING`, distingint el seu paper del de `WHERE`.
- Combinar diverses taules amb composicions internes seguint el camí de les claus alienes.
- Decidir quan una pregunta exigix una composició externa i escriure-la sense anul·lar-la amb un filtre mal col·locat.
- Resoldre amb autocomposicions les preguntes en què una taula es relaciona amb si mateixa.
- Escriure subconsultes d'una fila, de diverses files, correlacionades i amb `EXISTS`.
- Obtindre i interpretar el pla d'execució d'una consulta i aplicar criteris d'optimització.

### Temporalització

Esta part del tema ocupa **14 hores d'aula** (7 de teoria i 7 de pràctica). Les composicions
i les subconsultes són el nucli del RA4: convé no avançar fins que cada consulta
es puga escriure sense consultar els apunts.

{{< sesiones unidad="T4" horas="14" parte="Resum, composicions i subconsultes" >}}
items:
  - {h: 2, tipo: T, t: "Funcions d'agregat, GROUP BY i HAVING", ref: "§1 i §2 · laboratori d'agrupament"}
  - {h: 1, tipo: P, t: "Consultes resum", ref: "Pràctica 4.6"}
  - {h: 2, tipo: T, t: "Composicions internes: INNER JOIN i diverses taules", ref: "§3 · laboratori de composicions"}
  - {h: 2, tipo: P, t: "Composicions pas a pas", ref: "Pràctica 4.7"}
  - {h: 1, tipo: T, t: "Composicions externes i autocomposició", ref: "§4 i §5"}
  - {h: 1, tipo: P, t: "Informes per a prefectura", ref: "Pràctica 4.8"}
  - {h: 1, tipo: T, t: "Subconsultes i EXISTS", ref: "§6"}
  - {h: 1, tipo: P, t: "Subconsultes", ref: "Pràctica 4.9"}
  - {h: 1, tipo: T, t: "Optimització de consultes: pla d'execució", ref: "§7"}
  - {h: 1, tipo: P, t: "Optimització: mesurar abans i després", ref: "Pràctica 4.10"}
  - {h: 1, tipo: P, t: "Informes d'EduGest", ref: "Projecte EduGest-4"}
autonomo:
  - "Pràctiques 4.8 i 4.9 (acabar a casa el que no done temps)"
  - "Pràctica 4.11 (repte: el quadre de comandament)"
  - "Exercicis resolts i autoavaluació"
{{< /sesiones >}}

> [!IMPORTANT]
> Estudia este tema amb la base de dades oberta i amb un mètode fix per a cada consulta:
>
> 1. Escriu en castellà la pregunta que vols respondre.
> 2. Decidix **quines taules** la contenen i **per quines claus** s'enllacen.
> 3. **Prediu** quantes files ha de tornar i de quin tipus.
> 4. Executa i compara amb la teua predicció. Si no coincidix, l'error està en el teu model mental, no en Oracle: esbrina on.
>
> Si una consulta torna moltes més files de les esperades, quasi sempre falta una condició de composició. Si en torna menys, quasi sempre sobra un filtre o falta una composició externa.

---


{{< sesion n="1" h="2" tipo="t" >}}Funcions d'agregat, GROUP BY i HAVING{{< /sesion >}}

## 1. Funcions d'agregat

### 1.1 Quin problema resolen

Les funcions de fila del tema 4 (`UPPER`, `ROUND`, `TO_CHAR`…) tornen **un valor per cada fila**: entren 143 files i en isen 143. Però moltes preguntes no demanen files, demanen **un número que resumisca** les files: «quantes matrícules hi ha?», «quina és la nota mitjana?», «quina és la nota més alta?».

Per a això estan les **funcions d'agregat** (també anomenades funcions de grup o de columna): reben un conjunt de files i tornen **un únic valor**.

```mermaid
flowchart LR
    A[143 files de MATRICULA] -->|AVG nota_final| B[1 fila: 6,36]
```

{{< sgbd "Oracle 26ai" >}}

| Funció | Torna | Admet `DISTINCT` | Tipus admesos |
|---|---|---|---|
| `COUNT(*)` | Nombre de **files** del grup | No | — |
| `COUNT(expr)` | Nombre de files en què `expr` **no és nul·la** | Sí | qualsevol |
| `SUM(expr)` | Suma | Sí | numèrics |
| `AVG(expr)` | Mitjana aritmètica | Sí | numèrics |
| `MIN(expr)` / `MAX(expr)` | Valor menor / major | No (no aporta) | numèrics, text, dates |
| `STDDEV(expr)` / `VARIANCE(expr)` | Desviació típica / variància | Sí | numèrics |
| `MEDIAN(expr)` | Mediana | No | numèrics, dates |
| `LISTAGG(expr, sep)` | Concatena els valors del grup en una cadena | Sí | text |

> [!NOTE]
> `COUNT`, `SUM`, `AVG`, `MIN` i `MAX` són SQL estàndard i existixen en tots els SGBD. `STDDEV`, `VARIANCE`, `MEDIAN` i `LISTAGG` són extensions d'Oracle (algunes estan també en PostgreSQL amb un altre nom). `MEDIAN` i `LISTAGG` es tracten com a ampliació: l'avaluable del RA4.c són les cinc primeres.

### 1.2 Exemple senzill: comptar

```sql
SELECT COUNT(*)                    AS matriculas,
       COUNT(nota_final)           AS calificadas,
       COUNT(*) - COUNT(nota_final) AS sin_calificar,
       COUNT(DISTINCT id_alumno)   AS alumnos_distintos,
       COUNT(DISTINCT id_modulo)   AS modulos_distintos
FROM   matricula;
```

| MATRICULAS | CALIFICADAS | SIN_CALIFICAR | ALUMNOS_DISTINTOS | MODULOS_DISTINTOS |
|---|---|---|---|---|
| 143 | 137 | 6 | 29 | 24 |

*1 fila*

Element a element:

| Element | Significat |
|---|---|
| `COUNT(*)` | Compta **files**, sense mirar el seu contingut: 143 matrícules |
| `COUNT(nota_final)` | Compta les files en què `nota_final` **té valor**: 137 |
| `COUNT(*) - COUNT(nota_final)` | Les 6 matrícules sense qualificar |
| `COUNT(DISTINCT id_alumno)` | Valors distints d'`id_alumno`: 29 alumnes tenen matrícula (dels 32) |

> [!IMPORTANT]
> **Totes les funcions d'agregat excepte `COUNT(*)` ignoren els nuls.** No els compten, no els sumen i no els tenen en compte en la mitjana. Esta és la causa número u de resultats «rars» en les consultes resum, i la raó per la qual `COUNT(*)` i `COUNT(columna)` donen números distints.

### 1.3 Exemple aplicat: estadístics de les notes

```sql
SELECT COUNT(nota_final)            AS calificadas,
       ROUND(AVG(nota_final), 2)    AS media,
       MIN(nota_final)              AS minima,
       MAX(nota_final)              AS maxima,
       SUM(nota_final)              AS suma,
       ROUND(SUM(nota_final) / COUNT(*), 2) AS media_incorrecta
FROM   matricula;
```

| CALIFICADAS | MEDIA | MINIMA | MAXIMA | SUMA | MEDIA_INCORRECTA |
|---|---|---|---|---|---|
| 137 | 6.36 | 1.5 | 10 | 871 | 6.09 |

*1 fila*

L'última columna és deliberadament errònia i convé entendre-la bé:

- `AVG(nota_final)` calcula 871 / **137** = 6,36: dividix entre les matrícules **qualificades**.
- `SUM(nota_final) / COUNT(*)` calcula 871 / **143** = 6,09: dividix entre **totes** les matrícules, incloses les sis sense nota, com si foren zeros.

> [!WARNING]
> Les dos xifres responen a preguntes distintes i **cap és més correcta que l'altra en abstracte**: depén del que et demanen. «Nota mitjana dels alumnes qualificats» és 6,36. «Nota mitjana considerant els no presentats com un zero» és 6,09, i llavors convé escriure-ho explícitament amb `AVG(NVL(nota_final, 0))` perquè el lector veja la decisió. El que mai ha de passar és prendre una per l'altra sense adonar-se'n.

### 1.4 MIN i MAX no són només per a números

`MIN` i `MAX` funcionen amb text (ordre alfabètic segons `NLS_SORT`) i amb dates, on `MIN` és la més antiga:

```sql
SELECT MIN(fecha_nacimiento) AS mayor_edad,
       MAX(fecha_nacimiento) AS menor_edad,
       MIN(apellidos)        AS primero_alfabetico
FROM   alumno;
```

| MAYOR_EDAD | MENOR_EDAD | PRIMERO_ALFABETICO |
|---|---|---|
| 07/08/2000 | 25/12/2006 | Agulló Cerdá |

*1 fila*

### 1.5 Comptar condicions: SUM amb CASE

Una tècnica molt habitual en informes és comptar quantes files complixen una condició **dins** del mateix resum, en compte de llançar una consulta per cada condició:

```sql
SELECT COUNT(*)                                            AS matriculas,
       SUM(CASE WHEN nota_final >= 5 THEN 1 ELSE 0 END)     AS aprobadas,
       SUM(CASE WHEN nota_final <  5 THEN 1 ELSE 0 END)     AS suspensas,
       COUNT(*) - COUNT(nota_final)                         AS sin_calificar,
       ROUND(100 * SUM(CASE WHEN nota_final >= 5 THEN 1 ELSE 0 END)
             / COUNT(nota_final), 1)                        AS pct_aprobados
FROM   matricula;
```

| MATRICULAS | APROBADAS | SUSPENSAS | SIN_CALIFICAR | PCT_APROBADOS |
|---|---|---|---|---|
| 143 | 110 | 27 | 6 | 80.3 |

*1 fila*

Fixa't en el denominador del percentatge: `COUNT(nota_final)`, no `COUNT(*)`. El percentatge d'aprovats es calcula sobre els **qualificats**.

> [!TIP]
> En lloc de `SUM(CASE WHEN … THEN 1 ELSE 0 END)` també funciona `COUNT(CASE WHEN … THEN 1 END)`: com que `COUNT` ignora els nuls i el `CASE` sense `ELSE` torna `NULL` quan no es complix, l'efecte és el mateix. Usa la forma que et resulte més llegible, però **sigues coherent** dins d'un mateix informe.

### 1.6 Errors habituals amb els agregats

```sql
-- (a) Barrejar una columna normal amb un agregat sense GROUP BY
SELECT localidad, COUNT(*) FROM alumno;
-- ORA-00937: not a single-group group function

-- (b) Usar un agregat al WHERE
SELECT localidad FROM alumno WHERE COUNT(*) > 3 GROUP BY localidad;
-- ORA-00934: group function is not allowed here

-- (c) Aniuar agregats sense GROUP BY intermedi
SELECT MAX(AVG(nota_final)) FROM matricula;
-- ORA-00978: nested group function without GROUP BY
```

L'error (a) és el més freqüent: si demanes una columna normal junt amb un agregat, Oracle no sap **quina** localitat posar al costat d'un recompte de 32 alumnes. La solució és el `GROUP BY` de l'apartat següent.

---

## 2. Agrupament: GROUP BY i HAVING

### 2.1 Com es formen els grups

`GROUP BY` dividix les files en **grups** que compartixen el mateix valor en les columnes indicades, i després aplica les funcions d'agregat **a cada grup per separat**. El resultat té **una fila per grup**.

```sql
SELECT cod_grupo, COUNT(*) AS alumnos
FROM   alumno
GROUP  BY cod_grupo
ORDER  BY cod_grupo;
```

| COD_GRUPO | ALUMNOS |
|---|---|
| 1ASIR | 5 |
| 1DAM | 7 |
| 1DAW | 6 |
| 2DAM | 6 |
| 2DAW | 5 |
| (null) | 3 |

*6 files*

Observacions importants:

- Hi ha **sis** files perquè hi ha cinc valors distints de `cod_grupo` més el grup dels nuls.
- `GROUP BY` **reunix tots els nuls en un únic grup** (al contrari que l'operador `=`, que mai considera iguals dos nuls). Eixos són els 3 alumnes sense grup assignat.
- La suma dels recomptes és 32: cap fila es perd i cap es compta dos voltes.
- Els `NULL` apareixen al final perquè `ORDER BY … ASC` els col·loca al final en Oracle.

> [!NOTE]
> `GROUP BY` **no garantix l'ordre** del resultat, encara que a vegades ho semble. Si l'ordre importa, escriu `ORDER BY`. És un error clàssic confiar que els grups isquen ordenats.

### 2.2 Què pot aparéixer al SELECT

Esta és la regla que més errors provoca del tema:

> [!IMPORTANT]
> En una consulta amb `GROUP BY`, el `SELECT` només pot contindre:
>
> 1. les **columnes o expressions que apareixen al `GROUP BY`**,
> 2. **funcions d'agregat**,
> 3. constants i expressions calculades a partir d'1 i 2.
>
> Qualsevol altra columna provoca `ORA-00979: not a GROUP BY expression`.

```sql
-- Incorrecta: nombre no està al GROUP BY i no és un agregat
SELECT localidad, nombre, COUNT(*)
FROM   alumno
GROUP  BY localidad;
-- ORA-00979: not a GROUP BY expression
```

La consulta no té sentit: el grup «Alacant» conté 13 alumnes amb 13 noms distints; quin hauria de mostrar? Tens tres eixides possibles, segons el que realment vulgues:

| El que vols | Solució |
|---|---|
| Una fila per localitat, sense el nom | Lleva `nombre` del `SELECT` |
| Una fila per localitat **i** nom | Afig `nombre` al `GROUP BY` |
| Una fila per localitat amb **un** nom representatiu | `MIN(nombre)` o `MAX(nombre)` |
| Una fila per localitat amb **tots** els noms en una cel·la | `LISTAGG(nombre, ', ') WITHIN GROUP (ORDER BY nombre)` |

```sql
SELECT localidad,
       COUNT(*) AS alumnos,
       MIN(apellidos) AS primero,
       LISTAGG(nombre, ', ') WITHIN GROUP (ORDER BY nombre) AS nombres
FROM   alumno
WHERE  localidad IN ('Elche', 'El Campello')
GROUP  BY localidad
ORDER  BY localidad;
```

| LOCALIDAD | ALUMNOS | PRIMERO | NOMBRES |
|---|---|---|---|
| El Campello | 3 | Alemany Pérez | Daniel, Elena, Jorge |
| Elche | 3 | Iborra Ferri | Rubén, Sofía, Víctor |

*2 files*

{{% paso-a-paso titulo="Orden lógico de ejecución de un SELECT completo" %}}
{{% etapa titulo="1. FROM i JOIN" %}}
Es construïx el conjunt de files de partida unint les taules indicades.
{{% /etapa %}}
{{% etapa titulo="2. WHERE" %}}
Filtra files **abans** d'agrupar. No pot usar funcions d'agregat.
{{% /etapa %}}
{{% etapa titulo="3. GROUP BY" %}}
Forma els grups amb les files que queden.
{{% /etapa %}}
{{% etapa titulo="4. HAVING" %}}
Filtra grups **després** d'agrupar. Ací sí que es poden usar `COUNT`, `AVG`…
{{% /etapa %}}
{{% etapa titulo="5. SELECT" %}}
Calcula les expressions i els àlies del resultat.
{{% /etapa %}}
{{% etapa titulo="6. ORDER BY" %}}
Ordena. És l'única fase que veu els àlies del SELECT.
{{% /etapa %}}
{{% etapa titulo="7. FETCH FIRST" %}}
Limita el nombre de files tornades.
{{% /etapa %}}
{{% /paso-a-paso %}}

### 2.3 Ordre d'avaluació: WHERE enfront de HAVING

Ja coneixes l'ordre lògic de les clàusules; ara es completa amb `GROUP BY` i `HAVING`:

```text
FROM  →  WHERE  →  GROUP BY  →  HAVING  →  SELECT  →  ORDER BY
  1        2          3            4         5           6
```

```mermaid
flowchart LR
    F["1 · FROM<br/>143 files"] --> W["2 · WHERE<br/>filtra FILES"]
    W --> G["3 · GROUP BY<br/>forma grups"]
    G --> H["4 · HAVING<br/>filtra GRUPS"]
    H --> S["5 · SELECT<br/>calcula columnes"]
    S --> O["6 · ORDER BY<br/>ordena"]
```

D'este ordre es deriven totes les regles pràctiques:

| Pregunta | Resposta | Perquè… |
|---|---|---|
| Puc usar un agregat al `WHERE`? | **No** (ORA-00934) | El `WHERE` s'avalua abans de formar els grups |
| Puc usar un agregat al `HAVING`? | **Sí** | El `HAVING` s'avalua després d'agrupar |
| Puc usar un àlies del `SELECT` al `HAVING`? | **No** en Oracle | El `SELECT` s'avalua després del `HAVING` |
| Puc usar un àlies del `SELECT` a l'`ORDER BY`? | **Sí** | L'`ORDER BY` és l'últim |
| Filtre per `nota_final < 5` al `WHERE` o al `HAVING`? | Al **`WHERE`** | És una condició sobre files, no sobre grups |

Les dos clàusules es combinen amb freqüència, i cadascuna fa una feina distinta:

```sql
-- Mòduls amb 3 suspesos o més: qui està suspés es decidix fila a fila
-- (WHERE); quants suspesos té el grup es decidix després (HAVING).
SELECT id_modulo,
       COUNT(*)                  AS suspensos,
       ROUND(AVG(nota_final), 2) AS media_de_los_suspensos
FROM   matricula
WHERE  nota_final < 5
GROUP  BY id_modulo
HAVING COUNT(*) >= 3
ORDER  BY suspensos DESC, id_modulo;
```

| ID_MODULO | SUSPENSOS | MEDIA_DE_LOS_SUSPENSOS |
|---|---|---|
| 3 | 4 | 3.81 |
| 18 | 3 | 3 |

*2 files*

{{% details title="Què passaria si moguérem la condició `nota_final < 5` al HAVING?" %}}
No és possible escriure-la tal qual: `HAVING nota_final < 5` dona `ORA-00979`, perquè `nota_final` no està al `GROUP BY`. Si l'escrius com `HAVING MIN(nota_final) < 5`, la consulta és vàlida però respon a **una altra** pregunta: «mòduls en què hi ha almenys un suspés», i el `COUNT(*)` comptaria **totes** les matrícules del mòdul, no només les suspeses.

Regla pràctica: **si la condició es pot decidir mirant una sola fila, va al `WHERE`**. Si necessita veure el grup sencer, va al `HAVING`. A més, filtrar al `WHERE` és més eficient, perquè es descarten files abans d'agrupar.
{{% /details %}}

### 2.4 Agrupar per diverses columnes i per expressions

El `GROUP BY` pot contindre diverses columnes: llavors es forma un grup per cada **combinació** de valors present en les dades (mai s'inventen combinacions que no existisquen).

```sql
SELECT curso_academico, convocatoria,
       COUNT(*)                  AS matriculas,
       COUNT(nota_final)         AS calificadas,
       ROUND(AVG(nota_final), 2) AS media
FROM   matricula
GROUP  BY curso_academico, convocatoria
ORDER  BY curso_academico, convocatoria;
```

| CURSO_ACADEMICO | CONVOCATORIA | MATRICULAS | CALIFICADAS | MEDIA |
|---|---|---|---|---|
| 2025-26 | 1 | 140 | 134 | 6.38 |
| 2025-26 | 2 | 3 | 3 | 5.25 |

*2 files*

També es pot agrupar per una **expressió**, sempre que la mateixa expressió aparega al `GROUP BY`:

```sql
SELECT CASE WHEN nota_final IS NULL THEN 'Sin calificar'
            WHEN nota_final < 5     THEN 'Insuficiente'
            WHEN nota_final < 7     THEN 'Suficiente / Bien'
            WHEN nota_final < 9     THEN 'Notable'
            ELSE                         'Sobresaliente'
       END      AS tramo,
       COUNT(*) AS matriculas
FROM   matricula
GROUP  BY CASE WHEN nota_final IS NULL THEN 'Sin calificar'
               WHEN nota_final < 5     THEN 'Insuficiente'
               WHEN nota_final < 7     THEN 'Suficiente / Bien'
               WHEN nota_final < 9     THEN 'Notable'
               ELSE                         'Sobresaliente'
          END
ORDER  BY matriculas DESC;
```

| TRAMO | MATRICULAS |
|---|---|
| Suficiente / Bien | 52 |
| Notable | 49 |
| Insuficiente | 27 |
| Sobresaliente | 9 |
| Sin calificar | 6 |

*5 files*

> [!TIP]
> Repetir el `CASE` complet és incòmode i propens a errors. En Oracle **no** es pot escriure `GROUP BY tramo` usant l'àlies, però sí que es pot donar nom al càlcul amb una **subconsulta al `FROM`**:
>
> ```sql
> SELECT tramo, COUNT(*) AS matriculas
> FROM  (SELECT CASE WHEN nota_final IS NULL THEN 'Sin calificar'
>                    WHEN nota_final < 5     THEN 'Insuficiente'
>                    ELSE                         'Aprobada'
>               END AS tramo
>        FROM   matricula)
> GROUP  BY tramo
> ORDER  BY matriculas DESC;
> ```

### 2.5 Laboratori d'agrupament

Al laboratori següent treballes amb les **143 matrícules reals** d'EduGest (hi ha 6 notes sense posar, dos d'elles al mòdul 0490). Tria la columna d'agrupament, la funció d'agregat i, si vols, una condició `HAVING`, i observa tres coses alhora: quines files formen cada grup, què torna l'agregat i quin SQL estàs construint en realitat.

Presta atenció especialment a dos experiments:

1. Agrupa per `id_modulo` i compara `COUNT(*)` amb `COUNT(nota_final)` al mòdul 0490: hi ha dos matrícules sense nota.
2. Marca la casella **«afegir `id_alumno` al SELECT»**: veuràs l'error `ORA-00979`, que és el que més voltes apareix als primers exercicis del tema.

{{< group-lab >}}

{{< quiz >}}
- q: "La taula `MATRICULA` té 143 files i 6 tenen `nota_final` a `NULL`. Què torna `SELECT COUNT(*), COUNT(nota_final) FROM matricula`?"
  options: ["143 i 143", "143 i 137", "137 i 137", "137 i 143"]
  answer: 1
  explain: "`COUNT(*)` compta files (143) i `COUNT(columna)` compta valors no nuls (137). Totes les funcions d'agregat excepte `COUNT(*)` ignoren els nuls."
- q: "Per què falla `SELECT localidad, nombre, COUNT(*) FROM alumno GROUP BY localidad`?"
  options: ["Perquè `COUNT(*)` no admet `GROUP BY`", "Perquè `nombre` no està al `GROUP BY` ni és un agregat: ORA-00979", "Perquè falta `ORDER BY`", "Perquè `localidad` admet nuls"]
  answer: 1
  explain: "Cada grup conté diversos noms distints i Oracle no pot triar-ne un. Caldria afegir `nombre` al `GROUP BY`, llevar-lo del `SELECT` o resumir-lo amb `MIN`, `MAX` o `LISTAGG`."
- q: "Vols els mòduls la nota mitjana dels quals supera 6, calculada només amb les matrícules de primera convocatòria. On va cada condició?"
  options: ["Les dos al `WHERE`", "Les dos al `HAVING`", "`convocatoria = 1` al `WHERE` i `AVG(nota_final) > 6` al `HAVING`", "`convocatoria = 1` al `HAVING` i `AVG(nota_final) > 6` al `WHERE`"]
  answer: 2
  explain: "La convocatòria es decidix mirant una sola fila, així que filtra al `WHERE` (i a més reduïx les files abans d'agrupar). La mitjana només existix una vegada format el grup: va al `HAVING`."
{{< /quiz >}}

---


{{< sesion n="3" h="2" tipo="t" >}}Composicions internes: INNER JOIN i diverses taules{{< /sesion >}}

## 3. Composicions internes: INNER JOIN

### 3.1 Quin problema resolen

La normalització (Tema 2) reparteix la informació per a no repetir-la: a `MATRICULA` no es guarda el nom de l'alumne, sinó el seu `id_alumno`. És el disseny correcte, però deixa un problema pràctic: l'acta d'avaluació necessita el **nom**, no l'identificador.

Una **composició** (*join*) és l'operació que torna a unir eixa informació: combina files de dues o més taules emparellant-les per una condició, normalment la igualtat entre una clau aliena i la clau primària a la qual apunta.

```mermaid
flowchart LR
    M["MATRICULA<br/>id_alumno = 3<br/>nota = 8"] -->|id_alumno| A["ALUMNO<br/>id_alumno = 3<br/>Noelia Verdú Espí"]
    M -->|id_modulo| MO["MODULO<br/>id_modulo = 2<br/>Bases de datos"]
```

{{% curiosidad titulo="El cost d'un producte cartesià" %}}
Un `FROM a, b` sense condició d'unió combina cada fila de `a` amb cada fila de `b`. Amb dues taules de 1.000 files n'ixen **1.000.000**, i amb tres de 1.000 files, mil milions. Per això oblidar la condició del `JOIN` és un dels errors que més tarden a executar-se.
{{% /curiosidad %}}

### 3.2 El punt de partida: el producte cartesià

Si escrius dues taules al `FROM` **sense condició**, Oracle combina **cada** fila de la primera amb **cada** fila de la segona. Això és el **producte cartesià**, i en SQL modern s'escriu `CROSS JOIN`:

```sql
SELECT (SELECT COUNT(*) FROM grupo) AS grupos,
       (SELECT COUNT(*) FROM ciclo) AS ciclos,
       (SELECT COUNT(*) FROM grupo g CROSS JOIN ciclo c) AS producto
FROM   dual;
```

| GRUPOS | CICLOS | PRODUCTO |
|---|---|---|
| 6 | 4 | 24 |

*1 fila*

El producte cartesià de `GRUPO` i `CICLO` té **24 files**: 6 × 4. Predir este número és just el que cal aprendre a fer. Les primeres files, ordenades, deixen veure el problema:

```sql
SELECT g.cod_grupo, g.cod_ciclo AS ciclo_del_grupo, c.cod_ciclo AS ciclo_de_la_tabla
FROM   grupo g CROSS JOIN ciclo c
ORDER  BY g.cod_grupo, c.cod_ciclo
FETCH FIRST 8 ROWS ONLY;
```

| COD_GRUPO | CICLO_DEL_GRUPO | CICLO_DE_LA_TABLA |
|---|---|---|
| 1ASIR | ASIR | ASIR |
| 1ASIR | ASIR | DAM |
| 1ASIR | ASIR | DAW |
| 1ASIR | ASIR | SMR |
| 1DAM | DAM | ASIR |
| 1DAM | DAM | DAM |
| 1DAM | DAM | DAW |
| 1DAM | DAM | SMR |

*8 files*

De les quatre files de cada grup, **només una té sentit**: la que empareja el grup amb *el seu* cicle. Una composició interna és exactament el producte cartesià **més la condició** que selecciona eixes files amb sentit.

> [!CAUTION]
> El producte cartesià creix multiplicant. Amb les 143 matrícules i les 46 faltes d'EduGest són 6 578 files; amb dues taules d'un milió de files serien un bilió. Si una consulta tarda moltíssim o torna un nombre absurd de files, el primer que cal sospitar és **una condició de composició oblidada**.

### 3.3 Sintaxi `JOIN … ON`

{{< sgbd "SQL estándar" >}}

```text
SELECT columnas
FROM   tabla1 alias1
       [INNER] JOIN tabla2 alias2 ON condició_d_emparellament
       [INNER] JOIN tabla3 alias3 ON condició_d_emparellament
WHERE  condicions_de_filtrat
```

| Element | Significat |
|---|---|
| `JOIN tabla2` | Taula que s'afig a la composició |
| `ON condición` | Com s'emparellen les files; és **obligatòria** en `JOIN` |
| `INNER` | Opcional: `JOIN` sense més és sempre una composició **interna** |
| `alias` | Nom curt de la taula; imprescindible per a qualificar les columnes |

Exemple senzill, cada mòdul amb el nom complet del seu cicle:

```sql
SELECT mo.codigo, mo.nombre AS modulo, c.nombre AS ciclo, mo.curso, mo.horas
FROM   modulo mo
       JOIN ciclo c ON c.cod_ciclo = mo.cod_ciclo
WHERE  mo.cod_ciclo = 'ASIR'
ORDER  BY mo.codigo;
```

| CODIGO | MODULO | CICLO | CURSO | HORAS |
|---|---|---|---|---|
| 0369 | Implantación de sistemas operativos | Administración de Sistemas Informáticos en Red | 1 | 224 |
| 0370 | Planificación y administración de redes | Administración de Sistemas Informáticos en Red | 1 | 192 |
| 0371 | Fundamentos de hardware | Administración de Sistemas Informáticos en Red | 1 | 96 |
| 0372 | Gestión de bases de datos | Administración de Sistemas Informáticos en Red | 1 | 160 |
| 0373 | Lenguajes de marcas y sistemas de gestión de información | Administración de Sistemas Informáticos en Red | 1 | 96 |

*5 files*

Resultat esperat: **5 files**, les mateixes que mòduls d'ASIR. Una composició per clau aliena cap a una clau primària **no pot multiplicar files**: cada mòdul té exactament un cicle. Esta és la comprovació més útil del tema.

> [!IMPORTANT]
> **Usa sempre àlies de taula i qualifica totes les columnes.** No és una qüestió estètica:
>
> - `MODULO` i `CICLO` tenen les dos una columna `nombre`. Sense qualificar, `SELECT nombre` donaria `ORA-00918: column ambiguously defined`.
> - Quan llegisques la consulta mesos després, `c.nombre` diu d'on ix la dada; `nombre` no.
> - Si algú afig una columna a una taula, una consulta sense qualificar pot tornar-se ambigua de sobte i deixar de compilar.

### 3.4 Composició de tres i quatre taules

Les composicions s'encadenen. El mètode és sempre el mateix: **traçar el camí de claus alienes** des de la taula que té la dada que busques fins a la que té la dada que vols mostrar.

```mermaid
flowchart LR
    F[FALTA_ASISTENCIA] -->|id_matricula| M[MATRICULA]
    M -->|id_alumno| A[ALUMNO]
    M -->|id_modulo| MO[MODULO]
    MO -->|cod_ciclo| C[CICLO]
    A -->|cod_grupo| G[GRUPO]
```

Tres taules: alumnat de 2DAM amb el seu grup i el nom del cicle.

```sql
SELECT a.apellidos || ', ' || a.nombre AS alumno,
       g.cod_grupo, g.turno, c.nombre AS ciclo
FROM   alumno a
       JOIN grupo g ON g.cod_grupo = a.cod_grupo
       JOIN ciclo c ON c.cod_ciclo = g.cod_ciclo
WHERE  g.cod_grupo = '2DAM'
ORDER  BY a.apellidos;
```

| ALUMNO | COD_GRUPO | TURNO | CICLO |
|---|---|---|---|
| Alemany Vidal, Martina | 2DAM | M | Desarrollo de Aplicaciones Multiplataforma |
| Belda Quiles, Lucía | 2DAM | M | Desarrollo de Aplicaciones Multiplataforma |
| Brotons Iborra, Hugo | 2DAM | M | Desarrollo de Aplicaciones Multiplataforma |
| Cerdá Tomás, Nerea | 2DAM | M | Desarrollo de Aplicaciones Multiplataforma |
| Domènech Quiles, María | 2DAM | M | Desarrollo de Aplicaciones Multiplataforma |
| Ripoll Agulló, Iván | 2DAM | M | Desarrollo de Aplicaciones Multiplataforma |

*6 files*

Quatre taules: l'assignació docent de 2DAM, que creua `IMPARTE` amb `MODULO`, `GRUPO` i `PROFESOR`.

```sql
SELECT g.cod_grupo, mo.codigo, mo.nombre AS modulo,
       p.apellidos AS profesor, i.horas_semanales
FROM   imparte i
       JOIN modulo mo   ON mo.id_modulo   = i.id_modulo
       JOIN grupo g     ON g.cod_grupo    = i.cod_grupo
       JOIN profesor p  ON p.id_profesor  = i.id_profesor
WHERE  i.cod_grupo = '2DAM'
ORDER  BY mo.codigo;
```

| COD_GRUPO | CODIGO | MODULO | PROFESOR | HORAS_SEMANALES |
|---|---|---|---|---|
| 2DAM | 0486 | Acceso a datos | Ferrándiz Mora | 4 |
| 2DAM | 0488 | Desarrollo de interfaces | Navarro Ruiz | 4 |
| 2DAM | 0489 | Programación multimedia y dispositivos móviles | Cano Vidal | 3 |
| 2DAM | 0490 | Programación de servicios y procesos | Ferrándiz Mora | 2 |
| 2DAM | 0491 | Sistemas de gestión empresarial | Pastor Gil | 3 |

*5 files*

> [!TIP]
> **Construïx les composicions d'una en una.** Afig una taula, executa `SELECT COUNT(*)`, comprova que el número és el que esperes i passa a la següent. Així, quan el número se'n vaja de mare, sabràs exactament quin `JOIN` l'ha causat. La pràctica 4.7 està muntada sobre esta tècnica.

### 3.5 Composicions i agrupaments junts

Allò habitual en un informe és compondre i després resumir. L'ordre lògic no canvia: primer `FROM` (amb les seues composicions), després `WHERE`, després `GROUP BY`.

```sql
SELECT c.cod_ciclo, c.nombre AS ciclo,
       COUNT(m.id_matricula)     AS matriculas,
       COUNT(m.nota_final)       AS calificadas,
       ROUND(AVG(m.nota_final), 2) AS media
FROM   ciclo c
       JOIN modulo mo    ON mo.cod_ciclo = c.cod_ciclo
       JOIN matricula m  ON m.id_modulo  = mo.id_modulo
GROUP  BY c.cod_ciclo, c.nombre
ORDER  BY c.cod_ciclo;
```

| COD_CICLO | CICLO | MATRICULAS | CALIFICADAS | MEDIA |
|---|---|---|---|---|
| ASIR | Administración de Sistemas Informáticos en Red | 25 | 24 | 7.07 |
| DAM | Desarrollo de Aplicaciones Multiplataforma | 68 | 65 | 6.29 |
| DAW | Desarrollo de Aplicaciones Web | 50 | 48 | 6.09 |

*3 files*

Falta un dels quatre cicles: **SMR no apareix** perquè no té mòduls i, per tant, cap fila sobreviu a la composició interna. Eixe és precisament el problema que resol l'apartat 4.

> [!NOTE]
> Al `GROUP BY` s'han posat `c.cod_ciclo` **i** `c.nombre`, encara que el nom depenga funcionalment del codi. Oracle exigix al `GROUP BY` totes les columnes no agregades del `SELECT`. Quan agrupes per una entitat, inclou la seua clau primària al `GROUP BY`: garantix que no es fonguen dues entitats amb el mateix nom.

### 3.6 Sintaxi antiga i altres formes de composició

#### Sintaxi amb comes (heretada)

Abans de l'estàndard SQL-92, la condició de composició s'escrivia al `WHERE`:

```sql
-- Sintaxi antiga: NO l'uses en codi nou
SELECT mo.codigo, c.nombre
FROM   modulo mo, ciclo c
WHERE  c.cod_ciclo = mo.cod_ciclo
AND    mo.curso = 2;
```

Torna exactament el mateix que la versió amb `JOIN … ON`, però té dos problemes greus que expliquen per què la norma professional és no usar-la:

1. **Barreja** les condicions de composició amb les de filtrat: en una consulta de sis taules i deu condicions és impossible veure d'un colp d'ull si falta un emparellament.
2. Si **oblides** una condició, no hi ha cap error: obtens silenciosament un producte cartesià parcial amb resultats erronis.

Has de saber llegir-la perquè apareix en moltíssim codi heretat i en documentació antiga d'Oracle, però escriu sempre `JOIN … ON`.

#### `USING`

Quan les columnes que s'emparellen tenen **el mateix nom** a les dues taules, `USING` abreuja:

```sql
SELECT codigo, cod_ciclo, nombre_ciclo
FROM   (SELECT mo.codigo, mo.cod_ciclo, c.nombre AS nombre_ciclo
        FROM   modulo mo JOIN ciclo c USING (cod_ciclo))
FETCH FIRST 3 ROWS ONLY;
```

> [!WARNING]
> `USING` té una peculiaritat que sorprén: la columna comuna **deixa de pertànyer a una taula concreta** i no es pot qualificar. `SELECT mo.cod_ciclo … USING (cod_ciclo)` dona `ORA-25154: column part of USING clause cannot have qualifier`. Cal escriure `cod_ciclo` sense àlies.

#### `NATURAL JOIN`

`NATURAL JOIN` empareja automàticament per **totes** les columnes que tinguen el mateix nom a les dues taules. Sona còmode i és perillós:

```sql
SELECT COUNT(*) FROM modulo NATURAL JOIN ciclo;
```

| COUNT(*) |
|---|
| 0 |

*1 fila*

Zero files. `MODULO` i `CICLO` compartixen **dos** noms de columna: `cod_ciclo` **i** `nombre`. El `NATURAL JOIN` exigix que coincidisquen els dos, i cap mòdul es diu igual que el seu cicle.

> [!CAUTION]
> **No uses `NATURAL JOIN` en codi real.** La composició depén dels noms de les columnes, així que afegir una columna anomenada `nombre`, `fecha_alta` o `observaciones` a una taula pot canviar en silenci el resultat de consultes que portaven anys funcionant. Escriu sempre la condició explícitament a l'`ON`.

#### Condicions a l'`ON` o al `WHERE`

En una composició **interna** és igual posar una condició de filtrat a l'`ON` o al `WHERE`: el resultat és idèntic, i l'optimitzador d'Oracle ho reorganitza igual.

```sql
-- Equivalents (composició interna)
FROM modulo mo JOIN ciclo c ON c.cod_ciclo = mo.cod_ciclo AND mo.curso = 2
FROM modulo mo JOIN ciclo c ON c.cod_ciclo = mo.cod_ciclo WHERE mo.curso = 2
```

En una composició **externa** **no** són equivalents, i la diferència és una de les trampes més repetides del mòdul: s'analitza a l'apartat 4.4. Convenció recomanada: a l'`ON`, només el que empareja; al `WHERE`, el que filtra.

### 3.7 Laboratori de composicions

El laboratori següent compon dues taules reals d'EduGest: els 6 **grups** (un d'ells, 2ASIR, sense tutor assignat) i 7 **professors** (dos dels quals no són tutors de cap grup). Canvia el tipus de composició i observa tres coses: l'SQL que es genera, quines files es conserven i quantes files ixen.

Abans de tocar res, prediu els números: quantes files hauria de tornar cada tipus de composició? Després comprova-ho. Usa també les dos caselles inferiors, que reproduïxen els dos errors clàssics del tema: el filtre al `WHERE` que anul·la una composició externa i la diferència entre posar una condició a l'`ON` o al `WHERE`.

{{< join-lab >}}

{{< quiz >}}
- q: "Per què `SELECT nombre FROM modulo mo JOIN ciclo c ON c.cod_ciclo = mo.cod_ciclo` dona ORA-00918?"
  options: ["Perquè falta `INNER`", "Perquè `nombre` existix a les dues taules i no s'ha qualificat", "Perquè `cod_ciclo` admet nuls", "Perquè cal usar `USING`"]
  answer: 1
  explain: "ORA-00918 és *column ambiguously defined*. Cal escriure `mo.nombre` o `c.nombre`. És la raó per la qual es qualifiquen sempre totes les columnes."
{{< /quiz >}}

---


{{< sesion n="5" h="1" tipo="t" >}}Composicions externes i autocomposició{{< /sesion >}}

## 4. Composicions externes: LEFT, RIGHT i FULL JOIN

### 4.1 Quin problema resolen

Una composició interna només torna les files que **emparellen**. Això fa desaparéixer silenciosament informació que moltes vegades és la més important de l'informe:

| Pregunta d'EduGest | El que la composició interna oculta |
|---|---|
| Quants grups té cada cicle? | SMR, que no en té cap |
| Qui és el tutor de cada grup? | 2ASIR, que encara no té tutor |
| Quants alumnes té cada grup? | 2ASIR, sense alumnat matriculat |
| Quin professorat hi ha en cada departament? | Matemàtiques, sense professorat assignat |
| Quins alumnes tenen matrícula? | Els 3 alumnes sense grup ni matrícula |

En tots estos casos, la fila «sense parella» és justament la que cal detectar i resoldre. Una **composició externa** conserva les files d'una taula encara que no troben parella en l'altra, omplint amb `NULL` les columnes que falten.

| Tipus | Conserva | Quan usar-lo |
|---|---|---|
| `A LEFT [OUTER] JOIN B` | **Totes** les files d'`A` | «Tots els grups, amb el seu tutor si en tenen» |
| `A RIGHT [OUTER] JOIN B` | **Totes** les files de `B` | El mateix al contrari; poc usat a la pràctica |
| `A FULL [OUTER] JOIN B` | Totes les d'`A` **i** totes les de `B` | Conciliar dos llistats: detectar orfes en ambdós costats |

La paraula `OUTER` és opcional: `LEFT JOIN` i `LEFT OUTER JOIN` són el mateix.

### 4.2 `LEFT JOIN`: el cas habitual

```sql
SELECT g.cod_grupo, g.cod_ciclo, g.turno, g.id_tutor,
       p.apellidos || ', ' || p.nombre AS tutor
FROM   grupo g
       LEFT JOIN profesor p ON p.id_profesor = g.id_tutor
ORDER  BY g.cod_grupo;
```

| COD_GRUPO | COD_CICLO | TURNO | ID_TUTOR | TUTOR |
|---|---|---|---|---|
| 1ASIR | ASIR | M | 105 | Brotons Sala, Elena |
| 1DAM | DAM | M | 103 | Ferrándiz Mora, Lucía |
| 1DAW | DAW | T | 106 | Cano Vidal, Raúl |
| 2ASIR | ASIR | M | (null) | (null) |
| 2DAM | DAM | M | 104 | Navarro Ruiz, Andrés |
| 2DAW | DAW | T | 107 | Gómez Pérez, Nuria |

*6 files*

Resultat esperat: **les 6 files de `GRUPO`**, perquè `GRUPO` està a l'esquerra. La fila de 2ASIR es conserva amb totes les columnes de `PROFESOR` a `NULL`. Per a presentar-ho es combina amb les funcions del tema 4:

```sql
SELECT g.cod_grupo,
       NVL(p.apellidos || ', ' || p.nombre, '(sin tutor asignado)') AS tutor
FROM   grupo g
       LEFT JOIN profesor p ON p.id_profesor = g.id_tutor
ORDER  BY g.cod_grupo;
```

Un altre cas clàssic, amb la composició en el sentit 1:N. Tots els cicles, amb els seus grups:

```sql
SELECT c.cod_ciclo, c.nombre AS ciclo, g.cod_grupo, g.turno
FROM   ciclo c
       LEFT JOIN grupo g ON g.cod_ciclo = c.cod_ciclo
ORDER  BY c.cod_ciclo, g.cod_grupo;
```

| COD_CICLO | CICLO | COD_GRUPO | TURNO |
|---|---|---|---|
| ASIR | Administración de Sistemas Informáticos en Red | 1ASIR | M |
| ASIR | Administración de Sistemas Informáticos en Red | 2ASIR | M |
| DAM | Desarrollo de Aplicaciones Multiplataforma | 1DAM | M |
| DAM | Desarrollo de Aplicaciones Multiplataforma | 2DAM | M |
| DAW | Desarrollo de Aplicaciones Web | 1DAW | T |
| DAW | Desarrollo de Aplicaciones Web | 2DAW | T |
| SMR | Sistemas Microinformáticos y Redes | (null) | (null) |

*7 files*

Set files: les sis parelles reals més SMR, que apareix **una vegada** amb les columnes de grup nul·les.

### 4.3 COUNT en una composició externa: COUNT(*) enfront de COUNT(columna)

Ací els dos conceptes del tema es creuen i produïxen l'error més subtil del tema:

```sql
SELECT g.cod_grupo,
       COUNT(*)           AS filas_del_grupo,
       COUNT(a.id_alumno) AS alumnos
FROM   grupo g
       LEFT JOIN alumno a ON a.cod_grupo = g.cod_grupo
GROUP  BY g.cod_grupo
ORDER  BY g.cod_grupo;
```

| COD_GRUPO | FILAS_DEL_GRUPO | ALUMNOS |
|---|---|---|
| 1ASIR | 5 | 5 |
| 1DAM | 7 | 7 |
| 1DAW | 6 | 6 |
| 2ASIR | **1** | **0** |
| 2DAM | 6 | 6 |
| 2DAW | 5 | 5 |

*6 files*

> [!IMPORTANT]
> En una composició externa, la fila sense parella **existix** (per això `COUNT(*)` val 1 per a 2ASIR) però **no té dades** de la taula opcional (per això `COUNT(a.id_alumno)` val 0). En un `LEFT JOIN`, compta sempre una **columna de la taula opcional**, mai `COUNT(*)`, si el que vols és «quants fills té cada pare». El mateix val per a `SUM`, que tornarà `NULL` en compte de 0: embolica'l en `NVL(SUM(...), 0)`.

### 4.4 La trampa del WHERE: com anul·lar una composició externa

```sql
-- (a) INCORRECTA: el WHERE descarta la fila nul·la que acaba de crear el LEFT JOIN
SELECT g.cod_grupo, p.apellidos AS tutor
FROM   grupo g LEFT JOIN profesor p ON p.id_profesor = g.id_tutor
WHERE  p.id_departamento = 1;
-- 5 files: 2ASIR desapareix

-- (b) CORRECTA: la condició sobre la taula opcional va a l'ON
SELECT g.cod_grupo, p.apellidos AS tutor
FROM   grupo g LEFT JOIN profesor p
       ON p.id_profesor = g.id_tutor AND p.id_departamento = 1;
-- 6 files: 2ASIR apareix amb tutor nul
```

L'explicació està en l'ordre d'avaluació: el `LEFT JOIN` crea la fila de 2ASIR amb `p.id_departamento` a `NULL`; després, el `WHERE` avalua `NULL = 1`, que és `UNKNOWN`, i descarta la fila. Un `WHERE` sobre una columna de la taula opcional **converteix un `LEFT JOIN` en un `INNER JOIN`**.

> [!WARNING]
> **Regla per a recordar:** en una composició externa, les condicions sobre la **taula opcional** van a l'`ON`; les condicions sobre la **taula conservada** poden anar al `WHERE`.
>
> Hi ha una excepció deliberada: `WHERE columna_opcional IS NULL`, que és just el contrari, com es veu a l'apartat següent.

### 4.5 Anticomposició: buscar el que NO existix

Si el que vols són precisament les files **sense parella**, el patró és composició externa + `IS NULL` sobre una columna de la taula opcional. Es diu *anti-join*:

```sql
-- Alumnat sense cap matrícula
SELECT a.id_alumno, a.nombre, a.apellidos, a.cod_grupo
FROM   alumno a
       LEFT JOIN matricula m ON m.id_alumno = a.id_alumno
WHERE  m.id_matricula IS NULL
ORDER  BY a.id_alumno;
```

| ID_ALUMNO | NOMBRE | APELLIDOS | COD_GRUPO |
|---|---|---|---|
| 30 | Zoe | Iborra Valero | (null) |
| 31 | Lucas | Agulló Cerdá | (null) |
| 32 | Irene | Belda Iborra | (null) |

*3 files*

Són els tres alumnes que ni tenen grup ni estan matriculats: una dada de qualitat de dades que secretaria ha de revisar abans de tancar la matrícula.

> [!TIP]
> Tria per a l'`IS NULL` una columna de la taula opcional **que no admeta nuls** en la seua taula (normalment la seua clau primària). Si triares una columna que sí que admet nuls, no podries distingir «no hi ha parella» de «hi ha parella amb eixe valor nul».

### 4.6 `FULL OUTER JOIN`

Conserva les files de les dues taules. És l'eina per a **conciliar** dos llistats:

```sql
-- Conciliació grup ↔ tutor: grups sense tutor i professorat que no tutoritza
SELECT g.cod_grupo, p.id_profesor, p.apellidos
FROM   grupo g
       FULL OUTER JOIN profesor p ON p.id_profesor = g.id_tutor
WHERE  g.cod_grupo IS NULL OR p.id_profesor IS NULL
ORDER  BY g.cod_grupo, p.id_profesor;
```

| COD_GRUPO | ID_PROFESOR | APELLIDOS |
|---|---|---|
| 2ASIR | (null) | (null) |
| (null) | 101 | Soler Ivars |
| (null) | 102 | Pastor Gil |
| (null) | 108 | Lillo Martí |
| (null) | 109 | Ortiz Llorca |
| (null) | 110 | Ramos Climent |
| (null) | 111 | Vicent Ribes |
| (null) | 112 | Esteve Juan |

*8 files*

Un grup sense tutor i set professors que no són tutors de cap grup. Sense el `WHERE`, la composició tornaria 13 files: 5 parelles + 1 + 7.

## 5. Autocomposició i altres composicions

### 5.1 Autocomposició (*self join*)

Una taula també es pot compondre **amb si mateixa**. Ocorre sempre que una relació s'establix entre files de la mateixa taula: el cap d'un empleat, el prerequisit d'un mòdul, el professor que dirigix un departament del qual forma part.

La clau tècnica és que **calen dos àlies distints** perquè Oracle (i el lector) sàpia de quina «còpia» de la taula es parla.

A EduGest, cada professor pertany a un departament i cada departament té un cap que és, al seu torn, un professor. Per a posar al costat de cada docent el nom de la seua cap de departament, `PROFESOR` apareix **dues voltes**:

```sql
SELECT p.apellidos || ', ' || p.nombre AS profesor,
       d.nombre                        AS departamento,
       NVL(j.apellidos || ', ' || j.nombre, '(vacante)') AS jefe_departamento,
       CASE WHEN j.id_profesor = p.id_profesor THEN 'Sí' ELSE 'No' END AS es_el_jefe
FROM   profesor p
       JOIN departamento d  ON d.id_departamento = p.id_departamento
       LEFT JOIN profesor j ON j.id_profesor     = d.id_jefe
WHERE  d.id_departamento IN (2, 3, 5)
ORDER  BY d.nombre, p.apellidos;
```

| PROFESOR | DEPARTAMENTO | JEFE_DEPARTAMENTO | ES_EL_JEFE |
|---|---|---|---|
| Esteve Juan, David | Administración y Gestión | Esteve Juan, David | Sí |
| Ortiz Llorca, Carmen | Formación y Orientación Laboral | Ortiz Llorca, Carmen | Sí |
| Ramos Climent, Sergio | Formación y Orientación Laboral | Ortiz Llorca, Carmen | No |
| Vicent Ribes, Laura | Inglés | Vicent Ribes, Laura | Sí |

*4 files*

Observa els dos àlies de `PROFESOR`: `p` és «el docent» i `j` és «el seu cap de departament». El `LEFT JOIN` és necessari perquè un departament pot tindre la cap vacant.

> [!IMPORTANT]
> En una autocomposició, els àlies no són opcionals: sense ells, `WHERE id_jefe = id_profesor` seria ambigu i Oracle donaria `ORA-00918`. Tria àlies que diguen **el paper** que juga cada còpia (`p`/`j`, `empleado`/`jefe`, `modulo`/`prerrequisito`), no `t1`/`t2`.

### 5.2 Autocomposició per a comparar files entre si

L'altre ús de l'autocomposició és comparar files de la mateixa taula: duplicats, parelles, coincidències.

```sql
-- Parelles d'alumnes del mateix grup que viuen a la mateixa localitat
SELECT a.cod_grupo, a.localidad,
       a.apellidos AS alumno_1, b.apellidos AS alumno_2
FROM   alumno a
       JOIN alumno b ON b.cod_grupo = a.cod_grupo
                    AND b.localidad = a.localidad
                    AND b.id_alumno > a.id_alumno
WHERE  a.cod_grupo = '1DAM'
ORDER  BY a.localidad, a.apellidos, b.apellidos;
```

| COD_GRUPO | LOCALIDAD | ALUMNO_1 | ALUMNO_2 |
|---|---|---|---|
| 1DAM | Alicante | Brotons Soriano | Cerdá Pérez |
| 1DAM | Alicante | Ferri Baeza | Brotons Soriano |
| 1DAM | Alicante | Ferri Baeza | Brotons Soriano |
| 1DAM | Alicante | Ferri Baeza | Cerdá Pérez |
| 1DAM | Alicante | Ferri Baeza | Cerdá Pérez |
| 1DAM | Alicante | Ferri Baeza | Ferri Baeza |
| 1DAM | Sant Joan d'Alacant | Verdú Espí | Quiles Marco |

*7 files*

Dos detalls imprescindibles:

- La condició `b.id_alumno > a.id_alumno` evita que un alumne s'emparelle **amb si mateix** i que cada parella isca **dues voltes** (A-B i B-A). Si la lleves, les 7 files es convertixen en 22.
- A 1DAM hi ha dos alumnes distints que tenen per cognom «Ferri Baeza» (Adrián i Paula), cosa que explica les files aparentment repetides: són parelles diferents amb cognoms iguals. És un bon recordatori que **el cognom no identifica una persona**: per això la clau primària és `id_alumno`.

{{< sesion n="7" h="1" tipo="t" >}}Subconsultes i EXISTS{{< /sesion >}}

## 6. Subconsultes

### 6.1 Quin problema resolen

Hi ha preguntes que no es poden respondre d'una vegada perquè necessiten **una dada que al seu torn cal calcular**: «els mòduls amb més hores que la mitjana» exigix calcular primer la mitjana. Una **subconsulta** és una consulta `SELECT` escrita dins d'una altra, entre parèntesis, el resultat de la qual usa la consulta exterior.

Segons **on** s'escriga i **quantes files** torne, es comporta de forma distinta:

| Posició | Nom | Ha de tornar | Exemple d'ús |
|---|---|---|---|
| Al `WHERE` / `HAVING` | Subconsulta d'**una fila** | 1 fila, 1 columna | `horas > (SELECT AVG(horas) …)` |
| Al `WHERE` / `HAVING` | Subconsulta de **diverses files** | N files, 1 columna | `id_alumno IN (SELECT …)` |
| Al `FROM` | Taula en línia | N files, N columnes | Resumir abans de compondre |
| Al `SELECT` | Subconsulta **escalar** | 1 fila, 1 columna | Una dada calculada per fila |
| Amb `EXISTS` | Subconsulta d'**existència** | El que siga | «Hi ha alguna fila que…?» |

### 6.2 Subconsultes d'una fila

S'usen amb els operadors de comparació normals (`=`, `<>`, `>`, `<`, `>=`, `<=`). La subconsulta ha de tornar **exactament una fila i una columna**; normalment ho garantix una funció d'agregat sense `GROUP BY`.

```sql
-- Mitjana d'hores dels mòduls de DAM: 132
SELECT codigo, nombre, horas
FROM   modulo
WHERE  cod_ciclo = 'DAM'
AND    horas > (SELECT AVG(horas) FROM modulo WHERE cod_ciclo = 'DAM')
ORDER  BY horas DESC, codigo;
```

| CODIGO | NOMBRE | HORAS |
|---|---|---|
| 0485 | Programación | 256 |
| 0483 | Sistemas informáticos | 160 |
| 0484 | Bases de datos | 160 |

*3 files*

> [!WARNING]
> Si una subconsulta d'una fila en torna **més d'una**, Oracle llança `ORA-01427: single-row subquery returns more than one row`. És l'error típic de `WHERE horas > (SELECT horas FROM modulo WHERE cod_ciclo = 'DAM')`: hi ha 10 mòduls de DAM, així que hi ha 10 valors. La solució és o resumir (`AVG`, `MAX`…) o usar un operador de diverses files (`ANY`, `ALL`, `IN`).

Les subconsultes també funcionen al `HAVING`, quan la condició sobre el grup es compara amb un valor global:

```sql
-- Mòduls la nota mitjana dels quals supera la mitjana general del centre (6,36)
SELECT id_modulo, COUNT(nota_final) AS calificadas, ROUND(AVG(nota_final), 2) AS media
FROM   matricula
GROUP  BY id_modulo
HAVING AVG(nota_final) > (SELECT AVG(nota_final) FROM matricula)
ORDER  BY media DESC
FETCH FIRST 5 ROWS ONLY;
```

| ID_MODULO | CALIFICADAS | MEDIA |
|---|---|---|
| 21 | 4 | 8 |
| 20 | 5 | 7.4 |
| 5 | 7 | 7.21 |
| 24 | 5 | 6.85 |
| 22 | 5 | 6.8 |

*5 files*

### 6.3 Subconsultes de diverses files: IN, ANY i ALL

| Operador | Significat | Equivalent |
|---|---|---|
| `IN (subconsulta)` | Igual a **algun** dels valors | `= ANY` |
| `NOT IN (subconsulta)` | Distint de **tots** els valors | `<> ALL` |
| `> ANY (subconsulta)` | Major que **almenys un**: major que el **mínim** | `> MIN(…)` |
| `> ALL (subconsulta)` | Major que **tots**: major que el **màxim** | `> MAX(…)` |
| `< ANY` / `< ALL` | Menor que el màxim / menor que el mínim | |

```sql
-- Alumnat matriculat en Bases de dades (codi 0484, en qualsevol cicle)
SELECT a.id_alumno, a.apellidos || ', ' || a.nombre AS alumno, a.cod_grupo
FROM   alumno a
WHERE  a.id_alumno IN (SELECT m.id_alumno
                       FROM   matricula m
                              JOIN modulo mo ON mo.id_modulo = m.id_modulo
                       WHERE  mo.codigo = '0484')
ORDER  BY a.cod_grupo, a.apellidos;
```

| ID_ALUMNO | ALUMNO | COD_GRUPO |
|---|---|---|
| 5 | Brotons Soriano, Andrea | 1DAM |
| 6 | Cerdá Pérez, Tomás | 1DAM |
| 1 | Ferri Baeza, Adrián | 1DAM |
| 4 | Ferri Baeza, Paula | 1DAM |
| 2 | Iborra Ferri, Rubén | 1DAM |
| 7 | Quiles Marco, Valeria | 1DAM |
| 3 | Verdú Espí, Noelia | 1DAM |
| 18 | Alemany Pérez, Daniel | 1DAW |
| 16 | Espí Marco, Julia | 1DAW |
| 17 | Iborra Alemany, Jorge | 1DAW |
| 15 | Soriano Domènech, Manuel | 1DAW |
| 19 | Torregrosa Planelles, Alba | 1DAW |
| 14 | Valero Cerdá, Carla | 1DAW |

*13 files*

```sql
-- Mòduls de DAW amb més hores que el mòdul més curt d'ASIR (96 h)
SELECT codigo, nombre, horas
FROM   modulo
WHERE  cod_ciclo = 'DAW'
AND    horas > ANY (SELECT horas FROM modulo WHERE cod_ciclo = 'ASIR')
ORDER  BY horas, codigo;
```

| CODIGO | NOMBRE | HORAS |
|---|---|---|
| 0615 | Diseño de interfaces web | 120 |
| 0373 | Lenguajes de marcas y sistemas de gestión de información | 128 |
| 0612 | Desarrollo web en entorno cliente | 140 |
| 0483 | Sistemas informáticos | 160 |
| 0484 | Bases de datos | 160 |
| 0613 | Desarrollo web en entorno servidor | 160 |
| 0485 | Programación | 256 |

*7 files*

> [!TIP]
> `ANY` i `ALL` són difícils de llegir. Tradueix sempre a la forma amb agregat abans d'escriure'ls: `> ANY` és `> (SELECT MIN(...))` i `> ALL` és `> (SELECT MAX(...))`. Si dubtes, escriu la versió amb `MIN`/`MAX`: és equivalent i molt més clara. L'única diferència pràctica apareix amb subconsultes buides.

### 6.4 La trampa de NOT IN amb nuls

```sql
-- Professorat que NO és tutor de cap grup
SELECT COUNT(*) AS filas
FROM   profesor
WHERE  id_profesor NOT IN (SELECT id_tutor FROM grupo);
```

| FILAS |
|---|
| 0 |

*1 fila*

Zero files, quan sabem que hi ha set professors sense tutoria. **No és un error d'Oracle**: és la lògica de tres valors del tema 4. La subconsulta torna sis valors, i un d'ells és `NULL` (2ASIR no té tutor). Llavors:

```text
id_profesor NOT IN (105, 103, 106, NULL, 104, 107)
   ≡  id_profesor <> 105 AND … AND id_profesor <> NULL
   ≡  TRUE AND … AND UNKNOWN
   ≡  UNKNOWN   →  el WHERE no deixa passar cap fila
```

Hi ha dues formes correctes d'escriure-ho:

```sql
-- (a) Excloure els nuls de la subconsulta
SELECT id_profesor, apellidos
FROM   profesor
WHERE  id_profesor NOT IN (SELECT id_tutor FROM grupo WHERE id_tutor IS NOT NULL)
ORDER  BY id_profesor;

-- (b) NOT EXISTS: immune als nuls (recomanada)
SELECT p.id_profesor, p.apellidos || ', ' || p.nombre AS profesor
FROM   profesor p
WHERE  NOT EXISTS (SELECT 1 FROM grupo g WHERE g.id_tutor = p.id_profesor)
ORDER  BY p.id_profesor;
```

| ID_PROFESOR | PROFESOR |
|---|---|
| 101 | Soler Ivars, Marta |
| 102 | Pastor Gil, Javier |
| 108 | Lillo Martí, Pablo |
| 109 | Ortiz Llorca, Carmen |
| 110 | Ramos Climent, Sergio |
| 111 | Vicent Ribes, Laura |
| 112 | Esteve Juan, David |

*7 files*

> [!CAUTION]
> **`NOT IN` sobre una subconsulta que puga tornar `NULL` és un error de disseny esperant a ocórrer.** El dia que algú deixe una clau aliena a nul, la consulta deixarà de tornar files sense donar cap error. Usa `NOT EXISTS` o afig `IS NOT NULL` a la subconsulta. `IN` (afirmatiu) no patix este problema: amb nuls simplement no empareja.

### 6.5 Subconsultes correlacionades i EXISTS

Una subconsulta és **correlacionada** quan fa referència a una columna de la consulta exterior. Conceptualment s'avalua **una vegada per cada fila** de la consulta exterior, amb el valor d'eixa fila.

```sql
-- Matrícules de 2DAW la nota de les quals supera la mitjana del SEU mòdul
SELECT a.apellidos || ', ' || a.nombre AS alumno, mo.codigo, m.nota_final,
       (SELECT ROUND(AVG(m2.nota_final), 2)
        FROM   matricula m2
        WHERE  m2.id_modulo = m.id_modulo) AS media_del_modulo
FROM   matricula m
       JOIN alumno a  ON a.id_alumno  = m.id_alumno
       JOIN modulo mo ON mo.id_modulo = m.id_modulo
WHERE  a.cod_grupo = '2DAW'
AND    m.nota_final > (SELECT AVG(m2.nota_final)
                       FROM   matricula m2
                       WHERE  m2.id_modulo = m.id_modulo)
ORDER  BY mo.codigo, m.nota_final DESC;
```

| ALUMNO | CODIGO | NOTA_FINAL | MEDIA_DEL_MODULO |
|---|---|---|---|
| Carbonell Soriano, Elena | 0612 | 8.75 | 6.38 |
| Sala Brotons, Mateo | 0612 | 6.5 | 6.38 |
| Carbonell Soriano, Elena | 0613 | 7.25 | 5.8 |
| Amorós Guillem, Sara | 0613 | 6 | 5.8 |
| Verdú Castelló, Nicolás | 0614 | 8 | 4.9 |
| Sala Brotons, Mateo | 0614 | 7.5 | 4.9 |
| Sala Brotons, Mateo | 0615 | 9.25 | 6.75 |
| Amorós Guillem, Sara | 0615 | 7.25 | 6.75 |
| Planelles Marco, Sofía | 0615 | 7 | 6.75 |

*9 files*

La correlació està en `m2.id_modulo = m.id_modulo`: `m` és la fila exterior i `m2` recorre totes les matrícules d'**eixe** mòdul. Sense la correlació, la mitjana seria la general del centre i el resultat un altre.

**`EXISTS`** és un operador que només pregunta si la subconsulta torna **almenys una fila**; no mira els valors. Per això dins s'escriu `SELECT 1` (o `SELECT *`): és igual.

```sql
-- Alumnat amb almenys una falta no justificada
SELECT a.id_alumno, a.apellidos || ', ' || a.nombre AS alumno, a.cod_grupo
FROM   alumno a
WHERE  EXISTS (SELECT 1
               FROM   falta_asistencia f
                      JOIN matricula m ON m.id_matricula = f.id_matricula
               WHERE  m.id_alumno    = a.id_alumno
               AND    f.justificada  = 'N')
ORDER  BY a.cod_grupo, a.apellidos
FETCH FIRST 6 ROWS ONLY;
```

| ID_ALUMNO | ALUMNO | COD_GRUPO |
|---|---|---|
| 25 | Iborra Torregrosa, Diego | 1ASIR |
| 27 | Tomás Vidal, Álex | 1ASIR |
| 6 | Cerdá Pérez, Tomás | 1DAM |
| 1 | Ferri Baeza, Adrián | 1DAM |
| 7 | Quiles Marco, Valeria | 1DAM |
| 3 | Verdú Espí, Noelia | 1DAM |

*6 files*

| Tècnica | Quan preferir-la |
|---|---|
| `JOIN` | Necessites **mostrar** columnes de l'altra taula |
| `IN (subconsulta)` | Només filtres, la subconsulta és xicoteta i no torna nuls |
| `EXISTS` | Només filtres, la subconsulta és gran o correlacionada; o hi ha nuls |
| `NOT EXISTS` | «No n'hi ha cap que…»: sempre preferible a `NOT IN` |
| `LEFT JOIN … IS NULL` | Igual que `NOT EXISTS`; tria la que el teu equip llegisca millor |

> [!NOTE]
> Una composició pot **duplicar** files si l'altra taula té diverses coincidències; `EXISTS` mai ho fa, perquè només pregunta si n'hi ha alguna. Si una consulta amb `JOIN` et torna files repetides i el que volies era només filtrar, canvia-la per `EXISTS` en lloc d'afegir un `DISTINCT`.

{{< sesion n="9" h="1" tipo="t" >}}Optimització de consultes: pla d'execució{{< /sesion >}}

## 7. Optimització de consultes i pla d'execució

### 7.1 Què significa optimitzar

El criteri RA4.g demana aplicar criteris d'optimització. Optimitzar **no** és escriure la consulta més curta: és aconseguir que el SGBD lligc **menys dades** per a respondre la mateixa pregunta, i comprovar-ho amb mesuraments.

A Oracle, qui decidix **com** s'executa una consulta és l'**optimitzador basat en costos** (CBO). Tu escrius *què* vols (SQL és declaratiu) i ell tria el pla: quina taula llegir primer, si usar un índex i quin algorisme de composició aplicar. Les seues decisions es basen en les **estadístiques** de les taules (nombre de files, valors distints, distribució). Si les estadístiques estan obsoletes, el pla pot ser roïssim.

### 7.2 Obtindre el pla d'execució

{{< sgbd "Oracle 26ai" >}}

```sql
-- Opció 1: EXPLAIN PLAN (no executa la consulta, només l'analitza)
EXPLAIN PLAN FOR
SELECT a.cod_grupo, COUNT(*) AS matriculas
FROM   matricula m JOIN alumno a ON a.id_alumno = m.id_alumno
GROUP  BY a.cod_grupo;

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);
```

```sql
-- Opció 2: AUTOTRACE en SQLcl o SQL*Plus (executa i mostra pla + estadístiques reals)
SET AUTOTRACE ON EXPLAIN STATISTICS
SET TIMING ON
SELECT ... ;
SET AUTOTRACE OFF
```

| Eina | Com | Què dona |
|---|---|---|
| **SQL Developer / VS Code** | *Explicar pla* (`F10`) | Pla estimat, en arbre |
| **SQL Developer** | *Autotrace* (`F6`) | Pla **real** més lectures i ordenacions |
| **SQLcl / SQL\*Plus** | `EXPLAIN PLAN` + `DBMS_XPLAN.DISPLAY` | Pla en text, fàcil de guardar com a evidència |
| **Qualsevol** | `DBMS_XPLAN.DISPLAY_CURSOR` | Pla realment usat en l'última execució |

### 7.3 Llegir un pla

Un pla té este aspecte (els valors exactes de `Rows`, `Bytes`, `Cost` i `Time` depenen de les estadístiques, de la versió i de l'equip, per la qual cosa **els teus no seran idèntics**):

```text
-------------------------------------------------------------------------------
| Id | Operation            | Name      | Rows | Bytes | Cost (%CPU)| Time     |
-------------------------------------------------------------------------------
|  0 | SELECT STATEMENT     |           |    5 |    65 |     7  (15)| 00:00:01 |
|  1 |  HASH GROUP BY       |           |    5 |    65 |     7  (15)| 00:00:01 |
|* 2 |   HASH JOIN          |           |  143 |  1859 |     6   (0)| 00:00:01 |
|  3 |    TABLE ACCESS FULL | ALUMNO    |   32 |   288 |     3   (0)| 00:00:01 |
|  4 |    TABLE ACCESS FULL | MATRICULA |  143 |   572 |     3   (0)| 00:00:01 |
-------------------------------------------------------------------------------
```

Com es llig:

- **De dins cap a fora i d'amunt a avall**: primer les operacions més indentades (3 i 4), després la que les usa (2), i així fins a la 0.
- **`Rows`** és la **cardinalitat estimada**: quantes files creu l'optimitzador que tornarà aquest pas. Si l'estimació s'allunya molt de la realitat, les estadístiques són roïns i el pla serà roí.
- **`Cost`** és una estimació **relativa** de l'esforç (lectures de disc i CPU). Servix per a comparar dos plans de la **mateixa** consulta; no és un temps ni es pot comparar entre consultes distintes.

Operacions que has de reconéixer:

| Operació | Què fa | Quan és bon senyal |
|---|---|---|
| `TABLE ACCESS FULL` | Llig **tota** la taula | Taules xicotetes, o quan es necessita gran part de les files |
| `INDEX UNIQUE SCAN` | Localitza **una** fila per un índex únic | Cerca per clau primària: òptim |
| `INDEX RANGE SCAN` | Recorre un tram de l'índex | Filtre selectiu: quasi sempre és el desitjable |
| `TABLE ACCESS BY INDEX ROWID` | Va a la taula a buscar les files que ha assenyalat l'índex | Normal després d'un `RANGE SCAN` |
| `INDEX FAST FULL SCAN` | Llig l'índex sencer en compte de la taula | Quan l'índex ja té totes les columnes demanades |
| `NESTED LOOPS` | Per a cada fila d'A, busca en B (normalment per índex) | A torna poques files i B està indexada |
| `HASH JOIN` | Construïx una taula *hash* amb la taula xicoteta i recorre la gran | Composició de taules grans: el normal i eficient |
| `MERGE JOIN` | Ordena les dos entrades i les recorre en paral·lel | Quan ja venen ordenades |
| `SORT ORDER BY` / `HASH GROUP BY` | Ordena / agrupa | Normal; vigila si gasta molta memòria |

> [!NOTE]
> A EduGest, amb 32 alumnes i 143 matrícules, **el correcte és que aparega `TABLE ACCESS FULL`**. Llegir una taula de 143 files completa costa una sola lectura de blocs; usar un índex costaria més. Que l'optimitzador ignore els teus índexs en taules menudes no és una fallada: és la decisió encertada. Per a veure diferències mesurables fa falta volum, i això és el que construïx la **pràctica 4.11** amb una taula de 500 000 files.

### 7.4 Índexs i composicions

Oracle crea índexs automàticament per a `PRIMARY KEY` i `UNIQUE`, però **no** per a les claus alienes. Com que les claus alienes són justament les columnes per les quals es compon, indexar-les és la primera mesura d'optimització de qualsevol esquema. EduGest ja ho fa en l'script 01:

```sql
CREATE INDEX ix_matricula_modulo ON matricula (id_modulo);
CREATE INDEX ix_alumno_grupo     ON alumno (cod_grupo);
CREATE INDEX ix_imparte_profesor ON imparte (id_profesor);
```

| Convé indexar | No convé indexar |
|---|---|
| Claus alienes usades en composicions | Taules molt xicotetes |
| Columnes molt selectives al `WHERE` | Columnes amb pocs valors distints (`turno`, `justificada`) |
| Columnes d'`ORDER BY` sobre resultats grans | Columnes que s'actualitzen constantment |
| Conjunts de columnes d'una consulta crítica (índex de cobertura) | «Per si de cas»: cada índex alenteix els `INSERT` |

### 7.5 Com espatllar un índex sense adonar-se'n

Un índex sobre `columna` només es pot usar si el `WHERE` compara **la columna tal qual**. Si li apliques una funció o una operació, l'índex queda inservible perquè Oracle hauria d'avaluar la funció en totes les files per a saber quines complixen:

```sql
-- (a) NO pot usar un índex sobre fecha_matricula: hi ha una funció damunt
SELECT * FROM matricula WHERE TRUNC(fecha_matricula) = DATE '2025-09-15';

-- (b) SÍ que pot: la columna apareix sense modificar, el rang és equivalent
SELECT * FROM matricula
WHERE  fecha_matricula >= DATE '2025-09-15'
AND    fecha_matricula <  DATE '2025-09-16';
```

```sql
-- (c) Conversió implícita: nia és CHAR(8) i es compara amb un número
SELECT * FROM alumno WHERE nia = 10450037;    -- no usa l'índex
SELECT * FROM alumno WHERE nia = '10450037';  -- sí que el usa
```

Altres destructors d'índexs habituals:

| Patró | Per què no usa l'índex | Alternativa |
|---|---|---|
| `UPPER(email) = 'A@B.ES'` | Funció sobre la columna | Índex basat en funció: `CREATE INDEX … ON alumno (UPPER(email))` |
| `LIKE '%web%'` | El comodí inicial impedix recórrer l'arbre | Cerca de text (`Oracle Text`) o replantejar la dada |
| `nota_final + 1 > 6` | Operació sobre la columna | `nota_final > 5` |
| `cod_grupo <> '1DAM'` | Poc selectiu: torna quasi tot | Sol ser correcte l'accés complet |
| `WHERE col IS NULL` | Els índexs B\*Tree no indexen files amb totes les columnes nul·les | Índex compost o basat en funció |

> [!IMPORTANT]
> Que una condició puga usar un índex es diu que siga **«sargable»**. La regla pràctica és: **deixa la columna sola a un costat de l'operador** i mou tots els càlculs a l'altre costat.

### 7.6 Estadístiques

```sql
-- Recalcular les estadístiques d'una taula (necessari després d'una càrrega massiva)
EXEC DBMS_STATS.GATHER_TABLE_STATS(USER, 'MATRICULA');

-- Tot l'esquema
EXEC DBMS_STATS.GATHER_SCHEMA_STATS(USER);

-- Comprovar quan es van arreplegar i què creu Oracle que hi ha en la taula
SELECT table_name, num_rows, blocks, last_analyzed
FROM   user_tables
ORDER  BY table_name;
```

Oracle arreplega estadístiques automàticament en una finestra de manteniment nocturna, però **després de carregar o esborrar moltes files cal arreplegar-les a mà**: si l'optimitzador creu que la taula té 0 files i en realitat en té mig milió, triarà un `NESTED LOOPS` catastròfic.

### 7.7 Abans i després: un exemple mesurable

Este és l'experiment de la pràctica 4.11, resumit. Sobre una taula `ACCESO_PORTAL` amb **500 000 files** generades, la consulta `SELECT COUNT(*) FROM acceso_portal WHERE id_alumno = 1234` torna **100 files**, és a dir, el 0,02 % de la taula: un filtre molt selectiu.

| Situació | Operació del pla | Blocs llegits | Interpretació |
|---|---|---|---|
| **Sense índex** | `TABLE ACCESS FULL ACCESO_PORTAL` | Tota la taula | Llig 500 000 files per a quedar-se amb 100 |
| **Amb índex** `ix_acceso_alumno (id_alumno)` | `INDEX RANGE SCAN ix_acceso_alumno` | Uns pocs blocs de l'índex | Només recorre el tram de l'índex; com es demana `COUNT(*)`, ni visita la taula |

El cost estimat baixa en dues ordres de magnitud, i el temps també. Però el mateix índex **no** ajuda en `WHERE seccion = 'NOTAS'`, que torna el 20 % de les files: ací l'optimitzador prefereix l'accés complet, i fa bé, perquè anar i tornar a l'índex 100 000 voltes és més car que llegir la taula d'una passada.

> [!WARNING]
> Mesura sempre **dos o tres voltes** cada consulta i queda't amb les últimes: la primera execució carrega els blocs a la memòria cau d'Oracle i és artificialment lenta. I recorda que `Cost` és una **estimació**, no un temps: la prova definitiva és el temps de resposta i el nombre de blocs llegits (`SET AUTOTRACE ON STATISTICS`).

### Gràfic: lectures de bloc amb i sense índex

{{< grafico tipo="barras" titulo="Blocs llegits per a localitzar una fila (model simplificat)" datos="Sense índex · 1 milió de files=10000;Amb índex · 1 milió=4;Sense índex · 100 milions=1000000;Amb índex · 100 milions=5" unidad="blocs" log="true" nota="Model: 100 files per bloc i un B-tree amb unes 200 claus per node. Pulsa el botó per a canviar a escala logarítmica." >}}

Provar el model amb altres grandàries:

{{< coste-busqueda >}}

### 7.8 Llista de comprovació abans de donar per bona una consulta

- [ ] Torna el nombre de files que havia predit.
- [ ] Totes les taules del `FROM` tenen la seua condició d'emparellament: cap producte cartesià involuntari.
- [ ] Les composicions externes no estan anul·lades per un filtre al `WHERE`.
- [ ] Els `COUNT` i `SUM` sobre taules opcionals usen una columna d'eixa taula i estan protegits amb `NVL` si cal.
- [ ] Només es demanen les columnes necessàries; res de `SELECT *` en un informe.
- [ ] Els filtres s'apliquen com més prompte millor (al `WHERE`, no al `HAVING`).
- [ ] Les condicions del `WHERE` deixen la columna sola: no hi ha funcions ni conversions implícites sobre columnes indexades.
- [ ] Hi ha índexs sobre les claus alienes que participen en les composicions.
- [ ] S'ha mirat el pla d'execució i s'entén cada operació.
- [ ] La consulta porta un comentari amb la pregunta que respon i el nombre de files esperat.

---

## 8. Errors freqüents

| Símptoma | Causa | Solució |
|---|---|---|
| `ORA-00979: not a GROUP BY expression` | Una columna del `SELECT` no està al `GROUP BY` ni és un agregat | Afig-la al `GROUP BY`, lleva-la del `SELECT` o resumix-la amb `MIN`, `MAX` o `LISTAGG` |
| `ORA-00937: not a single-group group function` | Es barreja una columna normal amb un agregat **sense** `GROUP BY` | Afig el `GROUP BY` o elimina la columna |
| `ORA-00934: group function is not allowed here` | Un agregat al `WHERE`, al `GROUP BY` o en una restricció | Les condicions sobre agregats van al `HAVING` |
| `ORA-00918: column ambiguously defined` | Una columna amb el mateix nom en dues taules compostes, sense qualificar | Usa àlies de taula i qualifica **totes** les columnes |
| `ORA-00904: invalid identifier` | Àlies del `SELECT` usat al `WHERE` o al `HAVING`, o columna mal escrita | Repetix l'expressió, o posa-li nom amb una subconsulta al `FROM` |
| `ORA-01427: single-row subquery returns more than one row` | Subconsulta comparada amb `=`, `>`… que torna diverses files | Resumix amb `AVG`/`MAX`, o usa `IN`, `ANY` o `ALL` |
| `ORA-25154: column part of USING clause cannot have qualifier` | S'ha qualificat la columna comuna d'un `USING` | Escriu-la sense àlies, o canvia a `JOIN … ON` |
| La consulta torna **moltíssimes més** files de les esperades | Falta una condició de composició (producte cartesià) | Comprova que hi ha N−1 condicions `ON` per a N taules |
| Una composició externa «no funciona» | Un filtre al `WHERE` sobre la taula opcional l'ha convertida en interna | Mou la condició a l'`ON` |
| Un `COUNT` val 1 on hauria de valer 0 | `COUNT(*)` en un `LEFT JOIN` compta la fila sense parella | Compta una columna de la taula opcional |
| `NOT IN` no torna res i no dona error | La subconsulta conté un `NULL` | Usa `NOT EXISTS` o afig `IS NOT NULL` a la subconsulta |

---

## 9. Bones pràctiques

- **Escriu la pregunta abans que l'SQL.** Una consulta sense una pregunta clara darrere no es pot comprovar ni revisar.
- **Prediu el nombre de files** abans d'executar i compara'l després. És la comprovació més rendible que existix.
- **Construïx les composicions d'una en una**, verificant el recompte en cada pas.
- **Usa sempre `JOIN … ON`**, mai la sintaxi amb comes ni `(+)`, i mai `NATURAL JOIN`.
- **Àlies de taula curts i significatius**, i totes les columnes qualificades.
- **A l'`ON`, el que empareja; al `WHERE`, el que filtra.** En composicions externes esta separació no és estil: canvia el resultat.
- **Filtra com més prompte millor:** al `WHERE`, no al `HAVING`; i no filtres en l'aplicació el que pot filtrar el SGBD.
- **Compte amb els nuls en els agregats.** Decidix i documenta si un no presentat compta com a zero o no compta.
- **Prefereix `NOT EXISTS` a `NOT IN`** quan la subconsulta puga tornar nuls.
- **Nomena les columnes calculades** amb àlies comprensibles: és el que veurà qui lligca l'informe.
- **Mira el pla d'execució** de qualsevol consulta que vaja a executar-se de forma habitual, i guarda'l com a evidència quan optimitzes.
- **Comenta les consultes que lliures**: què responen, quines decisions has pres i quantes files tornen.

---

{{< tarjetas titulo="Repassa els termes del tema 4" >}}
- t: "INNER JOIN"
  d: "Torna només les files que tenen parella en ambdues taules."
- t: "LEFT JOIN"
  d: "Conserva totes les files de la taula esquerra, amb NULL si no hi ha parella."
- t: "HAVING"
  d: "Filtre que s'aplica als grups, després de GROUP BY."
- t: "Subconsulta correlacionada"
  d: "Subconsulta que usa columnes de la consulta externa i s'avalua fila a fila."
{{< /tarjetas >}}

## 10. Resum

| Concepte | Idea clau | Sintaxi essencial |
|---|---|---|
| Funcions d'agregat | Convertixen moltes files en un valor; **ignoren els nuls** excepte `COUNT(*)` | `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` |
| `GROUP BY` | Una fila per grup; al `SELECT`, només el que està agrupat o agregat | `GROUP BY col1, col2` |
| `HAVING` | Filtra **grups**; `WHERE` filtra **files** | `HAVING COUNT(*) >= 3` |
| Ordre lògic | `FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY` | — |
| Producte cartesià | Totes les combinacions; involuntari = error, deliberat = graella | `CROSS JOIN` |
| Composició interna | Només les files que emparellen | `JOIN t ON cond` |
| Composició externa | Conserva les files sense parella, amb `NULL` | `LEFT` / `RIGHT` / `FULL OUTER JOIN` |
| Anticomposició | Buscar el que no existix | `LEFT JOIN … WHERE t.pk IS NULL` |
| Autocomposició | Una taula amb si mateixa, amb **dos àlies** | `FROM profesor p JOIN profesor j ON …` |
| Subconsulta | Un `SELECT` dins d'un altre; d'una fila, de diverses o correlacionada | `IN`, `ANY`, `ALL`, `EXISTS` |
| Optimització | Llegir menys dades; mesurar-ho amb el pla | `EXPLAIN PLAN FOR` + `DBMS_XPLAN.DISPLAY` |

Idees que convé endur-se ben gravades:

1. Si una consulta torna més files de les esperades, **falta una condició de composició**.
2. Si en torna menys, **sobra un filtre** o **falta una composició externa**.
3. `COUNT(*)` i `COUNT(columna)` no són el mateix, i en un `LEFT JOIN` la diferència és just el que vols.
4. `NULL` continua sent la causa de la meitat de les sorpreses: en `AVG`, en `NOT IN` i en les composicions externes.

---

## 11. Autoavaluació

{{< quiz >}}
- q: "`MATRICULA` té 143 files, 6 amb `nota_final` nul·la. Quina parella de valors torna `SELECT AVG(nota_final), SUM(nota_final)/COUNT(*) FROM matricula`?"
  options: ["Els dos el mateix valor", "6,36 i 6,09: `AVG` dividix entre 137 i l'expressió entre 143", "6,09 i 6,36", "`AVG` dona error perquè hi ha nuls"]
  answer: 1
  explain: "`AVG` ignora els nuls i dividix entre les 137 matrícules qualificades; `COUNT(*)` compta les 143 files, així que la segona expressió tracta els no presentats com a zeros. Són respostes a preguntes distintes."
- q: "Quina d'estes consultes és correcta en Oracle?"
  options: ["`SELECT cod_grupo, nombre, COUNT(*) FROM alumno GROUP BY cod_grupo`", "`SELECT cod_grupo, COUNT(*) FROM alumno WHERE COUNT(*) > 3 GROUP BY cod_grupo`", "`SELECT cod_grupo, COUNT(*) AS n FROM alumno GROUP BY cod_grupo HAVING COUNT(*) > 3 ORDER BY n`", "`SELECT cod_grupo, COUNT(*) AS n FROM alumno GROUP BY cod_grupo HAVING n > 3`"]
  answer: 2
  explain: "La primera dona ORA-00979 (`nombre` no està agrupat); la segona, ORA-00934 (agregat al `WHERE`); la quarta falla perquè l'àlies `n` encara no existix quan s'avalua el `HAVING`. A l'`ORDER BY`, que és l'últim, sí que es pot usar."
- q: "Per què `SELECT g.cod_grupo, p.apellidos FROM grupo g LEFT JOIN profesor p ON p.id_profesor = g.id_tutor WHERE p.id_departamento = 1` perd el grup sense tutor?"
  options: ["Perquè `LEFT JOIN` no conserva les files sense parella", "Perquè la condició del `WHERE` s'avalua després de la composició i `NULL = 1` és `UNKNOWN`", "Perquè falta `OUTER`", "Perquè `id_departamento` és clau aliena"]
  answer: 1
  explain: "El `LEFT JOIN` crea la fila amb les columnes de `PROFESOR` a `NULL`, i el `WHERE` la descarta perquè la condició no és `TRUE`. Per a conservar-la, la condició sobre la taula opcional ha d'anar a l'`ON`."
- q: "En `GROUP BY g.cod_grupo` sobre un `GRUPO LEFT JOIN ALUMNO`, què torna `COUNT(*)` per a un grup sense alumnes?"
  options: ["0", "1, perquè la fila existix encara que no tinga dades d'ALUMNO", "NULL", "Depén de la versió d'Oracle"]
  answer: 1
  explain: "La composició externa genera una fila per a eixe grup, així que `COUNT(*)` val 1. Per a obtindre 0 cal comptar una columna de la taula opcional: `COUNT(a.id_alumno)`."
- q: "Quan és preferible `EXISTS` a un `JOIN`?"
  options: ["Sempre: `EXISTS` és més ràpid", "Quan només es vol filtrar i no mostrar columnes de l'altra taula, sobretot si podria duplicar files", "Quan l'altra taula té clau primària composta", "Mai: `EXISTS` és sintaxi antiga"]
  answer: 1
  explain: "`EXISTS` només comprova si hi ha alguna fila coincident, així que no duplica files ni obliga a afegir `DISTINCT`. Si necessites **mostrar** dades de l'altra taula, cal un `JOIN`."
- q: "Una consulta sobre una taula de 500 000 files usa `WHERE TRUNC(fecha_hora) = DATE '2024-03-15'` i el pla mostra `TABLE ACCESS FULL` malgrat existir un índex sobre `fecha_hora`. Per què?"
  options: ["Perquè l'índex està danyat", "Perquè la funció `TRUNC` s'aplica sobre la columna i l'índex indexa la columna sense modificar", "Perquè falten estadístiques", "Perquè `DATE` no es pot indexar"]
  answer: 1
  explain: "Una funció sobre la columna impedix usar l'índex: caldria avaluar-la en totes les files. Es corregix amb un rang de dates (`>= … AND < …`) o creant un índex basat en la funció `TRUNC(fecha_hora)`."
{{< /quiz >}}

## Referències

- [Oracle AI Database 26ai: SQL Language Reference, *SELECT*](https://docs.oracle.com/en/database/oracle/oracle-database/26/sqlrf/SELECT.html) — sintaxi completa de `JOIN`, `GROUP BY`, `HAVING`, subconsultes i operadors de conjunts.
- [Oracle AI Database 26ai: SQL Language Reference, *Aggregate Functions*](https://docs.oracle.com/en/database/oracle/oracle-database/26/sqlrf/Aggregate-Functions.html).
- [Oracle AI Database 26ai: SQL Language Reference, *Analytic Functions*](https://docs.oracle.com/en/database/oracle/oracle-database/26/sqlrf/Analytic-Functions.html).
- [Oracle AI Database 26ai: SQL Language Reference, *CREATE VIEW*](https://docs.oracle.com/en/database/oracle/oracle-database/26/sqlrf/CREATE-VIEW.html).
- [Oracle AI Database 26ai: SQL Tuning Guide](https://docs.oracle.com/en/database/oracle/oracle-database/26/tgsql/) — optimitzador, plans d'execució, índexs i estadístiques.
- [Oracle AI Database 26ai: Database PL/SQL Packages and Types Reference, *DBMS_XPLAN*](https://docs.oracle.com/en/database/oracle/oracle-database/26/arpls/DBMS_XPLAN.html).
- [Reial decret 1629/2009, de 30 d'octubre](https://www.boe.es/eli/es/rd/2009/10/30/1629) — ensenyaments mínims del mòdul 0372 Gestió de bases de dades (RA4 i RA3).
