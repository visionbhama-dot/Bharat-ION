/* Bharat iON Systems - site interactions + optional image wiring
   ----------------------------------------------------------------
   Real photos/branding are OPTIONAL. Drop image files into the folders under
   assets/images/ (see IMAGE-UPLOAD-GUIDE.md) and they are picked up here
   automatically. If a file is missing, the built-in design is used as a
   graceful fallback, so nothing ever looks broken.

   Paths are resolved RELATIVE TO THIS SCRIPT'S LOCATION, so they work no matter
   how deep the page is (/, /products/, /blog/) and no matter where the site is
   hosted (custom domain, GitHub Pages project path, local preview, etc.).
*/
(function () {
  'use strict';

  // Work out the site base URL from where main.js itself was loaded.
  var thisScript = document.currentScript || (function () {
    var s = document.getElementsByTagName('script');
    for (var i = s.length - 1; i >= 0; i--) {
      if (/(^|\/)main\.js(\?|#|$)/.test(s[i].src || '')) return s[i];
    }
    return null;
  })();
  // e.g. "https://site.com/js/main.js" -> "https://site.com/"
  var BASE = thisScript ? thisScript.src.replace(/js\/main\.js.*$/, '') : '';
  var IMG = BASE + 'assets/images/';
  var ASSETS = BASE + 'assets/';

  var PHOTO_EXT = ['jpg', 'jpeg', 'png', 'webp'];
  var LOGO_EXT = ['png', 'svg', 'webp', 'jpg', 'jpeg'];
  var ICON_EXT = ['png', 'svg', 'ico', 'webp', 'jpg'];

  // Try a list of candidate URLs in order; call onFound with the first that loads.
  function probe(urls, onFound) {
    var i = 0;
    (function next() {
      if (i >= urls.length) return;
      var url = urls[i++];
      var img = new Image();
      img.onload = function () { onFound(url); };
      img.onerror = next;
      img.src = url;
    })();
  }

  function candidates(base, exts) {
    return exts.map(function (e) { return base + '.' + e; });
  }

  function slugFromPath(path) {
    var last = (path || '').split('?')[0].split('#')[0].split('/').pop() || '';
    return last.replace(/\.html?$/i, '');
  }

  /* ---- enquiry form -> emails info@bharationsystems.com via FormSubmit ---- */
  function wireEnquiryForm() {
    var f = document.querySelector('form[data-enquiry]');
    if (!f) return;
    var email = 'info' + '@' + 'bharationsystems.com';
    function msgEl() {
      var m = f.querySelector('.form-msg');
      if (!m) { m = document.createElement('div'); m.className = 'form-msg'; f.appendChild(m); }
      return m;
    }
    f.addEventListener('submit', function (e) {
      var hp = f.querySelector('[name="_honey"]');
      if (hp && hp.value) { e.preventDefault(); return; }      // bot trap
      if (!f.checkValidity()) return;                          // let browser show errors
      e.preventDefault();
      var btn = f.querySelector('button[type="submit"], button:not([type])');
      var orig = btn ? btn.textContent : '';
      if (btn) { btn.disabled = true; btn.textContent = 'Sending\u2026'; }
      var m = msgEl(); m.className = 'form-msg'; m.textContent = '';
      fetch('https://formsubmit.co/ajax/' + email, {
        method: 'POST', headers: { 'Accept': 'application/json' }, body: new FormData(f)
      }).then(function (r) { return r.json(); }).then(function (data) {
        var okFlag = data && (data.success === true || data.success === 'true');
        m.className = 'form-msg ok';
        m.textContent = okFlag
          ? 'Thank you! Your enquiry has been sent \u2014 we\u2019ll get back to you shortly.'
          : 'Thank you! Your enquiry has been received.';
        f.reset();
      }).catch(function () {
        m.className = 'form-msg err';
        m.innerHTML = 'Sorry, something went wrong. Please call/WhatsApp us or email <a href="mailto:' + email + '">' + email + '</a>.';
      }).then(function () { if (btn) { btn.disabled = false; btn.textContent = orig; } });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    wireEnquiryForm();

    /* ---- mobile menu ---- */
    var burger = document.querySelector('.burger');
    var menu = document.querySelector('.menu');
    if (burger && menu) {
      burger.addEventListener('click', function () { menu.classList.toggle('open'); });
    }
    document.querySelectorAll('.menu a').forEach(function (a) {
      a.addEventListener('click', function () { if (menu) menu.classList.remove('open'); });
    });

    /* ---- optional favicon (new folder, then legacy assets/) ---- */
    probe(
      candidates(IMG + 'favicon/favicon', ICON_EXT)
        .concat(candidates(ASSETS + 'favicon', ICON_EXT))
        .concat(candidates(ASSETS + 'logo', ICON_EXT)),
      function (url) {
        var link = document.querySelector('link[rel="icon"]');
        if (!link) {
          link = document.createElement('link');
          link.rel = 'icon';
          document.head.appendChild(link);
        }
        link.href = url;
      }
    );

    /* ---- optional logo, header + footer (new folder, then legacy assets/) ---- */
    probe(
      candidates(IMG + 'logo/logo', LOGO_EXT)
        .concat(candidates(ASSETS + 'logo', LOGO_EXT)),
      function (url) {
        document.querySelectorAll('.logo, .flogo').forEach(function (holder) {
          if (holder.querySelector('.logo-img')) return;
          var img = document.createElement('img');
          img.className = 'logo-img';
          img.src = url;
          img.alt = 'Bharat iON Systems';
          holder.insertBefore(img, holder.firstChild);
          holder.classList.add('has-img');
        });
      }
    );

    /* ---- optional hero banner background ---- */
    var hero = document.querySelector('.hero');
    if (hero) {
      probe(candidates(IMG + 'banner/hero-banner', PHOTO_EXT), function (url) {
        hero.style.backgroundImage =
          "linear-gradient(150deg, rgba(8,33,78,.86) 0%, rgba(11,50,114,.80) 55%, rgba(22,86,196,.72) 120%), url('" + url + "')";
        hero.style.backgroundSize = 'cover';
        hero.style.backgroundPosition = 'center';
        hero.style.backgroundRepeat = 'no-repeat';
      });
    }

    /* ---- optional process-section background (the "Complete Line" band) ---- */
    document.querySelectorAll('.band').forEach(function (band) {
      probe(candidates(IMG + 'banner/process-bg', PHOTO_EXT), function (url) {
        band.style.backgroundImage =
          "linear-gradient(135deg, rgba(8,33,78,.88) 0%, rgba(22,86,196,.80) 120%), url('" + url + "')";
        band.style.backgroundSize = 'cover';
        band.style.backgroundPosition = 'center';
        band.style.backgroundRepeat = 'no-repeat';
      });
    });

    /* ---- optional product photos on cards (index / products / landing pages) ---- */
    document.querySelectorAll('a.pcard').forEach(function (card) {
      var slug = slugFromPath(card.getAttribute('href') || '');
      if (!slug) return;
      var box = card.querySelector('.im');
      if (!box) return;
      var titleEl = card.querySelector('h3');
      var alt = titleEl ? titleEl.textContent.trim() : slug;
      probe(candidates(IMG + 'products/' + slug, PHOTO_EXT), function (url) {
        if (box.querySelector('.ovimg')) return;
        var img = document.createElement('img');
        img.className = 'ovimg';
        img.src = url;
        img.alt = alt;
        img.loading = 'lazy';
        box.appendChild(img);
      });
    });

    /* ---- optional product photo on a product detail page ---- */
    var pdBox = document.querySelector('.pd .im');
    if (pdBox) {
      var slug = slugFromPath(location.pathname);
      var h1 = document.querySelector('.pd h1');
      var alt = h1 ? h1.textContent.trim() : slug;
      if (slug) {
        probe(candidates(IMG + 'products/' + slug, PHOTO_EXT), function (url) {
          if (pdBox.querySelector('.ovimg')) return;
          var img = document.createElement('img');
          img.className = 'ovimg';
          img.src = url;
          img.alt = alt;
          pdBox.appendChild(img);
        });
      }
    }
  });
})();
