---
title: "Còpies de seguretat, importació i exportació - Pràctiques (Part II)"
weight: 4
bookToc: true
---

# UD08 · Pràctiques · Còpies de seguretat, importació i exportació

{{< ra "RA6:a,b,c,d,e,f,g,h" >}}

| Pràctica | Tipus | Nivell | CE principals |
|---|---|---|---|
| [8.9 Còpia lògica i restauració de la base de dades EduGest](#pràctica-89--còpia-lògica-i-restauració-de-la-base-de-dades-edugest) | Guiada | ●●○ | RA6.a, RA6.b, RA6.c |
| [8.10 Exportar dades a CSV, JSON i SQL](#pràctica-810--exportar-dades-a-csv-json-i-sql) | Guiada | ●○○ | RA6.d, RA6.e |
| [8.11 Importar amb SQL\*Loader i llegir els errors](#pràctica-811--importar-amb-sqlloader-i-llegir-els-errors) | Autònoma | ●●○ | RA6.f, RA6.g |
| [8.12 Oracle cap a MongoDB](#pràctica-812--oracle-cap-a-mongodb) | Guiada | ●●○ | RA6.e, RA6.f, RA6.h |
| [8.13 Repte: pla de còpies i simulacre de desastre](#pràctica-813--repte-pla-de-còpies-i-simulacre-de-desastre) | Repte | ●●● | RA6.a, RA6.b, RA6.c, RA6.g |
| [Projecte EduGest · UD08b](#projecte-edugest--ud08b-seguretat-de-la-informació) | Projecte | ●●● | RA6 complet |

> [!IMPORTANT]
> Estes pràctiques suposen que tens EduGest carregat i els contenidors `oracle26ai` i `mongo8` en marxa (guia d'[entorn](/guia/entorno)). Les comprovacions de files suposen les dades originals: 32 alumnes i 143 matrícules.

---

## Pràctica 8.9 · Còpia lògica i restauració de la base de dades EduGest

{{< practica num="8.9" tipo="Guiada" duracion="2 sessions" nivel="2" ra="RA6: a, b, c" sgbd="Oracle 26ai · Data Pump · Docker" entrega="edugest_exp.log + edugest_imp.log + captures de la comprovació" >}}

#### Objectiu

Fer una còpia lògica de l'esquema `EDUGEST`, traure-la del contenidor i restaurar-la en un esquema de proves, comprovant que no s'ha perdut res.

#### Desenvolupament

{{% steps %}}

1. **Localitza el directori de Data Pump.** Com a `SYSTEM` a `FREEPDB1`:

    ```sql
    SELECT directory_path FROM dba_directories WHERE directory_name = 'DATA_PUMP_DIR';
    ```

    Anota la ruta. És la mateixa carpeta que conté les dades de la base de dades, o una apartada?

2. **Exporta l'esquema.** En una terminal del teu equip:

    ```bash
    docker exec -it oracle26ai expdp system/Oracle_2026@//localhost:1521/FREEPDB1 \
      schemas=EDUGEST directory=DATA_PUMP_DIR dumpfile=edugest_%U.dmp logfile=edugest_exp.log
    ```

    Llig les últimes línies. Ha d'aparéixer `successfully completed`. Anota quantes files va exportar d'`ALUMNO` i de `MATRICULA`.

3. **Trau la còpia del contenidor** i comprova la seua grandària:

    ```bash
    mkdir -p copias
    docker cp oracle26ai:<ruta-del-pas-1>/edugest_01.dmp ./copias/
    docker cp oracle26ai:<ruta-del-pas-1>/edugest_exp.log ./copias/
    ```

4. **Crea l'usuari de proves** (com a `SYSTEM`):

    ```sql
    CREATE USER edugest_copia IDENTIFIED BY "Copia_2026"
      DEFAULT TABLESPACE users QUOTA UNLIMITED ON users;
    GRANT CREATE SESSION, CREATE TABLE, CREATE SEQUENCE, CREATE VIEW,
          CREATE PROCEDURE, CREATE TRIGGER TO edugest_copia;
    ```

5. **Restaura en l'esquema de proves:**

    ```bash
    docker exec -it oracle26ai impdp system/Oracle_2026@//localhost:1521/FREEPDB1 \
      directory=DATA_PUMP_DIR dumpfile=edugest_%U.dmp logfile=edugest_imp.log \
      remap_schema=EDUGEST:EDUGEST_COPIA
    ```

6. **Comprova la restauració** comparant recomptes i diferències:

    ```sql
    SELECT 'ALUMNO' tabla, (SELECT COUNT(*) FROM edugest.alumno) original,
                           (SELECT COUNT(*) FROM edugest_copia.alumno) copia FROM dual
    UNION ALL
    SELECT 'MATRICULA', (SELECT COUNT(*) FROM edugest.matricula),
                        (SELECT COUNT(*) FROM edugest_copia.matricula) FROM dual;

    SELECT * FROM edugest.alumno MINUS SELECT * FROM edugest_copia.alumno;
    ```

7. **Obtín només l'estructura.** Executa `impdp` amb `sqlfile=estructura.sql` (sense `remap_schema` i sense importar). Obri el fitxer generat: reconeixes les sentències `CREATE TABLE` de la UD05?

{{% /steps %}}

#### Comprovació

{{% comprobacion %}}
- [ ] `edugest_exp.log` acaba amb `successfully completed` i el bolcat `.dmp` està fora del contenidor.
- [ ] El pas 6 mostra 32 alumnes i 143 matrícules en l'original i en la còpia, i la consulta amb `MINUS` torna 0 files.
- [ ] Saps explicar per què es restaura primer en `EDUGEST_COPIA` i no damunt d'`EDUGEST`.
{{% /comprobacion %}}

#### Errors habituals

> [!WARNING]
> - `ORA-39087` o `ORA-39070`: el nom del directori és incorrecte o t'has connectat a la CDB. Usa `FREEPDB1`.
> - `ORA-01918: user 'EDUGEST_COPIA' does not exist`: et vas saltar el pas 4.
> - El `.dmp` no apareix en fer `docker cp`: la ruta ha de ser la del pas 1, **dins del contenidor**.

#### Ampliació

Repetix l'exportació amb `content=metadata_only` i amb `tables=ALUMNO query=ALUMNO:"WHERE cod_grupo='1DAM'"`. Compara la grandària dels tres bolcats.

---

## Pràctica 8.10 · Exportar dades a CSV, JSON i SQL

{{< practica num="8.10" tipo="Guiada" duracion="1 sessió" nivel="1" ra="RA6: d, e" sgbd="Oracle 26ai · SQLcl · SQL Developer" entrega="alumnado.csv + alumnado.json + alumnado_insert.sql" >}}

#### Objectiu

Exportar el mateix resultat a diferents formats amb ferramentes de línia d'ordres i amb l'assistent gràfic.

#### Desenvolupament

{{% steps %}}

1. **CSV amb SQLcl.** Connectat com a `EDUGEST`:

    ```sql
    SET SQLFORMAT csv
    SPOOL alumnado.csv
    SELECT nia, nombre, apellidos, cod_grupo FROM alumno ORDER BY nia;
    SPOOL OFF
    ```

    Obri el fitxer amb un editor de text i amb un full de càlcul. Es veuen bé els accents en els dos?

2. **JSON i sentències `INSERT`:**

    ```sql
    SET SQLFORMAT json
    SPOOL alumnado.json
    SELECT nia, nombre, apellidos, cod_grupo FROM alumno ORDER BY nia;
    SPOOL OFF

    SET SQLFORMAT insert
    SPOOL alumnado_insert.sql
    SELECT nia, nombre, apellidos, cod_grupo FROM alumno ORDER BY nia;
    SPOOL OFF
    SET SQLFORMAT default
    ```

3. **Assistent gràfic.** En SQL Developer: clic dret sobre la taula `GRUPO` → *Exportar*. Tria format *CSV*, marca *Capçalera* i guarda el fitxer. Repetix amb format *insert*.

4. **Compara les tres eixides** en una taula: format, grandària del fitxer i què passa amb una columna que continga una coma o un valor nul.

{{% /steps %}}

#### Comprovació

{{% comprobacion %}}
- [ ] `alumnado.csv` té 33 línies (capçalera i 32 alumnes).
- [ ] `alumnado_insert.sql` conté 32 sentències `INSERT`.
- [ ] Has localitzat en el CSV un camp entre cometes i pots explicar per què.
{{% /comprobacion %}}

#### Errors habituals

> [!WARNING]
> Si el fitxer es crea buit, vas oblidar tancar amb `SPOOL OFF` o vas executar la consulta abans de `SPOOL`. Si els accents isquen malament en el full de càlcul, és un problema de **codificació** en obrir-lo, no de l'exportació.

---

## Pràctica 8.11 · Importar amb SQL\*Loader i llegir els errors

{{< practica num="8.11" tipo="Autónoma" duracion="1 sessió" nivel="2" ra="RA6: f, g" sgbd="Oracle 26ai · SQL*Loader" entrega="carga_alumnos.ctl + carga.log + carga.bad + informe" >}}

#### Objectiu

Carregar un fitxer CSV en una taula, localitzar les files rebutjades i explicar la causa de cada rebuig a partir del registre.

#### Enunciat

Crea la taula de destinació com a `EDUGEST`:

```sql
CREATE TABLE alumno_carga (
  nia        CHAR(8)       CONSTRAINT pk_alumno_carga PRIMARY KEY,
  nombre     VARCHAR2(50)  NOT NULL,
  apellidos  VARCHAR2(80),
  cod_grupo  VARCHAR2(6)   CONSTRAINT ck_alumno_carga_grupo
             CHECK (cod_grupo IN ('1DAM','2DAM','1DAW','2DAW','1ASIR','2ASIR'))
);
```

Guarda este contingut com a `alumnos_nuevos.csv` (UTF-8):

```text
nia,nombre,apellidos,cod_grupo
10460001,Lucía,Marín Soler,1ASIR
10460002,Pau,Giner Calvo,1ASIR
10460003,Aitana,Pérez Ruiz,1ASIR
10460004,Marc,"Vidal, Ferrando",1ASIR
10460002,Pablo,Giner Calvo,1ASIR
10460006,,Sempere Mira,1ASIR
10460007,Nuria,Beltrán Pons,3ASIR
10460008,Iván,Cano Lillo,1ASIR
```

1. Escriu el fitxer de control `carga_alumnos.ctl` (usa `CHARACTERSET UTF8`, `OPTIONS (SKIP=1)` per a saltar la capçalera, `APPEND` i els separadors adequats).
2. Copia els dos fitxers al contenidor (`docker cp ... oracle26ai:/tmp/`) i executa `sqlldr` amb `docker exec -w /tmp`, indicant `log=` i `bad=`.
3. Obri el `.log` i el `.bad`. Ompli una taula amb una fila per cada registre rebutjat: número de línia, codi `ORA-` i causa.
4. Corretgix el CSV (no la taula) i torna a carregar **només** les files rebutjades.

{{% details title="Pista: estructura del fitxer de control" %}}
Necessites `OPTIONS`, `LOAD DATA`, `CHARACTERSET`, `INFILE`, `APPEND`, `INTO TABLE`, `FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'`, `TRAILING NULLCOLS` i la llista de columnes entre parèntesis. Consulta l'exemple de la teoria §5.3.
{{% /details %}}

#### Comprovació

{{% comprobacion %}}
- [ ] Després de la primera càrrega, `SELECT COUNT(*) FROM alumno_carga;` torna **5** i el log indica 3 files rebutjades.
- [ ] Has identificat una violació de clau primària (`ORA-00001`), un valor nul en columna obligatòria (`ORA-01400`) i una violació de `CHECK` (`ORA-02290`).
- [ ] Després de la correcció, la taula té 8 files sense duplicats.
{{% /comprobacion %}}

#### Errors habituals

> [!WARNING]
> - `SQL*Loader-350: Syntax error`: revisa comes i parèntesis del `.ctl`.
> - Accents corruptes (`LucÃ­a`): falta `CHARACTERSET UTF8` o el CSV no està guardat en UTF-8.
> - `SQL*Loader-500: Unable to open file`: el CSV no està en la carpeta des d'on executes (`-w /tmp`).

---

## Pràctica 8.12 · Oracle cap a MongoDB

{{< practica num="8.12" tipo="Guiada" duracion="1 sessió" nivel="2" ra="RA6: e, f, h" sgbd="Oracle 26ai · SQLcl · MongoDB 8.0" entrega="alumnado_mongo.json + captures de la verificació" >}}

#### Objectiu

Transferir informació entre dos sistemes gestors diferents i comprovar que no es perd ni es deforma.

#### Desenvolupament

{{% steps %}}

1. **Genera un JSON per alumne des d'Oracle**, amb dates en ISO 8601:

    ```sql
    SET SQLFORMAT default
    SET PAGESIZE 0
    SET FEEDBACK OFF
    SET LINESIZE 4000
    SPOOL alumnado_mongo.json
    SELECT JSON_OBJECT(
             'nia'              VALUE nia,
             'nombre'           VALUE nombre,
             'apellidos'        VALUE apellidos,
             'grupo'            VALUE cod_grupo,
             'fecha_nacimiento' VALUE TO_CHAR(fecha_nacimiento, 'YYYY-MM-DD'))
    FROM   alumno ORDER BY nia;
    SPOOL OFF
    ```

    Obri el fitxer: ha d'haver-hi 32 línies, cadascuna un objecte JSON.

2. **Copia'l al contenidor de MongoDB i importa'l:**

    ```bash
    docker cp alumnado_mongo.json mongo8:/tmp/
    docker exec mongo8 mongoimport --db=edugest_gbd --collection=alumnado --file=/tmp/alumnado_mongo.json
    ```

3. **Verifica** en `mongosh`:

    ```javascript
    use edugest_gbd
    db.alumnado.countDocuments()
    db.alumnado.findOne({ nia: "10450037" })
    db.alumnado.countDocuments({ grupo: "1DAM" })
    ```

    Compara els resultats amb `SELECT COUNT(*) FROM alumno` i `... WHERE cod_grupo = '1DAM'` en Oracle.

4. **Inspecciona els tipus.** La data de naixement és en MongoDB un tipus data o un text? Usa `typeof db.alumnado.findOne().fecha_nacimiento` i explica què caldria fer per a guardar-la com a data.

5. **Exporta de tornada** una col·lecció amb `mongoexport` en CSV (`--type=csv --fields=nia,nombre,grupo`) i obri-la en un full de càlcul.

{{% /steps %}}

#### Comprovació

{{% comprobacion %}}
- [ ] `db.alumnado.countDocuments()` torna 32 i coincidix amb Oracle.
- [ ] L'alumne de NIA 10450037 apareix com «Adrián Ferri Baeza», amb l'accent ben posat.
- [ ] Expliques per què la data arriba com a text i com convertir-la.
{{% /comprobacion %}}

#### Errors habituals

> [!WARNING]
> Si `mongoimport` informa de `0 document(s) imported`, mira si el fitxer té línies que no són JSON (capçaleres, línies en blanc o missatges de SQLcl). Si falta `mongoimport`, consulta l'avís de la teoria §4.

---

## Pràctica 8.13 · Repte: pla de còpies i simulacre de desastre

{{< practica num="8.13" tipo="Reto" duracion="2 sessions" nivel="3" ra="RA6: a, b, c, g" sgbd="Oracle 26ai · Data Pump · Docker" entrega="plan_copias.md + copia_edugest.sh + registre del simulacre" >}}

#### Enunciat

L'institut et demana que protegisques EduGest. Has de lliurar:

1. **Un pla de còpies** (una pàgina) amb: què es copia, tipus de còpia, freqüència, on es guarda (regla 3-2-1), qui pot restaurar, quant es conserva, RPO i RTO justificats per a la secretaria durant el període d'avaluacions.
2. **Un guió** `copia_edugest.sh` que exporte l'esquema amb Data Pump, pose la data en el nom del fitxer, traga el `.dmp` i el `.log` del contenidor, **comprove** que el log conté `successfully completed` i avise si no és així.
3. **Un simulacre de desastre** sobre `EDUGEST_COPIA`: pren una còpia, esborra dades amb un `DELETE` sense `WHERE`, restaura-les amb `impdp` (`table_exists_action=REPLACE`) i demostra amb recomptes que has tornat a l'estat anterior. Registra l'hora d'inici i de fi: eixe és el teu RTO real.

{{% details title="Pista: comprovar el log en un guió" %}}
`grep -q "successfully completed" edugest_exp.log || echo "ERROR: la còpia ha fallat"`.
{{% /details %}}

#### Comprovació

{{% comprobacion %}}
- [ ] El pla complix 3-2-1 i justifica l'RPO.
- [ ] El guió genera un fitxer amb data en el nom i detecta una fallada (prova-ho amb un usuari o directori inexistent).
- [ ] El registre del simulacre inclou els recomptes abans, després del desastre i després de la restauració.
{{% /comprobacion %}}

---

## Projecte EduGest · UD08b: seguretat de la informació

{{< practica num="EduGest-8b" tipo="Proyecto" duracion="Treball transversal (1 setmana)" nivel="3" ra="RA6: a, b, c, d, e, f, g, h" sgbd="Oracle 26ai · MongoDB 8.0" entrega="edugest/10_seguridad/ + docs/10-seguridad.md" >}}

#### Enunciat

1. **Procediment de còpia i restauració** d'Oracle i de MongoDB, amb les ordres exactes, els usuaris necessaris i la ubicació dels fitxers.
2. **Guió d'exportació** del llistat d'alumnat d'un grup en CSV i JSON.
3. **Guió d'importació** d'un fitxer d'alumnat nou amb control de rebutjats i un informe de la càrrega.
4. **Transferència** dels expedients d'EduGest a MongoDB amb verificació de recomptes.
5. **Taula d'errors** amb almenys cinc missatges que hages obtingut, la seua causa i la seua solució.

#### Comprovació

{{% comprobacion %}}
- [ ] Un company pot restaurar EduGest seguint **només** el teu document.
- [ ] Cada transferència té la seua comprovació de recomptes.
- [ ] Les còpies que isquen de l'equip estan identificades amb data i s'indica com xifrar-les.
{{% /comprobacion %}}
