---
title: "Programació amb PL/SQL - Pràctiques"
weight: 2
bookToc: true
---

# UD09 · Pràctiques

{{< ra "RA5:a,b,c,d,e,f,g,h,i,j" "RA4:d,h" "RA6:h" >}}

| Pràctica | Tipus | Nivell | CE principals |
|---|---|---|---|
| [9.1 Primers blocs: l'expedient d'un alumne](#pràctica-91--primers-blocs-lexpedient-dun-alumne) | Guiada | ●○○ | RA5.b, RA5.c, RA5.e, RA5.g |
| [9.2 Biblioteca de funcions d'EduGest](#pràctica-92--biblioteca-de-funcions-dedugest) | Guiada | ●●○ | RA5.e, RA5.f |
| [9.3 Procediment de matrícula amb excepcions](#pràctica-93--procediment-de-matrícula-amb-excepcions) | Guiada | ●●○ | RA5.f, RA5.g, RA5.j |
| [9.4 Cursors: butlletins i informes](#pràctica-94--cursors-butlletins-i-informes) | Autònoma | ●●○ | RA5.g, RA5.i |
| [9.5 Disparadors d'integritat i auditoria](#pràctica-95--disparadors-dintegritat-i-auditoria) | Guiada | ●●● | RA5.h, RA6.h, RA4.h |
| [9.6 Repte: la taula mutant](#pràctica-96--repte-la-taula-mutant) | Repte | ●●● | RA5.h, RA5.i |
| [9.7 Tasques programades](#pràctica-97--tasques-programades) | Guiada | ●●○ | RA5.a, RA5.d, RA5.h |
| [9.8 Repte: el paquet de secretaria](#pràctica-98--repte-el-paquet-de-secretaria) | Repte | ●●● | RA5.d, RA5.f, RA5.j, RA4.d |
| [Projecte EduGest · UD09](#projecte-edugest--ud09-lògica-en-el-servidor) | Projecte | ●●● | RA5 complet, RA6.h |

> [!IMPORTANT]
> - Treballa com a `EDUGEST` sobre les dades originals (scripts 01 i 02).
> - Activa l'eixida en cada sessió: `SET SERVEROUTPUT ON` (en SQL Developer, també *Veure → Eixida de DBMS* i el botó **+** per a la connexió).
> - Guarda **cada** subprograma en el seu propi fitxer `.sql` acabat en `/`. Així podràs recompilar-lo i versionar-lo.

---

## Pràctica 9.1 · Primers blocs: l'expedient d'un alumne

{{< practica num="9.1" tipo="Guiada" duracion="2 sessions" nivel="1" ra="RA5: b, c, e, g" sgbd="Oracle 26ai · SQL Developer i SQLcl" entrega="p9_1.sql + eixida" >}}

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

## Pràctica 9.2 · Biblioteca de funcions d'EduGest

{{< practica num="9.2" tipo="Guiada" duracion="2 sessions" nivel="2" ra="RA5: e, f" sgbd="Oracle 26ai" entrega="funcions/*.sql + proves" >}}

#### Objectiu

Crear funcions d'usuari reutilitzables i usar-les tant en PL/SQL com en consultes SQL.

#### Desenvolupament

Crea estes funcions (les dues primeres estan en la [teoria](/ud09-plsql/ud09-teoria#8-funcions-dusuari)):

| Funció | Paràmetres | Torna |
|---|---|---|
| `fn_calificacion` | nota | `'NC'`, `'Insuficiente'`... `'Sobresaliente'` |
| `fn_edad` | data de naixement, data de referència (per defecte `SYSDATE`) | Anys complits |
| `fn_media_alumno` | id de l'alumne, curs acadèmic (per defecte `'2025-26'`) | Nota mitjana amb 2 decimals, o `NULL` si no té notes |
| `fn_horas_falta` | id de l'alumne, només no justificades (`'S'`/`'N'`, per defecte `'N'`) | Total d'hores de falta (0 si no en té) |
| `fn_nombre_completo` | id de l'alumne | `'Apellidos, Nombre'` o `NULL` si no existix (sense llançar error) |

{{< solucion id="ud09-001" title="Solució de fn_media_alumno y fn_nombre_completo" />}}

#### Comprovació

Executa esta consulta. El resultat ha de coincidir:

```sql
SELECT id_alumno, fn_nombre_completo(id_alumno) AS alumno,
       fn_media_alumno(id_alumno) AS media,
       fn_calificacion(fn_media_alumno(id_alumno)) AS calificacion,
       fn_horas_falta(id_alumno, 'N') + fn_horas_falta(id_alumno, 'S') AS horas_falta
FROM   alumno
WHERE  cod_grupo = '2DAW'
ORDER  BY id_alumno;
```

| ID_ALUMNO | ALUMNO | MEDIA | CALIFICACION | HORAS_FALTA |
|---|---|---|---|---|
| 20 | Sala Brotons, Mateo | 7.13 | Notable | 5 |
| 21 | Carbonell Soriano, Elena | 5.44 | Suficiente | 1 |
| 22 | Planelles Marco, Sofía | 5.56 | Suficiente | 4 |
| 23 | Amorós Guillem, Sara | 5.42 | Suficiente | 3 |
| 24 | Verdú Castelló, Nicolás | 6 | Bien | 0 |

- [ ] `SELECT fn_nombre_completo(999) FROM dual;` torna `NULL` sense error.
- [ ] `SELECT fn_media_alumno(30) FROM dual;` torna `NULL` (alumne sense matrícules).
- [ ] `SELECT object_name, status FROM user_objects WHERE object_type = 'FUNCTION';` mostra les cinc funcions `VALID`.

#### Ampliació

Què passa si intentes usar en un `SELECT` una funció que fa un `INSERT`? Prova-ho i anota l'error (`ORA-14551`). Per què Oracle ho impedix?

---

## Pràctica 9.3 · Procediment de matrícula amb excepcions

{{< practica num="9.3" tipo="Guiada" duracion="2 sessions" nivel="2" ra="RA5: f, g, j" sgbd="Oracle 26ai" entrega="pr_matricular.sql + bateria de proves" >}}

#### Objectiu

Implementar un procediment emmagatzemat que valida regles de negoci i comunica els errors de forma controlada.

#### Desenvolupament

{{% steps %}}

1. **Crea `pr_matricular`** tal com apareix en la [teoria](/ud09-plsql/ud09-teoria#105-exemple-complet-procediment-de-matrícula).

2. **Executa la bateria de proves.** Cada prova indica el resultat esperat:

    | # | Crida | Resultat esperat |
    |---|---|---|
    | P1 | `pr_matricular(1, 2, '2026-27')` | Correcte. Convocatòria 2 |
    | P2 | La mateixa crida una altra vegada | `ORA-20013`: ja està matriculat |
    | P3 | `pr_matricular(1, 12, '2026-27')` | `ORA-20010`: el mòdul és de DAW |
    | P4 | `pr_matricular(30, 2, '2026-27')` | `ORA-20012`: alumne sense grup |
    | P5 | `pr_matricular(999, 2, '2026-27')` | `ORA-20012` |
    | P6 | `pr_matricular(1, 999, '2026-27')` | `ORA-20012` |
    | P7 | `pr_matricular(1, 3, '2026/27')` | `ORA-02290` (`CK_MATRICULA_CURSO`): ho detecta la restricció, no el procediment |
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
- [ ] Pots explicar per què el procediment no fa `COMMIT`.

{{% details title="Per què P8 falla en la quarta crida?" %}}
L'alumne 1 ja tenia una matrícula del mòdul 4 en 2025-26 (convocatòria 1). El procediment calcula la convocatòria com `MAX(convocatoria) + 1`, així que les crides per a 2026-27, 2027-28 i 2028-29 creen les convocatòries 2, 3 i 4. La cinquena convocatòria no està permesa.
{{% /details %}}
{{% /comprobacion %}}

#### Ampliació

Afig un paràmetre `p_forzar BOOLEAN DEFAULT FALSE` que permeta saltar-se la regla del cicle (matrícula autoritzada per direcció). Es pot cridar a este procediment des de SQL\*Plus amb un `BOOLEAN`? I des d'Oracle 23ai?

---

## Pràctica 9.4 · Cursors: butlletins i informes

{{< practica num="9.4" tipo="Autónoma" duracion="2 sessions" nivel="2" ra="RA5: g, i" sgbd="Oracle 26ai" entrega="pr_boletin.sql + pr_alerta_faltas.sql + eixides" >}}

#### Enunciat

**1. Butlletí de notes.** Crea `pr_boletin(p_id_alumno)` que mostre el butlletí d'un alumne usant un **cursor explícit** sobre les seues matrícules. Per a l'alumne 20 l'eixida ha de ser:

```text
BOLETÍN DE NOTAS · Curso 2025-26
Alumno: Sala Brotons, Mateo (2DAW)
-------------------------------------------------------------
0612 Desarrollo web en entorno cliente              6.50  Bien
0613 Desarrollo web en entorno servidor             5.25  Suficiente
0614 Despliegue de aplicaciones web                 7.50  Notable
0615 Diseño de interfaces web                       9.25  Sobresaliente
-------------------------------------------------------------
Módulos: 4 · Aprobados: 4 · Media: 7.13
```

Pistes: `RPAD(nombre, 45)` alinea columnes; `TO_CHAR(nota, '90.00')` formata la nota; usa `fn_calificacion` i `fn_media_alumno` de la pràctica 9.2; compta els aprovats dins del bucle.

**2. Butlletins d'un grup.** Crea `pr_boletines_grupo(p_cod_grupo)` que recorrega l'alumnat del grup amb un **cursor `FOR`** i cride a `pr_boletin` per a cadascun.

**3. Alerta de faltes.** Crea `pr_alerta_faltas(p_umbral NUMBER DEFAULT 4)` que, amb un **cursor amb paràmetres**, mostre l'alumnat les hores de falta **no justificades** del qual siguen iguals o superiors al llindar, i que acabe indicant quants alumnes ha trobat.

#### Comprovació

{{% comprobacion %}}
- [ ] `EXEC pr_alerta_faltas(5);` troba 2 alumnes: Martina Alemany Vidal (6) i Valeria Quiles Marco (5).
- [ ] `EXEC pr_alerta_faltas;` (llindar per defecte, 4) troba 5 alumnes.
- [ ] `EXEC pr_boletines_grupo('2ASIR');` no dona error i mostra que el grup no té alumnat.
- [ ] El cursor explícit es tanca també si es produïx un error (secció `EXCEPTION` que comprova `%ISOPEN`).
{{% /comprobacion %}}

---

## Pràctica 9.5 · Disparadors d'integritat i auditoria

{{< practica num="9.5" tipo="Guiada" duracion="3 sessions" nivel="3" ra="RA5: h · RA6: h · RA4: h" sgbd="Oracle 26ai" entrega="triggers/*.sql + matriu de proves" >}}

#### Objectiu

Implementar amb disparadors l'auditoria de canvis i les restriccions d'EduGest que no van poder declarar-se en el model lògic (catàleg de la UD03).

#### Desenvolupament

{{% steps %}}

1. **Auditoria de notes.** Crea la taula `AUDITORIA_NOTA` i el disparador `trg_auditoria_nota` de la [teoria](/ud09-plsql/ud09-teoria#112-auditoria-de-canvis-de-nota). Amplia'l per a registrar també la **IP** de la sessió (`SYS_CONTEXT('USERENV', 'IP_ADDRESS')`) i el **tipus d'operació** (`'U'` en canvis de nota; afig l'esdeveniment `DELETE` i registra `'D'`).

2. **R1 · El cap pertany al departament** (els dos costats de la regla):

    - `trg_jefe_departamento` sobre `DEPARTAMENTO` (teoria, apartat 11.3).
    - `trg_profesor_cambio_dpto` sobre `PROFESOR`: impedix canviar de departament un professor que és cap del seu departament actual.

    ```sql
    CREATE OR REPLACE TRIGGER trg_profesor_cambio_dpto
    BEFORE UPDATE OF id_departamento ON profesor
    FOR EACH ROW
    WHEN (NEW.id_departamento <> OLD.id_departamento)
    DECLARE
        v_n NUMBER;
    BEGIN
        SELECT COUNT(*) INTO v_n FROM departamento
        WHERE  id_jefe = :OLD.id_profesor AND id_departamento = :OLD.id_departamento;
        IF v_n > 0 THEN
            RAISE_APPLICATION_ERROR(-20021,
                'El profesor ' || :OLD.id_profesor || ' es jefe de su departamento: asigna antes otra jefatura');
        END IF;
    END;
    /
    ```

3. **R3 · No hi ha faltes anteriors a la matrícula.** Escriu `trg_falta_fecha` (`BEFORE INSERT OR UPDATE OF fecha ON falta_asistencia`) que consulte la `fecha_matricula` i rebutge la falta amb `-20022` si és anterior.

4. **Normalització de dades.** Crea `trg_alumno_normaliza` (teoria, apartat 11.4).

5. **Executa la matriu de proves** i anota el resultat:

    | # | Sentència | Resultat esperat |
    |---|---|---|
    | T1 | `UPDATE matricula SET nota_final = 6 WHERE id_matricula = 10002;` | 1 fila; 1 registre en `AUDITORIA_NOTA` (4.75 → 6) |
    | T2 | `UPDATE matricula SET nota_final = 6 WHERE id_matricula = 10002;` (una altra vegada) | 1 fila; **cap** registre nou (no canvia el valor) |
    | T3 | `UPDATE departamento SET id_jefe = 111 WHERE id_departamento = 1;` | `ORA-20020` |
    | T4 | `UPDATE departamento SET id_jefe = 102 WHERE id_departamento = 1;` | Correcte |
    | T5 | `UPDATE profesor SET id_departamento = 2 WHERE id_profesor = 102;` | `ORA-20021` (després de T4, 102 és cap) |
    | T6 | `UPDATE profesor SET id_departamento = 2 WHERE id_profesor = 108;` | Correcte (108 no és cap) |
    | T7 | `INSERT INTO falta_asistencia (id_matricula, fecha, horas) VALUES (10001, DATE '2025-08-01', 2);` | `ORA-20022` |
    | T8 | `INSERT INTO alumno (nia, nombre, apellidos, fecha_nacimiento, email) VALUES ('10459999', '  marina ', 'lópez ortega', DATE '2007-01-01', ' Marina@Mail.COM ');` | Es guarda «Marina», «López Ortega», «marina@mail.com» |
    | T9 | `UPDATE matricula SET nota_final = nota_final WHERE id_alumno = 2;` | 5 files; cap registre d'auditoria |

6. Acaba amb `ROLLBACK` i comprova que l'auditoria també s'ha desfet. Per què? Com aconseguiries que el registre d'auditoria es conserve encara que la transacció es desfaça? (Pista: `PRAGMA AUTONOMOUS_TRANSACTION`.)

{{% /steps %}}

#### Comprovació

{{% comprobacion %}}
- [ ] La matriu completa coincidix amb l'esperat.
- [ ] `SELECT trigger_name, status FROM user_triggers;` mostra tots els disparadors `ENABLED`.
- [ ] Cada disparador té un comentari que cita la restricció del catàleg (R1, R3...) que implementa.

> [!WARNING]
> Si en carregar de nou les dades amb l'script 02 apareixen errors `ORA-200xx`, és que els teus disparadors rebutgen alguna dada d'exemple o l'ordre de càrrega. Desactiva'ls abans d'una càrrega massiva (`ALTER TABLE ... DISABLE ALL TRIGGERS`) i activa'ls després… **comprovant** després les dades amb una consulta.
{{% /comprobacion %}}

---

## Pràctica 9.6 · Repte: la taula mutant

{{< practica num="9.6" tipo="Reto" duracion="2 sessions" nivel="3" ra="RA5: h, i" sgbd="Oracle 26ai" entrega="trg_imparte_max_horas.sql + proves + explicació" >}}

#### Enunciat

Cal implementar la restricció R4: «un professor no pot superar 20 hores lectives setmanals en un curs acadèmic».

1. Escriu primer un disparador **de fila** `AFTER INSERT OR UPDATE ON imparte FOR EACH ROW` que sume les hores del professor en `IMPARTE`. Executa `UPDATE imparte SET horas_semanales = horas_semanales + 1 WHERE id_profesor = 102;` i anota l'error.
2. Explica per què es produïx `ORA-04091`.
3. Substituïx-lo per un **disparador compost** que funcione per a **qualsevol** curs acadèmic: guarda en una col·lecció les parelles (professor, curs) modificades i comprova-les en `AFTER STATEMENT`.
4. Proves:
    - `UPDATE imparte SET horas_semanales = horas_semanales + 1 WHERE id_profesor = 102;` → correcte (Javier passa de 16 a 20 hores).
    - Repetix la sentència → `ORA-20030` (24 hores: la sentència suma 1 hora a cadascuna de les seues 4 assignacions).
    - `INSERT` d'una assignació de 6 hores a Marta (101, 15 hores) en el curs 2026-27 → correcte (és un altre curs).
5. Què passaria amb dues sessions que, alhora, afigen hores al mateix professor sense confirmar? Garantix el disparador la regla en eixe cas? Relaciona-ho amb la UD08 i proposa una solució.

{{% details title="Pista per a l'apartat 5" %}}
Cada sessió veu només els seus propis canvis sense confirmar (consistència de lectura). Les dues poden sumar 19 hores i confirmar, deixant 22. Una solució és serialitzar les modificacions de cada professor bloquejant la seua fila en `PROFESOR` amb `SELECT ... FOR UPDATE` dins del disparador, abans de sumar.
{{% /details %}}

---

## Pràctica 9.7 · Tasques programades

{{< practica num="9.7" tipo="Guiada" duracion="1 sessió" nivel="2" ra="RA5: a, d, h" sgbd="Oracle 26ai · DBMS_SCHEDULER" entrega="jobs.sql + captura de l'historial" >}}

#### Objectiu

Automatitzar tasques periòdiques en el servidor i comprovar-ne l'execució.

#### Desenvolupament

{{% steps %}}

1. Crea la taula `RESUMEN_GRUPO` i el procediment `pr_recalcular_resumen` de la [teoria](/ud09-plsql/ud09-teoria#12-eventos-tareas-programadas).
2. Crea una taula `LOG_TAREA(momento TIMESTAMP, tarea VARCHAR2(50), mensaje VARCHAR2(200))` i modifica el procediment perquè escriga una fila en acabar, amb el nombre de grups processats.
3. Crea la tasca `JOB_RESUMEN_PRUEBA` que s'execute **cada minut** (`FREQ=MINUTELY; INTERVAL=1`).
4. Espera tres minuts i comprova:

    ```sql
    SELECT * FROM log_tarea ORDER BY momento;
    SELECT log_date, status FROM user_scheduler_job_run_details
    WHERE  job_name = 'JOB_RESUMEN_PRUEBA' ORDER BY log_date;
    ```

5. Provoca un error (per exemple, canvia el nom de la taula `RESUMEN_GRUPO`) i observa l'estat `FAILED` i el codi d'error en l'historial. Restaura la taula.
6. Canvia el calendari a «de dilluns a divendres a les 7:30» amb `DBMS_SCHEDULER.SET_ATTRIBUTE` i desactiva la tasca.

{{% /steps %}}

#### Comprovació

{{% comprobacion %}}
- [ ] `LOG_TAREA` té una fila per minut mentre la tasca està activa.
- [ ] L'historial mostra almenys una execució `SUCCEEDED` i una `FAILED`.
- [ ] El calendari final és `FREQ=WEEKLY; BYDAY=MON,TUE,WED,THU,FRI; BYHOUR=7; BYMINUTE=30`.

> [!TIP]
> Les tasques que no faces desaparéixer continuen executant-se al teu contenidor. En acabar: `EXEC DBMS_SCHEDULER.DROP_JOB('JOB_RESUMEN_PRUEBA');`
{{% /comprobacion %}}

---

## Pràctica 9.8 · Repte: el paquet de secretaria

{{< practica num="9.8" tipo="Reto" duracion="3 sessions" nivel="3" ra="RA5: d, f, j · RA4: d" sgbd="Oracle 26ai" entrega="pkg_secretaria.sql (especificació i cos) + proves + defensa" >}}

#### Enunciat

Agrupa la lògica de secretaria en un **paquet** `pkg_secretaria`:

```sql
CREATE OR REPLACE PACKAGE pkg_secretaria AS
    c_curso_actual CONSTANT matricula.curso_academico%TYPE := '2026-27';

    PROCEDURE matricular (p_id_alumno NUMBER, p_id_modulo NUMBER);
    PROCEDURE matricular_curso_completo (p_id_alumno NUMBER);
    PROCEDURE promocionar (p_curso_origen VARCHAR2, p_curso_destino VARCHAR2,
                           p_promocionados OUT NUMBER, p_pendientes OUT NUMBER);
    FUNCTION  media (p_id_alumno NUMBER, p_curso VARCHAR2 DEFAULT NULL) RETURN NUMBER;
END pkg_secretaria;
/
```

1. `matricular` reutilitza la lògica de la pràctica 9.3.
2. `matricular_curso_completo` matricula l'alumne en tots els mòduls del curs del seu grup cridant a `matricular`. Si alguna matrícula falla, **no** n'ha de quedar cap (usa un `SAVEPOINT`).
3. `promocionar` implementa el guió de promoció de la pràctica 8.7 com a procediment, torna els recomptes en paràmetres `OUT` i llança un error propi si ja existixen matrícules del curs destinació.
4. Escriu un bloc de prova que execute `promocionar('2025-26', '2026-27', ...)`, mostre els recomptes i faça `ROLLBACK`.

#### Comprovació

{{% comprobacion %}}
- [ ] La promoció torna 12 alumnes promoguts i 18 matrícules de pendents, igual que el guió de la UD08.
- [ ] Una segona crida llança l'error propi.
- [ ] El cos del paquet no té `COMMIT`.
{{% /comprobacion %}}

---

## Projecte EduGest · UD09: lògica en el servidor

{{< practica num="EduGest-9" tipo="Proyecto" duracion="Treball transversal (2 setmanes)" nivel="3" ra="RA5: a-j · RA6: h · RA4: h" sgbd="Oracle 26ai" entrega="edugest/09_plsql/ + docs/09-programacion.md" >}}

#### Enunciat

1. **Catàleg de restriccions tancat.** Implementa amb disparadors o procediments **totes** les restriccions del teu catàleg (UD03-UD05) que queden pendents. Per a cadascuna, una prova que demostre que funciona.
2. **Auditoria.** Audita els canvis de nota i les baixes d'alumnat. L'auditoria s'ha de conservar encara que la transacció es desfaça.
3. **API de secretaria.** Paquet `pkg_secretaria` (pràctica 9.8) i concessió d'`EXECUTE` sobre ell al rol de secretaria. Retira a eixe rol els privilegis `INSERT` directes sobre `MATRICULA`: ara només podrà matricular **a través del procediment**. Explica quin avantatge de seguretat té.
4. **Tasca nocturna** que recalcula el resum per grup i registra la seua execució.
5. **Documentació**: taula amb cada objecte PL/SQL, la seua finalitat, els seus paràmetres i els errors propis que pot llançar (codi i missatge).

#### Comprovació

{{% comprobacion %}}
- [ ] Tots els objectes estan `VALID` en `USER_OBJECTS`.
- [ ] L'usuari de secretaria pot matricular amb `EXEC edugest.pkg_secretaria.matricular(...)` però no amb un `INSERT` directe.
- [ ] Cada restricció del catàleg té la seua prova.
{{% /comprobacion %}}
