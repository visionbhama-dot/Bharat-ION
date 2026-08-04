#!/usr/bin/env python3
"""
Bharat iON Systems - Product Catalogue (world-class A4 PDF)
-----------------------------------------------------------
Generates a bold, professional multi-page product brochure using WeasyPrint,
reusing the brand palette and the vector machine illustrations in
products_data.py. Run standalone to write ../assets/catalogue.pdf, or import
render_catalogue_pdf() from the Flask app.
"""
import os
import base64
import html as _html

from weasyprint import HTML

try:
    import products_data as pd
except Exception:  # pragma: no cover
    pd = None

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")

# ---- Brand palette ----
NAVY = "#08214E"
NAVY2 = "#0B3272"
BLUE = "#1656C4"
BLUEL = "#2E74E8"
GREEN = "#24A24B"
GREENL = "#7FE0A0"
RED = "#E23127"
GOLD = "#D8A84A"
INK = "#1A2740"
MUTED = "#5B6B86"
SOFT = "#EEF3FB"
LINE = "#E2E8F2"


def esc(s):
    return _html.escape(str(s), quote=True) if s is not None else ""


def _fileuri(path):
    return "file://" + os.path.abspath(path) if path and os.path.exists(path) else ""


def _logo():
    for ext in (".png", ".svg", ".jpg", ".jpeg", ".webp"):
        p = os.path.join(ASSETS, "logo" + ext)
        if os.path.exists(p):
            return p
    return None


def _qr_data_uri(text):
    """Best-effort QR code as a base64 PNG data URI (returns '' if unavailable)."""
    try:
        import qrcode
        img = qrcode.make(text)
        import io
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return ""


def _svg(key):
    if pd and key in getattr(pd, "SVGS", {}):
        return pd.SVGS[key]()
    return ""


# ---- Catalogue content ----
COMPANY = {
    "name": "Bharat iON Systems Pvt. Ltd.",
    "tag": "Water Treatment &amp; Bottle Packaging Machinery",
    "phone": "+91 83840 61695",
    "email": "info@bharationsystems.com",
    "web": "www.bharationsystems.com",
    "addr": "2882, 1st Floor, Karheda, Ghaziabad, Uttar Pradesh 201007",
}

STATS = [
    ("RO &rarr; Pack", "Complete turnkey line"),
    ("6000 BPH", "Up to, per line"),
    ("Turnkey", "Install &amp; training"),
    ("Pan-India", "Service &amp; spares"),
]

PROCESS = [
    ("1", "RO Purification"), ("2", "PET Blowing"), ("3", "Filling &amp; Capping"),
    ("4", "Labelling"), ("5", "Batch Coding"), ("6", "Shrink Packing"),
]

