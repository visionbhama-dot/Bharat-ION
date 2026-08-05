#!/usr/bin/env python3
"""Bharat iON Systems - Company Profile (aesthetic multi-page A4 PDF)."""
import os
import base64
from weasyprint import HTML

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")


def _fileuri(p):
    return "file://" + os.path.abspath(p) if p and os.path.exists(p) else ""


def _root_asset(*p):
    return os.path.join(BASE, "..", "assets", *p)


def _logo():
    for e in (".png", ".svg", ".jpg", ".jpeg", ".webp"):
        p = os.path.join(ASSETS, "logo" + e)
        if os.path.exists(p):
            return p
    return None


def _banner():
    for name in ("hero-banner", "process-bg"):
        for e in (".jpg", ".jpeg", ".png", ".webp"):
            p = _root_asset("images", "banner", name + e)
            if os.path.exists(p):
                return p
    return None


def _qr(t):
    try:
        import qrcode, io
        b = io.BytesIO(); qrcode.make(t).save(b, format="PNG")
        return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()
    except Exception:
        return ""


CO = {
    "name": "Bharat iON Systems Pvt. Ltd.", "tag": "Water Treatment &amp; Bottle Packaging Machinery",
    "phone": "+91 83840 61695", "email": "info@bharationsystems.com",
    "web": "www.bharationsystems.com", "addr": "2882, 1st Floor, Karheda, Ghaziabad, Uttar Pradesh 201007",
}
STATS = [("RO&rarr;Pack", "Complete turnkey line"), ("6000", "Bottles/hour, up to"),
         ("11", "Machines in range"), ("Pan-India", "Sales &amp; service")]
