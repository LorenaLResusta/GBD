---
title: "Entorn de treball"
weight: 3
---

# Entorn de treball

Durant el curs usarem dos sistemes gestors:

| | Relacional (UD05 a UD09) | No relacional (UD10) |
|---|---|---|
| **SGBD** | Oracle AI Database 26ai Free | MongoDB Community Server 8.0 |
| **Versió de referència** | 23.26.x | 8.0.x |
| **Instal·lació recomanada** | Contenidor Docker o Podman | Contenidor Docker o Podman |
| **Client de línia d'ordres** | SQLcl (`sql`) o SQL\*Plus | `mongosh` |
| **Client gràfic** | Oracle SQL Developer o l'extensió *SQL Developer* per a VS Code | MongoDB Compass o l'extensió de MongoDB per a VS Code |
| **Modelatge** | Oracle SQL Developer Data Modeler, draw.io, Mermaid | — |

> [!NOTE]
> **Per què Oracle?** És un dels SGBD relacionals més implantats en grans organitzacions. El seu llenguatge procedimental (PL/SQL) és la referència per al RA5. L'edició *Free* no té cost, inclou les funcions de la versió comercial amb límits de grandària (2 CPU, 2 GB de RAM i 12 GB de dades d'usuari).
>
> **Per què MongoDB?** És la base de dades documental més utilitzada en el desenvolupament web i multiplataforma. El seu model de documents JSON permet comparar de forma molt clara amb el model relacional.

## 1. Requisits

- Sistema operatiu de 64 bits: Windows 10/11, macOS (Apple Silicon o Intel) o Linux.
- Almenys **8 GB de RAM** (Oracle Free reserva fins a 2 GB) i **15 GB lliures** en disc.
- **Docker Desktop** (Windows i macOS) o **Docker Engine / Podman** (Linux). En Windows, Docker Desktop necessita **WSL 2**.

> [!TIP]
> Si el teu equip no pot executar contenidors, en Windows pots instal·lar Oracle AI Database Free amb l'instal·lador ZIP oficial. També pots usar una màquina virtual Linux de l'aula. Els scripts del curs són els mateixos en tots els casos.

## 2. Oracle AI Database 26ai Free en un contenidor

{{% steps %}}

1. **Descarrega la imatge oficial** des del registre de contenidors d'Oracle:

    ```bash
    docker pull container-registry.oracle.com/database/free:latest
    ```

2. **Crea i arranca el contenidor.** La variable `ORACLE_PWD` fixa la contrasenya de `SYS`, `SYSTEM` i `PDBADMIN`. El volum `oracle-data` conserva les dades encara que esborres el contenidor.

    ```bash
    docker run -d --name oracle26ai \
      -p 1521:1521 \
      -e ORACLE_PWD=Oracle_2026 \
      -v oracle-data:/opt/oracle/oradata \
      container-registry.oracle.com/database/free:latest
    ```

    En PowerShell, substituïx `\` pel caràcter de continuació `` ` `` o escriu l'ordre en una sola línia.

3. **Espera que la base de dades estiga llesta.** La primera vegada tarda uns minuts. Seguix el registre fins a vore `DATABASE IS READY TO USE!`:

    ```bash
    docker logs -f oracle26ai
    ```

4. **Comprova la connexió** amb SQL\*Plus, que ve dins del contenidor:

    ```bash
    docker exec -it oracle26ai sqlplus system/Oracle_2026@//localhost:1521/FREEPDB1
    ```

    ```sql
    SELECT banner_full FROM v$version;
    SHOW CON_NAME
    ```

    El resultat ha de mostrar `Oracle AI Database 26ai Free` i el contenidor `FREEPDB1`.

{{% /steps %}}

> [!IMPORTANT]
> Oracle Free usa una arquitectura **multitenant**. `FREE` és la base de dades contenidora (CDB) i `FREEPDB1` és la base de dades connectable (PDB) on treballarem. **Connecta't sempre al servei `FREEPDB1`.** Si crees usuaris en la CDB obtindràs l'error `ORA-65096: invalid common user or role name`.

### Gestió diària del contenidor

```bash
docker stop oracle26ai      # detindre en acabar la classe
docker start oracle26ai     # arrancar de nou (les dades es conserven)
docker ps -a                # vore l'estat dels contenidors
```

## 3. Clients per a Oracle

{{< tabs >}}
{{% tab "SQL Developer (gràfic)" %}}
1. Descarrega **Oracle SQL Developer** des del web d'Oracle. És una aplicació Java que no necessita instal·lació: basta amb descomprimir-la.
2. Crea una connexió nova:
   - **Nom:** `EduGest`
   - **Usuari:** `edugest` · **Contrasenya:** `Edugest_2026`
   - **Nom de host:** `localhost` · **Port:** `1521`
   - **Nom del servei:** `FREEPDB1` (marca *Nom del servei*, no *SID*)
