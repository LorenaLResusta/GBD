---
title: "Còpies de seguretat, importació i exportació"
weight: 1
bookToc: true
---

# UD10 · Còpies de seguretat, importació i exportació de dades

## Resum del tema

Fins ara hem construït, consultat i programat una base de dades. Falta la pregunta que més s'enrecorda el dia que alguna cosa falla: **què passa si perdem les dades?** Un disc que s'espatlla, un `DELETE` sense `WHERE`, un ransomware o un contenidor esborrat per error tenen el mateix efecte: la informació desapareix. L'única defensa és haver fet **còpies de seguretat** i **haver comprovat que es poden restaurar**.

Esta unitat cobrix el **RA6** del mòdul: *executar tasques d'assegurament de la informació, analitzant-les i aplicant mecanismes de salvaguarda i transferència*. Treballarem sobre EduGest amb les eines d'**Oracle AI Database 26ai Free** (Data Pump, SQL\*Loader, SQLcl, SQL Developer) i amb les de **MongoDB 8.0** (`mongodump`, `mongorestore`, `mongoexport`, `mongoimport`).

{{< ra "RA6:a,b,c,d,e,f,g,h" >}}

### Objectius d'aprenentatge

En acabar esta part series capaç de:

- Distingir els tipus de còpia de seguretat (lògica i física, completa, incremental i diferencial, en fred i en calent) i triar una estratègia segons el temps de recuperació i la pèrdua de dades admissibles (RA6.a).
- Fer i restaurar una còpia lògica d'un esquema d'Oracle amb Data Pump (RA6.b, RA6.c).
- Fer i restaurar una còpia d'una base de dades de MongoDB amb `mongodump` i `mongorestore` (RA6.b, RA6.c).
- Identificar les ferramentes d'importació i exportació de cada gestor (RA6.d).
- Exportar dades a CSV, JSON i scripts SQL (RA6.e) i importar fitxers amb SQL\*Loader, SQL Developer i `mongoimport` (RA6.f).
- Llegir els missatges d'error i els fitxers de registre (`.log`, `.bad`) per a localitzar la causa d'un error (RA6.g).
- Transferir informació entre dos sistemes gestors diferents (Oracle i MongoDB) tenint cura de tipus, dates, nuls i codificació (RA6.h).

### Temporalització

La unitat ocupa **12 hores d'aula** (4 de teoria i 8 de pràctica).

{{< sesiones unidad="UD10" horas="12" >}}
items:
  - {h: 1, tipo: T, t: "Còpies de seguretat: tipus, estratègia i eines", ref: "§1 i §2"}
  - {h: 1, tipo: T, t: "Còpia lògica amb Data Pump i còpies en MongoDB", ref: "§3 i §4"}
  - {h: 2, tipo: P, t: "Còpia lògica d'EduGest i restauració", ref: "Pràctica 10.1"}
  - {h: 1, tipo: T, t: "Importar i exportar dades", ref: "§5"}
  - {h: 2, tipo: P, t: "Exportar dades a CSV, JSON i SQL", ref: "Pràctica 10.2"}
  - {h: 2, tipo: P, t: "Importar amb SQL*Loader i llegir els errors", ref: "Pràctica 10.3"}
  - {h: 1, tipo: T, t: "Transferència entre gestors i registres d'error", ref: "§6 i §7"}
  - {h: 2, tipo: P, t: "D'Oracle a MongoDB i projecte de seguretat", ref: "Pràctica 10.4 · Projecte EduGest · UD10"}
autonomo:
  - "Repte 10.5 (pla de còpies i simulacre de desastre)"
  - "Ampliacions de les pràctiques 10.1 a 10.4 i autoavaluació"
{{< /sesiones >}}

> [!IMPORTANT]
> Una còpia de seguretat **que mai no s'ha restaurat no és una còpia: és una esperança**. En cada pràctica d'esta part hi ha un pas de *restauració i comprovació*. No te'l salts.

