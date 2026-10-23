#!/usr/bin/env python3
"""Genera los diagramas explicativos de las UD01-UD04 (assets/images/*.svg).

Todos comparten estilo, tipografía del sistema y ajuste automático del texto a la
anchura de cada caja, de modo que nada se desborda ni se corta. Los elementos
con ``class="hot"`` y ``data-tip`` son interactivos cuando el SVG se incrusta
con el shortcode ``{{< diagrama >}}`` (tooltip al pasar el ratón o pulsar).

Uso: python3 tools/gen_infografias.py [nombre ...]
"""
import os, sys
from xml.sax.saxutils import escape
from PIL import ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("INFO_OUT") or os.path.join(HERE, "..", "assets", "images")
FD = "/usr/share/fonts/truetype/dejavu/"
_F = {}


def font(size, bold=False):
    k = (round(size * 4), bold)
    if k not in _F:
        _F[k] = ImageFont.truetype(FD + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), size * 4)
    return _F[k]


def tw(t, size, bold=False):
    """Anchura estimada (DejaVu Sans es más ancha que las fuentes del sistema: margen de seguridad)."""
    return font(size, bold).getlength(t) / 4 * 0.93


def wrap(t, size, maxw, bold=False):
    out, cur = [], ""
    for w in t.split():
        c = (cur + " " + w).strip()
        if tw(c, size, bold) <= maxw or not cur:
            cur = c
        else:
            out.append(cur)
            cur = w
    if cur:
        out.append(cur)
    return out


BG0, BG1, CARD, CARD2 = "#0f172a", "#1e293b", "#1e293b", "#334155"
INK, MUTED = "#f1f5f9", "#94a3b8"
BLUE, GREEN, PURPLE, ORANGE, RED, PINK = "#38bdf8", "#34d399", "#a78bfa", "#fbbf24", "#f87171", "#f472b6"
BLUE_D, GREEN_D, PURPLE_D, ORANGE_D, RED_D = "#0369a1", "#047857", "#6d28d9", "#b45309", "#b91c1c"
FONT = 'system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'


class Svg:
    def __init__(self, name, W, H, title, desc):
        self.name, self.W, self.H, self.svg_title, self.desc = name, W, H, title, desc
        self.e = []

    def add(self, s):
        self.e.append(s)

    # ---- primitivas
    def rect(self, x, y, w, h, fill=CARD, stroke=None, sw=2, rx=8, dash=None, extra=""):
        st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"{st}{d}{extra}/>')

    def text(self, x, y, t, size=14, fill=INK, bold=False, anchor="middle", italic=False, extra=""):
        if not t:
            return
        w = ' font-weight="700"' if bold else ""
        i = ' font-style="italic"' if italic else ""
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}"{w}{i}{extra}>{escape(t)}</text>')

    def para(self, x, y, t, size=13, fill=INK, maxw=300, lh=None, anchor="start", bold=False):
        """Párrafo ajustado a maxw. Devuelve la y de la línea siguiente."""
        lh = lh or size * 1.4
        for ln in wrap(t, size, maxw, bold):
            self.text(x, y, ln, size, fill, bold, anchor)
            y += lh
        return y

    def line(self, x1, y1, x2, y2, c=MUTED, w=2, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}/>')

    def card(self, x, y, w, h, color, title=None, tsize=16):
        self.rect(x, y, w, h, CARD, color, 2, 10)
        if title:
            self.text(x + w / 2, y + 28, title, tsize, color, True)

    def box(self, x, y, w, h, label, fill=BLUE_D, stroke=BLUE, size=13, color="#fff", bold=True, rx=6, tip=None, dash=None):
        """Caja con texto centrado que se ajusta (y crece en líneas) sin salirse."""
        if tip:
            self.add(f'<g class="hot" tabindex="0" data-tip="{escape(tip, {chr(34): "&quot;"})}">')
        self.rect(x, y, w, h, fill, stroke, 2, rx, dash)
        lines = wrap(label, size, w - 14, bold)
        lh = size * 1.25
        y0 = y + h / 2 - (len(lines) - 1) * lh / 2 + size * 0.35
        for i, ln in enumerate(lines):
            self.text(x + w / 2, y0 + i * lh, ln, size, color, bold)
        if tip:
            self.add("</g>")

    def diamond(self, cx, cy, w, h, label, fill=GREEN_D, stroke=GREEN, size=12, double=False, tip=None):
        if tip:
            self.add(f'<g class="hot" tabindex="0" data-tip="{escape(tip, {chr(34): "&quot;"})}">')
        pts = f"{cx},{cy - h / 2} {cx + w / 2},{cy} {cx},{cy + h / 2} {cx - w / 2},{cy}"
        self.add(f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        if double:
            k = 0.8
            pts = f"{cx},{cy - h / 2 * k} {cx + w / 2 * k},{cy} {cx},{cy + h / 2 * k} {cx - w / 2 * k},{cy}"
            self.add(f'<polygon points="{pts}" fill="none" stroke="{stroke}" stroke-width="1.4"/>')
        self.text(cx, cy + size * 0.35, label, size, "#fff", True)
        if tip:
            self.add("</g>")

    def ellipse(self, cx, cy, label, rx=None, ry=17, fill=PURPLE_D, stroke=PURPLE, size=12, underline=False, dash=False, double=False):
        rx = rx or tw(label, size) / 2 + 14
        d = ' stroke-dasharray="4 3"' if dash else ""
        self.add(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="1.8"{d}/>')
        if double:
            self.add(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx - 4:.1f}" ry="{ry - 4}" fill="none" stroke="{stroke}" stroke-width="1.2"/>')
        deco = ' text-decoration="underline"' if underline else ""
        self.text(cx, cy + size * 0.35, label, size, "#fff", False, extra=deco)
        return rx

    def arrow(self, x1, y1, x2, y2, c=MUTED, w=2, dash=None):
        self.line(x1, y1, x2, y2, c, w, dash)
        import math
        a = math.atan2(y2 - y1, x2 - x1)
        p = [(x2, y2), (x2 - 10 * math.cos(a - 0.4), y2 - 10 * math.sin(a - 0.4)), (x2 - 10 * math.cos(a + 0.4), y2 - 10 * math.sin(a + 0.4))]
        self.add(f'<polygon points="{" ".join(f"{px:.1f},{py:.1f}" for px, py in p)}" fill="{c}"/>')

    def title(self, t, y=40, size=21):
        self.text(self.W / 2, y, t, size, INK, True)

    def save(self):
        s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.W} {self.H}" width="{self.W}" height="{self.H}" role="img" aria-labelledby="t d" font-family=\'{FONT}\'>',
             f'<title id="t">{escape(self.svg_title)}</title><desc id="d">{escape(self.desc)}</desc>',
             '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0f172a"/><stop offset="1" stop-color="#1e293b"/></linearGradient></defs>',
             '<style>.hot{cursor:pointer;transition:filter .15s}.hot:hover,.hot:focus,.hot.on{filter:brightness(1.35) drop-shadow(0 0 6px rgba(255,255,255,.35));outline:none}</style>',
             f'<rect width="{self.W}" height="{self.H}" rx="12" fill="url(#bg)"/>']
        s += self.e + ["</svg>"]
        path = os.path.join(OUT, self.name + ".svg")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w", encoding="utf-8").write("\n".join(s))


