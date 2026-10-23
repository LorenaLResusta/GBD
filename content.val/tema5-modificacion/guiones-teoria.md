---
title: "Teoria · Guions de sentències"
weight: 20
bookToc: true
---

# Tema 5 · Guions de sentències

## Resum del tema

Fins ara, cada modificació s'ha escrit com una sentència solta. Però les tasques reals del centre (donar d'alta l'alumnat nou, passar de curs, carregar notes) són **seqüències de sentències** que cal executar en ordre, que no han de deixar la base de dades a mitges si alguna cosa falla i que es repetixen cada curs. Eixes tasques s'escriuen com a **guions** (*scripts*): fitxers que es poden llegir, revisar, repetir i auditar.

Quan el guió necessita **decidir** (té l'alumne faltes suficients per a perdre l'avaluació contínua?), **repetir** (recórrer tots els alumnes d'un grup) o **reaccionar a un error** (què faig si el mòdul no existix?), SQL per si sol no basta. Oracle oferix per a això **PL/SQL** (*Procedural Language / SQL*): SQL més variables, condicions, bucles i excepcions, organitzat en **blocs** que s'inclouen dins del guió.

El tema avança en quatre passos: primer quines formes hi ha d'automatitzar i amb quines eines es treballa (§1 i §2); després el bloc PL/SQL, les variables i el control de flux (§3 a §5); a continuació el tractament d'errors amb excepcions (§6); i finalment com es dissenya un **guió de manteniment** professional: transaccional, repetible i comprovable (§7).

Tots els exemples s'executen sobre l'esquema de referència **EDUGEST** amb els [scripts del projecte](/guia/proyecto-edugest#4-scripts-descarregables) carregats (32 alumnes, 143 matrícules, 46 faltes) i usen la sintaxi d'**Oracle AI Database 26ai Free**. Cada exemple indica l'eixida que has d'obtindre. Quan alguna cosa és pròpia d'un gestor concret se senyala amb una etiqueta o una nota.

{{< ra "RA5:e" >}}

### Objectius d'aprenentatge

En acabar este tema seràs capaç de:

- Distingir un guió d'un bloc anònim i triar la forma d'automatització adequada per a cada tasca.
- Editar i executar guions amb SQL Developer, SQLcl o SQL\*Plus, usant variables de substitució i l'eixida de `DBMS_OUTPUT`.
- Escriure blocs PL/SQL amb variables, constants i tipus `%TYPE` i `%ROWTYPE`, i distingir les variables de substitució del client de les variables PL/SQL del servidor.
- Aplicar estructures de control de flux (`IF`, `CASE`, `LOOP`, `WHILE`, `FOR`).
- Tractar errors amb excepcions predefinides i pròpies, `PRAGMA EXCEPTION_INIT` i `RAISE_APPLICATION_ERROR`.
- Dissenyar guions de manteniment transaccionals, repetibles i verificables.

### Temporalització

Esta part del tema ocupa **16 hores d'aula** (8 de teoria i 8 de pràctica). Desenvolupa el criteri RA5.e (*dissenyar guions de sentències per a dur a terme tasques complexes*) i s'hi apoya en el que s'ha vist al tema 5. Les pràctiques llargues i el projecte es completen fora de l'horari d'aula.

{{< sesiones unidad="T5" horas="16" parte="Guions de sentències" >}}
items:
  - {h: 2, tipo: T, t: "Formes d'automatitzar, eines i execució de guions", ref: "§1 i §2"}
  - {h: 2, tipo: T, t: "Bloc PL/SQL, variables i tipus", ref: "§3 i §4"}
  - {h: 2, tipo: P, t: "Primers blocs: l'expedient d'un alumne", ref: "Pràctica 5.7"}
  - {h: 1, tipo: T, t: "Estructures de control de flux", ref: "§5"}
  - {h: 1, tipo: T, t: "Excepcions", ref: "§6"}
  - {h: 2, tipo: P, t: "Matrícula amb excepcions", ref: "Pràctica 5.8"}
  - {h: 2, tipo: T, t: "Guions de manteniment: estructura, idempotència i proves", ref: "§7"}
  - {h: 3, tipo: P, t: "Repte: guió de promoció de curs", ref: "Pràctica 5.9"}
  - {h: 1, tipo: P, t: "Guions de manteniment d'EduGest", ref: "Projecte EduGest-5"}
autonomo:
  - "Acabar a casa el que no haja donat temps de les pràctiques 5.7 i 5.8"
  - "Exercicis resolts i autoavaluació"
{{< /sesiones >}}

> [!IMPORTANT]
> Treballa sempre connectat com a `EDUGEST` i amb l'eixida activada (`SET SERVEROUTPUT ON`). Tot el codi d'este tema es prova amb un mètode fix:
>
> 1. **Prediu** què ha de mostrar o tornar abans d'executar-lo.
> 2. Executa i compara amb l'eixida que figura en els apunts.
> 3. Si falla, llig l'error **d'amunt a avall**: el primer missatge (`PLS-` en compilació, `ORA-` en execució) és la causa; els següents només diuen on va ocórrer.
> 4. Guarda cada guió en el seu propi fitxer `.sql`: així es repetix i es versiona.

---


{{< sesion n="1" h="2" tipo="t" >}}Formes d'automatitzar, eines i execució de guions{{< /sesion >}}

## 1. Programar dins del servidor

### 1.1 Quin problema resol

SQL és un llenguatge **declaratiu**: dius *què* vols, no *com* obtindre-ho. És excel·lent per a consultar i modificar conjunts de files, però no té variables, ni condicions, ni bucles, ni forma de reaccionar a un error. Tan prompte una tasca necessita alguna d'eixes coses, hi ha dues opcions: traure les dades a una aplicació i programar allí la lògica, o **programar-la dins de la base de dades**.

Pensa en la matrícula d'un alumne a EduGest. Abans d'inserir la fila cal comprovar que l'alumne existix i té grup, que el mòdul és del seu cicle, que no està ja matriculat eixe curs i que no ha esgotat les quatre convocatòries. Són quatre consultes, tres decisions i un `INSERT`: això ja no és una sentència, és un xicotet programa.

### 1.2 Formes d'automatitzar tasques

El criteri RA5.e demana dissenyar **guions** que automatitzen tasques complexes. En Oracle hi ha dues formes d'escriure'ls:

| Forma | Què és | Quan s'executa | Exemple a EduGest |
|---|---|---|---|
| **Guió** (*script*) | Fitxer de text amb sentències SQL i ordres del client | Quan algú el llança (`@fichero.sql`) | `edugest_01_esquema.sql` |
| **Bloc anònim** | Bloc PL/SQL sense nom que el client envia al servidor | Quan el client l'envia; no es guarda | Un càlcul puntual de comprovació |

Un guió pot contindre blocs anònims. Fora del servidor existixen altres formes de llançar-los, també vàlides: el programador de tasques del sistema operatiu (`cron`, Programador de tasques de Windows) executant SQLcl, o la pròpia aplicació.

### 1.3 Què és PL/SQL

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

Cada pas d'un motor a l'altre (*context switch*) té un cost xicotet però mesurable. Per això, quan una tasca es pot escriure com **una sola sentència SQL**, eixa és quasi sempre la millor versió.

{{< sgbd "Oracle 26ai" >}}

PL/SQL és propi d'Oracle. Cada gestor té el seu llenguatge: PostgreSQL usa **PL/pgSQL**, MySQL i MariaDB usen el llenguatge de rutines emmagatzemades **SQL/PSM**, SQL Server usa **Transact-SQL (T-SQL)**. Els conceptes (variables, condicions, bucles, excepcions) són els mateixos; la sintaxi canvia.

---

## 2. Eines i execució de guions

### 2.1 Eines per a editar guions

El criteri RA5.e demana identificar les eines disponibles. Un guió PL/SQL és text: es pot escriure en qualsevol editor, però les eines especialitzades aporten ressaltat, execució directa i accés al diccionari de dades.

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

El criteri RA5.e demana reconéixer els mètodes d'execució de guions. Un guió pot executar-se de diverses maneres:

| Mètode | On | Què fa |
|---|---|---|
| `@ruta/fichero.sql` | SQLcl, SQL\*Plus | Executa el guió. La ruta és relativa al directori actual |
| `@@fichero.sql` | SQLcl, SQL\*Plus | Executa el guió **relatiu al guió que el crida**: útil en un guió mestre que n'invoca altres |
| `START fichero.sql` | SQLcl, SQL\*Plus | Sinònim de `@` |
| `sql edugest@servicio @fichero.sql` | Terminal | Es connecta i executa el guió en mode *batch* (sense interacció) |
| `F5` (*Executar script*) | SQL Developer | Executa **tot** el guió tal qual; `Ctrl+Intro` executa només la sentència sota el cursor |


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
| Bloc PL/SQL anònim | `;` **i** `/` en una línia sola | Dins del bloc hi ha molts `;`, així que el `;` ja no servix per a saber on acaba. La `/` diu «el bloc acaba ací, envia'l» |

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
> `DBMS_OUTPUT` és una eina de **depuració i de pràctiques**, no un mecanisme de producció: el text només existix mentre dura l'execució, es mostra al final (no mentre el bloc treballa) i un procediment que s'executa des d'una aplicació o una tasca programada no té ningú al davant per a llegir-lo. Per a deixar constància cal escriure en una **taula de registre** (pràctica 5.13).

### 2.5 Errors de compilació

Un bloc PL/SQL es **compila en enviar-se** al servidor. Si hi ha errors, no s'executa: Oracle torna un `ORA-06550` amb la línia i la columna i, a continuació, el missatge `PLS-` que explica la causa:

```text
ORA-06550: line 4, column 5:
PLS-00201: identifier 'V_NOTA' must be declared
ORA-06550: line 4, column 5:
PL/SQL: Statement ignored
```

| Missatge | Causa habitual |
|---|---|
| `PLS-00103: Encountered the symbol "..." when expecting one of the following` | Error de sintaxi: un `;` oblidat, un `END IF` sense tancar, una coma sobrant |
| `PLS-00201: identifier 'X' must be declared` | Nom mal escrit o variable no declarada |
| `PLS-00302: component 'X' must be declared` | S'usa una columna o un camp que no existix (`r_alumno.telefon`) |
| `PLS-00306: wrong number or types of arguments in call to 'X'` | Crida amb més, menys o distints paràmetres dels declarats |
| `PLS-00428: an INTO clause is expected in this SELECT statement` | Un `SELECT` dins d'un bloc sense `INTO` |
| `PLS-00363: expression 'X' cannot be used as an assignment target` | S'assigna a una constant, a un paràmetre `IN` o a l'índex d'un bucle `FOR` |

---

{{% curiosidad titulo="PL/SQL s'assembla a Ada" %}}
La sintaxi de PL/SQL (`BEGIN … END;`, `:=`, `IF … THEN … END IF;`, les excepcions) està inspirada en el llenguatge **Ada**. Va aparéixer a finals dels anys huitanta, per a poder ficar lògica de programa dins del servidor i no només sentències soltes.
{{% /curiosidad %}}

{{< sesion n="2" h="2" tipo="t" >}}Bloc PL/SQL, variables i tipus{{< /sesion >}}

## 3. Estructura d'un bloc PL/SQL

### 3.1 Les quatre seccions

Tot programa PL/SQL es construïx amb **blocs**. Un bloc té fins a quatre seccions, i només `BEGIN ... END` és obligatòria:

```text
DECLARE        -- 1. Declaracions (opcional): variables, constants, excepcions
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
| `SELECT` | Sí, **amb `INTO`** o dins d'un bucle `FOR` | `SELECT` sense `INTO` dona `PLS-00428` |
| `COMMIT`, `ROLLBACK`, `SAVEPOINT` | Sí | El control de la transacció (Tema 5) funciona igual |
| `CREATE`, `ALTER`, `DROP` (DDL) | **No directament** | Cal usar SQL dinàmic: `EXECUTE IMMEDIATE 'CREATE TABLE ...'` |
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

Els blocs aniuats no servixen només per a organitzar el codi: són l'eina per a **limitar l'abast d'una excepció** (§6.7).

### 3.4 Comentaris, majúscules i convencions de noms

PL/SQL no distingix majúscules de minúscules en el codi (`begin` és `BEGIN`), però sí en els **literals de text** (`'EduGest'` i `'EDUGEST'` són distints). Els comentaris són de línia (`-- texto`) o de diverses línies (`/* texto */`).

Un prefix en cada nom evita l'error més comú: que una variable es diga igual que una columna. Si en `WHERE id_alumno = id_alumno` tots dos són la columna, la condició és sempre vertadera. EduGest usa estes convencions:

| Element | Prefix | Exemple |
|---|---|---|
| Variable local | `v_` | `v_media` |
| Constant | `c_` | `c_max_convocatorias` |
| Paràmetre | `p_` | `p_id_alumno` |
| Registre (*record*) | `r_` | `r_alumno` |
| Excepció pròpia | `e_` | `e_sin_grupo` |
| Tipus definit per l'usuari | `t_` | `t_grupos` |

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

És la confusió més freqüent del tema. Observa este bloc:

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
| `SQLCODE`, `SQLERRM` | Codi i missatge de l'últim error (només dins d'un manejador, §6.3) |
| `SQL%ROWCOUNT` | Files afectades per l'última sentència DML |

Estes funcions són les que permeten registrar **qui** ha fet un canvi i **des d'on**: s'usen, per exemple, per a registrar qui ha executat un guió.

{{< quiz >}}
- q: "En el bloc `BEGIN DBMS_OUTPUT.PUT_LINE('Hola'); END;` no apareix res per pantalla, però tampoc hi ha error. Què falta?"
  options: ["Un `COMMIT` abans de l'`END`", "`SET SERVEROUTPUT ON` en el client", "Declarar una variable de tipus text", "Canviar `PUT_LINE` per `PRINT`"]
  answer: 1
  explain: "`DBMS_OUTPUT` escriu en un búfer del servidor i és el client qui el mostra, només si se li ha demanat amb `SET SERVEROUTPUT ON`. Sense eixa ordre el bloc s'executa correctament, però no es veu res."
- q: "Un bloc conté `WHERE cod_grupo = '&g'` i s'executa en SQLcl. Qui substituïx `&g` i quan?"
  options: ["Oracle, durant l'execució del bloc", "El client, abans d'enviar el bloc al servidor", "El motor PL/SQL, quan llig la variable `g`", "Ningú: és una variable PL/SQL que val `NULL`"]
  answer: 1
  explain: "`&g` és una variable de **substitució**: el client (SQLcl, SQL*Plus, SQL Developer) reemplaça el text abans d'enviar res. El servidor ja rep el valor i no sap que va existir un `&`. Per això no canvia dins d'un bucle del bloc."
- q: "Què ocorre amb `SELECT nombre INTO v_nombre FROM alumno WHERE nia LIKE '104507%';` si el patró coincidix amb tres alumnes?"
  options: ["S'assigna el primer i s'ignoren els altres", "S'assigna l'últim", "Es llança `TOO_MANY_ROWS` i no s'assigna cap valor", "Es llança `NO_DATA_FOUND`"]
  answer: 2
  explain: "`SELECT ... INTO` exigix exactament una fila. Amb diverses es llança `TOO_MANY_ROWS` (`ORA-01422`). Per a recórrer diverses files cal un bucle `FOR r IN (SELECT ...)`."
- q: "Quin avantatge té declarar `v_nia alumno.nia%TYPE` en lloc de `v_nia CHAR(8)`?"
  options: ["La variable és més ràpida", "La variable herete el tipus de la columna i continua sent correcta si la columna canvia", "Permet emmagatzemar valors nuls", "Fa que la variable siga una constant"]
  answer: 1
  explain: "`%TYPE` consulta el diccionari de dades: si s'amplia o canvia la columna, el codi continua sent coherent sense tocar-lo. Una longitud escrita a mà es queda anticuada."
{{< /quiz >}}


---


{{< sesion n="4" h="1" tipo="t" >}}Estructures de control de flux{{< /sesion >}}

## 5. Estructures de control de flux

El criteri RA5.e demana utilitzar estructures de control. PL/SQL té les tres famílies habituals: **condicionals** (`IF`, `CASE`), **repetitives** (`LOOP`, `WHILE`, `FOR`) i de **salt** (`EXIT`, `CONTINUE`, `GOTO`).

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
> **Una condició amb `NULL` no és vertadera ni falsa: és desconeguda** (*lògica trivaluada*, Tema 4), i `IF` només executa la branca `THEN` quan la condició és **vertadera**. Amb `v_nota` a `NULL`, `IF v_nota >= 5 THEN ... ELSE` executaria l'`ELSE` i marcaria com a suspés qui no s'ha presentat. Per això en l'exemple la primera pregunta és `IS NULL`. I mai s'escriu `v_nota = NULL`: no és vertadera mai.

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
| **`FOR` de consulta** | Recórrer les files d'una consulta | `FOR r IN (SELECT ...) LOOP ... END LOOP;` |

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
| `SELECT ... INTO` dins d'un bucle sobre files | Una consulta per volta i `NO_DATA_FOUND` possible | Usa un bucle `FOR r IN (SELECT ...)` |

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

{{< sesion n="5" h="1" tipo="t" >}}Excepcions{{< /sesion >}}

## 6. Excepcions

### 6.1 Què és una excepció

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

El criteri RA5.e demana utilitzar excepcions. N'hi ha tres classes:

| Classe | Qui la llança | Exemple |
|---|---|---|
| **Predefinida** | Oracle, amb nom ja assignat | `NO_DATA_FOUND`, `ZERO_DIVIDE` |
| **Oracle sense nom** | Oracle, amb codi `ORA-` però sense nom en el llenguatge | `ORA-02292` (esborrar un pare amb fills) |
| **Definida per l'usuari** | El programador, amb `RAISE` o `RAISE_APPLICATION_ERROR` | «L'alumne no té grup» |

### 6.2 Excepcions predefinides

| Excepció | Codi | Es llança quan… |
|---|---|---|
| `NO_DATA_FOUND` | `ORA-01403` | Un `SELECT ... INTO` no torna files |
| `TOO_MANY_ROWS` | `ORA-01422` | Un `SELECT ... INTO` torna més d'una fila |
| `DUP_VAL_ON_INDEX` | `ORA-00001` | Es viola una clau primària o una restricció `UNIQUE` |
| `ZERO_DIVIDE` | `ORA-01476` | Divisió per zero |
| `INVALID_NUMBER` | `ORA-01722` | Conversió de text a nombre impossible dins d'una sentència SQL |
| `VALUE_ERROR` | `ORA-06502` | Error de conversió o de mida en una assignació PL/SQL (`VARCHAR2(3) := 'Sala'`) |
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

### 6.3 `OTHERS`, `SQLCODE` y `SQLERRM`

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

### 6.4 Excepcions definides per l'usuari

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

Una excepció declarada així només existix dins del seu bloc. Si no es tracta, en arribar al client es mostra com `ORA-06510: PL/SQL: unhandled user-defined exception`, un missatge que no ajuda ningú: per això, per a errors que han d'arribar a l'aplicació, es prefereix `RAISE_APPLICATION_ERROR` (§6.6).

### 6.5 `PRAGMA EXCEPTION_INIT`: posar-li nom a un error d'Oracle

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
| `-54` | `ORA-00054`: recurs ocupat (`FOR UPDATE NOWAIT`, Tema 5) | `e_ocupado` |

### 6.6 `RAISE_APPLICATION_ERROR`: errors de negoci cap al client

`RAISE_APPLICATION_ERROR(código, mensaje)` detén el bloc i torna al qui crida un error amb el **codi** i el **missatge** que tu decidisques. És la forma estàndard de comunicar a una aplicació que s'ha incomplit una regla de negoci.

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

### 6.7 Blocs aniuats: limitar l'abast d'un error

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

### 6.8 Excepcions i transaccions

Un error **no** fa `ROLLBACK` de la transacció. El que ocorre depén de si es tracta o no:

| Situació | Què passa amb els canvis |
|---|---|
| L'excepció **no es tracta** i arriba al client | Oracle desfà els canvis de **la crida que ha fallat** (atomicitat de sentència, Tema 5). El que s'havia fet abans en la transacció roman, sense confirmar |
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
> No depengues del comportament implícit. Un bloc que fa diverses modificacions i tracta els seus propis errors ha de decidir **explícitament** què es conserva i què es desfà, i qui el crida ho ha de saber.

### 6.9 Exemple complet: matrícula validada en un bloc

Aquest bloc implementa la regla R2 del catàleg de restriccions (Tema 2) i les regles de convocatòria. Valida l'alumne, el mòdul i el curs acadèmic (que s'indiquen amb `DEFINE`) i, si tot és correcte, inserix la matrícula calculant la convocatòria. Reunix tot el que s'ha vist: variables, `SELECT INTO`, blocs aniuats, excepcions i `RAISE_APPLICATION_ERROR`.

{{< sgbd "Oracle 26ai" >}}

```sql
DEFINE id_alumno = 1
DEFINE id_modulo = 2
DEFINE curso     = 2026-27

DECLARE
    v_id_alumno          alumno.id_alumno%TYPE          := &id_alumno;
    v_id_modulo          modulo.id_modulo%TYPE          := &id_modulo;
    v_curso              matricula.curso_academico%TYPE := '&curso';
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
        WHERE  a.id_alumno = v_id_alumno;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RAISE_APPLICATION_ERROR(-20012, 'El alumno ' || v_id_alumno || ' no existe o no tiene grupo asignado');
    END;

    -- 2. El mòdul existix
    BEGIN
        SELECT cod_ciclo INTO v_ciclo_modulo FROM modulo WHERE id_modulo = v_id_modulo;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RAISE_APPLICATION_ERROR(-20012, 'El módulo ' || v_id_modulo || ' no existe');
    END;

    -- 3. R2: el mòdul és del cicle del grup de l'alumne
    IF v_ciclo_modulo <> v_ciclo_alumno THEN
        RAISE_APPLICATION_ERROR(-20010, 'El módulo ' || v_id_modulo || ' (' || v_ciclo_modulo || ') no es del ciclo del alumno ' || v_id_alumno || ' (' || v_ciclo_alumno || ')');
    END IF;

    -- 4. No està ja matriculat en eixe curs acadèmic
    SELECT COUNT(*)
    INTO   v_ya_matriculado
    FROM   matricula
    WHERE  id_alumno = v_id_alumno AND id_modulo = v_id_modulo AND curso_academico = v_curso;

    IF v_ya_matriculado > 0 THEN
        RAISE_APPLICATION_ERROR(-20013, 'El alumno ' || v_id_alumno || ' ya está matriculado del módulo ' || v_id_modulo || ' en ' || v_curso);
    END IF;

    -- 5. Convocatòria: una més que l'última matrícula del mòdul (màxim 4)
    SELECT NVL(MAX(convocatoria), 0) + 1
    INTO   v_convocatoria
    FROM   matricula
    WHERE  id_alumno = v_id_alumno AND id_modulo = v_id_modulo;

    IF v_convocatoria > c_max_convocatorias THEN
        RAISE_APPLICATION_ERROR(-20011, 'El alumno ' || v_id_alumno || ' ha agotado las ' || c_max_convocatorias || ' convocatorias del módulo ' || v_id_modulo);
    END IF;

    -- 6. Tot correcte: s'inserix. No hi ha COMMIT: ho decidix qui crida
    INSERT INTO matricula (id_alumno, id_modulo, curso_academico, convocatoria)
    VALUES (v_id_alumno, v_id_modulo, v_curso, v_convocatoria);
END;
/
```

Decisions de disseny que convé entendre:

| Decisió | Motiu |
|---|---|
| Els dos primers `SELECT INTO` van en **blocs aniuats** | Converteixen `NO_DATA_FOUND` en un error de negoci amb codi i missatge propis (`-20012`), en lloc de deixar passar un `ORA-01403` incomprensible |
| La convocatòria es calcula com `MAX(convocatoria) + 1` sobre **totes** les matrícules de l'alumne en eixe mòdul | Si mai s'ha matriculat, `MAX` torna `NULL`, `NVL(..., 0)` el convertix en 0 i la convocatòria és 1 |
| `RAISE_APPLICATION_ERROR` en cada regla | Un codi distint per regla: l'aplicació pot reaccionar sense analitzar el text |
| **No hi ha `COMMIT`** | La matrícula forma part d'una transacció major (matricular l'alumne en tot el curs, Tema 5); ho decidix qui crida |
| El curs acadèmic **no es valida** en el bloc | Ho fa la restricció `CK_MATRICULA_CURSO` de la taula. Duplicar la validació crearia dues regles que mantindre |

**Proves.** Amb l'alumne 1 (grup 1DAM, cicle DAM), que ja va cursar el mòdul 2 en 2025-26 i el va suspendre (nota 4,75):

```sql
DEFINE id_alumno = 1
DEFINE id_modulo = 2
DEFINE curso     = 2026-27
-- i torna a executar el bloc

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
DEFINE id_alumno = 1
DEFINE id_modulo = 2
DEFINE curso     = 2026-27   -- repetida
-- i torna a executar el bloc
```

```text
ORA-20013: El alumno 1 ya está matriculado del módulo 2 en 2026-27
ORA-06512: at line 43
```

```sql
DEFINE id_alumno = 1
DEFINE id_modulo = 12
DEFINE curso     = 2026-27   -- el mòdul 12 és de DAW; l'alumne 1 és de DAM
-- i torna a executar el bloc
```

```text
ORA-20010: El módulo 12 (DAW) no es del ciclo del alumno 1 (DAM)
ORA-06512: at line 33
```

Els números de línia d'`ORA-06512` compten des de la línia `DECLARE` i et porten al `RAISE_APPLICATION_ERROR` exacte. La bateria completa de huit proves està en la [pràctica 5.8](/tema5-modificacion/guiones-practicas#pràctica-58--matrícula-amb-excepcions). Quan acabes, `ROLLBACK;` torna la taula al seu estat original.

> [!TIP]
> Un bloc que valida sempre té la mateixa estructura: **comprovar → rebutjar amb un error clar → actuar**. Les comprovacions van primer i de més barata a més cara; l'`INSERT` va al final, quan ja no pot fallar per una regla de negoci.


---

{{< sesion n="7" h="2" tipo="t" >}}Guions de manteniment: estructura, idempotència i proves{{< /sesion >}}

## 7. Guions de manteniment

El criteri RA5.e demana **dissenyar guions de sentències per a dur a terme tasques complexes**. Un guió de manteniment és un fitxer `.sql` que una persona executa en un servidor real: ha de poder-se **llegir, revisar, repetir i auditar**.

### 7.1 Estructura d'un guió professional

```sql
-- =====================================================================
-- Guió     : justificar_faltas_huelga.sql
-- Autor    : Lorena L. Resusta
-- Data     : 2027-05-10
-- Entorn   : FREEPDB1 · esquema EDUGEST
-- Objectiu : Justificar les faltes del 12/03/2026 (vaga de transport)
-- Reversió : ROLLBACK abans del COMMIT final; després, restaurar des de
--            BAK_FALTA_20270510 amb el guió deshacer_faltas_huelga.sql
-- Files esperades: 1 (segons comprovació prèvia del 09/05/2027)
-- =====================================================================

WHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK   -- qualsevol error avorta i desfà
SET ECHO ON FEEDBACK ON TIMING ON
SPOOL justificar_faltas_huelga.log

-- 0. On estic? (queda en la traça)
SELECT sys_context('USERENV','DB_NAME') AS bd, user AS esquema, SYSDATE FROM dual;

-- 1. Còpia de seguretat de les files afectades  (DDL: ABANS de la transacció)
CREATE TABLE bak_falta_20270510 AS
SELECT * FROM falta_asistencia WHERE fecha = DATE '2026-03-12';

-- 2. Comprovació prèvia: les files que es van a modificar
SELECT id_falta, id_matricula, fecha, horas, justificada
FROM   falta_asistencia
WHERE  fecha = DATE '2026-03-12' AND justificada = 'N';

-- 3. Transacció
SAVEPOINT antes_de_justificar;

UPDATE falta_asistencia
SET    justificada = 'S'
WHERE  fecha = DATE '2026-03-12'
AND    justificada = 'N';

-- 4. Comprovació posterior: no ha de quedar cap sense justificar
SELECT COUNT(*) AS pendientes
FROM   falta_asistencia
WHERE  fecha = DATE '2026-03-12' AND justificada = 'N';   -- ha de ser 0

-- 5. Registre del que s'ha fet
INSERT INTO log_mantenimiento (guion, filas, observaciones)
VALUES ('justificar_faltas_huelga.sql', SQL%ROWCOUNT,
        'Huelga de transporte del 12/03/2026');

-- 6. Confirmació
COMMIT;

SPOOL OFF
```

| Element | Per a què servix |
|---|---|
| Capçalera amb autor, data, entorn i objectiu | Que qui ho lligca en 2029 sàpia què fa i qui en respon |
| `WHENEVER SQLERROR EXIT ... ROLLBACK` | Que un error **detinga** el guió i no deixe mitges tintes |
| `SPOOL` | Deixar traça de tot l'executat i dels seus resultats: és l'evidència de la intervenció |
| Còpia prèvia amb CTAS | Poder tornar arrere després del `COMMIT` |
| `SELECT` de comprovació prèvia | Verificar les files abans de tocar-les |
| `SAVEPOINT` | Poder retrocedir un pas sense perdre la resta |
| `SELECT` de comprovació posterior | Confirmar que el resultat és l'esperat |
| Registre en una taula d'auditoria | Saber què es va executar, quan i amb quin resultat |
| `COMMIT` **al final i una sola vegada** | Que tot el guió siga una única unitat de treball |

```sql
-- Taula d'auditoria dels guions de manteniment
CREATE TABLE log_mantenimiento (
    id_log         NUMBER(8) GENERATED BY DEFAULT ON NULL AS IDENTITY
                   CONSTRAINT pk_log_mantenimiento PRIMARY KEY,
    guion          VARCHAR2(80) CONSTRAINT nn_log_guion NOT NULL,
    ejecutado      TIMESTAMP DEFAULT SYSTIMESTAMP CONSTRAINT nn_log_fecha NOT NULL,
    usuario        VARCHAR2(30)  DEFAULT USER CONSTRAINT nn_log_usuario NOT NULL,
    filas          NUMBER(8),
    observaciones  VARCHAR2(400)
);
```

> [!WARNING]
> El `CREATE TABLE` del pas 1 és **DDL**: du `COMMIT` implícit. Per això està **abans** de la transacció i mai enmig. Si el col·locares entre l'`UPDATE` i el `COMMIT`, confirmaries l'`UPDATE` sense voler i el `WHENEVER SQLERROR ... ROLLBACK` ja no podria desfer-lo.

### 7.2 Idempotència

Un guió és **idempotent** si executar-lo dues voltes produïx el mateix resultat que executar-lo una. És una propietat valuosíssima: permet rellançar sense por un procés interromput.

| Forma d'aconseguir-la | Exemple |
|---|---|
| Condició que ja no es complix després de la primera passada | `WHERE justificada = 'N'`: la segona vegada afecta 0 files |
| `MERGE` en lloc d'`INSERT` | Actualitza el que ja hi és i afig el que falta (Tema 5, §5.4) |
| `INSERT … WHERE NOT EXISTS` | No duplica les files ja inserides |
| Clau primària que impedix el duplicat | `HISTORICO_NOTA` falla amb `ORA-00001` en el segon arxivat |
| Comprovació de guarda al principi | Si ja existixen matrícules de 2026-27, el guió s'atura |

```sql
-- Guarda: aturar el guió si ja es va executar
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

### 7.3 Com es prova un guió abans d'executar-lo en producció

- [ ] S'executa en un **entorn de proves** amb una còpia recent de les dades reals.
- [ ] S'anota el nombre de files afectades de **cada** sentència i es compara amb el previst.
- [ ] S'executa **dues voltes** per a comprovar la idempotència.
- [ ] Es provoca un error a mitat (canviant el nom d'una taula, per exemple) i es verifica que **no queda cap canvi** aplicat.
- [ ] Es comprova que existix i funciona el guió de reversió.
- [ ] Es revisa que no hi haja DDL dins de la transacció.
- [ ] S'executa en producció amb `SPOOL` actiu, i el `.log` s'arxiva junt amb el guió.


---


## 8. Errors freqüents

| Símptoma | Causa | Solució |
|---|---|---|
| El bloc «funciona» però no mostra res | Falta `SET SERVEROUTPUT ON` o el panell d'eixida està tancat | Activa'l en cada sessió (§2.4) |
| SQLcl es queda esperant després d'escriure el bloc | Falta la `/` final | Escriu-la en una línia sola (§2.3) |
| `PLS-00103: Encountered the symbol ...` | `;` oblidat, `END IF` o `END LOOP` sense tancar, coma sobrant | Revisa la línia que indica i l'anterior (§2.5) |
| `ORA-01403: no data found` | `SELECT ... INTO` sense files | Tracta `NO_DATA_FOUND` o usa un agregat (§6.2) |
| `ORA-01422: exact fetch returns more than requested number of rows` | `SELECT ... INTO` amb diverses files | Concreta el `WHERE` o recorre las filas con un bucle `FOR` |
| La condició `WHERE id_alumno = id_alumno` torna totes les files | Paràmetre o variable amb el mateix nom que la columna | Prefixos `p_` i `v_` (§3.4) |
| Un `IF x > 5 ... ELSE` marca com a suspés qui no té nota | La comparació amb `NULL` és desconeguda i cau en l'`ELSE` | Pregunta primer `IS NULL` (§5.1) |
| `ORA-06510: unhandled user-defined exception` | `RAISE` d'una excepció pròpia sense manejador | Tracta-la o usa `RAISE_APPLICATION_ERROR` |
| `WHEN OTHERS THEN NULL` i dades que no quadren | Un error s'ha empassat en silenci | Registra i rellança amb `RAISE;` (§6.3) |
| Els canvis del bloc no apareixen en una altra sessió | Falta el `COMMIT` (que, per disseny, el bloc no fa) | Confirma al final del guió |

---

## 9. Bones pràctiques

- **Usa `%TYPE` i `%ROWTYPE`** en lloc de repetir els tipus de les columnes.
- **Prefixos en els noms** (`v_`, `p_`, `c_`, `r_`, `e_`) per a no confondre variables, paràmetres i columnes.
- **Escriu sempre l'`ELSE`** d'un `CASE` i la branca `IS NULL` de les condicions que manegen dades que puguen faltar.
- **Tracta només els errors que saps tractar.** Res de `WHEN OTHERS THEN NULL`: registra i torna a llançar amb `RAISE;`.
- **Defineix un catàleg d'errors propis** (`-20010`...), amb un codi per regla i un missatge que diga quina dada ha fallat.
- **Guions versionats, amb capçalera, `SPOOL`, comprovacions i idempotència.** Res de canvis a mà en la reixeta per a tasques que es repetixen.
- **Un guió confirma una sola vegada, al final,** i només si les comprovacions han eixit bé.
- **Registra el que fas** en una taula d'auditoria: data, usuari, guió i files afectades.
- **Si has de desfer una part, usa `SAVEPOINT`** de forma explícita; no depengues del que ocorregue de forma implícita.
- **Marca en la documentació el que és específic d'Oracle** si el codi s'ha de portar a un altre gestor.

---

{{< tarjetas titulo="Repassa els termes del tema 5" >}}
- t: "Bloc anònim"
  d: "Codi PL/SQL sense nom: DECLARE, BEGIN, EXCEPTION, END."
- t: "Excepció"
  d: "Error controlat en la secció EXCEPTION."
{{< /tarjetas >}}

## 10. Resum

| Concepte | Idea clau | Sintaxi essencial |
|---|---|---|
| Execució de guions | Les ordres de client (`SET`, `SPOOL`, `@`) no les entén el servidor; els blocs PL/SQL acaben en `;` i `/` | `@fichero.sql`, `SET SERVEROUTPUT ON` |
| Bloc | `DECLARE` (opcional), `BEGIN` ... `EXCEPTION` (opcional) ... `END;` | `DECLARE ... BEGIN ... END;` |
| Variables | Amb tipus, heretables de la taula amb `%TYPE` i `%ROWTYPE`. Distintes de les variables de **substitució** (`&`), que resol el client | `v_x tabla.col%TYPE;`, `SELECT ... INTO` |
| Control de flux | `IF`/`ELSIF`, `CASE`, `LOOP`/`WHILE`/`FOR`; compte amb `NULL` | `IF ... THEN ... END IF;` |
| Excepcions | Predefinides, pròpies, `PRAGMA EXCEPTION_INIT`; `RAISE_APPLICATION_ERROR` entre -20000 i -20999 | `EXCEPTION WHEN ... THEN` |
| Guions de manteniment | Capçalera, còpia prèvia, comprovacions, `SAVEPOINT`, `COMMIT` únic, `SPOOL` i idempotència | `WHENEVER SQLERROR EXIT ROLLBACK`, `SPOOL` |

Idees que convé endur-se gravades:

1. **Un `&` el resol el client; un `v_` el resol el servidor.**
2. **L'excepció més perillosa és la que s'empassa en silenci.**
3. **Un guió ben fet es pot executar dues vegades sense trencar res.**
4. **Es prova abans en un entorn de proves, amb còpia prèvia i amb `SPOOL` actiu.**

---

## 11. Autoavaluació

{{< quiz >}}
- q: "Què fa `SELECT AVG(nota_final) INTO v_media FROM matricula WHERE id_alumno = 30;` si l'alumne 30 no té matrícules?"
  options: ["Llança `NO_DATA_FOUND`", "Llança `TOO_MANY_ROWS`", "Assigna `NULL` a `v_media`, sense error", "Assigna 0 a `v_media`"]
  answer: 2
  explain: "Un agregat sense `GROUP BY` torna sempre exactament una fila, encara que no hi haja dades d'entrada. `AVG` de cap valor és `NULL`: no hi ha excepció, i `v_media` queda a `NULL`."
- q: "En un guió s'escriu `&grupo` dins d'un bloc PL/SQL. Qui en substituïx el valor?"
  options: ["El servidor Oracle, en compilar el bloc", "El client (SQLcl, SQL*Plus, SQL Developer), abans d'enviar el text al servidor", "El bloc, en cada volta d'un bucle", "La base de dades, en confirmar la transacció"]
  answer: 1
  explain: "Una variable de substitució és text que el client apega en el codi abans d'enviar-lo. El servidor ja rep el valor i no sap que va existir un `&`."
- q: "Un bloc executa `SELECT nombre INTO v_nombre FROM alumno WHERE id_alumno = 999;` i l'alumne no existix. Què passa?"
  options: ["`v_nombre` queda a `NULL` sense error", "Es llança `NO_DATA_FOUND` (`ORA-01403`)", "Es llança `TOO_MANY_ROWS` (`ORA-01422`)", "El bloc no es compila"]
  answer: 1
  explain: "`SELECT ... INTO` exigix exactament una fila. Sense files es llança `NO_DATA_FOUND`; amb diverses, `TOO_MANY_ROWS`."
- q: "Un manejador `WHEN OTHERS THEN NULL;` després d'un `UPDATE` que falla. Quin problema té?"
  options: ["No es compila", "Es empassa l'error en silenci: el guió continua com si tot haguera anat bé", "Desfà automàticament la transacció", "Convertix l'error en un avís"]
  answer: 1
  explain: "L'excepció més perillosa és la que s'empassa. Si no saps tractar l'error, registra'l i rellança'l amb `RAISE;`."
- q: "Què significa que un guió de manteniment siga idempotent?"
  options: ["Que s'executa més ràpid la segona vegada", "Que executar-lo dues vegades deixa la base de dades igual que executar-lo una", "Que no necessita `COMMIT`", "Que només el pot executar un usuari"]
  answer: 1
  explain: "La idempotència permet rellançar un guió interromput sense duplicar ni corrompre dades (per exemple, amb `MERGE` o amb comprovacions prèvies)."
- q: "Enmig d'un guió transaccional apareix un `CREATE TABLE`. Quina conseqüència té?"
  options: ["Cap: el DDL es desfà amb el `ROLLBACK`", "Confirma implícitament la transacció en curs, i el que hi havia abans ja no es pot desfer", "Bloqueja totes les taules", "Només funciona dins d'un bloc anònim"]
  answer: 1
  explain: "Cada sentència DDL du un `COMMIT` implícit. Les còpies i els canvis d'estructura es fan abans d'obrir la transacció."
{{< /quiz >}}

## Referències

- [Oracle AI Database 26ai: Database PL/SQL Language Reference](https://docs.oracle.com/en/database/oracle/oracle-database/26/lnpls/) — blocs, variables, control de flux, cursors, excepcions i disparadors (inclosos els compostos i la restricció de la taula mutant).
- [Oracle AI Database 26ai: SQL*Plus User's Guide and Reference](https://docs.oracle.com/en/database/oracle/oracle-database/26/sqpug/) — variables de substitució, `SET SERVEROUTPUT`, `SPOOL` i execució de guions.
- [Oracle SQLcl: documentación](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/) y [Oracle SQL Developer](https://docs.oracle.com/en/database/oracle/sql-developer/).
- [Oracle AI Database 26ai: Database Error Messages](https://docs.oracle.com/en/error-help/db/) — `ORA-01403`, `ORA-02292`, `ORA-06510`...
- [Reial decret 1629/2009, de 30 d'octubre](https://www.boe.es/eli/es/rd/2009/10/30/1629) — ensenyaments mínims del mòdul 0372 Gestió de bases de dades (RA5.e).