PRODUCTS = [
    {
        "key": "semi", "cat": "PET Bottle Manufacturing",
        "name": "Semi-Automatic PET Blowing Machine",
        "lead": "Dependable auto-drop stretch blow moulding for start-ups and growing plants.",
        "specs": [("Mould Cavities", "1 / 2"), ("Bottle Volume", "100 ml &ndash; 2 Litre"),
                  ("Output", "1000 &ndash; 1200 BPH"), ("Clamping Force", "8 Ton"),
                  ("Blowing Pressure", "18 &ndash; 26 kg/cm&sup2;"), ("Operation", "Hydro-Pneumatic")],
        "hl": ["Auto-drop preform system", "Infrared conveyor heating",
               "Quick mould changeover", "Compact, low-power footprint"],
    },
    {
        "key": "handblow", "cat": "PET Bottle Manufacturing",
        "name": "Hand-Feed Automatic PET Blowing Machine",
        "lead": "Automatic blow cycle with simple manual preform feeding &mdash; more output at low cost.",
        "specs": [("Mould Cavities", "2 / 4"), ("Bottle Volume", "100 ml &ndash; 2 Litre"),
                  ("Output", "1800 &ndash; 2500 BPH"), ("Heating", "Infrared Oven"),
                  ("Clamping", "Hydraulic"), ("Power", "12 &ndash; 18 kW")],
        "hl": ["Fully automatic blow cycle", "Manual feed keeps cost low",
               "Uniform wall thickness", "Simple, robust operation"],
    },
    {
        "key": "full", "cat": "PET Bottle Manufacturing",
        "name": "Fully Automatic PET Blowing Machine",
        "lead": "High-speed servo blow moulding with automatic preform loading for large plants.",
        "specs": [("Mould Cavities", "2 / 4 / 6"), ("Bottle Volume", "200 ml &ndash; 2 Litre"),
                  ("Output", "Up to 4000 &ndash; 6000 BPH"), ("Drive", "Servo"),
                  ("Control", "PLC + HMI"), ("Feeding", "Automatic Preform Feeder")],
        "hl": ["Servo stretch-blow system", "Rotary / linear options",
               "Air recovery for efficiency", "Consistent high-volume output"],
    },
    {
        "key": "ro", "cat": "Water Treatment",
        "name": "Industrial RO Water Treatment Plant",
        "lead": "Multi-stage reverse osmosis for safe, IS 10500-grade packaged drinking water.",
        "specs": [("Capacity", "250 &ndash; 10,000 LPH"), ("Pre-treatment", "Multimedia + Carbon + Softener"),
                  ("Membranes", "Spiral-wound TFC"), ("Dosing", "Antiscalant + Chlorine"),
                  ("Body", "SS / FRP"), ("Options", "UV + Ozone")],
        "hl": ["Turnkey plant sizing", "High recovery, low rejection",
               "Automatic operation & controls", "Ozonation & UV polishing options"],
    },
    {
        "key": "station", "cat": "Filling & Capping",
        "name": "Station Filler (Bottle Filling Machine)",
        "lead": "Economical multi-head filling for small and medium bottling lines.",
        "specs": [("Filling Heads", "4 &ndash; 8"), ("Bottle Volume", "200 ml &ndash; 5 Litre"),
                  ("Output", "500 &ndash; 1500 BPH"), ("Fill Type", "Gravity / Volumetric"),
                  ("Contact Parts", "SS 304 / 316"), ("Capping", "Manual / Semi-auto")],
        "hl": ["Hygienic stainless build", "Drip-free filling nozzles",
               "Adjustable fill volume", "Easy to clean & maintain"],
    },
    {
        "key": "fill", "cat": "Filling & Capping",
        "name": "Fully Automatic Rinsing, Filling & Capping Machine",
        "lead": "A 3-in-1 monobloc that rinses, fills and caps in one hygienic, high-speed operation.",
        "specs": [("Configuration", "24-18-6 / customisable"), ("Output", "2000 &ndash; 6000 BPH"),
                  ("Bottle Volume", "200 ml &ndash; 2 Litre"), ("Rinsing", "Gripper type"),
                  ("Capping", "Magnetic torque head"), ("Contact Parts", "SS 304 / 316")],
        "hl": ["Single synchronised monobloc", "No-bottle / no-fill sensing",
               "CIP-ready hygienic design", "Smooth, high-speed handling"],
    },
    {
        "key": "label", "cat": "Labelling",
        "name": "Automatic Sticker Labelling Machine",
        "lead": "Servo-controlled self-adhesive labelling for crisp, consistent branding.",
        "specs": [("Output", "Up to 6000 BPH"), ("Label Material", "OPP / BOPP / Paper"),
                  ("Bottle Shape", "Round"), ("Accuracy", "&plusmn; 1 mm"),
                  ("Control", "Servo + PLC"), ("Add-on", "Online date/batch coder")],
        "hl": ["Wrinkle-free application", "Fast, tool-less changeover",
               "Wrap-around & front/back", "Integrates with coding"],
    },
    {
        "key": "shrink", "cat": "Secondary Packaging",
        "name": "Automatic Shrink Wrapping Machine",
        "lead": "Groups bottles into transport-ready multi-packs through a heat-shrink tunnel.",
        "specs": [("Film", "LDPE / POF"), ("Output", "Up to 12 packs / min"),
                  ("Pack Sizes", "6 / 12 / 24"), ("Tunnel", "SS heat chamber"),
                  ("Control", "PLC"), ("Sealing", "Web sealer")],
        "hl": ["Web sealer + shrink tunnel", "Adjustable pack sizes",
               "Uniform, tight wrap", "Energy-efficient heating"],
    },
    {
        "key": "ink", "cat": "Coding & Marking",
        "name": "Batch Coding Machine",
        "lead": "High-resolution coding of batch, MFG/EXP dates and MRP at full line speed.",
        "specs": [("Type", "Inkjet (CIJ / DOD)"), ("Print Lines", "1 &ndash; 4"),
                  ("Speed", "Line-synchronised"), ("Ink", "Food-grade, fast-dry"),
                  ("Interface", "Touchscreen"), ("Codes", "Text / Logo / Barcode")],
        "hl": ["Non-contact printing", "Fast-drying inks",
               "Logo & barcode support", "Low maintenance"],
    },
]

