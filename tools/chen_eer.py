#!/usr/bin/env python3
"""Generador de diagramas EER (SVG) con la notación de los apuntes del módulo.

Describe el modelo con objetos Python (entidades, relaciones, jerarquías,
agregaciones) y el script calcula la posición de los elementos y escribe un SVG
en blanco y negro, con la misma notación que se usa en clase (draw.io):

    Entidad            rectángulo              Entidad débil      rectángulo doble
    Relación           rombo blanco            Relación identificadora  rombo doble
    Ternaria           rombo con tres (o más) líneas; las N se rotulan N, M, P
    Dependencia en existencia   etiqueta E junto a la entidad dependiente (extensión didáctica)
    Participación      línea doble si es total (mínimo 1) y sencilla si es parcial
    Atributo           óvalo                   Identificador      subrayado continuo
    Clave alternativa  subrayado de puntos     Discriminador      subrayado discontinuo
    Multivaluado       óvalo doble             Derivado           óvalo discontinuo
    Compuesto          óvalo con sub-óvalos
    Especialización    círculo con d (disjunta) u o (solapada); cada subclase se une con
                       el símbolo de subconjunto ⊂ y la línea hasta la superclase es
                       doble si la especialización es total
    Agregación         recuadro doble alrededor de la relación agregada

Convenio de cardinalidades (el de la teoría de la UD02):
    la pareja (mín,máx) escrita JUNTO A UNA ENTIDAD indica con cuántas
    instancias de esa entidad se relaciona una instancia de la otra. Junto a
    cada punta del rombo se repite el máximo (1 o N).

Disposición: automática (Graphviz neato + recocido) o manual si el modelo
trae `pos={"NOMBRE": (x, y), ...}` en una rejilla (unidades de 100 px).
"""
import json
import math
import os
import subprocess
import tempfile
from dataclasses import dataclass, field
from PIL import ImageFont

FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
_f_reg = ImageFont.truetype(FONT_REG, 12)
_f_bold = ImageFont.truetype(FONT_BOLD, 13)

BG = "#ffffff"
FRAME = "#cbd5e1"
LINE = "#1f2937"
INK = "#111111"
ENT_F, ENT_S = "#ffffff", "#111111"
REL_F, REL_S = "#111111", "#111111"
ATT_F, ATT_S = "#ffffff", "#111111"
ISA_F, ISA_S = "#111111", "#111111"
CARD = "#1e3a8a"
ROLE = "#475569"
AGG_S = "#15803d"
TXT = "#111111"


# ---------------------------------------------------------------- modelo
@dataclass
class A:
    """Atributo. k=clave, kp=discriminador, mv=multivaluado, d=derivado."""
    name: str
    k: bool = False
    kp: bool = False
    mv: bool = False
    d: bool = False
    ak: bool = False
    comp: list = field(default_factory=list)  # lista de nombres (atributo compuesto)


def K(n):  return A(n, k=True)
def KP(n): return A(n, kp=True)
def MV(n): return A(n, mv=True)
def D(n):  return A(n, d=True)
def AK(n): return A(n, ak=True)
def C(n, *subs): return A(n, comp=list(subs))


@dataclass
class E:
    name: str
    attrs: list = field(default_factory=list)
    weak: bool = False


@dataclass
class R:
    """Relación. ends = [(entidad, '(mín,máx)', rol|None), ...]"""
    name: str
    ends: list
    attrs: list = field(default_factory=list)
    ident: object = False  # relación identificadora de una entidad débil (rombo doble)
    exist: object = False  # dependencia en existencia: True o nombre de la entidad dependiente (etiqueta E)
    rid: str = ""          # clave para la disposición manual (por defecto, el nombre)


@dataclass
class ISA:
    sup: str
    subs: list
    kind: str = "d"      # d disjunta · o solapada
    total: bool = False

    @property
    def label(self):
        return ("T" if self.total else "P") + "," + ("D" if self.kind == "d" else "S")


@dataclass
class AGG:
    """Agregación: recuadro que contiene entidades y relaciones y actúa como entidad."""
    name: str
    members: list


@dataclass
class Model:
    title: str
    desc: str
    ents: list
    rels: list = field(default_factory=list)
    isas: list = field(default_factory=list)
    aggs: list = field(default_factory=list)
    pos: dict = field(default_factory=dict)
    scale: float = 100


# ---------------------------------------------------------------- medidas
def tw(text, bold=False):
    return (_f_bold if bold else _f_reg).getlength(text)


def attr_size(a_name):
    w = tw(a_name) + 22
    return max(w, 54), 28


def ent_size(name):
    return max(tw(name, True) + 34, 84), 42


HW, HH = 34, 21      # semiejes del rombo (a lo largo del eje y perpendicular)
TR = 30              # radio del triángulo de las ternarias


def rel_size(name):
    return 58, 58


class Node:
    def __init__(self, kind, label, w, h):
        self.kind, self.label, self.w, self.h = kind, label, w, h
        self.x = self.y = 0.0
        self.obj = None
        self.attrs = []    # nodos atributo colgados


def support(kind, w, h, ang):
    """Distancia del centro al borde de la forma en la dirección ang."""
    c, s = math.cos(ang), math.sin(ang)
    hw, hh = w / 2, h / 2
    if kind in ("ent",):
        if abs(c) * hh > abs(s) * hw:
            return hw / max(abs(c), 1e-9)
        return hh / max(abs(s), 1e-9)
    if kind == "rel":
        return hw
    # elipse / círculo
    return 1 / math.sqrt((c / hw) ** 2 + (s / hh) ** 2)


