(function () {
  var itemsEl = document.getElementById('items');

  function esc(s) { return (s == null ? '' : String(s)).replace(/"/g, '&quot;'); }

  // wire an image dropbox (label.imgbox containing an <input type=file>) to show a preview
  function attachPreview(box) {
    var input = box.querySelector('input[type=file]');
    if (!input) return;
    input.addEventListener('change', function () {
      if (input.files && input.files[0]) {
        var url = URL.createObjectURL(input.files[0]);
        box.innerHTML = '<img src="' + url + '">';
        box.appendChild(input);
      }
    });
  }

  var PRODUCTS = window.__PRODUCTS__ || [];

  function prodOptions(selected) {
    var opts = '<option value="">&mdash; Custom / upload image &mdash;</option>';
    PRODUCTS.forEach(function (p) {
      opts += '<option value="' + esc(p.key) + '"' + (p.key === selected ? ' selected' : '') + '>' + esc(p.name) + '</option>';
    });
    return opts;
  }

  function itemRow(it) {
    it = it || {};
    var wrap = document.createElement('div');
    wrap.className = 'item';
    var prodField = PRODUCTS.length
      ? '<label>Use machine photo (no upload needed)</label>' +
        '<select name="item_prod" class="prodsel">' + prodOptions(it.prod) + '</select>'
      : '<input type="hidden" name="item_prod" value="">';
    wrap.innerHTML =
      '<span class="num"></span>' +
      '<button type="button" class="del">Remove</button>' +
      '<div class="top">' +
        '<label class="imgbox"><span>+ Add<br>image</span>' +
          '<input type="file" name="item_image" accept="image/*">' +
        '</label>' +
        '<div class="fields">' +
          '<label>Product name</label>' +
          '<input type="text" name="item_name" value="' + esc(it.name) + '" placeholder="Machine / product name">' +
          '<label>Description</label>' +
          '<input type="text" name="item_desc" value="' + esc(it.desc) + '" placeholder="Short description / specs">' +
          prodField +
        '</div>' +
      '</div>' +
      '<div class="row2">' +
        '<div><label>Quantity</label><input type="text" name="item_qty" value="' + esc(it.qty || '1 Set') + '"></div>' +
        '<div><label>Price (INR)</label><input type="text" name="item_price" value="' + esc(it.price) + '" placeholder="0"></div>' +
      '</div>';

    wrap.querySelector('.del').addEventListener('click', function () { wrap.remove(); renumber(); });
    var box = wrap.querySelector('.imgbox');
    var fileInput = box.querySelector('input[type=file]');
    attachPreview(box);

    // when a machine is picked, preview its permanent bundled photo (unless a file was uploaded)
    var sel = wrap.querySelector('.prodsel');
    if (sel) {
      var showProd = function () {
        if (fileInput.files && fileInput.files[0]) return;   // uploaded image wins
        if (sel.value) {
          box.innerHTML = '<img src="/prodimg/' + encodeURIComponent(sel.value) + '" alt="">';
          box.appendChild(fileInput);
        } else {
          box.innerHTML = '<span>+ Add<br>image</span>';
          box.appendChild(fileInput);
        }
      };
      sel.addEventListener('change', showProd);
      if (sel.value) showProd();
    }
    return wrap;
  }

  function renumber() {
    itemsEl.querySelectorAll('.item').forEach(function (r, i) {
      r.querySelector('.num').textContent = (i + 1);
    });
  }

  function addItem(it) { itemsEl.appendChild(itemRow(it)); renumber(); }

  (window.__ITEMS__ || [{}]).forEach(addItem);
  if (!itemsEl.children.length) addItem({});
  document.getElementById('addItem').addEventListener('click', function () { addItem({}); });

  // product-range image boxes (server-rendered) + logo preview
  document.querySelectorAll('.prodbox').forEach(attachPreview);

  var logoInput = document.getElementById('logoInput');
  var logoBox = document.getElementById('logoBox');
  if (logoInput) logoInput.addEventListener('change', function () {
    if (logoInput.files && logoInput.files[0]) {
      logoBox.innerHTML = '<img src="' + URL.createObjectURL(logoInput.files[0]) + '">';
    }
  });

  /* ============================================================
     Save draft + saved quotations (view / download / edit)
     Stored in this browser (localStorage) - survives restarts,
     needs no server/database. Uploaded photos aren't stored, but
     the bundled logo + machine photos are used automatically.
     ============================================================ */
  var form = document.getElementById('qform');
  var SAVES_KEY = 'bis_quote_saves';
  var currentId = null;

  var SINGLE = ['co_name', 'co_tag1', 'co_tag2', 'co_addr', 'co_phone', 'co_email', 'co_web', 'co_gstin',
    'bank_name', 'bank_ac', 'bank_branch', 'bank_ifsc', 'ref', 'date', 'validity',
    'cust_name', 'cust_firm', 'cust_city', 'cust_mob', 'subject', 'intro', 'note', 'specs', 'parts', 'terms'];

  function getVal(n) { var e = form.querySelector('[name="' + n + '"]'); return e ? e.value : ''; }
  function setVal(n, v) { var e = form.querySelector('[name="' + n + '"]'); if (e) e.value = (v == null ? '' : v); }
  function escHtml(s) { return (s == null ? '' : String(s)).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

  function serialize() {
    var d = { fields: {}, items: [], products: [], flatten: !!form.querySelector('[name="flatten"]:checked') };
    SINGLE.forEach(function (n) { d.fields[n] = getVal(n); });
    itemsEl.querySelectorAll('.item').forEach(function (r) {
      var g = function (n) { var e = r.querySelector('[name="' + n + '"]'); return e ? e.value : ''; };
      d.items.push({ name: g('item_name'), desc: g('item_desc'), qty: g('item_qty'), price: g('item_price'), prod: g('item_prod') });
    });
    form.querySelectorAll('.prow').forEach(function (r) {
      var k = r.querySelector('[name="prod_key"]'), nm = r.querySelector('[name="prod_name"]');
      d.products.push({ key: k ? k.value : '', name: nm ? nm.value : '' });
    });
    return d;
  }

  function populate(d) {
    if (!d) return;
    SINGLE.forEach(function (n) { if (d.fields && (n in d.fields)) setVal(n, d.fields[n]); });
    itemsEl.innerHTML = '';
    (d.items && d.items.length ? d.items : [{}]).forEach(addItem);
    renumber();
    (d.products || []).forEach(function (p) {
      var rows = [].slice.call(form.querySelectorAll('.prow'));
      for (var i = 0; i < rows.length; i++) {
        var k = rows[i].querySelector('[name="prod_key"]');
        if (k && k.value === p.key) { var nm = rows[i].querySelector('[name="prod_name"]'); if (nm) nm.value = p.name; break; }
      }
    });
    var fl = form.querySelector('[name="flatten"]'); if (fl) fl.checked = !!d.flatten;
  }

  function loadSaves() { try { return JSON.parse(localStorage.getItem(SAVES_KEY)) || []; } catch (e) { return []; } }
  function writeSaves(l) { try { localStorage.setItem(SAVES_KEY, JSON.stringify(l)); } catch (e) { alert('Browser storage is full or unavailable.'); } }

  function calcTotal(items) {
    var t = 0;
    (items || []).forEach(function (it) {
      var q = parseFloat(String(it.qty || '').replace(/[^0-9.]/g, '')) || 1;
      var p = parseFloat(String(it.price || '').replace(/[^0-9.]/g, '')) || 0;
      t += q * p;
    });
    return t;
  }

  function saveCurrent(status) {
    var data = serialize();
    var list = loadSaves();
    var id = currentId || ('q' + Date.now());
    var entry = {
      id: id, savedAt: Date.now(), status: status || 'draft',
      ref: data.fields.ref || '', firm: data.fields.cust_firm || data.fields.cust_name || '',
      total: calcTotal(data.items), data: data
    };
    var i = -1; for (var k = 0; k < list.length; k++) { if (list[k].id === id) { i = k; break; } }
    if (i >= 0) list[i] = entry; else list.push(entry);
    writeSaves(list); currentId = id; updateCount();
    return entry;
  }

  function fmtWhen(ts) {
    var d = new Date(ts);
    return d.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: '2-digit' }) +
      ' ' + d.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
  }
  function fmtMoney(n) { return '\u20B9' + (Math.round(n) || 0).toLocaleString('en-IN'); }

  function submitTo(action, target) {
    var oa = form.getAttribute('action'), ot = form.getAttribute('target');
    form.setAttribute('action', action);
    if (target) form.setAttribute('target', target); else form.removeAttribute('target');
    form.submit();
    form.setAttribute('action', oa || '/generate');
    if (ot) form.setAttribute('target', ot); else form.removeAttribute('target');
  }

  function renderList() {
    var list = loadSaves().slice().sort(function (a, b) { return b.savedAt - a.savedAt; });
    var host = document.getElementById('savedList');
    if (!list.length) { host.innerHTML = '<p class="hint" style="padding:18px 16px">No saved quotations yet. Click <b>Save draft</b>, or download a quotation and it will appear here.</p>'; return; }
    host.innerHTML = '';
    list.forEach(function (e) {
      var row = document.createElement('div'); row.className = 'sq';
      row.innerHTML =
        '<div class="sq-info"><b>' + (e.ref ? escHtml(e.ref) : '(no ref)') + '</b>' +
        '<span>' + escHtml(e.firm || '\u2014') + '</span>' +
        '<small>' + fmtWhen(e.savedAt) + (e.status === 'generated' ? ' \u00b7 downloaded' : ' \u00b7 draft') +
        (e.total ? (' \u00b7 ' + fmtMoney(e.total)) : '') + '</small></div>' +
        '<div class="sq-act">' +
        '<button data-a="edit" class="btn small">Edit</button>' +
        '<button data-a="view" class="btn ghost sm">View</button>' +
        '<button data-a="dl" class="btn ghost sm">Download</button>' +
        '<button data-a="del" class="btn ghost sm danger">Delete</button>' +
        '</div>';
      row.querySelector('[data-a=edit]').onclick = function () { currentId = e.id; populate(e.data); closeDrawer(); window.scrollTo({ top: 0, behavior: 'smooth' }); toast('Loaded for editing'); };
      row.querySelector('[data-a=view]').onclick = function () { currentId = e.id; populate(e.data); submitTo('/preview', '_blank'); };
      row.querySelector('[data-a=dl]').onclick = function () { currentId = e.id; populate(e.data); saveCurrent('generated'); submitTo('/generate', ''); };
      row.querySelector('[data-a=del]').onclick = function () {
        if (!confirm('Delete this saved quotation?')) return;
        writeSaves(loadSaves().filter(function (x) { return x.id !== e.id; }));
        renderList(); updateCount();
      };
      host.appendChild(row);
    });
  }

  var drawer = document.getElementById('savedDrawer');
  function openDrawer() { renderList(); drawer.hidden = false; }
  function closeDrawer() { drawer.hidden = true; }
  function updateCount() { var b = document.getElementById('btnSaved'); if (b) b.textContent = 'Saved (' + loadSaves().length + ')'; }

  document.getElementById('btnSaved').addEventListener('click', openDrawer);
  document.getElementById('drawerClose').addEventListener('click', closeDrawer);
  drawer.querySelector('.drawer-bg').addEventListener('click', closeDrawer);
  document.getElementById('btnSaveDraft').addEventListener('click', function () { saveCurrent('draft'); toast('Draft saved'); });

  document.getElementById('btnNewQuote').addEventListener('click', function () {
    if (confirm('Start a new blank quotation? Unsaved changes to the current one will be lost.')) location.reload();
  });
  document.getElementById('btnExportAll').addEventListener('click', function () {
    var blob = new Blob([JSON.stringify(loadSaves(), null, 2)], { type: 'application/json' });
    var a = document.createElement('a'); a.href = URL.createObjectURL(blob);
    a.download = 'bharat-quotations-backup.json'; document.body.appendChild(a); a.click(); a.remove();
  });
  var imp = document.getElementById('importFile');
  if (imp) imp.addEventListener('change', function () {
    var f = imp.files[0]; if (!f) return;
    var rd = new FileReader();
    rd.onload = function () {
      try {
        var arr = JSON.parse(rd.result); if (!Array.isArray(arr)) throw 0;
        var map = {}; loadSaves().forEach(function (e) { map[e.id] = e; });
        arr.forEach(function (e) { if (e && e.id) map[e.id] = e; });
        writeSaves(Object.keys(map).map(function (k) { return map[k]; }));
        renderList(); updateCount(); toast('Backup imported');
      } catch (e) { alert('That does not look like a valid backup file.'); }
    };
    rd.readAsText(f); imp.value = '';
  });

  // remember every downloaded quotation automatically
  document.querySelectorAll('button[formaction="/generate"]').forEach(function (b) {
    b.addEventListener('click', function () { saveCurrent('generated'); });
  });

  function toast(msg) {
    var t = document.createElement('div'); t.className = 'toast'; t.textContent = msg;
    document.body.appendChild(t);
    (window.requestAnimationFrame || function (f) { setTimeout(f, 16); })(function () { t.classList.add('show'); });
    setTimeout(function () { t.classList.remove('show'); setTimeout(function () { t.remove(); }, 250); }, 2200);
  }

  updateCount();
})();
