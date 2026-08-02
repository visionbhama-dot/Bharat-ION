/* Bharat iON Systems - Admin shared helpers, soft auth gate, sidebar, toast */
(function () {
  'use strict';
  var CFG = window.ADMIN_CONFIG || {};
  window.ADMIN = window.ADMIN || {};

  /* ---------- tiny DOM helpers ---------- */
  function el(tag, attrs, children) {
    var e = document.createElement(tag);
    attrs = attrs || {};
    Object.keys(attrs).forEach(function (k) {
      if (k === 'class') e.className = attrs[k];
      else if (k === 'html') e.innerHTML = attrs[k];
      else if (k === 'text') e.textContent = attrs[k];
      else if (k.slice(0, 2) === 'on' && typeof attrs[k] === 'function') e.addEventListener(k.slice(2), attrs[k]);
      else if (attrs[k] != null) e.setAttribute(k, attrs[k]);
    });
    (children || []).forEach(function (c) { if (c != null) e.appendChild(typeof c === 'string' ? document.createTextNode(c) : c); });
    return e;
  }
  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }
  function money(n) {
    var sym = (CFG.quotation && CFG.quotation.currencySymbol) || '\u20B9';
    var v = (Number(n) || 0).toFixed(2);
    // Indian grouping
    var parts = v.split('.');
    var x = parts[0];
    var last3 = x.length > 3 ? x.slice(-3) : x;
    var other = x.length > 3 ? x.slice(0, -3) : '';
    if (other) last3 = ',' + last3;
    other = other.replace(/\B(?=(\d{2})+(?!\d))/g, ',');
    return sym + other + last3 + '.' + parts[1];
  }

  /* ---------- toast ---------- */
  function toast(msg, kind) {
    var t = el('div', { class: 'toast ' + (kind || ''), text: msg });
    document.body.appendChild(t);
    requestAnimationFrame(function () { t.classList.add('show'); });
    setTimeout(function () { t.classList.remove('show'); setTimeout(function () { t.remove(); }, 300); }, 2600);
  }

  /* ---------- localStorage store ---------- */
  var store = {
    get: function (k, def) { try { var v = localStorage.getItem('bis_' + k); return v == null ? def : JSON.parse(v); } catch (e) { return def; } },
    set: function (k, v) { try { localStorage.setItem('bis_' + k, JSON.stringify(v)); } catch (e) {} },
    del: function (k) { try { localStorage.removeItem('bis_' + k); } catch (e) {} }
  };

  /* ---------- optional backend ---------- */
  function apiPost(path, body, isForm) {
    var base = CFG.apiBaseUrl || '';
    if (!base) return Promise.reject(new Error('no-api'));
    return fetch(base.replace(/\/$/, '') + path, {
      method: 'POST',
      headers: isForm ? undefined : { 'Content-Type': 'application/json' },
      body: isForm ? body : JSON.stringify(body)
    }).then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json().catch(function () { return {}; }); });
  }

  /* ---------- download helper ---------- */
  function download(filename, text, mime) {
    var blob = new Blob([text], { type: mime || 'text/plain;charset=utf-8' });
    var url = URL.createObjectURL(blob);
    var a = el('a', { href: url, download: filename });
    document.body.appendChild(a); a.click();
    setTimeout(function () { a.remove(); URL.revokeObjectURL(url); }, 100);
  }
  function copy(text) {
    if (navigator.clipboard) { navigator.clipboard.writeText(text).then(function () { toast('Copied to clipboard', 'ok'); }); }
    else { toast('Copy not supported', 'err'); }
  }

  /* ---------- soft auth gate ---------- */
  function gate() {
    var pass = CFG.auth && CFG.auth.passcode;
    if (!pass) return;                     // gate disabled
    if (store.get('auth_ok') === true) return;
    var g = el('div', { class: 'gate' });
    var input = el('input', { type: 'password', placeholder: 'Enter passcode', style: 'margin-bottom:14px' });
    var btn = el('button', { class: 'btn btn-primary', style: 'width:100%', text: 'Enter' });
    function tryLogin() {
      if (input.value === pass) { store.set('auth_ok', true); g.remove(); }
      else { input.value = ''; input.style.borderColor = 'var(--red)'; toast('Wrong passcode', 'err'); }
    }
    btn.addEventListener('click', tryLogin);
    input.addEventListener('keydown', function (e) { if (e.key === 'Enter') tryLogin(); });
    g.appendChild(el('div', { class: 'box' }, [
      el('h2', { text: 'Admin Access' }),
      el('p', { text: 'This is a lightweight client-side gate. For real security, use your backend authentication.' }),
      input, btn
    ]));
    document.body.appendChild(g);
    setTimeout(function () { input.focus(); }, 50);
  }
  function logout() { store.del('auth_ok'); location.reload(); }

  /* ---------- sidebar (rendered into [data-sidebar]) ---------- */
  var NAV = [
    { href: 'index.html', label: 'Dashboard', icon: 'M3 12l9-8 9 8M5 10v9h5v-6h4v6h5v-9' },
    { href: 'quotation.html', label: 'Quotation Maker', icon: 'M7 3h7l5 5v13H7zM14 3v5h5M9 13h6M9 17h6' },
    { href: 'blog.html', label: 'Blog Composer', icon: 'M4 5h16v14H4zM4 9h16M8 13h8M8 16h5' },
    { href: 'images.html', label: 'Image Manager', icon: 'M4 5h16v14H4zM8 11l3 3 3-4 4 5H4z' }
  ];
  function renderSidebar() {
    var host = document.querySelector('[data-sidebar]');
    if (!host) return;
    var current = (location.pathname.split('/').pop() || 'index.html');
    var co = CFG.company || {};
    var links = NAV.map(function (n) {
      return el('a', { href: n.href, class: current === n.href ? 'active' : '' }, [
        svg(n.icon), document.createTextNode(n.label)
      ]);
    });
    host.className = 'sidebar';
    host.innerHTML = '';
    host.appendChild(el('div', { class: 'brand' }, [
      el('div', {}, [
        el('b', { html: 'BHARAT <i>iON</i>' }),
        el('small', { text: 'Admin Panel' })
      ])
    ]));
    var nav = el('nav', {}, links);
    host.appendChild(nav);
    host.appendChild(el('div', { class: 'side-foot' }, [
      el('a', { href: '../index.html', target: '_blank', text: 'View website \u2197' }),
      el('br'), el('br'),
      el('a', { href: '#', onclick: function (e) { e.preventDefault(); logout(); }, text: 'Log out' }),
      el('br'), el('br'),
      el('span', { html: 'by <a href="https://www.bhamavision.com" target="_blank" rel="noopener">Bhama Vision</a>' })
    ]));
  }
  function svg(path) {
    var s = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    s.setAttribute('viewBox', '0 0 24 24'); s.setAttribute('fill', 'none');
    var p = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    p.setAttribute('d', path); p.setAttribute('stroke', 'currentColor');
    p.setAttribute('stroke-width', '1.8'); p.setAttribute('stroke-linecap', 'round'); p.setAttribute('stroke-linejoin', 'round');
    s.appendChild(p); return s;
  }

  function topbarMenuToggle() {
    var t = document.querySelector('.menu-toggle');
    var sb = document.querySelector('[data-sidebar]');
    if (t && sb) t.addEventListener('click', function () { sb.classList.toggle('open'); });
  }

  document.addEventListener('DOMContentLoaded', function () {
    gate(); renderSidebar(); topbarMenuToggle();
  });

  /* expose */
  window.ADMIN = {
    el: el, esc: esc, money: money, toast: toast, store: store,
    apiPost: apiPost, download: download, copy: copy, cfg: CFG, logout: logout
  };
})();
