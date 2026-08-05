#!/usr/bin/env python3
"""
Bharat iON Systems - Product Catalogue (bold full-bleed blue poster style)
--------------------------------------------------------------------------
Each page is a full-bleed brand-blue poster: wordmark + TYPE badge, big bold
title, large product photo card, bright stat tiles, feature icon tiles and a
short description. Rendered with WeasyPrint.
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


def esc(s):
    return _html.escape(str(s), quote=True) if s is not None else ""


def _fileuri(path):
    return "file://" + os.path.abspath(path) if path and os.path.exists(path) else ""


def _root_asset(*p):
    return os.path.join(BASE, "..", "assets", *p)


def _logo():
    for ext in (".png", ".svg", ".jpg", ".jpeg", ".webp"):
        p = os.path.join(ASSETS, "logo" + ext)
        if os.path.exists(p):
            return p
    return None


def _product_photo(key):
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        p = os.path.join(ASSETS, "products", str(key) + ext)
        if os.path.exists(p):
            return p
    return None


def _svg(key):
    if pd and key in getattr(pd, "SVGS", {}):
        return pd.SVGS[key]()
    return ""


def _visual(key):
    photo = _product_photo(key)
    return f'<img src="{_fileuri(photo)}" alt="">' if photo else _svg(key)


def _banner():
    for name in ("hero-banner", "process-bg"):
        for ext in (".jpg", ".jpeg", ".png", ".webp"):
            p = _root_asset("images", "banner", name + ext)
            if os.path.exists(p):
                return p
    return _product_photo("ro")


def _qr(text):
    try:
        import qrcode, io
        buf = io.BytesIO()
        qrcode.make(text).save(buf, format="PNG")
        return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return ""


ICONS = {
    "bolt": "<path d='M13 3 6 13h5l-1 8 8-12h-5z'/>",
    "gauge": "<path d='M4 15a8 8 0 0 1 16 0'/><path d='M12 15l4-4'/><circle cx='12' cy='15' r='1'/>",
    "drop": "<path d='M12 3c4 6 6 8 6 11a6 6 0 0 1-12 0c0-3 2-5 6-11z'/>",
    "gear": "<circle cx='12' cy='12' r='3'/><path d='M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M5 19l2-2'/>",
    "shield": "<path d='M12 3l7 3v5c0 4-3 7-7 8-4-1-7-4-7-8V6z'/><path d='M9 12l2 2 4-4'/>",
    "leaf": "<path d='M20 4C9 4 4 11 4 20c9 0 16-5 16-16z'/><path d='M4 20C8 14 13 10 18 8'/>",
    "clock": "<circle cx='12' cy='12' r='8'/><path d='M12 8v4l3 2'/>",
    "wrench": "<path d='M14.5 6.5a3.5 3.5 0 0 0-4.9 4.9l-6 6 2 2 6-6a3.5 3.5 0 0 0 4.9-4.9l-2.1 2.1-2-2z'/>",
    "barcode": "<path d='M4 5v14M8 5v14M11 5v14M15 5v14M18 5v14M20 5v14'/>",
}


def icon(name):
    return (f"<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.9' "
            f"stroke-linecap='round' stroke-linejoin='round'>{ICONS.get(name, '')}</svg>")


COMPANY = {
    "name": "Bharat iON Systems Pvt. Ltd.", "tag": "Water Treatment & Bottle Packaging Machinery",
    "phone": "+91 83840 61695", "email": "info@bharationsystems.com",
    "web": "www.bharationsystems.com", "addr": "2882, 1st Floor, Karheda, Ghaziabad, Uttar Pradesh 201007",
}
STATS = [("RO&rarr;Pack", "Complete line"), ("6000", "BPH, up to"), ("09", "Core machines"), ("Pan-India", "Service")]
PROCESS = [("1", "RO Purification"), ("2", "PET Blowing"), ("3", "Filling &amp; Capping"),
           ("4", "Labelling"), ("5", "Batch Coding"), ("6", "Shrink Packing")]

PRODUCTS = [
    {"key": "semi", "cat": "PET Bottle Manufacturing", "name": "Semi-Automatic PET Blowing Machine",
     "lead": "A dependable auto-drop stretch blow moulding machine for start-ups and growing plants \u2014 hygienic PET bottles with a compact footprint and low running cost.",
     "specs": [("Mould Cavities", "1 / 2"), ("Bottle Volume", "100 ml &ndash; 2 L"), ("Output", "1000 &ndash; 1200 BPH"),
               ("Clamping Force", "8 Ton"), ("Blowing Pressure", "18 &ndash; 26 kg/cm&sup2;"), ("Operation", "Hydro-Pneumatic")]},
    {"key": "handblow", "cat": "PET Bottle Manufacturing", "name": "Hand-Feed Automatic PET Blowing Machine",
     "lead": "An automatic blow cycle with simple manual preform feeding \u2014 higher output at low cost with consistent bottle quality.",
     "specs": [("Mould Cavities", "2 / 4"), ("Bottle Volume", "100 ml &ndash; 2 L"), ("Output", "1800 &ndash; 2500 BPH"),
               ("Heating", "Infrared Oven"), ("Clamping", "Hydraulic"), ("Power", "12 &ndash; 18 kW")]},
    {"key": "full", "cat": "PET Bottle Manufacturing", "name": "Fully Automatic PET Blowing Machine",
     "lead": "High-speed servo blow moulding with automatic preform loading for large plants \u2014 built for consistent, high-volume production.",
     "specs": [("Mould Cavities", "2 / 4 / 6"), ("Bottle Volume", "200 ml &ndash; 2 L"), ("Output", "Up to 6000 BPH"),
               ("Drive", "Servo"), ("Control", "PLC + HMI"), ("Feeding", "Auto Preform Feeder")]},
    {"key": "ro", "cat": "Water Treatment", "name": "Industrial RO Water Treatment Plant",
     "lead": "Multi-stage reverse osmosis for safe, IS 10500-grade packaged drinking water \u2014 turnkey plants sized to your capacity with automatic operation.",
     "specs": [("Capacity", "250 &ndash; 10,000 LPH"), ("Pre-treatment", "MMF + Carbon + Softener"), ("Membranes", "Spiral-wound TFC"),
               ("Dosing", "Antiscalant + Chlorine"), ("Body", "SS / FRP"), ("Options", "UV + Ozone")]},
    {"key": "station", "cat": "Filling & Capping", "name": "Station Filler (Bottle Filling Machine)",
     "lead": "Economical multi-head filling for small and medium bottling lines \u2014 hygienic stainless build with drip-free, adjustable filling.",
     "specs": [("Filling Heads", "4 &ndash; 8"), ("Bottle Volume", "200 ml &ndash; 5 L"), ("Output", "500 &ndash; 1500 BPH"),
               ("Fill Type", "Gravity / Volumetric"), ("Contact Parts", "SS 304 / 316"), ("Capping", "Manual / Semi-auto")]},
    {"key": "fill", "cat": "Filling & Capping", "name": "Automatic Rinsing Filling & Capping Machine",
     "lead": "A 3-in-1 monobloc that rinses, fills and caps in one hygienic, high-speed operation \u2014 the heart of a modern bottling line.",
     "specs": [("Configuration", "24-18-6 / custom"), ("Output", "2000 &ndash; 6000 BPH"), ("Bottle Volume", "200 ml &ndash; 2 L"),
               ("Rinsing", "Gripper type"), ("Capping", "Magnetic torque"), ("Contact Parts", "SS 304 / 316")]},
    {"key": "label", "cat": "Labelling", "name": "Automatic Sticker Labelling Machine",
     "lead": "Servo-controlled self-adhesive labelling for crisp, consistent branding \u2014 wrinkle-free application at high speed.",
     "specs": [("Output", "Up to 6000 BPH"), ("Label Material", "OPP / BOPP / Paper"), ("Bottle Shape", "Round"),
               ("Accuracy", "&plusmn; 1 mm"), ("Control", "Servo + PLC"), ("Add-on", "Online coder")]},
    {"key": "shrink", "cat": "Secondary Packaging", "name": "Automatic Shrink Wrapping Machine",
     "lead": "Groups bottles into transport-ready multi-packs through a heat-shrink tunnel \u2014 tight, uniform wraps with energy-efficient heating.",
     "specs": [("Film", "LDPE / POF"), ("Output", "Up to 12 packs/min"), ("Pack Sizes", "6 / 12 / 24"),
               ("Tunnel", "SS heat chamber"), ("Control", "PLC"), ("Sealing", "Web sealer")]},
    {"key": "ink", "cat": "Coding & Marking", "name": "Batch Coding Machine",
     "lead": "High-resolution non-contact coding of batch, MFG/EXP dates and MRP at full line speed \u2014 fast-drying, food-grade inks.",
     "specs": [("Type", "Inkjet (CIJ / DOD)"), ("Print Lines", "1 &ndash; 4"), ("Speed", "Line-synced"),
               ("Ink", "Food-grade, fast-dry"), ("Interface", "Touchscreen"), ("Codes", "Text / Logo / Barcode")]},
]

EXTRA = {
    "semi": {"model": "BIS-SB2",
             "badges": [("1200", "BPH", "Max Output"), ("8", "Ton", "Clamping")],
             "features": [("gear", "Auto-Drop System"), ("bolt", "Low Power Use"), ("clock", "Quick Mould Change"), ("shield", "1-Year Warranty")]},
    "handblow": {"model": "BIS-HB4",
                 "badges": [("2500", "BPH", "Max Output"), ("4", "Cav.", "Cavities")],
                 "features": [("gear", "Automatic Cycle"), ("bolt", "Cost-Efficient"), ("drop", "Even Walls"), ("wrench", "Easy Service")]},
    "full": {"model": "BIS-FA6",
             "badges": [("6000", "BPH", "Max Output"), ("6", "Cav.", "Cavities")],
             "features": [("gear", "Servo Stretch-Blow"), ("leaf", "Air Recovery"), ("bolt", "High Speed"), ("shield", "Robust Build")]},
    "ro": {"model": "BIS-RO",
           "badges": [("10000", "LPH", "Max Capacity"), ("4+", "Stage", "Pre-treatment")],
           "features": [("drop", "IS 10500 Water"), ("gear", "Auto Controls"), ("leaf", "High Recovery"), ("shield", "SS / FRP Build")]},
    "station": {"model": "BIS-SF8",
                "badges": [("1500", "BPH", "Max Output"), ("8", "Head", "Filling")],
                "features": [("drop", "Drip-Free Nozzles"), ("gear", "Adjustable Fill"), ("shield", "Hygienic Build"), ("wrench", "Easy to Clean")]},
    "fill": {"model": "BIS-RFC",
             "badges": [("6000", "BPH", "Max Output"), ("3-in-1", "", "Monobloc")],
             "features": [("gear", "Synchronised"), ("drop", "No-Bottle No-Fill"), ("shield", "SS 304 / 316"), ("clock", "High-Speed")]},
    "label": {"model": "BIS-LB",
              "badges": [("6000", "BPH", "Max Output"), ("&plusmn;1", "mm", "Accuracy")],
              "features": [("gear", "Servo Controlled"), ("bolt", "Wrinkle-Free"), ("clock", "Fast Changeover"), ("barcode", "Coder-Ready")]},
    "shrink": {"model": "BIS-SW",
               "badges": [("12", "/min", "Packs"), ("24", "pack", "Max Size")],
               "features": [("gear", "Web Sealer + Tunnel"), ("leaf", "Energy Saving"), ("shield", "Tight Wrap"), ("wrench", "Low Upkeep")]},
    "ink": {"model": "BIS-BC",
            "badges": [("4", "Lines", "Print Lines"), ("HD", "", "Resolution")],
            "features": [("bolt", "Non-Contact"), ("clock", "Fast-Drying"), ("barcode", "Logo + Barcode"), ("wrench", "Low Maintenance")]},
}

APPLICATIONS = ["Packaged Drinking Water Plants", "Mineral Water Bottling Units", "Beverage &amp; Juice Filling",
                "Carbonated Soft Drink Plants", "Dairy &amp; Liquid Packaging", "Distributors, Dealers &amp; OEM"]
WHY = [("Single Accountable Partner", "One team supplies, installs and supports your whole line."),
       ("Right-Sized For You", "Configurations matched to your output, budget and space."),
       ("Installation &amp; Training", "On-site commissioning and operator training included."),
       ("Genuine Spares &amp; Service", "Prompt after-sales support and authentic spare parts."),
       ("Manufacturer Pricing", "Direct-from-maker value, with no middlemen."),
       ("Robust, Hygienic Builds", "Food-grade stainless construction, built to last.")]


CSS = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800;900&family=Inter:wght@400;500;600;700&display=swap');
* { box-sizing:border-box; }
body { margin:0; font-family:'Inter',sans-serif; color:#fff; }
h1,h2,h3 { font-family:'Poppins',sans-serif; margin:0; line-height:1.05; }
@page { size:A4; margin:0; }
.page { position:relative; width:210mm; height:297mm; overflow:hidden; padding:15mm 15mm 13mm; display:flex; flex-direction:column;
  background:linear-gradient(140deg,#071B44 0%,#0C336F 55%,#123E86 120%); color:#fff; }
.pb { page-break-before:always; }
.tex1 { position:absolute; top:-55mm; right:-45mm; width:170mm; height:170mm; background:rgba(255,255,255,.05); border-radius:34mm; transform:rotate(22deg); }
.tex2 { position:absolute; bottom:-60mm; left:-45mm; width:150mm; height:150mm; border-radius:50%; background:rgba(46,116,232,.20); }
.z { position:relative; z-index:2; flex:1; display:flex; flex-direction:column; }

.wm { font-family:'Poppins'; font-weight:800; font-size:12pt; letter-spacing:.5px; color:#fff; }
.wm em { color:#7FE0A0; font-style:normal; }
.wm small { display:block; font-family:'Inter'; font-weight:500; font-size:7pt; letter-spacing:2px; color:#9DC4FF; text-transform:uppercase; }
.tophead { display:flex; justify-content:space-between; align-items:center; }
.type { display:inline-flex; align-items:stretch; border-radius:30px; overflow:hidden; font-family:'Poppins'; font-weight:700; font-size:8.5pt; border:1px solid rgba(255,255,255,.35); }
.type b { background:#fff; color:#08214E; padding:2.4mm 5mm; letter-spacing:1px; }
.type span { padding:2.4mm 6mm; color:#fff; letter-spacing:1.5px; }

.kick { font-family:'Poppins'; font-weight:700; letter-spacing:3px; font-size:8.5pt; text-transform:uppercase; color:#7FE0A0; }
.ptitle { font-family:'Poppins'; font-weight:900; font-size:25pt; color:#fff; letter-spacing:-.5px; margin:3mm 0 0; max-width:150mm; }
.ptitle em { color:#8FBEFF; font-style:normal; }
.tagline { display:inline-block; margin-top:4mm; background:linear-gradient(90deg,rgba(255,255,255,.16),rgba(255,255,255,0)); border-left:3px solid #7FE0A0; padding:2.2mm 6mm; font-size:8.5pt; letter-spacing:2px; text-transform:uppercase; color:#dfeaff; }

.hero { display:flex; gap:7mm; margin-top:6mm; align-items:stretch; }
.hero .left { width:44%; display:flex; flex-direction:column; gap:5mm; }
.hero .right { flex:1; }
.photocard { background:#fff; border-radius:16px; padding:5mm; height:80mm; display:flex; align-items:center; justify-content:center;
  box-shadow:0 12px 30px rgba(0,0,0,.28); }
.photocard img { max-width:100%; max-height:100%; object-fit:contain; }
.photocard svg { width:100%; height:100%; }

.stat { background:linear-gradient(160deg,#1C61D6,#1147A8); border:1px solid rgba(255,255,255,.28); border-radius:14px; padding:6mm 5mm; flex:1;
  display:flex; flex-direction:column; justify-content:center; box-shadow:0 8px 18px rgba(0,0,0,.18); }
.stat .v { font-family:'Poppins'; font-weight:900; font-size:32pt; color:#fff; line-height:.95; }
.stat .v span { font-size:12pt; color:#BcD8FF; font-weight:700; margin-left:1.5mm; }
.stat .l { font-size:8pt; letter-spacing:2px; text-transform:uppercase; color:#Bcd5f7; margin-top:3mm; }
.stat .ln { width:14mm; height:3px; background:#7FE0A0; border-radius:2px; margin-top:4mm; }

.feats { display:flex; gap:4mm; margin-top:5mm; align-items:stretch; }
.feat { flex:1; background:rgba(255,255,255,.09); border:1px solid rgba(255,255,255,.2); border-radius:13px; padding:4mm 2.5mm; text-align:center; overflow:hidden; display:flex; flex-direction:column; align-items:center; justify-content:flex-start; }
.feat .ic { width:10mm; height:10mm; border-radius:50%; background:rgba(143,190,255,.18); color:#8FBEFF; display:flex; align-items:center; justify-content:center; margin:0 auto 2.5mm; flex:none; }
.feat .ic svg { width:5mm; height:5mm; }
.feat span { font-size:7.4pt; font-weight:600; color:#eaf1ff; line-height:1.25; }

.specrow { display:flex; gap:7mm; margin-top:5mm; }
.specpanel { flex:1; background:rgba(255,255,255,.07); border:1px solid rgba(255,255,255,.16); border-radius:13px; padding:4.5mm 5mm; }
.specpanel .lbl { font-family:'Poppins'; font-weight:700; font-size:8pt; letter-spacing:2px; text-transform:uppercase; color:#7FE0A0; margin-bottom:3mm; }
.spec2 { display:flex; gap:8mm; }
.spec2 > div { flex:1; }
.spec { width:100%; border-collapse:collapse; font-size:8.6pt; }
.spec td { padding:2mm 0; border-bottom:1px solid rgba(255,255,255,.13); }
.spec td.k { color:#Aec3e8; }
.spec td.v { text-align:right; font-weight:700; color:#fff; }
.desc { margin-top:auto; padding-top:6mm; display:flex; justify-content:space-between; align-items:flex-end; gap:10mm; }
.desc p { font-size:8.4pt; color:#c8d7ef; max-width:120mm; line-height:1.5; margin:0; }
.desc .web { font-family:'Poppins'; font-weight:700; font-size:8pt; color:#7FE0A0; white-space:nowrap; }

/* ---------- COVER ---------- */
.cover-hero { margin-top:7mm; flex:1; min-height:95mm; border-radius:16px; overflow:hidden; box-shadow:0 16px 40px rgba(0,0,0,.35); border:1px solid rgba(255,255,255,.2); }
.cover-hero img { width:100%; height:100%; object-fit:cover; display:block; }
.cover h1 { font-family:'Poppins'; font-weight:900; font-size:40pt; letter-spacing:-1px; margin-top:6mm; max-width:175mm; }
.cover h1 em { color:#8FBEFF; font-style:normal; }
.cover .sub { color:#cfe0f5; font-size:11.5pt; margin-top:4mm; max-width:150mm; }
.statrow { display:flex; gap:5mm; margin-top:auto; }
.statrow .s { flex:1; background:rgba(255,255,255,.08); border:1px solid rgba(255,255,255,.2); border-radius:12px; padding:4.5mm 4mm; }
.statrow .s b { font-family:'Poppins'; font-weight:800; font-size:15pt; display:block; color:#fff; }
.statrow .s span { font-size:8pt; color:#B8CEF0; }
.cover-foot { margin-top:6mm; display:flex; justify-content:space-between; border-top:1px solid rgba(255,255,255,.2); padding-top:5mm; font-size:9pt; color:#cfe0f5; }
.cover-foot b { color:#fff; }

/* ---------- SECTION / GENERIC ---------- */
.big-title { font-family:'Poppins'; font-weight:900; font-size:34pt; margin:3mm 0; max-width:150mm; }
.bar { width:24mm; height:4px; background:#7FE0A0; border-radius:3px; margin:4mm 0 7mm; }
.lead-big { font-family:'Poppins'; font-weight:700; font-size:17pt; line-height:1.35; max-width:160mm; }
.lead-big em { color:#8FBEFF; font-style:normal; }
.tiles { margin-top:8mm; }
.trow { display:flex; gap:5mm; margin-bottom:5mm; align-items:stretch; }
.tiles .t { flex:1; background:rgba(255,255,255,.08); border:1px solid rgba(255,255,255,.18); border-radius:13px; padding:5.5mm 6mm 6.5mm; display:flex; gap:4mm; align-items:flex-start; }
.tiles .t .no { font-family:'Poppins'; font-weight:900; font-size:17pt; color:#8FBEFF; width:11mm; flex:none; }
.tiles .t h4 { font-family:'Poppins'; font-weight:700; font-size:10.5pt; color:#fff; line-height:1.2; }
.tiles .t p { font-size:8.2pt; color:#c2d3ee; margin:1.5mm 0 0; line-height:1.45; }
.applist2 { margin-top:8mm; }
.applist2 .a { flex:1; background:rgba(255,255,255,.08); border-left:4px solid #7FE0A0; border-radius:10px; padding:5mm 6mm; font-family:'Poppins'; font-weight:600; font-size:12pt; }
.flowrow { display:flex; justify-content:space-between; margin-top:9mm; }
.flowrow .n { text-align:center; width:15%; }
.flowrow .dot { width:15mm; height:15mm; border-radius:50%; background:linear-gradient(160deg,#1C61D6,#1147A8); border:2px solid rgba(255,255,255,.35);
  font-family:'Poppins'; font-weight:800; font-size:15pt; display:flex; align-items:center; justify-content:center; margin:0 auto 3mm; }
.flowrow b { font-size:8pt; color:#dfeaff; }
.statrow2 { display:flex; gap:5mm; margin-top:9mm; }
.statrow2 .s { flex:1; background:linear-gradient(160deg,#1C61D6,#1147A8); border:1px solid rgba(255,255,255,.25); border-radius:13px; padding:5mm; text-align:center; }
.statrow2 .s b { font-family:'Poppins'; font-weight:900; font-size:19pt; display:block; }
.statrow2 .s span { font-size:8pt; color:#Bcd6ff; }

/* ---------- DIVIDER ---------- */
.divnum { position:absolute; top:40mm; right:16mm; font-family:'Poppins'; font-weight:900; font-size:150pt; color:rgba(255,255,255,.07); z-index:1; }

/* ---------- BACK ---------- */
.back h2 { font-family:'Poppins'; font-weight:900; font-size:34pt; margin-top:6mm; max-width:150mm; }
.back h2 em { color:#7FE0A0; font-style:normal; }
.back .p { color:#cfe0f5; font-size:11.5pt; margin-top:4mm; max-width:150mm; }
.back-cta { display:inline-block; margin-top:8mm; background:#E23127; color:#fff; font-family:'Poppins'; font-weight:700; padding:5mm 11mm; border-radius:10px; font-size:12pt; }
.back-contact { margin-top:auto; display:flex; justify-content:space-between; align-items:flex-end; border-top:1px solid rgba(255,255,255,.2); padding-top:6mm; }
.back-contact .info div { font-size:10pt; color:#e6eefb; margin:2mm 0; }
.back-contact .info b { color:#fff; }
.qr { text-align:center; }
.qr img { width:30mm; height:30mm; background:#fff; padding:2mm; border-radius:8px; }
.qr span { display:block; font-size:7.5pt; color:#cfe0f5; margin-top:2mm; }
"""