# ---------------------------------------------------------------- layout
def build_nodes(m: Model):
    nodes, edges = {}, []
    for e in m.ents:
        w, h = ent_size(e.name)
        n = Node("ent", e.name, w, h)
        n.obj = e
        nodes["E:" + e.name] = n
    for i, r in enumerate(m.rels):
        w, h = rel_size(r.name)
        n = Node("rel", r.name, w, h)
        n.obj = r
        nodes[f"R:{i}"] = n
        aggnames = {g.name for g in m.aggs}
        for j, (en, card, role) in enumerate(r.ends):
            key = f"G:{en}" if en in aggnames else f"E:{en}"
            edges.append((key, f"R:{i}", dict(card=card, role=role, idx=j, rel=r)))
    for i, s in enumerate(m.isas):
        n = Node("isa", s.label, 22, 22)
        n.obj = s
        nodes[f"I:{i}"] = n
        edges.append((f"E:{s.sup}", f"I:{i}", dict(total=s.total, isa="sup")))
        for sb in s.subs:
            edges.append((f"I:{i}", f"E:{sb}", dict(isa="sub")))
    for g in m.aggs:
        n = Node("agg", g.name, 10, 10)
        n.obj = g
        nodes["G:" + g.name] = n
    return nodes, edges


def natt(a):
    return 1 + len(a.comp)


def layout_radius(n):
    obj = n.obj
    if n.kind == "isa":
        return 34
    if n.kind == "agg":
        return 20
    cnt = sum(natt(a) for a in obj.attrs) if hasattr(obj, "attrs") else 0
    if n.kind == "ent":
        return max(n.w / 2 + 12, 24 + 8 * cnt + n.w * 0.1)
    recursiva = len({e[0] for e in obj.ends}) < len(obj.ends)
    return max(n.w / 2 + 44 + (40 if recursiva else 0), 30 + 10 * cnt)


def run_neato(nodes, edges, seed, spread):
    lines = ["graph G {", f'graph [start={seed}, overlap=prism, sep="+6", splines=false];',
             "node [shape=box, fixedsize=true, label=\"\"];"]
    rad = {k: layout_radius(n) for k, n in nodes.items()}
    for k, n in nodes.items():
        d = rad[k] * 2 / 72
        lines.append(f'"{k}" [width={d:.3f}, height={d:.3f}];')
    for a, b, info in edges:
        ln = (rad[a] + rad[b]) * spread / 72
        lines.append(f'"{a}" -- "{b}" [len={ln:.3f}];')
    lines.append("}")
    with tempfile.NamedTemporaryFile("w", suffix=".dot", delete=False) as f:
        f.write("\n".join(lines))
        path = f.name
    out = subprocess.run(["neato", "-Tjson", path], capture_output=True, text=True)
    os.unlink(path)
    if out.returncode != 0:
        raise RuntimeError(out.stderr)
    data = json.loads(out.stdout)
    for o in data["objects"]:
        x, y = map(float, o["pos"].split(","))
        nodes[o["name"]].x, nodes[o["name"]].y = x, -y
    return rad



import random


def refine(nodes, edges, rad, iters=3500, seed=0):
    """Recocido simulado sobre el esqueleto: compacta y evita solapes/cruces."""
    rnd = random.Random(seed)
    keys = list(nodes)
    idx = {k: i for i, k in enumerate(keys)}
    P = [[nodes[k].x, nodes[k].y] for k in keys]
    R = [rad[k] for k in keys]
    E_ = [(idx[a], idx[b]) for a, b, _ in edges]

    def cost():
        c = 0.0
        n = len(P)
        for i in range(n):
            for j in range(i + 1, n):
                d = math.hypot(P[i][0] - P[j][0], P[i][1] - P[j][1])
                need = (R[i] + R[j]) * 1.0
                if d < need:
                    c += (need - d) ** 2 * 1.6
        for a, b in E_:
            c += math.hypot(P[a][0] - P[b][0], P[a][1] - P[b][1]) * 0.9
        for i in range(len(E_)):
            a, b = E_[i]
            for j in range(i + 1, len(E_)):
                x, y = E_[j]
                if len({a, b, x, y}) < 4:
                    continue
                if seg_inter(P[a], P[b], P[x], P[y]):
                    c += 4000
            for k in range(n):
                if k in (a, b):
                    continue
                # distancia del nodo k al segmento ab
                ax, ay = P[a]; bx, by = P[b]
                dx, dy = bx - ax, by - ay
                L2 = dx * dx + dy * dy or 1
                t = max(0, min(1, ((P[k][0] - ax) * dx + (P[k][1] - ay) * dy) / L2))
                dd = math.hypot(P[k][0] - (ax + t * dx), P[k][1] - (ay + t * dy))
                lim = R[k] * 0.55 + 14
                if dd < lim:
                    c += (lim - dd) ** 2 * 3
        xs0 = min(P[i][0] - R[i] for i in range(n)); xs1 = max(P[i][0] + R[i] for i in range(n))
        ys0 = min(P[i][1] - R[i] for i in range(n)); ys1 = max(P[i][1] + R[i] for i in range(n))
        Wd, Ht = xs1 - xs0, ys1 - ys0
        c += Wd * Ht * 0.004
        if Ht > Wd * 0.9:
            c += (Ht - Wd * 0.9) * 8
        if Wd > Ht * 2.0:
            c += (Wd - Ht * 2.0) * 8
        return c

    cur = cost()
    T0 = 60.0
    for it in range(iters):
        T = T0 * (1 - it / iters) + 0.5
        i = rnd.randrange(len(P))
        ox, oy = P[i]
        step = 8 + 90 * (1 - it / iters)
        P[i][0] += rnd.gauss(0, step)
        P[i][1] += rnd.gauss(0, step)
        nc = cost()
        if nc < cur or rnd.random() < math.exp((cur - nc) / (T * 12)):
            cur = nc
        else:
            P[i][0], P[i][1] = ox, oy
    for k, p in zip(keys, P):
        nodes[k].x, nodes[k].y = p
    return cur