---

## 1. Per què i com es fan còpies

### 1.1 Què pot eixir malament

| Causa | Exemple en EduGest | Què ho evita |
|---|---|---|
| Error humà | Un `DELETE FROM matricula;` sense `WHERE` i amb `COMMIT` | Còpia recent; auditoria; permisos mínims |
| Fallada de maquinari | S'espatlla el disc on està el volum `oracle-data` | Còpia en **un altre** dispositiu |
| Fallada de programari | Una actualització corromp el contenidor | Còpia anterior a l'actualització |
| Atac | Ransomware que xifra el servidor | Còpia desconnectada de la xarxa |
| Desastre | Incendi o robatori de l'equip | Còpia fora de l'edifici o en el núvol |

### 1.2 Dos números que manen: RPO i RTO

- **RPO** (*Recovery Point Objective*): quantes dades ens podem permetre perdre, mesurat en temps. Si fem còpia cada nit, l'RPO és de fins a 24 hores.
- **RTO** (*Recovery Time Objective*): quant de temps podem estar sense servei mentre restaurem.

> [!TIP]
> Abans de triar ferramentes, pregunta al «client» quant costa una hora aturat i quanta informació pot perdre. Una secretaria que grava notes durant l'avaluació necessita un RPO molt menor que el repositori de programacions.

### 1.3 Classificació de les còpies

| Criteri | Tipus | Idea |
|---|---|---|
| **Què es copia** | Lògica / Física | La **lògica** guarda els objectes i les dades com a sentències o files (`CREATE TABLE`, `INSERT`...). La **física** copia els fitxers de la base de dades tal qual. |
| **Quant es copia** | Completa / Incremental / Diferencial | La **completa** copia tot. La **incremental** copia el canviat des de l'última còpia (de qualsevol tipus). La **diferencial** copia el canviat des de l'última completa. |
| **Com està el servei** | En fred / En calent | En **fred** la base de dades està parada. En **calent** continua funcionant mentre es copia. |

Per a restaurar una incremental necessites la completa i **totes** les incrementals intermèdies. Per a una diferencial, la completa i l'última diferencial. Per això les incrementals ocupen menys però tarden més a restaurar-se.

### 1.4 La regla 3-2-1

> [!IMPORTANT]
> **3** còpies de les dades, en **2** tipus de suport diferents, amb **1** còpia fora del lloc original. I una quarta regla de sentit comú: **xifra** les còpies que isquen de l'organització, perquè contenen dades personals.

## 2. Ferramentes de còpia

| Gestor | Ferramenta | Tipus | Quan usar-la |
|---|---|---|---|
| Oracle | **Data Pump** (`expdp` / `impdp`) | Lògica | Copiar o moure un esquema o unes taules; treballar en equips diferents |
| Oracle | **RMAN** (*Recovery Manager*) | Física | Còpies completes i incrementals de tota la base de dades |
| Oracle | Còpia en fred del volum | Física | Entorns de classe: parar el contenidor i copiar el volum |
| Oracle | **SQL Developer** (*Ferramentes → Exportació de base de dades*) | Lògica (assistent) | Generar scripts de DDL i dades amb interfície gràfica |
| MongoDB | **`mongodump` / `mongorestore`** | Lògica (BSON) | Còpia i restauració de bases de dades o col·leccions |

> [!NOTE]
> **RMAN** és la ferramenta professional de còpia física d'Oracle (`rman target /` i ordres com `BACKUP DATABASE`). Funciona de manera molt diferent segons la base de dades estiga en mode `ARCHIVELOG` o `NOARCHIVELOG`: sense arxivat només permet còpies amb la base de dades muntada però tancada. En el contenidor de classe no la utilitzarem; treballarem amb **Data Pump**, que és lògica i funciona amb la base de dades oberta.

### 2.1 Còpia en fred del contenidor

És la còpia més simple i ajuda a entendre què és una còpia física: es **para** el servei perquè els fitxers estiguen consistents i es copien.

