---
title: "Pràctiques · Modificació de dades i transaccions"
weight: 11
bookToc: true
---

# Tema 5 · Pràctiques: modificació de dades i transaccions
{{< ra "RA2:g" "RA5:a,b,c,d,f,g,h" >}}

| Pràctica | Tipus | Nivell | CE principals |
|---|---|---|---|
| [5.1 Altes, canvis i baixes a EduGest](#pràctica-51--altes-canvis-i-baixes-a-edugest) | Guiada | ●○○ | RA5.a, RA5.b |
| [5.2 Còpies, històrics i INSERT … SELECT](#pràctica-52--còpies-històrics-i-insert--select) | Guiada | ●●○ | RA5.c |
| [5.3 Laboratori de transaccions](#pràctica-53--laboratori-de-transaccions) | Guiada | ●●○ | RA5.f, RA5.g |
| [5.4 Dues sessions, una dada: concurrència i bloquejos](#pràctica-54--dues-sessions-una-dada-concurrència-i-bloquejos) | Guiada | ●●● | RA5.d, RA5.h |
| [Projecte EduGest · Tema 5](#projecte-edugest--tema-5-modificació-de-dades) | Projecte | ●●● | RA5 complet |

> [!IMPORTANT]
> Abans de **cada** pràctica, restaura EduGest executant els scripts 01 i 02 del [projecte](/guia/proyecto-edugest#4-scripts-descarregables). Els números de files afectades que s'indiquen suposen les dades originals.

---

## Pràctica 5.1 · Altes, canvis i baixes a EduGest

{{< practica num="5.1" tipo="Guiada" duracion="2 sessions" nivel="1" ra="RA5: a, b" sgbd="Oracle 26ai · SQL Developer" entrega="p8_1.sql + captures de la reixeta" >}}

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
> - Si la segona sessió **es queda penjada** en el pas 5 o 6, és que intenta modificar una fila bloquejada per la primera sessió, que encara no ha fet `COMMIT`. Ho estudiaràs en la pràctica 5.4.
> - Tancar SQL Developer amb canvis pendents mostra un avís per a confirmar-los o desfer-los. **Llig l'avís.**

---

## Pràctica 5.2 · Còpies, històrics i INSERT … SELECT

{{< practica num="5.2" tipo="Guiada" duracion="1 sessió" nivel="2" ra="RA5: c" sgbd="Oracle 26ai · EDUGEST" entrega="p8_2.sql" >}}

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

---

## Pràctica 5.3 · Laboratori de transaccions

{{< practica num="5.3" tipo="Guiada" duracion="1 sessió" nivel="2" ra="RA5: f, g" sgbd="Oracle 26ai" entrega="p8_4.sql + taula de resultats" >}}

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

{{< solucion id="tema5-002" title="Resultats esperats" />}}

#### Comprovació

{{% comprobacion %}}
- [ ] Has predit correctament almenys 5 dels 6 experiments. Si no, explica en què t'has equivocat.
- [ ] Pots explicar amb les teues paraules l'**atomicitat de sentència** (experiment 4) i per què és perillosa si l'aplicació confirma sense comprovar els errors.
{{% /comprobacion %}}

---

## Pràctica 5.4 · Dues sessions, una dada: concurrència i bloquejos

{{< practica num="5.4" tipo="Guiada" duracion="2 sessions" nivel="3" ra="RA5: d, h" sgbd="Oracle 26ai · dues sessions simultànies (dos fulls amb sessió pròpia o dos terminals SQLcl) + SYSTEM" entrega="Cronogrames completats + captures" >}}

#### Objectiu

Observar en directe els efectes de les distintes polítiques de bloqueig i dels nivells d'aïllament.

#### Preparació

Usa la taula `CUENTA` de la pràctica 5.3 restaurada a A = 1000, B = 200, C = 50. Obri **dues sessions** com a `EDUGEST`: **S1** i **S2**. En SQL Developer, obri el segon full amb *Full de treball SQL no compartit* (`Ctrl+Mayús+N`); si no, els dos fulls compartixen sessió i no veuràs res.

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

## Projecte EduGest · Tema 5: modificació de dades

{{< practica num="EduGest-5" tipo="Proyecto" duracion="Treball transversal (1 setmana)" nivel="3" ra="RA5: a, b, c, d, f, g, h" sgbd="Oracle 26ai · SQLcl" entrega="edugest/08_modificaciones/*.sql + docs/08-transacciones.md" >}}

#### Enunciat

1. **Alta d'alumnat nou.** Escriu un guió `alta_nuevo_alumnado.sql` que done d'alta **deu** alumnes nous de primer amb les seues matrícules, en una sola transacció.
2. **Baixa lògica.** Afig a `ALUMNO` una columna `fecha_baja` i escriu el guió que dona de baixa un alumne **sense esborrar** el seu expedient.
3. **Política de concurrència.** En `08-transacciones.md`, decidix i justifica l'estratègia de bloqueig (pessimista o optimista) per a tres operacions de l'aplicació: posar notes, matricular i registrar faltes.
4. **Integritat.** Revisa el teu catàleg de restriccions (Tema 2-Tema 3): alguna pot implementar-se amb una restricció diferida o amb un guió transaccional? Documenta les que queden sense implementar (RA2.i).

#### Comprovació

{{% comprobacion %}}
- [ ] Tots els guions són transaccionals: un error deixa la base de dades com estava.
- [ ] Cap guió conté DDL entre sentències DML de la mateixa transacció.
- [ ] L'estratègia de concurrència està justificada amb arguments de la pràctica 5.4.
{{% /comprobacion %}}
