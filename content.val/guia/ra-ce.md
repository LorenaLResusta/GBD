---
title: "Resultats d'aprenentatge i criteris d'avaluació"
weight: 1
---

# Resultats d'aprenentatge i criteris d'avaluació

El mòdul **0372. Gestió de bases de dades** (1r d'Administració de Sistemes Informàtics en Xarxa, ASIX) es regix pel **Reial decret 1629/2009, de 30 d'octubre**, que n'establix el títol i les ensenyances mínimes. El mòdul té **6 resultats d'aprenentatge (RA)** amb **47 criteris d'avaluació (CE)**.

> [!IMPORTANT]
> Un **resultat d'aprenentatge** descriu el que sabràs fer en acabar el mòdul. Un **criteri d'avaluació** és una evidència concreta que demostra que ho has aconseguit. Cada unitat, pràctica i exercici d'estos apunts indica quin CE treballa.

## Mapa de contribució

```mermaid
flowchart TB
    RA1["RA1 · Elements de les BD i SGBD"] --- U1[UD01] & U6[UD06]
    RA2["RA2 · Disseny lògic normalitzat"] --- U2[UD02] & U3[UD03] & U5[UD05]
    RA3["RA3 · Disseny físic (DDL)"] --- U1[UD01] & U2[UD02] & U3[UD03] & U4[UD04]
    RA4["RA4 · Consultes"] --- U4[UD04]
    RA5["RA5 · Modificació i transaccions"] --- U5[UD05]
    RA6["RA6 · Seguretat: còpies, importació i exportació"] --- U5[UD05] & U6[UD06]
```

> [!NOTE]
> L'ordre de les unitats no coincidix amb el número dels RA. Primer es **dissenya** (RA2), després s'**implementa** (RA3) i es consulta i modifica (RA4 i RA5). El currículum descriu *què* cal aconseguir, no l'ordre en què s'ensenya. Les unitats de PL/SQL i de bases de dades NoSQL amplien el mòdul més enllà del mínim oficial.

## Criteris d'avaluació per resultat d'aprenentatge

Text literal de les ensenyances mínimes. L'última columna indica en quines unitats es treballa cada criteri.

## RA1. Reconeix els elements de les bases de dades analitzant-ne les funcions i valorant la utilitat dels sistemes gestors.

| CE | Criteri d'avaluació | Unitats |
|---|---|---|
| RA1.a | S'han analitzat els diferents sistemes lògics d'emmagatzematge i les seues funcions. | [UD01](/ud01-introduccion) |
| RA1.b | S'han identificat els diferents tipus de bases de dades segons el model de dades utilitzat. | [UD01](/ud01-introduccion), [UD06](/ud06-aseguramiento) |
| RA1.c | S'han identificat els diferents tipus de bases de dades en funció de la ubicació de la informació. | [UD01](/ud01-introduccion) |
| RA1.d | S'ha reconegut la utilitat d'un sistema gestor de bases de dades. | [UD01](/ud01-introduccion) |
| RA1.e | S'ha descrit la funció de cada un dels elements d'un sistema gestor de bases de dades. | [UD01](/ud01-introduccion) |
| RA1.f | S'han classificat els sistemes gestors de bases de dades. | [UD01](/ud01-introduccion) |

## RA2. Dissenya models lògics normalitzats interpretant diagrames entitat/relació.

| CE | Criteri d'avaluació | Unitats |
|---|---|---|
| RA2.a | S'ha identificat el significat de la simbologia pròpia dels diagrames entitat/relació. | [UD02](/ud02-diseno-logico) |
| RA2.b | S'han utilitzat ferramentes gràfiques per a representar el disseny lògic. | [UD02](/ud02-diseno-logico), [UD03](/ud03-ddl-dcl) |
| RA2.c | S'han identificat les taules del disseny lògic. | [UD02](/ud02-diseno-logico) |
| RA2.d | S'han identificat els camps que formen part de les taules del disseny lògic. | [UD02](/ud02-diseno-logico) |
| RA2.e | S'han identificat les relacions entre les taules del disseny lògic. | [UD02](/ud02-diseno-logico) |
| RA2.f | S'han definit els camps clau. | [UD02](/ud02-diseno-logico), [UD03](/ud03-ddl-dcl) |
| RA2.g | S'han aplicat les regles d'integritat. | [UD02](/ud02-diseno-logico), [UD03](/ud03-ddl-dcl), [UD05](/ud05-dml-plsql) |
| RA2.h | S'han aplicat les regles de normalització fins a un nivell adequat. | [UD02](/ud02-diseno-logico) |
| RA2.i | S'han identificat i documentat les restriccions que no poden plasmar-se en el disseny lògic. | [UD02](/ud02-diseno-logico), [UD05](/ud05-dml-plsql) |

## RA3. Realitza el disseny físic de bases de dades utilitzant assistents, ferramentes gràfiques i el llenguatge de definició de dades.

| CE | Criteri d'avaluació | Unitats |
|---|---|---|
| RA3.a | S'han definit les estructures físiques d'emmagatzematge. | [UD01](/ud01-introduccion), [UD02](/ud02-diseno-logico), [UD03](/ud03-ddl-dcl) |
| RA3.b | S'han creat taules. | [UD03](/ud03-ddl-dcl) |
| RA3.c | S'han seleccionat els tipus de dades adequats. | [UD03](/ud03-ddl-dcl) |
| RA3.d | S'han definit els camps clau en les taules. | [UD02](/ud02-diseno-logico), [UD03](/ud03-ddl-dcl) |
| RA3.e | S'han implantat totes les restriccions reflectides en el disseny lògic. | [UD02](/ud02-diseno-logico), [UD03](/ud03-ddl-dcl) |
| RA3.f | S'ha verificat mitjançant un conjunt de dades de prova que la implementació s'ajusta al model. | [UD03](/ud03-ddl-dcl) |
| RA3.g | S'han utilitzat assistents i ferramentes gràfiques. | [UD03](/ud03-ddl-dcl) |
| RA3.h | S'ha utilitzat el llenguatge de definició de dades. | [UD03](/ud03-ddl-dcl), [UD04](/ud04-consultas) |
| RA3.i | S'ha definit i documentat el diccionari de dades. | [UD03](/ud03-ddl-dcl) |

## RA4. Consulta la informació emmagatzemada manejant assistents, ferramentes gràfiques i el llenguatge de manipulació de dades.

| CE | Criteri d'avaluació | Unitats |
|---|---|---|
| RA4.a | S'han identificat les ferramentes i sentències per a realitzar consultes. | [UD04](/ud04-consultas) |
| RA4.b | S'han realitzat consultes simples sobre una taula. | [UD04](/ud04-consultas) |
| RA4.c | S'han realitzat consultes que generen valors de resum. | [UD04](/ud04-consultas) |
| RA4.d | S'han realitzat consultes sobre el contingut de diverses taules mitjançant composicions internes. | [UD04](/ud04-consultas) |
| RA4.e | S'han realitzat consultes sobre el contingut de diverses taules mitjançant composicions externes. | [UD04](/ud04-consultas) |
| RA4.f | S'han realitzat consultes amb subconsultes. | [UD04](/ud04-consultas) |
| RA4.g | S'han valorat els avantatges i inconvenients de les diferents opcions vàlides per a dur a terme una consulta determinada. | [UD04](/ud04-consultas) |

## RA5. Modifica la informació emmagatzemada utilitzant assistents, ferramentes gràfiques i el llenguatge de manipulació de dades.

| CE | Criteri d'avaluació | Unitats |
|---|---|---|
| RA5.a | S'han identificat les ferramentes i sentències per a modificar el contingut de la base de dades. | [UD05](/ud05-dml-plsql) |
| RA5.b | S'han inserit, esborrat i actualitzat dades en les taules. | [UD05](/ud05-dml-plsql) |
| RA5.c | S'ha inclòs en una taula la informació resultant de l'execució d'una consulta. | [UD05](/ud05-dml-plsql) |
| RA5.d | S'han adoptat mesures per a mantindre la integritat i consistència de la informació. | [UD05](/ud05-dml-plsql) |
| RA5.e | S'han dissenyat guions de sentències per a dur a terme tasques complexes. | [UD05](/ud05-dml-plsql) |
| RA5.f | S'ha reconegut el funcionament de les transaccions. | [UD05](/ud05-dml-plsql) |
| RA5.g | S'han anul·lat parcial o totalment els canvis produïts per una transacció. | [UD05](/ud05-dml-plsql) |
| RA5.h | S'han identificat els efectes de les diferents polítiques de bloqueig de registres. | [UD05](/ud05-dml-plsql) |

## RA6. Executa tasques d'assegurament de la informació, analitzant-les i aplicant mecanismes de salvaguarda i transferència.

| CE | Criteri d'avaluació | Unitats |
|---|---|---|
| RA6.a | S'han identificat ferramentes gràfiques i en línia d'ordres per a l'administració de còpies de seguretat. | [UD06](/ud06-aseguramiento) |
| RA6.b | S'han realitzat còpies de seguretat. | [UD06](/ud06-aseguramiento) |
| RA6.c | S'han restaurat còpies de seguretat. | [UD06](/ud06-aseguramiento) |
| RA6.d | S'han identificat les ferramentes per a importar i exportar dades. | [UD06](/ud06-aseguramiento) |
| RA6.e | S'han exportat dades a diversos formats. | [UD06](/ud06-aseguramiento) |
| RA6.f | S'han importat dades amb diferents formats. | [UD06](/ud06-aseguramiento) |
| RA6.g | S'ha interpretat correctament la informació subministrada pels missatges d'error i els fitxers de registre. | [UD05](/ud05-dml-plsql), [UD06](/ud06-aseguramiento) |
| RA6.h | S'ha transferit informació entre sistemes gestors. | [UD06](/ud06-aseguramiento) |

## Evidències d'aprenentatge

Per a cada criteri d'avaluació es recullen evidències de diferents tipus:

| Tipus d'evidència | Exemples | CE en els quals s'usa sobretot |
|---|---|---|
| Qüestionaris i preguntes de raonament | Autoavaluacions de cada unitat, preguntes de justificació | RA1 |
| Diagrames i documents de disseny | Diagrama E/R, esquema relacional, informe de normalització | RA2 |
| Scripts SQL executables | Scripts DDL, DCL, de consulta i de modificació | RA3, RA4, RA5 |
| Plans d'execució i sessions concurrents | Captures i registres d'execució | RA4.g, RA5.h |
| Còpies, exportacions i importacions | Scripts de còpia i restauració, fitxers exportats, registres d'error | RA6 |
| Lliuraments del projecte EduGest | Una tasca de projecte al final de cada unitat | Tots |

## Font

- [Reial decret 1629/2009, de 30 d'octubre, pel qual s'establix el títol de Tècnic Superior en Administració de Sistemes Informàtics en Xarxa (BOE-A-2009-17588)](https://www.boe.es/buscar/act.php?id=BOE-A-2009-17588).
