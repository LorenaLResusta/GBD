#!/usr/bin/env python3
"""Leyenda de la notación de Chen extendida (EER) (rombos blancos/negros, ID/E, T/P-D/S)."""
import math
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from chen_eer import BG, FRAME, INK, AGG_S, CARD, tw

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "ud02", "chen-eer-leyenda.svg")
W, H = 980, 600
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d" font-family="DejaVu Sans, Verdana, Arial, sans-serif">',
     '<title id="t">Leyenda de la notación de Chen extendida (EER)</title>',
     '<desc id="d">Entidad, entidad débil con relación identificadora (rombo doble), relaciones binarias y ternaria con participación parcial (línea sencilla) y total (línea doble), atributos (clave, clave alternativa, discriminador, multivaluado, derivado, compuesto), especialización con círculo d u o, y agregación.</desc>',
     f'<rect width="{W}" height="{H}" rx="10" fill="{BG}" stroke="{FRAME}"/>']


def text(x, y, s, size=12, color=INK, anchor="middle", bold=False, italic=False):
    o.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}"'
             f'{" font-weight=\"700\"" if bold else ""}{" font-style=\"italic\"" if italic else ""}>{s}</text>')


def cap(x, y, s):
    text(x, y, s, 11.5, "#334155")


def title(x, y, s):
    text(x, y, s, 13, "#1e3a8a", "start", True)


def line(x1, y1, x2, y2, w=1.4):
    o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{INK}" stroke-width="{w}"/>')


