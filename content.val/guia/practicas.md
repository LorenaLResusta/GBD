---
title: "Com són les pràctiques"
weight: 4
---

# Com són les pràctiques

Cada unitat té una pàgina de **pràctiques**. Les pràctiques són la part principal del mòdul: els criteris d'avaluació de RA2 a RA7 es demostren **fent**, no memoritzant.

## 1. Tipus de pràctica

| Tipus | Què és | Com es treballa |
|---|---|---|
| **Guiada** | Es presenta el procediment pas a pas. El seu objectiu és aprendre la tècnica. | A classe. Es comprova al final de la sessió amb la llista de comprovació. |
| **Autònoma** | Es planteja un problema semblant sense el procediment. El seu objectiu és aplicar la tècnica. | Individual. Es lliura i s'avalua. |
| **Repte** | Un problema obert o amb una dificultat extra. Exigix analitzar i decidir. | Opcional o per a pujar nota. Es defén oralment. |
| **Projecte** | La tasca d'EduGest de la unitat. | Individual o per parelles. Forma part del projecte final. |

La dificultat s'indica amb tres punts: ●○○ bàsic, ●●○ intermedi i ●●● avançat.

## 2. Estructura d'una pràctica

Totes les pràctiques seguixen el mateix esquema. Així saps què s'espera en cada apartat:

{{< practica num="X.Y" tipo="Guiada" duracion="Tiempo orientativo" nivel="2" ra="RAx: criterios" sgbd="Software y versión" entrega="Qué hay que entregar" >}}

1. **Objectiu.** Quina competència o resultat es pretén desenvolupar.
2. **Context.** La situació professional que es planteja.
3. **Requisits.** Programari, versions i coneixements previs.
4. **Enunciat.** El problema que has de resoldre.
5. **Desenvolupament.** El procediment guiat (només en pràctiques guiades).
6. **Comprovació.** Proves que permeten verificar que el resultat és correcte.
7. **Errors habituals.** Problemes freqüents i com diagnosticar-los.
8. **Ampliació.** Una modificació que t'obliga a aplicar el que has aprés pel teu compte.

> [!TIP]
> Llig la **Comprovació** abans de començar. Et diu exactament quin resultat has d'obtindre i t'estalvia temps.

## 3. Organització del repositori

Crea un repositori Git privat per al mòdul amb esta estructura:

```text
bbdd-<tu-usuario>/
├── README.md                 # nom, grup i estat de cada pràctica
├── ud01/
│   └── p1.1-analisis.md
├── ud02/
│   ├── p2.1-biblioteca.drawio
│   └── p2.1-biblioteca.png
├── ud05/
│   ├── p5.1-tienda.sql
│   └── evidencias/p5.1-salida.txt
├── ...
└── edugest/                  # el proyecto transversal
    ├── 01_esquema.sql
    ├── 02_datos.sql
    ├── 03_seguridad.sql
    └── docs/diseno.md
```

## 4. Normes per als scripts SQL

Un script lliurat ha de poder **executar-se de principi a fi** en una base de dades neta sense errors inesperats. Per això:

```sql
-- =============================================================
-- Pràctica 5.2 · Botiga en línia · Script de creació
-- Autor/a: Nom Cognoms (1DAM)
-- SGBD: Oracle AI Database 26ai Free 23.26
-- Data: 2026-11-10
-- =============================================================

-- 1. Neteja per a poder rellançar l'script
DROP TABLE linea_pedido CASCADE CONSTRAINTS PURGE;

-- 2. Creació de taules (cada restricció amb nom)
CREATE TABLE cliente (
    id_cliente NUMBER(6) CONSTRAINT pk_cliente PRIMARY KEY
    -- ...
);

-- 3. Comprovacions
SELECT constraint_name, constraint_type FROM user_constraints WHERE table_name = 'CLIENTE';
```

- Una sentència per bloc, acabada en `;`.
- Comentaris que expliquen el **perquè**, no només el què.
- Restriccions amb **nom** (`pk_`, `fk_`, `uq_`, `ck_`, `nn_`).
- Identificadors en minúscules i amb guió baix (`fecha_nacimiento`), sense accents ni espais.
- Les evidències d'execució es guarden amb `SPOOL` o amb captures a la carpeta `evidencias/`.

## 5. Autoavaluació de les pràctiques

Les pràctiques autònomes i les de projecte s'autoavaluen amb esta rúbrica comuna. Cada pràctica indica quins criteris d'avaluació (CE) treballa.

| Aspecte | Excel·lent (4) | Adequat (3) | Millorable (2) | Insuficient (1) |
|---|---|---|---|---|
| **Resultat** | Funciona i supera totes les comprovacions | Errors menors que no afecten el resultat | Funciona parcialment | No funciona o no s'executa |
| **Disseny i decisions** | Justifica cada decisió i valora alternatives | Decisions correctes amb poca justificació | Decisions discutibles sense justificar | Decisions incorrectes |
| **Qualitat del codi o del diagrama** | Llegible, comentat, amb noms coherents | Llegible amb pocs comentaris | Difícil de seguir | Desordenat |
| **Comprovació i evidències** | Proves pròpies a més de les demanades | Inclou les comprovacions demanades | Comprovacions incompletes | Sense evidències |

> [!WARNING]
> **Integritat acadèmica.** Pots consultar documentació, fòrums i assistents d'IA, però has d'**entendre i poder defendre** tot el que lliures. En la defensa oral se't pot demanar que modifiques la teua solució en directe. Indica en el `README.md` les fonts i eines que hages usat.
