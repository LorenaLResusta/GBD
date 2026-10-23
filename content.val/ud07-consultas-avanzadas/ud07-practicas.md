---
title: "Consultes avançades - Pràctiques"
weight: 2
bookToc: true
---

# UD07 · Pràctiques

{{< ra "RA3:a,c,d,e,f,g,h" "RA2:f" >}}

| Pràctica | Tipus | Nivell | CE principals |
|---|---|---|---|
| [7.1 Consultes resum](#pràctica-71--consultes-resum) | Guiada | ●○○ | RA3.e |
| [7.2 Composicions pas a pas](#pràctica-72--composicions-pas-a-pas) | Guiada | ●●○ | RA3.c, RA3.d |
| [7.3 Informes per a cap d'estudis](#pràctica-73--informes-per-a-cap-destudis) | Autònoma | ●●○ | RA3.c, RA3.d, RA3.e |
| [7.4 Subconsultes](#pràctica-74--subconsultes) | Autònoma | ●●○ | RA3.f |
| [7.5 Múltiples seleccions i vistes](#pràctica-75--múltiples-seleccions-i-vistes) | Autònoma | ●●○ | RA3.g, RA2.f |
| [7.6 Optimització: mesurar abans i després](#pràctica-76--optimització-mesurar-abans-i-després) | Guiada | ●●● | RA3.h |
| [7.7 Repte: el quadre de comandament](#pràctica-77--repte-el-quadre-de-comandament) | Repte | ●●● | RA3.c-h |
| [Projecte EduGest · UD07](#projecte-edugest--ud07-informes) | Projecte | ●●● | RA3 complet |

> [!IMPORTANT]
> Treballa sobre **EDUGEST amb les dades originals** (scripts 01 i 02) i amb `ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY';`. Intenta cada consulta abans d'obrir la solució; com a mínim, comprova que obtens el **mateix nombre de files**.

---

## Pràctica 7.1 · Consultes resum

{{< practica num="7.1" tipo="Guiada" duracion="2 sessions" nivel="1" ra="RA3: e" sgbd="Oracle 26ai · EDUGEST" entrega="p7_1.sql" >}}

#### Objectiu

Usar funcions d'agregat, `GROUP BY` i `HAVING`, i entendre com influïxen els valors nuls en els resultats.

#### Desenvolupament

{{% steps %}}

1. **Totals generals.** Quants alumnes hi ha, quants tenen grup i en quants grups distints estan?

    ```sql
    SELECT COUNT(*) AS alumnos, COUNT(cod_grupo) AS con_grupo, COUNT(DISTINCT cod_grupo) AS grupos
    FROM   alumno;
    ```

    | ALUMNOS | CON_GRUPO | GRUPOS |
    |---|---|---|
    | 32 | 29 | 5 |

    *1 fila*


2. **Agrupar per una columna.** Nombre d'alumnes per localitat, de més a menys.

    ```sql
    SELECT localidad, COUNT(*) AS alumnos
    FROM   alumno
    GROUP  BY localidad
    ORDER  BY alumnos DESC, localidad;
    ```

    | LOCALIDAD | ALUMNOS |
    |---|---|
    | Alicante | 13 |
    | Mutxamel | 6 |
    | Sant Joan d'Alacant | 4 |
    | El Campello | 3 |
    | Elche | 3 |
    | San Vicente del Raspeig | 3 |

    *6 files*


3. **Agrupar per diverses columnes.** Faltes i hores de falta per mes i per tipus (justificada o no).

    ```sql
    SELECT TO_CHAR(fecha, 'YYYY-MM') AS mes, justificada,
           COUNT(*) AS faltas, SUM(horas) AS horas
    FROM   falta_asistencia
    GROUP  BY TO_CHAR(fecha, 'YYYY-MM'), justificada
    ORDER  BY mes, justificada;
    ```

    | MES | JUSTIFICADA | FALTAS | HORAS |
    |---|---|---|---|
    | 2025-09 | N | 3 | 5 |
    | 2025-09 | S | 2 | 2 |
    | 2025-10 | N | 4 | 6 |
    | 2025-10 | S | 3 | 4 |
    | 2025-11 | N | 2 | 5 |
    | 2025-11 | S | 2 | 4 |
    | 2025-12 | N | 2 | 2 |
    | 2026-01 | N | 5 | 10 |
    | 2026-02 | N | 3 | 5 |
    | 2026-02 | S | 5 | 11 |
    | 2026-03 | N | 5 | 11 |
    | 2026-03 | S | 4 | 5 |
    | 2026-04 | N | 3 | 6 |
    | 2026-04 | S | 1 | 1 |
    | 2026-05 | S | 2 | 4 |

    *15 files*


4. **Filtrar grups.** Mòduls (per `id_modulo`) amb almenys un suspés i el seu nombre de suspesos, només si n'hi ha **dos o més**.

    ```sql
    SELECT id_modulo, COUNT(*) AS suspensos
    FROM   matricula
    WHERE  nota_final < 5
    GROUP  BY id_modulo
    HAVING COUNT(*) >= 2
    ORDER  BY suspensos DESC, id_modulo;
    ```

    | ID_MODULO | SUSPENSOS |
    |---|---|
    | 3 | 4 |
    | 18 | 3 |
    | 2 | 2 |
    | 6 | 2 |
    | 7 | 2 |
    | 10 | 2 |
    | 11 | 2 |
    | 13 | 2 |

    *8 files*


5. **Comptar condicions.** Per a cada convocatòria: matrícules, aprovades, suspeses i sense qualificar.

    ```sql
    SELECT convocatoria,
           COUNT(*) AS total,
           SUM(CASE WHEN nota_final >= 5 THEN 1 ELSE 0 END) AS aprobadas,
           SUM(CASE WHEN nota_final <  5 THEN 1 ELSE 0 END) AS suspensas,
           COUNT(*) - COUNT(nota_final)                    AS sin_calificar
    FROM   matricula
    GROUP  BY convocatoria
    ORDER  BY convocatoria;
    ```

    | CONVOCATORIA | TOTAL | APROBADAS | SUSPENSAS | SIN_CALIFICAR |
    |---|---|---|---|---|
    | 1 | 140 | 108 | 26 | 6 |
    | 2 | 3 | 2 | 1 | 0 |

    *2 files*


6. **Provoca els errors típics** i anota el missatge:

    ```sql
    SELECT localidad, nombre, COUNT(*) FROM alumno GROUP BY localidad;   -- ORA-00979
    SELECT localidad, COUNT(*) FROM alumno;                              -- ORA-00937
    SELECT localidad FROM alumno WHERE COUNT(*) > 3 GROUP BY localidad;  -- ORA-00934
    ```

{{% /steps %}}

#### Comprovació

{{% comprobacion %}}
- [ ] Al pas 1 entens per què `COUNT(*)` i `COUNT(cod_grupo)` donen resultats distints.
- [ ] Al pas 5, la suma d'aprovades, suspeses i sense qualificar coincidix amb el total de cada convocatòria.
- [ ] Saps corregir cada un dels tres errors del pas 6.
{{% /comprobacion %}}

#### Ampliació

Repeteix el pas 2 afegint `ROLLUP`: `GROUP BY ROLLUP(localidad)`. Quina fila nova apareix? Quin valor té `localidad` en ella?

---

## Pràctica 7.2 · Composicions pas a pas

{{< practica num="7.2" tipo="Guiada" duracion="2 sessions" nivel="2" ra="RA3: c, d" sgbd="Oracle 26ai · EDUGEST" entrega="p7_2.sql + respostes" >}}

#### Objectiu

Construir composicions de diverses taules seguint el camí de claus alienes, i decidir quan fa falta una composició externa.

#### Desenvolupament

{{% steps %}}

1. **Traça el camí.** Volem, per a cada falta d'assistència, el nom de l'alumne, el nom del mòdul i el cicle. Sobre el diagrama relacional d'EduGest, el camí és:

    ```mermaid
    flowchart LR
        F[FALTA_ASISTENCIA] -- id_matricula --> M[MATRICULA]
        M -- id_alumno --> A[ALUMNO]
        M -- id_modulo --> MO[MODULO]
        MO -- cod_ciclo --> C[CICLO]
    ```

2. **Afig les taules una a una** i comprova el nombre de files en cada pas. Si el nombre **augmenta** de forma inesperada, falta una condició o la composició no seguix una clau aliena.

    ```sql
    -- Pas a: només faltes
    SELECT COUNT(*) FROM falta_asistencia f;                                  -- 46
    -- Pas b: + matrícula
    SELECT COUNT(*) FROM falta_asistencia f
           JOIN matricula m ON m.id_matricula = f.id_matricula;              -- 46
    -- Pas c: + alumne i mòdul
    SELECT COUNT(*) FROM falta_asistencia f
           JOIN matricula m ON m.id_matricula = f.id_matricula
           JOIN alumno a    ON a.id_alumno    = m.id_alumno
           JOIN modulo mo   ON mo.id_modulo   = m.id_modulo;                 -- 46
    ```

3. **Escriu la consulta final**, limitada a les faltes no justificades de 3 hores:

    ```sql
    SELECT f.fecha, a.apellidos || ', ' || a.nombre AS alumno,
           mo.nombre AS modulo, c.cod_ciclo, f.horas
    FROM   falta_asistencia f
           JOIN matricula m ON m.id_matricula = f.id_matricula
           JOIN alumno a    ON a.id_alumno    = m.id_alumno
           JOIN modulo mo   ON mo.id_modulo   = m.id_modulo
           JOIN ciclo c     ON c.cod_ciclo    = mo.cod_ciclo
    WHERE  f.justificada = 'N' AND f.horas = 3
    ORDER  BY f.fecha;
    ```

    | FECHA | ALUMNO | MODULO | COD_CICLO | HORAS |
    |---|---|---|---|---|
    | 22/09/2025 | Quiles Marco, Valeria | Entornos de desarrollo | DAM | 3 |
    | 21/10/2025 | Ripoll Agulló, Iván | Sistemas de gestión empresarial | DAM | 3 |
    | 25/11/2025 | Cerdá Tomás, Nerea | Sistemas informáticos | DAM | 3 |
    | 06/01/2026 | Amorós Guillem, Sara | Diseño de interfaces web | DAW | 3 |
    | 21/01/2026 | Tomás Vidal, Álex | Lenguajes de marcas y sistemas de gestión de información | ASIR | 3 |
    | 25/02/2026 | Alemany Vidal, Martina | Sistemas de gestión empresarial | DAM | 3 |
    | 10/03/2026 | Cerdá Pérez, Tomás | Programación | DAM | 3 |
    | 19/03/2026 | Ferri Baeza, Adrián | Programación | DAM | 3 |
    | 25/03/2026 | Alemany Pérez, Daniel | Entornos de desarrollo | DAW | 3 |
    | 29/04/2026 | Alemany Vidal, Martina | Programación de servicios y procesos | DAM | 3 |

    *10 files*


4. **Provoca un producte cartesià** traient la condició `ON` de `MODULO` (en Oracle, substituïx `JOIN modulo mo ON ...` per `CROSS JOIN modulo mo`). Quantes files ixen ara al pas c? Per què?

5. **Interna enfront d'externa.** Executa les dues consultes i explica la diferència:

    ```sql
    -- (a) Interna
    SELECT c.cod_ciclo, COUNT(g.cod_grupo) AS grupos
    FROM   ciclo c JOIN grupo g ON g.cod_ciclo = c.cod_ciclo
    GROUP  BY c.cod_ciclo ORDER BY c.cod_ciclo;

    -- (b) Externa
    SELECT c.cod_ciclo, COUNT(g.cod_grupo) AS grupos
    FROM   ciclo c LEFT JOIN grupo g ON g.cod_ciclo = c.cod_ciclo
    GROUP  BY c.cod_ciclo ORDER BY c.cod_ciclo;
    ```

    | (a) Interna | | (b) Externa | |
    |---|---|---|---|
    | ASIR | 2 | ASIR | 2 |
    | DAM | 2 | DAM | 2 |
    | DAW | 2 | DAW | 2 |
    | | | **SMR** | **0** |

6. **La trampa del WHERE.** Volem tots els professors i les hores que impartixen **a 2DAM** (0 si no hi impartixen). Compara:

    ```sql
    -- (a) Incorrecta: el WHERE elimina qui no impartix a 2DAM
    SELECT p.nombre, NVL(SUM(i.horas_semanales), 0) AS horas_2dam
    FROM   profesor p LEFT JOIN imparte i ON i.id_profesor = p.id_profesor
    WHERE  i.cod_grupo = '2DAM'
    GROUP  BY p.id_profesor, p.nombre ORDER BY p.id_profesor;     -- 4 files

    -- (b) Correcta: la condició sobre la taula opcional va a l'ON
    SELECT p.nombre, NVL(SUM(i.horas_semanales), 0) AS horas_2dam
    FROM   profesor p LEFT JOIN imparte i
           ON i.id_profesor = p.id_profesor AND i.cod_grupo = '2DAM'
    GROUP  BY p.id_profesor, p.nombre ORDER BY p.id_profesor;     -- 12 files
    ```

    | NOMBRE | HORAS_2DAM |
    |---|---|
    | Marta | 0 |
    | Javier | 3 |
    | Lucía | 6 |
    | Andrés | 4 |
    | Elena | 0 |
    | Raúl | 3 |
    | Nuria | 0 |
    | Pablo | 0 |
    | Carmen | 0 |
    | Sergio | 0 |
    | Laura | 0 |
    | David | 0 |

    *12 files*


{{% /steps %}}

#### Comprovació

{{% comprobacion %}}
- [ ] Les tres consultes del pas 2 tornen 46 files.
- [ ] Al pas 4 obtens 46 × 24 = 1104 files i saps explicar-ho.
- [ ] Saps explicar per què SMR només apareix amb `LEFT JOIN` i per què el `COUNT` dona 0 i no 1.
- [ ] Al pas 6, la versió (b) torna els 12 professors.
{{% /comprobacion %}}

---

## Pràctica 7.3 · Informes per a cap d'estudis

{{< practica num="7.3" tipo="Autónoma" duracion="3 sessions" nivel="2" ra="RA3: c, d, e" sgbd="Oracle 26ai · EDUGEST" entrega="p7_3.sql comentat" >}}

#### Objectiu

Resoldre de forma autònoma consultes de diverses taules, decidint el tipus de composició i combinant-les amb agrupaments.

#### Enunciat

**J1.** Llistat de mòduls amb el nom complet del seu cicle, només de 2n curs.

{{< solucion id="ud07-001" title="Solució J1" />}}

**J2.** Professorat amb el nom del seu departament i, si és cap d'algun departament, el nom d'eixe departament (si no, buit).

{{< solucion id="ud07-002" title="Solució J2" />}}

**J3.** Càrrega docent: per a cada professor que impartix classe, nombre de mòduls, nombre de grups distints i hores setmanals totals, de més a menys hores.

{{< solucion id="ud07-003" title="Solució J3" />}}

**J4.** Tots els grups amb el seu nombre d'alumnes i el seu tutor; han d'aparéixer els grups sense alumnes i sense tutor.

{{< solucion id="ud07-004" title="Solució J4" />}}

**J5.** Percentatge d'aprovats per mòdul de DAM (codi, nom, matrícules qualificades i percentatge amb un decimal), del pitjor al millor percentatge.

{{< solucion id="ud07-005" title="Solució J5" />}}

**J6.** Alumnat amb més de 3 hores de faltes **no justificades** en total (nom, grup i hores).

{{< solucion id="ud07-006" title="Solució J6" />}}

**J7.** Professorat del departament d'Informàtica i Comunicacions que **no** és tutor de cap grup.

{{< solucion id="ud07-007" title="Solució J7" />}}

**J8.** Per a cada alumne de 1DAM, la seua nota en *Bases de dades* (0484) i en *Programació* (0485) en la mateixa fila.

{{< solucion id="ud07-008" title="Solució J8" />}}

#### Comprovació

{{% comprobacion %}}
- [ ] Has triat composició interna o externa segons la pregunta i ho justifiques en un comentari.
- [ ] J4 mostra 2ASIR amb 0 alumnes i «(sin tutor)».
- [ ] J5 no dividix entre les matrícules sense qualificar.
{{% /comprobacion %}}

---

## Pràctica 7.4 · Subconsultes

{{< practica num="7.4" tipo="Autónoma" duracion="2 sessions" nivel="2" ra="RA3: f" sgbd="Oracle 26ai · EDUGEST" entrega="p7_4.sql" >}}

#### Enunciat

**S1.** Alumnat de major edat (pot haver-hi empats).

{{< solucion id="ud07-009" title="Solució S1" />}}

**S2.** Mòduls de DAW amb més hores que **qualsevol** mòdul de 2n de DAM.

{{< solucion id="ud07-010" title="Solució S2" />}}

**S3.** Alumnes que tenen **alguna** falta d'assistència (usa `EXISTS`).

{{< solucion id="ud07-011" title="Solució S3" />}}

**S4.** Alumnes amb grup que **no** tenen cap falta.

{{< solucion id="ud07-012" title="Solució S4" />}}

**S5.** Per a cada alumne de 2DAW, la seua nota mitjana i la diferència amb la mitjana del **seu grup** (subconsulta correlacionada).

{{< solucion id="ud07-013" title="Solució S5" />}}

**S6.** El grup (o grups) amb més alumnes. Resol-ho amb una subconsulta al `HAVING`.

{{< solucion id="ud07-014" title="Solució S6" />}}

**S7.** Explica per què esta consulta no torna files i corregix-la de dues formes:

```sql
SELECT nombre FROM profesor WHERE id_profesor NOT IN (SELECT id_tutor FROM grupo);
```

{{< solucion id="ud07-015" title="Solució S7" />}}

---

## Pràctica 7.5 · Múltiples seleccions i vistes

{{< practica num="7.5" tipo="Autónoma" duracion="1 sessió" nivel="2" ra="RA3: g · RA2: f" sgbd="Oracle 26ai · EDUGEST" entrega="p7_5.sql" >}}

#### Enunciat

**U1.** Llista única de totes les **localitats** en què viu alumnat de DAM o de DAW (sense repetir).

{{< solucion id="ud07-016" title="Solució U1" />}}

**U2.** Localitats amb alumnat **tant** de DAM **com** de DAW.

{{< solucion id="ud07-017" title="Solució U2" />}}

**U3.** Codis de mòdul oficials que estan en DAM però **no** en DAW.

{{< solucion id="ud07-018" title="Solució U3" />}}

**U4.** Crea la vista `v_acta` de la [teoria](/ud07-consultas-avanzadas/ud07-teoria#7-vistes-amb-composicions) i usa-la per a obtindre el nombre d'APTOS, NO APTOS i NC de cada mòdul de 1DAW.

{{< solucion id="ud07-019" title="Solució U4" />}}

---

## Pràctica 7.6 · Optimització: mesurar abans i després

{{< practica num="7.6" tipo="Guiada" duracion="2 sessions" nivel="3" ra="RA3: h" sgbd="Oracle 26ai · SQL Developer (Explicar pla, Autotrace) o SQLcl" entrega="p7_6.sql + taula de mesuraments + captures dels plans" >}}

#### Objectiu

Comprovar amb mesuraments reals com afecten els índexs i la forma d'escriure una consulta al seu pla d'execució i al seu rendiment.

#### Context

EduGest té molt poques dades per a notar diferències. Simularem l'**històric d'accessos** del portal de l'alumnat durant diversos cursos: mig milió de files.

#### Desenvolupament

{{% steps %}}

1. **Crea i omple la taula** (connectat com `EDUGEST`). `CONNECT BY LEVEL` és un truc d'Oracle per a generar files:

    ```sql
    CREATE TABLE acceso_portal (
        id_acceso   NUMBER(10)   CONSTRAINT pk_acceso_portal PRIMARY KEY,
        id_alumno   NUMBER(6)    NOT NULL,
        fecha_hora  DATE         NOT NULL,
        ip          VARCHAR2(15) NOT NULL,
        seccion     VARCHAR2(20) NOT NULL
    );

    INSERT INTO acceso_portal
    SELECT LEVEL,
           MOD(LEVEL * 7, 5000) + 1,
           DATE '2022-09-01' + MOD(LEVEL * 13, 1460) + MOD(LEVEL, 86400) / 86400,
           '10.0.' || MOD(LEVEL, 256) || '.' || MOD(LEVEL * 3, 256),
           CASE MOD(LEVEL, 5) WHEN 0 THEN 'NOTAS' WHEN 1 THEN 'FALTAS' WHEN 2 THEN 'HORARIO'
                              WHEN 3 THEN 'MENSAJES' ELSE 'PERFIL' END
    FROM   dual
    CONNECT BY LEVEL <= 500000;
    COMMIT;

    EXEC DBMS_STATS.GATHER_TABLE_STATS(USER, 'ACCESO_PORTAL');
    SET TIMING ON
    ```

2. **Consulta 1: buscar per alumne sense índex.**

    ```sql
    SELECT COUNT(*) FROM acceso_portal WHERE id_alumno = 1234;
    ```

    Obtín el pla (F10 en SQL Developer, o `EXPLAIN PLAN FOR ...` + `SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);`). Anota l'operació, el cost i el temps. Ha d'aparéixer `TABLE ACCESS FULL`.

3. **Crea un índex** i repetix el mesurament:

    ```sql
    CREATE INDEX ix_acceso_alumno ON acceso_portal (id_alumno);
    ```

    El pla ha de canviar a `INDEX RANGE SCAN`, amb un cost molt menor. Com que només es demana `COUNT(*)`, Oracle ni tan sols necessita llegir la taula.

4. **Consulta 2: funció sobre la columna.** Compara estes dues consultes equivalents:

    ```sql
    -- (a) Funció sobre la columna fecha_hora
    SELECT COUNT(*) FROM acceso_portal WHERE TRUNC(fecha_hora) = DATE '2024-03-15';
    -- (b) Rang sobre la columna sense modificar-la
    SELECT COUNT(*) FROM acceso_portal
    WHERE  fecha_hora >= DATE '2024-03-15' AND fecha_hora < DATE '2024-03-16';
    ```

    Crea `CREATE INDEX ix_acceso_fecha ON acceso_portal (fecha_hora);` i compara els plans de (a) i (b). Només (b) pot usar l'índex.

5. **Consulta 3: selectivitat.** Amb un índex sobre `seccion`, usa Oracle l'índex per a `WHERE seccion = 'NOTAS'`? Eixa condició torna el 20 % de la taula: el més probable és que l'optimitzador preferisca `TABLE ACCESS FULL`. Comprova-ho i explica per què és la decisió correcta.

6. **Consulta 4: composició.** Mesura la composició amb `ALUMNO` abans i després que existisca l'índex `ix_acceso_alumno`:

    ```sql
    SELECT a.cod_grupo, COUNT(*) AS accesos
    FROM   acceso_portal ap JOIN alumno a ON a.id_alumno = ap.id_alumno
    GROUP  BY a.cod_grupo;
    ```

7. **Neteja** en acabar: `DROP TABLE acceso_portal PURGE;`

{{% /steps %}}

#### Comprovació

{{% comprobacion %}}
Completa la taula de mesuraments amb les teues dades (els valors exactes depenen del teu equip):

| Consulta | Sin índice: operación / coste / tiempo | Con índice: operación / coste / tiempo |
|---|---|---|
| 1 · `id_alumno = 1234` | `TABLE ACCESS FULL` / … / … | `INDEX RANGE SCAN` / … / … |
| 2a · `TRUNC(fecha_hora) = ...` | | |
| 2b · rango de fechas | | |
| 3 · `seccion = 'NOTAS'` | | |
| 4 · composición con `ALUMNO` | | |

- [ ] La consulta 1 torna 100 accessos i el seu cost baixa de forma clara amb l'índex.
- [ ] Expliques per què 2a no usa l'índex i com ho aconseguiries sense reescriure-la (índex basat en funció sobre `TRUNC(fecha_hora)`).
- [ ] Expliques per què en la consulta 3 un accés complet pot ser millor que l'índex.

> [!WARNING]
> Els mesuraments de temps varien entre execucions perquè Oracle guarda en memòria cau els blocs llegits. Executa cada consulta **dos o tres voltes** i anota el temps de les últimes. El **cost** del pla és una estimació de l'optimitzador, no un temps.
{{% /comprobacion %}}

#### Ampliació

Afig `/*+ FULL(ap) */` just després de `SELECT` en la consulta 1 amb índex i compara. Els *hints* obliguen l'optimitzador a usar un pla concret; en producció només s'usen quan s'ha demostrat que l'optimitzador s'equivoca.

---

## Pràctica 7.7 · Repte: el quadre de comandament

{{< practica num="7.7" tipo="Reto" duracion="2 sessions" nivel="3" ra="RA3: c, d, e, f, g, h" sgbd="Oracle 26ai · EDUGEST" entrega="p7_7.sql + defensa oral" >}}

#### Enunciat

La direcció vol un **quadre de comandament** amb una sola consulta per indicador. Resol cadascun amb la tècnica que consideres més adequada i justifica l'elecció:

1. Per a cada cicle (inclòs SMR): nombre de grups, d'alumnes, de matrícules i nota mitjana.
2. Els **dos** millors alumnes de cada grup segons la seua nota mitjana (pista: `RANK()` o `ROW_NUMBER()` amb `PARTITION BY`).
3. Per a cada professor que impartix classe: la nota mitjana dels seus alumnes en els mòduls que impartix **en els grups en què els impartix**. (Compte: la composició entre `IMPARTE` i `MATRICULA` ha d'usar el mòdul **i** el grup de l'alumne.)
4. Alumnes que han suspés **tots** els mòduls en què estan qualificats.
5. Percentatge d'hores de falta justificades sobre el total, per grup.
6. Escriu una de les consultes anteriors de dues formes distintes (per exemple, subconsulta enfront de composició) i compara els seus plans d'execució.

#### Comprovació

{{% comprobacion %}}
- [ ] L'indicador 1 té 4 files i SMR apareix amb zeros.
- [ ] L'indicador 3 no barreja alumnes d'altres grups amb el mateix mòdul.
- [ ] Pots defendre cada consulta i explicar el seu pla d'execució.

{{% details title="Pista per a l'indicador 4" %}}
«Tots suspesos» equival a «no n'hi ha cap d'aprovat» i «en té almenys un de qualificat»: `NOT EXISTS (... nota_final >= 5)` i `EXISTS (... nota_final IS NOT NULL)`. Una altra forma: `GROUP BY` alumne amb `HAVING MAX(nota_final) < 5`.
{{% /details %}}
{{% /comprobacion %}}

---

## Projecte EduGest · UD07: informes

{{< practica num="EduGest-7" tipo="Proyecto" duracion="Treball transversal (2 setmanes)" nivel="3" ra="RA3: a-h · RA2: f" sgbd="Oracle 26ai · EDUGEST" entrega="edugest/06_informes.sql + 07_vistas_informes.sql + docs/07-optimizacion.md" >}}

#### Enunciat

1. Escriu **deu informes** per a EduGest que en conjunt usen: composicions internes i externes (almenys tres taules en algun), consultes resum amb `HAVING`, subconsultes (una correlacionada i una amb `EXISTS`), un operador de conjunts i una funció analítica.
2. Converteix els tres informes més usats en **vistes** i concedix `SELECT` sobre elles al rol adequat de la pràctica 5.7.
3. **Optimització:** tria dos dels teus informes, obtín el seu pla d'execució, proposa una millora (índex o reescriptura) i documenta l'abans i el després en `07-optimizacion.md`. Si EduGest té poques dades per a notar la diferència, explica-ho i recolza't en la pràctica 7.6.

#### Comprovació

{{% comprobacion %}}
- [ ] Cada informe té un comentari amb el perfil que l'usa, la pregunta que respon i el nombre de files.
- [ ] Les vistes es poden consultar des de l'usuari del rol corresponent.
- [ ] El document d'optimització inclou els plans abans i després.
{{% /comprobacion %}}