def _wm():
    return '<div class="wm">BHARAT <em>iON</em> SYSTEMS<small>Water &amp; Packaging Machinery</small></div>'


def _cover():
    banner = _banner()
    hero = f'<div class="cover-hero"><img src="{_fileuri(banner)}" alt=""></div>' if banner else ''
    stats = "".join(f'<div class="s"><b>{a}</b><span>{b}</span></div>' for a, b in STATS)
    return f"""
<div class="page cover"><div class="tex1"></div><div class="tex2"></div><div class="z">
  <div class="tophead">{_wm()}<span class="type"><b>CATALOGUE</b><span>EDITION 2026</span></span></div>
  <h1>Complete <em>Water Bottling</em><br>&amp; Packaging Machinery</h1>
  <div class="sub">RO plants, PET blowing, filling &amp; capping, labelling, coding and shrink packaging &mdash; individual machines or a fully integrated turnkey line.</div>
  {hero}
  <div class="cover-foot"><div><b>{COMPANY['name']}</b> &nbsp;&middot;&nbsp; {COMPANY['tag']}</div><div>{COMPANY['phone']} &nbsp;&middot;&nbsp; {COMPANY['web']}</div></div>
</div></div>"""


def _intro():
    stats = "".join(f'<div class="s"><b>{a}</b><span>{b}</span></div>' for a, b in STATS)
    flow = "".join(f'<div class="n"><div class="dot">{n}</div><b>{t}</b></div>' for n, t in PROCESS)
    return f"""
<div class="page pb"><div class="tex1"></div><div class="tex2"></div><div class="z">
  <div class="tophead">{_wm()}<span class="type"><b>ABOUT</b><span>COMPANY PROFILE</span></span></div>
  <div style="margin-top:12mm"><div class="kick">One Partner, The Complete Line</div>
  <h2 class="big-title">Machinery That Helps<br>You Produce More</h2><div class="bar"></div></div>
  <p class="lead-big">Bharat iON Systems manufactures <em>world-class</em> machinery for the water,
  beverage and packaging industry &mdash; from RO purification to blowing, filling, labelling, coding
  and shrink packaging, backed end-to-end by one accountable team.</p>
  <div class="statrow2">{stats}</div>
  <div style="margin-top:12mm"><div class="kick">The Production Flow</div></div>
  <div class="flowrow">{flow}</div>
  <div class="desc"><p>Individual machines or a fully integrated turnkey line \u2014 supplied, installed, trained and supported across India.</p><span class="web">{COMPANY['web']}</span></div>
</div></div>"""