```bash
docker stop oracle26ai
docker run --rm -v oracle-data:/datos -v "$PWD":/copia busybox \
       tar czf /copia/oracle-data_$(date +%Y%m%d).tgz -C /datos .
docker start oracle26ai
```

{{< sgbd "Docker" >}} El volum `oracle-data` es munta en un contenidor auxiliar que el comprimix en la carpeta actual. Per a restaurar es fa l'operació inversa sobre un volum buit. Desavantatge: el servei queda **parat** mentre es copia.

## 3. Còpia lògica amb Data Pump (Oracle)

**Data Pump** es compon de dos programes que s'executen en el **servidor**: `expdp` (exportar) i `impdp` (importar). Escriuen en un **directori** d'Oracle (un objecte `DIRECTORY` que apunta a una carpeta del servidor), i generen un fitxer de bolcat `.dmp` i un fitxer de registre `.log`.

### 3.1 Preparar el directori

{{< sgbd "Oracle 26ai" >}} Connectat com a `SYSTEM` a `FREEPDB1`:

```sql
SELECT directory_name, directory_path
FROM   dba_directories
WHERE  directory_name = 'DATA_PUMP_DIR';
```

`DATA_PUMP_DIR` és el directori per defecte de Data Pump. Anota la ruta: ahí apareixeran els fitxers. Si no existira, crea'l amb `CREATE DIRECTORY dir_copias AS '/ruta/del/servidor';` (la carpeta ha d'existir i ser escrivible per l'usuari `oracle`).

### 3.2 Exportar un esquema

```bash
docker exec -it oracle26ai expdp system/Oracle_2026@//localhost:1521/FREEPDB1 \
  schemas=EDUGEST directory=DATA_PUMP_DIR \
  dumpfile=edugest_%U.dmp logfile=edugest_exp.log
```

Cada paràmetre té una raó:

| Paràmetre | Significat |
|---|---|
| `schemas=EDUGEST` | Mode esquema: exporta tots els objectes de l'usuari `EDUGEST` |
| `directory=` | Objecte `DIRECTORY` on s'escriuen els fitxers |
| `dumpfile=edugest_%U.dmp` | Nom del bolcat; `%U` genera `01`, `02`... si hi ha diversos fitxers |
| `logfile=` | Fitxer amb el registre de l'operació |
| `content=metadata_only` | (opcional) Només estructures, sense dades |
| `tables=ALUMNO,MATRICULA` | (opcional) Mode taula en lloc d'esquema |
| `query=ALUMNO:"WHERE cod_grupo='1DAM'"` | (opcional) Exportar només algunes files |
| `parfile=copia.par` | (opcional) Guardar els paràmetres en un fitxer |

Al final ha d'aparéixer una línia com `Job "SYSTEM"."SYS_EXPORT_SCHEMA_01" successfully completed`. Si apareix `completed with N error(s)`, **cal llegir el log**.

### 3.3 Traure la còpia del contenidor

La còpia no servix si està dins del mateix disc que la base de dades que protegix:

```bash
docker cp oracle26ai:/opt/oracle/admin/FREE/dpdump/<ruta-anotada>/edugest_01.dmp ./copias/
docker cp oracle26ai:/opt/oracle/admin/FREE/dpdump/<ruta-anotada>/edugest_exp.log ./copias/
```

### 3.4 Importar i restaurar

`impdp` és el camí invers. L'opció `remap_schema` permet restaurar en un altre usuari, que és la forma segura de **provar** una còpia sense tocar les dades reals:

```sql
-- Com a SYSTEM: usuari de prova per a la restauració
CREATE USER edugest_copia IDENTIFIED BY "Copia_2026"
  DEFAULT TABLESPACE users QUOTA UNLIMITED ON users;
GRANT CREATE SESSION, CREATE TABLE, CREATE SEQUENCE, CREATE VIEW,
      CREATE PROCEDURE, CREATE TRIGGER TO edugest_copia;
```