def edge_angles(nodes, edges, key):
    n = nodes[key]
    if n.kind == "rel" and getattr(n, "geo", None):
        g = n.geo
        res = [math.atan2(d[1], d[0]) for d in g["dirs"].values()]
        if g.get("lab"):
            lb = g["lab"]
            res.append(math.atan2(lb.y - n.y, lb.x - n.x))
        return res
    res = []
    for a, b, info in edges:
        if a == key or b == key:
            o = nodes[b] if a == key else nodes[a]
            res.append(math.atan2(o.y - n.y, o.x - n.x))
    return res


def ang_dist(a, b):
    d = abs(a - b) % (2 * math.pi)
    return min(d, 2 * math.pi - d)


def place_attrs(nodes, edges):
    """Reparte los atributos en el círculo alrededor de cada entidad/relación."""
    attr_nodes = []
    for key, n in list(nodes.items()):
        if n.kind not in ("ent", "rel") or not n.obj.attrs:
            continue
        taken = edge_angles(nodes, edges, key)
        k = len(n.obj.attrs)
        chosen = []
        cands = [i * math.pi / 36 for i in range(72)]
        # tamaños para ordenar: primero atributos largos en horizontales
        for _ in range(k):
            best, bs = None, -1
            for c in cands:
                items = taken + chosen
                clear = min(ang_dist(c, t) for t in items) if items else math.pi
                # las aristas pesan más: no queremos atributos sobre ellas
                clear_edge = min((ang_dist(c, t) for t in taken), default=math.pi)
                score = min(clear, clear_edge * 1.6)
                if score > bs:
                    best, bs = c, score
            chosen.append(best)
        chosen.sort()
        attrs = list(n.obj.attrs)
        # los atributos más anchos van a las direcciones más horizontales
        order = sorted(range(k), key=lambda i: abs(math.cos(chosen[i])))
        sizes = sorted(range(k), key=lambda i: -attr_size(attrs[i].name)[0])
        assign = {}
        for rank, ci in enumerate(order[::-1]):
            assign[ci] = sizes[rank]
        for ci in range(k):
            a = attrs[assign[ci]]
            ang = chosen[ci]
            w, h = attr_size(a.name)
            gap = 26 if n.kind == "ent" else 22
            r = support(n.kind, n.w, n.h, ang) + support("att", w, h, ang) + gap
            if k > 5 and ci % 2:
                r += 22
            an = Node("att", a.name, w, h)
            an.obj = a
            an.x, an.y = n.x + r * math.cos(ang), n.y + r * math.sin(ang)
            an.parent = n
            an.owner, an.r, an.ang = n, r, ang
            n.attrs.append(an)
            attr_nodes.append(an)
            # atributos compuestos: hijos más afuera en abanico
            if a.comp:
                m = len(a.comp)
                used = []
                for j, sub in enumerate(a.comp):
                    sw, sh = attr_size(sub)
                    bestsa, bsc = ang, -9
                    for k2 in range(-14, 15):
                        off = k2 * 0.09
                        cand = ang + off
                        ce = min((ang_dist(cand, t) for t in taken), default=math.pi)
                        cc = min((ang_dist(cand, u) for u in used), default=math.pi)
                        sc = min(ce * 1.3, cc * 1.0, 0.9) - 0.12 * abs(off)
                        if sc > bsc:
                            bestsa, bsc = cand, sc
                    sa = bestsa
                    used.append(sa)
                    sr = r + support("att", w, h, sa) + support("att", sw, sh, sa) + 18
                    sn = Node("att", sub, sw, sh)
                    sn.obj = A(sub)
                    sn.x, sn.y = n.x + sr * math.cos(sa), n.y + sr * math.sin(sa)
                    sn.parent = an
                    sn.owner, sn.r, sn.ang = n, sr, sa
                    an.attrs.append(sn)
                    attr_nodes.append(sn)
    return attr_nodes



def relax_attrs(nodes, attr_nodes, edges=(), rounds=60):
    """Aparta los óvalos que se pisan entre sí o con otras formas."""
    allv = [v for v in nodes.values() if v.kind != "agg"] + attr_nodes + rel_labels(nodes)
    skel = [(p, q) for p, q, _, _ in skel_segments(nodes, edges)]
    def tot(an):
        t = 0.0
        segs = [((an.parent.x, an.parent.y), (an.x, an.y))] + [((an.x, an.y), (c.x, c.y)) for c in an.attrs]
        for sg in segs:
            for sk in skel:
                if seg_inter(sg[0], sg[1], sk[0], sk[1]):
                    t += 3000
            for v in allv:
                if v is an or v is an.parent or v in an.attrs or v is getattr(an.parent, "parent", None):
                    continue
                if v.kind == "att" and (v.parent is an):
                    continue
                if seg_hits_box(sg[0], sg[1], v, 3):
                    t += 1500
        for v in allv:
            if v is an or v is an.parent:
                continue
            if getattr(an.parent, "parent", None) is v:
                continue
            t += overlap_area(an, v, 6)
        return t
    def put(an, r, ang):
        an.r, an.ang = r, ang
        an.x = an.owner.x + r * math.cos(ang)
        an.y = an.owner.y + r * math.sin(ang)
    for _ in range(rounds):
        moved = False
        for an in attr_nodes:
            cur = tot(an)
            if cur <= 0:
                continue
            r0, a0 = an.r, an.ang
            best = (cur, r0, a0)
            for dr in (0, 10, 22, 36, 52):
                for da in (0, 0.1, -0.1, 0.22, -0.22, 0.36, -0.36):
                    if dr == 0 and da == 0:
                        continue
                    put(an, r0 + dr, a0 + da)
                    c = tot(an)
                    if c < best[0] - 1e-6:
                        best = (c, r0 + dr, a0 + da)
            put(an, best[1], best[2])
            if best[0] < cur:
                moved = True
        if not moved:
            break