APPLICATIONS = [
    "Packaged Drinking Water Plants", "Mineral Water Bottling Units",
    "Beverage &amp; Juice Filling Lines", "Carbonated Soft Drink Plants",
    "Dairy &amp; Liquid Packaging", "Distributors, Dealers &amp; OEM Buyers",
]

WHY = [
    ("Single Accountable Partner", "One team supplies, installs and supports your entire line."),
    ("Right-Sized For You", "Configurations matched to your output, budget and space."),
    ("Installation &amp; Training", "On-site commissioning and operator training included."),
    ("Genuine Spares &amp; Service", "Prompt after-sales support and authentic spare parts."),
    ("Manufacturer Pricing", "Direct-from-maker value, no middlemen."),
    ("Robust, Hygienic Builds", "Food-grade stainless construction built to last."),
]


CSS = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800;900&family=Inter:wght@400;500;600;700&display=swap');
@page { size:A4; margin:20mm 15mm 16mm 15mm;
  @top-right { content:"BHARAT iON SYSTEMS  \\00b7  Product Catalogue"; font-family:'Poppins'; font-weight:700; font-size:7.5pt; color:#1656C4; }
  @bottom-left { content:"www.bharationsystems.com"; font-family:'Inter'; font-size:7.5pt; color:#8aa0c0; }
  @bottom-right { content:"Page " counter(page); font-family:'Inter'; font-size:7.5pt; color:#8aa0c0; }
}
@page cover { margin:0; @top-right{content:none} @bottom-left{content:none} @bottom-right{content:none} }
@page back  { margin:0; @top-right{content:none} @bottom-left{content:none} @bottom-right{content:none} }
* { box-sizing:border-box; }
body { font-family:'Inter',sans-serif; color:#1A2740; margin:0; font-size:10.5pt; line-height:1.5; }
h1,h2,h3,h4 { font-family:'Poppins',sans-serif; margin:0; color:#08214E; line-height:1.1; }
.cover { page:cover; }
.back { page:back; }
.pb { page-break-before:always; }

/* ---------- COVER ---------- */
.cover-wrap { position:relative; width:210mm; height:297mm; overflow:hidden;
  background:linear-gradient(150deg,#08214E 0%,#0B3272 55%,#1656C4 120%); color:#fff; }
.cover-blob { position:absolute; border-radius:50%; }
.cover-inner { position:absolute; inset:0; padding:26mm 22mm; display:flex; flex-direction:column; }
.cover img.logo { height:20mm; width:auto; margin-bottom:auto; }
.cover .ey { font-family:'Poppins'; font-weight:700; letter-spacing:3px; font-size:10pt; color:#7FE0A0; text-transform:uppercase; }
.cover h1 { color:#fff; font-size:52pt; font-weight:900; letter-spacing:-1px; margin:6mm 0 4mm; }
.cover h1 .g { color:#7FE0A0; }
.cover .sub { font-size:13pt; color:#cfe0f5; max-width:150mm; }
.cover .yr { margin-top:6mm; font-family:'Poppins'; font-weight:700; font-size:11pt; color:#D8A84A; }
.cover .strip { display:flex; gap:6mm; margin-top:12mm; }
.cover .strip .chip { flex:1; background:rgba(255,255,255,.08); border:1px solid rgba(255,255,255,.18);
  border-radius:10px; padding:5mm; }
.cover .strip .chip svg { width:100%; height:26mm; display:block; }
.cover .foot { margin-top:auto; display:flex; justify-content:space-between; align-items:flex-end;
  border-top:1px solid rgba(255,255,255,.2); padding-top:5mm; font-size:9.5pt; color:#cfe0f5; }
.cover .foot b { color:#fff; font-family:'Poppins'; }

/* ---------- SECTION HEADERS ---------- */
.kicker { font-family:'Poppins'; font-weight:700; letter-spacing:2px; font-size:8pt; text-transform:uppercase;
  color:#1656C4; }
.sec-title { font-size:24pt; font-weight:800; margin:2mm 0 3mm; }
.rule { height:4px; width:22mm; background:linear-gradient(90deg,#24A24B,#1656C4,#E23127); border-radius:3px; margin-bottom:6mm; }
.lead { color:#5B6B86; font-size:11pt; max-width:165mm; }

/* ---------- INTRO ---------- */
.stats { display:flex; gap:5mm; margin:8mm 0; }
.stats .s { flex:1; background:#EEF3FB; border:1px solid #E2E8F2; border-radius:12px; padding:6mm 5mm; }
.stats .s b { display:block; font-family:'Poppins'; font-weight:800; font-size:16pt; color:#08214E; }
.stats .s span { font-size:8.5pt; color:#5B6B86; }
.flow { display:flex; align-items:flex-start; justify-content:space-between; margin-top:6mm; }
.flow .node { text-align:center; width:15%; }
.flow .dot { width:13mm; height:13mm; border-radius:50%; background:#1656C4; color:#fff; font-family:'Poppins';
  font-weight:800; font-size:14pt; display:flex; align-items:center; justify-content:center; margin:0 auto 3mm;
  border:3px solid #cfe0f5; }
.flow .node b { font-size:8pt; color:#08214E; display:block; }

/* ---------- PRODUCT PAGE ---------- */
.prod { padding-top:2mm; }
.ptag { display:inline-block; background:#08214E; color:#fff; font-family:'Poppins'; font-weight:700;
  font-size:7.5pt; letter-spacing:1px; text-transform:uppercase; padding:2mm 4mm; border-radius:20px; }
.prod h2 { font-size:22pt; font-weight:800; margin:3mm 0 2mm; }
.prod .lead { font-size:11pt; color:#33425f; margin-bottom:5mm; }
.pvisual { background:linear-gradient(180deg,#F3FAFD,#DCF0F7); border:1px solid #E2E8F2; border-radius:16px;
  padding:6mm; height:78mm; display:flex; align-items:center; justify-content:center; }
.pvisual svg { width:100%; height:100%; }
.pcols { display:flex; gap:7mm; margin-top:6mm; }
.pcols .box { flex:1; }
.pcols h3 { font-size:11pt; color:#08214E; margin-bottom:3mm; padding-bottom:2mm; border-bottom:2px solid #1656C4; display:inline-block; }
.spec { width:100%; border-collapse:collapse; font-size:9.5pt; }
.spec td { padding:2.4mm 0; border-bottom:1px solid #E2E8F2; }
.spec td.k { color:#5B6B86; }
.spec td.v { text-align:right; font-weight:600; color:#08214E; }
.feat { list-style:none; padding:0; margin:0; }
.feat li { position:relative; padding:2mm 0 2mm 7mm; font-size:9.8pt; color:#33425f; border-bottom:1px solid #F0F4FA; }
.feat li:before { content:""; position:absolute; left:0; top:3mm; width:4mm; height:4mm; border-radius:50%;
  background:#24A24B; }

/* ---------- APPLICATIONS / WHY (grids) ---------- */
.grid2 { display:flex; flex-wrap:wrap; gap:5mm; margin-top:6mm; }
.grid2 .card { width:calc(50% - 2.5mm); background:#fff; border:1px solid #E2E8F2; border-radius:12px; padding:6mm; }
.grid2 .card h4 { font-size:11pt; color:#08214E; margin-bottom:2mm; }
.grid2 .card p { margin:0; font-size:9.5pt; color:#5B6B86; }
.applist { display:flex; flex-wrap:wrap; gap:4mm; margin-top:6mm; }
.applist .a { width:calc(50% - 2mm); background:#EEF3FB; border-left:4px solid #24A24B; border-radius:8px;
  padding:4.5mm 5mm; font-weight:600; color:#08214E; font-size:10.5pt; }

/* section divider (full colour) */
.divider { page:cover; }
.divider-wrap { width:210mm; height:297mm; background:linear-gradient(135deg,#08214E,#1656C4 130%); color:#fff;
  display:flex; flex-direction:column; justify-content:center; padding:0 26mm; position:relative; overflow:hidden; }
.divider-wrap .n { font-family:'Poppins'; font-weight:900; font-size:120pt; color:rgba(255,255,255,.08); position:absolute; top:20mm; right:22mm; }
.divider-wrap .k { font-family:'Poppins'; font-weight:700; letter-spacing:3px; text-transform:uppercase; color:#7FE0A0; font-size:11pt; }
.divider-wrap h2 { color:#fff; font-size:40pt; font-weight:900; margin:4mm 0; max-width:150mm; }
.divider-wrap p { color:#cfe0f5; font-size:12pt; max-width:140mm; }

/* ---------- BACK COVER ---------- */
.back-wrap { width:210mm; height:297mm; background:linear-gradient(150deg,#08214E,#0B3272 120%); color:#fff;
  padding:26mm 22mm; display:flex; flex-direction:column; }
.back-wrap img.logo { height:18mm; width:auto; margin-bottom:12mm; }
.back-wrap h2 { color:#fff; font-size:34pt; font-weight:900; }
.back-wrap h2 .g { color:#7FE0A0; }
.back-wrap .p { color:#cfe0f5; font-size:12pt; max-width:150mm; margin-top:4mm; }
.back-cta { display:inline-block; margin-top:8mm; background:#E23127; color:#fff; font-family:'Poppins';
  font-weight:700; padding:5mm 10mm; border-radius:10px; font-size:12pt; }
.contact { margin-top:auto; display:flex; justify-content:space-between; align-items:flex-end;
  border-top:1px solid rgba(255,255,255,.2); padding-top:6mm; }
.contact .info div { margin:1.5mm 0; font-size:10.5pt; color:#e6eefb; }
.contact .info b { color:#fff; }
.contact .qr { text-align:center; }
.contact .qr img { width:30mm; height:30mm; background:#fff; padding:2mm; border-radius:8px; }
.contact .qr span { display:block; font-size:8pt; color:#cfe0f5; margin-top:2mm; }
"""


def _cover():
    logo = _logo()
    logo_img = f'<img class="logo" src="{_fileuri(logo)}" alt="">' if logo else ''
    chips = "".join(f'<div class="chip">{_svg(k)}</div>' for k in ("ro", "full", "fill"))
    return f"""
<div class="cover"><div class="cover-wrap">
  <div class="cover-blob" style="width:180mm;height:180mm;background:rgba(36,162,75,.14);top:-70mm;right:-60mm"></div>
  <div class="cover-blob" style="width:120mm;height:120mm;background:rgba(226,49,39,.10);bottom:-50mm;left:-40mm"></div>
  <div class="cover-inner">
    {logo_img}
    <div class="ey">Product Catalogue</div>
    <h1>Complete <span class="g">Water Bottling</span><br>&amp; Packaging Machinery</h1>
    <div class="sub">RO plants, PET blowing, filling &amp; capping, labelling, coding and shrink packaging &mdash; individual machines or a fully integrated turnkey line.</div>
    <div class="yr">Edition 2026</div>
    <div class="strip">{chips}</div>
    <div class="foot">
      <div><b>{COMPANY['name']}</b><br>{COMPANY['tag']}</div>
      <div style="text-align:right">{COMPANY['phone']}<br>{COMPANY['web']}</div>
    </div>
  </div>
</div></div>"""


def _intro():
    stats = "".join(f'<div class="s"><b>{a}</b><span>{b}</span></div>' for a, b in STATS)
    flow = "".join(f'<div class="node"><div class="dot">{n}</div><b>{t}</b></div>' for n, t in PROCESS)
    return f"""
<section class="pb">
  <div class="kicker">Who We Are</div>
  <h2 class="sec-title">One Partner, The Complete Line</h2>
  <div class="rule"></div>
  <p class="lead">{COMPANY['name']} manufactures and supplies world-class machinery for the
  water treatment, beverage and packaging industry. From reverse-osmosis purification to
  bottle blowing, filling, labelling, coding and shrink packaging &mdash; we help you produce
  more, reliably, with a single accountable partner from design to after-sales support.</p>
  <div class="stats">{stats}</div>
  <div class="kicker">The Production Flow</div>
  <h3 style="font-size:15pt;margin:2mm 0 4mm">From Raw Water to Ready-to-Ship Packs</h3>
  <div class="flow">{flow}</div>
</section>"""


def _divider(num, kicker, title, sub):
    return f"""
<div class="divider"><div class="divider-wrap">
  <div class="n">{num}</div>
  <div class="k">{kicker}</div>
  <h2>{title}</h2>
  <p>{sub}</p>
</div></div>"""


def _product(p):
    specs = "".join(f'<tr><td class="k">{k}</td><td class="v">{v}</td></tr>' for k, v in p["specs"])
    feats = "".join(f'<li>{h}</li>' for h in p["hl"])
    return f"""
<section class="pb prod">
  <span class="ptag">{p['cat']}</span>
  <h2>{p['name']}</h2>
  <div class="lead">{p['lead']}</div>
  <div class="pvisual">{_svg(p['key'])}</div>
  <div class="pcols">
    <div class="box"><h3>Key Specifications</h3>
      <table class="spec">{specs}</table></div>
    <div class="box"><h3>Highlights</h3>
      <ul class="feat">{feats}</ul></div>
  </div>
</section>"""


def _applications():
    apps = "".join(f'<div class="a">{a}</div>' for a in APPLICATIONS)
    return f"""
<section class="pb">
  <div class="kicker">Where It's Used</div>
  <h2 class="sec-title">Applications &amp; Industries</h2>
  <div class="rule"></div>
  <p class="lead">Our machinery powers packaging lines across a wide range of liquids and businesses.</p>
  <div class="applist">{apps}</div>
</section>"""


def _why():
    cards = "".join(f'<div class="card"><h4>{t}</h4><p>{d}</p></div>' for t, d in WHY)
    return f"""
<section class="pb">
  <div class="kicker">Why Bharat iON</div>
  <h2 class="sec-title">Built Around Your Success</h2>
  <div class="rule"></div>
  <div class="grid2">{cards}</div>
</section>"""


def _back():
    logo = _logo()
    logo_img = f'<img class="logo" src="{_fileuri(logo)}" alt="">' if logo else ''
    qr = _qr_data_uri("https://bharationsystems.com")
    qr_html = (f'<div class="qr"><img src="{qr}" alt=""><span>bharationsystems.com</span></div>' if qr else '')
    return f"""
<div class="back"><div class="back-wrap">
  {logo_img}
  <h2>Let's build your <span class="g">bottling plant</span>.</h2>
  <div class="p">Tell us your target capacity and city &mdash; we'll prepare a tailored machine list and budget, then supply, install and support the complete line.</div>
  <div><span class="back-cta">Get a Free Quote &amp; Plant Plan</span></div>
  <div class="contact">
    <div class="info">
      <div><b>{COMPANY['name']}</b></div>
      <div>&#9742; {COMPANY['phone']}</div>
      <div>&#9993; {COMPANY['email']}</div>
      <div>&#9737; {COMPANY['web']}</div>
      <div style="max-width:95mm">&#9741; {COMPANY['addr']}</div>
    </div>
    {qr_html}
  </div>
</div></div>"""


def build_html():
    parts = [_cover(), _intro(),
             _divider("01", "Machinery Range", "Our Machinery, In Detail",
                      "Nine core machines that together form a complete packaged-water and beverage line.")]
    parts += [_product(p) for p in PRODUCTS]
    parts += [_applications(), _why(), _back()]
    return ("<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'>"
            f"<style>{CSS}</style></head><body>{''.join(parts)}</body></html>")


def render_catalogue_pdf():
    return HTML(string=build_html(), base_url=BASE).write_pdf()


if __name__ == "__main__":
    out = os.path.abspath(os.path.join(BASE, "..", "assets", "catalogue.pdf"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "wb") as f:
        f.write(render_catalogue_pdf())
    print("wrote", out, os.path.getsize(out) // 1024, "KB")
