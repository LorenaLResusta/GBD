---
title: "Resultats d'aprenentatge i criteris d'avaluació"
weight: 1
---

# Resultats d'aprenentatge i criteris d'avaluació

El mòdul **0372. Gestió de bases de dades** (1r d'Administració de Sistemes Informàtics en Xarxa, ASIR) es regix pel **Reial decret 1629/2009, de 30 d'octubre**, que establix el títol i els seus ensenyaments mínims. El mòdul té **6 resultats d'aprenentatge (RA)** amb **47 criteris d'avaluació (CE)**. Estos apunts s'impartixen en **160 hores d'aula** (5 per setmana): el RD fixa 105 hores com a mínim, i el currículum de la Comunitat Valenciana amplia el mòdul fins a les 160.

> [!IMPORTANT]
> Un **resultat d'aprenentatge** descriu el que sabràs fer en acabar el mòdul. Un **criteri d'avaluació** és una evidència concreta que demostra que ho has aconseguit. Cada tema, pràctica i exercici d'estos apunts indica quins CE treballa.

## Hores per resultat d'aprenentatge

El mòdul s'organitza en **6 temes, un per cada RA** (el tema 1 desenvolupa el RA1, el tema 2 el RA2, i així fins al tema 6 i el RA6). Tot el contingut dels temes es correspon amb els criteris d'avaluació del RD 1629/2009.

| RA | Resultat d'aprenentatge | Tema | Hores |
|---|---|---|:-:|
| **RA1** | Reconeix els elements de les bases de dades analitzant-ne les funcions i valorant la utilitat dels sistemes gestors. | [Tema 1](/tema1-introduccion) | 8 |
| **RA2** | Dissenya models lògics normalitzats interpretant diagrames entitat/relació. | [Tema 2](/tema2-diseno-logico) | 32 |
| **RA3** | Realitza el disseny físic de bases de dades utilitzant assistents, ferramentes gràfiques i el llenguatge de definició de dades. | [Tema 3](/tema3-diseno-fisico) | 24 |
| **RA4** | Consulta la informació emmagatzemada manejant assistents, ferramentes gràfiques i el llenguatge de manipulació de dades. | [Tema 4](/tema4-consultas) | 26 |
| **RA5** | Modifica la informació emmagatzemada utilitzant assistents, ferramentes gràfiques i el llenguatge de manipulació de dades. | [Tema 5](/tema5-modificacion) | 52 |
| **RA6** | Executa tasques d'assegurament de la informació, analitzant-les i aplicant mecanismes de salvaguarda i transferència. | [Tema 6](/tema6-aseguramiento) | 9 |
| | *Proves d'avaluació (3 × 3 h)* | | 9 |
| | **Total** | | **160** |

```mermaid
flowchart LR
    T1["Tema 1 · RA1<br/>Elements de les BD i SGBD"] --> T2
    T2["Tema 2 · RA2<br/>Disseny lògic normalitzat"] --> T3
    T3["Tema 3 · RA3<br/>Disseny físic (DDL)"] --> T4
    T4["Tema 4 · RA4<br/>Consultes"] --> T5
    T5["Tema 5 · RA5<br/>Modificació, transaccions i guions"] --> T6
    T6["Tema 6 · RA6<br/>Seguretat: còpies, importació i exportació"]
```

## Criteris d'avaluació per resultat d'aprenentatge

Text literal de les ensenyances mínimes. L'última columna indica en quin tema es treballa cada criteri.

## RA1. Reconeix els elements de les bases de dades analitzant-ne les funcions i valorant la utilitat dels sistemes gestors.

| CE | Criteri d'avaluació | Tema |
|---|---|---|
| RA1.a | S'han analitzat els diferents sistemes lògics d'emmagatzematge i les seues funcions. | [Tema 1](/tema1-introduccion) |
| RA1.b | S'han identificat els diferents tipus de bases de dades segons el model de dades utilitzat. | [Tema 1](/tema1-introduccion) |
| RA1.c | S'han identificat els diferents tipus de bases de dades en funció de la ubicació de la informació. | [Tema 1](/tema1-introduccion) |
| RA1.d | S'ha reconegut la utilitat d'un sistema gestor de bases de dades. | [Tema 1](/tema1-introduccion) |
| RA1.e | S'ha descrit la funció de cada un dels elements d'un sistema gestor de bases de dades. | [Tema 1](/tema1-introduccion) |
| RA1.f | S'han classificat els sistemes gestors de bases de dades. | [Tema 1](/tema1-introduccion) |

## RA2. Dissenya models lògics normalitzats interpretant diagrames entitat/relació.

| CE | Criteri d'avaluació | Tema |
|---|---|---|
| RA2.a | S'ha identificat el significat de la simbologia pròpia dels diagrames entitat/relació. | [Tema 2](/tema2-diseno-logico) |
| RA2.b | S'han utilitzat ferramentes gràfiques per a representar el disseny lògic. | [Tema 2](/tema2-diseno-logico), [Tema 3](/tema3-diseno-fisico) |
| RA2.c | S'han identificat les taules del disseny lògic. | [Tema 2](/tema2-diseno-logico) |
| RA2.d | S'han identificat els camps que formen part de les taules del disseny lògic. | [Tema 2](/tema2-diseno-logico) |
| RA2.e | S'han identificat les relacions entre les taules del disseny lògic. | [Tema 2](/tema2-diseno-logico) |
| RA2.f | S'han definit els camps clau. | [Tema 2](/tema2-diseno-logico) |
| RA2.g | S'han aplicat les regles d'integritat. | [Tema 2](/tema2-diseno-logico), [Tema 3](/tema3-diseno-fisico), [Tema 5](/tema5-modificacion) |
| RA2.h | S'han aplicat les regles de normalització fins a un nivell adequat. | [Tema 2](/tema2-diseno-logico) |
| RA2.i | S'han identificat i documentat les restriccions que no poden plasmar-se en el disseny lògic. | [Tema 2](/tema2-diseno-logico) |

## RA3. Realitza el disseny físic de bases de dades utilitzant assistents, ferramentes gràfiques i el llenguatge de definició de dades.

| CE | Criteri d'avaluació | Tema |
|---|---|---|
| RA3.a | S'han definit les estructures físiques d'emmagatzematge. | [Tema 3](/tema3-diseno-fisico) |
| RA3.b | S'han creat taules. | [Tema 3](/tema3-diseno-fisico) |
| RA3.c | S'han seleccionat els tipus de dades adequats. | [Tema 3](/tema3-diseno-fisico) |
| RA3.d | S'han definit els camps clau en les taules. | [Tema 3](/tema3-diseno-fisico) |
| RA3.e | S'han implantat totes les restriccions reflectides en el disseny lògic. | [Tema 2](/tema2-diseno-logico), [Tema 3](/tema3-diseno-fisico) |
| RA3.f | S'ha verificat mitjançant un conjunt de dades de prova que la implementació s'ajusta al model. | [Tema 3](/tema3-diseno-fisico) |
| RA3.g | S'han utilitzat assistents i ferramentes gràfiques. | [Tema 3](/tema3-diseno-fisico) |
| RA3.h | S'ha utilitzat el llenguatge de definició de dades. | [Tema 3](/tema3-diseno-fisico) |
| RA3.i | S'ha definit i documentat el diccionari de dades. | [Tema 3](/tema3-diseno-fisico) |

## RA4. Consulta la informació emmagatzemada manejant assistents, ferramentes gràfiques i el llenguatge de manipulació de dades.

| CE | Criteri d'avaluació | Tema |
|---|---|---|
| RA4.a | S'han identificat les ferramentes i sentències per a realitzar consultes. | [Tema 4](/tema4-consultas) |
| RA4.b | S'han realitzat consultes simples sobre una taula. | [Tema 4](/tema4-consultas) |
| RA4.c | S'han realitzat consultes que generen valors de resum. | [Tema 4](/tema4-consultas) |
| RA4.d | S'han realitzat consultes sobre el contingut de diverses taules mitjançant composicions internes. | [Tema 4](/tema4-consultas) |
| RA4.e | S'han realitzat consultes sobre el contingut de diverses taules mitjançant composicions externes. | [Tema 4](/tema4-consultas) |
| RA4.f | S'han realitzat consultes amb subconsultes. | [Tema 4](/tema4-consultas) |
| RA4.g | S'han valorat els avantatges i inconvenients de les diferents opcions vàlides per a dur a terme una consulta determinada. | [Tema 4](/tema4-consultas) |

## RA5. Modifica la informació emmagatzemada utilitzant assistents, ferramentes gràfiques i el llenguatge de manipulació de dades.

| CE | Criteri d'avaluació | Tema |
|---|---|---|
| RA5.a | S'han identificat les ferramentes i sentències per a modificar el contingut de la base de dades. | [Tema 5](/tema5-modificacion) |
| RA5.b | S'han inserit, esborrat i actualitzat dades en les taules. | [Tema 5](/tema5-modificacion) |
| RA5.c | S'ha inclòs en una taula la informació resultant de l'execució d'una consulta. | [Tema 5](/tema5-modificacion) |
| RA5.d | S'han adoptat mesures per a mantindre la integritat i consistència de la informació. | [Tema 5](/tema5-modificacion) |
| RA5.e | S'han dissenyat guions de sentències per a dur a terme tasques complexes. | [Tema 5](/tema5-modificacion) |
| RA5.f | S'ha reconegut el funcionament de les transaccions. | [Tema 5](/tema5-modificacion) |
| RA5.g | S'han anul·lat parcial o totalment els canvis produïts per una transacció. | [Tema 5](/tema5-modificacion) |
| RA5.h | S'han identificat els efectes de les diferents polítiques de bloqueig de registres. | [Tema 5](/tema5-modificacion) |

## RA6. Executa tasques d'assegurament de la informació, analitzant-les i aplicant mecanismes de salvaguarda i transferència.

| CE | Criteri d'avaluació | Tema |
|---|---|---|
| RA6.a | S'han identificat ferramentes gràfiques i en línia d'ordres per a l'administració de còpies de seguretat. | [Tema 6](/tema6-aseguramiento) |
| RA6.b | S'han realitzat còpies de seguretat. | [Tema 6](/tema6-aseguramiento) |
| RA6.c | S'han restaurat còpies de seguretat. | [Tema 6](/tema6-aseguramiento) |
| RA6.d | S'han identificat les ferramentes per a importar i exportar dades. | [Tema 6](/tema6-aseguramiento) |
| RA6.e | S'han exportat dades a diversos formats. | [Tema 6](/tema6-aseguramiento) |
| RA6.f | S'han importat dades amb diferents formats. | [Tema 6](/tema6-aseguramiento) |
| RA6.g | S'ha interpretat correctament la informació subministrada pels missatges d'error i els fitxers de registre. | [Tema 6](/tema6-aseguramiento) |
| RA6.h | S'ha transferit informació entre sistemes gestors. | [Tema 6](/tema6-aseguramiento) |

## Evidències d'aprenentatge

Per a cada criteri d'avaluació es recullen evidències de diferents tipus:

| Tipus d'evidència | Exemples | CE en els quals s'usa sobretot |
|---|---|---|
| Qüestionaris i preguntes de raonament | Autoavaluacions de cada tema, preguntes de justificació | RA1 |
| Diagrames i documents de disseny | Diagrama E/R, esquema relacional, informe de normalització | RA2 |
| Scripts SQL executables | Scripts DDL, de consulta i de modificació | RA3, RA4, RA5 |
| Guions PL/SQL amb proves | Blocs amb variables, control de flux i excepcions amb la seua bateria de proves | RA5.e |
| Captures i registres d'execució | Plans d'execució, sessions concurrents, fitxers `.log` de Data Pump i SQL*Loader | RA4.g, RA5.h, RA6.g |
| Lliuraments del projecte EduGest | Una tasca de projecte al final de cada tema | Tots |

## Font

- [Reial decret 1629/2009, de 30 d'octubre, pel qual s'establix el títol de Tècnic Superior en Administració de Sistemes Informàtics en Xarxa](https://www.boe.es/eli/es/rd/2009/10/30/1629).
