#!/usr/bin/env python3
"""
Bharat ION Systems - Quotation Generator (backend)
--------------------------------------------------
A small Flask app: fill an editor form (type the changing fields, upload a
logo and per-item product images) and instantly download a locked, non-editable
A4 6-page quotation PDF.

Run:  python3 app.py    then open  http://localhost:5000
"""
import os
import time
import copy

from flask import Flask, request, render_template, send_file, abort
from werkzeug.utils import secure_filename

import quote_render as qr

BASE = os.path.dirname(os.path.abspath(__file__))
UPLOADS = os.path.join(BASE, "uploads")
os.makedirs(UPLOADS, exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024  # 25 MB total upload
IMG_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif"}


def _save_upload(filestorage, prefix):
    """Save an uploaded image and return its absolute path (or None)."""
    if not filestorage or not filestorage.filename:
        return None
    ext = os.path.splitext(filestorage.filename)[1].lower()
    if ext not in IMG_EXT:
        return None
    name = f"{prefix}_{int(time.time()*1000)}_{secure_filename(filestorage.filename)}"
    path = os.path.join(UPLOADS, name)
    filestorage.save(path)
    return path


def _parse_specs(text):
    out = []
    for line in (text or "").splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        k, v = line.split(":", 1)
        out.append((k.strip(), v.strip()))
    return out


def _parse_parts(text):
    out = []
    for line in (text or "").splitlines():
        line = line.strip()
        if not line:
            continue
        cols = [c.strip() for c in line.split("|")]
        while len(cols) < 3:
            cols.append("")
        out.append((cols[0], cols[1], cols[2]))
    return out


def _parse_terms(text):
    out = []
    for line in (text or "").splitlines():
        line = line.strip()
        if not line:
            continue
        if "|" in line:
            t, b = line.split("|", 1)
            out.append((t.strip(), b.strip()))
        else:
            out.append((line, ""))
    return out


def _build_data_from_form():
    d = copy.deepcopy(qr.default_data())
    f = request.form

    co = d["company"]
    for key, field in [("name", "co_name"), ("tag1", "co_tag1"), ("tag2", "co_tag2"),
                       ("addr", "co_addr"), ("phone", "co_phone"), ("email", "co_email"),
                       ("web", "co_web"), ("gstin", "co_gstin")]:
        if f.get(field) is not None and f.get(field) != "":
            co[key] = f.get(field)

    bk = d["bank"]
    for key, field in [("name", "bank_name"), ("ac", "bank_ac"), ("branch", "bank_branch"), ("ifsc", "bank_ifsc")]:
        if f.get(field):
            bk[key] = f.get(field)

    for key, field in [("ref", "ref"), ("date", "date"), ("validity", "validity")]:
        if f.get(field):
            d["meta"][key] = f.get(field)

    for key, field in [("name", "cust_name"), ("firm", "cust_firm"), ("city", "cust_city"), ("mob", "cust_mob")]:
        if f.get(field) is not None:
            d["customer"][key] = f.get(field)

    if f.get("subject") is not None:
        d["subject"] = f.get("subject")
    if f.get("intro") is not None:
        d["intro"] = f.get("intro")
    if f.get("note") is not None:
        d["note"] = f.get("note")

    if f.get("specs"):
        d["specs"] = _parse_specs(f.get("specs"))
    if f.get("parts"):
        d["parts"] = _parse_parts(f.get("parts"))
    if f.get("terms"):
        d["terms"] = _parse_terms(f.get("terms"))

    # logo: use new upload, else reuse persisted logo, else fallback emblem
    logo_up = _save_upload(request.files.get("logo"), "logo")
    persisted = os.path.join(UPLOADS, "logo_current")
    if logo_up:
        # remember the latest logo for future generations
        ext = os.path.splitext(logo_up)[1]
        try:
            import shutil
            shutil.copy(logo_up, persisted + ext)
        except Exception:
            pass
        co["logo"] = logo_up
    else:
        for ext in (".png", ".jpg", ".jpeg", ".webp"):
            if os.path.exists(persisted + ext):
                co["logo"] = persisted + ext
                break

    # watermark: optional separate mark (falls back to logo in the renderer)
    wm_up = _save_upload(request.files.get("watermark"), "wm")
    wm_persisted = os.path.join(UPLOADS, "wm_current")
    if wm_up:
        ext = os.path.splitext(wm_up)[1]
        try:
            import shutil
            shutil.copy(wm_up, wm_persisted + ext)
        except Exception:
            pass
        co["watermark"] = wm_up
    else:
        for ext in (".png", ".jpg", ".jpeg", ".webp"):
            if os.path.exists(wm_persisted + ext):
                co["watermark"] = wm_persisted + ext
                break

    # price items (parallel arrays + per-row image files)
    names = f.getlist("item_name")
    descs = f.getlist("item_desc")
    qtys = f.getlist("item_qty")
    prices = f.getlist("item_price")
    prods = f.getlist("item_prod")          # optional: reuse a bundled machine photo
    images = request.files.getlist("item_image")
    items = []
    for i, name in enumerate(names):
        if not (name and name.strip()):
            continue
        img_path = None
        if i < len(images):
            img_path = _save_upload(images[i], f"item{i}")
        # no upload for this row? fall back to the permanent bundled product photo
        if not img_path and i < len(prods) and prods[i]:
            img_path = qr._product_default_img(prods[i])
        items.append({
            "img": img_path,
            "name": name.strip(),
            "desc": (descs[i].strip() if i < len(descs) else ""),
            "qty": (qtys[i].strip() if i < len(qtys) and qtys[i].strip() else "1 Set"),
            "price": (prices[i].strip() if i < len(prices) else "0"),
        })
    if items:
        d["items"] = items

    # product-range images (one per product; uploaded once and remembered)
    pd = getattr(qr, "_pd", None)
    if pd:
        catmap = {k: (n, c) for n, c, k in pd.PRODUCT_RANGE}
        pkeys = f.getlist("prod_key")
        pnames = f.getlist("prod_name")
        namemap = {pkeys[i]: (pnames[i].strip() if i < len(pnames) else "") for i in range(len(pkeys))}
        order = pkeys if pkeys else [k for _, _, k in pd.PRODUCT_RANGE]
        products = []
        for key in order:
            base_name, cat = catmap.get(key, ("", ""))
            name = namemap.get(key) or base_name
            img = None
            dest = os.path.join(UPLOADS, "prod_" + key)
            # each product has a UNIQUE file field name -> no positional mis-alignment
            up = _save_upload(request.files.get("prod_img_" + key), "prod_" + key)
            if up:
                try:
                    import shutil
                    shutil.copy(up, dest + os.path.splitext(up)[1])
                except Exception:
                    pass
                img = up
            else:
                for ext in (".png", ".jpg", ".jpeg", ".webp"):
                    if os.path.exists(dest + ext):
                        img = dest + ext
                        break
            products.append({"name": name, "cat": cat, "key": key, "img": img})
        if products:
            d["products"] = products
    return d


import html as _html


def _u(s):
    return _html.unescape(s) if isinstance(s, str) else s


def _build_view():
    d = qr.default_data()
    co, bk = d["company"], d["bank"]
    return {
        "co_name": _u(co["name"]), "co_tag1": _u(co["tag1"]), "co_tag2": _u(co["tag2"]),
        "co_addr": _u(co["addr"]), "co_phone": _u(co["phone"]), "co_email": _u(co["email"]),
        "co_web": _u(co["web"]), "co_gstin": _u(co["gstin"]),
        "bank_name": _u(bk["name"]), "bank_ac": _u(bk["ac"]), "bank_branch": _u(bk["branch"]), "bank_ifsc": _u(bk["ifsc"]),
        "ref": d["meta"]["ref"], "date": d["meta"]["date"], "validity": d["meta"]["validity"],
        "cust_name": _u(d["customer"]["name"]), "cust_firm": _u(d["customer"]["firm"]),
        "cust_city": _u(d["customer"]["city"]), "cust_mob": _u(d["customer"]["mob"]),
        "subject": _u(d["subject"]), "intro": _u(d["intro"]), "note": _u(d["note"]),
        "specs_text": "\n".join(f"{_u(k)}: {_u(v)}" for k, v in d["specs"]),
        "parts_text": "\n".join(f"{_u(a)} | {_u(b)} | {_u(c)}" for a, b, c in d["parts"]),
        "terms_text": "\n".join(f"{_u(t)} | {_u(b)}" for t, b in d["terms"]),
        "items": [{"name": _u(it["name"]), "desc": _u(it["desc"]),
                   "qty": _u(it["qty"]), "price": it["price"]} for it in d["items"]],
        "products": ([{"name": _u(n), "cat": _u(c), "key": k} for n, c, k in qr._pd.PRODUCT_RANGE]
                     if getattr(qr, "_pd", None) else []),
    }


@app.route("/")
def editor():
    return render_template("editor.html", v=_build_view())


@app.route("/logoimg")
def logoimg():
    """Serve the permanent bundled company logo (for the editor preview)."""
    p = qr._default_logo()
    if not p or not os.path.exists(p):
        abort(404)
    return send_file(p)


@app.route("/prodimg/<key>")
def prodimg(key):
    """Serve a permanent bundled product photo by key (for the editor preview)."""
    p = qr._product_default_img(key)
    if not p or not os.path.exists(p):
        abort(404)
    return send_file(p)


@app.route("/catalogue")
def catalogue():
    """Generate and download the full product catalogue PDF."""
    import catalogue_render as cat
    pdf = cat.render_catalogue_pdf()
    return send_file(_bio(pdf), mimetype="application/pdf", as_attachment=True,
                     download_name="Bharat-iON-Systems-Catalogue.pdf")


@app.route("/company-profile")
def company_profile():
    import profile_render as pr
    return send_file(_bio(pr.render_pdf()), mimetype="application/pdf", as_attachment=True,
                     download_name="Bharat-iON-Systems-Company-Profile.pdf")


@app.route("/letterhead")
def letterhead():
    import letterhead_render as lh
    return send_file(_bio(lh.render_pdf()), mimetype="application/pdf", as_attachment=True,
                     download_name="Bharat-iON-Systems-Letterhead.pdf")


@app.route("/visiting-card")
def visiting_card():
    import visiting_card_render as vc
    return send_file(_bio(vc.render_pdf()), mimetype="application/pdf", as_attachment=True,
                     download_name="Bharat-iON-Systems-Visiting-Card.pdf")


@app.route("/preview", methods=["POST"])
def preview():
    data = _build_data_from_form()
    pdf = qr.render_pdf_bytes(data, flatten=False, lock=False)  # unlocked for quick viewing
    return send_file(_bio(pdf), mimetype="application/pdf", download_name="preview.pdf")


@app.route("/generate", methods=["POST"])
def generate():
    data = _build_data_from_form()
    flatten = request.form.get("flatten") == "on"
    pdf = qr.render_pdf_bytes(data, flatten=flatten, lock=True)  # locked / non-editable
    ref = (data["meta"]["ref"] or "quotation").replace("/", "-")
    return send_file(_bio(pdf), mimetype="application/pdf", as_attachment=True,
                     download_name=f"Quotation_{ref}.pdf")


def _bio(b):
    import io
    return io.BytesIO(b)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
