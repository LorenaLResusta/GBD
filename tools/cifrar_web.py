#!/usr/bin/env python3
"""Cifra con una contraseña todas las páginas HTML de un sitio ya compilado.

Uso:  WEB_CLAVE='...' python3 tools/cifrar_web.py public

Cada .html se sustituye por una página con un formulario de contraseña que lleva
el original cifrado (AES-256-GCM, clave derivada con PBKDF2-SHA256). El descifrado
se hace en el navegador con Web Crypto, así que funciona en GitHub Pages.
También se vacían el índice de búsqueda y los .xml, que contienen el texto en claro.
Requiere el paquete `cryptography` (pip install cryptography).
"""
import base64, os, pathlib, sys
from hashlib import pbkdf2_hmac
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ITER = 200_000
PLANTILLA = """<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Acceso protegido</title>
<style>
:root{color-scheme:light dark}
body{font-family:system-ui,sans-serif;display:grid;place-items:center;min-height:100vh;margin:0}
form{display:grid;gap:.75rem;width:min(22rem,90vw);padding:1.5rem;border:1px solid #8886;border-radius:.6rem}
input,button{font:inherit;padding:.55rem .7rem;border-radius:.4rem;border:1px solid #8888}
button{cursor:pointer;font-weight:600}
#msg{min-height:1.2em;color:#c0392b;font-size:.9rem;margin:0}
</style></head><body>
<form id="f"><h1 style="font-size:1.2rem;margin:0">Acceso protegido</h1>
<input id="p" type="password" placeholder="Contraseña" autocomplete="current-password" autofocus required>
<button>Entrar</button><p id="msg" role="alert"></p></form>
<script>
const S="__SAL__",I="__IV__",C="__DATOS__",N=__ITER__;
const b=s=>Uint8Array.from(atob(s),c=>c.charCodeAt(0));
async function abrir(pw){
  const t=new TextEncoder();
  const k0=await crypto.subtle.importKey("raw",t.encode(pw),"PBKDF2",false,["deriveKey"]);
  const k=await crypto.subtle.deriveKey({name:"PBKDF2",salt:b(S),iterations:N,hash:"SHA-256"},k0,{name:"AES-GCM",length:256},false,["decrypt"]);
  const pt=await crypto.subtle.decrypt({name:"AES-GCM",iv:b(I)},k,b(C));
  const h=location.hash;
  document.open();document.write(new TextDecoder().decode(pt));document.close();
  if(h)setTimeout(()=>{const e=document.getElementById(decodeURIComponent(h.slice(1)));if(e)e.scrollIntoView()},300);
}
const KEY="web-clave";
function guardar(pw){try{sessionStorage.setItem(KEY,pw)}catch(e){}}
function leer(){try{return sessionStorage.getItem(KEY)}catch(e){return null}}
document.getElementById("f").addEventListener("submit",async e=>{
  e.preventDefault();const pw=document.getElementById("p").value;
  try{await abrir(pw);guardar(pw)}catch(x){document.getElementById("msg").textContent="Contraseña incorrecta."}
});
(async()=>{const pw=leer();if(pw){try{await abrir(pw)}catch(e){try{sessionStorage.removeItem(KEY)}catch(x){}}}})();
</script></body></html>
"""

def main():
    raiz = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "public")
    clave = os.environ.get("WEB_CLAVE", "")
    if not clave:
        sys.exit("Falta la contraseña: define la variable de entorno WEB_CLAVE")
    n = 0
    for f in raiz.rglob("*.html"):
        sal, iv = os.urandom(16), os.urandom(12)
        k = pbkdf2_hmac("sha256", clave.encode(), sal, ITER, 32)
        ct = AESGCM(k).encrypt(iv, f.read_bytes(), None)
        b64 = lambda x: base64.b64encode(x).decode()
        f.write_text(PLANTILLA.replace("__SAL__", b64(sal)).replace("__IV__", b64(iv))
                     .replace("__DATOS__", b64(ct)).replace("__ITER__", str(ITER)), encoding="utf-8")
        n += 1
    for f in raiz.rglob("*.search-data.min.*.json"):
        f.write_text("{}")
    for f in raiz.rglob("*.xml"):
        f.unlink()
    (raiz / "robots.txt").write_text("User-agent: *\nDisallow: /\n")
    print(f"{n} páginas cifradas")

main()
