#!/usr/bin/env python3
"""Bharat iON Systems - professional A4 letterhead (all info in header, watermark, blank body)."""
import os
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


CO = {
    "phone": "+91 83840 61695", "email": "info@bharationsystems.com",
    "web": "www.bharationsystems.com", "gstin": "[GSTIN to be added]",
    "addr": "2882, 1st Floor, Karheda, Ghaziabad, Uttar Pradesh 201007",
}

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&family=Inter:wght@400;500;600&display=swap');
@page { size:A4; margin:0; }
* { box-sizing:border-box; }
body { margin:0; font-family:'Inter',sans-serif; color:#16232B; }
.sheet { position:relative; width:210mm; height:297mm; overflow:hidden; background:#fff; padding:15mm 16mm 14mm 22mm; }
/* left brand stripe */
.stripe { position:absolute; left:0; top:0; bottom:0; width:6mm; background:linear-gradient(180deg,#08214E,#1656C4 55%,#24A24B); }
/* soft corner accents */
.corner { position:absolute; width:70mm; height:70mm; z-index:0; }
.corner.tr { top:-35mm; right:-35mm; background:radial-gradient(circle at center, rgba(22,86,196,.10), transparent 70%); }
.corner.bl { bottom:-30mm; left:-15mm; background:radial-gradient(circle at center, rgba(36,162,75,.10), transparent 70%); }
/* watermark */
.wm { position:absolute; top:52%; left:52%; transform:translate(-50%,-50%); width:130mm; opacity:.05; z-index:0; }
.wm img { width:100%; }
/* header - everything lives here */
.head { position:relative; z-index:2; display:flex; justify-content:space-between; align-items:center; }
.head .lg { height:21mm; width:auto; }
.head .hc { text-align:right; font-size:9pt; color:#3a496a; line-height:1.85; }
.head .hc b { color:#08214E; font-family:'Poppins'; font-weight:700; font-size:10pt; }
.addr { position:relative; z-index:2; margin-top:5mm; display:flex; justify-content:space-between; gap:8mm;
  font-size:8.6pt; color:#5C6E7A; }
.addr .a { max-width:120mm; }
.addr b { color:#08214E; }
.rule { position:relative; z-index:2; margin-top:4mm; height:3px; border-radius:2px;
  background:linear-gradient(90deg,#24A24B,#1656C4 45%,#08214E 75%,#E23127); }
"""


def build_html():
    logo = _logo()
    lg = f'<img class="lg" src="{_fileuri(logo)}" alt="">' if logo else ''
    wm = f'<div class="wm"><img src="{_fileuri(logo)}" alt=""></div>' if logo else ''
    return f"""<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>
<div class="sheet">
  <div class="stripe"></div>
  <div class="corner tr"></div><div class="corner bl"></div>
  {wm}
  <div class="head">
    {lg}
    <div class="hc"><b>{CO['phone']}</b><br>{CO['email']}<br>{CO['web']}</div>
  </div>
  <div class="addr">
    <span class="a">&#9737;&nbsp; {CO['addr']}</span>
    <span><b>GSTIN:</b> {CO['gstin']}</span>
  </div>
  <div class="rule"></div>
</div></body></html>"""


def render_pdf():
    return HTML(string=build_html(), base_url=BASE).write_pdf()


if __name__ == "__main__":
    out = os.path.abspath(os.path.join(BASE, "..", "assets", "letterhead.pdf"))
    with open(out, "wb") as f:
        f.write(render_pdf())
    print("wrote", out, os.path.getsize(out) // 1024, "KB")
