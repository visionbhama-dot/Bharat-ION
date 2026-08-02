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
})();
