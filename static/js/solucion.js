/* Descifrado en el navegador de las soluciones (AES-GCM + PBKDF2-SHA256, contenido comprimido con gzip). */
(function () {
  'use strict';
  var KEY = 'bd-sol-pw';
  function b64(s) { var b = atob(s), a = new Uint8Array(b.length); for (var i = 0; i < b.length; i++) a[i] = b.charCodeAt(i); return a; }
  function getPw() { try { return sessionStorage.getItem(KEY) || ''; } catch (e) { return ''; } }
  function setPw(p) { try { sessionStorage.setItem(KEY, p); } catch (e) {} }
  async function descifrar(data, pw) {
    var enc = new TextEncoder();
    var base = await crypto.subtle.importKey('raw', enc.encode(pw), 'PBKDF2', false, ['deriveKey']);
    var key = await crypto.subtle.deriveKey({ name: 'PBKDF2', salt: b64(data.s), iterations: data.n, hash: 'SHA-256' }, base, { name: 'AES-GCM', length: 256 }, false, ['decrypt']);
    var plain = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: b64(data.i) }, key, b64(data.c));
    var stream = new Blob([plain]).stream().pipeThrough(new DecompressionStream('gzip'));
    return await new Response(stream).text();
  }
  function loadScript(src) {
    return new Promise(function (ok, ko) { var s = document.createElement('script'); s.src = src; s.onload = ok; s.onerror = ko; document.head.appendChild(s); });
  }
  async function posproceso(el, base) {
    el.querySelectorAll('a.sol-zoom').forEach(function (a) {
      var img = a.querySelector('img'); if (!img) return;
      fetch(img.src).then(function (r) { return r.blob(); }).then(function (b) { a.href = URL.createObjectURL(b); });
    });
    var mm = el.querySelectorAll('pre.mermaid');
    if (mm.length) {
      try {
        if (!window.mermaid) await loadScript(base + 'mermaid.min.js');
        window.mermaid.initialize({ startOnLoad: false });
        await window.mermaid.run({ nodes: mm });
      } catch (e) { /* si falla, queda el código del diagrama */ }
    }
  }
  async function abrir(d, pw, silent) {
    var msg = d.querySelector('.sol-msg'); msg.className = 'sol-msg'; msg.textContent = d.dataset.msgLoad;
    var r;
    try { r = await fetch(d.dataset.src, { cache: 'no-cache' }); } catch (e) { r = null; }
    if (!r || !r.ok) { msg.className = 'sol-msg ko'; msg.textContent = d.dataset.msgNone; return false; }
    var data = await r.json(), html;
    try { html = await descifrar(data, pw); }
    catch (e) { msg.className = 'sol-msg ko'; msg.textContent = silent ? '' : d.dataset.msgErr; return false; }
    var out = d.querySelector('.sol-out'); out.innerHTML = html;
    d.classList.add('sol-open'); msg.textContent = ''; setPw(pw);
    await posproceso(out, d.dataset.base);
    return true;
  }
  function init() {
    document.querySelectorAll('details.sol-lock').forEach(function (d) {
      var f = d.querySelector('.sol-form');
      f.addEventListener('submit', function (ev) { ev.preventDefault(); abrir(d, d.querySelector('.sol-pw').value, false); });
      d.addEventListener('toggle', function () {
        if (d.open && !d.classList.contains('sol-open') && getPw()) abrir(d, getPw(), true);
      });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