def box(n):
    return (n.x - n.w / 2, n.y - n.h / 2, n.x + n.w / 2, n.y + n.h / 2)


def overlap_area(a, b, pad=3):
    ax0, ay0, ax1, ay1 = box(a)
    bx0, by0, bx1, by1 = box(b)
    w = min(ax1, bx1) - max(ax0, bx0) + pad
    h = min(ay1, by1) - max(ay0, by0) + pad
    return w * h if w > 0 and h > 0 else 0


def seg_inter(p1, p2, p3, p4):
    def ccw(a, b, c):
        return (c[1] - a[1]) * (b[0] - a[0]) - (b[1] - a[1]) * (c[0] - a[0])
    d1, d2 = ccw(p1, p2, p3), ccw(p1, p2, p4)
    d3, d4 = ccw(p3, p4, p1), ccw(p3, p4, p2)
    return d1 * d2 < 0 and d3 * d4 < 0


def seg_hits_box(p, q, n, shrink=4):
    x0, y0, x1, y1 = box(n)
    x0 += shrink; y0 += shrink; x1 -= shrink; y1 -= shrink
    corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    for i in range(4):
        if seg_inter(p, q, corners[i], corners[(i + 1) % 4]):
            return True
    inside = lambda pt: x0 < pt[0] < x1 and y0 < pt[1] < y1
    return inside(p) or inside(q)


def skel_segments(nodes, edges):
    """Segmentos del esqueleto; las aristas duplicadas (reflexivas) se curvan."""
    groups = {}
    for a, b, info in edges:
        groups.setdefault(frozenset((a, b)), []).append((a, b))
    segs, seen = [], {}
    for a, b, info in edges:
        key = frozenset((a, b))
        k = len(groups[key])
        gi = seen.get(key, 0); seen[key] = gi + 1
        na, nb = nodes[a], nodes[b]
        if k > 1:
            curve = (gi - (k - 1) / 2) * 70
            dx, dy = nb.x - na.x, nb.y - na.y
            L = math.hypot(dx, dy) or 1
            c = ((na.x + nb.x) / 2 - dy / L * curve, (na.y + nb.y) / 2 + dx / L * curve)
            mid = Node("mid", "", 1, 1); mid.x, mid.y = c
            segs.append(((na.x, na.y), c, na, mid))
            segs.append((c, (nb.x, nb.y), mid, nb))
        else:
            segs.append(((na.x, na.y), (nb.x, nb.y), na, nb))
    return segs


def all_edges_geometry(nodes, edges, attr_nodes):
    segs = skel_segments(nodes, edges)
    for an in attr_nodes:
        segs.append(((an.parent.x, an.parent.y), (an.x, an.y), an.parent, an))
    return segs


def penalty(nodes, edges, attr_nodes):
    allv = [v for v in nodes.values() if v.kind != "agg"] + attr_nodes + rel_labels(nodes)
    p = 0.0
    for i in range(len(allv)):
        for j in range(i + 1, len(allv)):
            p += overlap_area(allv[i], allv[j]) * 4.0
    segs = all_edges_geometry(nodes, edges, attr_nodes)
    for i in range(len(segs)):
        for j in range(i + 1, len(segs)):
            a, b = segs[i], segs[j]
            if len({id(a[2]), id(a[3]), id(b[2]), id(b[3])}) < 4:
                continue
            if seg_inter(a[0], a[1], b[0], b[1]):
                p += 4000
    for (p1, p2, na, nb) in segs:
        for v in allv:
            if v is na or v is nb:
                continue
            if seg_hits_box(p1, p2, v):
                p += 3000
    # etiquetas de cardinalidad que pisan otros nodos
    for a, b, info in edges:
        if "card" not in info:
            continue
        ent = nodes[a] if a.startswith("E:") else nodes[b]
        oth = nodes[b] if a.startswith("E:") else nodes[a]
        bp = boundary_point(ent, (oth.x, oth.y))
        d = math.hypot(oth.x - bp[0], oth.y - bp[1]) or 1
        t = min(0.85, 30 / d)
        lx, ly = bp[0] + (oth.x - bp[0]) * t, bp[1] + (oth.y - bp[1]) * t
        lab = Node("lab", "", 42, 18); lab.x, lab.y = lx, ly
        for v in allv:
            if v is ent or v is oth:
                continue
            p += overlap_area(lab, v, 0) * 6
    xs = [v.x for v in allv]; ys = [v.y for v in allv]
    Wd, Ht = max(xs) - min(xs), max(ys) - min(ys)
    p += Wd * Ht * 0.006
    if Ht > Wd * 1.25:
        p += (Ht - Wd * 1.25) * 40
    if Wd > Ht * 2.2:
        p += (Wd - Ht * 2.2) * 40
    return p


