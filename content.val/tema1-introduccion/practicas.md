---
title: "Pràctiques"
weight: 11
bookToc: true
---

# Tema 1 · Pràctiques

{{< ra "RA1" >}}

| Pràctica | Tipus | Nivell | CE principals |
|---|---|---|---|
| [1.1 De la fulla de càlcul al SGBD](#pràctica-11--de-la-fulla-de-càlcul-al-sgbd) | Guiada | ●○○ | RA1.a, RA1.d |
| [1.2 Primer contacte amb Oracle](#pràctica-12--primer-contacte-amb-oracle-dins-dun-sgbd) | Guiada | ●●○ | RA1.e |
| [1.3 Triar un SGBD per a cada cas](#pràctica-13--triar-un-sgbd-per-a-cada-cas) | Autònoma | ●●○ | RA1.b, RA1.f |
| [Projecte EduGest · Tema 1](#projecte-edugest--tema-1-informe-danàlisi) | Projecte | ●●○ | RA1.d |

---

## Pràctica 1.1 · De la fulla de càlcul al SGBD

{{< practica num="1.1" tipo="Guiada" duracion="2 sessions" nivel="1" ra="RA1: a, d" sgbd="Full de càlcul (LibreOffice Calc / Excel)" entrega="Document amb les respostes" >}}

#### Objectiu

Detectar els problemes que provoca guardar la informació en fitxers independents i justificar amb arguments tècnics per què una organització necessita un sistema gestor de bases de dades.

#### Context

L'acadèmia d'idiomes **Lingua** ho gestiona tot amb un full de càlcul que compartixen la secretària i dos professors per correu electrònic. Cada fila representa la inscripció d'un alumne en un curs:

| fila | alumne | telefon | email | curs | professor | tlf_professor | preu | pagat |
|---|---|---|---|---|---|---|---|---|
| 1 | Ana Ruiz | 611222333 | ana@mail.com | Anglés B1 | John Smith | 699111222 | 90 € | Sí |
| 2 | Ana Ruiz | 611222333 | ana.ruiz@mail.com | Francés A2 | Marie Blanc | 699333444 | 80 € | No |
| 3 | Luis Gil | 622333444 | luis@mail.com | Anglés B1 | John Smith | 699111222 | 90 € | Sí |
| 4 | Eva Mora | 633444555 | eva@mail.com | Anglés B1 | Jhon Smith | 699111000 | 95 € | Sí |
| 5 | Luis Gil | 622333444 | luis@mail.com | Alemany A1 | | | 100 | Sí |

A més, el professor d'anglés guarda una **còpia pròpia** del fitxer en el seu portàtil, on afig les notes dels seus alumnes.

#### Requisits

- Haver llegit els apartats 3 i 4 de la teoria (fitxers tradicionals i SGBD).
- Un full de càlcul per a reproduir la taula (opcional).

#### Enunciat

Analitza el full i respon de manera raonada:

1. Localitza almenys **quatre inconsistències** en les dades. Indica la fila i la columna de cadascuna.
2. Identifica la **redundància**: quines dades es repetixen i quantes vegades caldria modificar el full si John Smith canvia de telèfon?
3. Descriu una **anomalia d'inserció**, una de **modificació** i una d'**esborrat** amb exemples concrets d'este full.
4. Quins problemes provoca la **còpia pròpia** del professor d'anglés?
5. Què ocorre si la secretària i un professor obrin i guarden el fitxer alhora?
6. Redacta un paràgraf dirigit a la direcció de l'acadèmia que justifique l'ús d'un SGBD. Usa almenys cinc de les funcions d'un SGBD que apareixen en la teoria.

#### Desenvolupament

{{% steps %}}

1. **Busca valors distints per a un mateix fet.** Recorre el full columna a columna. Pregunta't: «Pot tindre este dada un únic valor correcte?». Per exemple, el correu d'una persona o el preu d'un curs.

2. **Compta les repeticions.** Per a cada entitat (alumne, professor, curs), anota quantes files repetixen les seues dades. Això és redundància.

3. **Pensa en operacions, no en dades.** Per a trobar anomalies imagina tres situacions: donar d'alta un curs nou que encara no té alumnes, canviar el preu de l'anglés B1 i donar de baixa l'única alumna d'un curs.

4. **Relaciona cada problema amb una funció del SGBD.** Per exemple: redundància ↔ disseny integrat de les dades; accés simultani ↔ control de concurrència.

{{% /steps %}}

{{% details title="Pista per a l'apartat 3" %}}
- **Inserció:** es pot registrar el curs *Italià A1* amb el seu preu si encara no hi ha cap alumne inscrit?
- **Modificació:** si l'anglés B1 puja a 95 €, quantes files cal canviar? Què passa si se n'oblida una?
- **Esborrat:** si Luis Gil es dona de baixa d'alemany (fila 5), quina informació sobre el curs d'alemany desapareix?
{{% /details %}}

#### Comprovació

{{% comprobacion %}}
La teua resposta és completa si:

- [ ] Trobes les inconsistències del correu d'Ana (files 1 i 2), del nom i el telèfon del professor (fila 4), del preu d'anglés B1 (fila 4) i del format del preu (fila 5, sense «€»).
- [ ] Indiques que el telèfon de John Smith hauria de canviar-se en **3 files**.
- [ ] Les tres anomalies s'expliquen amb un exemple del full, no amb una definició genèrica.
- [ ] El paràgraf final menciona concurrència, integritat, seguretat, independència de les dades i còpies de seguretat.

{{< solucion id="tema1-001" title="Solució orientativa" />}}
{{% /comprobacion %}}

#### Errors habituals

> [!WARNING]
> - Confondre **redundància** amb **inconsistència**. La redundància és repetir una dada; la inconsistència és que les seues còpies no coincidisquen. La primera provoca la segona.
> - Respondre amb definicions copiades en lloc d'exemples del full. El criteri RA1.d demana **avaluar** la utilitat del SGBD en un cas concret.

#### Ampliació

Proposa com dividiries el full en **diverses taules** perquè cada dada aparega una sola vegada. No cal usar la notació formal: basta amb indicar quines columnes aniria en cada taula i com es relacionen. Guarda la proposta: la revisarem en el tema 2 (normalització).

---

## Pràctica 1.2 · Primer contacte amb Oracle: dins d'un SGBD

{{< practica num="1.2" tipo="Guiada" duracion="3 sessions" nivel="2" ra="RA1: e" sgbd="Oracle AI Database 26ai Free · Docker · SQL Developer o SQLcl" entrega="Fitxer d'eixida (SPOOL) + respostes" >}}

#### Objectiu

Instal·lar un SGBD real i reconéixer en ell els elements estudiats en la teoria: instància i base de dades, processos, memòria, fitxers de dades, diccionari de dades, usuaris i sessions.

#### Context

T'incorpores al departament de sistemes d'EduGest. Abans de començar a desenvolupar, el teu responsable et demana que poses en marxa l'entorn i que redactes una breu **fitxa tècnica** del servidor de bases de dades.

#### Requisits

- Docker Desktop (Windows/macOS) o Docker Engine (Linux) funcionant.
- 8 GB de RAM i 15 GB lliures en disc.
- La guia d'[instal·lació de l'entorn](/guia/entorno).

#### Desenvolupament

{{% steps %}}

1. **Instal·la i arranca Oracle AI Database 26ai Free** seguint la [guia de l'entorn](/guia/entorno#2-oracle-ai-database-26ai-free-en-un-contenidor). Espera al missatge `DATABASE IS READY TO USE!`.

2. **Connecta't com a `SYSTEM` al servei `FREEPDB1`** i activa el registre de la sessió per a conservar les evidències:

    ```sql
    SPOOL p1_2_salida.txt
    SHOW USER
    SHOW CON_NAME
    ```

3. **Identifica la versió i la instància.** Una *instància* és el conjunt de processos i memòria que dona servei; la *base de dades* són els fitxers en disc.

    ```sql
    SELECT banner_full FROM v$version;

    SELECT instance_name, host_name, version_full, status, startup_time
    FROM   v$instance;

    -- Bases de dades connectables (multitenant)
    SELECT con_id, name, open_mode FROM v$pdbs;
    ```

4. **Observa els processos en segon pla.** Cadascun correspon a un component de la teoria:

    ```sql
    SELECT name, description
    FROM   v$bgprocess
    WHERE  paddr <> '00'
    AND    name IN ('PMON', 'SMON', 'DBW0', 'LGWR', 'CKPT', 'MMON', 'RECO')
    ORDER  BY name;
    ```

5. **Revisa la memòria i la grandària de bloc.** El bloc és la unitat mínima de lectura i escriptura en disc (nivell intern d'ANSI/SPARC).

    ```sql
    SELECT name, value
    FROM   v$parameter
    WHERE  name IN ('db_block_size', 'sga_target', 'pga_aggregate_target', 'processes');
    ```

6. **Localitza els fitxers físics** de la base de dades connectable:

    ```sql
    SELECT tablespace_name, file_name, ROUND(bytes / 1024 / 1024) AS mb
    FROM   dba_data_files
    ORDER  BY tablespace_name;

    SELECT tablespace_name, contents, status FROM dba_tablespaces;
    ```

    Comprova que existixen de veritat des del terminal del teu equip:

    ```bash
    docker exec oracle26ai ls -lh /opt/oracle/oradata/FREE/FREEPDB1
    ```

7. **Consulta el diccionari de dades.** És la base de dades que descriu la base de dades (metadades).

    ```sql
    SELECT COUNT(*) AS vistas_diccionario FROM dictionary;

    SELECT table_name, comments
    FROM   dictionary
    WHERE  table_name IN ('USER_TABLES', 'USER_CONSTRAINTS', 'DBA_USERS', 'V$SESSION');
    ```

8. **Identifica els usuaris i les sessions obertes:**

    ```sql
    SELECT username, account_status, created
    FROM   dba_users
    WHERE  oracle_maintained = 'N'
    ORDER  BY created;

    SELECT sid, username, program, status
    FROM   v$session
    WHERE  username IS NOT NULL;
    ```

    Obri **una segona connexió** (per exemple, SQL Developer i SQLcl alhora) i repetix l'última consulta. Què canvia?

9. **Tanca el registre** amb `SPOOL OFF`.

{{% /steps %}}

> [!TIP]
> Les vistes que comencen per `V$` són **vistes dinàmiques de rendiment**: mostren l'estat de la instància en memòria en eixe moment. Les que comencen per `DBA_`, `ALL_` i `USER_` formen el **diccionari de dades**: descriuen els objectes guardats en la base de dades.

#### Preguntes

1. Quina diferència hi ha entre la **instància** `FREE` i la **base de dades** `FREEPDB1`?
2. Associa cada procés del pas 4 amb una funció del SGBD (escriptura de dades, registre de transaccions, recuperació després d'una fallada...).
3. Quina és la grandària de bloc? Per què un SGBD llig blocs i no files soltes?
4. En quin nivell de l'arquitectura ANSI/SPARC situaries els fitxers `.dbf` del pas 6? I la vista `USER_TABLES`?
5. Quants usuaris no mantinguts per Oracle hi ha? Quin usuari usaries per a treballar en el projecte i per què **no** hauries d'usar `SYSTEM`?

#### Comprovació

{{% comprobacion %}}
- [ ] `v$version` mostra *Oracle AI Database 26ai Free*.
- [ ] `v$pdbs` mostra `FREEPDB1` en mode `READ WRITE`.
- [ ] Apareixen almenys els processos `PMON`, `SMON`, `DBW0`, `LGWR` i `CKPT`.
- [ ] El fitxer `p1_2_salida.txt` conté l'eixida de totes les consultes.
- [ ] En obrir la segona connexió apareix una sessió més en `v$session`.

{{< solucion id="tema1-002" title="Solució de les preguntes" />}}
{{% /comprobacion %}}

#### Errors habituals

| Error | Causa | Solució |
|---|---|---|
| `ORA-00942: table or view does not exist` en consultar `v$...` | Estàs connectat amb un usuari sense privilegis d'administració | Connecta't com a `SYSTEM` |
| `ORA-12514` | La base de dades encara arranca o has escrit mal el servei | Espera i usa `FREEPDB1` |
| `docker: Error response from daemon: Conflict` | Ja existix un contenidor amb eixe nom | `docker start oracle26ai` en lloc de `docker run` |

#### Ampliació

Executa `docker stats oracle26ai` mentre llances diverses consultes. Anota la memòria que consumix el contenidor i relaciona-la amb el paràmetre `sga_target`. Després executa l'script `edugest_00_usuario.sql` del [projecte EduGest](/guia/proyecto-edugest) i comprova que el nou usuari apareix en `dba_users`.

---

## Pràctica 1.3 · Triar un SGBD per a cada cas

{{< practica num="1.3" tipo="Autónoma" duracion="2 sessions" nivel="2" ra="RA1: b, d, f" sgbd="Navegador web (documentació oficial, DB-Engines)" entrega="Informe comparatiu (màx. 4 pàgines)" >}}

#### Objectiu

Classificar els SGBD amb criteris tècnics i justificar quin convé en situacions professionals distintes.

#### Context

Una consultora de desenvolupament rep quatre encàrrecs i et demana una recomanació raonada del sistema d'emmagatzematge de cadascun.

#### Enunciat

| Cas | Descripció |
|---|---|
| **A. App de receptes sense connexió** | Aplicació Android que guarda receptes i llistes de la compra al mòbil. Ha de funcionar sense Internet. Un únic usuari. |
| **B. Botiga en línia** | Catàleg de 5000 productes, comandes, pagaments i factures. Diversos empleats treballen alhora. Els pagaments no poden quedar a mitges. |
| **C. Xarxa professional** | Milions d'usuaris. La funció principal és recomanar contactes de «segon i tercer grau» (amics d'amics). |
| **D. Monitoratge d'hivernacles** | 3000 sensors envien temperatura i humitat cada 10 segons. Es consulten gràfiques per rangs de temps. |

Per a cada cas:

1. Classifica la necessitat segons el **model de dades**, el **nombre d'usuaris**, la **ubicació** i el **propòsit** (OLTP, OLAP o un altre).
2. Proposa **dos** SGBD concrets i compara'ls en una taula: model, llicència, desplegament (local, núvol), suport de transaccions i última versió estable (consulta el web oficial).
3. Recomana'n un i justifica la decisió en un paràgraf. Indica també què **perdries** amb l'altra opció.

Acaba amb una taula resum i una conclusió: existix un SGBD que siga el millor per a tot?

#### Comprovació

{{% comprobacion %}}
- [ ] Cada cas té classificació, comparativa, recomanació i el desavantatge de l'alternativa.
- [ ] Les versions i llicències procedixen de fonts oficials i estan citades amb data de consulta.
- [ ] Almenys un cas usa un SGBD relacional i almenys un altre un de no relacional.
- [ ] El cas B justifica la necessitat de **transaccions ACID**.

{{% details title="Pista: per on començar" %}}
- Fixa't en les paraules clau de cada enunciat: «sense connexió» i «un únic usuari» → embegut; «pagaments no poden quedar a mitges» → transaccions; «amics d'amics» → relacions entre nodes; «cada 10 segons» i «rangs de temps» → sèries temporals.
- [DB-Engines](https://db-engines.com/en/ranking) classifica centenars de SGBD per model i popularitat. Usa'l com a punt de partida, però contrasta les dades en el web oficial de cada producte.
{{% /details %}}
{{% /comprobacion %}}

#### Errors habituals

> [!WARNING]
> Triar el SGBD «més popular» o «el que conec» no és una justificació. Cada recomanació ha de recolzar-se en una característica del cas.

#### Ampliació

Afig un cas E proposat per tu, a partir d'una empresa real del teu entorn (per exemple, la de les teues pràctiques en empresa), i resol-lo amb el mateix esquema.

---

## Projecte EduGest · Tema 1: informe d'anàlisi

{{< practica num="EduGest-1" tipo="Proyecto" duracion="Treball transversal (1 setmana)" nivel="2" ra="RA1: c, d, f · Ampliació" sgbd="Document Markdown en el repositori" entrega="edugest/docs/01-analisis.md" >}}

#### Objectiu

Iniciar el projecte transversal amb una anàlisi del sistema actual i la justificació tècnica de la solució.

#### Enunciat

Llig l'[enunciat d'EduGest](/guia/proyecto-edugest) i redacta `01-analisis.md` amb estos apartats:

1. **Situació actual.** El centre usa un full de càlcul per cicle i un altre de faltes per cada professor. Descriu tres problemes concrets que provoca.
2. **Usuaris del sistema.** Identifica els perfils (secretaria, professorat, tutoria, direcció, alumnat, administrador de la base de dades) i què necessita fer cadascun. Relaciona'ls amb els perfils d'usuari d'un SGBD.
3. **Solució proposada.** Tipus de SGBD (model, ubicació, llicència) i justificació. Explica per què usarem Oracle per a la part relacional.
4. **Glossari.** Deu termes del tema amb la teua pròpia definició.

#### Comprovació

{{% comprobacion %}}
- [ ] El document està en el repositori, en Markdown, i es llig bé en GitHub o GitLab.
- [ ] Cada perfil d'usuari té almenys dos operacions concretes.
- [ ] L'elecció del SGBD es recolza en característiques del cas, no en preferències.
{{% /comprobacion %}}