3. Prem **Provar** i després **Connectar**.

Executa una sentència amb `Ctrl+Intro` i l'script complet amb `F5`.
{{% /tab %}}
{{% tab "VS Code" %}}
1. Instal·la l'extensió **SQL Developer for VS Code** (publicada per Oracle).
2. En el panell de l'extensió, crea una connexió amb les mateixes dades: `localhost`, port `1521`, servei `FREEPDB1`, usuari `edugest`.
3. Obri un fitxer `.sql`, selecciona la connexió i executa amb `Ctrl+Intro` (sentència) o `F5` (script).

És una bona opció si ja uses VS Code en altres mòduls i treballes els scripts amb Git.
{{% /tab %}}
{{% tab "SQLcl (terminal)" %}}
**SQLcl** és el client modern de línia d'ordres d'Oracle. Necessita Java 11 o superior.

```bash
sql edugest/Edugest_2026@//localhost:1521/FREEPDB1
```

Ordres útils de SQLcl i SQL\*Plus (no són SQL, són ordres del client):

| Ordre | Per a què servix |
|---|---|
| `DESC tabla` | Mostra l'estructura d'una taula |
| `@fichero.sql` | Executa un script |
| `SET SERVEROUTPUT ON` | Mostra l'eixida de `DBMS_OUTPUT` (UD09) |
| `SPOOL salida.txt` / `SPOOL OFF` | Guarda l'eixida en un fitxer (evidències) |
| `SET SQLFORMAT ansiconsole` | Taules més llegibles (només SQLcl) |
| `HISTORY` | Historial d'ordres (només SQLcl) |
{{% /tab %}}
{{< /tabs >}}

## 4. Crear l'esquema EduGest

Descarrega els scripts del [projecte EduGest](/guia/proyecto-edugest#4-scripts-descarregables) i executa'ls en ordre: `00` com a `SYSTEM`, i `01` i `02` com a `EDUGEST`.

```sql
-- Comprovació final, connectat com a EDUGEST
SELECT table_name, num_rows FROM user_tables ORDER BY table_name;
SELECT COUNT(*) FROM matricula;   -- 143
```

> [!WARNING]
> `num_rows` d'`USER_TABLES` mostra les **estadístiques** de l'optimitzador. Pot valdre `NULL` fins que Oracle les recopile. Per a comptar files de veritat usa `COUNT(*)`.

## 5. MongoDB Community Server 8.0 (UD10)

```bash
docker run -d --name mongo8 -p 27017:27017 \
  -v mongo-data:/data/db \
  mongodb/mongodb-community-server:8.0-ubi9

# La imatge inclou mongosh
docker exec -it mongo8 mongosh
```

```javascript
// Dins de mongosh
db.version()          // ha de començar per 8.0
show dbs
```

Com a client gràfic usa **MongoDB Compass** amb la cadena de connexió `mongodb://localhost:27017`.

> [!CAUTION]
> Estes instal·lacions són **per a l'aula**. MongoDB arranca sense autenticació i les contrasenyes d'Oracle són d'exemple. En la UD05 i en la UD10 vorem per què un servidor de bases de dades mai no ha d'exposar-se així en producció.

## 6. Problemes freqüents

| Símptoma | Causa probable | Solució |
|---|---|---|
| `ORA-12514: listener does not currently know of service` | La base de dades encara està arrancant o el servei és incorrecte | Espera a `DATABASE IS READY TO USE!` i usa `FREEPDB1` |
| `ORA-01017: invalid username/password` | Contrasenya incorrecta o usuari creat en una altra PDB | Revisa a quin servei et connectes en crear l'usuari |
| `ORA-65096: invalid common user or role name` | Estàs connectat a la CDB (`FREE`) | Connecta't a `FREEPDB1` |
| `ORA-01950: no privileges on tablespace 'USERS'` | L'usuari no té quota | `ALTER USER edugest QUOTA UNLIMITED ON users;` |
| El port 1521 o 27017 està ocupat | Hi ha una altra instància executant-se | `docker ps` i deté l'altra o canvia el port (`-p 1522:1521`) |
| El contenidor es deté sol | Falta memòria | Assigna almenys 4 GB a Docker Desktop o WSL 2 |

## Referències

- [Oracle AI Database Free: guia d'inici](https://www.oracle.com/database/free/get-started/).
- [Registre de contenidors d'Oracle: imatge `database/free`](https://container-registry.oracle.com/ords/ocr/ba/database/free).
- [Instal·lar MongoDB Community amb Docker](https://www.mongodb.com/docs/manual/administration/install-community-docker/).
