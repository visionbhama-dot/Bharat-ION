/* Bharat iON Systems - Image Manager */
(function () {
  'use strict';
  var A = window.ADMIN, CFG = A.cfg;
  var hasApi = !!CFG.apiBaseUrl;

  // slot.path is relative to the SITE ROOT. Admin pages sit in /admin/, so we
  // prefix "../" to preview/reference the live image.
  var REL = '../';

  function baseName(path) { return path.split('/').pop(); }
  function baseNoExt(path) { return baseName(path).replace(/\.[^.]+$/, ''); }
  function extOf(name) { var m = /\.([^.]+)$/.exec(name || ''); return m ? m[1].toLowerCase() : 'png'; }

  function buildSlots() {
    var brand = [
      { path: 'assets/images/logo/logo.png', label: 'Logo', note: 'Header & footer. Transparent PNG works best.' },
      { path: 'assets/images/favicon/favicon.png', label: 'Favicon', note: 'Browser tab icon. Square (e.g. 512\u00d7512).' }
    ];
    var bg = [
      { path: 'assets/images/banner/hero-banner.jpg', label: 'Home hero banner', note: 'Wide ~1920\u00d71080. Dark overlay auto-applied.' },
      { path: 'assets/images/banner/process-bg.jpg', label: 'Process section background', note: 'Wide ~1920\u00d7760. Dark overlay auto-applied.' }
    ];
    var prod = (CFG.products || []).map(function (p) {
      return { path: 'assets/images/products/' + p.slug + '.jpg', label: p.name, note: 'Landscape ~800\u00d7600 (4:3).' };
    });
    render('slots-brand', brand);
    render('slots-bg', bg);
    render('slots-prod', prod);
  }

  function render(hostId, slots) {
    var host = document.getElementById(hostId);
    slots.forEach(function (slot) {
      var prev = A.el('div', { class: 'prev', style: "background-image:url('" + REL + slot.path + "?t=" + Date.now() + "')", text: '' });
      // if the current image fails, keep the "no image" text
      var probe = new Image(); probe.onload = function () {}; probe.onerror = function () { prev.textContent = 'no image yet'; }; probe.src = REL + slot.path;

      var fileInput = A.el('input', { type: 'file', accept: 'image/*', style: 'display:none' });
      var pickBtn = A.el('button', { class: 'btn btn-sm', text: 'Choose image' });
      var actionBtn = A.el('button', { class: 'btn btn-sm btn-primary', text: hasApi ? 'Upload' : 'Download renamed', disabled: 'disabled' });
      var picked = null;

      pickBtn.addEventListener('click', function () { fileInput.click(); });
      fileInput.addEventListener('change', function () {
        picked = fileInput.files[0];
        if (!picked) return;
        var url = URL.createObjectURL(picked);
        prev.style.backgroundImage = "url('" + url + "')";
        prev.textContent = '';
        actionBtn.disabled = false;
      });

      actionBtn.addEventListener('click', function () {
        if (!picked) return;
        var targetName = baseNoExt(slot.path) + '.' + extOf(picked.name);
        if (hasApi) {
          var fd = new FormData();
          fd.append('file', picked, targetName);
          fd.append('slot', slot.path);
          A.apiPost('/upload', fd, true)
            .then(function () { A.toast('Uploaded: ' + targetName, 'ok'); })
            .catch(function () { A.toast('Upload failed', 'err'); });
        } else {
          // download the picked file renamed to the correct target file name
          var a = A.el('a', { href: URL.createObjectURL(picked), download: targetName });
          document.body.appendChild(a); a.click();
          setTimeout(function () { a.remove(); }, 100);
          A.toast('Saved as ' + targetName + ' \u2014 add it to /' + slot.path.replace(baseName(slot.path), ''), 'ok');
        }
      });

      var meta = A.el('div', { class: 'meta' }, [
        A.el('b', { text: slot.label }),
        A.el('code', { text: '/' + slot.path }),
        A.el('div', { class: 'muted', style: 'font-size:12px;margin-top:2px', text: slot.note })
      ]);
      var act = A.el('div', { class: 'act' }, [pickBtn, actionBtn, fileInput]);
      host.appendChild(A.el('div', { class: 'slot' }, [prev, meta, act]));
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('modeNote').innerHTML = hasApi
      ? 'Backend connected. Choose an image and click <b>Upload</b> \u2014 it is sent to your server with the correct file name.'
      : 'No backend connected, so this tool prepares files for you: choose an image and click <b>Download renamed</b> to get it with the exact required file name. Then add that file to the matching folder in your repo (e.g. via GitHub \u201cUpload files\u201d) and it appears on the site automatically. Connect a backend in <code>config.js</code> for one-click uploads.';
    buildSlots();
  });
})();
