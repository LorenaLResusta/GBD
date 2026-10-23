---
title: "Programació de la base de dades amb PL/SQL"
weight: 1
bookToc: true
---

# UD09 · Programació de la base de dades amb PL/SQL

## Resum del tema

Fins ara, la lògica de les nostres tasques vivia **fora** de la base de dades: en un guió `.sql` que llançàvem a mà o en l'aplicació que consulta Oracle. Això funciona mentre la tasca siga una seqüència de sentències. Deixa de funcionar quan cal **decidir** (té l'alumne faltes suficients per a perdre l'avaluació contínua?), **repetir** (recórrer tots els alumnes d'un grup), **reaccionar a un error** (què faig si el mòdul no existix?) o **garantir una regla** que ningú puga saltar-se, entre elles les que a la UD03 vam anomenar *restriccions que el model lògic no pot expressar*.

La solució és programar **dins del servidor**. Oracle incorpora per a això el llenguatge **PL/SQL** (*Procedural Language / SQL*): SQL més variables, condicions, bucles, cursors i excepcions, organitzat en **blocs**. Amb ell es construïxen els objectes que guarda la pròpia base de dades: **funcions**, **procediments**, **paquets** i **disparadors**, i amb el planificador `DBMS_SCHEDULER` s'executen sols a l'hora que s'indique.

La unitat avança en cinc passos: primer quines formes hi ha d'automatitzar i amb quines eines es treballa (§1 i §2); després el llenguatge (blocs, variables, control de flux, funcions del gestor i cursors, §3 a §7); a continuació els subprogrames emmagatzemats i el tractament d'errors (§8 a §10); després els disparadors, amb l'auditoria de notes, la integritat que les restriccions no arriben a cobrir i el famós error de la **taula mutant** (§11); i finalment les tasques programades, els paquets i la comparació amb altres gestors (§12 a §14).

Tots els exemples s'executen sobre l'esquema de referència **EDUGEST** amb els [scripts del projecte](/guia/proyecto-edugest#4-scripts-descarregables) carregats (32 alumnes, 143 matrícules, 46 faltes) i usen la sintaxi d'**Oracle AI Database 26ai Free**. Cada exemple indica l'eixida que has d'obtindre. Quan alguna cosa és pròpia d'un gestor concret se senyala amb una etiqueta o una nota.

{{< ra "RA5:a,b,c,d,e,f,g,h,i,j" "RA4:d,h" "RA6:h" >}}

### Objectius d'aprenentatge

En acabar esta unitat seràs capaç de:

- Distingir una consulta, un guió, un bloc anònim, una funció, un procediment, un paquet, un disparador i una tasca programada, i triar la forma d'automatització adequada per a cada necessitat (RA5.a).
- Editar i executar guions amb SQL Developer, SQLcl o SQL\*Plus, usant variables de substitució i l'eixida de `DBMS_OUTPUT` (RA5.b, RA5.c).
- Escriure blocs PL/SQL amb variables, constants i tipus `%TYPE` i `%ROWTYPE`, i distingir les variables de substitució del client de les variables PL/SQL del servidor.
- Aplicar estructures de control de flux (`IF`, `CASE`, `LOOP`, `WHILE`, `FOR`) i les funcions predefinides del gestor (RA5.e, RA5.g).
- Recórrer conjunts de files amb cursors implícits, explícits, de bucle `FOR` i amb paràmetres (RA5.i).
- Definir funcions i procediments d'usuari amb paràmetres `IN`, `OUT` i `IN OUT` (RA5.f).
- Tractar errors amb excepcions predefinides i pròpies, `PRAGMA EXCEPTION_INIT` i `RAISE_APPLICATION_ERROR` (RA5.j).
- Implementar amb disparadors l'auditoria de canvis i les regles d'integritat que el model lògic no pot declarar, i resoldre l'error de taula mutant amb un disparador compost (RA5.h, RA4.h, RA6.h).
- Programar tasques periòdiques amb `DBMS_SCHEDULER`, agrupar subprogrames en paquets i reconéixer els equivalents en MySQL/MariaDB, PostgreSQL i SQL Server (RA5.a, RA5.d, RA4.d).

### Temporalització

La unitat ocupa **7 hores d'aula** (4 de teoria i 3 de pràctica). És la unitat amb més codi del curs: convé escriure'l a mà i recompilar-lo, no copiar-lo i apegar-lo. Les pràctiques llargues (la taula mutant, les tasques programades, el paquet de secretaria i el projecte) es completen fora de l'horari d'aula.

{{< sesiones unidad="UD09" horas="7" >}}
items:
  - {h: 1, tipo: T, t: "Formes d'automatitzar, eines, estructura del bloc, variables, tipus i `DBMS_OUTPUT`", ref: "§1 a §4"}
  - {h: 1, tipo: P, t: "Primers blocs: l'expedient d'un alumne", ref: "Pràctica 9.1"}
  - {h: 1, tipo: T, t: "Control de flux, funcions del gestor, cursors i funcions d'usuari", ref: "§5 a §8 · laboratori de blocs"}
  - {h: 1, tipo: P, t: "Biblioteca de funcions d'EduGest", ref: "Pràctica 9.2"}
  - {h: 1, tipo: T, t: "Excepcions i procediments emmagatzemats", ref: "§9 i §10"}
  - {h: 1, tipo: P, t: "Matrícula amb excepcions (la 9.4, butlletins amb cursors, s'acaba a casa)", ref: "Pràctiques 9.3 i 9.4"}
  - {h: 1, tipo: T, t: "Disparadors, tasques programades amb `DBMS_SCHEDULER` i paquets", ref: "§11 a §14 · simulador de disparadors"}
autonomo:
  - "Pràctica 9.4 (cursors: butlletins i informes), si no s'ha acabat a l'aula"
  - "Pràctica 9.5 (disparadors d'integritat i auditoria)"
  - "Pràctica 9.6 (repte: la taula mutant)"
  - "Pràctica 9.7 (tasques programades)"
  - "Pràctica 9.8 (repte: el paquet de secretaria)"
  - "Projecte EduGest · UD09 (lògica en el servidor)"
{{< /sesiones >}}

> [!IMPORTANT]
> Treballa sempre connectat com a `EDUGEST` i amb l'eixida activada (`SET SERVEROUTPUT ON`). Tot el codi d'esta unitat es prova amb un mètode fix:
>
> 1. **Prediu** què ha de mostrar o tornar abans d'executar-lo.
> 2. Executa i compara amb l'eixida que figura en els apunts.
> 3. Si falla, llig l'error **d'amunt a avall**: el primer missatge (`PLS-` en compilació, `ORA-` en execució) és la causa; els següents només diuen on va ocórrer.
> 4. Guarda cada subprograma en el seu propi fitxer `.sql` acabat en `/`: així es recompila i es versiona.

---

{{< sesion n="1" h="1" tipo="t" >}}Formes d'automatitzar, eines, blocs i variables{{< /sesion >}}

## 1. Programar dins del servidor

### 1.1 Quin problema resol

SQL és un llenguatge **declaratiu**: dius *què* vols, no *com* obtindre-ho. És excel·lent per a consultar i modificar conjunts de files, però no té variables, ni condicions, ni bucles, ni forma de reaccionar a un error. Tan prompte una tasca necessita alguna d'eixes coses, hi ha dues opcions: traure les dades a una aplicació i programar allí la lògica, o **programar-la dins de la base de dades**.

Pensa en la matrícula d'un alumne a EduGest. Abans d'inserir la fila cal comprovar que l'alumne existix i té grup, que el mòdul és del seu cicle, que no està ja matriculat eixe curs i que no ha esgotat les quatre convocatòries. Són quatre consultes, tres decisions i un `INSERT`, i eixes regles s'han de complir **sempre**, vinga la matrícula de l'aplicació web, d'un script de la secretaria o d'una eina gràfica.

La UD03 ja va identificar les regles de negoci d'EduGest que el model lògic no pot expressar. Esta unitat les implementa:

| Codi | Regla de negoci | Per què no basta una restricció declarativa | On s'implementa |
|---|---|---|---|
| R1 | El cap d'un departament pertany a eixe departament | Compara una fila de `DEPARTAMENTO` amb una de `PROFESOR` | Disparador (§11.3) |
| R2 | Un alumne només es matricula en mòduls del cicle del seu grup, fins a 4 convocatòries | Implica `ALUMNO`, `GRUPO`, `MODULO` i `MATRICULA` | Procediment de matrícula (§10.5) |
| R3 | No hi ha faltes anteriors a la data de matrícula | Compara dues taules | Disparador (pràctica 9.5) |
| R4 | Un professor no supera 20 hores lectives setmanals | És una **suma** sobre diverses files | Disparador compost (pràctica 9.6) |
| R5 | Un grup no supera 30 alumnes | És un **recompte** sobre diverses files | Disparador compost (§11.6) |
| R6 | La nota va en múltiples de 0,25 | És una regla d'**una fila** | `CHECK` (UD05): no necessita PL/SQL |

> [!NOTE]
> La regla R6 està en la taula a propòsit: **no tot es resol amb un disparador**. Si una restricció declarativa (`CHECK`, `UNIQUE`, clau aliena) pot expressar la regla, és sempre preferible: és més ràpida, més clara i l'optimitzador la coneix.

### 1.2 Formes d'automatitzar tasques

El criteri RA5.a demana identificar les formes d'automatitzar una tasca en un gestor. En Oracle són estes:

| Forma | Què és | Quan s'executa | Exemple a EduGest |
|---|---|---|---|
| **Guió** (*script*) | Fitxer de text amb sentències SQL i ordres del client | Quan algú el llança (`@fichero.sql`) | `edugest_01_esquema.sql` |
| **Bloc anònim** | Bloc PL/SQL sense nom que el client envia al servidor | Quan el client l'envia; no es guarda | Un càlcul puntual de comprovació |
| **Funció emmagatzemada** | Subprograma amb nom que **torna un valor** | Quan s'invoca des d'SQL o PL/SQL | `fn_calificacion` |
| **Procediment emmagatzemat** | Subprograma amb nom que **realitza una acció** | Quan s'invoca (`EXEC`, `CALL`, un altre bloc) | `pr_matricular` |
| **Paquet** | Agrupació de subprogrames, constants i variables | Quan s'invoca un dels seus elements | `pkg_secretaria` |
| **Disparador** (*trigger*) | Bloc PL/SQL associat a un **esdeveniment** | **Automàticament** en ocórrer l'esdeveniment (un `UPDATE`, un `CREATE`, una connexió) | `trg_auditoria_nota` |
| **Tasca programada** (*job*) | Execució d'un subprograma o bloc segons un calendari | A l'hora indicada, sense intervenció humana | `JOB_RESUMEN_NOCTURNO` |

Fora del servidor existixen altres formes d'automatitzar, també vàlides: el programador de tasques del sistema operatiu (`cron`, Programador de tasques de Windows) llançant SQLcl, o la pròpia aplicació. La diferència és **on viu la lògica**: dins, viatja amb la base de dades i la protegixen els seus privilegis; fora, depén d'un altre sistema.

### 1.3 Consulta, guió, bloc, funció, procediment, paquet i disparador

És la confusió més freqüent en començar. Esta taula les separa per les seues propietats:

| | Consulta | Guió | Bloc anònim | Funció | Procediment | Paquet | Disparador |
|---|---|---|---|---|---|---|---|
| **Contingut** | Una sentència SQL | Diverses sentències i ordres del client | Un bloc PL/SQL | Un bloc PL/SQL amb `RETURN` | Un bloc PL/SQL | Especificació + cos | Un bloc PL/SQL + esdeveniment |
| **Es guarda en la BD?** | No (excepte com a vista) | No: viu en un fitxer | No | **Sí** | **Sí** | **Sí** | **Sí** |
| **Té nom?** | No | El del fitxer | No | Sí | Sí | Sí | Sí |
| **Qui l'executa?** | El client | El client | El client | Qui el crida | Qui el crida | Qui el crida | **El propi Oracle** |
| **Torna valor?** | Un conjunt de files | No | No | **Un valor** | No (usa paràmetres `OUT`) | Segons l'element | No |
| **S'usa dins d'un `SELECT`?** | Com a subconsulta | No | No | **Sí** | No | Les seues funcions, sí | No |
| **Es compila** | En cada execució | En cada execució | En cada execució | **Una vegada**, en crear-la | **Una vegada** | **Una vegada** | **Una vegada** |

Tres idees per a quedar-se amb la taula:

1. **El que es guarda en la base de dades es compila una sola vegada** i s'executa moltes. Un guió o un bloc anònim s'analitzen cada vegada que s'envien.
2. **Una funció torna un valor i es pot usar en una consulta; un procediment fa alguna cosa.** Si necessites cridar-la des d'un `SELECT`, és una funció.
3. **Un disparador ningú no el crida:** s'executa quan ocorre el seu esdeveniment. Per això cal escriure'ls amb molta cura.

### 1.4 Client o servidor: on posar la lògica

Cada vegada que una aplicació llança una sentència SQL hi ha un **viatge d'anada i tornada** per la xarxa. Si la matrícula d'un alumne en cinc mòduls es programa en l'aplicació, són desenes de viatges; si es programa en un procediment emmagatzemat, és **una** crida.

```text
 Lògica en l'aplicació                         Lògica en el servidor
 ───────────────────────                       ──────────────────────
 App ──SELECT alumno──────────► Oracle         App ──pr_matricular(1, 2, '2026-27')──► Oracle
 App ◄─────────────files──────  Oracle                                                  │ valida
 App ──SELECT módulo──────────► Oracle                                                  │ calcula
 App ◄─────────────files──────  Oracle                                                  │ calcula
 App ──INSERT matricula───────► Oracle         App ◄──────────────────────OK / error─────┘
 App ◄──────────────files─────  Oracle
 (3 viatges com a mínim)                       (1 viatge)
```

| A favor de programar en el servidor | En contra |
|---|---|
| **Menys tràfic de xarxa**: una crida en lloc de moltes | **Portabilitat**: PL/SQL només funciona en Oracle; canviar de gestor obliga a reescriure |
| **Una única implementació** de la regla, vàlida per a totes les aplicacions | Més difícil de **provar, depurar i versionar** que el codi d'una aplicació |
| **Seguretat**: es pot concedir `EXECUTE` sobre un procediment sense donar accés a les taules | Consumix **CPU del servidor**, que és el recurs més car d'escalar |
| **Integritat**: la regla no es pot saltar inserint per una altra via | La lògica queda **repartida** entre base de dades i aplicació |
| **Rendiment**: el codi ja està compilat i les sentències SQL, analitzades | Un disparador mal pensat és una **lògica oculta** que sorprén tothom |

> [!TIP]
> Regla pràctica: posa en el servidor el que protegix la **integritat** de les dades i el que és una **operació atòmica de negoci** (matricular, promocionar, anul·lar). Deixa en l'aplicació la presentació, els fluxos d'usuari i tot el que no afecte la correcció de les dades.

### 1.5 Què és PL/SQL

**PL/SQL** és l'extensió procedimental d'SQL d'Oracle. Un programa PL/SQL s'envia al servidor i l'executa el **motor PL/SQL**, que s'encarrega de les instruccions procedimentals (assignacions, condicions, bucles) i lliura al **motor SQL** les sentències SQL que troba (`SELECT`, `INSERT`, `UPDATE`...).

```text
       Client (SQL Developer, SQLcl, aplicació)
                       │  bloc PL/SQL
                       ▼
        ┌─────────────────────────────────┐
        │          SERVIDOR ORACLE        │
        │   Motor PL/SQL  ──sentències─► Motor SQL ──► Dades
        │   (variables, IF, bucles,      │  (SELECT, INSERT...)
        │    excepcions)   ◄──resultat───┘
        └─────────────────────────────────┘
```

Cada pas d'un motor a l'altre (*context switch*) té un cost xicotet però mesurable. Per això, quan una tasca es pot escriure com **una sola sentència SQL**, eixa és quasi sempre la millor versió (§7.7).

{{< sgbd "Oracle 26ai" >}}

PL/SQL és propi d'Oracle. Cada gestor té el seu llenguatge: PostgreSQL usa **PL/pgSQL**, MySQL i MariaDB usen el llenguatge de rutines emmagatzemades **SQL/PSM**, SQL Server usa **Transact-SQL (T-SQL)**. Els conceptes (variables, condicions, bucles, cursors, excepcions, disparadors) són els mateixos; la sintaxi canvia. L'apartat 14 els compara.

---

## 2. Eines i execució de guions

### 2.1 Eines per a editar guions

El criteri RA5.c demana identificar les eines disponibles. Un guió PL/SQL és text: es pot escriure en qualsevol editor, però les eines especialitzades aporten ressaltat, execució directa i accés al diccionari de dades.

| Eina | Tipus | Què aporta | Quan usar-la |
|---|---|---|---|
| **Oracle SQL Developer** | Gràfica, gratuïta | Editor amb autocompletat, arbre d'objectes, depurador PL/SQL, panell *Eixida de DBMS* | Desenvolupament i depuració diària |
| **Extensió SQL Developer per a VS Code** | Gràfica (extensió de VS Code) | El mateix dins de l'editor amb què ja treballes, amb control de versions integrat | Si la resta del projecte s'edita en VS Code |
| **SQLcl** (`sql`) | Línia d'ordres | SQL\*Plus modern: historial, autocompletat, format de resultats (`SET SQLFORMAT`) | Automatització i treball remot |
| **SQL\*Plus** (`sqlplus`) | Línia d'ordres | L'eina clàssica, present en totes les instal·lacions | Servidors on només hi ha això |
| **Editor de text + Git** | Text | Guions versionats i revisables | Sempre: **el guió en Git és la font de veritat** |

> [!NOTE]
> En el contenidor *Oracle AI Database 26ai Free* el servei al qual es connecta l'alumnat és `FREEPDB1`: `sql edugest@localhost:1521/FREEPDB1`.

### 2.2 Mètodes d'execució de guions

El criteri RA5.b demana reconéixer els mètodes d'execució de guions. Un guió pot executar-se de diverses maneres:

| Mètode | On | Què fa |
|---|---|---|
| `@ruta/fichero.sql` | SQLcl, SQL\*Plus | Executa el guió. La ruta és relativa al directori actual |
| `@@fichero.sql` | SQLcl, SQL\*Plus | Executa el guió **relatiu al guió que el crida**: útil en un guió mestre que n'invoca altres |
| `START fichero.sql` | SQLcl, SQL\*Plus | Sinònim de `@` |
| `sql edugest@servicio @fichero.sql` | Terminal | Es connecta i executa el guió en mode *batch* (sense interacció) |
| `F5` (*Executar script*) | SQL Developer | Executa **tot** el guió tal qual; `Ctrl+Intro` executa només la sentència sota el cursor |
| Tasca programada | `DBMS_SCHEDULER` | Executa un procediment o bloc a l'hora indicada (§12) |

Un guió pot rebre **paràmetres posicionals** (`&1`, `&2`...), que són substituïts pel client abans d'enviar res al servidor:

```sql
-- informe_grupo.sql · Ús: @informe_grupo.sql 2DAW
SET VERIFY OFF
WHENEVER SQLERROR EXIT FAILURE ROLLBACK
SPOOL informe_&1..txt

SELECT nia, apellidos, nombre
FROM   alumno
WHERE  cod_grupo = '&1'
ORDER  BY apellidos;

SPOOL OFF
```

{{< sgbd "Oracle 26ai" >}}

En llançar `@informe_grupo.sql 2DAW` es crea el fitxer `informe_2DAW.txt` (el segon punt de `&1..txt` és el literal; el primer acaba el nom de la variable) amb:

| NIA | APELLIDOS | NOMBRE |
|---|---|---|
| 10450851 | Amorós Guillem | Sara |
| 10450777 | Carbonell Soriano | Elena |
| 10450814 | Planelles Marco | Sofía |
| 10450740 | Sala Brotons | Mateo |
| 10450888 | Verdú Castelló | Nicolás |

*5 files*

Les ordres d'un guió són de dues classes que convé no confondre:

| Classe | Exemples | Qui les entén |
|---|---|---|
| **Sentències SQL i blocs PL/SQL** | `SELECT`, `INSERT`, `CREATE TABLE`, `BEGIN ... END;` | El **servidor** Oracle |
| **Ordres del client** | `SET SERVEROUTPUT ON`, `SET VERIFY OFF`, `SPOOL`, `DEFINE`, `ACCEPT`, `WHENEVER`, `@` | Només **SQLcl i SQL\*Plus** (SQL Developer entén la majoria). El servidor no les coneix |

### 2.3 Com s'acaba cada cosa: `;` i `/`

El client necessita saber on acaba cada sentència per a enviar-la al servidor. La regla és simple però és la causa de molts errors de principiant:

| S'escriu | Terminador | Motiu |
|---|---|---|
| Sentència SQL (`SELECT`, `UPDATE`...) | `;` | El punt i coma és del client: li diu «envia això» |
| Ordre del client (`SET`, `SPOOL`...) | Res (fi de línia) | No és SQL |
| Bloc PL/SQL anònim, `CREATE PROCEDURE`, `CREATE FUNCTION`, `CREATE TRIGGER`, `CREATE PACKAGE` | `;` **i** `/` en una línia sola | Dins del bloc hi ha molts `;`, així que el `;` ja no servix per a saber on acaba. La `/` diu «el bloc acaba ací, envia'l» |

```sql
BEGIN
    DBMS_OUTPUT.PUT_LINE('Hola');   -- este ; tanca la instrucció PL/SQL
END;                                 -- este ; tanca el bloc
/                                    -- esta / l'envia al servidor
```

> [!WARNING]
> Si oblides la `/`, SQLcl es queda esperant sense executar res (a vegades mostra un número de línia, `2  3  4...`). Si l'escrius de més, executes **una altra vegada** l'últim bloc. Un `CREATE OR REPLACE` repetit és inofensiu; un bloc amb un `INSERT`, no.

### 2.4 L'eixida del servidor: `DBMS_OUTPUT`

PL/SQL no té una instrucció `PRINT`. El paquet `DBMS_OUTPUT` escriu text en un **búfer del servidor**, i és el client qui el bolca per pantalla quan el bloc acaba, **si se li ha demanat**:

```sql
SET SERVEROUTPUT ON
```

| Element | Què fa |
|---|---|
| `SET SERVEROUTPUT ON` | Demana al client que mostre el búfer en acabar cada bloc. Sense esta ordre el bloc funciona, però **no es veu res** |
| `SET SERVEROUTPUT ON SIZE UNLIMITED` | Igual, sense límit de grandària del búfer |
| `DBMS_OUTPUT.PUT_LINE(texto)` | Afig una línia al búfer |
| `DBMS_OUTPUT.PUT(texto)` i `NEW_LINE` | Afigen text sense salt de línia i el salt, respectivament |

En SQL Developer, a més de `SET SERVEROUTPUT ON`, ha d'estar obert el panell *Veure → Eixida de DBMS* i habilitada la connexió amb el botó **+**.

> [!WARNING]
> `DBMS_OUTPUT` és una eina de **depuració i de pràctiques**, no un mecanisme de producció: el text només existix mentre dura l'execució, es mostra al final (no mentre el bloc treballa) i un procediment que s'executa des d'una aplicació o una tasca programada no té ningú al davant per a llegir-lo. Per a deixar constància cal escriure en una **taula de registre** (pràctica 9.7).

### 2.5 Errors de compilació

Un procediment, funció o disparador es **compila en crear-lo**. Si hi ha errors, Oracle el crea igualment però en estat `INVALID` i avisa amb `Warning: Procedure created with compilation errors.` Els errors de compilació comencen per `PLS-`:

```sql
SHOW ERRORS
-- o, des de qualsevol client:
SELECT line, position, text
FROM   user_errors
WHERE  name = 'FN_EDAD'
ORDER  BY sequence;
```

| Missatge | Causa habitual |
|---|---|
| `PLS-00103: Encountered the symbol "..." when expecting one of the following` | Error de sintaxi: un `;` oblidat, un `END IF` sense tancar, una coma sobrant |
| `PLS-00201: identifier 'X' must be declared` | Nom mal escrit, variable no declarada, o falta de privilegi sobre l'objecte |
| `PLS-00302: component 'X' must be declared` | S'usa una columna o un camp que no existix (`r_alumno.telefon`) |
| `PLS-00306: wrong number or types of arguments in call to 'X'` | Crida amb més, menys o distints paràmetres dels declarats |
| `PLS-00428: an INTO clause is expected in this SELECT statement` | Un `SELECT` dins d'un bloc sense `INTO` (ni cursor) |
| `PLS-00363: expression 'X' cannot be used as an assignment target` | S'assigna a una constant, a un paràmetre `IN` o a l'índex d'un bucle `FOR` |

---

{{% curiosidad titulo="PL/SQL s'assembla a Ada" %}}
La sintaxi de PL/SQL (`BEGIN … END;`, `:=`, `IF … THEN … END IF;`, les excepcions) està inspirada en el llenguatge **Ada**. Va aparéixer a finals dels anys huitanta, per a poder ficar lògica de programa dins del servidor i no només sentències soltes.
{{% /curiosidad %}}

## 3. Estructura d'un bloc PL/SQL

### 3.1 Les quatre seccions

Tot programa PL/SQL es construïx amb **blocs**. Un bloc té fins a quatre seccions, i només `BEGIN ... END` és obligatòria:

```text
DECLARE        -- 1. Declaracions (opcional): variables, constants, cursors, excepcions
    ...
BEGIN          -- 2. Instruccions (obligatòria): el programa en si
    ...
EXCEPTION      -- 3. Tractament d'errors (opcional)
    ...
END;           -- 4. Fi del bloc
```

{{< sgbd "Oracle 26ai" >}}

```sql
SET SERVEROUTPUT ON
DECLARE
    c_centro  CONSTANT VARCHAR2(20) := 'EduGest';      -- constant
    v_hoy     DATE := SYSDATE;                          -- variable inicialitzada
BEGIN
    DBMS_OUTPUT.PUT_LINE('Centro:  ' || c_centro);
    DBMS_OUTPUT.PUT_LINE('Usuario: ' || USER);
    DBMS_OUTPUT.PUT_LINE('Fecha:   ' || TO_CHAR(v_hoy, 'DD/MM/YYYY'));
END;
/
```

```text
Centro:  EduGest
Usuario: EDUGEST
Fecha:   07/10/2026

PL/SQL procedure successfully completed.
```

La data és la del teu sistema. L'última línia l'escriu el client, no el bloc: confirma que el servidor l'ha executat sense errors.

| Part | Què fa |
|---|---|
| `DECLARE` | Reserva nom i tipus per a les dades que usarà el bloc. Si no hi ha res que declarar, s'omet |
| `CONSTANT` | El valor no pot canviar després de la declaració |
| `:=` | Operador d'assignació. (La igualtat s'escriu `=`) |
| `BEGIN ... END;` | Les instruccions, acabades cadascuna en `;` |
| `\|\|` | Concatenació de text. Converteix números i dates a text de forma implícita |
| `USER` | Funció del sistema: l'usuari connectat |