def solve_manual(m: Model):
    nodes, edges = build_nodes(m)
    S = m.scale
    for k, n in nodes.items():
        if n.kind == "agg":
            continue
        if n.kind == "ent":
            name = n.obj.name
        elif n.kind == "rel":
            name = n.obj.rid or n.obj.name
        else:
            name = "ISA:" + n.obj.sup
        if name not in m.pos:
            raise KeyError(f"falta la posición de {name}")
        x, y = m.pos[name]
        n.x, n.y = x * S, y * S
    for k, n in nodes.items():
        if n.kind == "agg":
            mem = [nodes.get("E:" + x) or next(v for v in nodes.values() if v.kind == "rel" and (v.obj.rid or v.obj.name) == x)
                   for x in n.obj.members]
            n.members = mem
            x0 = min(v.x - v.w / 2 for v in mem); x1 = max(v.x + v.w / 2 for v in mem)
            y0 = min(v.y - v.h / 2 for v in mem); y1 = max(v.y + v.h / 2 for v in mem)
            n.x, n.y, n.w, n.h = (x0 + x1) / 2, (y0 + y1) / 2, x1 - x0, y1 - y0
    orient(nodes, edges)
    at = place_attrs(nodes, edges)
    relax_attrs(nodes, at, edges)
    return (0, nodes, edges, at, 0, 1)


def solve(m: Model, tries=14):
    if m.pos:
        return solve_manual(m)
    best = None
    for seed in range(1, tries + 1):
        nodes, edges = build_nodes(m)
        try:
            rad = run_neato(nodes, edges, seed, 0.8)
        except Exception:
            continue
        refine(nodes, edges, rad, seed=seed)
        orient(nodes, edges)
        at = place_attrs(nodes, edges)
        relax_attrs(nodes, at, edges)
        p = penalty(nodes, edges, at)
        if best is None or p < best[0]:
            best = (p, nodes, edges, at, seed, 0.8)
    return best


# ---------------------------------------------------------------- geometría de relaciones
def _many(card):
    """True si el máximo de la pareja (mín,máx) es mayor que 1."""
    mx = card.strip("() ").replace(":", ",").split(",")[-1].strip().upper()
    return not (mx == "1")


def _max(card):
    mx = card.strip("() ").replace(":", ",").split(",")[-1].strip().upper()
    return "N" if mx in ("N", "M", "*") else mx


def _center(n):
    return (n.x, n.y)


def _unit(dx, dy):
    L = math.hypot(dx, dy) or 1
    return dx / L, dy / L


def _label_node(n, text, cands, nodes):
    """Coloca el nombre de la relación en la dirección candidata más despejada."""
    w, h = tw(text, True) + 10, 18
    others = [v for v in nodes.values() if v is not n and v.kind != "agg"]
    best = None
    for (dx, dy, base) in cands:
        d = base + support("ent", w, h, math.atan2(dy, dx)) + 4
        lab = Node("lab", text, w, h)
        lab.x, lab.y = n.x + dx * d, n.y + dy * d
        sc = sum(overlap_area(lab, v, 6) for v in others)
        # se prefiere encima o a la derecha
        sc += (0 if dy < -0.3 or dx > 0.3 else 30)
        if best is None or sc < best[0]:
            best = (sc, lab)
    return best[1]


def _snap(dx, dy):
    """Vector unitario alineado con el eje dominante (horizontal o vertical)."""
    if abs(dx) >= abs(dy):
        return (1.0 if dx >= 0 else -1.0, 0.0)
    return (0.0, 1.0 if dy >= 0 else -1.0)


def orient(nodes, edges):
    """Calcula forma, puertos y etiqueta de cada relación según dónde están sus entidades."""
    ends_of = {}
    for a, b, info in edges:
        if "card" in info:
            ends_of.setdefault(b, []).append((info["idx"], nodes[a], info))
    for key, n in nodes.items():
        if n.kind != "rel":
            continue
        ends = sorted(ends_of.get(key, []), key=lambda t: t[0])
        c = (n.x, n.y)
        geo = {"ports": {}, "dirs": {}, "polys": [], "outline": [], "tips": {}}
        if len(ends) == 2:
            (i0, A_, inf0), (i1, B_, inf1) = ends
            if A_ is B_:  # reflexiva
                dx, dy = _snap(n.x - A_.x, n.y - A_.y)
                ux, uy = -dy, dx
                geo["reflex"] = (dx, dy)
            else:
                # rombo siempre alineado con los ejes (legible); la punta apunta hacia cada entidad
                ux, uy = _snap(B_.x - A_.x, B_.y - A_.y)
            vx, vy = -uy, ux
            tA = (c[0] - ux * HW, c[1] - uy * HW)
            tB = (c[0] + ux * HW, c[1] + uy * HW)
            top = (c[0] + vx * HH, c[1] + vy * HH)
            bot = (c[0] - vx * HH, c[1] - vy * HH)
            geo["outline"] = [tA, top, tB, bot]
            geo["polys"] = [([tA, top, bot], _many(inf0["card"])), ([tB, top, bot], _many(inf1["card"]))]
            geo["ports"] = {i0: tA, i1: tB}
            geo["dirs"] = {i0: (-ux, -uy), i1: (ux, uy)}
            geo["tips"] = {i0: _max(inf0["card"]), i1: _max(inf1["card"])}
            geo["axis"] = (ux, uy)
            if "reflex" in geo:
                cands = [(geo["reflex"][0], geo["reflex"][1], HH)]
            else:
                cands = [(vx, vy, HH), (-vx, -vy, HH)]
        else:
            # ternaria o n-aria: rombo de Chen más grande, con un puerto por entidad
            hw, hh = 46, 32
            geo["outline"] = [(c[0] - hw, c[1]), (c[0], c[1] - hh), (c[0] + hw, c[1]), (c[0], c[1] + hh)]
            for j, (idx, E_, inf) in enumerate(ends):
                dx, dy = _unit(E_.x - n.x, E_.y - n.y)
                port = _ray_poly(c, (n.x + dx * 400, n.y + dy * 400), geo["outline"])
                geo["ports"][idx] = port
                geo["dirs"][idx] = (dx, dy)
                geo["tips"][idx] = _max(inf["card"])
            cands = [(1, 0, hw), (-1, 0, hw), (0, -1, hh), (0, 1, hh)]
        geo["lab"] = _label_node(n, n.label, cands, nodes)
        n.geo = geo