def _divider(num, kicker, title, sub):
    return f"""
<div class="page pb"><div class="tex1"></div><div class="tex2"></div><div class="divnum">{num}</div>
<div class="z" style="justify-content:center">
  <div class="kick">{kicker}</div>
  <h2 class="big-title" style="font-size:44pt">{title}</h2>
  <div class="bar"></div>
  <p class="lead-big" style="font-weight:500;font-size:13pt;color:#cfe0f5">{sub}</p>
</div></div>"""


def _accent_title(name):
    parts = name.split(" ", 1)
    if len(parts) == 2:
        return f'<em>{parts[0]}</em> {parts[1]}'
    return name


def _product(idx, p):
    ex = EXTRA.get(p["key"], {})
    model = ex.get("model", "")
    stats = "".join(
        f'<div class="stat"><div class="v">{v}{f"<span>{u}</span>" if u else ""}</div><div class="l">{l}</div><div class="ln"></div></div>'
        for v, u, l in ex.get("badges", []))
    feats = "".join(f'<div class="feat"><div class="ic">{icon(ic)}</div><span>{lab}</span></div>' for ic, lab in ex.get("features", []))
    sp = p["specs"]
    half = (len(sp) + 1) // 2

    def tbl(rows):
        return '<table class="spec">' + "".join(f'<tr><td class="k">{k}</td><td class="v">{v}</td></tr>' for k, v in rows) + '</table>'
    return f"""
<div class="page pb"><div class="tex1"></div><div class="tex2"></div><div class="z">
  <div class="tophead">{_wm()}<span class="type"><b>TYPE</b><span>{model}</span></span></div>
  <div style="margin-top:9mm"><div class="kick">{p['cat']}</div>
  <h1 class="ptitle">{_accent_title(p['name'])}</h1></div>
  <div class="hero">
    <div class="left">{stats}</div>
    <div class="right"><div class="photocard">{_visual(p['key'])}</div></div>
  </div>
  <div class="feats">{feats}</div>
  <div class="specrow"><div class="specpanel"><div class="lbl">Technical Specifications</div>
    <div class="spec2"><div>{tbl(sp[:half])}</div><div>{tbl(sp[half:])}</div></div></div></div>
  <div class="desc"><p>{p['lead']}</p><span class="web">{COMPANY['web']}</span></div>
</div></div>"""