### 3.2 Què es pot escriure dins d'un bloc

| Instrucció | Permesa directament? | Observacions |
|---|---|---|
| `INSERT`, `UPDATE`, `DELETE`, `MERGE` | Sí | S'escriuen igual que en SQL |
| `SELECT` | Sí, **amb `INTO`** o dins d'un cursor | `SELECT` sense `INTO` dona `PLS-00428` |
| `COMMIT`, `ROLLBACK`, `SAVEPOINT` | Sí | El control de la transacció (UD08) funciona igual |
| `CREATE`, `ALTER`, `DROP` (DDL) | **No directament** | Cal usar SQL dinàmic: `EXECUTE IMMEDIATE 'CREATE TABLE ...'` |
| `GRANT`, `REVOKE` (DCL) | **No directament** | També amb `EXECUTE IMMEDIATE` |
| Ordres de client (`SET`, `SPOOL`, `DEFINE`...) | **No** | Són del client, no del servidor |

### 3.3 Blocs aniuats i àmbit

Un bloc pot contindre altres blocs en la seua secció executable o en la d'excepcions. Una variable és visible en el bloc on es declara i en els blocs que conté; si un bloc interior en declara una amb el mateix nom, **oculta** l'exterior mentre dura.

```sql
DECLARE
    v_x  NUMBER := 1;                                    -- bloc exterior
BEGIN
    DECLARE
        v_x  NUMBER := 2;                                -- oculta l'exterior
        v_y  NUMBER := 10;
    BEGIN
        DBMS_OUTPUT.PUT_LINE('Interior: x=' || v_x || ' y=' || v_y);
    END;
    DBMS_OUTPUT.PUT_LINE('Exterior: x=' || v_x);
    -- DBMS_OUTPUT.PUT_LINE(v_y);   -- PLS-00201: v_y no existix fora del seu bloc
END;
/
```

```text
Interior: x=2 y=10
Exterior: x=1
```

Els blocs aniuats no servixen només per a organitzar el codi: són l'eina per a **limitar l'abast d'una excepció** (§9.7).

### 3.4 Comentaris, majúscules i convencions de noms

PL/SQL no distingix majúscules de minúscules en el codi (`begin` és `BEGIN`), però sí en els **literals de text** (`'EduGest'` i `'EDUGEST'` són distints). Els comentaris són de línia (`-- texto`) o de diverses línies (`/* texto */`).

Un prefix en cada nom evita l'error més comú: que una variable es diga igual que una columna. Si en `WHERE id_alumno = id_alumno` tots dos són la columna, la condició és sempre vertadera. EduGest usa estes convencions:

| Element | Prefix | Exemple |
|---|---|---|
| Variable local | `v_` | `v_media` |
| Constant | `c_` | `c_max_convocatorias` |
| Paràmetre | `p_` | `p_id_alumno` |
| Registre (*record*) | `r_` | `r_alumno` |
| Cursor | `c_` o `cur_` | `c_notas` |
| Excepció pròpia | `e_` | `e_sin_grupo` |
| Tipus definit per l'usuari | `t_` | `t_grupos` |
| Funció / procediment | `fn_` / `pr_` | `fn_edad`, `pr_matricular` |
| Disparador | `trg_` | `trg_auditoria_nota` |
| Paquet | `pkg_` | `pkg_secretaria` |

---

## 4. Variables, constants i tipus

### 4.1 Declaració

```text
nom  [CONSTANT]  tipus  [NOT NULL]  [:= valor_inicial | DEFAULT valor_inicial];
```

| Tipus | S'usa per a | Observacions |
|---|---|---|
| `VARCHAR2(n)` | Text de longitud variable | **La longitud és obligatòria** en variables. En PL/SQL admet fins a 32 767 bytes; en una columna, 4000 |
| `NUMBER(p,s)` | Números exactes | Igual que en les taules. `NUMBER` sense paràmetres admet qualsevol valor |
| `PLS_INTEGER` | Enters (comptadors, índexs) | Aritmètica entera més ràpida que `NUMBER` |
| `DATE` | Dates amb hora fins al segon | `SYSDATE`, `DATE '2027-05-14'` |
| `TIMESTAMP` | Data i hora amb fraccions de segon | `SYSTIMESTAMP` |
| `BOOLEAN` | `TRUE`, `FALSE`, `NULL` | Sempre ha existit en PL/SQL; des d'Oracle 23ai també en SQL (columnes i expressions) |

Dues regles valen per a tots: una variable sense valor inicial val `NULL`, i una constant **ha de** tindre valor inicial.

### 4.2 Assignar valors: `:=` i `SELECT ... INTO`

Una variable rep valor de dues formes: amb l'operador `:=` o llegint d'una consulta amb `INTO`.

```sql
DECLARE
    v_nia     alumno.nia%TYPE;
    v_nombre  VARCHAR2(130);
BEGIN
    SELECT nia, apellidos || ', ' || nombre
    INTO   v_nia, v_nombre
    FROM   alumno
    WHERE  id_alumno = 20;

    DBMS_OUTPUT.PUT_LINE(v_nia || ' · ' || v_nombre);
END;
/
```

```text
10450740 · Sala Brotons, Mateo
```

`SELECT ... INTO` exigix que la consulta torne **exactament una fila**:

| La consulta torna | Resultat |
|---|---|
| Una fila | Correcte: les columnes es copien a les variables, **en ordre** |
| Cap fila | Excepció `NO_DATA_FOUND` (`ORA-01403`) |
| Més d'una fila | Excepció `TOO_MANY_ROWS` (`ORA-01422`), i no s'assigna res |

El laboratori de l'apartat 7.6 permet veure-ho pas a pas amb els tres casos.

> [!CAUTION]
> Un `SELECT ... INTO` amb una funció d'agregat **sense `GROUP BY`** torna sempre una fila, encara que no hi haja dades: `SELECT AVG(nota_final) INTO v_media FROM matricula WHERE id_alumno = 30;` no llança `NO_DATA_FOUND`; `v_media` queda a `NULL`. És una diferència important entre «la consulta no troba res» i «l'agregat de res».

### 4.3 `%TYPE` i `%ROWTYPE`: heretar el tipus de la taula

Escriure `v_nia CHAR(8)` funciona fins al dia en què algú amplia la columna. Els atributs `%TYPE` i `%ROWTYPE` fan que la variable **herete el tipus directament del diccionari de dades**:

| Atribut | Declara | Exemple |
|---|---|---|
| `tabla.columna%TYPE` | Una variable amb el tipus exacte d'eixa columna | `v_nia alumno.nia%TYPE;` |
| `variable%TYPE` | Una variable del mateix tipus que una altra | `v_otra v_nia%TYPE;` |
| `tabla%ROWTYPE` | Un **registre** amb un camp per cada columna de la taula | `r_mod modulo%ROWTYPE;` |
| `cursor%ROWTYPE` | Un registre amb les columnes del cursor | `r_nota c_notas%ROWTYPE;` |

```sql
DECLARE
    r_mod  modulo%ROWTYPE;                              -- un camp per columna de MODULO
BEGIN
    SELECT * INTO r_mod FROM modulo WHERE id_modulo = 2;

    DBMS_OUTPUT.PUT_LINE(r_mod.codigo || ' ' || r_mod.nombre ||
                         ' (' || r_mod.cod_ciclo || ', curso ' || r_mod.curso ||
                         ', ' || r_mod.horas || ' h)');
END;
/
```

```text
0484 Bases de datos (DAM, curso 1, 160 h)
```

S'accedix a cada camp amb `registro.columna`. Avantatges de `%ROWTYPE`: el `SELECT *` no necessita una variable per columna, i si s'afig una columna a `MODULO` el bloc continua compilant. El seu inconvenient: **porta totes les columnes**, encara que només n'uses dos.

Quan interessa un registre amb camps triats, es defineix un tipus propi amb `RECORD`:

```sql
DECLARE
    TYPE t_resumen IS RECORD (
        nia     alumno.nia%TYPE,
        nombre  VARCHAR2(130),
        media   NUMBER(4,2)
    );
    r  t_resumen;
BEGIN
    SELECT a.nia, a.apellidos || ', ' || a.nombre, ROUND(AVG(m.nota_final), 2)
    INTO   r
    FROM   alumno a
           JOIN matricula m ON m.id_alumno = a.id_alumno
    WHERE  a.id_alumno = 20
    GROUP  BY a.nia, a.apellidos, a.nombre;

    DBMS_OUTPUT.PUT_LINE(r.nia || ' · ' || r.nombre || ' · media ' || r.media);
END;
/
```

```text
10450740 · Sala Brotons, Mateo · media 7.13
```

> [!NOTE]
> Els números es converteixen a text amb el separador decimal de la sessió (`NLS_NUMERIC_CHARACTERS`). En el contenidor de pràctiques és el punt, com en les eixides d'estos apunts; amb una configuració regional espanyola veuries `7,13`. Per a controlar-ho, usa `TO_CHAR(x, '990D00')`.

### 4.4 Variables de substitució enfront de variables PL/SQL

És la confusió més freqüent de la unitat. Observa este bloc:

```sql
SET VERIFY ON
DEFINE g_grupo = 2DAW
BEGIN
    DBMS_OUTPUT.PUT_LINE('Grupo: &g_grupo');
END;
/
```

```text
old   2:     DBMS_OUTPUT.PUT_LINE('Grupo: &g_grupo');
new   2:     DBMS_OUTPUT.PUT_LINE('Grupo: 2DAW');
Grupo: 2DAW
```

Les dues línies `old` i `new` les escriu el **client** (SQLcl, SQL\*Plus, SQL Developer): ha **substituït** `&g_grupo` per `2DAW` en el text del bloc i només després l'ha enviat a Oracle. El servidor mai no ha vist el `&`. Una variable de substitució no és una variable: és un **marcador de «buscar i reemplaçar» del client**.

| | Variable de substitució (`&nombre`) | Variable PL/SQL (`v_nombre`) |
|---|---|---|
| **Qui la resol?** | El **client**, abans d'enviar el text | El **servidor**, mentre s'executa |
| **Quan?** | Abans que el bloc existisca | En temps d'execució |
| **Què és?** | Text que s'apega en el codi | Un valor amb tipus, dins de la memòria del bloc |
| **Declaració** | `DEFINE`, `ACCEPT` o es pregunta en executar | `DECLARE v_nombre tipo;` |
| **Existix en un procediment emmagatzemat?** | **No**: es resoldria una vegada en crear-lo | Sí |
| **Canvia dins d'un bucle?** | **No**: ja és text fix | Sí |
| **Pròpia de** | SQL\*Plus / SQLcl / SQL Developer | PL/SQL |

| Ordre | Efecte |
|---|---|
| `DEFINE nombre = valor` | Crea la variable de substitució amb eixe valor (sense cometes: s'apega literalment) |
| `ACCEPT nombre PROMPT 'texto'` | Demana el valor per teclat |
| `&nombre` | Se substituïx. Si no està definida, el client **pregunta** |
| `&&nombre` | Com `&`, però a més la deixa definida: no torna a preguntar |
| `SET VERIFY ON \| OFF` | Mostra (o no) les línies `old` i `new` |
| `SET DEFINE OFF` | Desactiva la substitució: el `&` passa a ser un caràcter normal |

> [!WARNING]
> Com que `&variable` és text apegat en el codi, **escriure `&id_alumno` en un guió que rep dades d'una persona és una via d'injecció de codi**. Servix per a pràctiques amb un guió que executes tu; en una aplicació s'usen sempre **variables d'enllaç** (`:nombre`) o paràmetres d'un procediment. I a la inversa: si les teues dades contenen un `&` (`'Gómez & Pérez'`), el client intentarà substituir-lo i preguntarà per una variable; l'script de dades d'EduGest comença amb `SET DEFINE OFF` per eixa raó.

Les **variables d'enllaç** (*bind variables*) es declaren en el client amb `VARIABLE` i es lligen amb `:nombre`. Sí que les entén el servidor, que les rep com a valors:

```sql
VARIABLE v_total NUMBER
BEGIN
    SELECT COUNT(*) INTO :v_total FROM alumno WHERE cod_grupo = '2DAW';
END;
/
PRINT v_total
```

```text
   V_TOTAL
----------
         5
```

### 4.5 Variables del sistema i del context de la sessió

PL/SQL no té variables globals del sistema com a tals: s'obtenen amb funcions. Estes són les més útils:

| Expressió | Torna |
|---|---|
| `USER` | Usuari connectat (`EDUGEST`) |
| `SYSDATE` | Data i hora del servidor (tipus `DATE`) |
| `SYSTIMESTAMP` | Data i hora amb fraccions de segon i zona horària |
| `SYS_CONTEXT('USERENV', 'SESSION_USER')` | Usuari de la sessió |
| `SYS_CONTEXT('USERENV', 'HOST')` | Nom de l'equip client |
| `SYS_CONTEXT('USERENV', 'IP_ADDRESS')` | Adreça IP del client |
| `SYS_CONTEXT('USERENV', 'DB_NAME')` | Nom de la base de dades |
| `SYS_CONTEXT('USERENV', 'CON_NAME')` | Nom de la base de dades connectable (*PDB*), p. ex. `FREEPDB1` |
| `SQLCODE`, `SQLERRM` | Codi i missatge de l'últim error (només dins d'un manejador, §9.3) |
| `SQL%ROWCOUNT` | Files afectades per l'última sentència DML (§7.1) |

Estes funcions són les que permeten registrar **qui** ha fet un canvi i **des d'on**: s'usen en l'auditoria (§11.2).

{{< quiz >}}
- q: "En el bloc `BEGIN DBMS_OUTPUT.PUT_LINE('Hola'); END;` no apareix res per pantalla, però tampoc hi ha error. Què falta?"
  options: ["Un `COMMIT` abans de l'`END`", "`SET SERVEROUTPUT ON` en el client", "Declarar una variable de tipus text", "Canviar `PUT_LINE` per `PRINT`"]
  answer: 1
  explain: "`DBMS_OUTPUT` escriu en un búfer del servidor i és el client qui el mostra, només si se li ha demanat amb `SET SERVEROUTPUT ON`. Sense eixa ordre el bloc s'executa correctament, però no es veu res."
- q: "Un bloc conté `WHERE cod_grupo = '&g'` i s'executa en SQLcl. Qui substituïx `&g` i quan?"
  options: ["Oracle, durant l'execució del bloc", "El client, abans d'enviar el bloc al servidor", "El motor PL/SQL, quan llig la variable `g`", "Ningú: és una variable PL/SQL que val `NULL`"]
  answer: 1
  explain: "`&g` és una variable de **substitució**: el client (SQLcl, SQL*Plus, SQL Developer) reemplaça el text abans d'enviar res. El servidor ja rep el valor i no sap que va existir un `&`. Per això no existix dins d'un procediment emmagatzemat."
- q: "Què ocorre amb `SELECT nombre INTO v_nombre FROM alumno WHERE nia LIKE '104507%';` si el patró coincidix amb tres alumnes?"
  options: ["S'assigna el primer i s'ignoren els altres", "S'assigna l'últim", "Es llança `TOO_MANY_ROWS` i no s'assigna cap valor", "Es llança `NO_DATA_FOUND`"]
  answer: 2
  explain: "`SELECT ... INTO` exigix exactament una fila. Amb diverses es llança `TOO_MANY_ROWS` (`ORA-01422`). Per a recórrer diverses files cal un cursor (§7)."
- q: "Quin avantatge té declarar `v_nia alumno.nia%TYPE` en lloc de `v_nia CHAR(8)`?"
  options: ["La variable és més ràpida", "La variable herete el tipus de la columna i continua sent correcta si la columna canvia", "Permet emmagatzemar valors nuls", "Fa que la variable siga una constant"]
  answer: 1
  explain: "`%TYPE` consulta el diccionari de dades: si s'amplia o canvia la columna, el codi continua sent coherent sense tocar-lo. Una longitud escrita a mà es queda anticuada."
{{< /quiz >}}


---

{{< sesion n="3" h="1" tipo="t" >}}Control de flux, funcions del gestor, cursors i funcions d'usuari{{< /sesion >}}

## 5. Estructures de control de flux

El criteri RA5.g demana utilitzar estructures de control. PL/SQL té les tres famílies habituals: **condicionals** (`IF`, `CASE`), **repetitives** (`LOOP`, `WHILE`, `FOR`) i de **salt** (`EXIT`, `CONTINUE`, `GOTO`).

### 5.1 `IF`, `ELSIF` y `ELSE`

```text
IF condició1 THEN
    instruccions;
[ELSIF condició2 THEN
    instruccions;]
[ELSE
    instruccions;]
END IF;
```

S'escriu `ELSIF` (sense la `E` d'*else if*) i es tanca amb `END IF;`. Les condicions s'avaluen **en ordre** i s'executa la primera branca vertadera.

```sql
DECLARE
    v_nota   matricula.nota_final%TYPE := 6.5;
    v_texto  VARCHAR2(15);
BEGIN
    IF v_nota IS NULL THEN
        v_texto := 'NC';
    ELSIF v_nota < 5 THEN
        v_texto := 'Insuficiente';
    ELSIF v_nota < 6 THEN
        v_texto := 'Suficiente';
    ELSIF v_nota < 7 THEN
        v_texto := 'Bien';
    ELSIF v_nota < 9 THEN
        v_texto := 'Notable';
    ELSE
        v_texto := 'Sobresaliente';
    END IF;

    DBMS_OUTPUT.PUT_LINE(v_nota || ' -> ' || v_texto);
END;
/
```

```text
6.5 -> Bien
```

> [!WARNING]
> **Una condició amb `NULL` no és vertadera ni falsa: és desconeguda** (*lògica trivaluada*, UD06), i `IF` només executa la branca `THEN` quan la condició és **vertadera**. Amb `v_nota` a `NULL`, `IF v_nota >= 5 THEN ... ELSE` executaria l'`ELSE` i marcaria com a suspés qui no s'ha presentat. Per això en l'exemple la primera pregunta és `IS NULL`. I mai s'escriu `v_nota = NULL`: no és vertadera mai.

| `x` | `y` | `x = y` | `x <> y` | `x IS NULL` |
|---|---|---|---|---|
| 5 | 5 | `TRUE` | `FALSE` | `FALSE` |
| 5 | 6 | `FALSE` | `TRUE` | `FALSE` |
| 5 | `NULL` | **`NULL`** | **`NULL`** | `FALSE` |
| `NULL` | `NULL` | **`NULL`** | **`NULL`** | `TRUE` |

### 5.2 `CASE`: sentència i expressió

`CASE` és l'alternativa més llegible quan hi ha moltes branques. Existix en dues formes, i cadascuna en dos usos:

| Forma | Sintaxi | S'usa quan |
|---|---|---|
| **Simple** | `CASE variable WHEN valor1 THEN ... WHEN valor2 THEN ... END` | Es compara **una expressió amb diversos valors** |
| **Amb condicions** (*searched*) | `CASE WHEN condición1 THEN ... WHEN condición2 THEN ... END` | Cada branca té **la seua pròpia condició** |

| Ús | Acaba en | Què produïx |
|---|---|---|
| **Sentència** `CASE` | `END CASE;` | Executa instruccions |
| **Expressió** `CASE` | `END` | **Torna un valor** que s'assigna o es concatena |

```sql
DECLARE
    v_turno  grupo.turno%TYPE;
BEGIN
    SELECT turno INTO v_turno FROM grupo WHERE cod_grupo = '2DAW';

    -- CASE simple com a sentència
    CASE v_turno
        WHEN 'M' THEN DBMS_OUTPUT.PUT_LINE('2DAW: turno de mañana');
        WHEN 'T' THEN DBMS_OUTPUT.PUT_LINE('2DAW: turno de tarde');
        ELSE          DBMS_OUTPUT.PUT_LINE('2DAW: turno desconocido');
    END CASE;

    -- CASE amb condicions com a expressió
    DBMS_OUTPUT.PUT_LINE('Hora de entrada: ' ||
        CASE WHEN v_turno = 'M' THEN '08:00' ELSE '15:00' END);
END;
/
```

```text
2DAW: turno de tarde
Hora de entrada: 15:00
```

> [!CAUTION]
> Si cap branca d'una **sentència** `CASE` es complix i no hi ha `ELSE`, Oracle llança `CASE_NOT_FOUND` (`ORA-06592`). L'**expressió** `CASE` sense `ELSE` torna `NULL` en silenci. Escriu sempre l'`ELSE`.

### 5.3 Bucles

| Bucle | Quan usar-lo | Sintaxi |
|---|---|---|
| **`LOOP`** bàsic | No se sap quantes voltes; l'eixida es decidix al mig | `LOOP ... EXIT WHEN cond; ... END LOOP;` |
| **`WHILE`** | La condició es comprova **abans** de cada volta (pot no executar-se mai) | `WHILE cond LOOP ... END LOOP;` |
| **`FOR`** numèric | Se sap quantes voltes | `FOR i IN 1..n LOOP ... END LOOP;` |
| **`FOR` de cursor** | Recórrer les files d'una consulta (§7.3) | `FOR r IN (SELECT ...) LOOP ... END LOOP;` |

Un exemple amb cadascun, sobre les convocatòries que li queden a un alumne que va per la segona:

```sql
DECLARE
    v_conv  PLS_INTEGER := 2;                      -- convocatòria actual
BEGIN
    -- LOOP bàsic: l'eixida està al mig
    LOOP
        EXIT WHEN v_conv > 4;
        DBMS_OUTPUT.PUT_LINE('Queda la convocatoria ' || v_conv);
        v_conv := v_conv + 1;
    END LOOP;

    -- WHILE: equivalent, amb la condició al principi
    v_conv := 2;
    WHILE v_conv <= 4 LOOP
        DBMS_OUTPUT.PUT_LINE('(while) convocatoria ' || v_conv);
        v_conv := v_conv + 1;
    END LOOP;
END;
/
```

```text
Queda la convocatoria 2
Queda la convocatoria 3
Queda la convocatoria 4
(while) convocatoria 2
(while) convocatoria 3
(while) convocatoria 4
```

El bucle `FOR` numèric declara **ell mateix** el seu comptador, que només existix dins del bucle i **no es pot modificar**:

