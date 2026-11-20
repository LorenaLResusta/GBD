---
title: "Pràctiques · Guions de sentències"
weight: 21
bookToc: true
---

# Tema 5 · Pràctiques: guions de sentències
{{< ra "RA5:d,e" >}}

| Pràctica | Tipus | Nivell | CE principals |
|---|---|---|---|
| [5.5 Primers blocs: l'expedient d'un alumne](#pràctica-55--primers-blocs-lexpedient-dun-alumne) | Guiada | ●○○ | RA5.e |
| [5.6 Matrícula amb excepcions](#pràctica-56--matrícula-amb-excepcions) | Guiada | ●●○ | RA5.e |
| [Projecte EduGest · Tema 5](#projecte-edugest--tema-5-guions-de-manteniment) | Projecte | ●●● | RA5.d, RA5.e |

> [!IMPORTANT]
> - Treballa com a `EDUGEST` sobre les dades originals (scripts 01 i 02).
> - Activa l'eixida en cada sessió: `SET SERVEROUTPUT ON` (en SQL Developer, també *Veure → Eixida de DBMS* i el botó **+** per a la connexió).
> - Guarda **cada** guió en el seu propi fitxer `.sql`: així el pots repetir i versionar.

---

## Pràctica 5.5 · Primers blocs: l'expedient d'un alumne

{{< practica num="5.5" tipo="Guiada" duracion="2 sessions" nivel="1" ra="RA5: e" sgbd="Oracle 26ai · SQL Developer i SQLcl" entrega="p9_1.sql + eixida" >}}

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

## Pràctica 5.6 · Matrícula amb excepcions

{{< practica num="5.6" tipo="Guiada" duracion="2 sessions" nivel="2" ra="RA5: e" sgbd="Oracle 26ai" entrega="matricula_bloque.sql + bateria de proves" >}}

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

---

## Projecte EduGest · Tema 5: guions de manteniment

{{< practica num="EduGest-5" tipo="Proyecto" duracion="Treball transversal (1 setmana)" nivel="3" ra="RA5: d, e" sgbd="Oracle 26ai · SQLcl" entrega="edugest/09_guiones/*.sql + docs/09-guiones.md" >}}

#### Enunciat

1. **Matrícula.** Lliura el bloc de matrícula de la pràctica 5.6 complet: comprovacions prèvies, excepcions amb missatges clars, `COMMIT` únic i `SPOOL`.
2. **Alta d'alumnat nou.** Convertix el teu `alta_nuevo_alumnado.sql` (EduGest-5) en un guió professional: capçalera, còpia prèvia, bloc amb excepcions que explique l'error, `COMMIT` únic i `SPOOL`.
3. **Documentació.** En `09-guiones.md` indica, per a cada guió, l'ordre d'execució, què comprova abans de modificar, què passa si falla a mitges i com es torna arrere.

#### Comprovació

{{% comprobacion %}}
- [ ] Els guions s'executen de principi a fi sobre EduGest restaurat amb els scripts 01 i 02.
- [ ] Executar qualsevol d'ells per segona vegada no canvia res o s'atura amb un missatge clar.
- [ ] Un error provocat a mitges no deixa cap canvi aplicat.
{{% /comprobacion %}}