```bash
docker exec -it oracle26ai impdp system/Oracle_2026@//localhost:1521/FREEPDB1 \
  directory=DATA_PUMP_DIR dumpfile=edugest_%U.dmp logfile=edugest_imp.log \
  remap_schema=EDUGEST:EDUGEST_COPIA
```

| Opció útil | Efecte |
|---|---|
| `table_exists_action=REPLACE` | Si la taula ja existix: `SKIP` (per defecte), `APPEND`, `TRUNCATE` o `REPLACE` |
| `remap_tablespace=` | Canvia l'espai de taules de destinació |
| `include=TABLE:"IN ('ALUMNO')"` | Importar només alguns objectes |
| `sqlfile=estructura.sql` | No importa: escriu en un fitxer el DDL que executaria |

### 3.5 Comprovar la restauració

Restaurar no acaba quan `impdp` diu *completed*. Es comprova que les dades coincidixen:

```sql
SELECT 'ALUMNO' AS tabla, COUNT(*) FROM edugest.alumno
UNION ALL SELECT 'ALUMNO_COPIA', COUNT(*) FROM edugest_copia.alumno
UNION ALL SELECT 'MATRICULA', COUNT(*) FROM edugest.matricula
UNION ALL SELECT 'MATRICULA_COPIA', COUNT(*) FROM edugest_copia.matricula;

-- Files que estan en l'original i no en la còpia (ha de tornar 0 files)
SELECT * FROM edugest.alumno
MINUS
SELECT * FROM edugest_copia.alumno;
```

## 4. Còpia i restauració en MongoDB

`mongodump` genera fitxers **BSON** (format binari de MongoDB) i `mongorestore` els carrega.

```bash
docker exec mongo8 mongodump --db=edugest --out=/tmp/copia_mongo
docker cp mongo8:/tmp/copia_mongo ./copias/mongo

# Restaurar en una base de dades de proves
docker exec mongo8 mongorestore --nsFrom='edugest.*' --nsTo='edugest_copia.*' /tmp/copia_mongo
```

> [!WARNING]
> Estes ferramentes formen part de les *MongoDB Database Tools*. Comprova que estan en la teua imatge amb `docker exec mongo8 mongodump --version`. Si no, instal·la-les des del web de MongoDB i executa-les des del teu equip amb `--uri="mongodb://localhost:27017"`.

Per a comprovar: `db.expedientes.countDocuments()` en `edugest` i en `edugest_copia` ha de donar el mateix nombre.

## 5. Importar i exportar dades

Una còpia servix per a restaurar el **mateix** gestor. L'**exportació** i la **importació** de dades servix per a intercanviar informació amb altres aplicacions i amb altres gestors, usant formats de text.

### 5.1 Formats

| Format | Avantatges | Compte amb |
|---|---|---|
| **CSV** | Universal; l'obri qualsevol full de càlcul | Separador (`,` o `;`), cometes, salts de línia dins de camps, dates, decimals (`.` o `,`) |
| **JSON** | Conserva l'estructura aniuada; natural per a MongoDB i APIs | Els tipus són pocs: les dates són text; els `NULL` s'escriuen `null` o s'ometen |
| **Script SQL** | S'executa en el mateix gestor o en un de paregut | Dialecte propi de cada gestor |
| **XML** | Intercanvi entre sistemes empresarials | Verbós |

### 5.2 Exportar en Oracle

Amb **SQLcl** o amb la consola de SQL Developer es poden canviar els formats d'eixida d'una consulta:

```sql
SET SQLFORMAT csv
SPOOL alumnado.csv
SELECT nia, nombre, apellidos, cod_grupo FROM alumno ORDER BY nia;
SPOOL OFF
SET SQLFORMAT default
```