```sql
DECLARE
    v_nombre  modulo.nombre%TYPE;
BEGIN
    FOR i IN 1..3 LOOP
        SELECT nombre INTO v_nombre FROM modulo WHERE id_modulo = i;
        DBMS_OUTPUT.PUT_LINE(i || '. ' || v_nombre);
    END LOOP;

    FOR i IN REVERSE 1..3 LOOP                       -- compte enrere
        DBMS_OUTPUT.PUT_LINE('Cuenta atrás: ' || i);
    END LOOP;
END;
/
```

```text
1. Sistemas informáticos
2. Bases de datos
3. Programación
Cuenta atrás: 3
Cuenta atrás: 2
Cuenta atrás: 1
```

### 5.4 `EXIT`, `CONTINUE`, etiquetes i `GOTO`

| Instrucció | Efecte |
|---|---|
| `EXIT;` / `EXIT WHEN cond;` | Ix del bucle més intern |
| `CONTINUE;` / `CONTINUE WHEN cond;` | Salta al principi de la volta següent |
| `<<etiqueta>>` abans d'un bucle | Li dona nom; permet `EXIT etiqueta;` per a eixir d'un bucle exterior des d'un d'interior |
| `GOTO etiqueta;` | Salt incondicional. **Evita'l**: trenca la lectura lineal del codi |

```sql
BEGIN
    <<externo>>
    FOR g IN 1..3 LOOP
        FOR a IN 1..3 LOOP
            CONTINUE WHEN a = 2;                     -- se salta la volta a = 2
            EXIT externo WHEN g = 2;                 -- ix dels DOS bucles
            DBMS_OUTPUT.PUT_LINE('g=' || g || ' a=' || a);
        END LOOP;
    END LOOP externo;
END;
/
```

```text
g=1 a=1
g=1 a=3
```

### 5.5 Errors habituals amb els bucles

| Error | Símptoma | Solució |
|---|---|---|
| `LOOP` sense `EXIT` assolible | Bucle infinit: el client es queda penjat | Comprova que la variable de la condició canvia dins del bucle |
| Assignar al comptador del `FOR` | `PLS-00363: expression 'I' cannot be used as an assignment target` | Copia el valor a una altra variable |
| Usar el comptador fora del `FOR` | `PLS-00201: identifier 'I' must be declared` | És local al bucle |
| `SELECT ... INTO` dins d'un bucle sobre files | Una consulta per volta i `NO_DATA_FOUND` possible | Usa un cursor `FOR` (§7.3) |

{{% details title="Prova tu: marcar els mòduls llargs" %}}
**Enunciat.** Escriu un bloc que mostre els mòduls amb identificador 1 a 5 i marque amb un asterisc els que tinguen més de 150 hores.

**Solució.**

```sql
DECLARE
    r_mod  modulo%ROWTYPE;
BEGIN
    FOR i IN 1..5 LOOP
        SELECT * INTO r_mod FROM modulo WHERE id_modulo = i;
        DBMS_OUTPUT.PUT_LINE(
            CASE WHEN r_mod.horas > 150 THEN '* ' ELSE '  ' END ||
            r_mod.codigo || ' ' || r_mod.nombre || ' (' || r_mod.horas || ' h)');
    END LOOP;
END;
/
```

```text
* 0483 Sistemas informáticos (160 h)
* 0484 Bases de datos (160 h)
* 0485 Programación (256 h)
  0487 Entornos de desarrollo (96 h)
  0373 Lenguajes de marcas y sistemas de gestión de información (128 h)
```

El `CASE` és una **expressió**: torna el prefix que es concatena al text.
{{% /details %}}

---

## 6. Funcions proporcionades pel sistema gestor

El criteri RA5.e demana fer ús de les funcions del gestor. Ja les coneixes de SQL (UD06); en PL/SQL són les mateixes i s'usen igual en les expressions.

### 6.1 Catàleg de funcions útils

{{< sgbd "Oracle 26ai" >}}

| Categoria | Funció | Exemple | Resultat |
|---|---|---|---|
| **Text** | `UPPER`, `LOWER` | `UPPER('Sala Brotons')` | `SALA BROTONS` |
| | `INITCAP` | `INITCAP('sala BROTONS')` | `Sala Brotons` |
| | `SUBSTR(t, inicio, n)` | `SUBSTR('10450740', 1, 4)` | `1045` |
| | `INSTR(t, buscado)` | `INSTR('mateosala20@alu.edugest.es', '@')` | `12` |
| | `LENGTH` | `LENGTH('Bases de datos')` | `14` |
| | `LPAD`, `RPAD` | `LPAD(7, 3, '0')` | `007` |
| | `TRIM` | `TRIM('  hola  ')` | `hola` |
| | `REPLACE` | `REPLACE('2025-26', '-', '/')` | `2025/26` |
| **Numèriques** | `ROUND(n, d)` | `ROUND(7.125, 2)` | `7.13` |
| | `TRUNC(n, d)` | `TRUNC(7.125, 1)` | `7.1` |
| | `MOD`, `CEIL`, `FLOOR`, `ABS` | `MOD(10, 3)`, `CEIL(4.2)` | `1`, `5` |
| **Data** | `SYSDATE` | `TRUNC(SYSDATE)` | Hui a les 00:00 |
| | `ADD_MONTHS` | `ADD_MONTHS(DATE '2026-09-09', 9)` | `09/06/2027` |
| | `MONTHS_BETWEEN` | `MONTHS_BETWEEN(DATE '2027-06-09', DATE '2026-09-09')` | `9` |
| | `LAST_DAY` | `LAST_DAY(DATE '2027-02-10')` | `28/02/2027` |
| | `EXTRACT` | `EXTRACT(YEAR FROM DATE '2027-05-14')` | `2027` |
| **Conversió** | `TO_CHAR(fecha, formato)` | `TO_CHAR(DATE '2027-05-14', 'DD/MM/YYYY')` | `14/05/2027` |
| | `TO_DATE(texto, formato)` | `TO_DATE('14/05/2027', 'DD/MM/YYYY')` | `14/05/2027` |
| **Nuls** | `NVL(x, y)` | `NVL(NULL, 0)` | `0` |
| | `NVL2(x, si, no)` | `NVL2(nota, 'con nota', 'NC')` | `con nota` si `nota` no és nul·la |
| | `COALESCE(a, b, c...)` | `COALESCE(NULL, NULL, 5)` | `5` |
| | `NULLIF(a, b)` | `NULLIF(5, 5)` | `NULL` |

Un bloc que les combina sobre un alumne real:

```sql
DECLARE
    r_alu  alumno%ROWTYPE;
BEGIN
    SELECT * INTO r_alu FROM alumno WHERE id_alumno = 20;

    DBMS_OUTPUT.PUT_LINE('Ficha:     ' || UPPER(r_alu.apellidos) || ', ' || r_alu.nombre);
    DBMS_OUTPUT.PUT_LINE('Iniciales: ' || SUBSTR(r_alu.nombre, 1, 1) || SUBSTR(r_alu.apellidos, 1, 1));
    DBMS_OUTPUT.PUT_LINE('Nació:     ' ||
        TO_CHAR(r_alu.fecha_nacimiento, 'fmDD "de" month "de" YYYY', 'NLS_DATE_LANGUAGE=SPANISH'));
    DBMS_OUTPUT.PUT_LINE('Edad:      ' ||
        TRUNC(MONTHS_BETWEEN(DATE '2026-10-06', r_alu.fecha_nacimiento) / 12) || ' años');
    DBMS_OUTPUT.PUT_LINE('Dominio:   ' ||
        SUBSTR(r_alu.email, INSTR(r_alu.email, '@') + 1));
END;
/
```

```text
Ficha:     SALA BROTONS, Mateo
Iniciales: MS
Nació:     9 de abril de 2003
Edad:      23 años
Dominio:   alu.edugest.es
```

> [!TIP]
> Fixa't que l'edat es calcula amb `MONTHS_BETWEEN(...) / 12` i `TRUNC`, no amb `(fecha1 - fecha2) / 365`. Restar dates dona dies i els anys de traspàs desajusten el resultat. Eixa expressió és el nucli de la funció `fn_edad` (§8.3).

### 6.2 Quines funcions són d'Oracle i quines estàndard

No totes les funcions existixen en altres gestors. Si el codi ha de ser portable, convé saber-ho:

| Necessitat | Funció d'Oracle | Equivalent estàndard o portable |
|---|---|---|
| Substituir un nul | `NVL(x, y)` (Oracle) | `COALESCE(x, y)` (SQL estàndard) |
| Condicional | `DECODE(x, a, r1, r2)` (Oracle) | `CASE WHEN ... END` (estàndard) |
| Data i hora actuals | `SYSDATE` (Oracle) | `CURRENT_DATE`, `CURRENT_TIMESTAMP` (estàndard) |
| Subcadena | `SUBSTR`, `INSTR` (Oracle, també en MySQL) | `SUBSTRING`, `POSITION` (estàndard) |
| Convertir a text amb format | `TO_CHAR(f, 'DD/MM/YYYY')` (Oracle i PostgreSQL) | `CAST` + format propi de cada gestor |
| Concatenar | `\|\|` (estàndard; MySQL usa `CONCAT`) | `CONCAT` |

> [!NOTE]
> Les funcions d'**agregat** (`SUM`, `AVG`, `COUNT`...), les **analítiques** i `DECODE` només es poden usar dins d'una sentència SQL; no en una instrucció procedimental. Per a obtindre un total, cal escriure'l en un `SELECT ... INTO`; per a decidir, usa `CASE`.

### 6.3 Funcions pròpies de PL/SQL

A més de les de SQL, PL/SQL oferix funcions i atributs que només existixen en el llenguatge procedimental:

| Element | Què fa | Apartat |
|---|---|---|
| `SQLCODE`, `SQLERRM` | Codi i text de l'error que s'està tractant | §9.3 |
| `SQL%ROWCOUNT`, `SQL%FOUND`, `SQL%NOTFOUND` | Resultat de l'última sentència DML | §7.1 |
| `c%FOUND`, `c%NOTFOUND`, `c%ROWCOUNT`, `c%ISOPEN` | Estat d'un cursor explícit | §7.2 |
| `COUNT`, `FIRST`, `LAST`, `NEXT`, `EXISTS`... | Mètodes de les col·leccions | §11.6 |
| `DBMS_OUTPUT`, `DBMS_SCHEDULER`, `DBMS_UTILITY`... | Paquets que subministra Oracle | §2.4, §12 |

---

## 7. Cursors

### 7.1 Què és un cursor i quin és l'implícit

