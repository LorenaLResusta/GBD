---
title: "Sistemes d'emmagatzematge i SGBD - Pràctiques"
weight: 2
bookToc: true
---

# UD01 · Pràctiques

{{< ra "RA1:a,b,c,d,e,f,g,h,i,j" "RA2:a" >}}

| Pràctica | Tipus | Nivell | CE principals |
|---|---|---|---|
| [1.1 De la fulla de càlcul al SGBD](#pràctica-11--de-la-fulla-de-càlcul-al-sgbd) | Guiada | ●○○ | RA1.a, RA1.d |
| [1.2 Primer contacte amb Oracle](#pràctica-12--primer-contacte-amb-oracle-dins-dun-sgbd) | Guiada | ●●○ | RA1.e, RA2.a |
| [1.3 Triar un SGBD per a cada cas](#pràctica-13--triar-un-sgbd-per-a-cada-cas) | Autònoma | ●●○ | RA1.b, RA1.f |
| [1.4 Disseny de la distribució de dades](#pràctica-14--disseny-de-la-distribució-de-dades) | Autònoma | ●●○ | RA1.c, RA1.g, RA1.h |
| [1.5 Auditoria de protecció de dades](#pràctica-15--auditoria-de-protecció-de-dades) | Repte | ●●● | RA1.i |
| [1.6 De les dades a les decisions](#pràctica-16--de-les-dades-a-les-decisions) | Autònoma | ●○○ | RA1.j |
| [Projecte EduGest · UD01](#projecte-edugest--ud01-informe-danàlisi) | Projecte | ●●○ | RA1.d, RA1.i |

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

{{< solucion id="ud01-001" title="Solució orientativa" />}}
{{% /comprobacion %}}

#### Errors habituals

> [!WARNING]
> - Confondre **redundància** amb **inconsistència**. La redundància és repetir una dada; la inconsistència és que les seues còpies no coincidisquen. La primera provoca la segona.
> - Respondre amb definicions copiades en lloc d'exemples del full. El criteri RA1.d demana **avaluar** la utilitat del SGBD en un cas concret.

#### Ampliació

Proposa com dividiries el full en **diverses taules** perquè cada dada aparega una sola vegada. No cal usar la notació formal: basta amb indicar quines columnes aniria en cada taula i com es relacionen. Guarda la proposta: la revisarem en la UD04 (normalització).

---

## Pràctica 1.2 · Primer contacte amb Oracle: dins d'un SGBD

{{< practica num="1.2" tipo="Guiada" duracion="3 sessions" nivel="2" ra="RA1: e · RA2: a, h" sgbd="Oracle AI Database 26ai Free · Docker · SQL Developer o SQLcl" entrega="Fitxer d'eixida (SPOOL) + respostes" >}}

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

{{< solucion id="ud01-002" title="Solució de les preguntes" />}}
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

## Pràctica 1.4 · Disseny de la distribució de dades

{{< practica num="1.4" tipo="Autónoma" duracion="2 sessions" nivel="2" ra="RA1: c, g, h" sgbd="Paper o draw.io (SQL conceptual)" entrega="Document amb el disseny" >}}

#### Objectiu

Decidir quan distribuir una base de dades i dissenyar una política de fragmentació que complisca les regles de completesa, reconstrucció i disjunció.

#### Context

**FarmaRed** és una cadena de farmàcies amb seus a València, Alacant i Castelló. Cada seu té el seu propi servidor. La taula central de clients és:

```text
CLIENTE(id_cliente, dni, nombre, apellidos, telefono, provincia,
        historial_dispensaciones, alergias, puntos_fidelidad)
```

- Cada farmàcia atén sobretot clients de la seua província.
- El departament de màrqueting (a València) necessita `id_cliente`, `nombre`, `provincia` i `puntos_fidelidad` de **tots** els clients.
- Només el personal farmacèutic pot consultar `historial_dispensaciones` i `alergias`.

#### Enunciat

1. Justifica si té sentit una base de dades **distribuïda** o si basta amb una **centralitzada**. Considera la disponibilitat si cau la connexió entre seus.
2. Dissenya una **fragmentació horitzontal** de `CLIENTE` per província. Escriu la condició de cada fragment i en quin node es guarda.
3. Dissenya una **fragmentació vertical** que separe les dades sanitàries. Quina columna ha de repetir-se en tots els fragments? Per què?
4. Combina-les en una **fragmentació mixta** i dibuixa el resultat (nodes i fragments).
5. Escriu en SQL **conceptual** com es reconstruiria la taula completa (usa `UNION ALL` i `JOIN`).
6. Comprova que el teu disseny complix les tres regles de la fragmentació.
7. Replicaries algun fragment? Justifica la resposta.

#### Comprovació

- [ ] Cada fragment horitzontal té una condició, i entre totes cobrixen totes les províncies sense solapar-se.
- [ ] Els fragments verticals compartixen la clau primària `id_cliente`.
- [ ] La reconstrucció usa `UNION ALL` per als fragments horitzontals i `JOIN` per als verticals.
- [ ] El disseny té en compte que les dades sanitàries són una **categoria especial** segons el RGPD.

{{< solucion id="ud01-003" title="Solució parcial: reconstrucció" />}}

#### Ampliació

Investiga què és el **sharding** en MongoDB i quin paper té la *clau de fragmentació* (*shard key*). Quin camp triaries com a clau en FarmaRed? Què passaria si triares `dni`?

---

## Pràctica 1.5 · Auditoria de protecció de dades

{{< practica num="1.5" tipo="Reto" duracion="2 sessions" nivel="3" ra="RA1: i · RA6: h" sgbd="Documentació (RGPD, LOPDGDD, guies de l'AEPD)" entrega="Informe d'auditoria + defensa oral (5 min)" >}}

#### Objectiu

Identificar la legislació de protecció de dades que afecta una base de dades i traduir els seus principis en mesures tècniques concretes.

#### Context

L'institut va a substituir els seus fulls de càlcul per EduGest. La direcció et demana una **auditoria prèvia** que garantisca que el disseny complix el RGPD des del principi.

#### Enunciat

Usa l'[enunciat d'EduGest](/guia/proyecto-edugest#1-enunciat-entrevista-amb-la-direcció-destudis) i estes noves peticions del centre:

- El departament d'orientació vol registrar **diagnòstics de necessitats educatives especials**.
- Es vol guardar una **fotografia** de l'alumnat per al carnet.
- Una empresa d'autoescoles ha oferit diners pels correus i telèfons de l'alumnat major d'edat.
- Les dades dels antics alumnes es guarden «per a sempre».

Elabora un informe amb:

1. **Inventari de dades personals** d'EduGest: taula amb la dada, la persona interessada, si és una categoria especial i la seua finalitat.
2. Un **registre simplificat de l'activitat de tractament** (art. 30 RGPD): responsable, finalitats, categories de dades i interessats, destinataris, terminis de conservació i mesures de seguretat.
3. Per a cada nova petició, indica si és lícita, quines condicions exigiria i quins canvis implicaria en la base de dades.
4. Almenys **sis mesures tècniques** que aplicaràs en les unitats següents, indicant la unitat (per exemple: «vista sense dades de contacte per al professorat, UD05»).
5. El procediment que seguiria el centre davant d'una **bretxa de seguretat**.

#### Comprovació

{{% comprobacion %}}
- [ ] Es citen correctament el Reglament (UE) 2016/679 i la Llei Orgànica 3/2018.
- [ ] Els diagnòstics s'identifiquen com a **dades de salut** (categoria especial).
- [ ] Es rebutja la cessió a l'autoescola i s'explica per què.
- [ ] Es proposa un termini de conservació i què fer quan acabe (supressió o anonimització).
- [ ] Les mesures tècniques són concretes i verificables.

{{% details title="Pista: on trobar la informació" %}}
L'AEPD publica guies pràctiques per a centres educatius i models de registre d'activitats de tractament. Busca en [aepd.es](https://www.aepd.es/) la secció dedicada a educació. Recorda que la **base legal** del tractament de les dades acadèmiques en un centre públic és el compliment d'una missió d'interés públic, no el consentiment.
{{% /details %}}
{{% /comprobacion %}}

#### Ampliació

Dissenya com **anonimitzaries** les dades dels antics alumnes per a poder continuar fent estadístiques (per exemple, taxa d'aprovats per cicle i any) sense conservar dades personals.

---

## Pràctica 1.6 · De les dades a les decisions

{{< practica num="1.6" tipo="Autónoma" duracion="1 sessió" nivel="1" ra="RA1: j" sgbd="Full de càlcul (taules dinàmiques)" entrega="Full de càlcul + 3 conclusions" >}}

#### Objectiu

Reconéixer què és un procés d'intel·ligència de negocis i en què es diferencia un ús analític (OLAP) d'un de transaccional (OLTP).

#### Context

La direcció d'estudis vol saber si el percentatge d'aprovats en *Bases de dades* depén del torn o del cicle.

#### Enunciat

1. Crea en un full de càlcul una taula amb estes columnes i almenys 40 files inventades: `curso_academico`, `ciclo`, `turno`, `modulo`, `nota`.
2. Amb una **taula dinàmica**, calcula la nota mitjana i el nombre d'aprovats per cicle i torn.
3. Crea un gràfic que ho represente.
4. Escriu tres conclusions que podria usar la direcció d'estudis per a prendre decisions.
5. Respon: per què no convé llançar estes anàlisis directament sobre la base de dades amb la qual secretaria matricula cada dia? Relaciona-ho amb OLTP/OLAP.

#### Comprovació

{{% comprobacion %}}
- [ ] La taula dinàmica agrupa per dues dimensions (cicle i torn).
- [ ] Les conclusions es recolzen en les dades i no en opinions.
- [ ] La resposta del punt 5 menciona l'impacte en el rendiment i les dades històriques.

> [!TIP]
> Això que acabes de fer amb la taula dinàmica és una **consulta resum**. En la UD07 l'escriuràs en SQL amb `GROUP BY` i `AVG`.
{{% /comprobacion %}}

---

## Projecte EduGest · UD01: informe d'anàlisi

{{< practica num="EduGest-1" tipo="Proyecto" duracion="Treball transversal (1 setmana)" nivel="2" ra="RA1: c, d, f, i" sgbd="Document Markdown en el repositori" entrega="edugest/docs/01-analisis.md" >}}

#### Objectiu

Iniciar el projecte transversal amb una anàlisi del sistema actual i la justificació tècnica de la solució.

#### Enunciat

Llig l'[enunciat d'EduGest](/guia/proyecto-edugest) i redacta `01-analisis.md` amb estos apartats:

1. **Situació actual.** El centre usa un full de càlcul per cicle i un altre de faltes per cada professor. Descriu tres problemes concrets que provoca.
2. **Usuaris del sistema.** Identifica els perfils (secretaria, professorat, tutoria, direcció, alumnat, administrador de la base de dades) i què necessita fer cadascun. Relaciona'ls amb els perfils d'usuari d'un SGBD.
3. **Solució proposada.** Tipus de SGBD (model, ubicació, llicència) i justificació. Explica per què usarem Oracle per a la part relacional.
4. **Protecció de dades.** Resum de les conclusions de la pràctica 1.5 aplicades a EduGest.
5. **Glossari.** Deu termes de la unitat amb la teua pròpia definició.

#### Comprovació

{{% comprobacion %}}
- [ ] El document està en el repositori, en Markdown, i es llig bé en GitHub o GitLab.
- [ ] Cada perfil d'usuari té almenys dos operacions concretes.
- [ ] L'elecció del SGBD es recolza en característiques del cas, no en preferències.
{{% /comprobacion %}}
