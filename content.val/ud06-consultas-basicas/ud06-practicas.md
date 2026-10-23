---
title: "Consultes sobre una taula - Pràctiques"
weight: 2
bookToc: true
---

# UD06 · Pràctiques

{{< ra "RA3:a,b" "RA5:e" >}}

| Pràctica | Tipus | Nivell | CE principals |
|---|---|---|---|
| [6.1 Primeres consultes i eines](#pràctica-61--primeres-consultes-i-eines) | Guiada | ●○○ | RA3.a, RA3.b |
| [6.2 Consultes per a secretaria](#pràctica-62--consultes-per-a-secretaria) | Autònoma | ●●○ | RA3.b |
| [6.3 Laboratori de valors nuls](#pràctica-63--laboratori-de-valors-nuls) | Guiada | ●●○ | RA3.b |
| [6.4 Funcions per a informes](#pràctica-64--funcions-per-a-informes) | Autònoma | ●●○ | RA3.b, RA5.e |
| [6.5 Validar dades amb SQL](#pràctica-65--validar-dades-amb-sql) | Repte | ●●● | RA3.b, RA5.e |
| [Projecte EduGest · UD06](#projecte-edugest--ud06-consultes-del-dia-a-dia) | Projecte | ●●○ | RA3.a, RA3.b |

> [!IMPORTANT]
> Totes les pràctiques usen l'esquema de referència **EDUGEST** amb les dades de l'[script 02](/guia/proyecto-edugest#4-scripts-descarregables). Abans de començar, executa en la teua sessió:
>
> ```sql
> ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY';
> ```
>
> Si has modificat les dades en altres pràctiques, torna a executar els scripts 01 i 02 perquè els teus resultats coincidisquen amb les solucions.

---

## Pràctica 6.1 · Primeres consultes i eines

{{< practica num="6.1" tipo="Guiada" duracion="1 sessió" nivel="1" ra="RA3: a, b" sgbd="Oracle 26ai · SQL Developer (o extensió de VS Code)" entrega="p6_1.sql + captura del generador de consultes" >}}

#### Objectiu

Conéixer les eines de consulta (full de treball, generador de consultes, pestanya de dades) i escriure les primeres consultes sobre una taula.

#### Desenvolupament

{{% steps %}}

1. **Explora sense SQL.** En el navegador de connexions, desplega *Taules* → `MODULO` → pestanya *Dades*. Usa el filtre de la part superior (escriu `cod_ciclo = 'DAW'`). Observa que l'eina **genera** una condició SQL.

2. **Usa el generador de consultes.** Obri un full de treball, clic dret → *Generador de consultes*. Arrossega la taula `PROFESOR`, marca `NOMBRE`, `APELLIDOS` i `ESPECIALIDAD`, i afig el criteri `ID_DEPARTAMENTO = 1`. Passa a la pestanya *SQL* i copia la consulta generada. Fes una captura.

3. **Escriu i executa** cada consulta amb `Ctrl+Intro`. Comprova que el nombre de files coincidix.

    ```sql
    -- 1. Tots els grups
    SELECT * FROM grupo;                                              -- 6 files

    -- 2. Nom i hores dels mòduls de 2n de DAM
    SELECT nombre, horas FROM modulo WHERE cod_ciclo = 'DAM' AND curso = 2;   -- 5 files

    -- 3. Grups de vesprada
    SELECT cod_grupo, cod_ciclo FROM grupo WHERE turno = 'T';         -- 2 files

    -- 4. Professorat ordenat per data d'alta, del més antic al més recent
    SELECT nombre, apellidos, fecha_alta FROM profesor ORDER BY fecha_alta;   -- 12 files
    ```

4. **Executa l'script complet** amb `F5` i compara: el resultat apareix com a text en la *Eixida de script*, com en SQLcl.

5. **Exporta un resultat.** Clic dret sobre la graella del resultat 4 → *Exportar* → format CSV.

{{% /steps %}}

#### Comprovació

{{% comprobacion %}}
- [ ] Les quatre consultes tornen 6, 5, 2 i 12 files.
- [ ] La consulta del generador és equivalent a `SELECT nombre, apellidos, especialidad FROM profesor WHERE id_departamento = 1;` i torna 8 files.
- [ ] Saps explicar la diferència entre executar amb `Ctrl+Intro` i amb `F5`.
{{% /comprobacion %}}

---

## Pràctica 6.2 · Consultes per a secretaria

{{< practica num="6.2" tipo="Autónoma" duracion="3 sessions" nivel="2" ra="RA3: b" sgbd="Oracle 26ai · esquema EDUGEST" entrega="p6_2.sql comentat" >}}

#### Objectiu

Resoldre de manera autònoma consultes reals sobre una taula combinant projecció, selecció, ordenació, operadors i eliminació de duplicats.

#### Context

Secretaria necessita respostes ràpides a preguntes del dia a dia. Escriu una consulta per a cadascuna. Abans de mirar la solució, comprova que obtens **el mateix nombre de files**.

#### Enunciat

**Bloc A · Projecció i ordenació**

**A1.** Codi, nom i hores de tots els mòduls d'ASIR, de més a menys hores.

{{< solucion id="ud06-001" title="Solució A1" />}}

**A2.** Nom complet del professorat en el format «Cognoms, Nom», ordenat alfabèticament, amb una columna anomenada `profesor`.

{{< solucion id="ud06-002" title="Solució A2" />}}

**A3.** Les distintes especialitats del professorat, sense repetir.

{{< solucion id="ud06-003" title="Solució A3" />}}

**A4.** Els distints parells (cicle, curs) que existixen en la taula de mòduls.

{{< solucion id="ud06-004" title="Solució A4" />}}

**Bloc B · Selecció**

**B1.** Alumnat que viu a Elx o a El Campello (nom, cognoms i localitat).

{{< solucion id="ud06-005" title="Solució B1" />}}

**B2.** Mòduls que tenen entre 96 i 128 hores, ambdues incloses.

{{< solucion id="ud06-006" title="Solució B2" />}}

**B3.** Alumnat nascut abans de 2005, del major al menor.

{{< solucion id="ud06-007" title="Solució B3" />}}

**B4.** Professorat del departament 1 que **no** té l'especialitat «Informática».

{{< solucion id="ud06-008" title="Solució B4" />}}

**B5.** Mòduls el nom dels quals conté la paraula «web» (en qualsevol combinació de majúscules).

{{< solucion id="ud06-009" title="Solució B5" />}}

**B6.** Matrícules en segona convocatòria o posterior (id de matrícula, alumne, mòdul, convocatòria i nota).

{{< solucion id="ud06-010" title="Solució B6" />}}

**B7.** Faltes **justificades** de 3 hores.

{{< solucion id="ud06-011" title="Solució B7" />}}

**B8.** Faltes registrades al desembre de 2025.

{{< solucion id="ud06-012" title="Solució B8" />}}

**Bloc C · Valors nuls i límits**

**C1.** Matrícules **sense qualificar**.

{{< solucion id="ud06-013" title="Solució C1" />}}

**C2.** Grups sense tutor assignat.

{{< solucion id="ud06-014" title="Solució C2" />}}

**C3.** Les tres matrícules amb pitjor nota (entre les qualificades), amb desempat per `id_matricula`.

{{< solucion id="ud06-015" title="Solució C3" />}}

**C4.** Els dos professors amb més antiguitat al centre.

{{< solucion id="ud06-016" title="Solució C4" />}}

#### Comprovació

{{% comprobacion %}}
- [ ] Cada consulta comença amb un comentari que repetix la pregunta.
- [ ] Cap consulta compara amb `= NULL` ni usa dates com a text.
- [ ] Totes les consultes que tornen llistats tenen `ORDER BY`.
- [ ] El nombre de files de cada consulta coincidix amb la solució.
{{% /comprobacion %}}

#### Errors habituals

> [!WARNING]
> - En B4, la condició `especialidad <> 'Informática'` exclou també qui tinga l'especialitat a `NULL`. En estes dades no n'hi ha cap, però en una consulta real hauries de decidir si incloure'ls amb `OR especialidad IS NULL`.
> - En B8, `fecha BETWEEN DATE '2025-12-01' AND DATE '2025-12-31'` no inclouria una falta del 31 a les 10:00. En estes dades totes les dates són a les 00:00, però acostuma't a l'interval semiobert.

#### Ampliació

Escriu B5 de tres formes distintes (amb `UPPER`, amb `LOWER` i amb `REGEXP_LIKE(nombre, 'web', 'i')`) i comprova que donen el mateix resultat.

---

## Pràctica 6.3 · Laboratori de valors nuls

{{< practica num="6.3" tipo="Guiada" duracion="1 sessió" nivel="2" ra="RA3: b" sgbd="Oracle 26ai · esquema EDUGEST" entrega="Taula de prediccions + resultats reals" >}}

#### Objectiu

Comprendre la lògica de tres valors **predient** el resultat de consultes amb `NULL` abans d'executar-les.

#### Desenvolupament

Per a cada consulta, **escriu primer la teua predicció** del nombre de files. Després executa-la i anota el resultat real. Si no coincidixen, explica per què.

Dades de partida: `ALUMNO` té 32 files; 3 sense grup, 4 sense DNI, 3 sense email i 5 sense telèfon. `MATRICULA` té 143 files, de les quals 6 estan sense qualificar.

| # | Consulta | La teua predicció | Real |
|---|---|---|---|
| 1 | `SELECT COUNT(*) FROM alumno WHERE dni = NULL;` | | |
| 2 | `SELECT COUNT(*) FROM alumno WHERE dni IS NULL;` | | |
| 3 | `SELECT COUNT(*) FROM alumno WHERE cod_grupo <> '1DAM';` | | |
| 4 | `SELECT COUNT(*) FROM alumno WHERE cod_grupo <> '1DAM' OR cod_grupo IS NULL;` | | |
| 5 | `SELECT COUNT(*) FROM alumno WHERE email IS NULL OR telefono IS NULL;` | | |
| 6 | `SELECT COUNT(*) FROM matricula WHERE nota_final >= 5;` | | |
| 7 | `SELECT COUNT(*) FROM matricula WHERE NOT (nota_final >= 5);` | | |
| 8 | `SELECT COUNT(*) FROM matricula WHERE NVL(nota_final, 0) < 5;` | | |
| 9 | `SELECT COUNT(*) FROM alumno WHERE cod_grupo NOT IN ('1DAM', '2DAM');` | | |
| 10 | `SELECT COUNT(*) FROM alumno WHERE cod_grupo NOT IN ('1DAM', NULL);` | | |

{{< solucion id="ud06-017" title="Resultats reals i explicació" />}}

> [!CAUTION]
> El cas 10 és una trampa clàssica que apareixerà de nou a la UD07 amb les subconsultes: `WHERE id NOT IN (SELECT ...)` no torna res si la subconsulta torna algun `NULL`.

---

## Pràctica 6.4 · Funcions per a informes

{{< practica num="6.4" tipo="Autónoma" duracion="2 sessions" nivel="2" ra="RA3: b · RA5: e" sgbd="Oracle 26ai · esquema EDUGEST" entrega="p6_4.sql comentat" >}}

#### Objectiu

Usar les funcions de fila d'Oracle per a transformar i presentar les dades.

#### Enunciat

**F1.** Genera l'**etiqueta del caseller** de cada alumne d'1DAM: inicial del nom, punt, primer cognom en majúscules i el NIA entre claudàtors. Exemple: `A. FERRI [10450037]`.

{{< solucion id="ud06-018" title="Solució F1" />}}

**F2.** Per a cada mòdul de DAW, mostra el codi, el nom i una columna `duracion` amb el text «Corto» (menys de 100 hores), «Medio» (de 100 a 159) o «Largo» (160 o més).

{{< solucion id="ud06-019" title="Solució F2" />}}

**F3.** Per al professorat, mostra el nom, la data d'alta amb el format «01/09/2009» i el nombre d'**anys complets** d'antiguitat a data 1 de setembre de 2026.

{{< solucion id="ud06-020" title="Solució F3" />}}

**F4.** Mostra el telèfon de l'alumnat de 2DAM de manera que, si no en té, aparega «Sin teléfono», i una columna `contacto` que mostre l'email si existix i, si no, el telèfon.

{{< solucion id="ud06-021" title="Solució F4" />}}

**F5.** Nom del dia de la setmana (en castellà) de cada falta d'assistència de la matrícula 10044.

{{< solucion id="ud06-022" title="Solució F5" />}}

**F6.** Per a les matrícules de l'alumne 9, mostra la nota amb **dos decimals** com a text (`TO_CHAR`), la nota arredonida i una columna `estado` amb «Aprobado», «Suspenso» o «Pendiente».

{{< solucion id="ud06-023" title="Solució F6" />}}

#### Comprovació

{{% comprobacion %}}
- [ ] F1 funciona encara que un cognom tinga accents.
- [ ] F3 calcula anys **complets**, no la diferència d'anys del calendari.
- [ ] F5 mostra els dies en castellà encara que la teua sessió estiga en anglés.
{{% /comprobacion %}}

---

## Pràctica 6.5 · Validar dades amb SQL

{{< practica num="6.5" tipo="Reto" duracion="1 sessió" nivel="3" ra="RA3: b · RA5: e" sgbd="Oracle 26ai · esquema EDUGEST" entrega="p6_5.sql + informe de qualitat de dades" >}}

#### Objectiu

Usar consultes i funcions del SGBD per a auditar la **qualitat de les dades**, una tasca professional habitual abans de migrar o explotar una base de dades.

#### Context

Direcció d'estudis sospita que hi ha dades mal introduïdes. Et demana un informe de qualitat.

#### Enunciat

1. **Lletra del DNI.** La lletra d'un DNI és el caràcter que ocupa la posició `MOD(número, 23) + 1` en la cadena `'TRWAGMYFPDXBNJZSQVHLCKE'`. Escriu una consulta que mostre el professorat el DNI del qual té la lletra **incorrecta**.
2. **Format del correu.** Llista l'alumnat l'email del qual no complix el patró `texto@alu.edugest.es`.
3. **NIA.** Comprova que tots els NIA tenen exactament 8 dígits numèrics.
4. **Coherència d'edats.** Hi ha alumnat menor de 16 anys a data 15/09/2025? I major de 30?
5. **Dates de faltes.** Hi ha faltes registrades en dissabte o diumenge?
6. Redacta un **informe** amb els problemes trobats i proposa, per a cadascun, una restricció (UD05) o un trigger (UD09) que l'hauria evitat.

{{% details title="Pista per a l'apartat 1" %}}
```sql
SELECT nombre, apellidos, dni,
       SUBSTR('TRWAGMYFPDXBNJZSQVHLCKE', MOD(TO_NUMBER(SUBSTR(dni, 1, 8)), 23) + 1, 1) AS letra_correcta
FROM   profesor
WHERE  SUBSTR(dni, 9, 1) <> SUBSTR('TRWAGMYFPDXBNJZSQVHLCKE', MOD(TO_NUMBER(SUBSTR(dni, 1, 8)), 23) + 1, 1);
```
Has de trobar **2** professors amb la lletra incorrecta. Valdria esta consulta per a un NIE (que comença per X, Y o Z)?
{{% /details %}}

{{% details title="Pista per a l'apartat 5" %}}
`TO_CHAR(fecha, 'D')` depén del territori de la sessió (en uns països la setmana comença en diumenge i en altres en dilluns). És més fiable `TO_CHAR(fecha, 'DY', 'NLS_DATE_LANGUAGE=ENGLISH') IN ('SAT', 'SUN')`.
{{% /details %}}

---

## Projecte EduGest · UD06: consultes del dia a dia

{{< practica num="EduGest-6" tipo="Proyecto" duracion="Treball transversal (1 setmana)" nivel="2" ra="RA3: a, b" sgbd="Oracle 26ai · esquema EDUGEST" entrega="edugest/05_consultas_basicas.sql" >}}

#### Enunciat

Entrevista (o imagina) tres perfils d'EduGest: secretaria, tutoria i direcció d'estudis. Per a cadascun, escriu **cinc preguntes** que es responguen amb una consulta sobre **una sola taula** i resol-les. Cada consulta ha de:

1. Anar precedida d'un comentari amb el perfil, la pregunta i el nombre de files que torna.
2. Usar almenys una d'estes tècniques: `CASE`, una funció de data, una funció de text, `NVL`/`COALESCE`, `FETCH FIRST`, `LIKE`, `IN` o `BETWEEN`.
3. Estar ordenada quan torne un llistat.

Inclou també una consulta creada amb el **generador de consultes** de SQL Developer i explica què ha generat.

#### Comprovació

{{% comprobacion %}}
- [ ] 15 consultes, totes executables sense errors.
- [ ] Les tècniques indicades apareixen almenys una vegada cadascuna.
- [ ] Les preguntes són realistes i distintes a les de la pràctica 6.2.
{{% /comprobacion %}}