{{< sgbd "SQLcl" >}} `SQLFORMAT` admet `csv`, `json`, `xml`, `insert` (genera sentències `INSERT`) i altres. `SPOOL` escriu el resultat en un fitxer. Amb l'**assistent gràfic** de SQL Developer: clic dret sobre una taula → *Exportar*, i es tria format, columnes i destinació.

També es pot generar JSON a partir de taules amb les funcions SQL/JSON d'Oracle (`JSON_OBJECT`, `JSON_ARRAYAGG`), útil per a portar les dades a MongoDB.

### 5.3 Importar en Oracle amb SQL\*Loader

**SQL\*Loader** (`sqlldr`) carrega fitxers de text en taules. Necessita un **fitxer de control** que diu on estan les dades i com mapar-les:

```text
-- carga_alumnos.ctl
LOAD DATA
CHARACTERSET UTF8
INFILE 'alumnos_nuevos.csv'
APPEND
INTO TABLE alumno_carga
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(nia, nombre, apellidos, cod_grupo)
```

```bash
sqlldr userid=edugest/Edugest_2026@//localhost:1521/FREEPDB1 \
       control=carga_alumnos.ctl log=carga.log bad=carga.bad
```

| Fitxer | Contingut |
|---|---|
| `.log` | Resum: files llegides, carregades, rebutjades, errors |
| `.bad` | Les files **rebutjades** per la base de dades (per exemple, violen una restricció) |
| `.dsc` | (si es demana amb `discard=`) Files descartades per una condició `WHEN` |

`APPEND` afig files; `TRUNCATE` buida la taula abans de carregar; `INSERT` exigix que la taula estiga buida.

> [!NOTE]
> A classe usarem també l'**assistent d'importació** de SQL Developer (clic dret sobre la taula → *Importar dades*), que genera el mateix tipus de càrrega sense escriure el fitxer de control. Els assistents ajuden, però cal entendre què fan: cal saber llegir els seus missatges.

### 5.4 Importar i exportar en MongoDB

```bash
# Exportar una col·lecció a JSON (un document per línia)
docker exec mongo8 mongoexport --db=edugest --collection=expedientes --out=/tmp/expedientes.json

# Importar un fitxer JSON (si és un array, afig --jsonArray)
docker exec mongo8 mongoimport --db=edugest_copia --collection=expedientes --file=/tmp/expedientes.json
```

Per a CSV: `mongoexport --type=csv --fields=nia,nombre,grupo ...` i `mongoimport --type=csv --headerline ...`.

## 6. Transferir informació entre gestors

Passar dades d'Oracle a MongoDB (o a PostgreSQL, o a un full de càlcul) és una tasca habitual. El procés sempre té els mateixos passos:

1. **Origen:** definir quines dades es transferixen (consulta).
2. **Transformació:** adaptar tipus, dates, nuls i estructura a la destinació.
3. **Exportació** a un format intermedi (CSV o JSON).
4. **Importació** a la destinació.
5. **Verificació:** comparar recomptes i revisar una mostra.

| Aspecte | Què pot fallar | Com evitar-ho |
|---|---|---|
| **Codificació** | `Ramón` es converteix en `RamÃ³n` | Exportar i importar en **UTF-8** |
| **Dates** | `14/03/2007` s'interpreta com `03/14/...` | Usar format ISO 8601: `2007-03-14` |
| **Decimals** | `4,75` no és un nombre en CSV amb coma com a separador | Usar punt decimal o separador `;` |
| **Nuls** | Una cadena buida no és el mateix que `NULL` | Decidir com es representen i comprovar en importar |
| **Estructura** | Una relació 1:N es converteix en un array incrustat | Dissenyar el document abans (UD10) |
| **Claus alienes** | La destinació no valida la integritat | Validar amb consultes després d'importar |

## 7. Missatges d'error i fitxers de registre

Aprendre a llegir els registres és la diferència entre resoldre una fallada en cinc minuts o en cinc hores.

### 7.1 Mètode

