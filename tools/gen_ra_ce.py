#!/usr/bin/env python3
"""Genera content.*/guia/ra-ce.md a partir de data/curriculo*.yaml y de los shortcodes `ra` de las unidades."""
import glob, os, re, yaml
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def cobertura(lang, cur):
    cov = {}
    for p in sorted(glob.glob(f'{R}/content.{lang}/ud*/t*-*.md')):
        carpeta = p.split('/')[-2]; nn = re.search(r't(\d+)-', os.path.basename(p)).group(1); u = 'T' + nn
        carpeta = f'{carpeta}/t{nn}-teoria'
        s = open(p, encoding='utf-8').read()
        for ln in s.split('\n'):
            if ln.startswith('{{< ra '):
                for a in re.findall(r'"([^"]*)"', ln):
                    ra, _, ls = a.partition(':')
                    for l in (ls.split(',') if ls else list(cur[ra]['ce'])): cov.setdefault((ra, l), {})[u] = carpeta
        for v in re.findall(r'ra="([^"]*)"', s):
            for ra, ls in re.findall(r'(RA\d)\s*:\s*([a-i](?:\s*[,-]\s*[a-i])*)', v):
                letras = []
                for part in re.split(r'\s*,\s*', ls):
                    m = re.fullmatch(r'([a-i])\s*-\s*([a-i])', part)
                    letras += [chr(x) for x in range(ord(m.group(1)), ord(m.group(2)) + 1)] if m else [part]
                for l in letras:
                    if l in cur[ra]['ce']: cov.setdefault((ra, l), {})[u] = carpeta
    return cov