def rel_labels(nodes):
    return [n.geo["lab"] for n in nodes.values() if n.kind == "rel" and getattr(n, "geo", None)]


def _ray_poly(c, toward, poly):
    """Punto donde el rayo c→toward corta el borde del polígono."""
    dx, dy = toward[0] - c[0], toward[1] - c[1]
    best = None
    for i in range(len(poly)):
        p, q = poly[i], poly[(i + 1) % len(poly)]
        ex, ey = q[0] - p[0], q[1] - p[1]
        den = dx * ey - dy * ex
        if abs(den) < 1e-9:
            continue
        t = ((p[0] - c[0]) * ey - (p[1] - c[1]) * ex) / den
        u = ((p[0] - c[0]) * dy - (p[1] - c[1]) * dx) / den
        if t > 0 and -1e-6 <= u <= 1 + 1e-6:
            if best is None or t < best:
                best = t
    if best is None:
        return c
    return (c[0] + dx * best, c[1] + dy * best)


# ---------------------------------------------------------------- dibujo
def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def boundary_point(n, toward, extra=0):
    if n.kind == "rel" and getattr(n, "geo", None):
        return _ray_poly((n.x, n.y), toward, n.geo["outline"])
    if n.kind == "agg":
        b = n.box
        cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
        ang = math.atan2(toward[1] - cy, toward[0] - cx)
        d = support("ent", b[2] - b[0], b[3] - b[1], ang)
        return cx + d * math.cos(ang), cy + d * math.sin(ang)
    ang = math.atan2(toward[1] - n.y, toward[0] - n.x)
    d = support(n.kind if n.kind in ("ent",) else "att", n.w, n.h, ang) + extra
    return n.x + d * math.cos(ang), n.y + d * math.sin(ang)


def parallel(p, q, off):
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L * off, dx / L * off
    return (p[0] + nx, p[1] + ny), (q[0] + nx, q[1] + ny)


def label(x, y, text, color=CARD, size=12, italic=False, bold=True, bg=True):
    w = tw(text) + 8
    st = ' font-style="italic"' if italic else ""
    wt = ' font-weight="700"' if bold else ""
    r = (f'<rect x="{x - w / 2:.1f}" y="{y - 9:.1f}" width="{w:.1f}" height="17" rx="3" fill="{BG}" opacity="0.94"/>' if bg else "")
    return r + f'<text x="{x:.1f}" y="{y + 4.5:.1f}" font-size="{size}" fill="{color}" text-anchor="middle"{st}{wt}>{esc(text)}</text>'


def _pts(ps):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in ps)


