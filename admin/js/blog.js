/* Bharat iON Systems - Blog Composer */
(function () {
  'use strict';
  var A = window.ADMIN, CFG = A.cfg;
  var $ = function (id) { return document.getElementById(id); };
  var currentId = null;

  function slugify(s) {
    return String(s || '').toLowerCase().trim()
      .replace(/&/g, ' and ').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 80);
  }
  function todayISO() { return new Date().toISOString().slice(0, 10); }
  function fmtDate(iso) {
    if (!iso) return '';
    var d = new Date(iso + 'T00:00:00'); if (isNaN(d)) return iso;
    return d.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
  }
  function productName(slug) {
    var p = (CFG.products || []).find(function (x) { return x.slug === slug; });
    return p ? p.name : slug;
  }

  /* ---------- textarea insert helpers ---------- */
  function insert(before, after, placeholder) {
    var ta = $('bodyInput');
    var s = ta.selectionStart, e = ta.selectionEnd;
    var sel = ta.value.slice(s, e) || placeholder || '';
    var text = before + sel + (after || '');
    ta.value = ta.value.slice(0, s) + text + ta.value.slice(e);
    ta.focus();
    ta.selectionStart = s + before.length;
    ta.selectionEnd = s + before.length + sel.length;
    render();
  }

  /* ---------- gather / render ---------- */
  function gather() {
    var related = Array.prototype.map.call(document.querySelectorAll('#relList input:checked'), function (i) { return i.value; });
    var title = $('f_title').value.trim();
    return {
      id: currentId || ('b_' + Date.now()),
      title: title,
      slug: ($('f_slug').value.trim() || slugify(title)),
      category: $('f_cat').value,
      date: $('f_date').value || todayISO(),
      read: +$('f_read').value || 6,
      desc: $('f_desc').value.trim(),
      body: $('bodyInput').value,
      related: related
    };
  }

  function render() {
    var d = gather();
    if (!$('f_slug').value) $('f_slug').placeholder = slugify($('f_title').value) || 'auto-from-title';
    $('descCount').textContent = d.desc.length + ' characters' + (d.desc.length > 160 ? ' (a bit long for Google)' : '');
    var rel = d.related.length
      ? '<div style="margin-top:16px;padding-top:12px;border-top:1px solid #eee"><b>Related machinery:</b> ' +
        d.related.map(function (s) { return '<a href="#">' + A.esc(productName(s)) + '</a>'; }).join(', ') + '</div>'
      : '';
    $('preview').innerHTML =
      (d.category ? '<span class="cat">' + A.esc(d.category) + '</span>' : '') +
      '<h1>' + (A.esc(d.title) || 'Post title') + '</h1>' +
      '<div class="meta">' + fmtDate(d.date) + ' &middot; ' + d.read + ' min read &middot; by Bharat iON Systems</div>' +
      (d.body || '<p class="muted">Start writing the body\u2026</p>') + rel;
  }

  /* ---------- output builders ---------- */
  function postHTML(d) {
    var site = (CFG.company && CFG.company.website) || 'https://bharationsystems.com';
    var url = site.replace(/\/$/, '') + '/blog/' + d.slug + '.html';
    var img = site.replace(/\/$/, '') + '/assets/logo.png';
    var rel = d.related.length ? (
      '\n    <div class="relbox"><h3>Related machinery</h3>' +
      d.related.map(function (s) { return '<a href="../products/' + s + '.html">' + A.esc(productName(s)) + '</a>'; }).join('') +
      '</div>'
    ) : '';
    var ld1 = {
      "@context": "https://schema.org", "@type": "BlogPosting", "headline": d.title,
      "description": d.desc, "datePublished": d.date, "dateModified": d.date,
      "author": { "@type": "Organization", "name": "Bharat ION Systems Pvt. Ltd." },
      "publisher": { "@type": "Organization", "name": "Bharat ION Systems Pvt. Ltd.", "logo": { "@type": "ImageObject", "url": img } },
      "image": img, "mainEntityOfPage": url
    };
    var ld2 = {
      "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": site.replace(/\/$/, '') + "/" },
        { "@type": "ListItem", "position": 2, "name": "Blog", "item": site.replace(/\/$/, '') + "/blog.html" },
        { "@type": "ListItem", "position": 3, "name": d.title, "item": url }
      ]
    };
    return [
      '<!DOCTYPE html>',
      '<html lang="en">',
      '<head>',
      '<meta charset="utf-8">',
      '<meta name="viewport" content="width=device-width, initial-scale=1">',
      '<title>' + A.esc(d.title) + ' | Bharat iON Systems</title>',
      '<meta name="description" content="' + A.esc(d.desc) + '">',
      '<link rel="canonical" href="' + url + '">',
      '<meta name="robots" content="index,follow">',
      '<meta name="theme-color" content="#08214E">',
      '<meta property="og:type" content="article">',
      '<meta property="og:title" content="' + A.esc(d.title) + '">',
      '<meta property="og:description" content="' + A.esc(d.desc) + '">',
      '<meta property="og:url" content="' + url + '">',
      '<meta property="og:site_name" content="Bharat iON Systems">',
      '<meta property="og:image" content="' + img + '">',
      '<meta name="twitter:card" content="summary_large_image">',
      '<link rel="icon" href="../assets/logo.png">',
      '<link rel="preconnect" href="https://fonts.googleapis.com">',
      '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
      '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">',
      '<link rel="stylesheet" href="../css/style.css">',
      '<script type="application/ld+json">' + JSON.stringify(ld1) + '<\/script>',
      '<script type="application/ld+json">' + JSON.stringify(ld2) + '<\/script>',
      '</head>',
      '<body>',
      '',
      '<header>',
      '  <div class="container nav">',
      '    <a href="../index.html" class="logo" aria-label="Bharat iON Systems home"><span class="lk"><b>BHARAT <i>iON</i> SYSTEMS</b><small>Water & Packaging Machinery</small></span></a>',
      '    <nav><ul class="menu">',
      '      <li><a href="../index.html">Home</a></li>',
      '      <li><a href="../about.html">About</a></li>',
      '      <li><a href="../products.html">Products</a></li>',
      '      <li><a href="../applications.html">Applications</a></li>',
      '      <li><a href="../blog.html" aria-current="page">Blog</a></li>',
      '      <li><a href="../contact.html">Contact</a></li>',
      '    </ul></nav>',
      '    <div class="nav-cta">',
      '      <a href="../contact.html" class="btn btn-red">Get a Quote</a>',
      '      <button class="burger" aria-label="Menu"><span></span><span></span><span></span></button>',
      '    </div>',
      '  </div>',
      '</header>',
      '<main>',
      '',
      '<section class="arthero"><div class="container">',
      '  <div class="crumb" style="color:#cfe0f5"><a href="../index.html" style="color:#cfe0f5">Home</a> / <a href="../blog.html" style="color:#cfe0f5">Blog</a> / <b style="color:#fff">Article</b></div>',
      '  <span class="cat">' + A.esc(d.category) + '</span>',
      '  <h1>' + A.esc(d.title) + '</h1>',
      '  <div class="meta">' + fmtDate(d.date) + ' &middot; ' + d.read + ' min read &middot; by Bharat iON Systems</div>',
      '</div></section>',
      '<section class="sec"><div class="container">',
      '  <article class="article">',
      '    ',
      d.body,
      rel,
      '    <div style="margin-top:30px"><a href="../contact.html" class="btn btn-red btn-lg">Get a Free Quote</a></div>',
      '  </article>',
      '</div></section>',
      '</main>',
      '',
      footerHTML(),
      '<script src="../js/main.js"><\/script>',
      '</body>',
      '</html>',
      ''
    ].join('\n');
  }

  function footerHTML() {
    // mirrors the site footer (with Bhama Vision credit), relative "../" paths
    return [
      '<footer>',
      '  <div class="container">',
      '    <div class="fcols">',
      '      <div>',
      '        <div class="flogo"><span>BHARAT <i>iON</i> SYSTEMS</span></div>',
      '        <p style="max-width:280px">Bharat ION Systems Pvt. Ltd. &mdash; manufacturer &amp; supplier of complete water treatment and bottle-packaging machinery, from RO to shrink packaging.</p>',
      '      </div>',
      '      <div><h4>Company</h4><ul>',
      '        <li><a href="../index.html">Home</a></li>',
      '        <li><a href="../about.html">About Us</a></li>',
      '        <li><a href="../applications.html">Applications</a></li>',
      '        <li><a href="../blog.html">Blog</a></li>',
      '        <li><a href="../contact.html">Contact</a></li>',
      '      </ul></div>',
      '      <div><h4>Get in Touch</h4><ul>',
      '        <li><a href="tel:+918384061695">+91 83840 61695</a></li>',
      '        <li><a href="mailto:info@bharationsystems.com">info@bharationsystems.com</a></li>',
      '        <li>2882, 1st Floor, Karheda, Ghaziabad, Uttar Pradesh 201007</li>',
      '      </ul></div>',
      '    </div>',
      '    <div class="fbot">&copy; 2026 Bharat ION Systems Pvt. Ltd.. All rights reserved. &nbsp;|&nbsp; Water Treatment & Bottle Packaging Machinery Manufacturer. &nbsp;|&nbsp; Designed &amp; Developed by <a href="https://www.bhamavision.com" target="_blank" rel="noopener">Bhama Vision</a>.</div>',
      '  </div>',
      '</footer>'
    ].join('\n');
  }

  function cardHTML(d) {
    return [
      '    <a class="bcard" href="blog/' + d.slug + '.html">',
      '      <div class="top"><span class="c">' + A.esc(d.category) + '</span></div>',
      '      <div class="bd">',
      '        <h3>' + A.esc(d.title) + '</h3>',
      '        <p>' + A.esc(d.desc) + '</p>',
      '        <div class="meta">' + fmtDate(d.date) + ' &middot; ' + d.read + ' min read</div>',
      '        <span class="lk">Read article<svg width="13" height="13" viewBox="0 0 24 24" style="vertical-align:middle;margin-left:4px"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></span>',
      '      </div>',
      '    </a>'
    ].join('\n');
  }

  function sitemapHTML(d) {
    var site = ((CFG.company && CFG.company.website) || 'https://bharationsystems.com').replace(/\/$/, '');
    return '  <url><loc>' + site + '/blog/' + d.slug + '.html</loc><changefreq>monthly</changefreq><priority>0.6</priority></url>';
  }

  /* ---------- actions ---------- */
  function saveDraft(silent) {
    var d = gather();
    if (!d.title) { A.toast('Add a title first', 'err'); return null; }
    var list = A.store.get('blog_drafts', []);
    var i = list.findIndex(function (x) { return x.id === d.id; });
    if (i >= 0) list[i] = d; else list.push(d);
    A.store.set('blog_drafts', list);
    currentId = d.id;
    if (!silent) A.toast('Draft saved', 'ok');
    return d;
  }

  function generate() {
    var d = gather();
    if (!d.title || !d.desc) { A.toast('Title and meta description are required', 'err'); return; }
    saveDraft(true);
    $('fileNameLbl').textContent = d.slug + '.html';
    $('outHtml').textContent = postHTML(d);
    $('outCard2').textContent = cardHTML(d);
    $('outSitemap').textContent = sitemapHTML(d);
    $('outCard').style.display = 'block';
    $('outCard').scrollIntoView({ behavior: 'smooth' });
    if (CFG.apiBaseUrl) {
      var b = $('btnApiBlog'); b.style.display = 'inline-flex';
      b.onclick = function () {
        A.apiPost('/blog', { post: d, html: postHTML(d) })
          .then(function () { A.toast('Sent to backend', 'ok'); })
          .catch(function () { A.toast('Backend error', 'err'); });
      };
    }
    window._lastPost = { name: d.slug + '.html', html: postHTML(d) };
  }

  function fillForm(d) {
    currentId = d.id || null;
    $('f_title').value = d.title || '';
    $('f_slug').value = d.slug || '';
    $('f_cat').value = d.category || (CFG.blogCategories && CFG.blogCategories[0]) || '';
    $('f_date').value = d.date || todayISO();
    $('f_read').value = d.read || 6;
    $('f_desc').value = d.desc || '';
    $('bodyInput').value = d.body || '';
    Array.prototype.forEach.call(document.querySelectorAll('#relList input'), function (i) {
      i.checked = (d.related || []).indexOf(i.value) >= 0;
    });
    render();
  }

  /* ---------- init ---------- */
  document.addEventListener('DOMContentLoaded', function () {
    (CFG.blogCategories || ['General']).forEach(function (c) { $('f_cat').appendChild(A.el('option', { value: c, text: c })); });
    (CFG.products || []).forEach(function (p) {
      var id = 'rel_' + p.slug;
      var lbl = A.el('label', { class: 'pill', for: id }, [
        A.el('input', { type: 'checkbox', id: id, value: p.slug, onchange: render }),
        document.createTextNode(p.name)
      ]);
      $('relList').appendChild(lbl);
    });

    // toolbar
    document.querySelectorAll('.toolbar button').forEach(function (b) {
      b.addEventListener('click', function () {
        var t = b.getAttribute('data-ins'), w = b.getAttribute('data-wrap');
        if (w) return insert('<' + w + '>', '</' + w + '>', 'bold text');
        if (t === 'h2') return insert('\n<h2>', '</h2>\n', 'Section heading');
        if (t === 'p') return insert('\n<p>', '</p>\n', 'Your paragraph text.');
        if (t === 'ul') return insert('\n<ul>\n<li>', '</li>\n<li>Second point</li>\n</ul>\n', 'First point');
        if (t === 'ol') return insert('\n<ol>\n<li>', '</li>\n<li>Step two</li>\n</ol>\n', 'Step one');
        if (t === 'link') return insert('<a href="https://">', '</a>', 'link text');
        if (t === 'prodlink') {
          var first = (CFG.products || [])[0] || { slug: 'industrial-ro-water-treatment-plant', name: 'RO plant' };
          return insert('<a href="../products/' + first.slug + '.html">', '</a>', first.name);
        }
      });
    });

    ['f_title', 'f_slug', 'f_cat', 'f_date', 'f_read', 'f_desc', 'bodyInput'].forEach(function (id) {
      $(id).addEventListener('input', render);
    });
    $('btnSaveDraft').addEventListener('click', function () { saveDraft(false); });
    $('btnGenerate').addEventListener('click', generate);
    $('btnNew').addEventListener('click', function () {
      if (!confirm('Start a new blank post?')) return;
      currentId = null; history.replaceState(null, '', 'blog.html');
      fillForm({ date: todayISO(), read: 6 });
      $('outCard').style.display = 'none';
    });
    $('btnDownload').addEventListener('click', function () {
      if (window._lastPost) A.download(window._lastPost.name, window._lastPost.html, 'text/html;charset=utf-8');
    });
    document.querySelectorAll('[data-copy]').forEach(function (b) {
      b.addEventListener('click', function () { A.copy($(b.getAttribute('data-copy')).textContent); });
    });

    var id = new URLSearchParams(location.search).get('id');
    var draft = id && (A.store.get('blog_drafts', []).find(function (x) { return x.id === id; }));
    if (draft) fillForm(draft); else fillForm({ date: todayISO(), read: 6 });
  });
})();
