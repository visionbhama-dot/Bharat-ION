#!/usr/bin/env python3
"""
Bharat iON Systems - Product Catalogue (editorial / premium magazine style)
---------------------------------------------------------------------------
A distinct design from the website: warm paper background, Playfair Display
serif headings, IBM Plex Mono labels, hairline rules, large faint index
numerals, rectangular photo frames and a dark back cover. Rendered with
WeasyPrint. Run standalone to write ../assets/catalogue.pdf.
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


def _root_asset(*parts):
    return os.path.join(BASE, "..", "assets", *parts)


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
    if photo:
        return f'<img src="{_fileuri(photo)}" alt="">'
    return _svg(key)


def _banner():
    for name in ("hero-banner", "process-bg"):
        for ext in (".jpg", ".jpeg", ".png", ".webp"):
            p = _root_asset("images", "banner", name + ext)
            if os.path.exists(p):
                return p
    return _product_photo("ro")


def _qr_data_uri(text):
    try:
        import qrcode, io
        buf = io.BytesIO()
        qrcode.make(text).save(buf, format="PNG")
        return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return ""


# ---- Content ----
COMPANY = {
    "name": "Bharat iON Systems Pvt. Ltd.",
    "tag": "Water Treatment &amp; Bottle Packaging Machinery",
    "phone": "+91 83840 61695",
    "email": "info@bharationsystems.com",
    "web": "www.bharationsystems.com",
    "addr": "2882, 1st Floor, Karheda, Ghaziabad, Uttar Pradesh 201007",
}

STATS = [("RO&rarr;Pack", "Complete turnkey line"), ("6000", "Bottles per hour, up to"),
         ("09", "Core machines"), ("Pan-India", "Service &amp; spares")]

PROCESS = [("1", "RO Purification"), ("2", "PET Blowing"), ("3", "Filling &amp; Capping"),
           ("4", "Labelling"), ("5", "Batch Coding"), ("6", "Shrink Packing")]

PRODUCTS = [
    {"key": "semi", "cat": "PET Bottle Manufacturing", "name": "Semi-Automatic PET Blowing Machine",
     "lead": "Dependable auto-drop stretch blow moulding for start-ups and growing plants.",
     "specs": [("Mould Cavities", "1 / 2"), ("Bottle Volume", "100 ml &ndash; 2 Litre"),
               ("Output", "1000 &ndash; 1200 BPH"), ("Clamping Force", "8 Ton"),
               ("Blowing Pressure", "18 &ndash; 26 kg/cm&sup2;"), ("Operation", "Hydro-Pneumatic")],
     "hl": ["Auto-drop preform system", "Infrared conveyor heating", "Quick mould changeover", "Compact, low-power footprint"]},
    {"key": "handblow", "cat": "PET Bottle Manufacturing", "name": "Hand-Feed Automatic PET Blowing Machine",
     "lead": "Automatic blow cycle with simple manual preform feeding \u2014 more output at low cost.",
     "specs": [("Mould Cavities", "2 / 4"), ("Bottle Volume", "100 ml &ndash; 2 Litre"),
               ("Output", "1800 &ndash; 2500 BPH"), ("Heating", "Infrared Oven"),
               ("Clamping", "Hydraulic"), ("Power", "12 &ndash; 18 kW")],
     "hl": ["Fully automatic blow cycle", "Manual feed keeps cost low", "Uniform wall thickness", "Simple, robust operation"]},
    {"key": "full", "cat": "PET Bottle Manufacturing", "name": "Fully Automatic PET Blowing Machine",
     "lead": "High-speed servo blow moulding with automatic preform loading for large plants.",
     "specs": [("Mould Cavities", "2 / 4 / 6"), ("Bottle Volume", "200 ml &ndash; 2 Litre"),
               ("Output", "Up to 4000 &ndash; 6000 BPH"), ("Drive", "Servo"),
               ("Control", "PLC + HMI"), ("Feeding", "Automatic Preform Feeder")],
     "hl": ["Servo stretch-blow system", "Rotary / linear options", "Air recovery for efficiency", "Consistent high-volume output"]},
    {"key": "ro", "cat": "Water Treatment", "name": "Industrial RO Water Treatment Plant",
     "lead": "Multi-stage reverse osmosis for safe, IS 10500-grade packaged drinking water.",
     "specs": [("Capacity", "250 &ndash; 10,000 LPH"), ("Pre-treatment", "Multimedia + Carbon + Softener"),
               ("Membranes", "Spiral-wound TFC"), ("Dosing", "Antiscalant + Chlorine"),
               ("Body", "SS / FRP"), ("Options", "UV + Ozone")],
     "hl": ["Turnkey plant sizing", "High recovery, low rejection", "Automatic operation &amp; controls", "Ozonation &amp; UV polishing options"]},
    {"key": "station", "cat": "Filling &amp; Capping", "name": "Station Filler (Bottle Filling Machine)",
     "lead": "Economical multi-head filling for small and medium bottling lines.",
     "specs": [("Filling Heads", "4 &ndash; 8"), ("Bottle Volume", "200 ml &ndash; 5 Litre"),
               ("Output", "500 &ndash; 1500 BPH"), ("Fill Type", "Gravity / Volumetric"),
               ("Contact Parts", "SS 304 / 316"), ("Capping", "Manual / Semi-auto")],
     "hl": ["Hygienic stainless build", "Drip-free filling nozzles", "Adjustable fill volume", "Easy to clean &amp; maintain"]},
    {"key": "fill", "cat": "Filling &amp; Capping", "name": "Fully Automatic Rinsing, Filling &amp; Capping Machine",
     "lead": "A 3-in-1 monobloc that rinses, fills and caps in one hygienic, high-speed operation.",
     "specs": [("Configuration", "24-18-6 / customisable"), ("Output", "2000 &ndash; 6000 BPH"),
               ("Bottle Volume", "200 ml &ndash; 2 Litre"), ("Rinsing", "Gripper type"),
               ("Capping", "Magnetic torque head"), ("Contact Parts", "SS 304 / 316")],
     "hl": ["Single synchronised monobloc", "No-bottle / no-fill sensing", "CIP-ready hygienic design", "Smooth, high-speed handling"]},
    {"key": "label", "cat": "Labelling", "name": "Automatic Sticker Labelling Machine",
     "lead": "Servo-controlled self-adhesive labelling for crisp, consistent branding.",
     "specs": [("Output", "Up to 6000 BPH"), ("Label Material", "OPP / BOPP / Paper"),
               ("Bottle Shape", "Round"), ("Accuracy", "&plusmn; 1 mm"),
               ("Control", "Servo + PLC"), ("Add-on", "Online date/batch coder")],
     "hl": ["Wrinkle-free application", "Fast, tool-less changeover", "Wrap-around &amp; front/back", "Integrates with coding"]},
    {"key": "shrink", "cat": "Secondary Packaging", "name": "Automatic Shrink Wrapping Machine",
     "lead": "Groups bottles into transport-ready multi-packs through a heat-shrink tunnel.",
     "specs": [("Film", "LDPE / POF"), ("Output", "Up to 12 packs / min"),
               ("Pack Sizes", "6 / 12 / 24"), ("Tunnel", "SS heat chamber"),
               ("Control", "PLC"), ("Sealing", "Web sealer")],
     "hl": ["Web sealer + shrink tunnel", "Adjustable pack sizes", "Uniform, tight wrap", "Energy-efficient heating"]},
    {"key": "ink", "cat": "Coding &amp; Marking", "name": "Batch Coding Machine",
     "lead": "High-resolution coding of batch, MFG/EXP dates and MRP at full line speed.",
     "specs": [("Type", "Inkjet (CIJ / DOD)"), ("Print Lines", "1 &ndash; 4"),
               ("Speed", "Line-synchronised"), ("Ink", "Food-grade, fast-dry"),
               ("Interface", "Touchscreen"), ("Codes", "Text / Logo / Barcode")],
     "hl": ["Non-contact printing", "Fast-drying inks", "Logo &amp; barcode support", "Low maintenance"]},
]

# ---- Icon set (simple line icons, stroke = currentColor) ----
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
    return (f"<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' "
            f"stroke-linecap='round' stroke-linejoin='round'>{ICONS.get(name, '')}</svg>")


# ---- Extra marketing data per product (model, headline stats, feature chips) ----
EXTRA = {
    "semi": {"model": "BIS-SB2",
             "badges": [("1200", "BPH", "Max Output"), ("2", "L", "Max Bottle"), ("2", "Cav.", "Mould"), ("8", "Ton", "Clamping")],
             "features": [("gear", "Auto-Drop System"), ("bolt", "Low Power Use"), ("clock", "Quick Mould Change"), ("shield", "1-Year Warranty")]},
    "handblow": {"model": "BIS-HB4",
                 "badges": [("2500", "BPH", "Max Output"), ("2", "L", "Max Bottle"), ("4", "Cav.", "Cavities"), ("18", "kW", "Power")],
                 "features": [("gear", "Automatic Cycle"), ("bolt", "Cost-Efficient"), ("drop", "Even Wall Thickness"), ("wrench", "Easy Service")]},
    "full": {"model": "BIS-FA6",
             "badges": [("6000", "BPH", "Max Output"), ("6", "Cav.", "Cavities"), ("2", "L", "Max Bottle"), ("PLC", "+HMI", "Control")],
             "features": [("gear", "Servo Stretch-Blow"), ("leaf", "Air Recovery"), ("bolt", "High Speed"), ("shield", "Robust Build")]},
    "ro": {"model": "BIS-RO",
           "badges": [("10,000", "LPH", "Max Capacity"), ("4+", "Stage", "Pre-treatment"), ("UV+O&#8323;", "", "Polishing"), ("24&times;7", "", "Operation")],
           "features": [("drop", "IS 10500 Water"), ("gear", "Automatic Controls"), ("leaf", "High Recovery"), ("shield", "SS / FRP Build")]},
    "station": {"model": "BIS-SF8",
                "badges": [("1500", "BPH", "Max Output"), ("8", "Head", "Filling"), ("5", "L", "Max Bottle"), ("SS", "304/316", "Contact")],
                "features": [("drop", "Drip-Free Nozzles"), ("gear", "Adjustable Fill"), ("shield", "Hygienic Build"), ("wrench", "Easy to Clean")]},
    "fill": {"model": "BIS-RFC",
             "badges": [("6000", "BPH", "Max Output"), ("3-in-1", "", "Monobloc"), ("2", "L", "Max Bottle"), ("CIP", "Ready", "Hygiene")],
             "features": [("gear", "Synchronised Monobloc"), ("drop", "No-Bottle / No-Fill"), ("shield", "SS 304 / 316"), ("clock", "High-Speed")]},
    "label": {"model": "BIS-LB",
              "badges": [("6000", "BPH", "Max Output"), ("&plusmn;1", "mm", "Accuracy"), ("OPP", "BOPP", "Labels"), ("Servo", "", "Control")],
              "features": [("gear", "Servo Controlled"), ("bolt", "Wrinkle-Free"), ("clock", "Fast Changeover"), ("barcode", "Coder-Ready")]},
    "shrink": {"model": "BIS-SW",
               "badges": [("12", "/min", "Packs"), ("24", "pack", "Max Size"), ("POF", "LDPE", "Film"), ("PLC", "", "Control")],
               "features": [("gear", "Web Sealer + Tunnel"), ("leaf", "Energy Saving"), ("shield", "Tight Uniform Wrap"), ("wrench", "Low Upkeep")]},
    "ink": {"model": "BIS-BC",
            "badges": [("4", "Lines", "Print"), ("CIJ", "DOD", "Technology"), ("HD", "", "Resolution"), ("Fast", "Dry", "Ink")],
            "features": [("bolt", "Non-Contact"), ("clock", "Fast-Drying"), ("barcode", "Logo + Barcode"), ("wrench", "Low Maintenance")]},
}

APPLICATIONS = ["Packaged Drinking Water Plants", "Mineral Water Bottling Units",
                "Beverage &amp; Juice Filling Lines", "Carbonated Soft Drink Plants",
                "Dairy &amp; Liquid Packaging", "Distributors, Dealers &amp; OEM Buyers"]

WHY = [("Single Accountable Partner", "One team supplies, installs and supports your entire line."),
       ("Right-Sized For You", "Configurations matched to your output, budget and space."),
       ("Installation &amp; Training", "On-site commissioning and operator training included."),
       ("Genuine Spares &amp; Service", "Prompt after-sales support and authentic spare parts."),
       ("Manufacturer Pricing", "Direct-from-maker value, with no middlemen."),
       ("Robust, Hygienic Builds", "Food-grade stainless construction, built to last.")]


CSS = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;0,800;0,900;1,600;1,700&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500;600&display=swap');
* { box-sizing:border-box; }
body { font-family:'Inter',sans-serif; color:#16232B; margin:0; font-size:10pt; line-height:1.6; background:#FBFAF7; }
h1,h2,h3,h4 { font-family:'Playfair Display',Georgia,serif; color:#16232B; margin:0; line-height:1.08; font-weight:800; }
p { margin:0; }
.kick { font-family:'IBM Plex Mono',monospace; font-size:8pt; letter-spacing:2.5px; text-transform:uppercase; color:#0F5F6B; }
.hr { height:1px; background:#E5E0D6; border:0; margin:8mm 0; }

@page { size:A4; margin:22mm 18mm 18mm 18mm;
  @top-left { content:"BHARAT iON SYSTEMS"; font-family:'IBM Plex Mono'; font-size:7pt; letter-spacing:1.5px; color:#0F5F6B; }
  @top-right { content:"Product Catalogue \\2014 2026"; font-family:'IBM Plex Mono'; font-size:7pt; letter-spacing:1.5px; color:#A6ADA9; }
  @bottom-left { content:"bharationsystems.com"; font-family:'IBM Plex Mono'; font-size:7pt; color:#A6ADA9; }
  @bottom-right { content:counter(page,decimal-leading-zero); font-family:'IBM Plex Mono'; font-size:8pt; color:#16232B; }
}
@page cover { margin:0; @top-left{content:none} @top-right{content:none} @bottom-left{content:none} @bottom-right{content:none} }
@page back  { margin:0; @top-left{content:none} @top-right{content:none} @bottom-left{content:none} @bottom-right{content:none} }
.cover { page:cover; } .back { page:back; } .divider { page:cover; } .pb { page-break-before:always; }

/* ---------- COVER (photo-led editorial) ---------- */
.cover-wrap { width:210mm; height:297mm; background:#FBFAF7; display:flex; flex-direction:column; }
.cover-photo { height:168mm; width:100%; object-fit:cover; display:block; }
.cover-body { flex:1; padding:14mm 20mm 16mm; display:flex; flex-direction:column; }
.cover-top { display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #E5E0D6; padding-bottom:5mm; margin-bottom:7mm; }
.cover-top img { height:12mm; width:auto; }
.cover-top .ed { font-family:'IBM Plex Mono'; font-size:8pt; letter-spacing:2px; color:#0F5F6B; text-transform:uppercase; }
.cover-body h1 { font-size:38pt; font-weight:900; letter-spacing:-.5px; max-width:172mm; }
.cover-body h1 em { font-style:italic; color:#0F5F6B; font-weight:700; }
.cover-body .sub { margin-top:5mm; color:#5F6E76; font-size:11pt; max-width:150mm; }
.cover-body .foot { margin-top:auto; display:flex; justify-content:space-between; align-items:flex-end;
  font-family:'IBM Plex Mono'; font-size:8.5pt; color:#5F6E76; }
.cover-body .foot b { color:#16232B; font-family:'Inter'; }

/* ---------- INTRO ---------- */
.lead-serif { font-family:'Playfair Display',serif; font-weight:600; font-size:19pt; line-height:1.35; max-width:165mm; }
.lead-serif em { font-style:italic; color:#0F5F6B; }
.stat-row { display:flex; margin:9mm 0; }
.stat-row .s { flex:1; padding:0 6mm; border-left:1px solid #E5E0D6; }
.stat-row .s:first-child { padding-left:0; border-left:0; }
.stat-row .s b { font-family:'Playfair Display'; font-size:20pt; font-weight:800; display:block; color:#0F5F6B; }
.stat-row .s span { font-size:8.5pt; color:#5F6E76; }
.tl { display:flex; justify-content:space-between; margin-top:7mm; }
.tl .n { width:15%; text-align:center; }
.tl .num { font-family:'IBM Plex Mono'; font-weight:600; font-size:9pt; color:#0F5F6B; border:1px solid #0F5F6B;
  border-radius:50%; width:9mm; height:9mm; line-height:8.4mm; margin:0 auto 3mm; }
.tl b { font-size:7.5pt; color:#16232B; font-weight:600; }

/* ---------- PRODUCT ---------- */
.prod { position:relative; padding-top:2mm; }
.bignum { position:absolute; top:20mm; right:0; font-family:'Playfair Display'; font-weight:900;
  font-size:74pt; color:#F0ECE2; line-height:1; z-index:0; }
.prod .cat, .prod h2, .prod .lead { position:relative; z-index:1; }
.prod h2 { font-size:28pt; font-weight:800; max-width:150mm; margin:3mm 0; }
.prod .lead { color:#5F6E76; font-size:11pt; max-width:150mm; margin-bottom:6mm; }
.phead { display:flex; justify-content:space-between; align-items:center; position:relative; z-index:1; }
.model { font-family:'IBM Plex Mono'; font-size:8pt; letter-spacing:1px; color:#16232B; border:1px solid #16232B;
  border-radius:20px; display:inline-flex; align-items:center; overflow:hidden; padding-right:4mm; }
.model b { background:#0F5F6B; color:#fff; padding:2mm 3mm; margin-right:3mm; font-weight:600; letter-spacing:1.5px; }
.frame { border:1px solid #E5E0D6; background:#fff; padding:5mm; height:60mm; display:flex; align-items:center; justify-content:center; position:relative; z-index:1; }
.frame img { max-width:100%; max-height:100%; object-fit:contain; }
.frame svg { width:100%; height:100%; }
.badges { display:flex; gap:4mm; margin-top:5mm; }
.badge { flex:1; background:#EAF3F4; border:1px solid #D6E7E9; border-radius:10px; padding:4mm 2mm; text-align:center; }
.badge .bv { font-family:'Playfair Display'; font-weight:800; font-size:18pt; color:#0F5F6B; line-height:1; }
.badge .bv span { font-family:'IBM Plex Mono'; font-size:7.5pt; color:#2E8896; margin-left:1mm; font-weight:600; }
.badge .bl { font-family:'IBM Plex Mono'; font-size:6.5pt; letter-spacing:1px; text-transform:uppercase; color:#5F6E76; margin-top:2mm; }
.fchips { display:flex; gap:4mm; margin-top:6mm; border-top:1px solid #E5E0D6; padding-top:5mm; }
.fchip { flex:1; display:flex; align-items:center; gap:2.5mm; }
.fchip svg { width:8mm; height:8mm; flex:none; color:#0F5F6B; background:#EAF3F4; border-radius:8px; padding:1.6mm; }
.fchip span { font-size:8pt; font-weight:600; color:#16232B; line-height:1.15; }
.pmeta { display:flex; gap:12mm; margin-top:6mm; }
.pmeta .col { flex:1; }
.lbl { font-family:'IBM Plex Mono'; font-size:7.5pt; letter-spacing:2px; text-transform:uppercase; color:#0F5F6B;
  border-bottom:1px solid #16232B; padding-bottom:2mm; margin-bottom:3mm; }
.spec { width:100%; border-collapse:collapse; font-size:9.5pt; }
.spec td { padding:2.5mm 0; border-bottom:1px solid #EFEBE2; }
.spec td.k { color:#5F6E76; font-family:'IBM Plex Mono'; font-size:8.5pt; }
.spec td.v { text-align:right; font-weight:600; color:#16232B; }
.hl { list-style:none; margin:0; padding:0; }
.hl li { padding:2.5mm 0 2.5mm 6mm; border-bottom:1px solid #EFEBE2; position:relative; font-size:10pt; color:#2b3942; }
.hl li:before { content:"\\2014"; position:absolute; left:0; color:#0F5F6B; font-weight:700; }

/* ---------- DIVIDER ---------- */
.divider-wrap { width:210mm; height:297mm; background:#FBFAF7; padding:0 26mm; display:flex; flex-direction:column;
  justify-content:center; position:relative; }
.divider-wrap .bg { position:absolute; top:34mm; right:22mm; font-family:'Playfair Display'; font-weight:900;
  font-size:150pt; color:#EFEBE1; line-height:1; }
.divider-wrap h2 { font-size:42pt; font-weight:900; max-width:150mm; margin-top:4mm; }
.divider-wrap .r { width:24mm; height:2px; background:#0F5F6B; margin-top:6mm; }
.divider-wrap p { color:#5F6E76; margin-top:5mm; max-width:130mm; font-size:11.5pt; }

/* ---------- APPLICATIONS / WHY (editorial lists) ---------- */
.applist { margin-top:8mm; }
.applist .a { display:flex; align-items:baseline; gap:6mm; padding:4.5mm 0; border-bottom:1px solid #E5E0D6; }
.applist .a .no { font-family:'IBM Plex Mono'; color:#0F5F6B; font-size:9pt; width:8mm; }
.applist .a .t { font-family:'Playfair Display'; font-size:15pt; font-weight:700; color:#16232B; }
.why { margin-top:6mm; }
.why .w { display:flex; gap:7mm; padding:5mm 0; border-bottom:1px solid #E5E0D6; }
.why .w .no { font-family:'Playfair Display'; font-weight:800; font-size:20pt; color:#E1DACB; width:14mm; }
.why .w h4 { font-family:'Playfair Display'; font-size:13pt; font-weight:700; }
.why .w p { color:#5F6E76; font-size:9.5pt; margin-top:1mm; }

/* ---------- BACK COVER (dark) ---------- */
.back-wrap { width:210mm; height:297mm; background:#10222A; color:#fff; padding:26mm 22mm; display:flex; flex-direction:column; }
.back-wrap .wm { font-family:'Playfair Display'; font-weight:800; font-size:15pt; color:#fff; letter-spacing:.5px; }
.back-wrap .wm em { color:#7FD0D9; font-style:italic; }
.back-wrap .k { color:#4FB3C0; margin-top:12mm; }
.back-wrap h2 { color:#fff; font-size:34pt; font-weight:900; margin-top:4mm; max-width:150mm; }
.back-wrap h2 em { font-style:italic; color:#7FD0D9; }
.back-wrap .p { color:#b8c6cc; font-size:11.5pt; margin-top:4mm; max-width:150mm; }
.back-cta { display:inline-block; margin-top:8mm; border:1.5px solid #4FB3C0; color:#fff; font-family:'IBM Plex Mono';
  letter-spacing:1px; padding:4mm 8mm; font-size:9.5pt; text-transform:uppercase; }
.back-contact { margin-top:auto; display:flex; justify-content:space-between; align-items:flex-end;
  border-top:1px solid rgba(255,255,255,.18); padding-top:6mm; }
.back-contact .info div { font-family:'IBM Plex Mono'; font-size:9pt; color:#cdd8dc; margin:1.8mm 0; }
.back-contact .info b { color:#fff; font-family:'Inter'; }
.qr { text-align:center; }
.qr img { width:28mm; height:28mm; background:#fff; padding:2mm; border-radius:4px; }
.qr span { display:block; font-family:'IBM Plex Mono'; font-size:7pt; color:#9fb0b6; margin-top:2mm; }
"""