def _pairs(items):
    return [items[i:i + 2] for i in range(0, len(items), 2)]


def _applications():
    rows = ""
    for pair in _pairs(APPLICATIONS):
        rows += '<div class="trow">' + "".join(f'<div class="a">{a}</div>' for a in pair) + '</div>'
    return f"""
<div class="page pb"><div class="tex1"></div><div class="tex2"></div><div class="z">
  <div class="tophead">{_wm()}<span class="type"><b>USE</b><span>APPLICATIONS</span></span></div>
  <div style="margin-top:12mm"><div class="kick">Where It Is Used</div>
  <h2 class="big-title">Applications &amp; Industries</h2><div class="bar"></div></div>
  <div class="applist2">{rows}</div>
  <div class="desc"><p>Our machinery powers packaging lines across a wide range of liquids and businesses.</p><span class="web">{COMPANY['web']}</span></div>
</div></div>"""


def _why():
    rows, n = "", 0
    for pair in _pairs(WHY):
        cells = ""
        for t, d in pair:
            n += 1
            cells += f'<div class="t"><div class="no">{n:02d}</div><div><h4>{t}</h4><p>{d}</p></div></div>'
        rows += f'<div class="trow">{cells}</div>'
    return f"""
<div class="page pb"><div class="tex1"></div><div class="tex2"></div><div class="z">
  <div class="tophead">{_wm()}<span class="type"><b>WHY</b><span>BHARAT iON</span></span></div>
  <div style="margin-top:12mm"><div class="kick">Why Choose Us</div>
  <h2 class="big-title">Built Around Your Success</h2><div class="bar"></div></div>
  <div class="tiles">{rows}</div>
</div></div>"""