def bullets(s, x, y, w, items, color, mark="✓", size=13):
    for t in items:
        ok = mark if not t.startswith("!") else "✗"
        t = t.lstrip("!")
        col = color if ok == "✓" else RED
        s.text(x, y, ok, size, col, True, "start")
        y = s.para(x + 20, y, t, size, INK, w - 20)
        y += 4
    return y


# =====================================================================  UD01
def acid():
    s = Svg("acid-transactions", 820, 455, "Propiedades ACID de las transacciones",
            "Cuatro tarjetas: Atomicidad, Consistencia, Aislamiento y Durabilidad, con su significado.")
    s.title("Propiedades ACID de las transacciones")
    items = [("A", "Atomicidad", "Atomicity", "«Todo o nada»", "Todas las operaciones de la transacción se completan (COMMIT) o ninguna surte efecto (ROLLBACK).", RED,
              "Transferencia de 100 €: o se resta de una cuenta Y se suma en la otra, o no ocurre nada."),
             ("C", "Consistencia", "Consistency", "«De estado válido a estado válido»", "La base de datos pasa de un estado correcto a otro correcto: se cumplen claves, restricciones CHECK, FK y reglas.", ORANGE,
              "Una transacción que dejara un pedido sin cliente se rechaza por la FK."),
             ("I", "Aislamiento", "Isolation", "«Sin interferencias»", "Las transacciones concurrentes no se interfieren: los cambios no se ven fuera hasta confirmarse.", BLUE,
              "Dos usuarios reservando el último asiento: el SGBD los serializa."),
             ("D", "Durabilidad", "Durability", "«Los cambios permanecen»", "Una vez confirmada (COMMIT), los datos persisten aunque haya un fallo del sistema o un reinicio.", GREEN,
              "El redo log permite recuperar lo confirmado tras un corte de luz.")]
    for i, (l, n, en, lema, d, c, tip) in enumerate(items):
        x, y = 30 + (i % 2) * 390, 70 + (i // 2) * 190
        s.add(f'<g class="hot" tabindex="0" data-tip="{escape(tip)}">')
        s.rect(x, y, 370, 175, CARD, c, 2, 10)
        s.rect(x + 16, y + 16, 46, 46, c, None, 0, 8)
        s.text(x + 39, y + 49, l, 26, "#0f172a", True)
        s.text(x + 76, y + 36, f"{n} ({en})", 16, c, True, "start")
        s.text(x + 76, y + 56, lema, 13, MUTED, False, "start", True)
        s.para(x + 18, y + 92, d, 13.5, INK, 334, 19)
        s.add("</g>")
    s.save()


def sgbd_overview():
    s = Svg("sgbd-overview", 820, 515, "Visión general de un SGBD",
            "Usuarios y aplicaciones envían consultas SQL al SGBD, que gestiona el almacenamiento físico.")
    s.title("Visión general de un SGBD")
    s.card(24, 70, 220, 380, BLUE, "Usuarios y apps")
    for i, (t, tip) in enumerate([("Apps web / móvil", "Aplicaciones que se conectan al SGBD mediante un driver (JDBC, ODBC…)."), ("Usuarios finales", "Consultan datos a través de formularios o informes; no escriben SQL."),
                                  ("Administrador (DBA)", "Crea usuarios, ajusta el rendimiento, hace copias de seguridad."), ("Programadores SQL", "Escriben consultas y procedimientos almacenados.")]):
        s.box(42, 118 + i * 78, 184, 56, t, CARD2, "#475569", 14, INK, False, 8, tip)
    s.card(300, 70, 230, 380, "#60a5fa", "SGBD (DBMS)")
    for i, (t, tip) in enumerate([("Procesador de consultas", "Analiza (parser) y valida cada sentencia SQL."), ("Optimizador de SQL", "Elige el plan de ejecución más barato: qué índice usar, en qué orden hacer los joins."),
                                  ("Gestor de transacciones", "Garantiza ACID: COMMIT, ROLLBACK, bloqueos y recuperación."), ("Seguridad e integridad", "Comprueba privilegios y restricciones (PK, FK, CHECK).")]):
        s.box(318, 118 + i * 78, 194, 56, t, "#2563eb", "#93c5fd", 14, "#fff", True, 8, tip)
    s.card(586, 70, 210, 380, GREEN, "Almacenamiento")
    for i, (t, tip) in enumerate([("Datos físicos", "Ficheros de datos en disco, organizados en bloques/páginas."), ("Diccionario de datos", "Metadatos: qué tablas, columnas y usuarios existen. Se consulta con vistas como USER_TABLES (Oracle)."),
                                  ("Índices", "Estructuras (B-tree) que aceleran búsquedas."), ("Logs (redo/undo)", "Registro de cambios para deshacer y rehacer transacciones.")]):
        s.box(604, 118 + i * 78, 174, 56, t, GREEN_D, GREEN, 14, "#fff", True, 8, tip)
    for y in (216, 294):
        s.arrow(244, y, 298, y, BLUE, 2.5)
        s.arrow(532, y, 584, y, GREEN, 2.5)
    s.text(410, 480, "El SGBD es la capa intermedia entre las aplicaciones y el almacenamiento físico.", 14, MUTED)
    s.text(410, 502, "Pasa el ratón sobre cada bloque para ver qué hace.", 12, MUTED, False, "middle", True)
    s.save()


def timeline():
    s = Svg("timeline-evolution", 960, 430, "Evolución histórica de las bases de datos",
            "Línea del tiempo desde las tarjetas Hollerith hasta SQL y NoSQL.")
    s.title("Evolución histórica de las bases de datos")
    ev = [("1890", "Tarjetas Hollerith", "Censo de EE. UU.", BLUE, "Herman Hollerith patentó la tabuladora en 1884; se usó en el censo de 1890 y su empresa acabó en IBM."),
          ("Años 50", "Cintas magnéticas", "Acceso secuencial", GREEN, "Ficheros secuenciales: para leer el registro 1000 había que pasar por los 999 anteriores."),
          ("Años 60", "Modelos jerárquico y red", "IMS · CODASYL", ORANGE, "IMS de IBM nació en el programa Apolo para gestionar listas de materiales. CODASYL definió el modelo en red."),
          ("1970", "Modelo relacional", "E. F. Codd (IBM)", RED, "Codd publicó «A Relational Model of Data for Large Shared Data Banks»: datos en tablas y lenguaje declarativo."),
          ("1976", "Modelo E/R", "Peter Chen", PURPLE, "Chen propuso el modelo Entidad-Relación para el diseño conceptual."),
          ("1979–86", "SQL comercial y ANSI", "Oracle · SQL-86", PINK, "Oracle V2 (1979) fue el primer SQL comercial; ANSI estandarizó SQL en 1986."),
          ("2009+", "NoSQL y la nube", "MongoDB · Cloud", BLUE, "El término NoSQL se popularizó en 2009 ante la necesidad de escalar horizontalmente.")]
    n = len(ev)
    x0, x1, ym = 70, 890, 220
    s.line(x0 - 20, ym, x1 + 20, ym, "#475569", 4)
    for i, (d, t, sub, c, tip) in enumerate(ev):
        x = x0 + i * (x1 - x0) / (n - 1)
        up = i % 2 == 0
        bw = 124
        bx = min(max(x - bw / 2, 10), 960 - bw - 10)
        by = 80 if up else 262
        s.add(f'<g class="hot" tabindex="0" data-tip="{escape(tip)}">')
        s.line(x, ym, x, by + (112 if up else 0), c, 2)
        s.rect(bx, by, bw, 112, CARD, c, 2, 10)
        s.text(bx + bw / 2, by + 26, d, 16, c, True)
        yy = s.para(bx + bw / 2, by + 50, t, 13, INK, bw - 12, 16, "middle", True)
        s.para(bx + bw / 2, yy + 2, sub, 12, MUTED, bw - 12, 15, "middle")
        s.add("</g>")
        s.add(f'<circle cx="{x:.1f}" cy="{ym}" r="9" fill="{c}" stroke="{BG0}" stroke-width="3"/>')
    s.text(480, 410, "Pulsa o pasa el ratón sobre cada hito para ver el contexto.", 12, MUTED, False, "middle", True)
    s.save()


def file_access():
    s = Svg("file-access-methods", 880, 560, "Métodos de organización y acceso a ficheros",
            "Acceso secuencial, directo con fórmula de desplazamiento e indexado.")
    s.title("Métodos de organización y acceso a ficheros")
    # 1
    s.card(24, 66, 832, 130, BLUE)
    s.text(44, 94, "1. Acceso secuencial (cintas magnéticas)", 16, BLUE, True, "start")
    s.text(44, 116, "Para leer el registro 4 hay que recorrer antes el 1, el 2 y el 3.", 13, MUTED, False, "start")
    for i, t in enumerate(["Registro 1", "Registro 2", "Registro 3"]):
        s.box(44 + i * 130, 134, 118, 44, t, "#2563eb", "#93c5fd", 13, "#fff", True, 6, "Leído y descartado: no es el que buscamos.")
    s.box(44 + 3 * 130, 134, 150, 44, "Registro 4 (buscado)", GREEN_D, GREEN, 13, "#fff", True, 6, "Solo se llega a él tras leer todos los anteriores: coste O(n).")
    s.arrow(100, 188, 560, 188, RED, 2)
    s.text(600, 192, "recorrido paso a paso (lento)", 12, RED, False, "start", True)
    # 2
    s.card(24, 212, 832, 150, GREEN)
    s.text(44, 240, "2. Acceso directo (discos; registros de longitud fija L)", 16, GREEN, True, "start")
    s.text(44, 262, "Desplazamiento = N × L: se salta directamente a la posición.", 13, MUTED, False, "start")
    s.box(44, 282, 190, 50, "Reg 0 · bytes 0–229", CARD2, "#64748b", 13, INK, False, 6, "Con L = 230 bytes, el registro 0 ocupa los bytes 0 a 229.")
    s.box(246, 282, 210, 50, "Reg 1 · bytes 230–459", CARD2, "#64748b", 13, INK, False, 6, "El registro 1 empieza en 1 × 230 = 230.")
    s.box(468, 282, 190, 50, "Reg N · offset N × 230", GREEN_D, GREEN, 13, "#fff", True, 6, "Fórmula del desplazamiento: N × L.")
    s.para(676, 302, "Ejemplo: el registro 10 está en el byte 2300.", 13, ORANGE, 170, 17, "start", True)
    # 3
    s.card(24, 378, 832, 160, PURPLE)
    s.text(44, 406, "3. Acceso indexado (índices, árboles B)", 16, PURPLE, True, "start")
    s.text(44, 428, "Un índice guarda pares (clave → puntero) y permite buscar rápido en ficheros de longitud variable.", 13, MUTED, False, "start")
    s.box(44, 452, 230, 56, "Índice: ID 25 → puntero #402", PURPLE_D, PURPLE, 13, "#fff", True, 6, "El índice se recorre rápido (está ordenado) y devuelve la posición del bloque.")
    s.arrow(276, 480, 410, 480, ORANGE, 2.5)
    s.box(414, 452, 280, 56, "Bloque de datos #402 en disco", CARD2, "#64748b", 13, INK, True, 6, "Un único acceso al bloque devuelve el registro.")
    s.save()


def file_vs_sgbd():
    s = Svg("file-vs-sgbd", 860, 445, "Sistemas de ficheros frente a SGBD", "Cada programa con su fichero frente a un SGBD centralizado.")
    s.title("Sistemas de ficheros frente a SGBD")
    s.card(24, 66, 400, 350, RED, "Sistema de ficheros")
    s.box(44, 106, 150, 48, "Programa de nóminas", CARD2, "#64748b", 13, INK, False, 6)
    s.box(244, 106, 160, 48, "Fichero_Empleados.dat", RED_D, RED, 12, "#fff", True, 6, "Cada programa guarda sus propios datos: el empleado puede estar duplicado en varios ficheros.")
    s.line(194, 130, 244, 130, RED, 2)
    s.box(44, 176, 150, 48, "Programa de facturación", CARD2, "#64748b", 13, INK, False, 6)
    s.box(244, 176, 160, 48, "Fichero_Clientes.dat", RED_D, RED, 12, "#fff", True, 6, "Si cambia el formato del fichero hay que modificar el programa.")
    s.line(194, 200, 244, 200, RED, 2)
    s.rect(44, 244, 360, 156, "#0f172a", None, 0, 8)
    bullets(s, 60, 272, 330, ["!Redundancia e inconsistencia", "!Dependencia entre datos y programas", "!Concurrencia y seguridad limitadas", "!Sin control central de integridad", "!Datos aislados entre programas"], RED)
    s.card(436, 66, 400, 350, GREEN, "Enfoque con SGBD")
    for i, t in enumerate(["Nóminas", "Facturación", "RR. HH. web"]):
        s.box(452 + i * 122, 106, 112, 44, t, CARD2, "#64748b", 13, INK, False, 6)
        s.line(508 + i * 122, 150, 636, 186, GREEN, 2)
    s.box(452, 186, 368, 48, "SGBD: capa centralizada", GREEN_D, GREEN, 15, "#fff", True, 8, "Todas las aplicaciones acceden a los datos por el SGBD, nunca directamente al fichero.")
    s.rect(452, 250, 368, 150, "#0f172a", None, 0, 8)
    bullets(s, 468, 278, 340, ["Sin redundancias innecesarias", "Independencia física y lógica", "Control de concurrencia y ACID", "Seguridad con permisos finos", "Reglas de integridad unificadas"], GREEN)
    s.save()


def ansi_sparc():
    s = Svg("ansi-sparc-architecture", 820, 560, "Arquitectura ANSI/SPARC de tres niveles",
            "Nivel externo (vistas), conceptual (esquema global) e interno (almacenamiento).")
    s.title("Arquitectura ANSI/SPARC de tres niveles")
    lv = [("NIVEL EXTERNO · vistas de usuario", BLUE, ["Vista de recepción", "Vista de contabilidad", "Vista de dirección / BI"], "Cada grupo de usuarios ve solo lo que necesita (vistas, permisos)."),
          ("NIVEL CONCEPTUAL · esquema global", GREEN, ["Tablas, relaciones, claves y restricciones de integridad"], "Describe QUÉ datos hay y cómo se relacionan, sin detalles de almacenamiento."),
          ("NIVEL INTERNO · almacenamiento físico", PURPLE, ["Ficheros, páginas de disco, índices B-tree, cifrado y compresión"], "Describe CÓMO se guardan los datos en disco.")]
    ys = [70, 230, 390]
    for i, (t, c, its, tip) in enumerate(lv):
        y = ys[i]
        s.add(f'<g class="hot" tabindex="0" data-tip="{escape(tip)}">')
        s.rect(34, y, 752, 100, CARD, c, 2, 12)
        s.text(410, y + 28, t, 16, c, True)
        n = len(its)
        bw = (752 - 40 - (n - 1) * 14) / n
        for j, it in enumerate(its):
            s.box(54 + j * (bw + 14), y + 44, bw, 44, it, {BLUE: BLUE_D, GREEN: GREEN_D, PURPLE: PURPLE_D}[c], c, 13, "#fff", True, 6)
        s.add("</g>")
    for y, t, c in [(170, "Transformación lógica (vistas)", BLUE), (330, "Transformación física (acceso a disco)", GREEN)]:
        s.line(410, y, 410, y + 58, c, 2, "5 4")
        s.text(424, y + 34, t, 12.5, c, False, "start", True)
    s.rect(34, 502, 752, 44, "#0f172a", None, 0, 8)
    s.text(410, 530, "Independencia lógica (externo ↔ conceptual) e independencia física (conceptual ↔ interno).", 12.5, INK)
    s.save()


def keys():
    s = Svg("relational-model-keys", 860, 480, "El modelo relacional: tablas, claves primarias y foráneas",
            "Tablas SOCIO y PRESTAMO relacionadas por id_socio.")
    s.title("El modelo relacional: PK y FK")
    cols = [(24, "SOCIO", BLUE, BLUE_D, ["id_socio (PK)", "nombre", "email"], [["101", "Laura Gómez", "laura@mail.com"], ["102", "Carlos Ruiz", "carlos@mail.com"], ["103", "Ana Martínez", "ana@mail.com"]], [110, 120, 150]),
            (470, "PRESTAMO", GREEN, GREEN_D, ["id_prestamo", "id_socio (FK)", "fecha"], [["5001", "101", "2026-10-01"], ["5002", "103", "2026-10-02"], ["5003", "101", "2026-10-05"]], [100, 130, 110])]
    xs = {}
    for x, name, c, cd, head, rows, wd in cols:
        W = sum(wd) + 30
        s.card(x, 66, W, 280, c)
        s.rect(x, 66, W, 44, cd, c, 2, 10)
        s.text(x + W / 2, 94, f"Tabla: {name}", 17, "#fff", True)
        s.rect(x + 12, 124, W - 24, 34, CARD2, None, 0, 4)
        cx = x + 20
        for h, w in zip(head, wd):
            col = ORANGE if "FK" in h else (c if "PK" in h or h == "id_prestamo" else MUTED)
            s.text(cx, 146, h, 13, col, True, "start")
            cx += w
        for r, row in enumerate(rows):
            yy = 168 + r * 40
            s.rect(x + 12, yy, W - 24, 34, "#0f172a" if r % 2 == 0 else CARD, None, 0, 4)
            cx = x + 20
            for k, (v, w) in enumerate(zip(row, wd)):
                col = c if k == 0 and name == "SOCIO" else (ORANGE if name == "PRESTAMO" and k == 1 else INK)
                s.text(cx, yy + 22, v, 13, col, k == 0 or (name == "PRESTAMO" and k == 1), "start")
                cx += w
        xs[name] = (x, W)
    # flecha FK -> PK
    x0, W0 = xs["PRESTAMO"]
    s.add(f'<g class="hot" tabindex="0" data-tip="Cada valor de id_socio en PRESTAMO debe existir en SOCIO: es la integridad referencial. El SGBD rechaza un préstamo del socio 999 si no existe.">')
    s.add(f'<path d="M{x0} 208 C{x0 - 20} 208 {xs["SOCIO"][0] + xs["SOCIO"][1] + 20} 208 {xs["SOCIO"][0] + xs["SOCIO"][1]} 208" stroke="{ORANGE}" stroke-width="2.5" stroke-dasharray="7 5" fill="none"/>')
    s.add(f'<polygon points="{xs["SOCIO"][0] + xs["SOCIO"][1]},208 {xs["SOCIO"][0] + xs["SOCIO"][1] + 11},202 {xs["SOCIO"][0] + xs["SOCIO"][1] + 11},214" fill="{ORANGE}"/>')
    s.add("</g>")
    s.text(24 + 190, 376, "PK: identifica cada fila de forma única", 13, BLUE, True)
    s.text(470 + 180, 376, "FK: referencia la PK de otra tabla", 13, ORANGE, True)
    s.rect(34, 400, 792, 56, "#0f172a", None, 0, 8)
    s.para(430, 424, "La clave foránea apunta a la clave primaria de otra tabla y garantiza la consistencia de los datos.", 13, INK, 740, 18, "middle")
    s.save()


def db_arch():
    s = Svg("db-architectures", 860, 400, "Arquitecturas de despliegue de bases de datos", "Centralizada, cliente-servidor y distribuida.")
    s.title("Arquitecturas de despliegue")
    cols = [("1. Centralizada", BLUE, BLUE_D, "Servidor único: app + SGBD + BD", "Terminales o usuarios locales", ["Mantenimiento sencillo", "!Cuello de botella", "!Punto único de fallo"], "Todo vive en una máquina: simple, pero si cae, cae todo."),
            ("2. Cliente-servidor", GREEN, GREEN_D, "Servidor SGBD (SQL)", "Clientes: PC, web, móvil", ["Escalabilidad", "Carga repartida", "Modelo estándar actual"], "Los clientes envían SQL por la red; el servidor lo ejecuta."),
            ("3. Distribuida", PURPLE, PURPLE_D, "Nodos: Madrid · Barcelona · Valencia", "Datos repartidos o replicados", ["Alta disponibilidad", "Tolerancia a fallos", "!Réplicas complejas"], "Los datos se reparten (fragmentación) o copian (réplica) entre nodos.")]
    for i, (t, c, cd, main, sub, bl, tip) in enumerate(cols):
        x = 24 + i * 278
        s.add(f'<g class="hot" tabindex="0" data-tip="{escape(tip)}">')
        s.card(x, 66, 262, 300, c, t)
        s.box(x + 20, 100, 222, 70, main, cd, c, 14, "#fff", True, 8)
        s.text(x + 131, 198, sub, 12.5, MUTED, False, "middle", True)
        s.rect(x + 16, 222, 230, 130, "#0f172a", None, 0, 8)
        bullets(s, x + 30, 252, 205, bl, c)
        s.add("</g>")
    s.save()


# =====================================================================  UD02
def er_components():
    s = Svg("er-components", 880, 505, "Componentes del modelo entidad-relación",
            "Entidad fuerte y débil, relación con cardinalidades y tipos de atributos.")
    s.title("Componentes del modelo E/R")
    s.card(24, 66, 410, 160, BLUE, "1. Entidades")
    s.box(54, 110, 150, 52, "ALUMNO", BLUE_D, BLUE, 15, "#fff", True, 3, "Entidad fuerte: existe por sí misma y tiene clave propia.")
    s.add(f'<g class="hot" tabindex="0" data-tip="Entidad débil: depende de otra (p. ej. un EJEMPLAR depende de su LIBRO) y su clave es parcial."><rect x="244" y="110" width="150" height="52" fill="{BLUE_D}" stroke="{BLUE}" stroke-width="2"/><rect x="249" y="115" width="140" height="42" fill="none" stroke="{BLUE}" stroke-width="1.5"/>')
    s.text(319, 141, "EJEMPLAR", 15, "#fff", True)
    s.add("</g>")
    s.text(129, 192, "Entidad fuerte (rectángulo)", 12.5, MUTED)
    s.text(319, 192, "Entidad débil (doble rectángulo)", 12.5, MUTED)
    s.card(446, 66, 410, 160, GREEN, "2. Relaciones y cardinalidades")
    s.box(466, 118, 100, 44, "CLIENTE", GREEN_D, GREEN, 13, "#fff", True, 3)
    s.box(746, 118, 90, 44, "PEDIDO", GREEN_D, GREEN, 13, "#fff", True, 3)
    s.line(566, 140, 631, 140, GREEN, 2)
    s.line(691, 140, 746, 140, GREEN, 2)
    s.diamond(661, 140, 80, 52, "REALIZA", "#065f46", GREEN, 11, False, "Una relación asocia entidades. REALIZA une CLIENTE y PEDIDO.")
    s.text(598, 130, "(0,n)", 12, ORANGE, True)
    s.text(718, 130, "(1,1)", 12, ORANGE, True)
    s.text(651, 204, "(mín, máx): un cliente hace 0..n pedidos; un pedido es de 1 cliente", 11.5, MUTED)
    s.card(24, 242, 832, 250, PURPLE, "3. Tipos de atributos")
    xs = [110, 260, 440, 640, 780]
    s.ellipse(xs[0], 322, "dni", 46, 20, underline=True)
    s.text(xs[0], 366, "Identificador (PK)", 12.5, MUTED)
    s.ellipse(xs[1], 322, "nombre", 56, 20)
    s.text(xs[1], 366, "Simple", 12.5, MUTED)
    s.ellipse(xs[2], 300, "dirección", 54, 18)
    s.ellipse(xs[2] - 55, 366, "calle", 36, 16)
    s.ellipse(xs[2] + 55, 366, "ciudad", 42, 16)
    s.line(xs[2] - 20, 316, xs[2] - 45, 351, MUTED, 1.5)
    s.line(xs[2] + 20, 316, xs[2] + 45, 351, MUTED, 1.5)
    s.text(xs[2], 408, "Compuesto", 12.5, MUTED)
    s.ellipse(xs[3], 322, "teléfono", 54, 20, double=True)
    s.text(xs[3], 366, "Multivaluado", 12.5, MUTED)
    s.ellipse(xs[4], 322, "edad", 40, 20, dash=True)
    s.text(xs[4], 366, "Derivado", 12.5, MUTED)
    s.rect(44, 430, 792, 46, "#0f172a", None, 0, 8)
    s.text(440, 458, "Subrayado = clave · doble elipse = varios valores · línea discontinua = se calcula de otro dato", 12.5, INK)
    s.save()


def generalization():
    s = Svg("generalization-hierarchy", 880, 555, "Jerarquías EER: generalización y especialización",
            "PERSONA como supertipo de ALUMNO, PROFESOR y PAS, con restricciones disjunta/solapada y total/parcial.")
    s.title("Generalización y especialización")
    s.box(340, 70, 200, 56, "PERSONA", BLUE_D, BLUE, 16, "#fff", True, 8, "Supertipo: atributos comunes (dni, nombre, email).")
    s.line(437, 126, 437, 150, BLUE, 2)
    s.line(443, 126, 443, 150, BLUE, 2)
    s.add(f'<g class="hot" tabindex="0" data-tip="Círculo con d = disjunta (un solo subtipo). La línea doble hasta el supertipo indica participación total (todo supertipo está en algún subtipo)."><circle cx="440" cy="168" r="18" fill="#fff" stroke="{ORANGE}" stroke-width="2"/>')
    s.text(440, 173, "d", 14, "#0f172a", True)
    s.add("</g>")
    s.line(440, 186, 440, 212, ORANGE, 2)
    s.line(150, 212, 730, 212, ORANGE, 2)
    for x, t, tip in [(150, "ALUMNO", "Subtipo con atributos propios: nº de expediente, ciclo."), (440, "PROFESOR", "Subtipo: especialidad, departamento."), (730, "PAS", "Personal de administración y servicios: puesto, unidad.")]:
        s.line(x, 212, x, 240, ORANGE, 2)
        s.box(x - 90, 240, 180, 52, t, GREEN_D, GREEN, 14, "#fff", True, 8, tip)
    s.card(34, 320, 812, 210, BLUE, "Restricciones de la jerarquía", 16)
    rows = [("Disjunta (D)", ORANGE, "Una instancia del supertipo pertenece a UN solo subtipo."), ("Solapada (S)", ORANGE, "Una instancia puede pertenecer a VARIOS subtipos a la vez."),
            ("Total (T)", GREEN, "Toda instancia del supertipo pertenece al menos a un subtipo."), ("Parcial (P)", GREEN, "Puede haber instancias que no estén en ningún subtipo.")]
    for i, (a, c, b) in enumerate(rows):
        x, y = 54 + (i % 2) * 400, 380 + (i // 2) * 76
        s.text(x, y, a, 14, c, True, "start")
        s.para(x, y + 20, b, 13, INK, 360, 17)
    s.save()


def agregacion():
    s = Svg("aggregation-ternary", 880, 540, "Agregación y relación ternaria",
            "A la izquierda, MATRIMONIO como agregación relacionada con JUZGADO; a la derecha, la ternaria PROFESOR–ASIGNATURA–GRUPO.")
    s.title("Agregación y relación ternaria")
    s.card(24, 66, 420, 440, ORANGE, "1. Agregación")
    s.rect(54, 108, 360, 140, "#0f172a", ORANGE, 2, 10, "7 5")
    s.text(234, 130, "Agregado: MATRIMONIO", 13, ORANGE, True)
    s.box(70, 160, 100, 46, "HOMBRE", BLUE_D, BLUE, 13, "#fff", True, 3)
    s.box(298, 160, 100, 46, "MUJER", BLUE_D, BLUE, 13, "#fff", True, 3)
    s.line(170, 183, 202, 183, BLUE, 2)
    s.line(266, 183, 298, 183, BLUE, 2)
    s.diamond(234, 183, 64, 44, "CASA", "#065f46", GREEN, 11, False, "Relación binaria entre HOMBRE y MUJER. Se agrega para poder relacionarla con otra entidad.")
    s.line(234, 248, 234, 300, ORANGE, 2)
    s.diamond(234, 322, 120, 52, "CIVIL EN", "#92400e", ORANGE, 12, False, "Una relación no puede unirse a otra relación; con la agregación, el matrimonio completo se relaciona con JUZGADO.")
    s.line(234, 348, 234, 392, ORANGE, 2)
    s.box(174, 392, 120, 46, "JUZGADO", GREEN_D, GREEN, 13, "#fff", True, 3)
    s.para(234, 470, "Se agrupa una relación como si fuera una entidad.", 12.5, MUTED, 360, 16, "middle")
    s.card(456, 66, 400, 440, GREEN, "2. Relación ternaria")
    s.box(480, 120, 130, 46, "PROFESOR", GREEN_D, GREEN, 13, "#fff", True, 3)
    s.box(702, 120, 130, 46, "ASIGNATURA", GREEN_D, GREEN, 13, "#fff", True, 3)
    s.box(591, 380, 130, 46, "GRUPO", GREEN_D, GREEN, 13, "#fff", True, 3)
    s.line(545, 166, 656, 262, GREEN, 2)
    s.line(767, 166, 656, 262, GREEN, 2)
    s.line(656, 300, 656, 380, GREEN, 2)
    s.diamond(656, 280, 100, 62, "IMPARTE", "#065f46", GREEN, 12, False, "Un profesor imparte una asignatura a un grupo: solo la combinación de los tres tiene sentido.")
    s.para(656, 460, "Lectura: una pareja de entidades frente a la tercera.", 12.5, MUTED, 340, 16, "middle")
    s.save()


def pava():
    s = Svg("eer-example-pava", 920, 560, "Diagrama EER de la empresa de repostería PAVA S.A.",
            "CLIENTE realiza PEDIDO, que incluye FORMATO_PRODUCTO; PRODUCTO se compone de INGREDIENTE y compite con COMPETIDOR.")
    s.title("Caso: repostería «PAVA S.A.»")
    def e(x, y, t, fill, stroke, tip):
        s.box(x, y, 170, 50, t, fill, stroke, 13, "#fff", True, 3, tip)
    e(30, 90, "CLIENTE", BLUE_D, BLUE, "Quien compra. Atributos: nif, nombre, dirección.")
    e(270, 90, "PEDIDO", BLUE_D, BLUE, "Compra realizada por un cliente en una fecha.")
    e(510, 90, "FORMATO_PRODUCTO", GREEN_D, GREEN, "Presentación comercial de un producto: peso en gramos y precio.")
    e(740, 90, "PROMOCIÓN", PURPLE_D, PURPLE, "Descuento aplicable a un formato.")
    e(510, 230, "PRODUCTO", GREEN_D, GREEN, "Tarta, bizcocho, galleta…")
    e(270, 230, "INGREDIENTE", GREEN_D, GREEN, "Materia prima. Un producto tiene varios ingredientes.")
    e(510, 360, "COMPETIDOR", RED_D, RED, "Producto equivalente de una marca rival.")
    for (a, b, t) in [(200, 270, "REALIZA"), (440, 510, "INCLUYE")]:
        s.line(a, 115, b, 115, MUTED, 2)
        s.diamond((a + b) / 2, 115, 62, 40, "", "#065f46", GREEN, 10)
    s.text(235, 88, "REALIZA", 11.5, INK, True)
    s.text(475, 88, "INCLUYE", 11.5, INK, True)
    s.line(680, 115, 740, 115, PURPLE, 2)
    s.line(595, 140, 595, 230, MUTED, 2)
    s.line(440, 255, 510, 255, MUTED, 2)
    s.diamond(475, 255, 62, 40, "", "#065f46", GREEN, 10)
    s.text(475, 292, "COMPUESTO", 11.5, INK, True)
    s.line(595, 280, 595, 360, RED, 2)
    s.diamond(595, 320, 62, 40, "", "#7f1d1d", RED, 10)
    s.text(660, 324, "SIMILAR A", 11.5, INK, True, "start")
    s.rect(30, 440, 860, 104, "#0f172a", BLUE, 2, 10)
    s.text(50, 466, "Aspectos clave del modelo", 14, BLUE, True, "start")
    y = 488
    for t in ["Composición: relación M:N entre PRODUCTO e INGREDIENTE, con el porcentaje de participación.", "Formatos: PRODUCTO se vende en varios FORMATO_PRODUCTO (peso en gramos y precio propio).", "Competencia: PRODUCTO se relaciona con los COMPETIDOR de marcas rivales."]:
        s.text(50, y, "•", 13, ORANGE, True, "start")
        s.text(66, y, t, 12.5, INK, False, "start")
        y += 19
    s.save()


# =====================================================================  UD03
def anatomia():
    s = Svg("relational-table-anatomy", 900, 515, "Anatomía de una relación (tabla)", "Tabla EMPLEADO con atributos, tuplas, grado y cardinalidad.")
    s.title("Anatomía de una tabla relacional")
    s.card(24, 66, 600, 320, BLUE)
    s.rect(24, 66, 600, 44, BLUE_D, BLUE, 2, 10)
    s.text(324, 94, "Relación EMPLEADO", 17, "#fff", True)
    head = ["id_emp (PK)", "nombre", "salario", "id_dep (FK)"]
    wd = [130, 150, 120, 120]
    s.add('<g class="hot" tabindex="0" data-tip="Atributo (columna): una propiedad con su dominio. Aquí hay 4, así que el grado de la relación es 4.">')
    s.rect(40, 124, 568, 36, CARD2, None, 0, 4)
    cx = 54
    for h, w in zip(head, wd):
        s.text(cx, 147, h, 13.5, ORANGE if "FK" in h else (BLUE if "PK" in h else INK), True, "start")
        cx += w
    s.add("</g>")
    rows = [["101", "Ana Torres", "2400.00", "10"], ["102", "Carlos Ruiz", "1950.00", "20"], ["103", "Lucía Vega", "3100.00", "10"], ["104", "David Sanz", "2100.00", "30"]]
    for r, row in enumerate(rows):
        yy = 172 + r * 48
        s.add(f'<g class="hot" tabindex="0" data-tip="Tupla (fila): un empleado concreto. Hay 4 tuplas, así que la cardinalidad es 4.">')
        s.rect(40, yy, 568, 40, "#0f172a" if r % 2 == 0 else CARD, GREEN if r == 1 else None, 2, 4)
        cx = 54
        for k, (v, w) in enumerate(zip(row, wd)):
            s.text(cx, yy + 26, v, 13.5, ORANGE if k == 3 else (BLUE if k == 0 else INK), k in (0, 3), "start")
            cx += w
        s.add("</g>")
    s.line(624, 268, 664, 268, GREEN, 2)
    s.box(664, 70, 214, 76, "Atributo / campo: grado = 4 columnas", "#0c4a6e", BLUE, 13, BLUE, True, 8)
    s.box(664, 230, 214, 76, "Tupla / fila / registro: cardinalidad = 4 filas", "#064e3b", GREEN, 13, GREEN, True, 8)
    s.box(664, 310, 214, 76, "Clave foránea (FK): referencia a DEPARTAMENTO", "#78350f", ORANGE, 13, ORANGE, True, 8)
    s.line(608, 336, 664, 348, ORANGE, 2)
    s.line(608, 142, 664, 108, BLUE, 2)
    s.rect(24, 410, 852, 84, "#0f172a", None, 0, 8)
    s.text(450, 440, "Grado = número de atributos (4).  Cardinalidad = número de tuplas (4).", 14, INK, True)
    s.text(450, 466, "La PK identifica cada tupla; la FK enlaza con la PK de otra relación.", 13, MUTED)
    s.save()


def reglas():
    s = Svg("eer-to-relational-rules", 900, 560, "Reglas de transformación del modelo E/R al relacional", "Cuatro reglas: 1:N, N:M, entidad débil y relación reflexiva.")
    s.title("Del E/R al relacional: 4 reglas")
    cards = [("1. Relación 1:N", BLUE, "La PK del lado «1» pasa al lado «N» como FK.", ["DEPARTAMENTO (id_dep PK, nombre)", "EMPLEADO (id_emp PK, nombre, id_dep FK)"], "No se crea tabla nueva: la FK viaja al lado N."),
             ("2. Relación N:M", GREEN, "Se crea una tabla intermedia con las dos claves.", ["ALUMNO (id_alumno PK) · ASIGNATURA (id_asig PK)", "MATRICULA (id_alumno PK,FK · id_asig PK,FK · nota)"], "La PK de la tabla nueva es compuesta; los atributos de la relación (nota) van aquí."),
             ("3. Entidad débil", PURPLE, "La PK de la débil incluye la PK de su propietaria.", ["EDIFICIO (id_edificio PK, dirección)", "AULA (id_edificio PK,FK · num_aula PK)"], "Sin edificio no hay aula: la FK forma parte de la PK."),
             ("4. Reflexiva 1:N", PINK, "Autorreferencia: la FK apunta a su propia tabla.", ["EMPLEADO (id_emp PK, nombre,", "id_jefe FK → EMPLEADO.id_emp)"], "El jefe de un empleado es otro empleado; la FK admite NULL para el director.")]
    for i, (t, c, d, code, tip) in enumerate(cards):
        x, y = 24 + (i % 2) * 438, 66 + (i // 2) * 240
        s.add(f'<g class="hot" tabindex="0" data-tip="{escape(tip)}">')
        s.card(x, y, 420, 224, c, t)
        s.para(x + 20, y + 58, d, 13.5, INK, 380, 18)
        for j, ln in enumerate(code):
            fw = "700" if j else "400"
            s.rect(x + 20, y + 100 + j * 52, 380, 42, "#0f172a", c, 1.5, 6)
            s.para(x + 32, y + 126 + j * 52 - (8 if tw(ln, 12.5, True) > 356 else 0), ln, 12.5, INK, 356, 15)
        s.add("</g>")
    s.text(450, 548, "Pasa el ratón sobre cada regla para ver el porqué.", 12, MUTED, False, "middle", True)
    s.save()


# =====================================================================  Chen (ejemplos de UD04 / UD02)
def _attr_row(s, cx, cy_ent, ent_h, attrs, side, gap=82):
    """Coloca atributos (lista de (texto, estilo)) encima/debajo de una forma centrada en cx."""
    if not attrs:
        return
    ws = [tw(t, 12.5) + 30 for t, _ in attrs]
    total = sum(ws) + 14 * (len(attrs) - 1)
    x = cx - total / 2
    y = cy_ent + (ent_h / 2 + gap if side == "down" else -(ent_h / 2 + gap))
    for (t, st), w in zip(attrs, ws):
        ax = x + w / 2
        ys = cy_ent + (ent_h / 2 if side == "down" else -ent_h / 2)
        s.line(cx + (ax - cx) * 0.35, ys, ax, y - (17 if side == "down" else -17), MUTED, 1.6)
        s.ellipse(ax, y, t, rx=w / 2, ry=17, underline=("pk" in st or "parcial" in st), dash=("parcial" in st), size=12.5)
        x += w + 14


def chen_binary(name, title, left, right, rel, cl, cr, tip, left_attrs, right_attrs, rel_attrs=(), weak_right=False, ident=False):
    W, H, ym = 1000, 390, 190
    s = Svg(name, W, H, title, title)
    lx, rx_, cx = 150, 850, 500
    bw, bh = 170, 56
    s.box(lx - bw / 2, ym - bh / 2, bw, bh, left, BLUE_D, BLUE, 16, "#fff", True, 2)
    s.box(rx_ - bw / 2, ym - bh / 2, bw, bh, right, BLUE_D if not weak_right else "#0f172a", BLUE, 16, "#fff", True, 2)
    if weak_right:
        s.rect(rx_ - bw / 2 + 6, ym - bh / 2 + 6, bw - 12, bh - 12, "none", BLUE, 1.5, 0)
    s.line(lx + bw / 2, ym, cx - 85, ym, MUTED, 2)
    s.line(cx + 85, ym, rx_ - bw / 2, ym, MUTED, 2)
    s.diamond(cx, ym, 170, 82, rel, GREEN_D, GREEN, 14, ident, tip)
    s.text(lx + bw / 2 + 36, ym - 12, cl, 15, ORANGE, True)
    s.text(rx_ - bw / 2 - 36, ym - 12, cr, 15, ORANGE, True)
    # atributos: primero (clave) arriba, resto abajo
    _attr_row(s, lx, ym, bh, left_attrs[:1], "up")
    _attr_row(s, lx, ym, bh, left_attrs[1:], "down")
    _attr_row(s, rx_, ym, bh, right_attrs[:1], "up")
    _attr_row(s, rx_, ym, bh, right_attrs[1:], "down")
    _attr_row(s, cx, ym, 82, list(rel_attrs), "down", 70)
    s.save()


def chen_all():
    PK, N, PAR = "pk", "", "parcial"
    chen_binary("chen-actor-pelicula", "ACTOR participa en PELICULA (N:M)", "ACTOR", "PELICULA", "PARTICIPA", "N", "M",
                "N:M: un actor participa en muchas películas y una película tiene muchos actores. Los atributos de la relación (personaje, orden) pertenecen a la pareja.",
                [("id_actor", PK), ("nombre", N)], [("id_pelicula", PK), ("titulo", N)], [("personaje", N), ("orden_aparicion", N)])
    chen_binary("chen-alumno-asignatura", "ALUMNO se matricula en ASIGNATURA (N:M)", "ALUMNO", "ASIGNATURA", "MATRICULA", "N", "M",
                "N:M con atributos propios: la nota depende de la pareja alumno-asignatura. Pasará a una tabla intermedia.",
                [("id_alumno", PK), ("nombre", N)], [("id_asignatura", PK), ("titulo", N)], [("fecha", N), ("nota", N)])
    chen_binary("chen-cliente-pedido", "CLIENTE realiza PEDIDO (1:N)", "CLIENTE", "PEDIDO", "REALIZA", "1", "N",
                "1:N: un cliente hace muchos pedidos; cada pedido es de un único cliente. La FK irá en PEDIDO.",
                [("id_cliente", PK), ("nombre", N), ("email", N)], [("num_pedido", PK), ("fecha_pedido", N), ("importe", N)])
    chen_binary("chen-paciente-consulta", "PACIENTE realiza CONSULTA (1:N)", "PACIENTE", "CONSULTA", "REALIZA", "1", "N",
                "1:N: un paciente tiene muchas consultas; cada consulta es de un paciente.",
                [("id_paciente", PK), ("dni", N)], [("id_consulta", PK), ("fecha", N), ("importe", N)])
    chen_binary("chen-empleado-vehiculo", "EMPLEADO tiene asignado un VEHICULO (1:1 opcional)", "EMPLEADO", "VEHICULO", "ASIGNA", "(0,1)", "(0,1)",
                "1:1 con participación opcional en ambos lados: puede haber empleados sin vehículo y vehículos sin asignar.",
                [("id_empleado", PK), ("nombre", N)], [("matricula", PK), ("modelo", N)])
    chen_binary("chen-edificio-aula", "EDIFICIO identifica AULA (entidad débil)", "EDIFICIO", "AULA", "IDENTIFICA", "1", "N",
                "Entidad débil: el número de aula solo identifica dentro de su edificio. La PK de AULA será (cod_edificio, num_aula).",
                [("cod_edificio", PK), ("nombre", N)], [("num_aula", PAR), ("capacidad", N)], weak_right=True, ident=True)
    chen_binary("chen-hotel-habitacion", "HOTEL contiene HABITACION (entidad débil)", "HOTEL", "HABITACION", "CONTIENE", "1", "N",
                "La habitación 101 existe en muchos hoteles: solo se identifica junto a su hotel (clave parcial + PK del hotel).",
                [("id_hotel", PK), ("nombre", N)], [("num_habitacion", PAR), ("capacidad", N), ("precio_noche", N)], weak_right=True, ident=True)
    # biblioteca (ternaria de cadena: AUTOR - LIBRO - EJEMPLAR)
    W, H, ym = 1180, 400, 190
    s = Svg("chen-biblioteca", W, H, "Modelo E/R de biblioteca en notación Chen", "AUTOR N:M LIBRO; LIBRO 1:N EJEMPLAR (entidad débil)")
    xs = {"a": 130, "r1": 340, "l": 550, "r2": 770, "e": 1010}
    bw, bh = 160, 56
    s.box(xs["a"] - bw / 2, ym - bh / 2, bw, bh, "AUTOR", BLUE_D, BLUE, 16, "#fff", True, 2)
    s.box(xs["l"] - bw / 2, ym - bh / 2, bw, bh, "LIBRO", BLUE_D, BLUE, 16, "#fff", True, 2)
    s.box(xs["e"] - bw / 2, ym - bh / 2, bw, bh, "EJEMPLAR", "#0f172a", BLUE, 16, "#fff", True, 2)
    s.rect(xs["e"] - bw / 2 + 6, ym - bh / 2 + 6, bw - 12, bh - 12, "none", BLUE, 1.5, 0)
    s.line(xs["a"] + bw / 2, ym, xs["r1"] - 70, ym, MUTED, 2)
    s.line(xs["r1"] + 70, ym, xs["l"] - bw / 2, ym, MUTED, 2)
    s.line(xs["l"] + bw / 2, ym, xs["r2"] - 80, ym, MUTED, 2)
    s.line(xs["r2"] + 80, ym, xs["e"] - bw / 2, ym, MUTED, 2)
    s.diamond(xs["r1"], ym, 140, 74, "ESCRIBE", GREEN_D, GREEN, 13, False, "N:M: un autor escribe varios libros y un libro puede tener varios autores. orden_autoria indica quién firma primero.")
    s.diamond(xs["r2"], ym, 160, 74, "IDENTIFICA", GREEN_D, GREEN, 13, True, "Relación identificadora: el ejemplar no existe sin su libro; su clave es (isbn, num_ejemplar).")
    s.text(xs["a"] + bw / 2 + 30, ym - 12, "N", 15, ORANGE, True)
    s.text(xs["l"] - bw / 2 - 30, ym - 12, "M", 15, ORANGE, True)
    s.text(xs["l"] + bw / 2 + 28, ym - 12, "1", 15, ORANGE, True)
    s.text(xs["e"] - bw / 2 - 28, ym - 12, "N", 15, ORANGE, True)
    _attr_row(s, xs["a"], ym, bh, [("id_autor", "pk")], "up")
    _attr_row(s, xs["a"], ym, bh, [("nombre", "")], "down")
    _attr_row(s, xs["r1"], ym, 74, [("orden_autoria", "")], "down", 70)
    _attr_row(s, xs["l"], ym, bh, [("isbn", "pk")], "up")
    _attr_row(s, xs["l"], ym, bh, [("titulo", "")], "down")
    _attr_row(s, xs["e"], ym, bh, [("num_ejemplar", "parcial")], "up")
    _attr_row(s, xs["e"], ym, bh, [("estado", "")], "down")
    s.save()
    # jerarquía de empleados
    W, H = 900, 420
    s = Svg("chen-jerarquia-empleados", W, H, "Especialización de EMPLEADO", "EMPLEADO se especializa en PROGRAMADOR y ADMINISTRATIVO")
    s.box(370, 100, 160, 56, "EMPLEADO", BLUE_D, BLUE, 16, "#fff", True, 2)
    for t, dx, st in [("id_empleado", -230, "pk"), ("nombre", 0, ""), ("salario", 230, "")]:
        w = tw(t, 12.5) + 30
        s.line(450 + dx * 0.25, 100, 450 + dx, 58 + 17, MUTED, 1.6)
        s.ellipse(450 + dx, 58, t, rx=w / 2, ry=17, underline=(st == "pk"), size=12.5)
    s.line(450, 156, 450, 205, MUTED, 2)
    s.add(f'<g class="hot" tabindex="0" data-tip="ISA = «es un». Todo programador es un empleado y hereda sus atributos."><circle cx="450" cy="230" r="26" fill="#fff" stroke="{ORANGE}" stroke-width="2"/>')
    s.text(450, 235, "ISA", 12, "#0f172a", True)
    s.add("</g>")
    s.line(450, 256, 450, 285, MUTED, 2)
    s.line(250, 285, 650, 285, MUTED, 2)
    for x, t, a in [(250, "PROGRAMADOR", "lenguaje_principal"), (650, "ADMINISTRATIVO", "nivel_ofimatica")]:
        s.line(x, 285, x, 305, MUTED, 2)
        s.box(x - 90, 305, 180, 50, t, BLUE_D, BLUE, 14, "#fff", True, 2)
        w = tw(a, 12.5) + 30
        s.line(x, 355, x, 372 - 0, MUTED, 1.6)
        s.ellipse(x, 389, a, rx=w / 2, ry=17, size=12.5)
    s.save()


ALL = {f.__name__: f for f in [acid, sgbd_overview, timeline, file_access, file_vs_sgbd, ansi_sparc, keys, db_arch,
                              er_components, generalization, agregacion, pava, anatomia, reglas, chen_all]}

if __name__ == "__main__":
    for n in (sys.argv[1:] or ALL):
        ALL[n]()
        print("ok", n)
