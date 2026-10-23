#!/usr/bin/env python3
"""Protección de soluciones.

  separar   Saca las soluciones de las páginas de prácticas (content.*/**/*-practicas.md):
            - deja en el contenido público solo un candado  {{< solucion id=".." title=".." >}}
            - guarda el texto completo en privado/content.*  (carpeta que NO se sube al repositorio)
  cifrar    Construye el sitio con las soluciones en claro (copia temporal), extrae el HTML de cada
            solución y lo cifra con AES-256-GCM (clave derivada con PBKDF2-SHA256 de tu contraseña)
            en static/soluciones/<idioma>/<id>.json. Lo único público es el texto cifrado.

Uso:
  python3 tools/soluciones.py separar
  BD_CLAVE='tu clave larga' python3 tools/soluciones.py cifrar [--hugo ruta/a/hugo]
"""
import argparse, base64, glob, gzip, hashlib, json, os, re, shutil, subprocess, sys, tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRIV = os.path.join(RAIZ, 'privado')
ITER = 250_000
TITULOS = re.compile(
    r'^(Soluci[óo]n?|Soluciones|Solucions|Respuestas guiadas|Respostes guiades|Ver el diagrama de la soluci[óo]n?|'
    r'Veure el diagrama de la soluci[óo]|Preguntas al cliente y decisiones|Preguntes al client i decisions|'
    r'Resultados esperados|Resultats esperats|Resultados reales y explicaci[óo]n|Resultats reals i explicaci[óo]|'
    r'Diagrama relacional resultante|Diagrama relacional resultant)')
ABRE = re.compile(r'^\{\{% details title="([^"]*)"[^}]*%\}\}\s*$')
CIERRA = re.compile(r'^\{\{% /details %\}\}\s*$')


def separar():
    total = {}
    for lang in ('es', 'val'):
        for f in sorted(glob.glob(os.path.join(RAIZ, f'content.{lang}', '*', '*-practicas.md'))):
            rel = os.path.relpath(f, os.path.join(RAIZ, f'content.{lang}'))
            ud = rel.split('-')[0]
            L = open(f, encoding='utf-8').read().split('\n')
            pub, priv, pila, n, i = [], [], [], 0, 0
            while i < len(L):
                l = L[i]
                m = ABRE.match(l.strip())
                if m and TITULOS.match(m.group(1)):
                    titulo = m.group(1)
                    j, prof = i + 1, 1
                    while j < len(L):
                        s = L[j].strip()
                        if ABRE.match(s): prof += 1
                        elif CIERRA.match(s):
                            prof -= 1
                            if prof == 0: break
                        j += 1
                    assert j < len(L), (f, i)
                    n += 1
                    sid = f'{ud}-{n:03d}'
                    t = titulo.replace('"', "'")
                    priv.append(f'{{{{% solucion id="{sid}" title="{t}" %}}}}')
                    priv.extend(L[i + 1:j])
                    priv.append('{{% /solucion %}}')
                    pub.append(f'{{{{< solucion id="{sid}" title="{t}" />}}}}')
                    i = j + 1
                    continue
                pub.append(l); priv.append(l); i += 1
            if n:
                d = os.path.join(PRIV, f'content.{lang}', os.path.dirname(rel)); os.makedirs(d, exist_ok=True)
                open(os.path.join(PRIV, f'content.{lang}', rel), 'w', encoding='utf-8').write('\n'.join(priv))
                open(f, 'w', encoding='utf-8').write('\n'.join(pub))
                total[(lang, rel)] = n
    for k, v in total.items(): print(k, v)
    print('total', sum(total.values()))


def cifrar(hugo):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    clave = os.environ.get('BD_CLAVE')
    if not clave: sys.exit('Define la clave en la variable de entorno BD_CLAVE')
    tmp = tempfile.mkdtemp(prefix='bd_priv_')
    sitio = os.path.join(tmp, 'sitio')
    shutil.copytree(RAIZ, sitio, ignore=shutil.ignore_patterns('privado', 'public', 'resources', '.git', '_gen', 'static'), symlinks=True)
    shutil.copytree(os.path.join(RAIZ, 'static'), os.path.join(sitio, 'static'), dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('soluciones'))
    shutil.copytree(PRIV, sitio, dirs_exist_ok=True, ignore=shutil.ignore_patterns('tools'))
    sal = os.path.join(tmp, 'pub')
    r = subprocess.run([hugo, '-d', sal], cwd=sitio, capture_output=True, text=True)
    if r.returncode: sys.exit(r.stderr[-2000:])
    destino = os.path.join(RAIZ, 'static', 'soluciones')
    shutil.rmtree(destino, ignore_errors=True)
    patron = re.compile(r'<div hidden data-sol-start="([\w-]+)"></div>(.*?)<div hidden data-sol-end="\1"></div>', re.S)
    cuerpo = re.compile(r'<details class="sol-plain">.*?<div class="markdown-inner">(.*)</div>\s*</details>', re.S)
    cont = {'es': 0, 'val': 0}
    for ruta in glob.glob(os.path.join(sal, '**', 'index.html'), recursive=True):
        html = open(ruta, encoding='utf-8').read()
        if 'data-sol-start' not in html: continue
        lang = 'val' if os.path.relpath(ruta, sal).startswith('val' + os.sep) else 'es'
        for sid, bloque in patron.findall(html):
            m = cuerpo.search(bloque); assert m, sid
            inner = m.group(1)
            inner = incrustar(inner, sal)
            salt, iv = os.urandom(16), os.urandom(12)
            k = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER).derive(clave.encode())
            ct = AESGCM(k).encrypt(iv, gzip.compress(inner.encode('utf-8'), 9, mtime=0), None)
            d = os.path.join(destino, lang); os.makedirs(d, exist_ok=True)
            json.dump({'v': 1, 'n': ITER, 's': b64(salt), 'i': b64(iv), 'c': b64(ct)}, open(os.path.join(d, sid + '.json'), 'w'))
            cont[lang] += 1
    shutil.rmtree(tmp, ignore_errors=True)
    print('cifradas:', cont)


def b64(b): return base64.b64encode(b).decode()


def incrustar(html, sal):
    """Imágenes locales -> data URI, y el enlace «ampliar» -> clase para que el JS cree un blob."""
    mimes = {'.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.webp': 'image/webp'}
    def img(m):
        src = m.group(1)
        p = os.path.join(sal, re.sub(r'^/BBDD/', '', src).lstrip('/'))
        if not os.path.exists(p): return m.group(0)
        mt = mimes.get(os.path.splitext(p)[1].lower(), 'application/octet-stream')
        return f'<img src="data:{mt};base64,{b64(open(p, "rb").read())}"'
    html = re.sub(r'<img src="(/[^"]+)"', img, html)
    html = re.sub(r'<a href="/[^"]+\.(?:svg|png|jpg|jpeg|gif|webp)"( target="_blank")?', '<a class="sol-zoom" href="#"\\1', html)
    return html


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('orden', choices=['separar', 'cifrar'])
    ap.add_argument('--hugo', default='hugo')
    a = ap.parse_args()
    separar() if a.orden == 'separar' else cifrar(a.hugo)
