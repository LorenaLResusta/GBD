---
title: "Pràctiques · Guions de sentències"
weight: 21
bookToc: true
---

# Tema 5 · Pràctiques: guions de sentències
{{< ra "RA5:d,e" >}}

| Pràctica | Tipus | Nivell | CE principals |
|---|---|---|---|
| [5.7 Primers blocs: l'expedient d'un alumne](#pràctica-57--primers-blocs-lexpedient-dun-alumne) | Guiada | ●○○ | RA5.e |
| [5.8 Matrícula amb excepcions](#pràctica-58--matrícula-amb-excepcions) | Guiada | ●●○ | RA5.e |
| [5.9 Repte: guió de promoció de curs](#pràctica-59--repte-guió-de-promoció-de-curs) | Repte | ●●● | RA5.d-g |
| [Projecte EduGest · Tema 5](#projecte-edugest--tema-5-guions-de-manteniment) | Projecte | ●●● | RA5.d, RA5.e |

> [!IMPORTANT]
> - Treballa com a `EDUGEST` sobre les dades originals (scripts 01 i 02).
> - Activa l'eixida en cada sessió: `SET SERVEROUTPUT ON` (en SQL Developer, també *Veure → Eixida de DBMS* i el botó **+** per a la connexió).
> - Guarda **cada** guió en el seu propi fitxer `.sql`: així el pots repetir i versionar.

---

## Pràctica 5.7 · Primers blocs: l'expedient d'un alumne

{{< practica num="5.7" tipo="Guiada" duracion="2 sessions" nivel="1" ra="RA5: e" sgbd="Oracle 26ai · SQL Developer i SQLcl" entrega="p9_1.sql + eixida" >}}

#### Objectiu

Escriure i executar blocs anònims amb variables, consultes `SELECT INTO`, funcions del sistema gestor i estructures de control.

#### Desenvolupament

{{% steps %}}

1. **Bloc mínim i variables del sistema:**

    ```sql
    SET SERVEROUTPUT ON
    BEGIN
        DBMS_OUTPUT.PUT_LINE('Usuario: ' || USER);
        DBMS_OUTPUT.PUT_LINE('Fecha: '   || TO_CHAR(SYSDATE, 'DD/MM/YYYY HH24:MI'));
        DBMS_OUTPUT.PUT_LINE('Equipo cliente: ' || SYS_CONTEXT('USERENV', 'HOST'));
    END;
    /
    ```

2. **Dades d'un alumne** amb `%ROWTYPE` i una variable de substitució:

    ```sql
    DECLARE
        r_alumno  alumno%ROWTYPE;
        v_edad    NUMBER;
    BEGIN
        SELECT * INTO r_alumno FROM alumno WHERE id_alumno = &id_alumno;
        v_edad := TRUNC(MONTHS_BETWEEN(DATE '2026-10-06', r_alumno.fecha_nacimiento) / 12);

        DBMS_OUTPUT.PUT_LINE('EXPEDIENTE ' || r_alumno.nia);
        DBMS_OUTPUT.PUT_LINE(RPAD('-', 40, '-'));
        DBMS_OUTPUT.PUT_LINE('Alumno: ' || r_alumno.apellidos || ', ' || r_alumno.nombre);
        DBMS_OUTPUT.PUT_LINE('Grupo:  ' || NVL(r_alumno.cod_grupo, 'sin grupo'));
        DBMS_OUTPUT.PUT_LINE('Edad:   ' || v_edad || ' años');
    END;
    /
    ```

    SQLcl preguntarà `Enter value for id_alumno:`. Escriu **20**.

3. **Afig estadístiques** amb `SELECT INTO` de funcions d'agregat i una condició:

    ```sql
        -- (dins del bloc anterior; declara v_media NUMBER i v_horas NUMBER)
        SELECT ROUND(AVG(nota_final), 2) INTO v_media
        FROM   matricula WHERE id_alumno = r_alumno.id_alumno;

        SELECT NVL(SUM(f.horas), 0) INTO v_horas
        FROM   falta_asistencia f JOIN matricula m ON m.id_matricula = f.id_matricula
        WHERE  m.id_alumno = r_alumno.id_alumno;

        DBMS_OUTPUT.PUT_LINE('Media:  ' || NVL(TO_CHAR(v_media), 'sin notas'));
        DBMS_OUTPUT.PUT_LINE('Faltas: ' || v_horas || ' horas');

        IF v_horas >= 10 THEN
            DBMS_OUTPUT.PUT_LINE('AVISO: riesgo de pérdida de evaluación continua');
        ELSIF v_horas > 0 THEN
            DBMS_OUTPUT.PUT_LINE('Tiene faltas registradas');
        ELSE
            DBMS_OUTPUT.PUT_LINE('Sin faltas');
        END IF;
    ```

4. **Executa el guió des de SQLcl** amb `@p9_1.sql` i compara amb l'execució en SQL Developer.

{{% /steps %}}

#### Comprovació

Per a l'alumne 20 l'eixida ha de ser:

```text
EXPEDIENTE 10450740
----------------------------------------
Alumno: Sala Brotons, Mateo
Grupo:  2DAW
Edad:   23 años
Media:  7.13
Faltas: 5 horas
Tiene faltas registradas
```

- [ ] Amb l'alumne 30 (sense grup i sense matrícules) el bloc mostra «sense grup», «sense notes» i «Sense faltes».
- [ ] Amb l'alumne 999 es produïx `ORA-01403: no data found`. Afig una secció `EXCEPTION` que mostre «No existix l'alumne 999».

#### Errors habituals

| Símptoma | Causa |
|---|---|
| El bloc acaba sense mostrar res | Falta `SET SERVEROUTPUT ON` o el panell d'eixida de DBMS no està actiu |
| SQLcl es queda esperant amb un número de línia | Falta la `/` final |
| `PLS-00103: Encountered the symbol ...` | Error de sintaxi: sol ser un `;` oblidat o un `END IF` sense tancar |

---

## Pràctica 5.8 · Matrícula amb excepcions

{{< practica num="5.8" tipo="Guiada" duracion="2 sessions" nivel="2" ra="RA5: e" sgbd="Oracle 26ai" entrega="matricula_bloque.sql + bateria de proves" >}}

#### Objectiu

Escriure un bloc PL/SQL que valida regles de negoci i comunica els errors de forma controlada.

#### Desenvolupament

{{% steps %}}

1. **Guarda el bloc de matrícula** de la [teoria](/tema5-modificacion/guiones-teoria#69-exemple-complet-matrícula-validada-en-un-bloc) en `matricula_bloque.sql`.

2. **Executa la bateria de proves** canviant els `DEFINE` i tornant a executar el bloc. Cada prova indica el resultat esperat:

    | # | Dades (`DEFINE`) | Resultat esperat |
    |---|---|---|
    | P1 | alumne `1`, mòdul `2`, curs `2026-27` | Correcte. Convocatòria 2 |
    | P2 | La mateixa crida una altra vegada | `ORA-20013`: ja està matriculat |
    | P3 | alumne `1`, mòdul `12`, curs `2026-27` | `ORA-20010`: el mòdul és de DAW |
    | P4 | alumne `30`, mòdul `2`, curs `2026-27` | `ORA-20012`: alumne sense grup |
    | P5 | alumne `999`, mòdul `2`, curs `2026-27` | `ORA-20012` |
    | P6 | alumne `1`, mòdul `999`, curs `2026-27` | `ORA-20012` |
    | P7 | alumne `1`, mòdul `3`, curs `2026/27` | `ORA-02290` (`CK_MATRICULA_CURSO`): ho detecta la restricció, no el bloc |
    | P8 | Matricular l'alumne 1 en el mòdul 4 en els cursos `'2026-27'`, `'2027-28'`, `'2028-29'` i `'2029-30'` | Les tres primeres creen les convocatòries 2, 3 i 4; la quarta (convocatòria 5) dona `ORA-20011` |

3. **Comprova l'estat** després de les proves:

    ```sql
    SELECT id_modulo, curso_academico, convocatoria FROM matricula
    WHERE  id_alumno = 1 AND curso_academico <> '2025-26'
    ORDER  BY id_modulo, curso_academico;
    ROLLBACK;
    ```

{{% /steps %}}

#### Comprovació

{{% comprobacion %}}
- [ ] Les huit proves donen el resultat esperat.
- [ ] Després de les proves i abans del `ROLLBACK` hi ha 4 matrícules noves de l'alumne 1: mòdul 2 (convocatòria 2) i mòdul 4 (convocatòries 2, 3 i 4).
- [ ] Pots explicar per què el bloc no fa `COMMIT`.

{{% details title="Per què P8 falla en la quarta crida?" %}}
L'alumne 1 ja tenia una matrícula del mòdul 4 en 2025-26 (convocatòria 1). El bloc calcula la convocatòria com `MAX(convocatoria) + 1`, així que les crides per a 2026-27, 2027-28 i 2028-29 creen les convocatòries 2, 3 i 4. La cinquena convocatòria no està permesa.
{{% /details %}}
{{% /comprobacion %}}

#### Ampliació

Afig una variable `v_forzar BOOLEAN := FALSE` que permeta saltar-se la regla del cicle (matrícula autoritzada per prefectura) i comprova que, sense ella, la regla continua aplicant-se.

---


## Pràctica 5.9 · Repte: guió de promoció de curs

{{< practica num="5.9" tipo="Reto" duracion="3 sessions" nivel="3" ra="RA5: d, e, f, g" sgbd="Oracle 26ai · SQLcl" entrega="promocion_2026_27.sql + eixida (SPOOL) + defensa oral" >}}

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
## Projecte EduGest · Tema 5: guions de manteniment

{{< practica num="EduGest-5" tipo="Proyecto" duracion="Treball transversal (1 setmana)" nivel="3" ra="RA5: d, e" sgbd="Oracle 26ai · SQLcl" entrega="edugest/09_guiones/*.sql + docs/09-guiones.md" >}}

#### Enunciat

1. **Promoció de curs.** Lliura el teu `promocion_2026_27.sql` (pràctica 5.9) complet: comprovacions prèvies, transacció única, verificacions, `SPOOL` i idempotència.
2. **Alta d'alumnat nou.** Convertix el teu `alta_nuevo_alumnado.sql` (EduGest-5) en un guió professional: capçalera, còpia prèvia, bloc amb excepcions que explique l'error, `COMMIT` únic i `SPOOL`.
3. **Documentació.** En `09-guiones.md` indica, per a cada guió, l'ordre d'execució, què comprova abans de modificar, què passa si falla a mitges i com es torna arrere.

#### Comprovació

{{% comprobacion %}}
- [ ] Els guions s'executen de principi a fi sobre EduGest restaurat amb els scripts 01 i 02.
- [ ] Executar qualsevol d'ells per segona vegada no canvia res o s'atura amb un missatge clar.
- [ ] Un error provocat a mitges no deixa cap canvi aplicat.
{{% /comprobacion %}}
