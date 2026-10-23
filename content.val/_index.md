---
title: "Bases de Dades"
bookToc: true
---

# Bases de Dades · Mòdul 0484

Apunts del mòdul professional **0484. Bases de dades**, comú als cicles formatius de grau superior **Desenvolupament d'Aplicacions Multiplataforma (DAM)** i **Desenvolupament d'Aplicacions Web (DAW)**. Curs **2026/27**.

| Característica | Valor |
|---|---|
| **Referència curricular** | Reial decret 405/2023, de 29 de maig (actualitza els títols de DAM i DAW) |
| **Durada** | 105 hores (ensenyaments mínims) · 12 crèdits ECTS · 144 hores d'aula al centre (fins a la FE) |
| **Resultats d'aprenentatge** | 7 (RA1 a RA7) amb 57 criteris d'avaluació |
| **SGBD relacional** | Oracle AI Database 26ai Free (23.26) |
| **SGBD no relacional** | MongoDB Community Server 8.0 |
| **Projecte comú** | [EduGest: gestió d'un centre educatiu](/guia/proyecto-edugest) |

> [!NOTE]
> Estos apunts **no són un manual de SQL**. Estan organitzats perquè assolisques els resultats d'aprenentatge oficials del mòdul. Recorren el cicle de vida complet d'una base de dades:
> **anàlisi → model conceptual → model lògic → normalització → disseny físic → implementació → consultes → modificació → programació → optimització → NoSQL.**

## El cicle de treball amb una base de dades

```mermaid
flowchart LR
    A[Requisits] --> B[Model E/R<br/>UD02]
    B --> C[Model relacional<br/>UD03]
    C --> D[Normalització<br/>UD04]
    D --> E[DDL / DCL<br/>UD05]
    E --> F[Consultes<br/>UD06-UD07]
    F --> G[DML i transaccions<br/>UD08]
    G --> H[PL/SQL<br/>UD09]
    C -.comparació.-> I[NoSQL<br/>UD10]
    H -.-> I
```

## Guia didàctica del curs 2026/27

El mòdul s'imparteix amb una càrrega de **144 hores d'aula** (5 hores setmanals, una per dia lectiu) entre el **9 de setembre de 2026** i el **30 d'abril de 2027**. El **3 de maig** l'alumnat s'incorpora a la Formació en Empresa (FE) per ser de primer curs presencial, de manera que la docència del mòdul acaba a l'abril. Les hores es repartixen en tres avaluacions i s'han ajustat al calendari escolar i a les dates de proves comunicades pel centre.

> [!NOTE]
> Els ensenyaments mínims del RD 405/2023 fixen 105 hores per al mòdul. Les 144 hores són les d'**horari del centre** fins a l'inici de la FE; l'excés sobre el mínim es dedica a la pràctica guiada, al projecte EduGest i al reforç. Tots els criteris d'avaluació es cobrixen en les unitats; el repartiment d'hores és orientatiu i es pot ajustar a cada grup.

{{< calendario >}}

### Repartiment d'hores per avaluació

| Avaluació | Unitat | Hores | Del | Al | RA principal |
|---|---|:-:|---|---|---|
| **1a** (65 h) | UD01 · Sistemes d'emmagatzematge i SGBD | 12 | 09/09/2026 | 24/09/2026 | RA1 |
| | UD02 · Model Entitat/Relació | 19 | 25/09/2026 | 23/10/2026 | RA6 |
| | UD03 · Model relacional | 17 | 26/10/2026 | 17/11/2026 | RA6 · RA2 |
| | UD04 · Normalització | 14 | 18/11/2026 | 07/12/2026 | RA6 |
| | Prova i revisió de la 1a avaluació | 3 | 09/12/2026 | 11/12/2026 | |
| **2a** (43 h) | UD05 · Definició i control de dades | 17 | 14/12/2026 | 21/01/2027 | RA2 |
| | UD06 · Consultes sobre una taula | 23 | 22/01/2027 | 23/02/2027 | RA3 · RA5 |
| | Prova i revisió de la 2a avaluació | 3 | 24/02/2027 | 26/02/2027 | |
| **3a** (36 h) | UD07 · Consultes avançades | 16 | 01/03/2027 | 23/03/2027 | RA3 |
| | *Vacances de Pasqua* | | 25/03/2027 | 05/04/2027 | |
| | UD08 · DML, transaccions i concurrència | 6 | 24/03/2027 | 12/04/2027 | RA4 |
| | UD09 · Programació amb PL/SQL | 7 | 13/04/2027 | 21/04/2027 | RA5 |
| | UD10 · Bases de dades NoSQL | 4 | 22/04/2027 | 27/04/2027 | RA7 |
| | Prova i revisió de la 3a avaluació i final | 3 | 28/04/2027 | 30/04/2027 | |
| | *Formació en Empresa (FE)* | | 03/05/2027 | 18/06/2027 | |
| | **Total** | **144** | | | |

L'avaluació extraordinària està prevista per al **21 de juny de 2027**. Com que la FE ocupa de maig a juny, la prova de la 3a avaluació s'avança a l'última setmana d'abril (del 28 al 30).

### Criteris de la planificació

- **Teoria i pràctica en la mateixa unitat.** Cada unitat indica en la seua pàgina de teoria una *temporalització* amb el repartiment de sessions entre teoria (T) i pràctica (P). La suma d'hores de cada unitat coincidix amb la d'esta taula.
- **Pràctica guiada a l'aula, pràctica autònoma fora d'ella.** Les pràctiques guiades i la tasca del projecte EduGest es fan a classe. Les pràctiques autònomes, els reptes i les ampliacions són treball personal, i els dubtes es treballen en les sessions de pràctica.
- **Proves d'avaluació.** Cada avaluació reserva 3 hores a la prova i a la seua revisió, en la setmana indicada pel centre per als cicles de grau superior.
- **Un dia lectiu equival a una hora.** Els festius i els dies sense docència no compten. No hi ha setmana de reforç: els dies que es perguen per festes locals o activitats del centre es recuperen retallant les sessions de pràctica de l'última unitat impartida.

> [!WARNING]
> **La Formació en Empresa comença el 3 de maig.** L'alumnat de primer curs presencial se'n va a la FE el 3 de maig, per la qual cosa la 3a avaluació **es comprimix a l'abril** i les unitats finals (UD08 a UD10) queden amb 6, 7 i 4 hores d'aula. Això obliga que una part de les pràctiques d'eixes unitats es faça com a **treball autònom**; cada pàgina de teoria indica quines pràctiques es fan a l'aula i quines fora. Si el calendari canvia, l'arxiu `data/planificacion.json` i les taules de *temporalització* de cada unitat s'han d'ajustar alhora.

> [!CAUTION]
> **Calendari provisional.** Les dates procedixen del calendari escolar provisional 2026/27 i de les dates d'avaluació comunicades pel centre. Els festius locals i els tres dies no lectius que fixe el centre **no estan descomptats**: com que no queda marge abans de la FE, caldrà retallar sessions de pràctica d'UD08 a UD10. Quan es publique el calendari definitiu cal revisar l'arxiu `data/planificacion.json`; la taula i el calendari s'actualitzen sols i la compilació falla si les hores d'una unitat deixen de sumar.

## Unitats didàctiques

Cada unitat té dos pàgines: **teoria** (conceptes, exemples i autoavaluació) i **pràctiques** (pràctiques guiades, autònomes, reptes i la tasca del projecte EduGest).

<div class="bd-cards">
  <div class="bd-card"><span class="bd-card-ra">RA1</span><h3>UD01 · Sistemes d'emmagatzematge i SGBD</h3><p>Fitxers enfront de bases de dades, arquitectura i funcions d'un SGBD, tipus de bases de dades, distribució, Big Data i protecció de dades.</p><div class="bd-card-links"><a href="ud01-introduccion/ud01-teoria/">Teoria</a> · <a href="ud01-introduccion/ud01-practicas/">Pràctiques</a></div></div>
  <div class="bd-card"><span class="bd-card-ra">RA6</span><h3>UD02 · Model Entitat/Relació</h3><p>Anàlisi de requisits, entitats, atributs, relacions, cardinalitats, entitats febles i extensions EER.</p><div class="bd-card-links"><a href="ud02-modelo-er/ud02-teoria/">Teoria</a> · <a href="ud02-modelo-er/ud02-practicas/">Pràctiques</a></div></div>
  <div class="bd-card"><span class="bd-card-ra">RA6 · RA2</span><h3>UD03 · Model relacional</h3><p>Relacions, claus, restriccions, integritat i transformació del model E/R al model relacional.</p><div class="bd-card-links"><a href="ud03-modelo-relacional/ud03-teoria/">Teoria</a> · <a href="ud03-modelo-relacional/ud03-practicas/">Pràctiques</a></div></div>
  <div class="bd-card"><span class="bd-card-ra">RA6</span><h3>UD04 · Normalització</h3><p>Anomalies, dependències funcionals, 1FN, 2FN, 3FN i FNBC. Restriccions que el disseny lògic no pot expressar.</p><div class="bd-card-links"><a href="ud04-normalizacion/ud04-teoria/">Teoria</a> · <a href="ud04-normalizacion/ud04-practicas/">Pràctiques</a></div></div>
  <div class="bd-card"><span class="bd-card-ra">RA2</span><h3>UD05 · Definició i control de dades</h3><p>DDL en Oracle: taules, tipus, restriccions, índexs, vistes i seqüències. DCL: usuaris, rols i privilegis.</p><div class="bd-card-links"><a href="ud05-ddl-dcl/ud05-teoria/">Teoria</a> · <a href="ud05-ddl-dcl/ud05-practicas/">Pràctiques</a></div></div>
  <div class="bd-card"><span class="bd-card-ra">RA3</span><h3>UD06 · Consultes sobre una taula</h3><p>SELECT, projecció, selecció, ordenació, operadors, valors nuls i funcions de fila.</p><div class="bd-card-links"><a href="ud06-consultas-basicas/ud06-teoria/">Teoria</a> · <a href="ud06-consultas-basicas/ud06-practicas/">Pràctiques</a></div></div>
  <div class="bd-card"><span class="bd-card-ra">RA3</span><h3>UD07 · Consultes avançades</h3><p>Agrupament, composicions internes i externes, subconsultes, operadors de conjunts i optimització.</p><div class="bd-card-links"><a href="ud07-consultas-avanzadas/ud07-teoria/">Teoria</a> · <a href="ud07-consultas-avanzadas/ud07-practicas/">Pràctiques</a></div></div>
  <div class="bd-card"><span class="bd-card-ra">RA4</span><h3>UD08 · Manipulació de dades i transaccions</h3><p>INSERT, UPDATE, DELETE, MERGE, transaccions, ACID, concurrència i bloquejos.</p><div class="bd-card-links"><a href="ud08-dml-transacciones/ud08-teoria/">Teoria</a> · <a href="ud08-dml-transacciones/ud08-practicas/">Pràctiques</a></div></div>
  <div class="bd-card"><span class="bd-card-ra">RA5</span><h3>UD09 · Programació amb PL/SQL</h3><p>Blocs, variables, control de flux, procediments, funcions, cursors, excepcions, triggers i tasques programades.</p><div class="bd-card-links"><a href="ud09-plsql/ud09-teoria/">Teoria</a> · <a href="ud09-plsql/ud09-practicas/">Pràctiques</a></div></div>
  <div class="bd-card"><span class="bd-card-ra">RA7</span><h3>UD10 · Bases de dades NoSQL</h3><p>Tipus de bases de dades no relacionals, modelatge documental i operacions CRUD i d'agregació amb MongoDB.</p><div class="bd-card-links"><a href="ud10-nosql/ud10-teoria/">Teoria</a> · <a href="ud10-nosql/ud10-practicas/">Pràctiques</a></div></div>
</div>

## Relació entre unitats i resultats d'aprenentatge

| Unitat | RA1 | RA2 | RA3 | RA4 | RA5 | RA6 | RA7 |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| UD01 Sistemes d'emmagatzematge i SGBD | ● | ○ | | | | | ○ |
| UD02 Model Entitat/Relació | | | | | | ● | |
| UD03 Model relacional | | ○ | | | | ● | |
| UD04 Normalització | | | | | | ● | |
| UD05 Definició i control de dades | | ● | | | | ○ | |
| UD06 Consultes sobre una taula | | | ● | | ○ | | |
| UD07 Consultes avançades | | ○ | ● | | | | |
| UD08 Manipulació i transaccions | | | | ● | | ○ | |
| UD09 Programació PL/SQL | | | | ○ | ● | ○ | |
| UD10 Bases de dades NoSQL | ○ | | | | | | ● |

● contribució principal · ○ contribució secundària. El detall per criteri d'avaluació està en [Resultats d'aprenentatge i criteris d'avaluació](/guia/ra-ce).

## Com llegir estos apunts

Els apunts usen quadres de colors per a destacar informació:

> [!TIP]
> **Consell.** Una forma més còmoda o professional de fer una cosa.

> [!WARNING]
> **Atenció.** Un error habitual o alguna cosa que pot donar problemes.

> [!IMPORTANT]
> **Clau.** Un concepte imprescindible per al resultat d'aprenentatge.

> [!CAUTION]
> **Perill.** Una operació que pot destruir o exposar dades.

{{% details title="Pista (desplega'm)" %}}
Les pistes i les **solucions** dels exercicis apareixen plegades. Intenta resoldre l'exercici abans d'obrir-les.
{{% /details %}}

Els fragments de codi indiquen sempre el gestor al qual corresponen, per exemple {{< sgbd "Oracle 26ai" >}}, {{< sgbd "MongoDB 8.0" >}} o {{< sgbd "SQL estàndard" >}}.

Consulta també la [guia del mòdul](/guia): el projecte EduGest, la instal·lació de l'entorn i les convencions de les pràctiques.

## Fonts

- [Reial decret 405/2023, de 29 de maig](https://www.boe.es/buscar/act.php?id=BOE-A-2023-13221). Text consolidat al BOE.
- [Documentació d'Oracle AI Database 26ai](https://docs.oracle.com/en/database/oracle/oracle-database/26/).
- [Manual de MongoDB](https://www.mongodb.com/docs/manual/).