Quan Oracle executa una sentència SQL reserva una zona de memòria privada (l'**àrea de context**) amb la sentència analitzada i les files del resultat. Un **cursor** és el punter a eixa zona. `SELECT ... INTO` només pot portar **una fila**; per a recórrer un resultat de diverses files fa falta un cursor.

| Tipus | Qui el gestiona | S'usa per a |
|---|---|---|
| **Implícit** | Oracle, automàticament, per a cada sentència SQL del bloc | Conéixer el resultat de l'última sentència DML (`SQL%ROWCOUNT`) |
| **Explícit** | El programador: `CURSOR`, `OPEN`, `FETCH`, `CLOSE` | Recórrer consultes de diverses files amb control total |
| **Cursor `FOR`** | El programador declara la consulta; Oracle obri, llig i tanca | La forma habitual de recórrer files |
| **`REF CURSOR`** | El programador; la consulta es decidix en execució | Tornar un resultat a una aplicació (JDBC, Python...) |

Després de cada `INSERT`, `UPDATE`, `DELETE` o `MERGE`, el cursor implícit `SQL` informa del que ha passat:

| Atribut | Significat |
|---|---|
| `SQL%ROWCOUNT` | Nombre de files afectades per l'última sentència |
| `SQL%FOUND` | `TRUE` si la sentència ha afectat almenys una fila |
| `SQL%NOTFOUND` | `TRUE` si no n'ha afectat cap |
| `SQL%ISOPEN` | Sempre `FALSE`: Oracle ja l'ha tancat |

```sql
BEGIN
    UPDATE falta_asistencia
    SET    justificada = 'S'
    WHERE  justificada = 'N' AND fecha < DATE '2025-11-01';

    DBMS_OUTPUT.PUT_LINE('Faltas justificadas: ' || SQL%ROWCOUNT);   -- cal llegir-ho ARA

    IF SQL%NOTFOUND THEN
        DBMS_OUTPUT.PUT_LINE('No había ninguna falta que justificar');
    END IF;
    ROLLBACK;                                                         -- és una prova
END;
/
```

```text
Faltas justificadas: 7
```

> [!WARNING]
> `SQL%ROWCOUNT` se **sobreescriu amb cada sentència SQL** que s'execute després, inclòs un `SELECT INTO`. Llig-lo en la instrucció immediatament posterior al DML, o guarda'l en una variable. I recorda: un `UPDATE` que no troba files **no llança error** (`SQL%NOTFOUND` val `TRUE`); només `SELECT ... INTO` llança `NO_DATA_FOUND`.

### 7.2 Cursors explícits

Un cursor explícit seguix quatre passos:

| Pas | Instrucció | Què passa |
|---|---|---|
| 1. Declarar | `CURSOR c_notas IS SELECT ...;` | Es dona nom a una consulta. **No s'executa** |
| 2. Obrir | `OPEN c_notas;` | Oracle executa la consulta i deixa el cursor **abans de la primera fila** |
| 3. Llegir | `FETCH c_notas INTO variables;` | Copia la fila actual en les variables i avança una fila |
| 4. Tancar | `CLOSE c_notas;` | Allibera els recursos |

```sql
DECLARE
    CURSOR c_notas IS
        SELECT mo.codigo, m.nota_final
        FROM   matricula m JOIN modulo mo ON mo.id_modulo = m.id_modulo
        WHERE  m.id_alumno = 20
        ORDER  BY mo.codigo;
    v_codigo  modulo.codigo%TYPE;
    v_nota    matricula.nota_final%TYPE;
    v_filas   PLS_INTEGER := 0;
BEGIN
    OPEN c_notas;
    LOOP
        FETCH c_notas INTO v_codigo, v_nota;
        EXIT WHEN c_notas%NOTFOUND;                  -- just després del FETCH
        v_filas := v_filas + 1;
        DBMS_OUTPUT.PUT_LINE(v_codigo || '  ' || v_nota);
    END LOOP;
    CLOSE c_notas;
    DBMS_OUTPUT.PUT_LINE('Módulos leídos: ' || v_filas);
END;
/
```

```text
0612  6.5
0613  5.25
0614  7.5
0615  9.25
Módulos leídos: 4
```

Els atributs del cursor permeten saber en quin punt està:

| Atribut | Abans d'`OPEN` | Després d'`OPEN` | Després d'un `FETCH` amb fila | Després d'un `FETCH` sense fila | Després de `CLOSE` |
|---|---|---|---|---|---|
| `%ISOPEN` | `FALSE` | `TRUE` | `TRUE` | `TRUE` | `FALSE` |
| `%FOUND` | `ORA-01001` | `NULL` | `TRUE` | `FALSE` | `ORA-01001` |
| `%NOTFOUND` | `ORA-01001` | `NULL` | `FALSE` | `TRUE` | `ORA-01001` |
| `%ROWCOUNT` | `ORA-01001` | `0` | n.º de files llegides | n.º de files llegides | `ORA-01001` |

> [!CAUTION]
> Dos errors clàssics: (1) posar l'`EXIT WHEN c%NOTFOUND` **després** d'usar les variables. L'últim `FETCH`, el que no troba fila, **no canvia les variables**, i l'última fila es processaria dues vegades. (2) Oblidar el `CLOSE`: el cursor queda obert fins al final de la sessió i, en un bucle que l'obri una vegada i una altra, s'arriba al límit `OPEN_CURSORS` (`ORA-01000`).

### 7.3 Cursor `FOR`: la forma habitual

El bucle `FOR` de cursor **fa els quatre passos per tu**: obri el cursor, llig fila a fila, declara el registre i tanca el cursor en acabar, fins i tot si se n'ix per una excepció. És més curt, més segur i s'ha de preferir tret que calga el control fi del cursor explícit.

```sql
BEGIN
    FOR r IN (SELECT g.cod_grupo, COUNT(a.id_alumno) AS alumnos
              FROM   grupo g
                     LEFT JOIN alumno a ON a.cod_grupo = g.cod_grupo
              GROUP  BY g.cod_grupo
              ORDER  BY g.cod_grupo) LOOP
        DBMS_OUTPUT.PUT_LINE(RPAD(r.cod_grupo, 7) || LPAD(r.alumnos, 2) || ' alumnos');
    END LOOP;
END;
/
```

```text
1ASIR   5 alumnos
1DAM    7 alumnos
1DAW    6 alumnos
2ASIR   0 alumnos
2DAM    6 alumnos
2DAW    5 alumnos
```

Compara amb l'apartat anterior: ja no hi ha `OPEN`, `FETCH`, `CLOSE`, ni variables que declarar, ni `EXIT WHEN`. El registre `r` té un camp per cada columna del `SELECT` (`r.cod_grupo`, `r.alumnos`) i **només existix dins del bucle**. Observa també que el `LEFT JOIN` conserva el grup 2ASIR, que no té alumnat (UD07).

Si la consulta és llarga o es reutilitza, pot declarar-se amb nom i usar-se en el `FOR`:

```sql
DECLARE
    CURSOR c_grupos IS SELECT cod_grupo, turno FROM grupo ORDER BY cod_grupo;
BEGIN
    FOR r IN c_grupos LOOP
        DBMS_OUTPUT.PUT_LINE(r.cod_grupo || ' · ' || r.turno);
    END LOOP;
END;
/
```

### 7.4 Cursors amb paràmetres

Un cursor pot rebre paràmetres per a reutilitzar la mateixa consulta amb valors distints. Els paràmetres es declaren **sense longitud** i es passen en obrir el cursor:

```sql
DECLARE
    CURSOR c_modulos (p_ciclo  modulo.cod_ciclo%TYPE,
                      p_curso  modulo.curso%TYPE) IS
        SELECT codigo, nombre, horas
        FROM   modulo
        WHERE  cod_ciclo = p_ciclo AND curso = p_curso
        ORDER  BY codigo;
    v_total  PLS_INTEGER := 0;
BEGIN
    DBMS_OUTPUT.PUT_LINE('Módulos de DAW · segundo curso');
    FOR r IN c_modulos('DAW', 2) LOOP
        DBMS_OUTPUT.PUT_LINE(r.codigo || '  ' || RPAD(r.nombre, 36) || LPAD(r.horas, 4) || ' h');
        v_total := v_total + r.horas;
    END LOOP;
    DBMS_OUTPUT.PUT_LINE('Total: ' || v_total || ' h');
END;
/
```

```text
Módulos de DAW · segundo curso
0612  Desarrollo web en entorno cliente     140 h
0613  Desarrollo web en entorno servidor    160 h
0614  Despliegue de aplicaciones web         80 h
0615  Diseño de interfaces web              120 h
Total: 500 h
```

Amb un cursor explícit s'escriuria `OPEN c_modulos('DAW', 2);`. Dins de la consulta, el paràmetre s'usa com qualsevol valor; el prefix `p_` evita que es confonga amb una columna.

### 7.5 `FOR UPDATE`, `WHERE CURRENT OF` y `REF CURSOR`

Quan el recorregut va a **modificar** les files que llig, es bloquegen amb `FOR UPDATE` (bloqueig pessimista, UD08 §8.5) i s'actualitza la fila actual amb `WHERE CURRENT OF`:

```sql
-- Exemple de sintaxi: puja 0,25 punts a les notes del mòdul 16 (amb topall 10)
DECLARE
    CURSOR c_notas IS
        SELECT id_matricula, nota_final
        FROM   matricula
        WHERE  id_modulo = 16 AND nota_final IS NOT NULL
        FOR UPDATE OF nota_final;
BEGIN
    FOR r IN c_notas LOOP
        UPDATE matricula
        SET    nota_final = LEAST(r.nota_final + 0.25, 10)
        WHERE CURRENT OF c_notas;
    END LOOP;
    ROLLBACK;                                      -- és només una demostració
END;
/
```

Un **`REF CURSOR`** (`SYS_REFCURSOR`) és un cursor la consulta del qual es decidix en execució i que es pot **tornar** a qui crida. És el mecanisme per a lliurar un resultat a una aplicació:

```sql
CREATE OR REPLACE FUNCTION fn_alumnos_grupo (p_cod_grupo IN grupo.cod_grupo%TYPE)
RETURN SYS_REFCURSOR
IS
    c_res  SYS_REFCURSOR;
BEGIN
    OPEN c_res FOR
        SELECT nia, apellidos, nombre
        FROM   alumno
        WHERE  cod_grupo = p_cod_grupo
        ORDER  BY apellidos;
    RETURN c_res;                  -- qui crida és responsable de llegir-lo i tancar-lo
END fn_alumnos_grupo;
/
```

### 7.6 Laboratori: depurar blocs pas a pas

El depurador següent reprodueix, línia a línia, tres dels blocs d'esta unitat sobre dades reals d'EduGest. Mostra la **línia en execució**, el valor de cada **variable** (ressaltada quan canvia) i el contingut del **búfer de `DBMS_OUTPUT`**. Les traces estan precalculades: és una simulació didàctica, no un intèrpret de PL/SQL.

{{< plsql-trace >}}

**Experiment 1 · Una consulta, tres desenllaços.** Tria el bloc «`SELECT … INTO` i la secció `EXCEPTION`» i executa'l amb les seues tres entrades:

1. Amb el NIA `10450740` avança fins al final. Comprova que `INTO` copia els dos valors i que la secció `EXCEPTION` **no** arriba a executar-se.
2. Amb `10459999` (un NIA que no existix) observa a quina línia salta l'execució quan la consulta no torna files, i què valen aleshores `v_nia` i `v_nombre`.
3. Amb `104507%` la consulta coincidix amb tres alumnes. Fixa't que Oracle no assigna **ni tan sols la primera fila**, i que se salta el manejador de `NO_DATA_FOUND`.

{{% details title="Què hauries d'haver observat" %}}
Sense files es llança `NO_DATA_FOUND`, l'execució abandona el cos del bloc i se salta al manejador; les dues variables continuen a `NULL` perquè `INTO` no va arribar a assignar res. Amb tres files es llança `TOO_MANY_ROWS` i tampoc s'assigna res. En els dos casos el bloc acaba sense error **perquè l'excepció es tracta**; si s'eliminara la secció `EXCEPTION`, l'error arribaria al client (`ORA-01403` o `ORA-01422`) i el bloc haguera fallat.
{{% /details %}}

**Experiment 2 · Quan s'assabenta el cursor que no queden files?** Canvia al bloc «Cursor explícit: `OPEN`, `FETCH`, `CLOSE`» i avança pas a pas fins al cinqué `FETCH`:

1. Després d'`OPEN`, quant valen `%ROWCOUNT` i `%NOTFOUND`? S'ha llegit ja alguna fila?
2. En el cinqué `FETCH`, observa què li passa a `%NOTFOUND`, a `%ROWCOUNT` i a `v_codigo`/`v_nota`.
3. Canvia ara al bloc 1 («Bucle `FOR`») i compara'l: quines instruccions del cursor explícit han desaparegut i qui les fa?

{{% details title="Què hauries d'haver observat" %}}
Després d'`OPEN`, `%ROWCOUNT` és 0 i `%NOTFOUND` és `NULL`: el cursor està abans de la primera fila i no ha llegit res. El cinqué `FETCH` no troba fila: `%NOTFOUND` passa a `TRUE`, `%ROWCOUNT` es queda en 4 i les variables **conserven** els valors de l'última fila (0615 i 9,25). Si l'`EXIT WHEN` estiguera després del `PUT_LINE`, eixa última fila s'escriuria dues vegades. En el bloc `FOR` desapareixen `OPEN`, `FETCH`, `CLOSE` i la declaració de variables: les fa el mateix bucle.
{{% /details %}}

### 7.7 Quan no usar un cursor

Un cursor processa **fila a fila**, i cada volta costa un canvi de context entre el motor PL/SQL i el motor SQL. Si la tasca es pot escriure com una sola sentència, el motor SQL la fa en conjunt i molt més ràpid:

```sql
-- Lent i llarg: una sentència UPDATE per cada fila
BEGIN
    FOR r IN (SELECT id_falta FROM falta_asistencia
              WHERE justificada = 'N' AND fecha < DATE '2025-11-01') LOOP
        UPDATE falta_asistencia SET justificada = 'S' WHERE id_falta = r.id_falta;
    END LOOP;
END;
/

-- Millor: una sola sentència SQL que fa el mateix
UPDATE falta_asistencia
SET    justificada = 'S'
WHERE  justificada = 'N' AND fecha < DATE '2025-11-01';
```

> [!TIP]
> Un cursor és l'eina adequada quan, **per a cada fila, cal fer alguna cosa que SQL no pot fer en conjunt**: escriure un informe, cridar a un procediment, aplicar una lògica amb diverses decisions, tractar cada fila amb el seu propi control d'errors. Quan de debò cal processar moltes files amb PL/SQL, `BULK COLLECT` llig un lot de colp en una col·lecció i `FORALL` envia totes les seues modificacions al motor SQL en una sola crida; són optimitzacions que convé conéixer, no un punt de partida.

{{< quiz >}}
- q: "En llegir un cursor explícit en un bucle, l'`EXIT WHEN c%NOTFOUND;` s'escriu…"
  options: ["Abans del `FETCH`", "Immediatament després del `FETCH`, abans d'usar les variables", "Després d'usar les variables", "Dins de la secció `EXCEPTION`"]
  answer: 1
  explain: "El `FETCH` que no troba fila no canvia les variables. Si s'usen abans de comprovar `%NOTFOUND`, l'última fila es processa dues vegades."
- q: "Quina diferència hi ha entre un cursor explícit i un cursor `FOR`?"
  options: ["El cursor `FOR` no pot tindre paràmetres", "El cursor `FOR` obri, llig, declara el registre i tanca per si mateix", "El cursor explícit no admet `ORDER BY`", "No n'hi ha cap: són sinònims"]
  answer: 1
  explain: "El bucle `FOR` fa `OPEN`, `FETCH`, `CLOSE` i la declaració del registre automàticament, fins i tot si el bucle acaba per una excepció. Tots dos admeten paràmetres i qualsevol consulta."
- q: "Després d'`UPDATE matricula SET nota_final = 5 WHERE id_alumno = 999;` (no existix eixe alumne), què passa?"
  options: ["`NO_DATA_FOUND`", "`TOO_MANY_ROWS`", "No hi ha error: `SQL%ROWCOUNT` val 0 i `SQL%NOTFOUND` és `TRUE`", "`ORA-02291`"]
  answer: 2
  explain: "Un `UPDATE` o `DELETE` que no troba files és una operació correcta que n'afecta zero. Només `SELECT ... INTO` llança `NO_DATA_FOUND`."
- q: "Cal pujar un punt la nota de les 5 000 matrícules d'un mòdul. Quina és la millor solució?"
  options: ["Un cursor `FOR` amb un `UPDATE` per fila", "Un bucle `WHILE` amb `SELECT INTO`", "Una única sentència `UPDATE ... SET nota_final = nota_final + 1 WHERE ...`", "Un `REF CURSOR`"]
  answer: 2
  explain: "Si la tasca es pot expressar com una sola sentència SQL, el motor SQL l'executa en conjunt, sense canvis de context per fila. El cursor es reserva per a allò que SQL no pot fer en conjunt."
{{< /quiz >}}

---

## 8. Funcions d'usuari

### 8.1 Què és una funció i quan crear-la

Una **funció d'usuari** és un subprograma emmagatzemat en la base de dades que **rep paràmetres i torna un únic valor**. El criteri RA5.f demana definir-les. Es crea una funció quan hi ha un càlcul que es repetix i que es vol escriure **una sola vegada**: la qualificació en text d'una nota, l'edat a partir d'una data, la mitjana d'un alumne.

El seu gran avantatge sobre un procediment és que **es pot usar dins d'una consulta SQL**, com qualsevol funció del gestor:

```sql
SELECT nia, fn_edad(fecha_nacimiento) FROM alumno WHERE cod_grupo = '2DAW';
```

### 8.2 Sintaxi

```text
CREATE [OR REPLACE] FUNCTION nombre
    [(parámetro [IN] tipo [DEFAULT valor], ...)]
RETURN tipo_devuelto
[DETERMINISTIC]
IS | AS
    -- declaracions locals
BEGIN
    ...
    RETURN valor;
[EXCEPTION
    ...]
END [nombre];
```

| Element | Significat |
|---|---|
| `CREATE OR REPLACE` | Crea la funció o, si ja existix, la **substituïx conservant els seus privilegis**. És la forma de recompilar sense perdre els `GRANT` |
| `parámetro [IN] tipo` | Paràmetres d'entrada. **Sense longitud** en el tipus: `VARCHAR2`, no `VARCHAR2(20)`. En una funció es recomana usar només `IN` |
| `RETURN tipo` | Tipus del valor tornat (en la capçalera, sense longitud) |
| `DETERMINISTIC` | Promet que amb els mateixos arguments torna sempre el mateix valor; l'optimitzador pot reutilitzar resultats. Només si és cert |
| `RETURN valor;` | Instrucció que torna el valor i **acaba** la funció. S'ha d'executar en tots els camins |
| `IS` / `AS` | Equivalents: separen la capçalera de les declaracions |

### 8.3 Dues funcions d'EduGest: `fn_calificacion` i `fn_edad`

La primera convertix una nota en la seua qualificació en text. És la regla que ja vam vore en la vista `v_acta` (UD07), ara escrita **una sola vegada**:

{{< sgbd "Oracle 26ai" >}}

```sql
CREATE OR REPLACE FUNCTION fn_calificacion (p_nota IN NUMBER)
RETURN VARCHAR2
DETERMINISTIC
IS
BEGIN
    RETURN CASE
               WHEN p_nota IS NULL THEN 'NC'
               WHEN p_nota < 5     THEN 'Insuficiente'
               WHEN p_nota < 6     THEN 'Suficiente'
               WHEN p_nota < 7     THEN 'Bien'
               WHEN p_nota < 9     THEN 'Notable'
               ELSE                     'Sobresaliente'
           END;
END fn_calificacion;
/
```

La segona calcula els anys complits. Té un paràmetre amb valor per defecte: si no s'indica la data de referència, usa la d'hui.

```sql
CREATE OR REPLACE FUNCTION fn_edad (
    p_fecha_nacimiento  IN DATE,
    p_fecha_ref         IN DATE DEFAULT SYSDATE
) RETURN NUMBER
IS
BEGIN
    IF p_fecha_nacimiento IS NULL THEN
        RETURN NULL;
    END IF;
    RETURN TRUNC(MONTHS_BETWEEN(p_fecha_ref, p_fecha_nacimiento) / 12);
END fn_edad;
/
```

Si tot va bé, SQLcl respon `Function FN_CALIFICACION compiled`. Si hi ha errors de compilació, els mostra amb `SHOW ERRORS` (§2.5).

### 8.4 Usar una funció

Des de **SQL**, en el `SELECT`, el `WHERE` o l'`ORDER BY`:

```sql
SELECT a.nia,
       fn_edad(a.fecha_nacimiento, DATE '2026-10-06')  AS edad,
       ROUND(AVG(m.nota_final), 2)                      AS media,
       fn_calificacion(ROUND(AVG(m.nota_final), 2))     AS calificacion
FROM   alumno a
       JOIN matricula m ON m.id_alumno = a.id_alumno
WHERE  a.cod_grupo = '2DAW'
GROUP  BY a.nia, a.fecha_nacimiento
ORDER  BY a.nia;
```

| NIA | EDAD | MEDIA | CALIFICACION |
|---|---|---|---|
| 10450740 | 23 | 7.13 | Notable |
| 10450777 | 21 | 5.44 | Suficiente |
| 10450814 | 22 | 5.56 | Suficiente |
| 10450851 | 26 | 5.42 | Suficiente |
| 10450888 | 21 | 6 | Bien |

*5 files*

Des de **PL/SQL**, en una assignació o una expressió:

```sql
DECLARE
    v_nota  NUMBER := 9.25;
BEGIN
    DBMS_OUTPUT.PUT_LINE(v_nota || ' = ' || fn_calificacion(v_nota));
    DBMS_OUTPUT.PUT_LINE('Edad de Mateo en 2027: ' ||
                         fn_edad(DATE '2003-04-09', DATE '2027-04-09'));
END;
/
```

```text
9.25 = Sobresaliente
Edad de Mateo en 2027: 24
```

Els arguments es poden passar per **posició** (en l'ordre de la declaració) o per **nom** amb `=>`, que permet saltar-se els opcionals i millora la llegibilitat:

```sql
SELECT fn_edad(p_fecha_ref => DATE '2026-10-06',
               p_fecha_nacimiento => DATE '2003-04-09') AS edad
FROM   dual;
```

### 8.5 Una funció amb consulta: `fn_nombre_modulo`

Una funció pot llegir de les taules. Esta torna el nom d'un mòdul, o `NULL` si no existix, en lloc de propagar l'error al qui crida:

```sql
CREATE OR REPLACE FUNCTION fn_nombre_modulo (p_id_modulo IN modulo.id_modulo%TYPE)
RETURN modulo.nombre%TYPE
IS
    v_nombre  modulo.nombre%TYPE;
BEGIN
    SELECT nombre INTO v_nombre FROM modulo WHERE id_modulo = p_id_modulo;
    RETURN v_nombre;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN NULL;                       -- decisió de disseny: «no existix» no és un error
END fn_nombre_modulo;
/
```

```sql
SELECT fn_nombre_modulo(2) AS existe, fn_nombre_modulo(999) AS no_existe FROM dual;
```

| EXISTE | NO_EXISTE |
|---|---|
| Bases de datos | *(null)* |

*1 fila*

> [!NOTE]
> Decidir què fa una funció quan no troba la dada és una **decisió de disseny** que has de documentar: tornar `NULL` (còmode en una consulta) o llançar un error (obliga el qui crida a tractar-lo). En la pràctica 9.2, `fn_nombre_completo` torna `NULL`; en el procediment de matrícula (§10.5), un alumne inexistent és un error.

### 8.6 Restriccions de les funcions cridades des de SQL

Una funció que s'executa dins d'un `SELECT` està subjecta a regles, perquè Oracle ha de poder avaluar-la moltes vegades i en l'ordre que més li convinga:

| Regla | Si s'incompleix |
|---|---|
| No pot fer `INSERT`, `UPDATE` ni `DELETE` (en una consulta) | `ORA-14551: cannot perform a DML operation inside a query` |
| No pot fer `COMMIT`, `ROLLBACK` ni canviar la sessió | `ORA-14552: cannot perform a DDL, commit or rollback inside a query or DML` |
| No hauria de dependre de dades que canvien durant la mateixa sentència | Resultats impredictibles o `ORA-04091` si llig la taula que es modifica |
| Cada crida és un canvi de context entre el motor SQL i el motor PL/SQL | Una funció cridada 500 000 vegades en un `SELECT` pot ser lenta: si és possible, expressa el càlcul en SQL |

> [!TIP]
> Marca amb `DETERMINISTIC` les funcions pures com `fn_calificacion`; així Oracle pot reutilitzar el resultat per a arguments repetits i, a més, és requisit per a usar-les en un índex basat en funcions.

### 8.7 Gestionar les funcions

```sql
-- Quines funcions tinc i en quin estat estan?
SELECT object_name, status FROM user_objects WHERE object_type = 'FUNCTION' ORDER BY object_name;

-- Veure el codi font emmagatzemat
SELECT text FROM user_source WHERE name = 'FN_EDAD' ORDER BY line;

-- Eliminar-la
DROP FUNCTION fn_edad;
```

Si una funció depén d'una taula i esta canvia (per exemple, `ALTER TABLE`), Oracle la marca `INVALID` i la recompila sola en el pròxim ús; per a forçar-ho: `ALTER FUNCTION fn_edad COMPILE;`.


---

{{< sesion n="5" h="1" tipo="t" >}}Excepcions i procediments emmagatzemats{{< /sesion >}}

## 9. Excepcions

### 9.1 Què és una excepció

Una **excepció** és un error que ocorre durant l'execució d'un bloc. Quan es produïx, el flux normal s'**interromp**: Oracle abandona les instruccions restants de la secció `BEGIN` i busca un **manejador** en la secció `EXCEPTION`.

```text
BEGIN
    instrucció 1;          ← s'executa
    instrucció 2;          ← error! es llança una excepció
    instrucció 3;          ← NO s'executa
EXCEPTION
    WHEN una_excepcion THEN ← Oracle busca ací, de dalt a baix, el primer WHEN que coincidisca
        tractament;
    WHEN OTHERS THEN        ← comodí: qualsevol altra excepció
        tractament;
END;
```

| Situació | Resultat |
|---|---|
| Hi ha un manejador que coincidix | S'executa el seu codi i el bloc **acaba normalment** (com si no haguera passat res, excepte el que faça el manejador) |
| No hi ha manejador en este bloc | L'excepció **es propaga** al bloc exterior, i així successivament |
| Cap bloc la tracta | L'error arriba al client: `ORA-xxxxx` |

El criteri RA5.j demana utilitzar excepcions. N'hi ha tres classes:

| Classe | Qui la llança | Exemple |
|---|---|---|
| **Predefinida** | Oracle, amb nom ja assignat | `NO_DATA_FOUND`, `ZERO_DIVIDE` |
| **Oracle sense nom** | Oracle, amb codi `ORA-` però sense nom en el llenguatge | `ORA-02292` (esborrar un pare amb fills) |
| **Definida per l'usuari** | El programador, amb `RAISE` o `RAISE_APPLICATION_ERROR` | «L'alumne no té grup» |

### 9.2 Excepcions predefinides

| Excepció | Codi | Es llança quan… |
|---|---|---|
| `NO_DATA_FOUND` | `ORA-01403` | Un `SELECT ... INTO` no torna files |
| `TOO_MANY_ROWS` | `ORA-01422` | Un `SELECT ... INTO` torna més d'una fila |
| `DUP_VAL_ON_INDEX` | `ORA-00001` | Es viola una clau primària o una restricció `UNIQUE` |
| `ZERO_DIVIDE` | `ORA-01476` | Divisió per zero |
| `INVALID_NUMBER` | `ORA-01722` | Conversió de text a nombre impossible dins d'una sentència SQL |
| `VALUE_ERROR` | `ORA-06502` | Error de conversió o de mida en una assignació PL/SQL (`VARCHAR2(3) := 'Sala'`) |
| `CURSOR_ALREADY_OPEN` | `ORA-06511` | S'obri un cursor que ja està obert |
| `INVALID_CURSOR` | `ORA-01001` | Operació no permesa sobre un cursor (llegir-ne un de tancat) |
| `CASE_NOT_FOUND` | `ORA-06592` | Cap branca d'un `CASE` sense `ELSE` |
| `OTHERS` | qualsevol | Comodí: atrapa tot el que no s'haja tractat abans |

Un bloc que calcula les hores de falta per alumne d'un grup. El grup 2ASIR existix, però **no té alumnat**:

```sql
DECLARE
    v_alumnos  PLS_INTEGER;
    v_horas    PLS_INTEGER;
    v_media    NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_alumnos FROM alumno WHERE cod_grupo = '2ASIR';

    SELECT NVL(SUM(f.horas), 0)
    INTO   v_horas
    FROM   falta_asistencia f
           JOIN matricula m ON m.id_matricula = f.id_matricula
           JOIN alumno a    ON a.id_alumno    = m.id_alumno
    WHERE  a.cod_grupo = '2ASIR';

    v_media := v_horas / v_alumnos;                             -- 0 / 0 → ZERO_DIVIDE
    DBMS_OUTPUT.PUT_LINE('Horas de falta por alumno: ' || v_media);
EXCEPTION
    WHEN ZERO_DIVIDE THEN
        DBMS_OUTPUT.PUT_LINE('2ASIR no tiene alumnado: no se puede calcular la media');
END;
/
```

```text
2ASIR no tiene alumnado: no se puede calcular la media
```

I un `INSERT` que viola la clau primària de `CICLO`:

```sql
BEGIN
    INSERT INTO ciclo (cod_ciclo, nombre, grado, horas_totales)
    VALUES ('DAW', 'Desarrollo de Aplicaciones Web', 'SUPERIOR', 2000);
EXCEPTION
    WHEN DUP_VAL_ON_INDEX THEN
        DBMS_OUTPUT.PUT_LINE('El ciclo DAW ya existe');
END;
/
```

```text
El ciclo DAW ya existe
```

El cas de `NO_DATA_FOUND` i `TOO_MANY_ROWS` el tens pas a pas en el laboratori de l'apartat 7.6.

### 9.3 `OTHERS`, `SQLCODE` y `SQLERRM`

Dins d'un manejador, dues funcions descriuen l'error que s'està tractant:

| Funció | Torna |
|---|---|
| `SQLCODE` | Número de l'error. Negatiu per als `ORA-` (`-1476`); `+100` per a `NO_DATA_FOUND`; el de `RAISE_APPLICATION_ERROR` (`-20010`) |
| `SQLERRM` | Text complet amb el prefix: `ORA-01476: divisor is equal to zero` |

```sql
DECLARE
    v_cero  NUMBER := 0;
BEGIN
    DBMS_OUTPUT.PUT_LINE(10 / v_cero);
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('SQLCODE = ' || SQLCODE);
        DBMS_OUTPUT.PUT_LINE('SQLERRM = ' || SQLERRM);
END;
/
```

```text
SQLCODE = -1476
SQLERRM = ORA-01476: divisor is equal to zero
```

> [!CAUTION]
> **`WHEN OTHERS THEN NULL;` és el pitjor codi que es pot escriure en PL/SQL.** Es traga qualsevol error, fins i tot un d'inesperat, i deixa la base de dades en un estat incert sense deixar rastre. Un manejador `OTHERS` només és acceptable si **registra** l'error i el **torna a llançar** amb `RAISE;`:
>
> ```sql
> EXCEPTION
>     WHEN OTHERS THEN
>         DBMS_OUTPUT.PUT_LINE('Error ' || SQLCODE || ': ' || SQLERRM);   -- o, millor, a una taula de registre
>         RAISE;                                                          -- el MATEIX error continua el seu camí
> ```

`SQLERRM` està limitat a 512 bytes i no inclou *on* ha ocorregut l'error. Per a depurar, `DBMS_UTILITY.FORMAT_ERROR_STACK` torna la pila completa i `DBMS_UTILITY.FORMAT_ERROR_BACKTRACE` indica els números de línia de cada subprograma pel qual ha passat.

### 9.4 Excepcions definides per l'usuari

Quan l'«anomalia» és de negoci i no del gestor, es declara una excepció pròpia en la secció `DECLARE`, es llança amb `RAISE` i es tracta com les altres:

```sql
DECLARE
    e_sin_notas  EXCEPTION;                     -- 1. es declara
    v_notas      PLS_INTEGER;
BEGIN
    SELECT COUNT(nota_final) INTO v_notas FROM matricula WHERE id_alumno = 30;

    IF v_notas = 0 THEN
        RAISE e_sin_notas;                      -- 2. es llança
    END IF;
    DBMS_OUTPUT.PUT_LINE('El alumno 30 tiene ' || v_notas || ' notas');
EXCEPTION
    WHEN e_sin_notas THEN                       -- 3. es tracta
        DBMS_OUTPUT.PUT_LINE('El alumno 30 no tiene ninguna nota');
END;
/
```

```text
El alumno 30 no tiene ninguna nota
```

Una excepció declarada així només existix dins del seu bloc. Si no es tracta, en arribar al client es mostra com `ORA-06510: PL/SQL: unhandled user-defined exception`, un missatge que no ajuda ningú: per això, per a errors que han d'arribar a l'aplicació, es prefereix `RAISE_APPLICATION_ERROR` (§9.6).

### 9.5 `PRAGMA EXCEPTION_INIT`: posar-li nom a un error d'Oracle

Hi ha molts errors `ORA-` que no tenen nom predefinit. `PRAGMA EXCEPTION_INIT` associa un nom propi a un codi, per a poder tractar-lo en un `WHEN`. Un cas típic d'EduGest: esborrar un professor que encara imparteix mòduls (`ORA-02292`, clau aliena sense `ON DELETE`):

```sql
DECLARE
    e_tiene_hijos  EXCEPTION;
    PRAGMA EXCEPTION_INIT(e_tiene_hijos, -2292);        -- ORA-02292: child record found
BEGIN
    DELETE FROM profesor WHERE id_profesor = 105;
    DBMS_OUTPUT.PUT_LINE('Profesor borrado');
EXCEPTION
    WHEN e_tiene_hijos THEN
        DBMS_OUTPUT.PUT_LINE('No se puede borrar al profesor 105: imparte módulos (tabla IMPARTE)');
END;
/
```

```text
No se puede borrar al profesor 105: imparte módulos (tabla IMPARTE)
```

El segon argument és el codi **amb signe negatiu** (`-2292`, no `2292`). Altres codis que s'associen amb freqüència:

| Codi | Significat | Nom habitual |
|---|---|---|
| `-2291` | `ORA-02291`: *parent key not found* (la clau aliena apunta a una fila que no existix) | `e_padre_no_existe` |
| `-2292` | `ORA-02292`: *child record found* (s'esborra un pare amb fills) | `e_tiene_hijos` |
| `-1400` | `ORA-01400`: no es pot inserir `NULL` en una columna `NOT NULL` | `e_nulo_no_permitido` |
| `-2290` | `ORA-02290`: es viola una restricció `CHECK` | `e_check` |
| `-54` | `ORA-00054`: recurs ocupat (`FOR UPDATE NOWAIT`, UD08) | `e_ocupado` |

### 9.6 `RAISE_APPLICATION_ERROR`: errors de negoci cap al client

`RAISE_APPLICATION_ERROR(código, mensaje)` detén el subprograma i torna al qui crida un error amb el **codi** i el **missatge** que tu decidisques. És la forma estàndard de comunicar a una aplicació que s'ha incomplit una regla de negoci.

```sql
BEGIN
    RAISE_APPLICATION_ERROR(-20010, 'El módulo 12 no pertenece al ciclo del alumno');
END;
/
```

```text
ORA-20010: El módulo 12 no pertenece al ciclo del alumno
ORA-06512: at line 2
```

| Regla | Detall |
|---|---|
| Codi | Entre **-20000 i -20999**: el rang que Oracle reserva a les aplicacions |
| Missatge | Fins a 2048 bytes; ha de dir **què** ha fallat i amb **quines dades** |
| Efecte | L'excepció es propaga; si ningú la tracta, la sentència que va invocar el codi es desfà |
| Des d'un disparador | Avorta la sentència DML que el va disparar (§11) |

> [!TIP]
> Reserva un **catàleg de codis** per al projecte i documenta'l, igual que una taula d'errors HTTP. Així l'aplicació pot reaccionar al codi (`-20013` → «ja estàs matriculat») i no analitzar el text. EduGest usa:
>
> | Codi | Significat | On |
> |---|---|---|
> | `-20010` | El mòdul no és del cicle de l'alumne (R2) | `pr_matricular` |
> | `-20011` | Convocatòries esgotades (màxim 4) | `pr_matricular` |
> | `-20012` | Alumne o mòdul inexistent, o alumne sense grup | `pr_matricular` |
> | `-20013` | Alumne ja matriculat del mòdul en eixe curs | `pr_matricular` |
> | `-20020` | El cap no pertany al departament (R1) | `trg_jefe_departamento` |
> | `-20021` | Professor cap que canvia de departament (R1) | `trg_profesor_cambio_dpto` |
> | `-20022` | Falta anterior a la data de matrícula (R3) | `trg_falta_fecha` |
> | `-20030` | Un professor supera les 20 hores setmanals (R4) | `trg_imparte_max_horas` |
> | `-20040` | Un grup supera els 30 alumnes (R5) | `trg_grupo_max_alumnos` |

### 9.7 Blocs aniuats: limitar l'abast d'un error

Un `SELECT ... INTO` que no troba dades enmig d'un bucle avorta **tot** el bucle. Si el que es vol és tractar el cas i **continuar amb la fila següent**, la solució és embolicar la part arriscada en el seu propi bloc:

```sql
DECLARE
    TYPE t_ids IS TABLE OF PLS_INTEGER;
    v_ids     t_ids := t_ids(20, 999, 30);
    v_nombre  VARCHAR2(130);
BEGIN
    FOR i IN 1..v_ids.COUNT LOOP
        BEGIN                                              -- bloc interior, un per volta
            SELECT apellidos || ', ' || nombre
            INTO   v_nombre
            FROM   alumno
            WHERE  id_alumno = v_ids(i);
            DBMS_OUTPUT.PUT_LINE(v_ids(i) || ': ' || v_nombre);
        EXCEPTION
            WHEN NO_DATA_FOUND THEN
                DBMS_OUTPUT.PUT_LINE(v_ids(i) || ': no existe');
        END;
    END LOOP;
END;
/
```

```text
20: Sala Brotons, Mateo
999: no existe
30: Iborra Valero, Zoe
```

Dues particularitats que sorprenen:

1. **Una excepció en la secció `DECLARE` no la tracta el manejador del mateix bloc**, sinó el del bloc exterior. Amb `v_corto VARCHAR2(3) := 'Sala';` el bloc falla amb `ORA-06502` encara que tinga un `WHEN VALUE_ERROR`: encara no havia començat a executar-se.
2. **Una excepció dins d'un manejador** tampoc la tracta el mateix bloc: puja a l'exterior.

### 9.8 Excepcions i transaccions

Un error **no** fa `ROLLBACK` de la transacció. El que ocorre depén de si es tracta o no:

| Situació | Què passa amb els canvis |
|---|---|
| L'excepció **no es tracta** i arriba al client | Oracle desfà els canvis de **la crida que ha fallat** (atomicitat de sentència, UD08). El que s'havia fet abans en la transacció roman, sense confirmar |
| L'excepció **es tracta** i el bloc acaba | **No es desfà res.** El que el bloc ja havia fet abans de l'error es queda fet |
| Cal desfer només una part | `SAVEPOINT` al principi i `ROLLBACK TO SAVEPOINT` en el manejador |

```sql
BEGIN
    SAVEPOINT antes_de_borrar;
    DELETE FROM falta_asistencia WHERE id_matricula = 10060;
    DELETE FROM profesor WHERE id_profesor = 105;          -- ORA-02292
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK TO antes_de_borrar;                        -- desfà també el primer DELETE
        RAISE;
END;
/
```

> [!IMPORTANT]
> No depengues del comportament implícit. Un subprograma que fa diverses modificacions i tracta els seus propis errors ha de decidir **explícitament** què es conserva i què es desfà, i qui el crida ho ha de saber. En la pràctica 9.8 el paquet de secretaria usa exactament esta tècnica.

---

## 10. Procediments emmagatzemats

### 10.1 Què és un procediment

Un **procediment emmagatzemat** és un subprograma amb nom, guardat i compilat en la base de dades, que **realitza una acció** i no torna valor (la informació d'eixida viatja pels paràmetres `OUT`). S'invoca des d'un client, des d'un altre subprograma o des d'una tasca programada.

```text
CREATE [OR REPLACE] PROCEDURE nombre
    [(parámetro [IN | OUT | IN OUT] tipo [DEFAULT valor], ...)]
[AUTHID DEFINER | CURRENT_USER]
IS | AS
    -- declaracions locals
BEGIN
    -- instruccions
[EXCEPTION
    -- manejadors]
END [nombre];
```

L'estructura és la del bloc anònim, amb la capçalera `CREATE PROCEDURE` en lloc de `DECLARE`: les declaracions locals s'escriuen **entre `IS` i `BEGIN`**, sense la paraula `DECLARE`.

| Funció | Procediment |
|---|---|
| Torna **un valor** amb `RETURN` | No torna valor |
| Es pot usar **dins d'un `SELECT`** | S'invoca amb `EXEC`, `CALL` o des d'un altre bloc |
| Calcula | **Fa**: inserix, modifica, valida, registra |
| Paràmetres normalment només `IN` | Paràmetres `IN`, `OUT` i `IN OUT` |

### 10.2 Paràmetres `IN`, `OUT` i `IN OUT`

| Mode | Direcció | Dins del procediment | En cridar es passa |
|---|---|---|---|
| `IN` (per defecte) | Entrada | Només lectura | Un valor, una variable o una expressió |
| `OUT` | Eixida | Comença a `NULL`; se li assigna un valor | **Una variable** que rebrà el resultat |
| `IN OUT` | Entrada i eixida | Es llig i es modifica | **Una variable** amb valor inicial |

Un procediment que torna dades d'un mòdul mitjançant paràmetres `OUT`:

```sql
CREATE OR REPLACE PROCEDURE pr_datos_modulo (
    p_id_modulo  IN  modulo.id_modulo%TYPE,
    p_codigo     OUT modulo.codigo%TYPE,
    p_nombre     OUT modulo.nombre%TYPE,
    p_horas      OUT modulo.horas%TYPE
)
IS
BEGIN
    SELECT codigo, nombre, horas
    INTO   p_codigo, p_nombre, p_horas
    FROM   modulo
    WHERE  id_modulo = p_id_modulo;
END pr_datos_modulo;
/
```

Per a cridar-lo fa falta una variable per cada paràmetre `OUT`:

```sql
DECLARE
    v_codigo  modulo.codigo%TYPE;
    v_nombre  modulo.nombre%TYPE;
    v_horas   modulo.horas%TYPE;
BEGIN
    pr_datos_modulo(2, v_codigo, v_nombre, v_horas);               -- notació posicional
    DBMS_OUTPUT.PUT_LINE(v_codigo || ' ' || v_nombre || ': ' || v_horas || ' h');
END;
/
```

```text
0484 Bases de datos: 160 h
```

Un paràmetre `IN OUT` entra amb un valor i ix transformat:

```sql
CREATE OR REPLACE PROCEDURE pr_normalizar_nombre (p_texto IN OUT VARCHAR2)
IS
BEGIN
    p_texto := INITCAP(TRIM(p_texto));
END pr_normalizar_nombre;
/

DECLARE
    v_nombre  VARCHAR2(40) := '  mateo SALA  ';
BEGIN
    pr_normalizar_nombre(v_nombre);
    DBMS_OUTPUT.PUT_LINE('[' || v_nombre || ']');
END;
/
```

```text
[Mateo Sala]
```

**Notació posicional i nomenada.** Els arguments es poden passar en l'ordre de la declaració o per nom amb `=>`; esta segona és més llegible i permet ometre els paràmetres amb `DEFAULT`:

```sql
pr_datos_modulo(2, v_codigo, v_nombre, v_horas);                                       -- posicional
pr_datos_modulo(p_id_modulo => 2, p_horas => v_horas, p_nombre => v_nombre, p_codigo => v_codigo);   -- nomenada
```

> [!WARNING]
> Tres errors habituals amb els paràmetres: (1) **donar-los el nom d'una columna** (`id_alumno`): dins d'un `WHERE id_alumno = id_alumno` tots dos són la columna i la condició és sempre vertadera. Per això el prefix `p_`. (2) **Indicar longitud** en el tipus (`p_texto VARCHAR2(40)`): és un error de sintaxi; el paràmetre pren la longitud de l'argument. (3) Passar un **literal** a un paràmetre `OUT` (`PLS-00363`): necessita una variable.

### 10.3 Invocar un procediment

| Forma | On | Exemple |
|---|---|---|
| Des d'un bloc PL/SQL | Qualsevol client | `BEGIN pr_matricular(1, 2, '2026-27'); END;` |
| `EXEC` / `EXECUTE` | SQLcl, SQL\*Plus, SQL Developer | `EXEC pr_matricular(1, 2, '2026-27')` (és una abreviatura del bloc anterior; sense `;` ni `/`) |
| `CALL` | Qualsevol client SQL | `CALL pr_matricular(1, 2, '2026-27');` (els parèntesis són obligatoris, fins i tot sense paràmetres) |
| Des d'un altre subprograma o un disparador | PL/SQL | `pr_matricular(...);` |
| Des d'una tasca programada | `DBMS_SCHEDULER` | `job_type => 'STORED_PROCEDURE'` (§12) |

### 10.4 Procediments, transaccions i privilegis

**Qui confirma la transacció?** Un procediment que modifica dades **no hauria de fer `COMMIT`**: qui el crida pot estar encadenant diverses operacions que han de confirmar-se juntes (UD08). La regla pràctica:

| Tipus de subprograma | `COMMIT` |
|---|---|
| Operació de negoci **cridada des de l'aplicació o des d'un altre subprograma** (`pr_matricular`) | **No**: ho decidix el qui crida |
| Tasca **desatesa** sense ningú per damunt (un procediment que executa una tasca programada) | Sí: ningú més ho farà |

**Amb quins privilegis s'executa?** Per defecte un procediment s'executa amb els privilegis del seu **propietari** (`AUTHID DEFINER`), no amb els de qui el crida:

| | `AUTHID DEFINER` (per defecte) | `AUTHID CURRENT_USER` |
|---|---|---|
| Privilegis usats | Els del propietari | Els de qui executa |
| Rols del qui l'usa | No intervenen | S'apliquen |
| Per a què servix | Donar un **accés controlat**: `EXECUTE` sobre el procediment sense donar accés a les taules | Utilitats genèriques que han de respectar els permisos de cada usuari |

Esta és la base de la seguretat del projecte de la unitat: la secretaria pot matricular **només a través de** `pr_matricular`, sense permís `INSERT` sobre `MATRICULA`:

```sql
GRANT EXECUTE ON pr_matricular TO rol_secretaria;
```

> [!NOTE]
> En un procediment de drets del propietari, els privilegis que necessita sobre les taules han d'estar concedits **directament** al seu amo; els rebuts a través d'un rol no compten en temps de compilació (el símptoma és un `PLS-00201` o un `ORA-00942` sobre una taula que sí «veus» des de SQL). Si el propietari és el mateix esquema que les taules, com en `EDUGEST`, no hi ha problema.

### 10.5 Exemple complet: procediment de matrícula

`pr_matricular` implementa la regla R2 del catàleg de restriccions (UD03) i les regles de convocatòria. Rep l'alumne, el mòdul i el curs acadèmic, valida i, si tot és correcte, inserix la matrícula calculant la convocatòria. Reunix tot el que s'ha vist: paràmetres, `SELECT INTO`, blocs aniuats, excepcions i `RAISE_APPLICATION_ERROR`.

{{< sgbd "Oracle 26ai" >}}

```sql
CREATE OR REPLACE PROCEDURE pr_matricular (
    p_id_alumno  IN alumno.id_alumno%TYPE,
    p_id_modulo  IN modulo.id_modulo%TYPE,
    p_curso      IN matricula.curso_academico%TYPE
)
IS
    c_max_convocatorias  CONSTANT PLS_INTEGER := 4;
    v_ciclo_alumno       grupo.cod_ciclo%TYPE;
    v_ciclo_modulo       modulo.cod_ciclo%TYPE;
    v_ya_matriculado     PLS_INTEGER;
    v_convocatoria       PLS_INTEGER;
BEGIN
    -- 1. L'alumne existix i té grup (si no, el JOIN no torna cap fila)
    BEGIN
        SELECT g.cod_ciclo
        INTO   v_ciclo_alumno
        FROM   alumno a
               JOIN grupo g ON g.cod_grupo = a.cod_grupo
        WHERE  a.id_alumno = p_id_alumno;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RAISE_APPLICATION_ERROR(-20012, 'El alumno ' || p_id_alumno || ' no existe o no tiene grupo asignado');
    END;

    -- 2. El mòdul existix
    BEGIN
        SELECT cod_ciclo INTO v_ciclo_modulo FROM modulo WHERE id_modulo = p_id_modulo;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RAISE_APPLICATION_ERROR(-20012, 'El módulo ' || p_id_modulo || ' no existe');
    END;

    -- 3. R2: el mòdul és del cicle del grup de l'alumne
    IF v_ciclo_modulo <> v_ciclo_alumno THEN
        RAISE_APPLICATION_ERROR(-20010, 'El módulo ' || p_id_modulo || ' (' || v_ciclo_modulo || ') no es del ciclo del alumno ' || p_id_alumno || ' (' || v_ciclo_alumno || ')');
    END IF;

    -- 4. No està ja matriculat en eixe curs acadèmic
    SELECT COUNT(*)
    INTO   v_ya_matriculado
    FROM   matricula
    WHERE  id_alumno = p_id_alumno AND id_modulo = p_id_modulo AND curso_academico = p_curso;

    IF v_ya_matriculado > 0 THEN
        RAISE_APPLICATION_ERROR(-20013, 'El alumno ' || p_id_alumno || ' ya está matriculado del módulo ' || p_id_modulo || ' en ' || p_curso);
    END IF;

    -- 5. Convocatòria: una més que l'última matrícula del mòdul (màxim 4)
    SELECT NVL(MAX(convocatoria), 0) + 1
    INTO   v_convocatoria
    FROM   matricula
    WHERE  id_alumno = p_id_alumno AND id_modulo = p_id_modulo;

    IF v_convocatoria > c_max_convocatorias THEN
        RAISE_APPLICATION_ERROR(-20011, 'El alumno ' || p_id_alumno || ' ha agotado las ' || c_max_convocatorias || ' convocatorias del módulo ' || p_id_modulo);
    END IF;

    -- 6. Tot correcte: s'inserix. No hi ha COMMIT: ho decidix qui crida
    INSERT INTO matricula (id_alumno, id_modulo, curso_academico, convocatoria)
    VALUES (p_id_alumno, p_id_modulo, p_curso, v_convocatoria);
END pr_matricular;
/
```

Decisions de disseny que convé entendre:

| Decisió | Motiu |
|---|---|
| Els dos primers `SELECT INTO` van en **blocs aniuats** | Converteixen `NO_DATA_FOUND` en un error de negoci amb codi i missatge propis (`-20012`), en lloc de deixar passar un `ORA-01403` incomprensible |
| La convocatòria es calcula com `MAX(convocatoria) + 1` sobre **totes** les matrícules de l'alumne en eixe mòdul | Si mai s'ha matriculat, `MAX` torna `NULL`, `NVL(..., 0)` el convertix en 0 i la convocatòria és 1 |
| `RAISE_APPLICATION_ERROR` en cada regla | Un codi distint per regla: l'aplicació pot reaccionar sense analitzar el text |
| **No hi ha `COMMIT`** | La matrícula forma part d'una transacció major (matricular l'alumne en tot el curs, UD08); ho decidix qui crida |
| El curs acadèmic **no es valida** en el procediment | Ho fa la restricció `CK_MATRICULA_CURSO` de la taula. Duplicar la validació crearia dues regles que mantindre |

**Proves.** Amb l'alumne 1 (grup 1DAM, cicle DAM), que ja va cursar el mòdul 2 en 2025-26 i el va suspendre (nota 4,75):

```sql
EXEC pr_matricular(1, 2, '2026-27')

SELECT id_matricula, id_modulo, curso_academico, convocatoria
FROM   matricula
WHERE  id_alumno = 1 AND curso_academico = '2026-27';
```

| ID_MATRICULA | ID_MODULO | CURSO_ACADEMICO | CONVOCATORIA |
|---|---|---|---|
| 20001 | 2 | 2026-27 | 2 |

*1 fila* (l'identificador depén de les insercions que s'hagen fet abans en la taula)

La matrícula s'ha creat com a **segona convocatòria**. Ara, els errors:

```sql
EXEC pr_matricular(1, 2, '2026-27')      -- repetida
```

```text
ORA-20013: El alumno 1 ya está matriculado del módulo 2 en 2026-27
ORA-06512: at "EDUGEST.PR_MATRICULAR", line 45
ORA-06512: at line 1
```

```sql
EXEC pr_matricular(1, 12, '2026-27')     -- el mòdul 12 és de DAW; l'alumne 1 és de DAM
```

```text
ORA-20010: El módulo 12 (DAW) no es del ciclo del alumno 1 (DAM)
ORA-06512: at "EDUGEST.PR_MATRICULAR", line 35
ORA-06512: at line 1
```

Els números de línia d'`ORA-06512` compten des de la línia `PROCEDURE pr_matricular` i et porten al `RAISE_APPLICATION_ERROR` exacte (`SELECT text FROM user_source WHERE name = 'PR_MATRICULAR' ORDER BY line`). La bateria completa de huit proves està en la [pràctica 9.3](/ud09-plsql/ud09-practicas#pràctica-93--procediment-de-matrícula-amb-excepcions). Quan acabes, `ROLLBACK;` torna la taula al seu estat original.

> [!TIP]
> Un procediment que valida sempre té la mateixa estructura: **comprovar → rebutjar amb un error clar → actuar**. Les comprovacions van primer i de més barata a més cara; l'`INSERT` va al final, quan ja no pot fallar per una regla de negoci.

### 10.6 Gestionar els procediments

| Tasca | Sentència |
|---|---|
| Llistar els subprogrames i el seu estat | `SELECT object_name, object_type, status FROM user_objects WHERE object_type IN ('PROCEDURE','FUNCTION','PACKAGE','TRIGGER') ORDER BY 2, 1;` |
| Veure el codi | `SELECT text FROM user_source WHERE name = 'PR_MATRICULAR' ORDER BY line;` |
| Veure els errors de compilació | `SHOW ERRORS` o `SELECT * FROM user_errors WHERE name = 'PR_MATRICULAR';` |
| Recompilar | `ALTER PROCEDURE pr_matricular COMPILE;` |
| De què depén | `SELECT referenced_name, referenced_type FROM user_dependencies WHERE name = 'PR_MATRICULAR';` |
| Concedir-ne l'ús | `GRANT EXECUTE ON pr_matricular TO rol_secretaria;` |
| Esborrar | `DROP PROCEDURE pr_matricular;` |

Un subprograma passa a `INVALID` quan canvia alguna cosa de la qual depén (una taula, una altra funció). Oracle el recompila automàticament la pròxima vegada que s'usa, però un canvi d'estructura en producció ha de seguir-se d'una **recompilació de l'esquema** i d'una comprovació que tot està `VALID`.

{{< quiz >}}
- q: "En un procediment, què s'ha de passar com a argument a un paràmetre `OUT`?"
  options: ["Un literal amb el valor inicial", "Una variable que rebrà el resultat", "Una constant", "Res: els `OUT` no es passen"]
  answer: 1
  explain: "El paràmetre `OUT` torna un valor al qui crida, que necessita una variable on rebre'l. Passar-li un literal dona `PLS-00363`."
- q: "Un bloc té `WHEN OTHERS THEN NULL;` i el programa «funciona», però falten dades en la taula. Quin és el problema?"
  options: ["`NULL` no és una instrucció vàlida", "El manejador es traga qualsevol error sense deixar rastre", "`OTHERS` només es pot usar en funcions", "Falta un `COMMIT` en el manejador"]
  answer: 1
  explain: "Amb `WHEN OTHERS THEN NULL` qualsevol error desapareix en silenci. Un `OTHERS` només és acceptable si registra l'error i el torna a llançar amb `RAISE;`."
- q: "`PRAGMA EXCEPTION_INIT(e_tiene_hijos, -2292);` servix per a…"
  options: ["Crear l'error `ORA-02292`", "Donar nom a un error d'Oracle per a poder tractar-lo en un `WHEN`", "Evitar que es produïsca l'error", "Convertir l'error en una advertència"]
  answer: 1
  explain: "El pragma només associa un nom del programa a un codi d'error d'Oracle que no té nom predefinit. No canvia quan ni per què ocorre l'error."
- q: "Quins codis admet `RAISE_APPLICATION_ERROR`?"
  options: ["Qualsevol codi `ORA-`", "Només de -20000 a -20999", "Només positius", "Només els de la taula `USER_ERRORS`"]
  answer: 1
  explain: "El rang de -20000 a -20999 està reservat per Oracle a les aplicacions. Qualsevol altre valor llança `ORA-21000`."
- q: "El procediment `pr_matricular` no executa `COMMIT`. Per què?"
  options: ["Perquè Oracle no permet `COMMIT` en procediments", "Perquè la matrícula forma part d'una transacció major i ho ha de decidir qui crida", "Perquè `INSERT` ja confirma automàticament", "Perquè ho fa el disparador de la taula"]
  answer: 1
  explain: "Un `COMMIT` dins d'una operació de negoci impediria agrupar diverses operacions en una sola transacció. Oracle sí que permet el `COMMIT` en un procediment; és una decisió de disseny."
{{< /quiz >}}


---

{{< sesion n="7" h="1" tipo="t" >}}Disparadors, tasques programades i paquets{{< /sesion >}}

{{% paso-a-paso titulo="Qué dispara un trigger y en qué orden" %}}
{{% etapa titulo="1. Arriba la sentència" %}}
Un usuari executa `UPDATE empleado SET sueldo = sueldo * 1.05 WHERE id_dep = 10;` i afecta, per exemple, 3 files.
{{% /etapa %}}
{{% etapa titulo="2. BEFORE STATEMENT" %}}
S'executa **una vegada**, abans de tocar cap fila.
{{% /etapa %}}
{{% etapa titulo="3. BEFORE EACH ROW" %}}
S'executa **per cada fila afectada**, just abans de canviar-la. Ací es pot modificar `:NEW`.
{{% /etapa %}}
{{% etapa titulo="4. Es modifica la fila" %}}
Oracle aplica el canvi a eixa fila.
{{% /etapa %}}
{{% etapa titulo="5. AFTER EACH ROW" %}}
S'executa per cada fila, just després. Els passos 3-5 es repetixen per a les 3 files.
{{% /etapa %}}
{{% etapa titulo="6. AFTER STATEMENT" %}}
S'executa **una vegada** al final. Si alguna cosa falla en qualsevol punt, es desfà tota la sentència.
{{% /etapa %}}
{{% /paso-a-paso %}}

## 11. Disparadors (triggers)

### 11.1 Què és un disparador i com es construïx

Un **disparador** és un bloc PL/SQL guardat en la base de dades i associat a un **esdeveniment**. Ningú el crida: Oracle l'executa automàticament quan ocorre l'esdeveniment. És l'eina amb què s'implementen les regles d'integritat que el model lògic no pot declarar (RA6.h), l'auditoria i els valors calculats que s'han d'aplicar **sempre**, vinga el canvi d'on vinga (RA4.h).

```text
CREATE [OR REPLACE] TRIGGER nombre
{BEFORE | AFTER | INSTEAD OF}
{INSERT | UPDATE [OF columna, ...] | DELETE} [OR ...]
ON {tabla | vista}
[FOR EACH ROW]
[WHEN (condición)]
[DECLARE declaraciones]
BEGIN
    instrucciones
[EXCEPTION manejadores]
END;
```

Tres decisions definixen el comportament d'un disparador:

| Decisió | Opcions | Efecte |
|---|---|---|
| **Moment** | `BEFORE` / `AFTER` / `INSTEAD OF` | Abans o després que s'aplique el canvi; o en lloc d'ell (només vistes) |
| **Esdeveniment** | `INSERT`, `UPDATE [OF col]`, `DELETE` (combinables amb `OR`) | Quina sentència el dispara. `UPDATE OF nota_final` només si eixa columna apareix en el `SET` |
| **Nivell** | De **sentència** (per omissió) o de **fila** (`FOR EACH ROW`) | Una execució per sentència o una per cada fila afectada |

Combinant moment i nivell resulten els quatre punts de disparament clàssics:

| Punt de disparament | Quantes vegades | Què es pot fer | Ús típic |
|---|---|---|---|
| `BEFORE STATEMENT` | 1 per sentència | Comprovar condicions generals | Rebutjar canvis fora d'horari o sense permís |
| `BEFORE EACH ROW` | 1 per fila, abans del canvi | **Llegir i modificar `:NEW`** | Normalitzar dades, omplir valors, validar la fila |
| `AFTER EACH ROW` | 1 per fila, després del canvi | Llegir `:OLD` i `:NEW` | **Auditoria**, propagar canvis a una altra taula |
| `AFTER STATEMENT` | 1 per sentència | Consultar el resultat complet de la sentència | Comprovacions sobre el conjunt de files |

#### `:NEW`, `:OLD` i condicions

En un disparador **de fila**, `:OLD` conté els valors de la fila **abans** del canvi i `:NEW` els valors **després**:

| Esdeveniment | `:OLD.columna` | `:NEW.columna` |
|---|---|---|
| `INSERT` | `NULL` (no hi havia fila) | Els valors que s'inserixen |
| `UPDATE` | Valors abans del canvi | Valors després del canvi |
| `DELETE` | Valors de la fila esborrada | `NULL` (no queda fila) |

Regles que convé memoritzar:

- Dins del cos s'escriuen **amb dos punts**: `:NEW.nota_final`. En la clàusula `WHEN` s'escriuen **sense ells**: `WHEN (NEW.nota_final <> OLD.nota_final)`.
- **Només un `BEFORE EACH ROW` pot assignar a `:NEW`**. Fer-ho en un `AFTER` produïx `ORA-04084: cannot change NEW values for this trigger type`.
- Un disparador que atén diversos esdeveniments distingix quin ha sigut amb els predicats `INSERTING`, `UPDATING` (o `UPDATING('columna')`) i `DELETING`.
- `WHEN` evita executar el cos quan no cal: és la forma més eficient de filtrar.

Restriccions d'un disparador:

| No pot… | Error | Motiu |
|---|---|---|
| Fer `COMMIT` ni `ROLLBACK` | `ORA-04092: cannot COMMIT in a trigger` | Forma part de la transacció de la sentència que l'ha disparat |
| Executar DDL | Confirma la transacció (i no es permet) | El DDL du `COMMIT` implícit |
| Consultar o modificar la taula que està canviant la sentència (disparador de fila) | `ORA-04091: table is mutating` | És l'error de la **taula mutant** (§11.6) |

> [!IMPORTANT]
> Un disparador pertany a la transacció de la sentència que el dispara: si la sentència falla o es fa `ROLLBACK`, **també es desfà el que el disparador ha fet**. És el que es vol per a la integritat; no ho és per a un registre d'intents fallits (§11.2, nota final).

### 11.2 Auditoria de canvis de nota

Els canvis de nota són la dada més sensible d'EduGest. Un disparador `AFTER UPDATE` registra, per a cada canvi, **qui** l'ha fet, **quan**, i quin valor hi havia **abans** i **després**. Primer, la taula on es guarda:

{{< sgbd "Oracle 26ai" >}}

```sql
CREATE TABLE auditoria_nota (
    id_auditoria   NUMBER(10) GENERATED BY DEFAULT ON NULL AS IDENTITY
                   CONSTRAINT pk_auditoria_nota PRIMARY KEY,
    id_matricula   NUMBER(8)     CONSTRAINT nn_auditoria_matricula NOT NULL,
    nota_anterior  NUMBER(4,2),
    nota_nueva     NUMBER(4,2),
    usuario        VARCHAR2(128) CONSTRAINT nn_auditoria_usuario NOT NULL,
    fecha_cambio   TIMESTAMP     DEFAULT SYSTIMESTAMP CONSTRAINT nn_auditoria_fecha NOT NULL
);
COMMENT ON TABLE auditoria_nota IS 'Histórico de cambios de MATRICULA.NOTA_FINAL (trg_auditoria_nota)';
```

> [!NOTE]
> La taula d'auditoria **no du clau aliena** a `MATRICULA`: l'històric ha de sobreviure a la fila auditada. Si s'esborrara una matrícula i la clau aliena ho impedira (o ho arrossegara en cascada), l'auditoria perdria la seua raó de ser.

I el disparador:

```sql
CREATE OR REPLACE TRIGGER trg_auditoria_nota
AFTER UPDATE OF nota_final ON matricula
FOR EACH ROW
WHEN (NVL(NEW.nota_final, -1) <> NVL(OLD.nota_final, -1))
BEGIN
    INSERT INTO auditoria_nota (id_matricula, nota_anterior, nota_nueva, usuario)
    VALUES (:OLD.id_matricula, :OLD.nota_final, :NEW.nota_final, USER);
END trg_auditoria_nota;
/
```

| Part | Per què |
|---|---|
| `AFTER` | L'auditoria es registra quan el canvi ja s'ha acceptat: si una restricció el rebutja, no queda rastre d'una cosa que no va ocórrer |
| `UPDATE OF nota_final` | El disparador només s'avalua quan la sentència toca eixa columna |
| `FOR EACH ROW` | Cal `:OLD` i `:NEW`, que existixen per fila |
| `WHEN (NVL(NEW.nota_final, -1) <> NVL(OLD.nota_final, -1))` | Només s'audita si la nota **realment canvia**. `NVL` maneja els nuls: sense ell, passar de `NULL` a 6, o de 6 a `NULL`, donaria un resultat desconegut i no s'auditaria. El valor sentinella `-1` és segur perquè una nota vàlida va de 0 a 10 |
| `USER` | Qui ha fet el canvi |

**Prova.** Amb la matrícula `10002` (alumne 1, mòdul 2, nota 4,75):

```sql
UPDATE matricula SET nota_final = 6    WHERE id_matricula = 10002;   -- canvia 4,75 → 6
UPDATE matricula SET nota_final = 6    WHERE id_matricula = 10002;   -- el valor no canvia
UPDATE matricula SET nota_final = NULL WHERE id_matricula = 10002;   -- 6 → NULL (s'anul·la la nota)

SELECT id_matricula, nota_anterior, nota_nueva, usuario
FROM   auditoria_nota
ORDER  BY id_auditoria;
```

| ID_MATRICULA | NOTA_ANTERIOR | NOTA_NUEVA | USUARIO |
|---|---|---|---|
| 10002 | 4.75 | 6 | EDUGEST |
| 10002 | 6 | *(null)* | EDUGEST |

*2 files*

Les tres sentències han actualitzat una fila, però només s'han registrat **dos** canvis: la segona no va canviar el valor i el `WHEN` va impedir que el cos s'executara. Acaba amb `ROLLBACK;`: com que el disparador pertany a la transacció, l'auditoria també es desfà i la taula torna al seu estat inicial.

> [!NOTE]
> Eixa és justament la propietat que es vol per a la integritat (si el canvi no es confirma, la seua auditoria tampoc), però no per a un **registre d'intents**: si es vol deixar constància d'un intent encara que la transacció es desfaça, el registre s'ha de fer en una **transacció autònoma** (`PRAGMA AUTONOMOUS_TRANSACTION`), que confirma pel seu compte. És el que es demana en la pràctica 9.5 i en el projecte.

### 11.3 R1: el cap d'un departament pertany a eixe departament

La regla R1 compara una fila de `DEPARTAMENTO` amb una fila de `PROFESOR`: cap restricció declarativa pot fer-ho. Cal vigilar **dos costats**: quan s'assigna el cap (este disparador) i quan un professor cap canvia de departament (pràctica 9.5).

```sql
CREATE OR REPLACE TRIGGER trg_jefe_departamento
BEFORE INSERT OR UPDATE OF id_jefe ON departamento
FOR EACH ROW
WHEN (NEW.id_jefe IS NOT NULL)
DECLARE
    v_dpto  profesor.id_departamento%TYPE;
BEGIN
    SELECT id_departamento INTO v_dpto FROM profesor WHERE id_profesor = :NEW.id_jefe;
    IF v_dpto <> :NEW.id_departamento THEN
        RAISE_APPLICATION_ERROR(-20020, 'El profesor ' || :NEW.id_jefe || ' pertenece al departamento ' || v_dpto || ', no al ' || :NEW.id_departamento);
    END IF;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        NULL;      -- professor inexistent: ja el rebutjarà la clau aliena
END;
/
```

És un disparador `BEFORE` perquè **rebutja** el canvi abans d'aplicar-lo. Consulta `PROFESOR`, no la taula que es modifica (`DEPARTAMENTO`), així que no hi ha problema de taula mutant. Proves:

```sql
UPDATE departamento SET id_jefe = 111 WHERE id_departamento = 1;   -- 111 és Laura Vicent, del dpto. 3
```

```text
ORA-20020: El profesor 111 pertenece al departamento 3, no al 1
ORA-06512: at "EDUGEST.TRG_JEFE_DEPARTAMENTO", line 10
ORA-04088: error during execution of trigger 'EDUGEST.TRG_JEFE_DEPARTAMENTO'
```

```sql
UPDATE departamento SET id_jefe = 102 WHERE id_departamento = 1;   -- 102 és Javier Pastor, del dpto. 1
-- 1 fila actualitzada
```

Observa que l'error té **tres línies**: el missatge propi (`ORA-20020`), el lloc del codi on va ocórrer (`ORA-06512`, número de línia comptat des de la línia `TRIGGER`) i l'avís genèric que ha fallat un disparador (`ORA-04088`). La causa és sempre la primera.

> [!TIP]
> Les dades d'exemple de l'script 02 complixen la regla: els caps 101, 109, 111 i 112 pertanyen als seus departaments (1, 2, 3 i 5). Per això el disparador no impedix recarregar les dades.

### 11.4 Normalització de dades en guardar

Un `BEFORE ... FOR EACH ROW` pot **corregir** la dada abans que es guarde. És el lloc adequat perquè els noms arriben sempre amb la mateixa forma, vinga l'`INSERT` de l'aplicació o d'una eina gràfica:

```sql
CREATE OR REPLACE TRIGGER trg_alumno_normaliza
BEFORE INSERT OR UPDATE OF nombre, apellidos, email ON alumno
FOR EACH ROW
BEGIN
    :NEW.nombre    := INITCAP(TRIM(:NEW.nombre));
    :NEW.apellidos := INITCAP(TRIM(:NEW.apellidos));
    :NEW.email     := LOWER(TRIM(:NEW.email));
END trg_alumno_normaliza;
/
```

```sql
INSERT INTO alumno (nia, nombre, apellidos, fecha_nacimiento, email)
VALUES ('10459999', '  marina ', 'lópez ortega', DATE '2007-01-01', ' Marina@Mail.COM ');

SELECT nombre, apellidos, email FROM alumno WHERE nia = '10459999';
```

| NOMBRE | APELLIDOS | EMAIL |
|---|---|---|
| Marina | López Ortega | marina@mail.com |

*1 fila*

Dos observacions:

1. El disparador `BEFORE` s'executa **abans de comprovar** la restricció `UNIQUE` del correu. Així `Marina@Mail.COM` i `marina@mail.com` es detecten com a duplicats: sense normalitzar, la restricció els hauria considerat distints.
2. `INITCAP` no és perfecte: convertix `de la Cruz` en `De La Cruz`. Una normalització automàtica ha de ser **conservadora** i documentada.

Acaba amb `ROLLBACK;` per a no deixar l'alumne de prova.

### 11.5 Disparadors `INSTEAD OF`: vistes que es poden modificar

Una vista construïda amb composicions no sempre és actualitzable. Un disparador `INSTEAD OF` s'executa **en lloc de** la sentència DML sobre la vista, i decidix què fer amb les taules reals. És sempre de fila. Per exemple, una vista perquè la secretaria matricule indicant el NIA i el codi del mòdul, en lloc d'identificadors interns:

```sql
CREATE OR REPLACE VIEW v_matricula_nia AS
    SELECT a.nia, mo.codigo AS cod_modulo, mo.cod_ciclo,
           m.curso_academico, m.convocatoria, m.nota_final
    FROM   matricula m
           JOIN alumno a  ON a.id_alumno  = m.id_alumno
           JOIN modulo mo ON mo.id_modulo = m.id_modulo;

CREATE OR REPLACE TRIGGER trg_v_matricula_nia_ins
INSTEAD OF INSERT ON v_matricula_nia
FOR EACH ROW
DECLARE
    v_id_alumno  alumno.id_alumno%TYPE;
    v_id_modulo  modulo.id_modulo%TYPE;
BEGIN
    SELECT id_alumno INTO v_id_alumno FROM alumno WHERE nia = :NEW.nia;
    SELECT id_modulo INTO v_id_modulo FROM modulo
    WHERE  codigo = :NEW.cod_modulo AND cod_ciclo = :NEW.cod_ciclo;

    pr_matricular(v_id_alumno, v_id_modulo, :NEW.curso_academico);   -- reutilitza §10.5
END trg_v_matricula_nia_ins;
/
```

```sql
INSERT INTO v_matricula_nia (nia, cod_modulo, cod_ciclo, curso_academico)
VALUES ('10450037', '0484', 'DAM', '2026-27');
-- 1 fila creada (internament: pr_matricular(1, 2, '2026-27'))
```

L'`INSERT` sobre la vista no toca la vista (no emmagatzema res): activa el disparador, que traduïx el NIA i el codi a identificadors i delega en el procediment, **amb totes les seues validacions**. Prova'l i fes `ROLLBACK`.

### 11.6 La taula mutant (`ORA-04091`) i el disparador compost

La regla R5 diu que un grup no pot tindre més de 30 alumnes. És un **recompte sobre diverses files**: no es pot declarar. La idea òbvia és un disparador `AFTER ... FOR EACH ROW` que conte els alumnes del grup:

```sql
CREATE OR REPLACE TRIGGER trg_grupo_max_fila               -- INCORRECTE! Només per a veure l'error
AFTER INSERT OR UPDATE OF cod_grupo ON alumno
FOR EACH ROW
DECLARE
    v_n  PLS_INTEGER;
BEGIN
    SELECT COUNT(*) INTO v_n FROM alumno WHERE cod_grupo = :NEW.cod_grupo;
    IF v_n > 30 THEN
        RAISE_APPLICATION_ERROR(-20040, 'El grupo ' || :NEW.cod_grupo || ' supera los 30 alumnos');
    END IF;
END;
/
```

Compila sense problemes. Falla en executar-se:

```sql
UPDATE alumno SET cod_grupo = '2ASIR' WHERE id_alumno = 30;
```

```text
ORA-04091: table EDUGEST.ALUMNO is mutating, trigger/function may not see it
ORA-06512: at "EDUGEST.TRG_GRUPO_MAX_FILA", line 7
ORA-04088: error during execution of trigger 'EDUGEST.TRG_GRUPO_MAX_FILA'
```

**Per què.** Mentre una sentència modifica una taula, esta es troba en un estat intermedi: unes files ja han canviat i altres no. Un disparador de fila que la consultara obtindria un resultat que **depén de l'ordre** en què Oracle processe les files. Per a impedir-ho, Oracle prohibix que un disparador de fila (o una funció cridada des d'ell) lligga o modifique la taula que s'està modificant: és l'error de la **taula mutant**.

> [!NOTE]
> Hi ha excepcions puntuals a la restricció (per exemple, alguns `INSERT ... VALUES` d'una sola fila), però no s'han d'utilitzar: el disseny correcte no depén d'elles. Els disparadors de **sentència** no tenen esta restricció, perquè s'executen abans o després que la taula canvie.

**La solució: el disparador compost.** Un disparador `COMPOUND` agrupa en un sol objecte les seccions de diversos punts de disparament (`BEFORE STATEMENT`, `BEFORE EACH ROW`, `AFTER EACH ROW`, `AFTER STATEMENT`) que **compartixen les mateixes variables mentre dura la sentència**. La tècnica té dos passos:

1. En `AFTER EACH ROW` **no es consulta** la taula: només s'*anota* en una col·lecció quins grups ha tocat la sentència.
2. En `AFTER STATEMENT`, quan la sentència ja ha acabat i la taula **deixa d'estar mutant**, es recorre la col·lecció i es fa el recompte.

{{< sgbd "Oracle 26ai" >}}

```sql
CREATE OR REPLACE TRIGGER trg_grupo_max_alumnos
FOR INSERT OR UPDATE OF cod_grupo ON alumno
COMPOUND TRIGGER

    c_max  CONSTANT PLS_INTEGER := 30;                       -- R5: màxim d'alumnes per grup

    TYPE t_grupos IS TABLE OF PLS_INTEGER INDEX BY VARCHAR2(10);
    g_grupos  t_grupos;                                      -- grups tocats per la sentència
    v_grupo   grupo.cod_grupo%TYPE;
    v_n       PLS_INTEGER;

    AFTER EACH ROW IS
    BEGIN
        IF :NEW.cod_grupo IS NOT NULL THEN
            g_grupos(:NEW.cod_grupo) := 1;                   -- només anotar: NO consultar ALUMNO
        END IF;
    END AFTER EACH ROW;

    AFTER STATEMENT IS
    BEGIN
        v_grupo := g_grupos.FIRST;
        WHILE v_grupo IS NOT NULL LOOP
            SELECT COUNT(*) INTO v_n FROM alumno WHERE cod_grupo = v_grupo;
            IF v_n > c_max THEN
                RAISE_APPLICATION_ERROR(-20040, 'El grupo ' || v_grupo || ' superaría los ' || c_max || ' alumnos (tendría ' || v_n || ')');
            END IF;
            v_grupo := g_grupos.NEXT(v_grupo);
        END LOOP;
    END AFTER STATEMENT;

END trg_grupo_max_alumnos;
/
```

| Element | Què fa |
|---|---|
| `FOR INSERT OR UPDATE OF cod_grupo ON alumno` | La capçalera d'un compost usa `FOR` en lloc de `BEFORE`/`AFTER`, i **no** du `FOR EACH ROW` |
| Secció declarativa (abans de les seccions) | Variables i tipus **compartits** per totes les seccions. S'inicialitzen en començar cada sentència i es descarten en acabar |
| `TYPE t_grupos ... INDEX BY VARCHAR2(10)` | Col·lecció associativa indexada pel codi de grup: guarda cada grup una sola vegada, encara que la sentència toque diverses files |
| `AFTER EACH ROW IS ... END AFTER EACH ROW;` | S'executa per fila; `:NEW` està disponible. Anota el grup |
| `AFTER STATEMENT IS ... END AFTER STATEMENT;` | S'executa una vegada al final; ara sí que pot consultar `ALUMNO` |
| `FIRST` / `NEXT` | Recorren les claus de la col·lecció associativa |

**Proves.** Els alumnes 30, 31 i 32 no tenen grup, i `2ASIR` està buit. Amb `c_max = 30` la regla es complix:

```sql
UPDATE alumno SET cod_grupo = '2ASIR' WHERE cod_grupo IS NULL;
-- 3 files actualitzades
ROLLBACK;
```

Per a provocar l'error sense crear 28 alumnes, recompila el disparador amb `c_max CONSTANT PLS_INTEGER := 2;`:

```sql
UPDATE alumno SET cod_grupo = '2ASIR' WHERE cod_grupo IS NULL;
```

```text
ORA-20040: El grupo 2ASIR superaría los 2 alumnos (tendría 3)
ORA-06512: at "EDUGEST.TRG_GRUPO_MAX_ALUMNOS", line 25
ORA-04088: error during execution of trigger 'EDUGEST.TRG_GRUPO_MAX_ALUMNOS'
```

La sentència completa es desfà: les tres files continuen sense grup. Observa que la regla es comprova sobre el **resultat final**, no fila a fila, i que no apareix `ORA-04091`.

> [!WARNING]
> Este disparador comprova la regla en la **sessió que modifica**, però no veu els canvis sense confirmar d'altres sessions (consistència de lectura, UD08). Dos secretàries que afigen alhora un alumne a un grup amb 29 poden confirmar totes dues i deixar 31. La solució és **serialitzar** l'accés: bloquejar la fila del grup (`SELECT ... FROM grupo WHERE cod_grupo = ... FOR UPDATE`) abans de comptar. És l'apartat 5 de la [pràctica 9.6](/ud09-plsql/ud09-practicas#pràctica-96--repte-la-taula-mutant).

Altres formes de resoldre una restricció que necessita llegir la seua pròpia taula:

| Solució | Quan | Observacions |
|---|---|---|
| **Disparador compost** | L'opció general des d'Oracle 11g | La d'esta unitat |
| Disparador de sentència (`AFTER STATEMENT`) simple | No cal saber *quines files* han canviat | Torna a comprovar tota la taula |
| Variable de paquet + tres disparadors | Abans d'Oracle 11g | Obsolet: és el mateix que un compost, amb més peces |
| Un únic procediment d'accés (i revocar el DML directe) | Tot canvi passa per una API (`pkg_secretaria`) | La regla viu en el procediment, no en la taula |
| Redissenyar | La regla és un comptador | Columna amb el nombre d'alumnes mantinguda per l'API, o vista materialitzada amb restricció |
| `PRAGMA AUTONOMOUS_TRANSACTION` | **Mai per a això** | Llevaria l'error, però llegiria l'estat confirmat i no el de la sentència: la regla deixaria de ser fiable |

{{% details title="Prova tu: un disparador de fila que calcula una mitjana" %}}
**Enunciat.** Un company escriu un `AFTER UPDATE OF nota_final ON matricula FOR EACH ROW` que executa `SELECT AVG(nota_final) FROM matricula WHERE id_modulo = :NEW.id_modulo`. Quin error obté en executar `UPDATE matricula SET nota_final = nota_final + 0.25 WHERE id_modulo = 16;`? Com ho corregiries?

**Solució.** Obté `ORA-04091` (taula `MATRICULA` mutant): el disparador de fila llig la taula que la sentència està modificant. Es corregix amb un disparador compost: `AFTER EACH ROW` anota els `id_modulo` afectats en una col·lecció i `AFTER STATEMENT` calcula la mitjana de cada mòdul anotat. Si el que es vol és només mantindre una taula de resum, és més senzill calcular-ho en una tasca programada (§12).
{{% /details %}}

### 11.7 Laboratori: ordre de disparament i taula mutant

Este simulador reproduïx un `UPDATE` de **tres files** d'`ALUMNO` (els alumnes 30, 31 i 32, que passen al grup 2ASIR) i mostra, pas a pas, **quan s'executa cada punt de disparament** i en quin moment la taula està «mutant». És una simulació didàctica: les traces es generen amb regles fixes, no amb un gestor real.

{{< trigger-lab >}}

**Experiment 1 · L'ordre de disparament.** Amb l'escenari 1, avança fins al final i contesta:

1. Quantes vegades s'executen `BEFORE STATEMENT` i `AFTER STATEMENT`? I els disparadors de fila?
2. S'executen els tres `BEFORE EACH ROW` seguits i després els tres `AFTER EACH ROW`, o s'intercalen?
3. En quins punts de disparament apareix la taula com a «mutant»? On seria segur consultar `ALUMNO`?

**Experiment 2 · Dues formes de comprovar la regla R5.** Executa l'escenari 2 (el disparador de fila que compta) i fixa't en què li passa a la fila 30 quan salta l'error. Després executa l'escenari 3 amb el límit de 30 alumnes i amb el de 2: compara **quan** es fa la consulta `COUNT(*)` i **què veu** en cada cas.

{{% details title="Què hauries d'haver observat" %}}
`BEFORE STATEMENT` i `AFTER STATEMENT` s'executen **una vegada**; els de fila, **tres** (una per fila). Els disparadors de fila **s'intercalen per fila** (abans–canvi–després de la fila 30, després de la 31...) i la taula només és segura de consultar en `BEFORE STATEMENT` i `AFTER STATEMENT`, els dos punts que queden fora del recorregut de les files.

En l'escenari 2, la consulta del disparador de fila falla tan bon punt es canvia la primera fila, i Oracle desfà la sentència sencera: la fila 30 torna a `NULL`. En l'escenari 3 la consulta es mou a l'`AFTER STATEMENT`, on ja no hi ha taula mutant, i torna 3. Amb límit 30 la sentència acaba bé; amb límit 2 el disparador llança `ORA-20040` i es desfà igualment tota la sentència.
{{% /details %}}

### 11.8 Gestionar els disparadors i els disparadors de sistema

| Tasca | Sentència |
|---|---|
| Llistar els disparadors | `SELECT trigger_name, trigger_type, triggering_event, table_name, status FROM user_triggers ORDER BY table_name, trigger_name;` |
| Desactivar-ne un | `ALTER TRIGGER trg_auditoria_nota DISABLE;` |
| Activar-lo | `ALTER TRIGGER trg_auditoria_nota ENABLE;` |
| Desactivar tots els d'una taula | `ALTER TABLE matricula DISABLE ALL TRIGGERS;` (i `ENABLE ALL TRIGGERS`) |
| Veure el codi | `SELECT text FROM user_source WHERE name = 'TRG_AUDITORIA_NOTA' ORDER BY line;` |
| Esborrar-lo | `DROP TRIGGER trg_auditoria_nota;` |

> [!WARNING]
> Desactivar un disparador **apaga la regla** que implementa. Es fa en càrregues massives controlades (i es reactiva i es **comprova** després), mai «perquè funcione». Un disparador desactivat en producció és una restricció d'integritat que ja no existix.

Els disparadors no es limiten a les sentències DML. Oracle admet disparadors de **sistema**, que responen a esdeveniments de la base de dades o de la sessió (RA5.h: «esdeveniments i disparadors»):

| Categoria | Esdeveniment (exemple) | Ús típic |
|---|---|---|
| **DML** | `BEFORE`/`AFTER INSERT OR UPDATE OR DELETE ON tabla` | Integritat, auditoria, valors calculats |
| **Vista** | `INSTEAD OF INSERT OR UPDATE OR DELETE ON vista` | Fer actualitzable una vista complexa |
| **DDL** | `AFTER CREATE OR ALTER OR DROP ON SCHEMA` | Registrar canvis d'estructura (amb `ORA_SYSEVENT`, `ORA_DICT_OBJ_NAME`) |
| **Sessió** | `AFTER LOGON ON SCHEMA` | Fixar paràmetres de la sessió, registrar accessos |
| **Base de dades** | `STARTUP`, `SHUTDOWN`, `SERVERERROR` | Tasques d'arrancada, registrar els errors del servidor |

### 11.9 Quan NO usar un disparador

Un disparador és lògica **invisible**: no apareix en el codi de l'aplicació i s'executa sense que ningú el cride. Usa'l quan no hi haja una alternativa declarativa:

| Necessitat | Millor que un disparador |
|---|---|
| Valor per defecte | `DEFAULT` en la columna |
| Valor d'una sola fila dins d'un rang o llista | `CHECK` |
| Unicitat | `UNIQUE` |
| Integritat referencial | `FOREIGN KEY` |
| Clau autogenerada | Columna `IDENTITY` (en lloc de seqüència + disparador) |
| Operació de negoci completa que crida l'aplicació | Procediment emmagatzemat (com `pr_matricular`) |

> [!TIP]
> Dissenya els disparadors **curts i d'un únic propòsit**: un per a l'auditoria, un altre per a cada regla. Un disparador de 200 línies que valida, audita, recalcula i avisa és impossible de provar. Documenta en un comentari quina restricció del catàleg implementa (R1, R3...), i tingues una prova per a cadascuna.

{{< quiz >}}
- q: "En un disparador de fila `AFTER UPDATE ... FOR EACH ROW`, quin és el contingut de `:OLD.nota_final` i `:NEW.nota_final` en canviar la nota de 4,75 a 6?"
  options: ["`:OLD` és 6 i `:NEW` és 4,75", "`:OLD` és 4,75 i `:NEW` és 6", "Tots dos valen 6", "Tots dos valen `NULL`"]
  answer: 1
  explain: "`:OLD` conté la fila abans del canvi i `:NEW` la fila després. En un `INSERT` `:OLD` és nul; en un `DELETE`, `:NEW` és nul."
- q: "Per què `trg_auditoria_nota` usa `NVL(NEW.nota_final, -1) <> NVL(OLD.nota_final, -1)` en lloc de `NEW.nota_final <> OLD.nota_final`?"
  options: ["Perquè `<>` no existix en `WHEN`", "Perquè si alguna nota és `NULL` la comparació és desconeguda i el canvi no s'auditaria", "Perquè `NVL` és més ràpid", "Perquè `-1` és la nota mínima"]
  answer: 1
  explain: "Una comparació amb `NULL` no és vertadera ni falsa. Sense `NVL`, passar de `NULL` a 6 (o anul·lar una nota) no dispararia el cos i el canvi quedaria sense auditar."
- q: "Un `AFTER INSERT ... FOR EACH ROW` sobre `ALUMNO` executa `SELECT COUNT(*) FROM alumno ...`. Què passa?"
  options: ["Funciona i compta totes les files", "Oracle torna `ORA-04091` (taula mutant)", "El disparador no compila", "S'executa però compta zero files"]
  answer: 1
  explain: "Un disparador de fila no pot llegir la taula que està modificant la sentència: el resultat dependria de l'ordre de procés de les files. Compila bé i falla en executar-se."
- q: "En un disparador compost, en quina secció és segur consultar la taula que s'està modificant?"
  options: ["`BEFORE EACH ROW`", "`AFTER EACH ROW`", "`AFTER STATEMENT`", "En cap"]
  answer: 2
  explain: "En `AFTER STATEMENT` la sentència ja ha acabat i la taula deixa d'estar mutant. Per això la tècnica consistix a anotar en `AFTER EACH ROW` i comprovar en `AFTER STATEMENT`."
- q: "Un `INSTEAD OF INSERT` sobre una vista…"
  options: ["S'executa després de l'`INSERT` en la vista", "S'executa en lloc de l'`INSERT` i decidix què fer amb les taules reals", "Només es pot crear sobre taules", "És de sentència, no de fila"]
  answer: 1
  explain: "`INSTEAD OF` només existix sobre vistes, és sempre de fila i substituïx la sentència DML: el programador decidix com es tradueix a les taules base."
{{< /quiz >}}


---


## 12. Esdeveniments i tasques programades {#12-eventos-tareas-programadas}

### 12.1 Disparador, procediment o tasca programada

Hi ha tres maneres d'executar codi sense que una persona el llance a mà. Es distingixen per **què les posa en marxa**:

| | Què ho posa en marxa | Exemple en EduGest |
|---|---|---|
| **Disparador** | Un **esdeveniment de dades**: una sentència DML, una connexió, un `CREATE` | Auditar un canvi de nota |
| **Procediment** | Una **crida explícita** d'una persona o d'una aplicació | Matricular un alumne |
| **Tasca programada** (*job*) | El **rellotge**: un calendari | Recalcular cada nit el resum per grup |

La tasca programada servix per a treball periòdic i desatés: resums, neteges, tancaments, avisos. En Oracle l'oferix el paquet **`DBMS_SCHEDULER`**; altres gestors la diuen *esdeveniment* (MySQL/MariaDB) o deleguen en un agent extern (§12.5).

### 12.2 Un cas: la taula de resum per grup

Consultar la mitjana d'un grup recorre moltes files. Si la secretaria necessita eixa dada constantment, convé tindre-la ja calculada en una **taula de resum** (UD08 §5.3) que es refresque de matinada.

{{< sgbd "Oracle 26ai" >}}

```sql
CREATE TABLE resumen_grupo (
    cod_grupo    VARCHAR2(10) CONSTRAINT pk_resumen_grupo PRIMARY KEY,
    alumnos      NUMBER(3)    CONSTRAINT nn_resumen_grupo_alumnos NOT NULL,
    matriculas   NUMBER(5)    CONSTRAINT nn_resumen_grupo_matr NOT NULL,
    nota_media   NUMBER(4,2),
    horas_falta  NUMBER(5)    DEFAULT 0 CONSTRAINT nn_resumen_grupo_faltas NOT NULL,
    calculado    TIMESTAMP    DEFAULT SYSTIMESTAMP CONSTRAINT nn_resumen_grupo_calc NOT NULL,
    CONSTRAINT fk_resumen_grupo FOREIGN KEY (cod_grupo) REFERENCES grupo (cod_grupo)
);
COMMENT ON COLUMN resumen_grupo.nota_media IS 'Media de las notas no nulas del grupo';
```

El procediment que l'omple usa `MERGE` (UD08 §5.4): inserix els grups nous i actualitza els existents. Cada dada es calcula amb una subconsulta pròpia perquè les composicions de `MATRICULA` i `FALTA_ASISTENCIA` no duplique files:

```sql
CREATE OR REPLACE PROCEDURE pr_recalcular_resumen
IS
BEGIN
    MERGE INTO resumen_grupo r
    USING (
        SELECT g.cod_grupo,
               (SELECT COUNT(*) FROM alumno a
                WHERE  a.cod_grupo = g.cod_grupo)                          AS alumnos,
               (SELECT COUNT(*) FROM matricula m
                       JOIN alumno a ON a.id_alumno = m.id_alumno
                WHERE  a.cod_grupo = g.cod_grupo)                          AS matriculas,
               (SELECT ROUND(AVG(m.nota_final), 2) FROM matricula m
                       JOIN alumno a ON a.id_alumno = m.id_alumno
                WHERE  a.cod_grupo = g.cod_grupo)                          AS nota_media,
               (SELECT NVL(SUM(f.horas), 0) FROM falta_asistencia f
                       JOIN matricula m ON m.id_matricula = f.id_matricula
                       JOIN alumno a    ON a.id_alumno    = m.id_alumno
                WHERE  a.cod_grupo = g.cod_grupo)                          AS horas_falta
        FROM   grupo g
    ) o
    ON (r.cod_grupo = o.cod_grupo)
    WHEN MATCHED THEN
        UPDATE SET r.alumnos     = o.alumnos,
                   r.matriculas  = o.matriculas,
                   r.nota_media  = o.nota_media,
                   r.horas_falta = o.horas_falta,
                   r.calculado   = SYSTIMESTAMP
    WHEN NOT MATCHED THEN
        INSERT (cod_grupo, alumnos, matriculas, nota_media, horas_falta)
        VALUES (o.cod_grupo, o.alumnos, o.matriculas, o.nota_media, o.horas_falta);

    COMMIT;          -- tasca desatesa: ningú més confirmarà (vegeu §10.4)
END pr_recalcular_resumen;
/
```

```sql
EXEC pr_recalcular_resumen
SELECT cod_grupo, alumnos, matriculas, nota_media, horas_falta FROM resumen_grupo ORDER BY cod_grupo;
```

| COD_GRUPO | ALUMNOS | MATRICULAS | NOTA_MEDIA | HORAS_FALTA |
|---|---|---|---|---|
| 1ASIR | 5 | 25 | 7.07 | 11 |
| 1DAM | 7 | 35 | 6.4 | 18 |
| 1DAW | 6 | 30 | 6.19 | 14 |
| 2ASIR | 0 | 0 | *(null)* | 0 |
| 2DAM | 6 | 33 | 6.17 | 25 |
| 2DAW | 5 | 20 | 5.93 | 13 |

*6 files*

Comprovació: les matrícules sumen 143 i les hores de falta 81, les del total de la base de dades. El grup `2ASIR` no té alumnat: la seua mitjana és `NULL`, no 0.

### 12.3 `DBMS_SCHEDULER`: crear i governar tasques

`DBMS_SCHEDULER` separa el que s'executa (l'**acció**) de quan s'executa (el **calendari**). La unitat bàsica és el *job*:

| Concepte | Què és |
|---|---|
| **Job** (tasca) | Una acció més un calendari: «executa això a esta hora» |
| **Acció** (`job_type`) | `STORED_PROCEDURE` (crida a un procediment), `PLSQL_BLOCK` (un bloc anònim), `EXECUTABLE` (un programa del sistema) |
| **Calendari** (`repeat_interval`) | Una cadena de calendari, p. ex. `FREQ=DAILY; BYHOUR=2` |
| **Program** i **Schedule** | Acció i calendari amb nom, reutilitzables per diversos jobs |
| **Chain**, **Window** | Cadenes de tasques amb dependències; finestres de recursos. No s'estudien ací |

{{< sgbd "Oracle 26ai" >}}

```sql
BEGIN
    DBMS_SCHEDULER.CREATE_JOB(
        job_name        => 'JOB_RESUMEN_NOCTURNO',
        job_type        => 'STORED_PROCEDURE',
        job_action      => 'PR_RECALCULAR_RESUMEN',
        start_date      => SYSTIMESTAMP AT TIME ZONE 'Europe/Madrid',
        repeat_interval => 'FREQ=DAILY; BYHOUR=2; BYMINUTE=0; BYSECOND=0',
        enabled         => TRUE,
        auto_drop       => FALSE,
        comments        => 'Recalcula RESUMEN_GRUPO cada noche a las 02:00');
END;
/
```

| Paràmetre | Significat |
|---|---|
| `job_name` | Nom del job. Es guarda en majúscules |
| `job_type`, `job_action` | Què s'executa. Amb `STORED_PROCEDURE`, el nom del procediment |
| `start_date` | Des de quan val el calendari. Amb una zona horària amb nom (`Europe/Madrid`) el job respecta el canvi d'hora d'estiu |
| `repeat_interval` | El calendari (vegeu davall). Si s'omet, la tasca s'executa **una vegada** |
| `enabled` | `TRUE` l'activa en crear-la. Amb `FALSE` cal activar-la amb `ENABLE` |
| `auto_drop` | `TRUE` esborra el job quan acaba la seua última execució (útil per a tasques d'una sola vegada) |

> [!NOTE]
> Per a crear tasques fa falta el privilegi `CREATE JOB`. Si veus `ORA-27486: insufficient privileges`, qui administra la base de dades ha d'executar `GRANT CREATE JOB TO edugest;`. Els jobs amb `DBMS_SCHEDULER` substituïxen `DBMS_JOB`, el mecanisme antic que encara apareix en documentació vella.

**Cadenes de calendari.** Seguixen un format basat en l'estàndard iCalendar (RFC 5545): una freqüència (`FREQ`) i restriccions (`BY...`).

| Cadena | Quan s'executa |
|---|---|
| `FREQ=MINUTELY; INTERVAL=1` | Cada minut (per a proves) |
| `FREQ=HOURLY; INTERVAL=4` | Cada 4 hores |
| `FREQ=DAILY; BYHOUR=2; BYMINUTE=0` | Tots els dies a les 02:00 |
| `FREQ=WEEKLY; BYDAY=MON,TUE,WED,THU,FRI; BYHOUR=7; BYMINUTE=30` | De dilluns a divendres a les 07:30 |
| `FREQ=MONTHLY; BYMONTHDAY=1; BYHOUR=6` | El dia 1 de cada mes a les 06:00 |
| `FREQ=YEARLY; BYMONTH=9; BYMONTHDAY=1; BYHOUR=0` | L'1 de setembre, a mitjanit |

Oracle pot **calcular quan s'executaria** un calendari sense crear res, amb `EVALUATE_CALENDAR_STRING`. És la forma de comprovar que la cadena diu el que creus:

```sql
DECLARE
    v_proxima  TIMESTAMP WITH TIME ZONE;
BEGIN
    DBMS_SCHEDULER.EVALUATE_CALENDAR_STRING(
        calendar_string   => 'FREQ=WEEKLY; BYDAY=MON,TUE,WED,THU,FRI; BYHOUR=7; BYMINUTE=30',
        start_date        => NULL,
        return_date_after => TO_TIMESTAMP_TZ('14/05/2027 08:00 Europe/Madrid', 'DD/MM/YYYY HH24:MI TZR'),
        next_run_date     => v_proxima);
    DBMS_OUTPUT.PUT_LINE('Siguiente ejecución: ' || TO_CHAR(v_proxima, 'DD/MM/YYYY HH24:MI'));
END;
/
```

```text
Siguiente ejecución: 17/05/2027 07:30
```

El 14 de maig de 2027 és divendres i ja han passat les 07:30, així que la següent execució és el dilluns 17.

**Governar les tasques:**

| Tasca | Sentència |
|---|---|
| Executar ara, sense esperar | `EXEC DBMS_SCHEDULER.RUN_JOB('JOB_RESUMEN_NOCTURNO')` |
| Desactivar / activar | `EXEC DBMS_SCHEDULER.DISABLE('JOB_RESUMEN_NOCTURNO')` / `ENABLE` |
| Canviar el calendari | `EXEC DBMS_SCHEDULER.SET_ATTRIBUTE('JOB_RESUMEN_NOCTURNO', 'repeat_interval', 'FREQ=WEEKLY; BYDAY=MON,TUE,WED,THU,FRI; BYHOUR=7; BYMINUTE=30')` |
| Esborrar | `EXEC DBMS_SCHEDULER.DROP_JOB('JOB_RESUMEN_NOCTURNO')` |
| Veure les tasques i la seua pròxima execució | `SELECT job_name, enabled, state, last_start_date, next_run_date FROM user_scheduler_jobs;` |
| Veure l'historial d'execucions | `SELECT log_date, job_name, status, error#, additional_info FROM user_scheduler_job_run_details ORDER BY log_date DESC;` |

L'historial és l'eina de diagnòstic: cada execució queda registrada amb el seu `STATUS` (`SUCCEEDED` o `FAILED`) i, si falla, el codi d'error (`ERROR#`) i el seu text (`ADDITIONAL_INFO`).

> [!WARNING]
> Una tasca programada s'executa **sense ningú davant**: no hi ha pantalla on llegir un `DBMS_OUTPUT` ni a qui preguntar. Tres conseqüències: el procediment ha de fer el seu propi `COMMIT` (§10.4); ha de **registrar el seu resultat** en una taula de log; i cal **mirar l'historial** de tant en tant, perquè un job que falla cada nit no avisa ningú. I no oblides esborrar les tasques de prova (`DROP_JOB`): continuen executant-se al teu contenidor mentre existisca.

### 12.4 Tasques basades en esdeveniments

A més de les tasques per calendari, `DBMS_SCHEDULER` admet tasques **basades en esdeveniments**: s'executen quan una altra part del sistema envia un missatge a una cua (per exemple, quan arriba un fitxer o acaba una càrrega). Són tasques amb `event_condition` i `queue_spec` en lloc de `repeat_interval`. Queden fora de l'abast de la unitat, però convé saber que el planificador d'Oracle és, en realitat, un sistema de reaccions a esdeveniments, i no només un rellotge.

### 12.5 Equivalents en altres gestors

Ací la portabilitat és quasi nul·la: cada gestor resol les tasques programades de forma distinta, i dos d'ells ni tan sols les porten de sèrie.

{{< sgbd "MySQL / MariaDB" >}}

Són **esdeveniments** (`CREATE EVENT`), executats per l'*event scheduler*, que ha d'estar activat:

```sql
SET GLOBAL event_scheduler = ON;

CREATE EVENT ev_resumen_nocturno
ON SCHEDULE EVERY 1 DAY
STARTS (TIMESTAMP(CURRENT_DATE) + INTERVAL 1 DAY + INTERVAL 2 HOUR)
DO CALL pr_recalcular_resumen();
```

{{< sgbd "PostgreSQL" >}}

**No té planificador intern.** Les opcions són l'extensió **`pg_cron`**, l'agent **pgAgent** (de pgAdmin) o el `cron` del sistema operatiu:

```sql
-- Requerix instal·lar l'extensió pg_cron i carregar-la (shared_preload_libraries)
CREATE EXTENSION pg_cron;
SELECT cron.schedule('resumen-nocturno', '0 2 * * *', 'CALL pr_recalcular_resumen()');
```

{{< sgbd "SQL Server" >}}

Es programen amb **SQL Server Agent** (no disponible en l'edició Express) mitjançant procediments de `msdb`:

```sql
EXEC msdb.dbo.sp_add_job         @job_name = N'resumen_nocturno';
EXEC msdb.dbo.sp_add_jobstep     @job_name = N'resumen_nocturno', @step_name = N'recalcular',
                                 @subsystem = N'TSQL', @command = N'EXEC dbo.pr_recalcular_resumen;',
                                 @database_name = N'edugest';
EXEC msdb.dbo.sp_add_jobschedule @job_name = N'resumen_nocturno', @name = N'diario_2am',
                                 @freq_type = 4, @freq_interval = 1, @active_start_time = 020000;
EXEC msdb.dbo.sp_add_jobserver   @job_name = N'resumen_nocturno';
```

| | Oracle | MySQL / MariaDB | PostgreSQL | SQL Server |
|---|---|---|---|---|
| **Mecanisme** | `DBMS_SCHEDULER` (integrat) | `EVENT` (integrat) | `pg_cron` / pgAgent / `cron` (extern) | SQL Server Agent (servei apart) |
| **Calendari** | Cadena `FREQ=...` | `EVERY n unidad` | Expressió `cron` | Paràmetres `@freq_type`... |
| **Historial** | Vistes `*_SCHEDULER_JOB_RUN_DETAILS` | No guarda historial; cal registrar-lo | Taula `cron.job_run_details` | `msdb.dbo.sysjobhistory` |
| **Activació** | Per defecte actiu | `event_scheduler = ON` | Instal·lar i configurar l'extensió | Servei Agent en marxa |

---

## 13. Paquets

### 13.1 Què és un paquet

Un **paquet** agrupa subprogrames, constants, variables i tipus relacionats davall un mateix nom. És la unitat d'organització de PL/SQL (RA5.d, RA5.f): en lloc de vint procediments solts, un `pkg_secretaria` amb les operacions de la secretaria. Es compon de dues parts:

| Part | Què conté | Qui la veu |
|---|---|---|
| **Especificació** (*package specification*) | La **interfície pública**: capçaleres dels subprogrames i constants visibles | Tot el que tinga `EXECUTE` sobre el paquet |
| **Cos** (*package body*) | La **implementació** i els elements privats | Només el paquet |

Avantatges: un sol `GRANT EXECUTE`; es poden ocultar els detalls (el que no està en l'especificació és privat); les variables del paquet mantenen el seu valor durant la sessió; i canviar el cos no invalida els qui el criden, només canviar l'especificació.

### 13.2 Exemple: `pkg_informes`

{{< sgbd "Oracle 26ai" >}}

```sql
CREATE OR REPLACE PACKAGE pkg_informes AS
    c_aprobado  CONSTANT NUMBER(3,1) := 5;                       -- constant pública

    FUNCTION  alumnos_grupo (p_cod_grupo IN grupo.cod_grupo%TYPE) RETURN PLS_INTEGER;
    PROCEDURE resumen_grupo (p_cod_grupo IN grupo.cod_grupo%TYPE);
END pkg_informes;
/

CREATE OR REPLACE PACKAGE BODY pkg_informes AS

    -- Privada: no apareix en l'especificació, només la veuen els subprogrames del paquet
    FUNCTION media_grupo (p_cod_grupo IN grupo.cod_grupo%TYPE) RETURN NUMBER
    IS
        v_media  NUMBER;
    BEGIN
        SELECT ROUND(AVG(m.nota_final), 2)
        INTO   v_media
        FROM   matricula m JOIN alumno a ON a.id_alumno = m.id_alumno
        WHERE  a.cod_grupo = p_cod_grupo;
        RETURN v_media;
    END media_grupo;

    FUNCTION alumnos_grupo (p_cod_grupo IN grupo.cod_grupo%TYPE) RETURN PLS_INTEGER
    IS
        v_n  PLS_INTEGER;
    BEGIN
        SELECT COUNT(*) INTO v_n FROM alumno WHERE cod_grupo = p_cod_grupo;
        RETURN v_n;
    END alumnos_grupo;

    PROCEDURE resumen_grupo (p_cod_grupo IN grupo.cod_grupo%TYPE)
    IS
    BEGIN
        DBMS_OUTPUT.PUT_LINE('Grupo ' || p_cod_grupo || ': ' ||
                             alumnos_grupo(p_cod_grupo) || ' alumnos, media ' ||
                             NVL(TO_CHAR(media_grupo(p_cod_grupo)), 'sin notas'));
    END resumen_grupo;

END pkg_informes;
/
```

```sql
EXEC pkg_informes.resumen_grupo('2DAW')
EXEC pkg_informes.resumen_grupo('2ASIR')
SELECT pkg_informes.alumnos_grupo('1DAM') AS alumnos FROM dual;
```

```text
Grupo 2DAW: 5 alumnos, media 5.93
Grupo 2ASIR: 0 alumnos, media sin notas

   ALUMNOS
----------
         7
```

Es crida amb `paquete.elemento`. `media_grupo` no és accessible des de fora (`pkg_informes.media_grupo(...)` donaria `PLS-00302`); `alumnos_grupo` és pública i es pot usar fins i tot en una consulta SQL.

| Regla | Detall |
|---|---|
| Ordre en el cos | Un subprograma privat ha d'estar **declarat abans** que un altre l'use (per això `media_grupo` va primer) |
| Cos i especificació | Cada capçalera pública ha de coincidir **exactament** amb la seua implementació |
| Estat | Una variable o constant del paquet conserva el seu valor mentre dure la **sessió** de cada usuari |
| `ORA-04068` | Si recompiles un paquet amb estat mentre altres sessions l'estan usant, eixes sessions reben «existing state of packages has been discarded»; basta amb repetir la crida |
| Sobrecàrrega | Dins d'un paquet pot haver-hi diversos subprogrames amb el mateix nom i distints paràmetres |

> [!TIP]
> El repte de la [pràctica 9.8](/ud09-plsql/ud09-practicas#pràctica-98--repte-el-paquet-de-secretaria) consistix a construir `pkg_secretaria` amb `matricular`, `matricular_curso_completo`, `promocionar` i `media`. En el projecte, eixe paquet és l'**única via** de matrícula de la secretaria: té `EXECUTE` sobre ell però cap `INSERT` sobre `MATRICULA`. Així les regles del catàleg no es poden saltar amb una sentència directa.

---

## 14. Comparació amb altres gestors

PL/SQL és d'Oracle. Si demà treballes amb un altre gestor, els **conceptes** són els mateixos (variables, condicions, bucles, cursors, excepcions, disparadors); el que canvia és la sintaxi i algunes decisions de disseny. La taula marca el que és **específic de cada gestor**:

| | Oracle | PostgreSQL | MySQL / MariaDB | SQL Server |
|---|---|---|---|---|
| **Llenguatge** | PL/SQL | PL/pgSQL (i altres: PL/Python...) | SQL/PSM (rutines emmagatzemades) | Transact-SQL (T-SQL) |
| **Bloc anònim** | `DECLARE ... BEGIN ... END;` | `DO $$ ... $$;` | MariaDB: `BEGIN NOT ATOMIC ... END`; MySQL: no existix, cal crear una rutina | Un lot T-SQL, sense necessitat de bloc |
| **Variable** | `v_x NUMBER;` en `DECLARE` | `v_x numeric;` en `DECLARE` | `DECLARE v_x DECIMAL;` dins de `BEGIN` | `DECLARE @x DECIMAL;` |
| **Assignació** | `v_x := 1;` | `v_x := 1;` | `SET v_x = 1;` | `SET @x = 1;` |
| **Condicional** | `IF ... ELSIF ... END IF;` | `IF ... ELSIF ... END IF;` | `IF ... ELSEIF ... END IF;` | `IF ... ELSE ...` (amb `BEGIN/END`) |
| **Bucles** | `LOOP`, `WHILE`, `FOR` | `LOOP`, `WHILE`, `FOR` | `LOOP`, `WHILE`, `REPEAT` | Només `WHILE` |
| **Paràmetres** | `IN`, `OUT`, `IN OUT` | `IN`, `OUT`, `INOUT` | `IN`, `OUT`, `INOUT` | `@p tipo [OUTPUT]` |
| **Crida** | `EXEC` / `CALL` | `CALL` | `CALL` | `EXEC` |
| **Cursors** | `CURSOR`, cursor `FOR` | `FOR r IN SELECT ... LOOP` o cursor explícit | Cursor explícit amb `HANDLER ... NOT FOUND` | Cursor explícit amb `@@FETCH_STATUS` |
| **Capturar errors** | `EXCEPTION WHEN ...` | `EXCEPTION WHEN ...` | `DECLARE HANDLER FOR ...` | `TRY ... CATCH` |
| **Error propi** | `RAISE_APPLICATION_ERROR(-20xxx, ...)` | `RAISE EXCEPTION '...'` | `SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = ...` | `THROW 50000, '...', 1` |
| **Disparadors** | Fila i sentència; `BEFORE`/`AFTER`/`INSTEAD OF`; `:NEW`/`:OLD`; compostos | Fila i sentència; funció de disparador a banda; `NEW`/`OLD` | Només de fila; `BEFORE`/`AFTER`; `NEW.`/`OLD.`; sense `INSTEAD OF` | Només de sentència; `AFTER`/`INSTEAD OF`; taules `inserted` i `deleted` |
| **Taula mutant** | Sí (`ORA-04091`) | No existix com a error | Sí (error 1442) | No (el disparador veu el lot complet) |
| **Paquets** | Sí | No (esquemes i extensions) | No | No (esquemes) |
| **Tasques programades** | `DBMS_SCHEDULER` | `pg_cron` / `cron` | `CREATE EVENT` | SQL Server Agent |

### 14.1 La mateixa funció en quatre gestors

La funció `fn_calificacion` de §8.3 escrita en cadascun. Fixa't en què canvia: la capçalera, la manera de declarar el tipus tornat i els separadors del bloc; la lògica (`CASE`) és idèntica.

{{< sgbd "PostgreSQL 17" >}}

```sql
CREATE OR REPLACE FUNCTION fn_calificacion(p_nota NUMERIC) RETURNS TEXT
LANGUAGE plpgsql IMMUTABLE
AS $$
BEGIN
    RETURN CASE
               WHEN p_nota IS NULL THEN 'NC'
               WHEN p_nota < 5     THEN 'Insuficiente'
               WHEN p_nota < 6     THEN 'Suficiente'
               WHEN p_nota < 7     THEN 'Bien'
               WHEN p_nota < 9     THEN 'Notable'
               ELSE                     'Sobresaliente'
           END;
END;
$$;
```

{{< sgbd "MySQL / MariaDB" >}}

```sql
DELIMITER //
CREATE FUNCTION fn_calificacion(p_nota DECIMAL(4,2)) RETURNS VARCHAR(15)
DETERMINISTIC
BEGIN
    RETURN CASE
               WHEN p_nota IS NULL THEN 'NC'
               WHEN p_nota < 5     THEN 'Insuficiente'
               WHEN p_nota < 6     THEN 'Suficiente'
               WHEN p_nota < 7     THEN 'Bien'
               WHEN p_nota < 9     THEN 'Notable'
               ELSE                     'Sobresaliente'
           END;
END //
DELIMITER ;
```

`DELIMITER` és una ordre del client `mysql`: canvia temporalment el terminador perquè el `;` interior no tanque la rutina, el mateix problema que la `/` d'Oracle.

{{< sgbd "SQL Server" >}}

```sql
CREATE OR ALTER FUNCTION dbo.fn_calificacion (@nota DECIMAL(4,2))
RETURNS VARCHAR(15)
AS
BEGIN
    RETURN CASE
               WHEN @nota IS NULL THEN 'NC'
               WHEN @nota < 5     THEN 'Insuficiente'
               WHEN @nota < 6     THEN 'Suficiente'
               WHEN @nota < 7     THEN 'Bien'
               WHEN @nota < 9     THEN 'Notable'
               ELSE                    'Sobresaliente'
           END;
END;
```

### 14.2 El mateix disparador d'auditoria en tres gestors

El disparador `trg_auditoria_nota` (§11.2) en els altres tres gestors. La diferència més visible està en com cadascun accedix als valors abans i després del canvi.

{{< sgbd "PostgreSQL 17" >}}

```sql
-- En PostgreSQL el disparador són DOS objectes: una funció i el trigger que la invoca
CREATE OR REPLACE FUNCTION fn_trg_auditoria_nota() RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.nota_final IS DISTINCT FROM OLD.nota_final THEN
        INSERT INTO auditoria_nota (id_matricula, nota_anterior, nota_nueva, usuario)
        VALUES (OLD.id_matricula, OLD.nota_final, NEW.nota_final, current_user);
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_auditoria_nota
AFTER UPDATE OF nota_final ON matricula
FOR EACH ROW EXECUTE FUNCTION fn_trg_auditoria_nota();
```

{{< sgbd "MySQL / MariaDB" >}}

```sql
-- Sense "UPDATE OF columna" ni WHEN: la condició va dins del cos.
-- "<=>" és la igualtat que tracta NULL com un valor més.
DELIMITER //
CREATE TRIGGER trg_auditoria_nota
AFTER UPDATE ON matricula
FOR EACH ROW
BEGIN
    IF NOT (NEW.nota_final <=> OLD.nota_final) THEN
        INSERT INTO auditoria_nota (id_matricula, nota_anterior, nota_nueva, usuario)
        VALUES (OLD.id_matricula, OLD.nota_final, NEW.nota_final, CURRENT_USER());
    END IF;
END //
DELIMITER ;
```

{{< sgbd "SQL Server" >}}

```sql
-- Dispara una vegada per SENTÈNCIA: no hi ha :NEW/:OLD sinó les taules "inserted" i "deleted",
-- amb totes les files afectades. Es treballa en conjunt, no fila a fila.
CREATE OR ALTER TRIGGER trg_auditoria_nota
ON matricula
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    INSERT INTO auditoria_nota (id_matricula, nota_anterior, nota_nueva, usuario)
    SELECT d.id_matricula, d.nota_final, i.nota_final, SUSER_SNAME()
    FROM   deleted d
           JOIN inserted i ON i.id_matricula = d.id_matricula
    WHERE  ISNULL(i.nota_final, -1) <> ISNULL(d.nota_final, -1);
END;
```

> [!NOTE]
> El disseny de SQL Server és un canvi de mentalitat: no existix el disparador de fila, així que **el problema de la taula mutant no es planteja**, però cal pensar sempre en conjunts de files. I en MySQL/MariaDB, en no existir `INSTEAD OF` ni disparadors de sentència, les regles de diverses files (R4, R5) s'implementen normalment amb procediments que controlen l'accés.

---

## 15. Errors freqüents

| Símptoma | Causa | Solució |
|---|---|---|
| El bloc «funciona» però no mostra res | Falta `SET SERVEROUTPUT ON` o el panell d'eixida està tancat | Activa'l en cada sessió (§2.4) |
| SQLcl es queda esperant després d'escriure el bloc | Falta la `/` final | Escriu-la en una línia sola (§2.3) |
| `PLS-00103: Encountered the symbol ...` | `;` oblidat, `END IF` o `END LOOP` sense tancar, coma sobrant | Revisa la línia que indica i l'anterior (§2.5) |
| `PLS-00428: an INTO clause is expected` | `SELECT` en un bloc sense `INTO` ni cursor | Afig `INTO` o usa un cursor `FOR` |
| `Warning: ... created with compilation errors` | El subprograma té errors `PLS-` | `SHOW ERRORS` o `USER_ERRORS` |
| `ORA-01403: no data found` | `SELECT ... INTO` sense files | Tracta `NO_DATA_FOUND` o usa un agregat (§9.2) |
| `ORA-01422: exact fetch returns more than requested number of rows` | `SELECT ... INTO` amb diverses files | Concreta el `WHERE` o usa un cursor (§7) |
| La condició `WHERE id_alumno = id_alumno` torna totes les files | Paràmetre o variable amb el mateix nom que la columna | Prefixos `p_` i `v_` (§3.4) |
| Un `IF x > 5 ... ELSE` marca com a suspés qui no té nota | La comparació amb `NULL` és desconeguda i cau en l'`ELSE` | Pregunta primer `IS NULL` (§5.1) |
| L'últim registre del cursor ix duplicat | `EXIT WHEN c%NOTFOUND` col·locat després d'usar les variables | Just després del `FETCH` (§7.2) |
| `ORA-01000: maximum open cursors exceeded` | Cursors explícits sense `CLOSE` | Tanca sempre, o usa cursor `FOR` |
| `ORA-14551: cannot perform a DML operation inside a query` | Funció amb `INSERT`/`UPDATE` cridada des d'un `SELECT` | Convertix-la en procediment (§8.6) |
| `ORA-04091: table is mutating` | Disparador de fila que llig la seua pròpia taula | Disparador compost (§11.6) |
| `ORA-04092: cannot COMMIT in a trigger` | `COMMIT` o `ROLLBACK` dins d'un disparador | Lleva'l; el disparador va en la transacció de la sentència |
| `ORA-04084: cannot change NEW values for this trigger type` | Assignar `:NEW` en un `AFTER` | Usa un `BEFORE` |
| `ORA-04088` + `ORA-20xxx` | El disparador ha rebutjat la sentència a propòsit | La causa és l'`ORA-20xxx`: llig el seu missatge |
| `ORA-06510: unhandled user-defined exception` | `RAISE` d'una excepció pròpia sense manejador | Tracta-la o usa `RAISE_APPLICATION_ERROR` |
| `ORA-27486: insufficient privileges` en crear un job | Falta el privilegi `CREATE JOB` | `GRANT CREATE JOB TO edugest;` per part d'administració |
| `ORA-04068: existing state of packages has been discarded` | Es va recompilar un paquet amb estat mentre s'usava | Repetix la crida |
| `WHEN OTHERS THEN NULL` i dades que no quadren | Un error s'ha empassat en silenci | Registra i rellança amb `RAISE;` (§9.3) |
| Els canvis del procediment no apareixen en una altra sessió | Falta el `COMMIT` (que, per disseny, el procediment no fa) | Confirma des de qui el crida (§10.4) |

---

## 16. Bones pràctiques

- **Una sentència SQL abans que un bucle.** Si la tasca cap en un `UPDATE` o un `INSERT ... SELECT`, no l'escrigues amb un cursor (§7.7).
- **Usa `%TYPE` i `%ROWTYPE`** en lloc de repetir els tipus de les columnes.
- **Prefixos en els noms** (`v_`, `p_`, `c_`, `r_`, `e_`) per a no confondre variables, paràmetres i columnes.
- **Escriu sempre l'`ELSE`** d'un `CASE` i la branca `IS NULL` de les condicions que manegen dades que puguen faltar.
- **Un cursor `FOR` abans que un d'explícit**, tret que necessites el control fi d'`OPEN`/`FETCH`/`CLOSE`.
- **Una funció calcula i no modifica dades; un procediment fa.** Les funcions que es criden des de SQL han de ser pures.
- **Tracta només els errors que saps tractar.** Res de `WHEN OTHERS THEN NULL`: registra i torna a llançar amb `RAISE;`.
- **Defineix un catàleg d'errors propis** (`-20010`...), amb un codi per regla i un missatge que diga quina dada ha fallat.
- **No facis `COMMIT` en les operacions de negoci** que altres criden; sí en les tasques desateses.
- **Si has de desfer una part, usa `SAVEPOINT`** de forma explícita; no depengues del que ocorregue de forma implícita.
- **Una regla, un disparador; cada disparador curt.** Comenta quina restricció del catàleg implementa i escriu una prova per a cadascuna.
- **Abans d'un disparador, pregunta't si basta un `CHECK`, un `DEFAULT`, una clau aliena o un procediment** (§11.9).
- **Concedix `EXECUTE` sobre el procediment en lloc d'`INSERT` sobre la taula** quan la regla de negoci importe.
- **Una tasca programada registra el seu resultat** en una taula i es revisa el seu historial. No oblides esborrar les de prova.
- **Cada objecte en el seu propi `.sql`**, amb `CREATE OR REPLACE`, acabat en `/` i sota control de versions.
- **Marca en la documentació el que és específic d'Oracle** si el codi s'ha de portar a un altre gestor.

---

{{< tarjetas titulo="Repassa els termes de la UD09" >}}
- t: "Bloc anònim"
  d: "Codi PL/SQL sense nom: DECLARE, BEGIN, EXCEPTION, END."
- t: "Procediment"
  d: "Subprograma emmagatzemat amb nom que realitza una acció."
- t: "Funció"
  d: "Subprograma emmagatzemat que torna un valor i es pot usar en SQL."
- t: "Cursor"
  d: "Punter que recorre les files d'una consulta una a una."
- t: "Excepció"
  d: "Error controlat en la secció EXCEPTION."
- t: "Trigger"
  d: "Codi que s'executa automàticament davant d'un esdeveniment DML, DDL o de sistema."
- t: "Paquet"
  d: "Agrupació de procediments, funcions i variables relacionats."
{{< /tarjetas >}}

## 17. Resum

| Concepte | Idea clau | Sintaxi essencial |
|---|---|---|
| Formes d'automatitzar | Guió, bloc anònim, funció, procediment, paquet, disparador i tasca programada: es distingixen per **on viuen** i **què els executa** | — |
| Execució de guions | Les ordres de client (`SET`, `SPOOL`, `@`) no les entén el servidor; els blocs PL/SQL acaben en `;` i `/` | `@fichero.sql`, `SET SERVEROUTPUT ON` |
| Bloc | `DECLARE` (opcional), `BEGIN` ... `EXCEPTION` (opcional) ... `END;` | `DECLARE ... BEGIN ... END;` |
| Variables | Amb tipus, heretables de la taula amb `%TYPE` i `%ROWTYPE`. Distintes de les variables de **substitució** (`&`), que resol el client | `v_x tabla.col%TYPE;`, `SELECT ... INTO` |
| Control de flux | `IF`/`ELSIF`, `CASE`, `LOOP`/`WHILE`/`FOR`; compte amb `NULL` | `IF ... THEN ... END IF;` |
| Funcions del gestor | Les de SQL funcionen en PL/SQL (excepte agregades, analítiques i `DECODE`); `NVL` i `SYSDATE` són d'Oracle | `NVL`, `TO_CHAR`, `MONTHS_BETWEEN` |
| Cursors | Implícit (`SQL%ROWCOUNT`), explícit (`OPEN`/`FETCH`/`CLOSE`), `FOR`, amb paràmetres | `FOR r IN (SELECT ...) LOOP` |
| Funcions d'usuari | Tornen un valor i s'usen en SQL; sense DML si es criden des d'una consulta | `CREATE OR REPLACE FUNCTION ... RETURN` |
| Procediments | Fan alguna cosa; paràmetres `IN`, `OUT`, `IN OUT`; `EXECUTE` en lloc d'`INSERT` directe | `CREATE OR REPLACE PROCEDURE` |
| Excepcions | Predefinides, pròpies, `PRAGMA EXCEPTION_INIT`; `RAISE_APPLICATION_ERROR` entre -20000 i -20999 | `EXCEPTION WHEN ... THEN` |
| Disparadors | S'executen sols davant d'un esdeveniment; `:NEW`/`:OLD`; `BEFORE` modifica, `AFTER` audita; `INSTEAD OF` en vistes | `CREATE TRIGGER ... FOR EACH ROW` |
| Taula mutant | Un disparador de fila no pot llegir la seua taula (`ORA-04091`); es resol anotant en `AFTER EACH ROW` i comprovant en `AFTER STATEMENT` | `COMPOUND TRIGGER` |
| Tasques programades | Un calendari + una acció; sense ningú davant: cal registrar i vigilar | `DBMS_SCHEDULER.CREATE_JOB` |
| Paquets | Especificació (interfície) i cos (implementació); elements privats | `CREATE PACKAGE` / `PACKAGE BODY` |
| Altres gestors | Mateixos conceptes, sintaxi distinta; els disparadors i les tasques programades són el que més canvia | PL/pgSQL, SQL/PSM, T-SQL |

Idees que convé endur-se gravades:

1. **El que es guarda en la base de dades es compila una vegada.** La resta s'analitza cada vegada.
2. **Un `&` el resol el client; un `v_` el resol el servidor.**
3. **L'excepció més perillosa és la que s'empassa en silenci.**
4. **Una operació de negoci no confirma; qui la crida decidix.** Una tasca desatesa sí.
5. **Un disparador és una restricció que s'executa sola:** xicotet, amb un únic propòsit i amb la seua prova.
6. **Si necessites llegir la taula que estàs modificant, no ho facis fila a fila:** anota en la fila i comprova al final.

---

## 18. Autoavaluació

{{< quiz >}}
- q: "Què distingix una funció d'un procediment emmagatzemat?"
  options: ["La funció no pot tindre paràmetres", "La funció torna un valor i es pot usar dins d'un `SELECT`; el procediment realitza una acció", "El procediment no es guarda en la base de dades", "La funció només pot ser cridada des d'un disparador"]
  answer: 1
  explain: "Tots dos són subprogrames emmagatzemats amb paràmetres. La funció acaba amb `RETURN` i pot formar part d'una expressió SQL; el procediment s'invoca com una instrucció i torna informació, si de cas, per paràmetres `OUT`."
- q: "Un script usa `WHERE cod_grupo = '&grupo'`. Quina afirmació és correcta?"
  options: ["`&grupo` és una variable PL/SQL declarada en el servidor", "El client substituïx `&grupo` abans d'enviar el text al servidor", "El valor canvia en cada volta d'un bucle", "Funciona igual dins d'un procediment emmagatzemat"]
  answer: 1
  explain: "Una variable de substitució és text que el client apega al codi abans d'enviar-lo. Per això no existix en un procediment emmagatzemat ni canvia dins d'un bucle."
- q: "Què fa `SELECT AVG(nota_final) INTO v_media FROM matricula WHERE id_alumno = 30;` si l'alumne 30 no té matrícules?"
  options: ["Llança `NO_DATA_FOUND`", "Llança `TOO_MANY_ROWS`", "Assigna `NULL` a `v_media`, sense error", "Assigna 0 a `v_media`"]
  answer: 2
  explain: "Un agregat sense `GROUP BY` torna sempre exactament una fila, encara que no hi haja dades d'entrada. `AVG` de cap valor és `NULL`: no hi ha excepció, i `v_media` queda a `NULL`."
- q: "En un bucle amb un cursor explícit, per què s'escriu `EXIT WHEN c%NOTFOUND` just després del `FETCH`?"
  options: ["Perquè el cursor es tanca sol", "Perquè el `FETCH` sense fila no modifica les variables i es repetiria l'última", "Perquè `%NOTFOUND` només val després del `CLOSE`", "Perquè és obligatori per sintaxi"]
  answer: 1
  explain: "El `FETCH` que no troba fila deixa les variables amb els valors anteriors. Si es processen abans de comprovar `%NOTFOUND`, l'última fila es tracta dues vegades."
- q: "`RAISE_APPLICATION_ERROR(-20013, 'Ya matriculado')` dins de `pr_matricular` provoca…"
  options: ["Un `COMMIT` automàtic", "Un error `ORA-20013` que es propaga al qui crida, que pot tractar-lo", "La desactivació del procediment", "Que l'`INSERT` es confirme igualment"]
  answer: 1
  explain: "L'error detén el procediment i arriba al qui crida amb eixe codi i missatge. No confirma res; la sentència que va invocar el procediment es desfà si ningú el tracta."
- q: "Un procediment tracta una excepció amb `WHEN OTHERS THEN DBMS_OUTPUT.PUT_LINE('error');` i acaba. Què passa amb el que va fer abans de l'error?"
  options: ["Oracle ho desfà sempre", "Es queda fet: tractar l'excepció evita el rollback implícit", "Es confirma amb `COMMIT`", "Depén del valor de `SERVEROUTPUT`"]
  answer: 1
  explain: "Si l'excepció es tracta i el bloc acaba amb normalitat, Oracle no desfà res. Per a desfer una part fa falta un `SAVEPOINT` i un `ROLLBACK TO` en el manejador, i normalment rellançar l'error amb `RAISE;`."
- q: "Quin d'estos disparadors pot modificar el valor que es va a guardar?"
  options: ["`AFTER UPDATE FOR EACH ROW`", "`BEFORE INSERT FOR EACH ROW`", "`AFTER STATEMENT`", "Cap: `:NEW` és de només lectura"]
  answer: 1
  explain: "Només un disparador `BEFORE` de fila pot assignar a `:NEW`. En un `AFTER`, Oracle torna `ORA-04084`."
- q: "Per a implementar «un grup no pot superar els 30 alumnes» sense `ORA-04091`, la solució habitual és…"
  options: ["Un `CHECK` sobre `cod_grupo`", "`AFTER EACH ROW` amb `SELECT COUNT(*)`", "Un disparador compost: anotar el grup en `AFTER EACH ROW` i comptar en `AFTER STATEMENT`", "Desactivar el disparador durant la càrrega"]
  answer: 2
  explain: "Un `CHECK` no pot mirar altres files. El disparador de fila que compta provoca la taula mutant. El compost anota durant la sentència i consulta al final, quan la taula ja no està mutant."
- q: "Quin avantatge de seguretat té concedir `EXECUTE` sobre `pr_matricular` en lloc d'`INSERT` sobre `MATRICULA`?"
  options: ["Cap: són equivalents", "L'única via de matricular passa per les validacions del procediment", "L'usuari pot esborrar matrícules sense control", "El procediment s'executa amb els privilegis de qui el crida"]
  answer: 1
  explain: "Per defecte un procediment s'executa amb els privilegis del seu propietari. Així la secretaria pot matricular, però només a través del procediment, que aplica les regles del catàleg."
- q: "Una tasca creada amb `DBMS_SCHEDULER` falla cada nit. On es veu la causa?"
  options: ["En el búfer de `DBMS_OUTPUT`", "En `USER_SCHEDULER_JOB_RUN_DETAILS` (columnes `STATUS`, `ERROR#` i `ADDITIONAL_INFO`)", "En la pantalla de qui va crear la tasca", "En cap lloc: les tasques no guarden historial"]
  answer: 1
  explain: "L'historial d'execucions registra l'estat de cada vegada i, si falla, el codi i el text de l'error. Com que ningú mira l'eixida d'una tasca desatesa, la revisió periòdica de l'historial és imprescindible."
{{< /quiz >}}

## Referències

- [Oracle AI Database 26ai: Database PL/SQL Language Reference](https://docs.oracle.com/en/database/oracle/oracle-database/26/lnpls/) — blocs, variables, control de flux, cursors, subprogrames, paquets, excepcions i disparadors (inclosos els compostos i la restricció de la taula mutant).
- [Oracle AI Database 26ai: Database PL/SQL Packages and Types Reference, *DBMS_OUTPUT*](https://docs.oracle.com/en/database/oracle/oracle-database/26/arpls/DBMS_OUTPUT.html).
- [Oracle AI Database 26ai: Database PL/SQL Packages and Types Reference, *DBMS_SCHEDULER*](https://docs.oracle.com/en/database/oracle/oracle-database/26/arpls/DBMS_SCHEDULER.html) — tasques, calendaris i `EVALUATE_CALENDAR_STRING`.
- [Oracle AI Database 26ai: Database Administrator's Guide, *Scheduling Jobs with Oracle Scheduler*](https://docs.oracle.com/en/database/oracle/oracle-database/26/admin/scheduling-jobs-with-oracle-scheduler.html).
- [Oracle AI Database 26ai: SQL*Plus User's Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/26/sqpug/) — variables de substitució, `SET SERVEROUTPUT`, `SPOOL` i execució de guions.
- [Oracle SQLcl: documentación](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/) y [Oracle SQL Developer](https://docs.oracle.com/en/database/oracle/sql-developer/).
- [Oracle AI Database 26ai: Database Error Messages](https://docs.oracle.com/en/error-help/db/) — `ORA-04091`, `ORA-04088`, `ORA-01403`, `ORA-02292`, `ORA-27486`...
- [Oracle AI Database 26ai: Database Concepts, *Data Concurrency and Consistency*](https://docs.oracle.com/en/database/oracle/oracle-database/26/cncpt/data-concurrency-and-consistency.html) — consistència de lectura, rellevant per als disparadors.
- [PostgreSQL: PL/pgSQL](https://www.postgresql.org/docs/current/plpgsql.html) y [`pg_cron`](https://github.com/citusdata/pg_cron).
- [MySQL: Stored Objects](https://dev.mysql.com/doc/refman/8.4/en/stored-objects.html) y [MariaDB: Events](https://mariadb.com/kb/en/events/).
- [Microsoft: Transact-SQL, disparadors i SQL Server Agent](https://learn.microsoft.com/sql/t-sql/).
- [Real Decreto 405/2023, de 29 de mayo](https://www.boe.es/buscar/act.php?id=BOE-A-2023-13221) — ensenyaments mínims del mòdul 0484 Bases de dades (RA5, i els criteris RA4.d, RA4.h i RA6.h).