def ent(cx, cy, name="ENTIDAD", w=104, h=38, weak=False):
    o.append(f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" fill="#fff" stroke="{INK}" stroke-width="1.8"/>')
    if weak:
        o.append(f'<rect x="{cx - w / 2 + 4}" y="{cy - h / 2 + 4}" width="{w - 8}" height="{h - 8}" fill="none" stroke="{INK}" stroke-width="1.4"/>')
    text(cx, cy + 4.5, name, 12, bold=True)


def rombo(cx, cy, double=False, hw=34, hh=21):
    pts = lambda ps: " ".join(f"{x},{y}" for x, y in ps)
    P = [(cx - hw, cy), (cx, cy - hh), (cx + hw, cy), (cx, cy + hh)]
    o.append(f'<polygon points="{pts(P)}" fill="#fff" stroke="{INK}" stroke-width="1.8"/>')
    if double:
        Q = [(cx + (x - cx) * 0.8, cy + (y - cy) * 0.8) for x, y in P]
        o.append(f'<polygon points="{pts(Q)}" fill="none" stroke="{INK}" stroke-width="1.3"/>')


def dline(x1, y1, x2, y2):
    """Línea doble (participación total)."""
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L * 2.3, dx / L * 2.3
    line(x1 + nx, y1 + ny, x2 + nx, y2 + ny); line(x1 - nx, y1 - ny, x2 - nx, y2 - ny)


def card(x, y, s):
    w = tw(s) + 8
    o.append(f'<rect x="{x - w / 2}" y="{y - 9}" width="{w}" height="17" rx="3" fill="#fff"/>')
    text(x, y + 4.5, s, 12, CARD, bold=True)


def binaria(y, ca, cb, name, a="A", b="B", lt="1", rt="N", double=False, ta=False, tb=False, weak=False):
    ent(80, y, a, 70); ent(400, y, b, 70, weak=weak)
    (dline if ta else line)(115, y, 206, y)
    (dline if tb else line)(274, y, 365, y)
    rombo(240, y, double)
    text(240, y - 28, name, 12, bold=True, italic=True)
    text(198, y - 8, lt, 11); text(282, y - 8, rt, 11)
    card(150, y, ca); card(330, y, cb)


def att(cx, cy, name, w=None, k=False, kp=False, ak=False, mv=False, d=False):
    w = w or max(tw(name) + 22, 60)
    dash = ' stroke-dasharray="5 3"' if d else ""
    o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{w / 2}" ry="14" fill="#fff" stroke="{INK}" stroke-width="1.4"{dash}/>')
    if mv:
        o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{w / 2 - 4}" ry="10" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    text(cx, cy + 4, name, 12)
    if k or kp or ak:
        t = tw(name)
        da = ' stroke-dasharray="4 3"' if kp else (' stroke-dasharray="1.5 2.5"' if ak else "")
        o.append(f'<line x1="{cx - t / 2}" y1="{cy + 8}" x2="{cx + t / 2}" y2="{cy + 8}" stroke="{INK}" stroke-width="{1.8 if ak else 1.3}"{da}/>')


# ---------------------------------------------------------------- columna izquierda: relaciones
title(30, 34, "RELACIONES Y CARDINALIDADES")
binaria(80, "(0,1)", "(0,1)", "1:1", lt="1", rt="1")
cap(240, 118, "Rombo blanco; 1 o N junto al rombo, (mín,máx) junto a la entidad")
binaria(170, "(1,1)", "(0,N)", "1:N", ta=False)
cap(240, 208, "Línea sencilla: participación parcial (mínimo 0)")
binaria(260, "(1,N)", "(1,N)", "N:M", lt="N", rt="M", ta=True, tb=True)
cap(240, 298, "Línea doble: participación total (mínimo 1)")

# ternaria
ent(90, 380, "A", 60); ent(390, 380, "B", 60); ent(240, 470, "C", 60)
rombo(240, 388, False, 46, 32)
line(120, 380, 194, 386); line(360, 380, 286, 386); line(240, 451, 240, 420)
text(240, 336, "ternaria N:M:P", 12, bold=True, italic=True)
card(150, 378, "(0,N)"); card(330, 378, "(0,N)"); card(262, 440, "(0,N)")
text(176, 376, "N", 11); text(304, 376, "M", 11); text(252, 426, "P", 11)
cap(240, 510, "Un rombo con tres líneas; las N se rotulan N, M, P")

# dependencia
ent(80, 560, "FUERTE", 80); ent(400, 560, "DÉBIL", 80, weak=True)
line(120, 560, 206, 560); dline(274, 560, 360, 560)
rombo(240, 560, True)
card(150, 560, "(1,1)"); card(328, 560, "(1,N)")
cap(240, 592, "Entidad débil: rectángulo doble · relación identificadora: rombo doble")

# ---------------------------------------------------------------- columna derecha: atributos, jerarquía, agregación
title(520, 34, "ATRIBUTOS")
att(580, 80, "atributo"); cap(580, 112, "Simple")
att(700, 80, "clave", k=True); cap(700, 112, "Identificador")
att(830, 80, "nif", ak=True); cap(830, 112, "Clave alternativa")
att(580, 150, "nº_línea", kp=True); cap(580, 182, "Discriminador")
att(700, 150, "teléfono", mv=True); cap(700, 182, "Multivaluado")
att(830, 150, "edad", d=True); cap(830, 182, "Derivado")
att(905, 225, "dirección")
att(860, 270, "calle", 58); att(950, 270, "cp", 46)
line(890, 238, 868, 256); line(920, 238, 942, 256)
cap(905, 300, "Compuesto")

title(520, 230, "ESPECIALIZACIÓN (EER)")
ent(640, 270, "SUPERCLASE", 116)
dline(640, 289, 640, 322)
o.append(f'<circle cx="640" cy="334" r="11.5" fill="#fff" stroke="{INK}" stroke-width="1.6"/>')
text(640, 338.5, "d", 13, bold=True)
line(634, 344, 575, 370); line(646, 344, 705, 370)
for sx in (594, 686):
    ux, uy = (640 - sx), (334 - 358)
    L = math.hypot(ux, uy); ux, uy = ux / L, uy / L
    mx, my = (sx + 640) / 2 + (-5 if sx < 640 else 5), 358
    px, py = -uy, ux
    o.append(f'<path d="M{mx + px * 6:.1f} {my + py * 6:.1f} A6 6 0 0 1 {mx - px * 6:.1f} {my - py * 6:.1f}" fill="#fff" stroke="{INK}" stroke-width="1.5"/>')
ent(575, 388, "SUB_1", 80); ent(705, 388, "SUB_2", 80)
cap(640, 428, "d disjunta · o solapada · línea doble = total · ⊂ subclase")

title(520, 470, "AGREGACIÓN")
o.append(f'<rect x="520" y="486" width="300" height="74" fill="none" stroke="{AGG_S}" stroke-width="2"/>'
         f'<rect x="525" y="491" width="290" height="64" fill="none" stroke="{AGG_S}" stroke-width="1.2"/>')
ent(570, 523, "A", 50); ent(770, 523, "B", 50)
line(595, 523, 636, 523); line(704, 523, 745, 523)
rombo(670, 523)
line(820, 523, 885, 523)
ent(915, 523, "C", 60)
cap(700, 584, "La relación A–B se trata como una entidad")

o.append("</svg>")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write("\n".join(o))
print("ok", OUT)