T = {
 'es': dict(
  head='''---
title: "Resultados de aprendizaje y criterios de evaluación"
weight: 1
---

# Resultados de aprendizaje y criterios de evaluación

El módulo **0372. Gestión de bases de datos** (1º de Administración de Sistemas Informáticos en Red, ASIR) se rige por el **Real Decreto 1629/2009, de 30 de octubre**, que establece el título y sus enseñanzas mínimas. El módulo tiene **6 resultados de aprendizaje (RA)** con **47 criterios de evaluación (CE)**. Estos apuntes se imparten en **160 horas de aula** (5 por semana): el RD fija 105 horas como mínimo, y el currículo de la Comunitat Valenciana amplía el módulo hasta las 160.

> [!IMPORTANT]
> Un **resultado de aprendizaje** describe lo que sabrás hacer al terminar el módulo. Un **criterio de evaluación** es una evidencia concreta que demuestra que lo has conseguido. Cada unidad, práctica y ejercicio de estos apuntes indica qué CE trabaja.

## Horas y unidades por resultado de aprendizaje

Cada RA se corresponde con **una unidad didáctica** (UD01 a UD06), dividida en uno o varios *temas* numerados del 1 al 10. Así se puede evaluar un RA al terminar su unidad.

{tabla}

{mermaid}

> [!NOTE]
> Las unidades siguen el orden de los RA (UD01 es el RA1, UD02 el RA2, y así hasta la UD06 y el RA6). Todo el contenido de las unidades se corresponde con los criterios de evaluación del RD 1629/2009; las prácticas y los proyectos no añaden contenidos ajenos a ellos.

## Criterios de evaluación por resultado de aprendizaje

Texto literal de las enseñanzas mínimas. La última columna indica en qué unidades se trabaja cada criterio.
''',
  th='| CE | Criterio de evaluación | Temas |', tail='''
## Evidencias de aprendizaje

Para cada criterio de evaluación se recogen evidencias de distintos tipos:

| Tipo de evidencia | Ejemplos | CE en los que se usa sobre todo |
|---|---|---|
| Cuestionarios y preguntas de razonamiento | Autoevaluaciones de cada unidad, preguntas de justificación | RA1 |
| Diagramas y documentos de diseño | Diagrama E/R, esquema relacional, informe de normalización | RA2 |
| Scripts SQL ejecutables | Scripts DDL, de consulta y de modificación | RA3, RA4, RA5 |
| Guiones PL/SQL con pruebas | Bloques con variables, control de flujo y excepciones con su batería de pruebas | RA5.e |
| Capturas y registros de ejecución | Planes de ejecución, sesiones concurrentes, ficheros `.log` de Data Pump y SQL*Loader | RA4.g, RA5.h, RA6.g |
| Entregas del proyecto EduGest | Una tarea de proyecto al final de cada unidad | Todos |

## Fuente

- [Real Decreto 1629/2009, de 30 de octubre, por el que se establece el título de Técnico Superior en Administración de Sistemas Informáticos en Red](https://www.boe.es/eli/es/rd/2009/10/30/1629).
''', hdr=('RA','Resultado de aprendizaje','Unidad','Temas','Horas')),
 'val': dict(
  head='''---
title: "Resultats d'aprenentatge i criteris d'avaluació"
weight: 1
---

# Resultats d'aprenentatge i criteris d'avaluació

El mòdul **0372. Gestió de bases de dades** (1r d'Administració de Sistemes Informàtics en Xarxa, ASIR) es regix pel **Reial decret 1629/2009, de 30 d'octubre**, que establix el títol i els seus ensenyaments mínims. El mòdul té **6 resultats d'aprenentatge (RA)** amb **47 criteris d'avaluació (CE)**. Estos apunts s'impartixen en **160 hores d'aula** (5 per setmana): el RD fixa 105 hores com a mínim, i el currículum de la Comunitat Valenciana amplia el mòdul fins a les 160.

> [!IMPORTANT]
> Un **resultat d'aprenentatge** descriu el que sabràs fer en acabar el mòdul. Un **criteri d'avaluació** és una evidència concreta que demostra que ho has aconseguit. Cada unitat, pràctica i exercici d'estos apunts indica quins CE treballa.

## Hores i unitats per resultat d'aprenentatge

Cada RA es correspon amb **una unitat didàctica** (UD01 a UD06), dividida en un o diversos *temes* numerats de l'1 al 10. Així es pot avaluar un RA en acabar la seua unitat.

{tabla}

{mermaid}

> [!NOTE]
> Les unitats seguixen l'ordre dels RA (UD01 és el RA1, UD02 el RA2, i així fins a la UD06 i el RA6). Tot el contingut de les unitats es correspon amb els criteris d'avaluació del RD 1629/2009; les pràctiques i els projectes no afigen continguts aliens a ells.

## Criteris d'avaluació per resultat d'aprenentatge

Text literal de les ensenyances mínimes. L'última columna indica en quines unitats es treballa cada criteri.
''',
  th="| CE | Criteri d'avaluació | Temes |", tail='''
## Evidències d'aprenentatge

Per a cada criteri d'avaluació es recullen evidències de diferents tipus:

| Tipus d'evidència | Exemples | CE en els quals s'usa sobretot |
|---|---|---|
| Qüestionaris i preguntes de raonament | Autoavaluacions de cada unitat, preguntes de justificació | RA1 |
| Diagrames i documents de disseny | Diagrama E/R, esquema relacional, informe de normalització | RA2 |
| Scripts SQL executables | Scripts DDL, de consulta i de modificació | RA3, RA4, RA5 |
| Guions PL/SQL amb proves | Blocs amb variables, control de flux i excepcions amb la seua bateria de proves | RA5.e |
| Captures i registres d'execució | Plans d'execució, sessions concurrents, fitxers `.log` de Data Pump i SQL*Loader | RA4.g, RA5.h, RA6.g |
| Lliuraments del projecte EduGest | Una tasca de projecte al final de cada unitat | Tots |

## Font

- [Reial decret 1629/2009, de 30 d'octubre, pel qual s'establix el títol de Tècnic Superior en Administració de Sistemes Informàtics en Xarxa](https://www.boe.es/eli/es/rd/2009/10/30/1629).
''', hdr=('RA','Resultat d\'aprenentatge','Unitat','Temes','Hores'))}
import json
def main():
    plan = {u['c']: u for u in json.load(open(f'{R}/data/planificacion.json'))['unidades']}
    for lang in ('es', 'val'):
        cur = yaml.safe_load(open(f'{R}/data/curriculo{"_val" if lang=="val" else ""}.yaml', encoding='utf-8'))
        cov = cobertura(lang, cur); t = T[lang]
        # unidades principales por RA (las de la planificación)
        main_ra = {'RA1':['T01'],'RA2':['T02','T03','T04'],'RA3':['T05'],'RA4':['T06','T07'],'RA5':['T08','T09'],'RA6':['T10']}
        carpeta = {}
        for p in glob.glob(f'{R}/content.{lang}/ud*/_index.md'):
            c = p.split('/')[-2]; carpeta[c[:4].upper()] = c
        udof = {'RA1':'UD01','RA2':'UD02','RA3':'UD03','RA4':'UD04','RA5':'UD05','RA6':'UD06'}
        tb = ['| ' + ' | '.join(t['hdr']) + ' |', '|---|---|---|---|:-:|']
        for ra, us in main_ra.items():
            h = sum(plan[u]['h'] for u in us)
            tb.append(f"| **{ra}** | {cur[ra]['titulo']} | [{udof[ra]}](/{carpeta[udof[ra]]}) | " + ', '.join(f'T{int(u[1:])}' for u in us) + f' | {h} |')
        ev = sum(plan[e]['h'] for e in plan if e.startswith('EV'))
        tb.append(f"| | *{'Pruebas de evaluación (3 × 3 h)' if lang=='es' else 'Proves d\'avaluació (3 × 3 h)'}* | | | {ev} |")
        tot = sum(u['h'] for u in plan.values())
        tb.append(f"| | **Total** | | | **{tot}** |")
        lines = ['```mermaid', 'flowchart LR']
        names = {'RA1':'Elementos de las BD y SGBD','RA2':'Diseño lógico normalizado','RA3':'Diseño físico (DDL)','RA4':'Consultas','RA5':'Modificación, transacciones y guiones','RA6':'Seguridad: copias, importación y exportación'}
        if lang == 'val': names = {'RA1':'Elements de les BD i SGBD','RA2':'Disseny lògic normalitzat','RA3':'Disseny físic (DDL)','RA4':'Consultes','RA5':'Modificació, transaccions i guions','RA6':'Seguretat: còpies, importació i exportació'}
        for ra, us in main_ra.items():
            lines.append(f'    {ra}["{ra} · {names[ra]}"] --- {udof[ra]}["{udof[ra]}"] --- ' + ' & '.join(f'T{int(u[1:])}' for u in us))
        lines.append('```')
        out = t['head'].replace('{tabla}', '\n'.join(tb)).replace('{mermaid}', '\n'.join(lines))
        for ra in cur:
            out += f"\n## {ra}. {cur[ra]['titulo']}\n\n{t['th']}\n|---|---|---|\n"
            for c, txt in cur[ra]['ce'].items():
                us = cov.get((ra, c), {})
                cell = ', '.join(f'[{"Tema"} {int(u[1:])}](/{us[u]})' for u in sorted(us)) or '—'
                out += f'| {ra}.{c} | {txt} | {cell} |\n'
        out += t['tail']
        open(f'{R}/content.{lang}/guia/ra-ce.md', 'w', encoding='utf-8').write(out)
main()