def _cover():
    logo = _logo()
    banner = _banner()
    logo_img = f'<img src="{_fileuri(logo)}" alt="">' if logo else f'<span class="ed">{COMPANY["name"]}</span>'
    photo = f'<img class="cover-photo" src="{_fileuri(banner)}" alt="">' if banner else '<div class="cover-photo" style="background:#10222A"></div>'
    return f"""
<div class="cover"><div class="cover-wrap">
  {photo}
  <div class="cover-body">
    <div class="cover-top">{logo_img}<span class="ed">Product Catalogue &middot; Edition 2026</span></div>
    <h1>Machinery for <em>Water &amp; Beverage</em> Packaging</h1>
    <div class="sub">Reverse-osmosis purification, PET bottle blowing, filling &amp; capping, labelling, coding and shrink packaging &mdash; supplied as individual machines or a fully integrated turnkey line.</div>
    <div class="foot"><div><b>{COMPANY['name']}</b> &nbsp;&middot;&nbsp; {COMPANY['tag']}</div><div>{COMPANY['phone']}</div></div>
  </div>
</div></div>"""


def _intro():
    stats = "".join(f'<div class="s"><b>{a}</b><span>{b}</span></div>' for a, b in STATS)
    tl = "".join(f'<div class="n"><div class="num">{n}</div><b>{t}</b></div>' for n, t in PROCESS)
    return f"""
<section class="pb">
  <div class="kick">Company Profile</div>
  <p class="lead-serif" style="margin-top:5mm">We build <em>world-class</em> machinery for the water,
  beverage and packaging industry &mdash; helping you produce more, reliably, with one accountable
  partner from plant design through installation and after-sales support.</p>
  <div class="stat-row">{stats}</div>
  <hr class="hr">
  <div class="kick">The Production Flow</div>
  <div class="tl">{tl}</div>
</section>"""