def render(m: Model, best):
    _, nodes, edges, attr_nodes, seed, spread = best
    lines, shapes, texts, under = [], [], [], []
    # agregaciones: recuadro alrededor de miembros y sus atributos
    for n in nodes.values():
        if n.kind == "agg":
            items = []
            for v in n.members:
                items.append(v)
                items += [a for a in attr_nodes if a.owner is v]
                if v.kind == "rel":
                    items.append(v.geo["lab"])
            x0 = min(v.x - v.w / 2 for v in items) - 14; x1 = max(v.x + v.w / 2 for v in items) + 14
            y0 = min(v.y - v.h / 2 for v in items) - 14; y1 = max(v.y + v.h / 2 for v in items) + 14
            n.box = (x0, y0, x1, y1)
            n.x, n.y, n.w, n.h = (x0 + x1) / 2, (y0 + y1) / 2, x1 - x0, y1 - y0
            under.append(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{x1 - x0:.1f}" height="{y1 - y0:.1f}" fill="none" stroke="{AGG_S}" stroke-width="2"/>'
                         f'<rect x="{x0 + 5:.1f}" y="{y0 + 5:.1f}" width="{x1 - x0 - 10:.1f}" height="{y1 - y0 - 10:.1f}" fill="none" stroke="{AGG_S}" stroke-width="1.2"/>')
            texts.append(label(x0 + tw(n.label, True) / 2 + 14, y0 - 1, n.label, color=AGG_S, size=11, bold=True))
    # aristas de atributos
    for an in attr_nodes:
        p = boundary_point(an.parent, (an.x, an.y))
        q = boundary_point(an, (an.parent.x, an.parent.y))
        lines.append(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}"/>')

    nmp = {}
    for a, b, info in edges:
        if "card" in info and nodes[b].geo["tips"][info["idx"]] == "N":
            nmp.setdefault(b, []).append(info["idx"])
    for a, b, info in edges:
        na, nb = nodes[a], nodes[b]
        if "card" in info:
            rn = nb
            g = rn.geo
            idx = info["idx"]
            port = g["ports"][idx]
            d = g["dirs"][idx]
            r = info["rel"]
            if "reflex" in g:
                ctrl = (port[0] + d[0] * 46 - g["reflex"][0] * 10, port[1] + d[1] * 46 - g["reflex"][1] * 10)
                q = boundary_point(na, ctrl)
                lines.append(f'<path d="M{port[0]:.1f} {port[1]:.1f} Q{ctrl[0]:.1f} {ctrl[1]:.1f} {q[0]:.1f} {q[1]:.1f}" fill="none"/>')
                def pt_at(t, port=port, ctrl=ctrl, q=q):
                    t = 1 - t
                    return ((1 - t) ** 2 * port[0] + 2 * (1 - t) * t * ctrl[0] + t * t * q[0],
                            (1 - t) ** 2 * port[1] + 2 * (1 - t) * t * ctrl[1] + t * t * q[1])
                L = 90
            else:
                q = boundary_point(na, port)
                if info["card"].replace(" ", "").startswith("(1"):
                    for off in (-2.3, 2.3):
                        pp, qq = parallel(port, q, off)
                        lines.append(f'<line x1="{pp[0]:.1f}" y1="{pp[1]:.1f}" x2="{qq[0]:.1f}" y2="{qq[1]:.1f}"/>')
                else:
                    lines.append(f'<line x1="{port[0]:.1f}" y1="{port[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}"/>')
                L = math.hypot(port[0] - q[0], port[1] - q[1]) or 1
                def pt_at(t, port=port, q=q):
                    return (q[0] + (port[0] - q[0]) * t, q[1] + (port[1] - q[1]) * t)
            # (mín,máx) junto a la entidad
            x, y = pt_at(min(0.42, 28 / L))
            if "(" in info["card"]:
                texts.append(label(x, y, info["card"]))
            # máximo junto a la punta
            tip = g["tips"][idx]
            if tip == "N":
                tip = "NMP"[min(nmp[b].index(idx), 2)]
            px, py = -d[1], d[0]
            tx, ty = port[0] + d[0] * 9 + px * 10, port[1] + d[1] * 9 + py * 10
            texts.append(f'<text x="{tx:.1f}" y="{ty + 4:.1f}" font-size="11" fill="{INK}" text-anchor="middle">{esc(tip)}</text>')
            # dependencia en existencia (extensión didáctica del módulo): etiqueta E junto a la entidad dependiente
            if r.exist:
                target = r.exist if isinstance(r.exist, str) else None
                is_dep = (na.obj.name == target) if target else (na.kind == "ent" and na.obj.weak)
                if is_dep:
                    x2, y2 = pt_at(min(0.3, 10 / L))
                    ox, oy = _unit(-(q[1] - port[1]), q[0] - port[0])
                    if oy > 0:
                        ox, oy = -ox, -oy
                    texts.append(f'<text x="{x2 + ox * 24:.1f}" y="{y2 + oy * 24 + 4:.1f}" font-size="11" font-weight="700" fill="{INK}" text-anchor="middle">E</text>')
            if info.get("role"):
                xa, ya = pt_at(min(0.42, 28 / L) - 0.03)
                xb, yb = pt_at(min(0.42, 28 / L) + 0.03)
                ox, oy = _unit(-(yb - ya), xb - xa)
                if (xa + ox - rn.x) ** 2 + (ya + oy - rn.y) ** 2 < (xa - ox - rn.x) ** 2 + (ya - oy - rn.y) ** 2:
                    ox, oy = -ox, -oy
                cx_, cy_ = pt_at(min(0.42, 28 / L))
                rw = tw(info["role"]) / 2 + 6
                texts.append(label(cx_ + ox * (14 + abs(ox) * rw), cy_ + oy * 16, info["role"], color=ROLE, italic=True, bold=False, size=11, bg=False))
        elif info.get("isa") == "sub":
            # subclase → círculo, con el símbolo de subconjunto ⊂ abierto hacia la superclase
            p = boundary_point(nb, (na.x, na.y))
            lines.append(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{na.x:.1f}" y2="{na.y:.1f}"/>')
            ux, uy = _unit(na.x - p[0], na.y - p[1])
            L = math.hypot(na.x - p[0], na.y - p[1])
            mx, my = p[0] + ux * min(L * 0.5, L - 22), p[1] + uy * min(L * 0.5, L - 22)
            px, py = -uy, ux
            s0 = (mx + px * 6, my + py * 6); e0 = (mx - px * 6, my - py * 6)
            shapes.append(f'<path d="M{s0[0]:.1f} {s0[1]:.1f} A6 6 0 0 1 {e0[0]:.1f} {e0[1]:.1f}" fill="{BG}" stroke="{INK}" stroke-width="1.5"/>')
        elif info.get("isa") == "sup":
            # círculo → superclase: línea doble si la especialización es total
            q = boundary_point(na, (nb.x, nb.y))
            if info.get("total"):
                for off in (-2.3, 2.3):
                    pp, qq = parallel((nb.x, nb.y), q, off)
                    lines.append(f'<line x1="{pp[0]:.1f}" y1="{pp[1]:.1f}" x2="{qq[0]:.1f}" y2="{qq[1]:.1f}"/>')
            else:
                lines.append(f'<line x1="{nb.x:.1f}" y1="{nb.y:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}"/>')
            shapes.append(f'<circle cx="{nb.x:.1f}" cy="{nb.y:.1f}" r="11.5" fill="{BG}" stroke="{INK}" stroke-width="1.6"/>')
            shapes.append(f'<text x="{nb.x:.1f}" y="{nb.y + 4.5:.1f}" font-size="13" font-weight="700" text-anchor="middle" fill="{INK}">{nb.obj.kind}</text>')

    # formas
    for key, n in nodes.items():
        if n.kind == "ent":
            e = n.obj
            x0, y0, x1, y1 = box(n)
            shapes.append(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{n.w:.1f}" height="{n.h:.1f}" fill="{ENT_F}" stroke="{ENT_S}" stroke-width="1.8"/>')
            if e.weak:
                shapes.append(f'<rect x="{x0 + 4:.1f}" y="{y0 + 4:.1f}" width="{n.w - 8:.1f}" height="{n.h - 8:.1f}" fill="none" stroke="{ENT_S}" stroke-width="1.4"/>')
            texts.append(f'<text x="{n.x:.1f}" y="{n.y + 5:.1f}" font-size="13" font-weight="700" text-anchor="middle" fill="{TXT}">{esc(n.label)}</text>')
        elif n.kind == "rel":
            g = n.geo
            shapes.append(f'<polygon points="{_pts(g["outline"])}" fill="{BG}" stroke="{REL_S}" stroke-width="1.8" stroke-linejoin="round"/>')
            if n.obj.ident:
                c0 = (n.x, n.y)
                inner = [(c0[0] + (v[0] - c0[0]) * 0.8, c0[1] + (v[1] - c0[1]) * 0.8) for v in g["outline"]]
                shapes.append(f'<polygon points="{_pts(inner)}" fill="none" stroke="{REL_S}" stroke-width="1.3" stroke-linejoin="round"/>')
            lb = g["lab"]
            texts.append(f'<text x="{lb.x:.1f}" y="{lb.y + 4.5:.1f}" font-size="12.5" font-weight="700" font-style="italic" text-anchor="middle" fill="{TXT}">{esc(n.label)}</text>')
    for an in attr_nodes:
        a = an.obj
        dash = ' stroke-dasharray="5 3"' if a.d else ""
        shapes.append(f'<ellipse cx="{an.x:.1f}" cy="{an.y:.1f}" rx="{an.w / 2:.1f}" ry="{an.h / 2:.1f}" fill="{ATT_F}" stroke="{ATT_S}" stroke-width="1.4"{dash}/>')
        if a.mv:
            shapes.append(f'<ellipse cx="{an.x:.1f}" cy="{an.y:.1f}" rx="{an.w / 2 - 4:.1f}" ry="{an.h / 2 - 4:.1f}" fill="none" stroke="{ATT_S}" stroke-width="1.2"/>')
        texts.append(f'<text x="{an.x:.1f}" y="{an.y + 4:.1f}" font-size="12" text-anchor="middle" fill="{TXT}">{esc(an.label)}</text>')
        if a.k or a.kp or a.ak:
            w = tw(an.label)
            da = ' stroke-dasharray="4 3"' if a.kp else (' stroke-dasharray="1.5 2.5"' if a.ak else "")
            sw = "1.3" if not a.ak else "1.8"
            texts.append(f'<line x1="{an.x - w / 2:.1f}" y1="{an.y + 8:.1f}" x2="{an.x + w / 2:.1f}" y2="{an.y + 8:.1f}" stroke="{TXT}" stroke-width="{sw}"{da}/>')

    allv2 = [v for v in nodes.values() if v.kind not in ("agg",)] + attr_nodes + rel_labels(nodes)
    for n in nodes.values():
        if n.kind == "agg":
            b = Node("x", "", n.w, n.h + 20); b.x, b.y = n.x, n.y - 6
            allv2.append(b)
    minx = min(v.x - v.w / 2 for v in allv2) - 24
    maxx = max(v.x + v.w / 2 for v in allv2) + 24
    miny = min(v.y - v.h / 2 for v in allv2) - 24
    maxy = max(v.y + v.h / 2 for v in allv2) + 24
    W, H = maxx - minx, maxy - miny
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{minx:.0f} {miny:.0f} {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}" role="img" aria-labelledby="t d" font-family="DejaVu Sans, Verdana, Arial, sans-serif">',
           f'<title id="t">{esc(m.title)}</title><desc id="d">{esc(m.desc)}</desc>',
           f'<rect x="{minx:.0f}" y="{miny:.0f}" width="{W:.0f}" height="{H:.0f}" rx="10" fill="{BG}" stroke="{FRAME}"/>']
    svg += under
    svg += [f'<g stroke="{LINE}" stroke-width="1.4" fill="none">' + "".join(lines) + "</g>"]
    svg += shapes + texts + ["</svg>"]
    return "\n".join(svg), (W, H)


def draw(m: Model, path, tries=8):
    best = solve(m, tries)
    svg, size = render(m, best)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    return best[0], size


if __name__ == "__main__":
    demo = Model(
        "Demo", "Demo",
        [E("EMPLEADO", [K("dni"), AK("nss"), A("nombre"), C("direccion", "calle", "ciudad"), MV("telefono")]),
         E("DEPARTAMENTO", [K("codigo"), A("nombre")]),
         E("PROYECTO", [K("cod"), D("duracion")]),
         E("HIJO", [KP("nombre"), A("fecha_nac")], weak=True),
         E("TECNICO", [A("nivel")]), E("ADMINISTRATIVO", [A("idioma")])],
        [R("trabaja", [("EMPLEADO", "(0,N)", None), ("DEPARTAMENTO", "(1,1)", None)]),
         R("dirige", [("EMPLEADO", "(0,1)", "jefe"), ("EMPLEADO", "(0,N)", "subordinado")]),
         R("asigna", [("EMPLEADO", "(0,N)", None), ("PROYECTO", "(1,N)", None), ("DEPARTAMENTO", "(1,1)", None)], [A("fecha")]),
         R("tiene", [("EMPLEADO", "(1,1)", None), ("HIJO", "(0,N)", None)], ident=True)],
        [ISA("EMPLEADO", ["TECNICO", "ADMINISTRATIVO"], "d", True)])
    print(draw(demo, "/tmp/claude-0/-home-claude/3010f14d-a30e-5c7a-b169-b6aebcc67104/scratchpad/demo.svg", 10))