CATS = [
    ("Water Treatment", "Industrial multi-stage RO plants for IS 10500-grade drinking water."),
    ("PET Bottle Manufacturing", "Semi-automatic, hand-feed and fully automatic PET blowing machines."),
    ("Filling &amp; Capping", "Station fillers, 4-nozzle fillers and 3-in-1 rinsing-filling-capping monoblocs."),
    ("Labelling", "Servo-controlled self-adhesive sticker labelling machines."),
    ("Coding &amp; Marking", "Inkjet batch coding for dates, batch numbers and MRP."),
    ("Secondary Packaging", "Automatic shrink wrapping for transport-ready multi-packs."),
]
WHY = [
    ("Single Accountable Partner", "One team supplies, installs and supports your entire line."),
    ("Right-Sized Solutions", "Configurations matched to your output, budget and space."),
    ("Installation &amp; Training", "On-site commissioning and operator training included."),
    ("Genuine Spares &amp; Service", "Prompt after-sales support and authentic spare parts."),
    ("Manufacturer-Direct Value", "Honest pricing straight from the maker, no middlemen."),
    ("Robust, Hygienic Builds", "Food-grade stainless construction, engineered to last."),
]
APPS = ["Packaged Drinking Water Plants", "Mineral Water Bottling Units", "Beverage &amp; Juice Filling Lines",
        "Carbonated Soft Drink Plants", "Dairy &amp; Liquid Packaging", "Distributors, Dealers &amp; OEM Buyers"]

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800;900&family=Inter:wght@400;500;600;700&display=swap');
* { box-sizing:border-box; }
@page { size:A4; margin:0; }
body { margin:0; font-family:'Inter',sans-serif; color:#1A2740; font-size:10.5pt; line-height:1.6; }
h1,h2,h3,h4 { font-family:'Poppins',sans-serif; margin:0; color:#08214E; line-height:1.1; }
.pb { page-break-before:always; }

/* content page with navy sidebar */
.page { position:relative; width:210mm; height:297mm; overflow:hidden; background:#fff; padding:20mm 18mm 16mm 30mm; }
.side { position:absolute; left:0; top:0; bottom:0; width:16mm; background:linear-gradient(180deg,#08214E,#123E86); }
.side .pg { position:absolute; top:16mm; left:0; right:0; text-align:center; font-family:'Poppins'; font-weight:900; font-size:13pt; color:#fff; }
.side .pg small { display:block; font-size:6pt; font-weight:600; letter-spacing:2px; color:#7FB2F0; }
.side .sec { position:absolute; bottom:34mm; left:-24mm; width:64mm; text-align:center; transform:rotate(-90deg); font-family:'Poppins'; font-weight:700; letter-spacing:3px; text-transform:uppercase; font-size:8pt; color:#7FE0A0; }
.side .dot { position:absolute; bottom:16mm; left:50%; transform:translateX(-50%); width:5mm; height:5mm; border-radius:50%; background:#24A24B; }
.kick { font-family:'Poppins'; font-weight:700; letter-spacing:2.5px; font-size:8.5pt; text-transform:uppercase; color:#1656C4; }
.h { font-size:26pt; font-weight:800; margin:2mm 0 3mm; }
.rule { width:22mm; height:4px; background:linear-gradient(90deg,#24A24B,#1656C4); border-radius:3px; margin-bottom:7mm; }
.lead { color:#33425f; font-size:11pt; }
.foot { position:absolute; left:30mm; right:18mm; bottom:10mm; border-top:1px solid #E2E8F2; padding-top:3mm; font-size:7.5pt; color:#8593ab; display:flex; justify-content:space-between; }

.stats { display:flex; gap:5mm; margin:9mm 0; }
.stats .s { flex:1; background:#F4F8FE; border:1px solid #E2E8F2; border-radius:12px; padding:6mm 4mm; }
.stats .s b { font-family:'Poppins'; font-weight:800; font-size:17pt; color:#1656C4; display:block; }
.stats .s span { font-size:8pt; color:#5C6E7A; }

.vm { display:flex; gap:7mm; margin-top:6mm; }
.vm .card { flex:1; border:1px solid #E2E8F2; border-radius:14px; padding:8mm; background:#fff; box-shadow:0 8px 22px rgba(12,40,90,.06); }
.vm .card .ic { width:13mm; height:13mm; border-radius:11px; background:#EAF1FF; display:flex; align-items:center; justify-content:center; margin-bottom:4mm; }
.vm .card .ic svg { width:7mm; height:7mm; }
.vm .card h3 { font-size:15pt; margin-bottom:3mm; }
.vm .card p { color:#4a5a76; font-size:9.5pt; }
.vm .card ul { margin:0; padding-left:5mm; color:#4a5a76; font-size:9.5pt; }
.vm .card li { margin-bottom:2mm; }

.catgrid { display:flex; flex-wrap:wrap; gap:5mm; margin-top:7mm; }
.catgrid .c { width:calc(50% - 2.5mm); border:1px solid #E2E8F2; border-left:4px solid #1656C4; border-radius:10px; padding:5mm 6mm; }
.catgrid .c h4 { font-size:11.5pt; margin-bottom:1.5mm; }
.catgrid .c p { font-size:8.8pt; color:#5C6E7A; margin:0; }

.whyg { display:flex; flex-wrap:wrap; gap:5mm; margin-top:7mm; }
.whyg .w { width:calc(50% - 2.5mm); display:flex; gap:4mm; }
.whyg .w .n { font-family:'Poppins'; font-weight:900; font-size:16pt; color:#CBD8EC; width:10mm; }
.whyg .w h4 { font-size:11pt; }
.whyg .w p { font-size:8.6pt; color:#5C6E7A; margin:1mm 0 0; }

.apps { display:flex; flex-wrap:wrap; gap:4mm; margin-top:7mm; }
.apps .a { width:calc(50% - 2mm); background:#F4F8FE; border-radius:9px; padding:4.5mm 5mm; font-family:'Poppins'; font-weight:600; color:#08214E; font-size:10.5pt; border-left:4px solid #24A24B; }
.reach { margin-top:8mm; background:linear-gradient(135deg,#08214E,#1656C4 130%); color:#fff; border-radius:14px; padding:7mm 8mm; }
.reach h3 { color:#fff; font-size:14pt; }
.reach p { color:#cfe0f5; font-size:10pt; margin:2mm 0 0; }

/* full-bleed cover + back */
.full { position:relative; width:210mm; height:297mm; overflow:hidden; background:linear-gradient(140deg,#071B44,#0C336F 55%,#123E86 120%); color:#fff; }
.full .tex1 { position:absolute; top:-50mm; right:-45mm; width:180mm; height:180mm; border-radius:40mm; background:rgba(255,255,255,.05); transform:rotate(20deg); }
.full .tex2 { position:absolute; bottom:-60mm; left:-45mm; width:150mm; height:150mm; border-radius:50%; background:rgba(46,116,232,.20); }
.full .inner { position:absolute; inset:0; padding:24mm 22mm; display:flex; flex-direction:column; z-index:2; }
.chip { background:#fff; border-radius:11px; padding:3mm 5mm; display:inline-block; align-self:flex-start; box-shadow:0 8px 20px rgba(0,0,0,.2); }
.chip img { height:13mm; width:auto; display:block; }
.cover .k { font-family:'Poppins'; font-weight:700; letter-spacing:4px; text-transform:uppercase; color:#7FE0A0; font-size:11pt; margin-top:14mm; }
.cover h1 { color:#fff; font-family:'Poppins'; font-weight:900; font-size:46pt; letter-spacing:-1px; margin:4mm 0; }
.cover .sub { color:#cfe0f5; font-size:12pt; max-width:150mm; }
.cover-hero { margin-top:auto; height:96mm; border-radius:16px; overflow:hidden; border:1px solid rgba(255,255,255,.2); box-shadow:0 16px 40px rgba(0,0,0,.35); }
.cover-hero img { width:100%; height:100%; object-fit:cover; display:block; }
.cover .foot { margin-top:6mm; display:flex; justify-content:space-between; font-size:9pt; color:#cfe0f5; }
.cover .foot b { color:#fff; }

.back h2 { color:#fff; font-family:'Poppins'; font-weight:900; font-size:32pt; margin-top:12mm; }
.back h2 em { color:#7FE0A0; font-style:normal; }
.back .p { color:#cfe0f5; font-size:11.5pt; margin-top:4mm; max-width:150mm; }
.back .cbox { margin-top:10mm; display:flex; gap:8mm; }
.back .cinfo div { font-size:11pt; color:#e6eefb; margin:2.5mm 0; }
.back .cinfo b { color:#fff; }
.back .qr { margin-left:auto; text-align:center; }
.back .qr img { width:34mm; height:34mm; background:#fff; padding:2.5mm; border-radius:8px; }
.back .qr span { display:block; font-size:8pt; color:#cfe0f5; margin-top:2mm; }
.back .end { margin-top:auto; border-top:1px solid rgba(255,255,255,.2); padding-top:5mm; font-size:8.5pt; color:#9fb6d8; }
"""


def _ic(path):
    return (f"<svg viewBox='0 0 24 24' fill='none' stroke='#1656C4' stroke-width='1.9' "
            f"stroke-linecap='round' stroke-linejoin='round'>{path}</svg>")


def _content(pg, secname, kick, title, inner):
    return f"""
<div class="page pb">
  <div class="side"><div class="pg">{pg}<small>PAGE</small></div><div class="sec">{secname}</div><div class="dot"></div></div>
  <div class="kick">{kick}</div><h1 class="h">{title}</h1><div class="rule"></div>
  {inner}
  <div class="foot"><span>{CO['name']} &middot; Company Profile</span><span>{CO['web']}</span></div>
</div>"""


def build_html():
    logo = _logo(); lg = _fileuri(logo); banner = _banner(); qr = _qr("https://bharationsystems.com")
    chip = f'<div class="chip"><img src="{lg}" alt=""></div>' if lg else ''

    cover = f"""
<div class="full cover"><div class="tex1"></div><div class="tex2"></div><div class="inner">
  {chip}
  <div class="k">Company Profile</div>
  <h1>Bharat <span style="color:#8FBEFF">iON</span> Systems</h1>
  <div class="sub">Manufacturer of water treatment &amp; bottle packaging machinery &mdash; from RO purification to a complete turnkey bottling line.</div>
  {f'<div class="cover-hero"><img src="{_fileuri(banner)}" alt=""></div>' if banner else ''}
  <div class="foot"><div><b>{CO['name']}</b></div><div>{CO['phone']} &nbsp;&middot;&nbsp; {CO['web']}</div></div>
</div></div>"""

    about_stats = "".join(f'<div class="s"><b>{a}</b><span>{b}</span></div>' for a, b in STATS)
    about = _content("01", "About Us", "Who We Are", "A Trusted Machinery Partner", f"""
  <p class="lead">{CO['name']} is a manufacturer and supplier of world-class machinery for the water,
  beverage and packaging industry. From reverse-osmosis purification to PET bottle blowing, filling,
  capping, labelling, coding and shrink packaging, we deliver individual machines and fully integrated
  turnkey lines &mdash; engineered for performance, hygiene and dependable, round-the-clock production.</p>
  <div class="stats">{about_stats}</div>
  <p style="color:#4a5a76">Headquartered in Karheda, Ghaziabad &mdash; in the heart of Delhi NCR &mdash; we
  supply, install and support bottling plants for entrepreneurs, established manufacturers, distributors and
  OEM buyers across India. Our promise is simple: help you produce more, reliably, with one accountable partner
  from plant design through installation, training and after-sales service.</p>""")

    vm = _content("02", "Vision & Mission", "Our Purpose", "Vision &amp; Mission", f"""
  <div class="vm">
    <div class="card"><div class="ic">{_ic("<path d='M12 5c-5 0-8 4-9 7 1 3 4 7 9 7s8-4 9-7c-1-3-4-7-9-7z'/><circle cx='12' cy='12' r='2.5'/>")}</div>
      <h3>Vision</h3><p>To be India's most trusted partner for water and beverage packaging machinery &mdash;
      enabling entrepreneurs to build safe, profitable and future-ready bottling businesses.</p></div>
    <div class="card"><div class="ic">{_ic("<circle cx='12' cy='12' r='9'/><circle cx='12' cy='12' r='4.5'/><circle cx='12' cy='12' r='1'/>")}</div>
      <h3>Mission</h3><ul>
        <li>Deliver reliable, hygienic, world-class machinery.</li>
        <li>Offer honest, manufacturer-direct value.</li>
        <li>Support customers end-to-end &mdash; install, train, service.</li>
        <li>Continuously improve design and efficiency.</li>
      </ul></div>
  </div>""")

    cats = "".join(f'<div class="c"><h4>{t}</h4><p>{d}</p></div>' for t, d in CATS)
    what = _content("03", "What We Do", "Our Capabilities", "Machinery We Manufacture", f"""
  <p class="lead">A complete range that covers every stage of a packaged-water and beverage line &mdash;
  available as standalone machines or a single, integrated turnkey plant.</p>
  <div class="catgrid">{cats}</div>""")

    whyg = "".join(f'<div class="w"><div class="n">{i+1:02d}</div><div><h4>{t}</h4><p>{d}</p></div></div>'
                   for i, (t, d) in enumerate(WHY))
    why = _content("04", "Why Choose Us", "Our Strengths", "Built Around Your Success", f'<div class="whyg">{whyg}</div>')

    apps = "".join(f'<div class="a">{a}</div>' for a in APPS)
    reach = _content("05", "Applications & Reach", "Where We Serve", "Applications &amp; Reach", f"""
  <div class="apps">{apps}</div>
  <div class="reach"><h3>From Ghaziabad to all of India</h3>
  <p>Based in Delhi NCR, we deliver, install and service machinery for customers in Ghaziabad, Delhi, Noida,
  Meerut and across the country &mdash; with prompt support and genuine spare parts.</p></div>""")

    back = f"""
<div class="full back"><div class="tex1"></div><div class="tex2"></div><div class="inner">
  {chip}
  <h2>Let's build your <em>bottling plant</em>.</h2>
  <div class="p">Share your target capacity and city &mdash; we'll prepare a tailored machine list and budget,
  then supply, install and support the complete line, end to end.</div>
  <div class="cbox">
    <div class="cinfo">
      <div><b>{CO['name']}</b></div>
      <div>&#9742;&nbsp; {CO['phone']}</div>
      <div>&#9993;&nbsp; {CO['email']}</div>
      <div>&#9737;&nbsp; {CO['web']}</div>
      <div style="max-width:100mm">&#9741;&nbsp; {CO['addr']}</div>
    </div>
    {f'<div class="qr"><img src="{qr}" alt=""><span>bharationsystems.com</span></div>' if qr else ''}
  </div>
  <div class="end">&copy; Bharat iON Systems Pvt. Ltd. &nbsp;&middot;&nbsp; Water Treatment &amp; Bottle Packaging Machinery</div>
</div></div>"""

    return (f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>"
            f"{cover}{about}{vm}{what}{why}{reach}{back}</body></html>")


def render_pdf():
    return HTML(string=build_html(), base_url=BASE).write_pdf()


if __name__ == "__main__":
    out = os.path.abspath(os.path.join(BASE, "..", "assets", "company-profile.pdf"))
    with open(out, "wb") as f:
        f.write(render_pdf())
    print("wrote", out, os.path.getsize(out) // 1024, "KB")