def _divider(num, kicker, title, sub):
    return f"""
<div class="divider"><div class="divider-wrap">
  <div class="bg">{num}</div>
  <div class="kick">{kicker}</div>
  <h2>{title}</h2>
  <div class="r"></div>
  <p>{sub}</p>
</div></div>"""


def _product(idx, p):
    ex = EXTRA.get(p["key"], {})
    model = ex.get("model", "")
    model_html = f'<span class="model"><b>MODEL</b>{model}</span>' if model else ''
    badges = "".join(
        f'<div class="badge"><div class="bv">{v}{f"<span>{u}</span>" if u else ""}</div><div class="bl">{l}</div></div>'
        for v, u, l in ex.get("badges", []))
    chips = "".join(f'<div class="fchip">{icon(ic)}<span>{lab}</span></div>' for ic, lab in ex.get("features", []))
    specs = "".join(f'<tr><td class="k">{k}</td><td class="v">{v}</td></tr>' for k, v in p["specs"])
    feats = "".join(f'<li>{h}</li>' for h in p["hl"])
    return f"""
<section class="pb prod">
  <div class="bignum">{idx:02d}</div>
  <div class="phead"><div class="kick">{p['cat']}</div>{model_html}</div>
  <h2>{p['name']}</h2>
  <div class="lead">{p['lead']}</div>
  <div class="frame">{_visual(p['key'])}</div>
  <div class="badges">{badges}</div>
  <div class="pmeta">
    <div class="col"><div class="lbl">Specifications</div><table class="spec">{specs}</table></div>
    <div class="col"><div class="lbl">Highlights</div><ul class="hl">{feats}</ul></div>
  </div>
  <div class="fchips">{chips}</div>
</section>"""


