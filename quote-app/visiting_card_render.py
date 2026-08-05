#!/usr/bin/env python3
"""Bharat iON Systems - visiting / business card (90x54 mm, front + back)."""
import os
import base64
from weasyprint import HTML

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")


def _fileuri(p):
    return "file://" + os.path.abspath(p) if p and os.path.exists(p) else ""


def _logo():
    for e in (".png", ".svg", ".jpg", ".jpeg", ".webp"):
        p = os.path.join(ASSETS, "logo" + e)
        if os.path.exists(p):
            return p
    return None


def _qr(text):
    try:
        import qrcode, io
        b = io.BytesIO(); qrcode.make(text).save(b, format="PNG")
        return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()
    except Exception:
        return ""


# Personalise these two lines (or leave the role generic for a company card)
PERSON = {"name": "[ Your Name ]", "role": "Sales &amp; Support"}
CO = {
    "name": "Bharat iON Systems Pvt. Ltd.", "tag": "Water Treatment &amp; Packaging Machinery",
    "phone": "+91 83840 61695", "email": "info@bharationsystems.com",
    "web": "www.bharationsystems.com", "addr": "2882, 1st Floor, Karheda, Ghaziabad, U.P. 201007",
}

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800;900&family=Inter:wght@400;500;600;700&display=swap');
@page { size:90mm 54mm; margin:0; }
* { box-sizing:border-box; }
body { margin:0; font-family:'Inter',sans-serif; }
.card { position:relative; width:90mm; height:54mm; overflow:hidden; }
.pb { page-break-before:always; }

/* FRONT (white) */
.front { background:#fff; }
.front .bar { position:absolute; left:0; top:0; bottom:0; width:6mm; background:linear-gradient(180deg,#08214E,#1656C4 60%,#24A24B); }
.front .tex { position:absolute; right:-14mm; top:-14mm; width:40mm; height:40mm; border-radius:50%; background:rgba(22,86,196,.07); }
.front .inner { position:absolute; inset:0; padding:6mm 6mm 6mm 11mm; display:flex; flex-direction:column; }
.front .logo { height:9mm; width:auto; margin-bottom:2mm; }
.front .nm { font-family:'Poppins'; font-weight:800; font-size:11pt; color:#08214E; line-height:1.1; }
.front .role { font-size:7.5pt; color:#1656C4; font-weight:600; letter-spacing:.5px; margin-top:.5mm; }
.front .rule { height:2px; width:16mm; background:#24A24B; border-radius:2px; margin:2mm 0; }
.front .contact { margin-top:auto; font-size:7.4pt; color:#33425f; line-height:1.65; }
.front .contact .ic { display:inline-block; width:3mm; color:#1656C4; }
.front .contact b { color:#08214E; }

/* BACK (navy) */
.back { background:linear-gradient(140deg,#071B44,#0C336F 55%,#123E86 120%); color:#fff; }
.back .tex1 { position:absolute; top:-20mm; right:-18mm; width:55mm; height:55mm; border-radius:50%; background:rgba(255,255,255,.05); }
.back .inner { position:absolute; inset:0; padding:7mm; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; }
.back .chip { background:#fff; border-radius:7px; padding:2.5mm 4mm; display:inline-block; }
.back .chip img { height:8mm; width:auto; display:block; }
.back .tag { font-family:'Poppins'; font-weight:600; font-size:7.5pt; letter-spacing:2px; text-transform:uppercase; color:#7FE0A0; margin-top:3mm; }
.back .web { font-family:'Poppins'; font-weight:700; font-size:9pt; color:#fff; margin-top:2mm; }
.back .qr { position:absolute; bottom:5mm; right:5mm; background:#fff; padding:1mm; border-radius:4px; }
.back .qr img { width:14mm; height:14mm; display:block; }
"""


def build_html():
    logo = _logo()
    lg = _fileuri(logo)
    qr = _qr("https://bharationsystems.com")
    front = f"""
<div class="card front">
  <div class="bar"></div><div class="tex"></div>
  <div class="inner">
    {f'<img class="logo" src="{lg}" alt="">' if lg else ''}
    <div class="nm">{PERSON['name']}</div>
    <div class="role">{PERSON['role']}</div>
    <div class="rule"></div>
    <div class="contact">
      <div><span class="ic">&#9742;</span> <b>{CO['phone']}</b></div>
      <div><span class="ic">&#9993;</span> {CO['email']}</div>
      <div><span class="ic">&#9737;</span> {CO['web']}</div>
      <div><span class="ic">&#9741;</span> {CO['addr']}</div>
    </div>
  </div>
</div>"""
    back = f"""
<div class="card back pb">
  <div class="tex1"></div>
  <div class="inner">
    {f'<div class="chip"><img src="{lg}" alt=""></div>' if lg else ''}
    <div class="tag">{CO['tag']}</div>
    <div class="web">{CO['web']}</div>
  </div>
  {f'<div class="qr"><img src="{qr}" alt=""></div>' if qr else ''}
</div>"""
    return f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{front}{back}</body></html>"


def render_pdf():
    return HTML(string=build_html(), base_url=BASE).write_pdf()


if __name__ == "__main__":
    out = os.path.abspath(os.path.join(BASE, "..", "assets", "visiting-card.pdf"))
    with open(out, "wb") as f:
        f.write(render_pdf())
    print("wrote", out, os.path.getsize(out) // 1024, "KB")