1. **Llig el log complet**, no només l'última línia.
2. Busca el **primer** error: els següents solen ser conseqüència.
3. Anota el **codi** (`ORA-39002`, `SQL*Loader-500`...) i el text.
4. Busca el codi en la documentació oficial ([Oracle Error Help](https://docs.oracle.com/en/error-help/db/)).
5. Corretgix **una** cosa i repeteix.

### 7.2 Errors freqüents en còpies i importacions

| Missatge | Causa habitual | Solució |
|---|---|---|
| `ORA-39002: invalid operation` / `ORA-39070: Unable to open the log file` | El directori no existix o l'usuari no pot escriure | Comprovar `DBA_DIRECTORIES` i permisos |
| `ORA-39087: directory name DATA_PUMP_DIR is invalid` | L'objecte `DIRECTORY` no existix en la PDB | Crear-lo o connectar-se a `FREEPDB1` |
| `ORA-31655: no data or metadata objects selected for job` | El filtre (`schemas`, `include`) no coincidix amb res | Revisar majúscules i noms |
| `ORA-31684: Object type USER:"EDUGEST_COPIA" already exists` | L'usuari de destinació ja existix | És un avís; es pot ignorar si és l'esperat |
| `ORA-39151: Table "X"."Y" exists. All dependent metadata and data will be skipped` | La taula ja existix en la destinació | `table_exists_action=REPLACE` o `TRUNCATE` |
| `ORA-00001: unique constraint ... violated` (en `sqlldr`) | Clau duplicada en el fitxer | Revisar el `.bad` |
| `ORA-01722: invalid number` | Un text on s'esperava un nombre | Revisar separadors i decimals |
| `SQL*Loader-350: Syntax error` | Error en el fitxer `.ctl` | Revisar comes, parèntesis i nom de columnes |
| `mongorestore: ... E11000 duplicate key error` | El document ja existix en la destinació | Usar `--drop` o restaurar en una altra base de dades |

### 7.3 Altres fitxers de registre

- **Alert log** d'Oracle (`alert_FREE.log`): esdeveniments de la instància. En el contenidor, `docker logs oracle26ai` mostra l'arrancada.
- **Registre de Docker** de MongoDB: `docker logs mongo8`.
- **Historial de treballs de Data Pump**: `SELECT owner_name, job_name, state FROM dba_datapump_jobs;`

## 8. Errors freqüents

| Error | Conseqüència | Prevenció |
|---|---|---|
| Guardar la còpia en el mateix disc/contenidor | Es perd tot alhora | Regla 3-2-1 |
| No provar mai la restauració | La còpia no servix quan fa falta | Simulacre periòdic en un altre esquema |
| Exportar sense `UTF-8` | Caràcters corruptes | Fixar la codificació |
| Deixar còpies sense xifrar en un USB | Fuga de dades personals (RGPD) | Xifrar i limitar accessos |
| Restaurar damunt de les dades reals | Es perd el que ha ocorregut des de la còpia | Restaurar primer en un altre esquema |
| No registrar quina còpia és quina | No se sap quina restaurar | Noms amb data i documentació |

## 9. Bones pràctiques

- Automatitza les còpies (un guió programat) i **revisa els logs**.
- Anomena els fitxers amb data i contingut: `edugest_20271105_completa.dmp`.
- Defineix qui pot fer i qui pot restaurar còpies (**mínim privilegi**).
- Documenta el procediment de restauració pas a pas i prova'l.
- Conserva diverses generacions de còpies, no només l'última.

## 10. Resum

- Una còpia es tria segons l'**RPO** i l'**RTO**; la regla **3-2-1** guia on es guarda.
- **Data Pump** fa còpies lògiques d'esquemes d'Oracle; **RMAN** fa còpies físiques.
- **`mongodump` / `mongorestore`** fan el mateix en MongoDB.
- Importar i exportar usa **CSV**, **JSON** o **SQL**: cuida codificació, dates, decimals i nuls.
- **SQL\*Loader** carrega fitxers amb un fitxer de control i genera `.log` i `.bad`.
- Transferir entre gestors = exportar → transformar → importar → **verificar**.
- Els **logs** diuen la causa: llig el primer error.

## 11. Autoavaluació

{{< quiz >}}
- q: "Fas una còpia completa el diumenge i una incremental cada nit. El dijous es perd el servidor. Què necessites per a restaurar?"
  options: ["Només la còpia del dimecres", "La completa del diumenge i totes les incrementals fins al dimecres", "Només la completa del diumenge", "Només la incremental més recent"]
  answer: 1
  explain: "Cada incremental guarda els canvis des de la còpia anterior, així que s'apliquen totes en ordre sobre la completa."
- q: "Si l'RPO d'una aplicació és d'1 hora, quina d'estes estratègies servix?"
  options: ["Una còpia completa cada nit", "Una còpia setmanal", "Còpies freqüents (almenys cada hora) o arxivat continu", "Cap, l'RPO no afecta l'estratègia"]
  answer: 2
  explain: "L'RPO és la pèrdua de dades admissible. Amb 1 hora cal copiar, com a mínim, cada hora."
- q: "Què fa `impdp ... remap_schema=EDUGEST:EDUGEST_COPIA`?"
  options: ["Esborra EDUGEST i crea EDUGEST_COPIA", "Importa els objectes del bolcat en l'esquema EDUGEST_COPIA en lloc de en EDUGEST", "Canvia la contrasenya de l'usuari", "Exporta EDUGEST_COPIA"]
  answer: 1
  explain: "Permet restaurar en un altre usuari, que és la forma segura de provar una còpia sense tocar les dades reals."
- q: "Després d'una càrrega amb SQL*Loader, on mires les files que la base de dades ha rebutjat?"
  options: ["Només en el fitxer `.log`", "En el fitxer `.bad`", "En l'alert log", "En la taula de destinació"]
  answer: 1
  explain: "El `.bad` conté les files rebutjades; el `.log` explica per què."
- q: "Exportes un CSV des d'Oracle i en importar-lo en un altre gestor `Ramón` apareix com `RamÃ³n`. Quina és la causa més probable?"
  options: ["Un error de clau primària", "Una diferència de codificació (UTF-8 enfront d'una altra)", "Un problema d'RPO", "Falta de privilegis"]
  answer: 1
  explain: "És el símptoma típic de llegir un fitxer UTF-8 com si fóra una altra codificació."
- q: "Quina còpia és **física**?"
  options: ["Un bolcat `.dmp` de Data Pump", "Un `mongodump`", "Copiar el volum de dades amb el servei parat", "Un CSV exportat"]
  answer: 2
  explain: "Una còpia física copia els fitxers de la base de dades; les altres són lògiques (objectes i dades)."
{{< /quiz >}}

## Referències

- [Oracle AI Database 26ai: Utilities, *Oracle Data Pump*](https://docs.oracle.com/en/database/oracle/oracle-database/26/sutil/) — `expdp`, `impdp` i els seus paràmetres.
- [Oracle AI Database 26ai: Utilities, *SQL\*Loader*](https://docs.oracle.com/en/database/oracle/oracle-database/26/sutil/) — fitxer de control, `.log` i `.bad`.
- [Oracle AI Database 26ai: Backup and Recovery User's Guide](https://docs.oracle.com/en/database/oracle/oracle-database/26/bradv/) — RMAN i estratègies de còpia.
- [Oracle SQLcl: documentació](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/) — `SET SQLFORMAT`, `SPOOL`.
- [Oracle Database Error Help](https://docs.oracle.com/en/error-help/db/).
- [MongoDB Database Tools](https://www.mongodb.com/docs/database-tools/) — `mongodump`, `mongorestore`, `mongoexport` i `mongoimport`.
- [Reial decret 1629/2009, de 30 d'octubre (mòdul professional 0372 Gestió de bases de dades)](https://www.boe.es/eli/es/rd/2009/10/30/1629).
