/* Bharat iON Systems - Quotation Maker */
(function () {
  'use strict';
  var A = window.ADMIN, CFG = A.cfg;
  var Q = (CFG.quotation) || {};
  var CO = (CFG.company) || {};
  var $ = function (id) { return document.getElementById(id); };
  var currentId = null;

  function todayISO(offsetDays) {
    var d = new Date(); if (offsetDays) d.setDate(d.getDate() + offsetDays);
    return d.toISOString().slice(0, 10);
  }
  function fmtDate(iso) {
    if (!iso) return '';
    var d = new Date(iso + 'T00:00:00');
    if (isNaN(d)) return iso;
    return d.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
  }
  function nextNumber() {
    var n = (A.store.get('quote_counter', 0) || 0) + 1;
    var yr = new Date().getFullYear();
    return (Q.prefix || 'BIS') + '-' + yr + '-' + String(n).padStart(4, '0');
  }

  /* ---------- line items ---------- */
  function addRow(item) {
    item = item || {};
    var body = $('itemsBody');
    var tr = A.el('tr', { class: 'line-row' });
    var desc = A.el('input', { value: item.desc || '', placeholder: 'Item description' });
    var qty = A.el('input', { type: 'number', min: '0', step: '1', value: item.qty != null ? item.qty : 1 });
    var price = A.el('input', { type: 'number', min: '0', step: '0.01', value: item.price != null ? item.price : '' });
    var disc = A.el('input', { type: 'number', min: '0', max: '100', step: '0.01', value: item.disc != null ? item.disc : 0 });
    var amt = A.el('td', { class: 't-right', text: A.money(0) });
    var del = A.el('button', { class: 'btn btn-sm btn-ghost', title: 'Remove', text: '\u2715', onclick: function () { tr.remove(); recalc(); } });
    [qty, price, disc].forEach(function (inp) { inp.addEventListener('input', recalc); });
    desc.addEventListener('input', function () {});
    tr.appendChild(A.el('td', {}, [desc]));
    tr.appendChild(A.el('td', {}, [qty]));
    tr.appendChild(A.el('td', {}, [price]));
    tr.appendChild(A.el('td', {}, [disc]));
    tr.appendChild(amt);
    tr.appendChild(A.el('td', {}, [del]));
    tr._get = function () {
      return { desc: desc.value, qty: +qty.value || 0, price: +price.value || 0, disc: +disc.value || 0 };
    };
    tr._amtCell = amt;
    body.appendChild(tr);
    recalc();
  }

  function rowAmount(r) { return r.qty * r.price * (1 - (r.disc || 0) / 100); }

  function recalc() {
    var sub = 0;
    Array.prototype.forEach.call($('itemsBody').children, function (tr) {
      var r = tr._get(); var a = rowAmount(r); sub += a;
      tr._amtCell.textContent = A.money(a);
    });
    var gstp = +$('q_gst').value || 0;
    var gst = sub * gstp / 100;
    $('t_sub').textContent = A.money(sub);
    $('t_gstp').textContent = gstp;
    $('t_gst').textContent = A.money(gst);
    $('t_grand').textContent = A.money(sub + gst);
    return { sub: sub, gst: gst, gstp: gstp, total: sub + gst };
  }

  /* ---------- gather / fill ---------- */
  function gather() {
    var items = Array.prototype.map.call($('itemsBody').children, function (tr) { return tr._get(); })
      .filter(function (r) { return r.desc || r.price; });
    var t = recalc();
    return {
      id: currentId || ('q_' + Date.now()),
      number: $('q_number').value || nextNumber(),
      date: $('q_date').value, valid: $('q_valid').value,
      customer: {
        name: $('c_name').value, company: $('c_company').value, phone: $('c_phone').value,
        email: $('c_email').value, city: $('c_city').value, address: $('c_address').value
      },
      items: items, notes: $('q_notes').value, terms: $('q_terms').value,
      gstPercent: t.gstp, subtotal: t.sub, gst: t.gst, total: t.total
    };
  }
  function fill(q) {
    currentId = q.id || null;
    $('q_number').value = q.number || '';
    $('q_date').value = q.date || todayISO();
    $('q_valid').value = q.valid || todayISO(Q.validityDays || 15);
    var c = q.customer || {};
    $('c_name').value = c.name || ''; $('c_company').value = c.company || '';
    $('c_phone').value = c.phone || ''; $('c_email').value = c.email || '';
    $('c_city').value = c.city || ''; $('c_address').value = c.address || '';
    $('q_notes').value = q.notes || '';
    $('q_gst').value = q.gstPercent != null ? q.gstPercent : (Q.gstPercent != null ? Q.gstPercent : 18);
    $('q_terms').value = q.terms || Q.terms || '';
    $('itemsBody').innerHTML = '';
    (q.items && q.items.length ? q.items : [{}]).forEach(addRow);
    recalc();
  }

  /* ---------- save / export ---------- */
  function save(silent) {
    var q = gather();
    if (!q.customer.name) { A.toast('Enter a customer name first', 'err'); return null; }
    var list = A.store.get('quotes', []);
    var idx = list.findIndex(function (x) { return x.id === q.id; });
    if (idx >= 0) list[idx] = q; else {
      list.push(q);
      // bump counter only for a brand-new auto number
      var c = A.store.get('quote_counter', 0) || 0;
      if ($('q_number').value === '' || $('q_number').value === q.number) A.store.set('quote_counter', c + 1);
    }
    A.store.set('quotes', list);
    currentId = q.id;
    $('q_number').value = q.number;
    if (!silent) A.toast('Quotation saved', 'ok');
    if (CFG.apiBaseUrl) {
      A.apiPost('/quotations', q).then(function () { A.toast('Synced to backend', 'ok'); })
        .catch(function () { /* offline is fine */ });
    }
    return q;
  }

  /* ---------- printable preview ---------- */
  function previewHTML(q) {
    var co = CO;
    var rows = q.items.map(function (r) {
      return '<tr><td>' + A.esc(r.desc) + '</td><td class="c">' + r.qty +
        '</td><td class="r">' + A.money(r.price) + '</td><td class="c">' + (r.disc || 0) +
        '%</td><td class="r">' + A.money(rowAmount(r)) + '</td></tr>';
    }).join('');
    var gstin = co.gstin ? '<div>GSTIN: ' + A.esc(co.gstin) + '</div>' : '';
    return '' +
      '<div class="q-doc">' +
      '<div class="no-print" style="margin-bottom:16px;display:flex;gap:10px">' +
      '<button class="btn btn-primary" onclick="window.print()">\uD83D\uDDA8 Print / Save as PDF</button>' +
      '<button class="btn btn-ghost" id="btnClosePrev">Close preview</button></div>' +
      '<div class="q-head">' +
      '<div class="q-co"><img src="' + A.esc(co.logoPath) + '" alt="" onerror="this.style.display=\'none\'" class="q-logo">' +
      '<div class="q-coname">' + A.esc(co.name) + '</div>' +
      '<div class="q-cometa">' + A.esc(co.tagline || '') + '<br>' + A.esc(co.address || '') +
      '<br>' + A.esc(co.phone || '') + ' &middot; ' + A.esc(co.email || '') + gstin + '</div></div>' +
      '<div class="q-title"><h2>QUOTATION</h2>' +
      '<table class="q-meta"><tr><td>Quote #</td><td><b>' + A.esc(q.number) + '</b></td></tr>' +
      '<tr><td>Date</td><td>' + fmtDate(q.date) + '</td></tr>' +
      '<tr><td>Valid until</td><td>' + fmtDate(q.valid) + '</td></tr></table></div>' +
      '</div>' +
      '<div class="q-to"><span>Quotation for</span><b>' + A.esc(q.customer.company || q.customer.name) + '</b>' +
      (q.customer.company && q.customer.name ? '<div>Attn: ' + A.esc(q.customer.name) + '</div>' : '') +
      (q.customer.address ? '<div>' + A.esc(q.customer.address) + '</div>' : '') +
      (q.customer.city ? '<div>' + A.esc(q.customer.city) + '</div>' : '') +
      '<div>' + [q.customer.phone, q.customer.email].filter(Boolean).map(A.esc).join(' &middot; ') + '</div></div>' +
      '<table class="q-items"><thead><tr><th>Description</th><th class="c">Qty</th><th class="r">Unit price</th><th class="c">Disc</th><th class="r">Amount</th></tr></thead>' +
      '<tbody>' + rows + '</tbody></table>' +
      '<div class="q-tot"><table>' +
      '<tr><td>Subtotal</td><td class="r">' + A.money(q.subtotal) + '</td></tr>' +
      '<tr><td>GST (' + q.gstPercent + '%)</td><td class="r">' + A.money(q.gst) + '</td></tr>' +
      '<tr class="g"><td>Grand Total</td><td class="r">' + A.money(q.total) + '</td></tr></table></div>' +
      (q.notes ? '<div class="q-notes"><b>Notes:</b> ' + A.esc(q.notes) + '</div>' : '') +
      (q.terms ? '<div class="q-terms"><b>Terms &amp; Conditions</b><br>' + A.esc(q.terms) + '</div>' : '') +
      '<div class="q-foot">This is a computer-generated quotation. &nbsp;|&nbsp; ' + A.esc(co.website || '') +
      '<br>Designed &amp; Developed by Bhama Vision (www.bhamavision.com)</div>' +
      '</div>';
  }

  function preview() {
    var q = save(true); if (!q) return;
    var box = $('quotePreview');
    box.innerHTML = previewHTML(q);
    box.style.display = 'block';
    var close = document.getElementById('btnClosePrev');
    if (close) close.addEventListener('click', function () { box.style.display = 'none'; });
    box.scrollIntoView({ behavior: 'smooth' });
  }

  /* ---------- init ---------- */
  document.addEventListener('DOMContentLoaded', function () {
    // quote-app launcher
    var qa = (CFG.quoteApp) || {};
    var qaUrl = qa.url || '';
    var lbl = $('quoteAppUrlLbl'), hint = $('quoteAppHint'), launch = $('btnLaunchQuoteApp');
    if (lbl) lbl.textContent = qaUrl ? ('Opens: ' + qaUrl) : '';
    if (hint) hint.innerHTML = 'Not opening? The generator must be running first. ' +
      A.esc(qa.startHint || '') + ' You can change its address in <code>admin/config.js</code>.';
    if (launch) launch.addEventListener('click', function () {
      if (!qaUrl) { A.toast('Set quoteApp.url in config.js', 'err'); return; }
      window.open(qaUrl, '_blank', 'noopener');
    });

    // product dropdown
    var pick = $('prodPick');
    (CFG.products || []).forEach(function (p) { pick.appendChild(A.el('option', { value: p.slug, text: p.name })); });
    $('btnAddProd').addEventListener('click', function () {
      var slug = pick.value; if (!slug) { A.toast('Pick a machine first'); return; }
      var p = (CFG.products || []).find(function (x) { return x.slug === slug; });
      addRow({ desc: p ? p.name : slug, qty: 1, price: '', disc: 0 });
    });
    $('btnAddCustom').addEventListener('click', function () { addRow({}); });
    $('q_gst').addEventListener('input', recalc);

    ['btnPreview', 'btnPreview2'].forEach(function (id) { $(id).addEventListener('click', preview); });
    ['btnSave', 'btnSave2'].forEach(function (id) { $(id).addEventListener('click', function () { save(false); }); });
    $('btnExport').addEventListener('click', function () {
      var q = gather(); A.download('quotation-' + (q.number || 'draft') + '.json', JSON.stringify(q, null, 2), 'application/json');
    });
    $('btnNew').addEventListener('click', function () {
      if (!confirm('Start a new blank quotation?')) return;
      currentId = null; history.replaceState(null, '', 'quotation.html');
      fill({ number: nextNumber(), date: todayISO(), valid: todayISO(Q.validityDays || 15) });
    });
    if (CFG.apiBaseUrl) {
      var b = $('btnApi'); b.style.display = 'inline-flex';
      b.addEventListener('click', function () {
        var q = gather(); A.apiPost('/quotations', q)
          .then(function () { A.toast('Sent to backend', 'ok'); })
          .catch(function () { A.toast('Backend error', 'err'); });
      });
    }

    // load existing by ?id= or start fresh
    var id = new URLSearchParams(location.search).get('id');
    var existing = id && (A.store.get('quotes', []).find(function (x) { return x.id === id; }));
    if (existing) fill(existing);
    else fill({ number: nextNumber(), date: todayISO(), valid: todayISO(Q.validityDays || 15) });
  });
})();
