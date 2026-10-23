---
title: "Manipulació de dades i transaccions - Pràctiques"
weight: 2
bookToc: true
---

# UD08 · Pràctiques

{{< ra "RA4:a,b,c,d,e,f,g,h" "RA6:f" >}}

| Pràctica | Tipus | Nivell | CE principals |
|---|---|---|---|
| [8.1 Altes, canvis i baixes a EduGest](#pràctica-81--altes-canvis-i-baixes-a-edugest) | Guiada | ●○○ | RA4.a, RA4.b |
| [8.2 Còpies, històrics i INSERT … SELECT](#pràctica-82--còpies-històrics-i-insert--select) | Guiada | ●●○ | RA4.c |
| [8.3 Modificacions amb subconsultes](#pràctica-83--modificacions-amb-subconsultes) | Autònoma | ●●○ | RA4.b, RA4.c, RA4.h |
| [8.4 Laboratori de transaccions](#pràctica-84--laboratori-de-transaccions) | Guiada | ●●○ | RA4.e, RA4.f |
| [8.5 Dues sessions, una dada: concurrència i bloquejos](#pràctica-85--dues-sessions-una-dada-concurrència-i-bloquejos) | Guiada | ●●● | RA4.g, RA4.h |
| [8.6 Càrrega de notes amb MERGE](#pràctica-86--càrrega-de-notes-amb-merge) | Autònoma | ●●○ | RA4.b, RA4.c |
| [8.7 Repte: guió de promoció de curs](#pràctica-87--repte-guió-de-promoció-de-curs) | Repte | ●●● | RA4.d, RA4.e, RA4.f, RA4.h |
| [Projecte EduGest · UD08](#projecte-edugest--ud08-guions-de-manteniment) | Projecte | ●●● | RA4 complet |

> [!IMPORTANT]
> Abans de **cada** pràctica, restaura EduGest executant els scripts 01 i 02 del [projecte](/guia/proyecto-edugest#4-scripts-descarregables). Els números de files afectades que s'indiquen suposen les dades originals.

---

## Pràctica 8.1 · Altes, canvis i baixes a EduGest

{{< practica num="8.1" tipo="Guiada" duracion="2 sessions" nivel="1" ra="RA4: a, b" sgbd="Oracle 26ai · SQL Developer" entrega="p8_1.sql + captures de la reixeta" >}}

#### Objectiu

Inserir, modificar i esborrar dades amb SQL i amb l'eina gràfica, comprovant en cada pas l'efecte de les restriccions i la necessitat de confirmar els canvis.

#### Desenvolupament

{{% steps %}}

1. **Alta d'una alumna.** Fixa't que no indiquem `id_alumno`:

    ```sql
    INSERT INTO alumno (nia, dni, nombre, apellidos, fecha_nacimiento, email, localidad, cod_grupo)
    VALUES ('10452001', '48123456J', 'Marina', 'López Ortega', DATE '2007-03-14',
            'marinalopez@alu.edugest.es', 'Alicante', '1DAM');

    SELECT id_alumno, nombre, apellidos FROM alumno WHERE nia = '10452001';
    ```

    L'identificador generat ha de ser **1001**, perquè la columna identitat comença en eixe valor.

2. **Comprova l'aïllament.** Obri una **segona connexió** (un altre full de treball amb *Nova sessió*, `Ctrl+Mayús+N`, o SQLcl) i busca Marina. **No apareix**: el canvi no està confirmat. Torna a la primera sessió i executa `COMMIT;`. Repeteix la consulta en la segona: ara sí que apareix.

3. **Matricula-la** en Bases de dades de DAM per a 2026-27:

    ```sql
    INSERT INTO matricula (id_alumno, id_modulo, curso_academico, fecha_matricula)
    VALUES (1001, (SELECT id_modulo FROM modulo WHERE codigo = '0484' AND cod_ciclo = 'DAM'),
            '2026-27', DATE '2026-09-10');
    ```

    Quin valor ha pres `convocatoria`? I `nota_final`? Per què?

4. **Prova les restriccions** amb estes insercions incorrectes i anota l'error de cadascuna:

    ```sql
    -- a) Matrícula duplicada (mateix alumne, mòdul i curs)
    INSERT INTO matricula (id_alumno, id_modulo, curso_academico) VALUES (1001, 2, '2026-27');
    -- b) Curs acadèmic amb format incorrecte
    INSERT INTO matricula (id_alumno, id_modulo, curso_academico) VALUES (1001, 3, '2026/27');
    -- c) Nota fora de rang
    UPDATE matricula SET nota_final = 11 WHERE id_alumno = 1001;
    ```

5. **Modifica** el telèfon de Marina i el grup dels tres alumnes sense grup:

    ```sql
    UPDATE alumno SET telefono = '612345678' WHERE id_alumno = 1001;     -- 1 fila
    SELECT id_alumno, nombre FROM alumno WHERE cod_grupo IS NULL;       -- comprovar abans: 3 files
    UPDATE alumno SET cod_grupo = '1DAW' WHERE cod_grupo IS NULL;       -- 3 files
    ```

6. **Edita amb la reixeta.** Obri la taula `ALUMNO` → pestanya *Dades*, canvia la localitat de Marina a «Elche» i prem *Confirmar* (`F11`). Obri el *Log de sentències* (*Veure → Log*) i observa l'`UPDATE` que ha generat l'eina.

7. **Esborra** Marina. Què passa amb la seua matrícula? Consulta abans les claus alienes en `USER_CONSTRAINTS`:

    ```sql
    DELETE FROM alumno WHERE id_alumno = 1001;
    SELECT COUNT(*) FROM matricula WHERE id_alumno = 1001;   -- 0: esborrada en cascada
    COMMIT;
    ```

{{% /steps %}}

#### Comprovació

{{% comprobacion %}}
- [ ] El pas 4 produïx ORA-00001 (`UQ_MATRICULA`), ORA-02290 (`CK_MATRICULA_CURSO`) i ORA-02290 (`CK_MATRICULA_NOTA`).
- [ ] La matrícula del pas 3 té `convocatoria = 1` (valor per defecte) i `nota_final` a `NULL`.
- [ ] Després del pas 7, `SELECT COUNT(*) FROM alumno;` torna 32.
{{% /comprobacion %}}

#### Errors habituals

> [!WARNING]
> - Si la segona sessió **es queda penjada** en el pas 5 o 6, és que intenta modificar una fila bloquejada per la primera sessió, que encara no ha fet `COMMIT`. Ho estudiaràs en la pràctica 8.5.
> - Tancar SQL Developer amb canvis pendents mostra un avís per a confirmar-los o desfer-los. **Llig l'avís.**

---

## Pràctica 8.2 · Còpies, històrics i INSERT … SELECT

{{< practica num="8.2" tipo="Guiada" duracion="1 sessió" nivel="2" ra="RA4: c" sgbd="Oracle 26ai · EDUGEST" entrega="p8_2.sql" >}}

#### Objectiu

Guardar en taules el resultat de consultes: còpies de seguretat ràpides, taules d'històric i taules de resum.

#### Desenvolupament

{{% steps %}}

1. **Còpia de seguretat amb CTAS** abans d'un canvi delicat:

    ```sql
    CREATE TABLE bak_matricula AS SELECT * FROM matricula;
    SELECT COUNT(*) FROM bak_matricula;     -- 143
    ```

    Compara les restriccions de `MATRICULA` i de `BAK_MATRICULA` en `USER_CONSTRAINTS`. Quines s'han copiat?

2. **Taula d'històric** amb el seu propi disseny i càrrega amb `INSERT ... SELECT`:

    ```sql
    CREATE TABLE historico_nota (
        curso_academico  CHAR(7),
        nia              CHAR(8),
        alumno           VARCHAR2(130),
        cod_ciclo        VARCHAR2(5),
        cod_modulo       CHAR(4),
        nota_final       NUMBER(4,2),
        fecha_archivo    DATE DEFAULT SYSDATE,
        CONSTRAINT pk_historico_nota PRIMARY KEY (curso_academico, nia, cod_ciclo, cod_modulo)
    );

    INSERT INTO historico_nota (curso_academico, nia, alumno, cod_ciclo, cod_modulo, nota_final)
    SELECT m.curso_academico, a.nia, a.apellidos || ', ' || a.nombre, mo.cod_ciclo, mo.codigo, m.nota_final
    FROM   matricula m
           JOIN alumno a  ON a.id_alumno  = m.id_alumno
           JOIN modulo mo ON mo.id_modulo = m.id_modulo
    WHERE  m.curso_academico = '2025-26';
    -- 143 files creades
    COMMIT;
    ```

3. **Taula de resum** per al quadre de comandament:

    ```sql
    CREATE TABLE resumen_grupo AS
    SELECT a.cod_grupo,
           COUNT(*)                                          AS matriculas,
           SUM(CASE WHEN m.nota_final >= 5 THEN 1 ELSE 0 END) AS aprobadas,
           ROUND(AVG(m.nota_final), 2)                       AS media,
           SYSDATE                                           AS calculado
    FROM   matricula m JOIN alumno a ON a.id_alumno = m.id_alumno
    GROUP  BY a.cod_grupo;

    SELECT cod_grupo, matriculas, aprobadas, media FROM resumen_grupo ORDER BY cod_grupo;
    ```

    | COD_GRUPO | MATRICULAS | APROBADAS | MEDIA |
    |---|---|---|---|
    | 1ASIR | 25 | 21 | 7.07 |
    | 1DAM | 35 | 27 | 6.4 |
    | 1DAW | 30 | 24 | 6.19 |
    | 2DAM | 33 | 23 | 6.17 |
    | 2DAW | 20 | 15 | 5.93 |

4. **Restaura des de la còpia.** Simula un desastre i recupera les dades:

    ```sql
    UPDATE matricula SET nota_final = NULL;   -- desastre: 143 files
    COMMIT;                                   -- i a més confirmat!

    UPDATE matricula m
    SET    nota_final = (SELECT b.nota_final FROM bak_matricula b WHERE b.id_matricula = m.id_matricula);
    COMMIT;

    SELECT COUNT(nota_final) FROM matricula;  -- 137 una altra vegada
    ```

5. **Neteja:** `DROP TABLE bak_matricula PURGE; DROP TABLE resumen_grupo PURGE;`

{{% /steps %}}

#### Comprovació

{{% comprobacion %}}
- [ ] `BAK_MATRICULA` només conserva les restriccions `NOT NULL`.
- [ ] `HISTORICO_NOTA` té 143 files i la seua clau primària impedix arxivar dues voltes el mateix curs: repeteix l'`INSERT` i comprova que falla amb ORA-00001.
- [ ] Després del pas 4, les notes tornen a ser les originals.
{{% /comprobacion %}}

#### Ampliació

Per què la clau primària d'`HISTORICO_NOTA` inclou `cod_ciclo`? Pensa en el mòdul 0484, que existix en DAM i en DAW.

---

## Pràctica 8.3 · Modificacions amb subconsultes

{{< practica num="8.3" tipo="Autónoma" duracion="2 sessions" nivel="2" ra="RA4: b, c, h" sgbd="Oracle 26ai · EDUGEST" entrega="p8_3.sql (cada sentència amb el seu SELECT de comprovació)" >}}

#### Objectiu

Escriure modificacions que depenen de dades d'altres taules, comprovant abans i després les files afectades.

#### Enunciat

Executa les tasques **en ordre** sobre les dades originals. Per a cadascuna escriu: (1) un `SELECT` que mostre les files que es modificaran, (2) la sentència de modificació i (3) un `SELECT` de verificació. El nombre de files afectades ha de coincidir amb l'indicat.

| # | Tasca | Files |
|---|---|---|
| M1 | Donar d'alta l'alumna Marina López Ortega (NIA 10452001, nascuda el 14/03/2007, d'Alacant, grup 1DAM) | 1 |
| M2 | Matricular Marina en **tots** els mòduls de 1r de DAM per al curs 2026-27 amb una sola sentència | 5 |
| M3 | Pujar a 5 les notes de Bases de dades de DAM (`0484`) compreses entre 4,5 i 5 (sense incloure el 5) | 2 |
| M4 | Assignar el grup 1DAW als alumnes sense grup nascuts en 2006 | 3 |
| M5 | Assignar com a tutor de 2ASIR l'únic professor del departament d'Informàtica que no impartix classe (sense escriure el seu identificador) | 1 |
| M6 | Justificar totes les faltes de l'alumna Martina Alemany Vidal | 3 |
| M7 | Esborrar les faltes justificades anteriors a l'1 de novembre de 2025 | 5 |
| M8 | Augmentar un 10 % (arredonit) les hores dels mòduls de 2n de DAW | 4 |
| M9 | Canviar el domini del correu de **tot** el professorat de `@edugest.es` a `@iesserragelada.es` | 12 |
| M10 | Donar de baixa Adrián Ferri Baeza (id 1). Abans, compta quantes files de **cada taula** desapareixeran | 1 + 5 + 3 |

{{% details title="Pistes" %}}
- **M2:** `INSERT INTO matricula (...) SELECT 1001, id_modulo, '2026-27', ... FROM modulo WHERE ...`. Si Marina no té l'id 1001 en la teua base de dades, obtín l'id amb una subconsulta pel seu NIA.
- **M6:** les faltes no tenen l'alumne: cal arribar a ell a través de la matrícula. `WHERE id_matricula IN (SELECT m.id_matricula FROM matricula m JOIN alumno a ... )`. Martina té 3 faltes i una ja està justificada: sense condició addicional es modifiquen 3; si afigs `AND justificada = 'N'`, només 2. Les dues opcions deixen el mateix resultat.
- **M9:** `REPLACE(email, '@edugest.es', '@iesserragelada.es')`. Complix el nou correu el `CHECK` de l'email?
- **M10:** les faltes desapareixen perquè `fk_falta_matricula` també té `ON DELETE CASCADE`.
{{% /details %}}

{{< solucion id="ud08-001" title="Solució (M3, M5 y M10)" />}}

#### Comprovació

{{% comprobacion %}}
- [ ] Les files afectades coincidixen amb la taula. Si no coincidixen, **no** confirmes: fes `ROLLBACK` i revisa la condició.
- [ ] Al final, `SELECT COUNT(*) FROM alumno;` torna 32 (33 amb Marina menys Adrián) i `SELECT COUNT(*) FROM matricula;` torna 143 (+5 −5).
- [ ] Cap sentència usa identificadors escrits a mà quan l'enunciat demana obtindre'ls.

> [!CAUTION]
> M10 elimina documents acadèmics en cascada. En un sistema real no s'esborraria l'alumne: es marcaria com a **baixa** (per exemple, amb una columna `fecha_baja`) per a conservar el seu expedient. Escriu en el teu script un comentari que propose esta alternativa.
{{% /comprobacion %}}

---

## Pràctica 8.4 · Laboratori de transaccions

{{< practica num="8.4" tipo="Guiada" duracion="1 sessió" nivel="2" ra="RA4: e, f" sgbd="Oracle 26ai" entrega="p8_4.sql + taula de resultats" >}}

#### Objectiu

Comprovar experimentalment el funcionament de `COMMIT`, `ROLLBACK`, `SAVEPOINT`, la confirmació implícita del DDL i l'atomicitat de sentència.

#### Preparació

```sql
CREATE TABLE cuenta (
    id_cuenta  CHAR(1)       CONSTRAINT pk_cuenta PRIMARY KEY,
    titular    VARCHAR2(50)  NOT NULL,
    saldo      NUMBER(12,2)  NOT NULL CONSTRAINT ck_cuenta_saldo CHECK (saldo >= 0)
);
INSERT INTO cuenta VALUES ('A', 'Asociación de alumnado', 1000);
INSERT INTO cuenta VALUES ('B', 'Viaje de fin de curso',   200);
INSERT INTO cuenta VALUES ('C', 'Cantina',                 50);
COMMIT;
```

#### Desenvolupament

Executa cada experiment i **prediu** els saldos finals abans de consultar `SELECT * FROM cuenta ORDER BY id_cuenta;`.

| Exp. | Sentències | A | B | C |
|---|---|---|---|---|
| 1 | `UPDATE cuenta SET saldo = saldo - 100 WHERE id_cuenta = 'A';` `UPDATE cuenta SET saldo = saldo + 100 WHERE id_cuenta = 'B';` `ROLLBACK;` | | | |
| 2 | Les dues mateixes actualitzacions i `COMMIT;` | | | |
| 3 | `UPDATE cuenta SET saldo = saldo + 10 WHERE id_cuenta = 'C';` `SAVEPOINT s1;` `UPDATE cuenta SET saldo = 0;` `ROLLBACK TO SAVEPOINT s1;` `COMMIT;` | | | |
| 4 | `UPDATE cuenta SET saldo = saldo - 50 WHERE id_cuenta = 'B';` `UPDATE cuenta SET saldo = saldo - 100 WHERE id_cuenta = 'C';` (falla) `COMMIT;` | | | |
| 5 | `UPDATE cuenta SET saldo = saldo + 1000 WHERE id_cuenta = 'A';` `CREATE TABLE prueba (x NUMBER);` `ROLLBACK;` | | | |
| 6 | `UPDATE cuenta SET saldo = saldo - 10;` i tanca la sessió **de forma anòmala** (tanca la finestra del terminal o mata el procés). Torna a connectar | | | |

{{< solucion id="ud08-002" title="Resultats esperats" />}}

#### Comprovació

{{% comprobacion %}}
- [ ] Has predit correctament almenys 5 dels 6 experiments. Si no, explica en què t'has equivocat.
- [ ] Pots explicar amb les teues paraules l'**atomicitat de sentència** (experiment 4) i per què és perillosa si l'aplicació confirma sense comprovar els errors.
{{% /comprobacion %}}

#### Ampliació: la transferència segura

Escriu la transferència de 500 € d'A a C com una transacció que **no** confirme res si alguna de les dues actualitzacions no afecta exactament una fila. Usa `SQL%ROWCOUNT` en un bloc anònim (avanç de la UD09):

```sql
BEGIN
    UPDATE cuenta SET saldo = saldo - 500 WHERE id_cuenta = 'A';
    IF SQL%ROWCOUNT <> 1 THEN ROLLBACK; RAISE_APPLICATION_ERROR(-20001, 'Cuenta origen inexistente'); END IF;
    UPDATE cuenta SET saldo = saldo + 500 WHERE id_cuenta = 'Z';     -- compte inexistent
    IF SQL%ROWCOUNT <> 1 THEN ROLLBACK; RAISE_APPLICATION_ERROR(-20002, 'Cuenta destino inexistente'); END IF;
    COMMIT;
END;
/
```

---

## Pràctica 8.5 · Dues sessions, una dada: concurrència i bloquejos

{{< practica num="8.5" tipo="Guiada" duracion="2 sessions" nivel="3" ra="RA4: g, h" sgbd="Oracle 26ai · dues sessions simultànies (dos fulls amb sessió pròpia o dos terminals SQLcl) + SYSTEM" entrega="Cronogrames completats + captures" >}}

#### Objectiu

Observar en directe els efectes de les distintes polítiques de bloqueig i dels nivells d'aïllament.

#### Preparació

Usa la taula `CUENTA` de la pràctica 8.4 restaurada a A = 1000, B = 200, C = 50. Obri **dues sessions** com a `EDUGEST`: **S1** i **S2**. En SQL Developer, obri el segon full amb *Full de treball SQL no compartit* (`Ctrl+Mayús+N`); si no, els dos fulls compartixen sessió i no veuràs res.

#### Experiment 1 · Les lectures no es bloquegen

| t | S1 | S2 |
|---|---|---|
| 1 | `UPDATE cuenta SET saldo = 0 WHERE id_cuenta = 'A';` | |
| 2 | | `SELECT saldo FROM cuenta WHERE id_cuenta = 'A';` → ¿? |
| 3 | `COMMIT;` | |
| 4 | | `SELECT saldo FROM cuenta WHERE id_cuenta = 'A';` → ¿? |

{{% details title="Resultat" %}}
En t2, S2 veu **1000** sense esperar: Oracle li mostra l'última versió confirmada. En t4 veu **0**. No hi ha lectures brutes ni lectors bloquejats.
{{% /details %}}

#### Experiment 2 · Les escriptures sobre la mateixa fila esperen

| t | S1 | S2 |
|---|---|---|
| 1 | `UPDATE cuenta SET saldo = saldo + 100 WHERE id_cuenta = 'B';` | |
| 2 | | `UPDATE cuenta SET saldo = saldo + 200 WHERE id_cuenta = 'B';` → ¿? |
| 3 | Como `SYSTEM`, en una tercera sesión: `SELECT sid, username, blocking_session, event FROM v$session WHERE username = 'EDUGEST';` | |
| 4 | `COMMIT;` | → ¿qué ocurre en S2? |
| 5 | | `COMMIT;` y consulta el saldo de B |

{{% details title="Resultat" %}}
En t2, S2 es queda **esperant**. En t3 veuràs que la sessió de S2 té `blocking_session` igual al SID de S1 i l'esdeveniment `enq: TX - row lock contention`. En t4 S2 continua. El saldo final de B és 200 + 100 + 200 = **500**: no es perd cap actualització perquè cada `UPDATE` llig el valor **actual** en executar-se.
{{% /details %}}

#### Experiment 3 · L'actualització perduda (a l'aplicació)

Simulem dues aplicacions que **lligen** el saldo, calculen el nou valor **fora** de la base de dades i l'escriuen:

| t | S1 | S2 |
|---|---|---|
| 1 | `SELECT saldo FROM cuenta WHERE id_cuenta = 'C';` → 50 | |
| 2 | | `SELECT saldo FROM cuenta WHERE id_cuenta = 'C';` → 50 |
| 3 | `UPDATE cuenta SET saldo = 80 WHERE id_cuenta = 'C';` (50 + 30) | |
| 4 | `COMMIT;` | |
| 5 | | `UPDATE cuenta SET saldo = 70 WHERE id_cuenta = 'C';` (50 + 20) |
| 6 | | `COMMIT;` |

El saldo final és **70**: s'ha perdut l'ingrés de 30 de S1. Repeteix l'experiment amb les dues solucions i comprova que el saldo final és 100:

{{< tabs >}}
{{% tab "Pessimista: FOR UPDATE" %}}
En t1 i t2, ambdues sessions lligen amb `SELECT saldo FROM cuenta WHERE id_cuenta = 'C' FOR UPDATE;`. S2 **espera** en t2 fins que S1 confirma en t4, i llavors llig 80. Escriu 80 + 20 = 100.
{{% /tab %}}
{{% tab "Optimista: comprovar en escriure" %}}
En t5, S2 escriu `UPDATE cuenta SET saldo = 70 WHERE id_cuenta = 'C' AND saldo = 50;` → **0 files**: el saldo ja no és el que va llegir. L'aplicació torna a llegir (80) i escriu `... SET saldo = 100 WHERE id_cuenta = 'C' AND saldo = 80;` → 1 fila.
{{% /tab %}}
{{< /tabs >}}

#### Experiment 4 · NOWAIT i WAIT

| t | S1 | S2 |
|---|---|---|
| 1 | `SELECT * FROM cuenta WHERE id_cuenta = 'A' FOR UPDATE;` | |
| 2 | | `SELECT * FROM cuenta WHERE id_cuenta = 'A' FOR UPDATE NOWAIT;` → ¿? |
| 3 | | `SELECT * FROM cuenta WHERE id_cuenta = 'A' FOR UPDATE WAIT 3;` → ¿? |
| 4 | `ROLLBACK;` | |

{{% details title="Resultat" %}}
t2: error immediat `ORA-00054: resource busy and acquire with NOWAIT specified or timeout expired`. t3: espera 3 segons i dona `ORA-30006: resource busy; acquire with WAIT timeout expired`. Són útils en aplicacions que no han de quedar-se penjades.
{{% /details %}}

#### Experiment 5 · Interbloqueig

| t | S1 | S2 |
|---|---|---|
| 1 | `UPDATE cuenta SET saldo = saldo - 1 WHERE id_cuenta = 'A';` | |
| 2 | | `UPDATE cuenta SET saldo = saldo - 1 WHERE id_cuenta = 'B';` |
| 3 | `UPDATE cuenta SET saldo = saldo + 1 WHERE id_cuenta = 'B';` (espera) | |
| 4 | | `UPDATE cuenta SET saldo = saldo + 1 WHERE id_cuenta = 'A';` |
| 5 | → ¿? | |

{{% details title="Resultat" %}}
Als pocs segons, Oracle detecta el cicle i una de les sessions (normalment la que esperava primer, S1) rep `ORA-00060: deadlock detected while waiting for resource`. Només es desfà **eixa sentència**: la sessió continua tenint bloquejada la fila A i ha de fer `ROLLBACK`. Repeteix l'experiment fent que **les dues** sessions actualitzen primer A i després B: l'interbloqueig desapareix (S2 simplement espera).
{{% /details %}}

#### Experiment 6 · Informe consistent amb READ ONLY

| t | S1 (cap d'estudis, informe) | S2 (secretaria) |
|---|---|---|
| 1 | `SET TRANSACTION READ ONLY;` `SELECT SUM(saldo) FROM cuenta;` | |
| 2 | | `UPDATE cuenta SET saldo = saldo + 1000 WHERE id_cuenta = 'A';` `COMMIT;` |
| 3 | `SELECT SUM(saldo) FROM cuenta;` → mateix valor que en t1? | |
| 4 | `COMMIT;` i repeteix la suma | |

#### Comprovació

{{% comprobacion %}}
- [ ] Has completat els sis cronogrames amb els resultats obtinguts.
- [ ] Has capturat la consulta de `v$session` de l'experiment 2 mostrant la sessió bloquejada.
- [ ] Expliques, per a cada experiment, quin problema de concurrència apareix o s'evita.
{{% /comprobacion %}}

---

## Pràctica 8.6 · Càrrega de notes amb MERGE

{{< practica num="8.6" tipo="Autónoma" duracion="1 sessió" nivel="2" ra="RA4: b, c" sgbd="Oracle 26ai · assistent d'importació de SQL Developer" entrega="p8_6.sql + notas_0484_dam.csv" >}}

#### Context

El professor de Bases de dades de DAM lliura les notes finals en un CSV. Algunes matrícules ja tenien nota (cal actualitzar-la si ha canviat) i s'ha incorporat una alumna nova que no estava matriculada.

#### Enunciat

1. Crea el fitxer `notas_0484_dam.csv` amb este contingut:

    ```text
    NIA,NOTA
    10450037,5.25
    10450074,5
    10450111,8
    10450148,7
    10452001,6.5
    ```

2. Crea la taula de càrrega `carga_notas_0484 (nia CHAR(8), nota NUMBER(4,2))` i **importa-la** amb l'assistent de SQL Developer (clic dret → *Importar dades*).
3. Escriu un `MERGE` que, per a cada fila del CSV, actualitze la nota de la matrícula del curs 2025-26 en el mòdul 0484 de DAM **només si és distinta**.
4. Per al NIA 10452001, que no té matrícula de 2025-26, el `MERGE` no ha de fer res: escriu una consulta que ho detecte com a **incidència**.
5. Executa el `MERGE` dues voltes. Quantes files es fusionen cada vegada?

#### Comprovació

- [ ] La primera execució fusiona **3** files (la de 10450111 ja tenia un 8) i la segona, **0**.
- [ ] La consulta d'incidències torna el NIA 10452001.

{{% details title="Pista: el MERGE" %}}
```sql
MERGE INTO matricula m
USING (SELECT c.nota, mt.id_matricula
       FROM   carga_notas_0484 c
              JOIN alumno a     ON a.nia = c.nia
              JOIN matricula mt ON mt.id_alumno = a.id_alumno
              JOIN modulo mo    ON mo.id_modulo = mt.id_modulo
       WHERE  mo.codigo = '0484' AND mo.cod_ciclo = 'DAM' AND mt.curso_academico = '2025-26') o
ON (m.id_matricula = o.id_matricula)
WHEN MATCHED THEN UPDATE SET m.nota_final = o.nota
                  WHERE m.nota_final IS NULL OR m.nota_final <> o.nota;
```
{{% /details %}}

---

## Pràctica 8.7 · Repte: guió de promoció de curs

{{< practica num="8.7" tipo="Reto" duracion="3 sessions" nivel="3" ra="RA4: d, e, f, h" sgbd="Oracle 26ai · SQLcl" entrega="promocion_2026_27.sql + eixida (SPOOL) + defensa oral" >}}

#### Objectiu

Dissenyar un guió transaccional que realitze una tasca complexa de forma segura, verificable i repetible.

#### Context

Ha acabat el curs 2025-26 i cap d'estudis ha de preparar el curs 2026-27 per a l'alumnat de **primer curs**. Les regles són:

1. **Promociona** a segon l'alumnat de primer amb **com a màxim un** mòdul pendent. Un mòdul està pendent si la seua nota de 2025-26 és menor que 5 o està sense qualificar.
2. A l'alumnat que promociona se li canvia el grup al de segon del seu cicle (1DAM → 2DAM...) i se'l matricula en **tots** els mòduls de segon del seu cicle, en primera convocatòria.
3. **Tot** l'alumnat de primer (promocione o no) es matricula en 2026-27 dels seus mòduls **pendents**, amb la convocatòria següent a la que tenia.
4. Data de matrícula: 10 de setembre de 2026.

#### Enunciat

Escriu `promocion_2026_27.sql` amb esta estructura:

```sql
WHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK
SPOOL promocion_2026_27.log

-- 0. Comprovacions prèvies (no modifiquen res)
--    · Ja existixen matrícules de 2026-27? Si existixen, el guió no s'ha d'executar.
--    · Llistat de l'alumnat que promociona i del que no.

-- 1. Matrícules de mòduls pendents (regla 3)
-- 2. Matrícules de segon curs (regla 2) — abans de canviar el grup!
-- 3. Canvi de grup (regla 2)

-- 4. Verificacions: recomptes esperats
-- 5. COMMIT
SPOOL OFF
```

#### Comprovació

Amb les dades originals d'EduGest, el teu guió ha d'obtindre exactament:

| Comprovació | Valor esperat |
|---|---|
| Alumnat de primer que promociona | 12 (4 de 1DAM, 4 de 1DAW, 4 de 1ASIR) |
| Matrícules de pendents inserides | 18 |
| Matrícules de segon inserides | 36 (20 de DAM i 16 de DAW) |
| Files d'`ALUMNO` amb el grup canviat | 12 |
| Total de matrícules de 2026-27 | 54 |
| Alumnat per grup després del guió | 1ASIR 1 · 1DAM 3 · 1DAW 2 · 2ASIR 4 · 2DAM 10 · 2DAW 9 · sense grup 3 |

- [ ] Executar el guió **per segona vegada** no canvia res (s'atura en les comprovacions prèvies).
- [ ] Si provoques un error a mitat (per exemple, canviant el nom d'una taula), **no** queda cap canvi aplicat.
- [ ] Expliques per què l'alumnat de 1ASIR que promociona no rep matrícules de segon (pista: consulta quins mòduls d'ASIR existixen) i què hauria de fer el centre.

{{% details title="Pista: l'ordre importa" %}}
Si canvies el grup **abans** d'inserir les matrícules, ja no sabràs qui estava en primer ni podràs distingir l'alumnat que promociona del que ja estava en segon. Una altra opció professional és calcular primer la llista d'alumnes que promocionen i guardar-la en una **taula temporal global** (`CREATE GLOBAL TEMPORARY TABLE ... ON COMMIT PRESERVE ROWS`) creada **fora** del guió.
{{% /details %}}

{{% details title="Pista: aturar el guió si ja es va executar" %}}
```sql
DECLARE
    v_n NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_n FROM matricula WHERE curso_academico = '2026-27';
    IF v_n > 0 THEN
        RAISE_APPLICATION_ERROR(-20100, 'Ya existen ' || v_n || ' matrículas de 2026-27');
    END IF;
END;
/
```
Amb `WHENEVER SQLERROR EXIT`, l'error acaba el guió.
{{% /details %}}

---

## Projecte EduGest · UD08: guions de manteniment

{{< practica num="EduGest-8" tipo="Proyecto" duracion="Treball transversal (1 setmana)" nivel="3" ra="RA4: a-h" sgbd="Oracle 26ai · SQLcl" entrega="edugest/08_mantenimiento/*.sql + docs/08-transacciones.md" >}}

#### Enunciat

1. **Dades de 2026-27.** Executa el teu guió de promoció (pràctica 8.7) i afig un guió `alta_nuevo_alumnado.sql` que done d'alta **deu** alumnes nous de primer amb les seues matrícules, en una sola transacció.
2. **Baixa lògica.** Afig a `ALUMNO` una columna `fecha_baja` i escriu el guió que dona de baixa un alumne **sense esborrar** el seu expedient. Modifica les vistes de la UD05 perquè no mostren l'alumnat donat de baixa.
3. **Política de concurrència.** En `08-transacciones.md`, decidix i justifica l'estratègia de bloqueig (pessimista o optimista) per a tres operacions de l'aplicació: posar notes, matricular i registrar faltes.
4. **Integritat.** Revisa el teu catàleg de restriccions (UD03-UD05): alguna pot implementar-se amb una restricció diferida o amb un guió transaccional? Documenta què queda per a la UD09.

#### Comprovació

{{% comprobacion %}}
- [ ] Tots els guions són transaccionals: un error deixa la base de dades com estava.
- [ ] Cap guió conté DDL entre sentències DML de la mateixa transacció.
- [ ] L'estratègia de concurrència està justificada amb arguments de la pràctica 8.5.
{{% /comprobacion %}}
