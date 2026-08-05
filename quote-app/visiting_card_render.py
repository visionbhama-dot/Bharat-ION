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


# Personalise these (or leave generic for a company card)
PERSON = {"name": "[ Your Name ]", "role": "Designation"}
CO = {
    "tag": "Water Treatment &amp; Packaging Machinery",
    "phone": "+91 83840 61695", "email": "info@bharationsystems.com",
    "web": "www.bharationsystems.com", "city": "Ghaziabad, Uttar Pradesh",
}

ICON = {
    "phone": "<path d='M4 4h4l2 5-3 2a12 12 0 0 0 6 6l2-3 5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 2 6a2 2 0 0 1 2-2z'/>",
    "mail": "<rect x='3' y='5' width='18' height='14' rx='2'/><path d='M3 7l9 6 9-6'/>",
    "pin": "<path d='M12 21s7-6 7-11a7 7 0 0 0-14 0c0 5 7 11 7 11z'/><circle cx='12' cy='10' r='2.5'/>",
    "web": "<circle cx='12' cy='12' r='9'/><path d='M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18'/>",
}


def ic(name):
    return (f"<svg viewBox='0 0 24 24' fill='none' stroke='#1656C4' stroke-width='2' "
            f"stroke-linecap='round' stroke-linejoin='round'>{ICON.get(name, '')}</svg>")


CSS = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800;900&family=Inter:wght@400;500;600;700&display=swap');
@page { size:90mm 54mm; margin:0; }
* { box-sizing:border-box; }
body { margin:0; font-family:'Inter',sans-serif; }
.card { position:relative; width:90mm; height:54mm; overflow:hidden; }
.pb { page-break-before:always; }

/* FRONT */
.front { background:linear-gradient(140deg,#071B44,#0C336F 55%,#123E86 120%); display:flex; align-items:center; justify-content:center; }
.front .b1 { position:absolute; top:-16mm; right:-14mm; width:44mm; height:44mm; border-radius:50%; background:rgba(255,255,255,.05); }
.front .b2 { position:absolute; bottom:-18mm; left:-12mm; width:40mm; height:40mm; border-radius:50%; background:rgba(46,116,232,.20); }
.front .b3 { position:absolute; bottom:8mm; right:8mm; width:12mm; height:12mm; border:1px solid rgba(255,255,255,.15); border-radius:50%; }
.front .chip { background:#fff; border-radius:11px; padding:5mm 7mm; box-shadow:0 10px 26px rgba(0,0,0,.28); z-index:2; }
.front .chip img { height:14mm; width:auto; display:block; }
.front .tg { position:absolute; bottom:5mm; left:0; right:0; text-align:center; font-family:'Poppins'; font-weight:600;
  font-size:6.2pt; letter-spacing:2.5px; text-transform:uppercase; color:#9DC4FF; z-index:2; }

/* BACK */
.back { background:#fff; display:flex; align-items:center; padding:6mm; gap:5mm; }
.back .stripe { position:absolute; left:0; top:0; bottom:0; width:4mm; background:linear-gradient(180deg,#08214E,#1656C4 60%,#24A24B); }
.back .left { width:32mm; display:flex; align-items:center; justify-content:center; padding-left:3mm; }
.back .left img { max-width:100%; max-height:26mm; width:auto; }
.back .div { width:1px; align-self:stretch; background:#E2E8F2; margin:3mm 0; }
.back .right { flex:1; }
.back .web { font-family:'Poppins'; font-weight:800; font-size:8.5pt; color:#08214E; letter-spacing:.3px; }
.back .nm { font-size:6.8pt; color:#5C6E7A; letter-spacing:1.5px; text-transform:uppercase; margin:.6mm 0 3mm; }
.back .row { display:flex; align-items:center; gap:2.5mm; font-size:7.4pt; color:#33425f; margin:1.8mm 0; }
.back .row .ic { width:5.2mm; height:5.2mm; border-radius:50%; border:1px solid #cfe0fb; display:flex; align-items:center; justify-content:center; flex:none; }
.back .row .ic svg { width:2.7mm; height:2.7mm; }
"""


def build_html():
    lg = _fileuri(_logo())
    front = f"""
<div class="card front">
  <div class="b1"></div><div class="b2"></div><div class="b3"></div>
  {f'<div class="chip"><img src="{lg}" alt=""></div>' if lg else ''}
  <div class="tg">{CO['tag']}</div>
</div>"""
    back = f"""
<div class="card back pb">
  <div class="stripe"></div>
  <div class="left">{f'<img src="{lg}" alt="">' if lg else ''}</div>
  <div class="div"></div>
  <div class="right">
    <div class="web">{CO['web']}</div>
    <div class="nm">{PERSON['name']} &middot; {PERSON['role']}</div>
    <div class="row"><span class="ic">{ic('phone')}</span> {CO['phone']}</div>
    <div class="row"><span class="ic">{ic('mail')}</span> {CO['email']}</div>
    <div class="row"><span class="ic">{ic('pin')}</span> {CO['city']}</div>
  </div>
</div>"""
    return f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{front}{back}</body></html>"


def render_pdf():
    return HTML(string=build_html(), base_url=BASE).write_pdf()


if __name__ == "__main__":
    out = os.path.abspath(os.path.join(BASE, "..", "assets", "visiting-card.pdf"))
    with open(out, "wb") as f:
        f.write(render_pdf())
    print("wrote", out, os.path.getsize(out) // 1024, "KB")