def _applications():
    items = "".join(f'<div class="a"><span class="no">{i+1:02d}</span><span class="t">{a}</span></div>'
                    for i, a in enumerate(APPLICATIONS))
    return f"""
<section class="pb">
  <div class="kick">Where It Is Used</div>
  <h2 style="font-size:30pt;margin:3mm 0">Applications &amp; Industries</h2>
  <div class="applist">{items}</div>
</section>"""


def _why():
    ws = "".join(f'<div class="w"><div class="no">{i+1:02d}</div><div><h4>{t}</h4><p>{d}</p></div></div>'
                 for i, (t, d) in enumerate(WHY))
    return f"""
<section class="pb">
  <div class="kick">Why Bharat iON</div>
  <h2 style="font-size:30pt;margin:3mm 0">Built Around Your Success</h2>
  <div class="why">{ws}</div>
</section>"""


def _back():
    qr = _qr_data_uri("https://bharationsystems.com")
    qr_html = f'<div class="qr"><img src="{qr}" alt=""><span>bharationsystems.com</span></div>' if qr else ''
    return f"""
<div class="back"><div class="back-wrap">
  <div class="wm">BHARAT <em>iON</em> SYSTEMS</div>
  <div class="k">Let's Talk</div>
  <h2>Let us build your <em>bottling plant</em>.</h2>
  <div class="p">Share your target capacity and city &mdash; we will prepare a tailored machine list and
  budget, then supply, install and support the complete line, end to end.</div>
  <div><span class="back-cta">Get a Free Quote &amp; Plant Plan</span></div>
  <div class="back-contact">
    <div class="info">
      <div><b>{COMPANY['name']}</b></div>
      <div>T &nbsp; {COMPANY['phone']}</div>
      <div>E &nbsp; {COMPANY['email']}</div>
      <div>W &nbsp; {COMPANY['web']}</div>
      <div style="max-width:95mm">A &nbsp; {COMPANY['addr']}</div>
    </div>
    {qr_html}
  </div>
</div></div>"""


def build_html():
    parts = [_cover(), _intro(),
             _divider("01", "Machinery Range", "Our Machinery,\nIn Detail".replace("\n", "<br>"),
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