def _back():
    qr = _qr("https://bharationsystems.com")
    qr_html = f'<div class="qr"><img src="{qr}" alt=""><span>bharationsystems.com</span></div>' if qr else ''
    return f"""
<div class="page pb back"><div class="tex1"></div><div class="tex2"></div><div class="z">
  {_wm()}
  <div style="margin-top:14mm"><div class="kick">Let's Talk</div>
  <h2>Let us build your <em>bottling plant</em>.</h2></div>
  <div class="p">Share your target capacity and city &mdash; we'll prepare a tailored machine list and budget, then supply, install and support the complete line, end to end.</div>
  <div><span class="back-cta">Get a Free Quote &amp; Plant Plan</span></div>
  <div class="back-contact">
    <div class="info">
      <div><b>{COMPANY['name']}</b></div>
      <div>&#9742;&nbsp; {COMPANY['phone']}</div>
      <div>&#9993;&nbsp; {COMPANY['email']}</div>
      <div>&#9737;&nbsp; {COMPANY['web']}</div>
      <div style="max-width:95mm">&#9741;&nbsp; {COMPANY['addr']}</div>
    </div>
    {qr_html}
  </div>
</div></div>"""


def build_html():
    parts = [_cover(), _intro(),
             _divider("01", "Machinery Range", "Our Machinery, In Detail",
                      "Nine core machines that together form a complete packaged-water and beverage line.")]
    parts += [_product(i + 1, p) for i, p in enumerate(PRODUCTS)]
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
