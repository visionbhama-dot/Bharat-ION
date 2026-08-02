#!/usr/bin/env python3
"""
Bharat ION Systems - Quotation renderer (canonical design)
----------------------------------------------------------
Single source of truth for the world-class 6-page A4 quotation.
Used by the Flask app (editor -> PDF) and for sample generation.

- Every page is a fixed A4 sheet with a decorative double border.
- Fully parameterised by a `data` dict (see default_data()).
- render_pdf_bytes(data, flatten, lock) -> bytes
    lock=True    : AES-256 encrypt + disable editing/copying (non-editable)
    flatten=True : rasterise pages first (max tamper resistance)
"""
import io
import os
import secrets

from weasyprint import HTML
import pikepdf

try:
    import products_data as _pd
except Exception:
    _pd = None

C = {
    "NAVY": "#0A2A5E", "NAVY2": "#0E3C7E", "BLUE": "#1656C4", "GREEN": "#179E4E",
    "RED": "#E23127", "GOLD": "#E6A11C", "INK": "#14243A", "MUTED": "#5E6E82",
    "LINE": "#DCE5F0", "SOFT": "#EEF3FA", "ICE": "#F5F9FD", "WHITE": "#FFFFFF",
}


# ---------------------------------------------------------------- logo / art
def emblem(size=54):
    return f'''
<svg width="{size}" height="{size}" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" style="flex:none">
  <circle cx="46" cy="48" r="33" fill="#0E4AA8"/>
  <circle cx="46" cy="48" r="33" fill="none" stroke="#8FBBF2" stroke-width="1" opacity=".6"/>
  <ellipse cx="46" cy="48" rx="14" ry="33" fill="none" stroke="#AFD0F7" stroke-width="1" opacity=".45"/>
  <line x1="15" y1="40" x2="77" y2="40" stroke="#AFD0F7" stroke-width="1" opacity=".4"/>
  <line x1="15" y1="56" x2="77" y2="56" stroke="#AFD0F7" stroke-width="1" opacity=".4"/>
  <path d="M18 18 A33 33 0 0 1 82 38" fill="none" stroke="{C['GREEN']}" stroke-width="7" stroke-linecap="round"/>
  <path d="M22 74 C46 62 60 74 84 30" fill="none" stroke="{C['RED']}" stroke-width="7.5" stroke-linecap="round"/>
  <path d="M84 30 l-4 15 l16 -5 z" fill="{C['RED']}"/>
  <g transform="translate(74,70)"><circle r="17" fill="{C['GOLD']}"/><circle r="7" fill="{C['NAVY']}"/>
  {''.join(f'<rect x="-3" y="-22" width="6" height="8" rx="1.5" fill="{C["GOLD"]}" transform="rotate({a})"/>' for a in range(0,360,45))}</g>
</svg>'''


def wordmark(size=16):
    return (f'<div style="font-family:\'Poppins\';font-weight:800;font-size:{size}pt;line-height:1;letter-spacing:.02em;color:{C["NAVY"]}">'
            f'BHARAT <span style="color:{C["GOLD"]}">iON</span> '
            f'<span style="font-weight:700;letter-spacing:.18em;font-size:{size*0.62:.0f}pt">SYSTEMS</span></div>')


def _fileuri(path):
    return "file://" + os.path.abspath(path) if path else ""


def logo_block(logo_path):
    if logo_path and os.path.exists(logo_path):
        inner = f'<img src="{_fileuri(logo_path)}" alt="logo" style="height:auto;width:auto;max-height:17mm;max-width:52mm;object-fit:contain">'
    else:
        inner = f'{emblem(50)}{wordmark(15)}'
    return f'<div style="display:flex;align-items:center;gap:11px;flex:none">{inner}</div>'


def placeholder_thumb():
    return (f'<svg viewBox="0 0 130 96" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%">'
            f'<rect width="130" height="96" rx="8" fill="{C["ICE"]}" stroke="{C["LINE"]}"/>'
            f'<rect x="40" y="34" width="50" height="34" rx="4" fill="none" stroke="{C["MUTED"]}" stroke-width="2"/>'
            f'<circle cx="53" cy="46" r="4" fill="{C["MUTED"]}"/>'
            f'<path d="M44 64 l12 -12 l9 9 l7 -6 l10 9" fill="none" stroke="{C["MUTED"]}" stroke-width="2"/>'
            f'<text x="65" y="86" text-anchor="middle" font-family="Inter,Arial" font-size="7" fill="{C["MUTED"]}">product image</text></svg>')


def item_image(img_path):
    if img_path and os.path.exists(img_path):
        return f'<img src="{_fileuri(img_path)}" alt="" style="width:100%;height:100%;object-fit:cover;border-radius:6px">'
    return placeholder_thumb()


def inr(n):
    try:
        n = int(round(float(n)))
    except Exception:
        return str(n)
    s = str(n)
    if len(s) <= 3:
        return s
    last3 = s[-3:]; rest = s[:-3]; parts = []
    while len(rest) > 2:
        parts.insert(0, rest[-2:]); rest = rest[:-2]
    if rest:
        parts.insert(0, rest)
    return ",".join(parts) + "," + last3


# ---------------------------------------------------------------- CSS
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:'Inter',Arial,sans-serif;color:[[INK]];font-size:10pt;line-height:1.5}
h1,h2,h3,h4,.pop{font-family:'Poppins',Arial,sans-serif}
/* content area = page margins; header/footer/border live in the margins and REPEAT on every page */
@page{size:A4;margin:36mm 15mm 22mm 15mm;
  @top-center{content:element(hdr);vertical-align:middle}
  @bottom-center{content:element(ftr);vertical-align:middle}}
.section{page-break-before:always}
.section:first-of-type{page-break-before:auto}

/* decorative border (fixed -> repeats on every page) */
.frame{position:fixed;top:-30mm;left:-9mm;right:-9mm;bottom:-16mm;border:2px solid [[NAVY]];border-radius:6px;z-index:1;pointer-events:none}
.frame:before{content:"";position:absolute;top:3px;left:3px;right:3px;bottom:3px;border:1px solid [[GOLD]];border-radius:4px}

/* header -> runs in the @top-center margin box on every page */
.hd{position:running(hdr)}
.hd .hd-row{display:flex;align-items:center;gap:16px}
.hd .r{flex:1;text-align:right;font-size:7.6pt;color:[[MUTED]];line-height:1.5;border-left:2px solid [[LINE]];padding-left:16px}
.hd .r b{color:[[NAVY]]}
.hd .gst{margin-top:4px;font-weight:700;color:[[NAVY]];font-size:7.8pt}
.hdbar{height:3px;background:linear-gradient(90deg,[[GREEN]],[[BLUE]] 45%,[[NAVY]] 70%,[[RED]]);margin:7px -9mm 0}

/* footer */
.ft{position:running(ftr)}
.ftbar{height:3px;background:linear-gradient(90deg,[[RED]],[[NAVY]] 30%,[[BLUE]] 60%,[[GREEN]]);margin:0 -9mm}
.ft .in{background:[[NAVY]];color:#d7e3f5;padding:3.5mm 9mm;font-size:7.4pt;display:flex;justify-content:space-between;gap:10px;align-items:center;margin:0 -9mm}
.ft .in b{color:#fff}
.pageno{color:#9fb6d8}

/* generic */
.muted{color:[[MUTED]]}.small{font-size:8.6pt}.b{font-weight:700}.navy{color:[[NAVY]]}
.ribbon{display:inline-block;background:[[NAVY]];color:#fff;font-family:'Poppins';font-weight:700;font-size:12pt;letter-spacing:.06em;padding:7px 20px 7px 16px;border-radius:0 22px 22px 0;margin-left:-9mm;box-shadow:0 4px 10px rgba(10,42,94,.18)}
.ribbon i{color:[[GOLD]];font-style:normal}
.h2c{text-align:center;font-family:'Poppins';font-weight:700;color:[[NAVY]];font-size:12.5pt;margin:14px 0 10px}
.h2c:after{content:"";display:block;width:54px;height:3px;background:[[GOLD]];margin:6px auto 0;border-radius:2px}

/* cover */
.metarow{display:flex;justify-content:space-between;margin-top:4px}
.reftag{background:[[SOFT]];border-left:4px solid [[BLUE]];padding:8px 12px;border-radius:0 8px 8px 0;font-size:9.4pt}
.reftag b{color:[[NAVY]]}
.tobox{margin:16px 0 6px}
.subj{background:[[SOFT]];border:1px solid [[LINE]];border-left:4px solid [[GOLD]];padding:9px 13px;border-radius:0 8px 8px 0;margin:12px 0}
.subj b{color:[[NAVY]]}
.anx{width:100%;border-collapse:collapse;margin:12px 0}
.anx td{border:1px solid [[LINE]];padding:9px 12px;font-size:9.4pt}
.anx td.k{background:[[NAVY]];color:#fff;font-weight:700;width:42%;font-family:'Poppins'}
.sign{margin-top:24px}
.sign .co{font-weight:800;color:[[NAVY]];font-family:'Poppins'}
.sign .ln{margin-top:20px;border-top:1.4px solid [[NAVY]];width:56mm;padding-top:4px;font-size:8.6pt;color:[[MUTED]]}
.pgwm{position:fixed;top:95mm;left:0;right:0;opacity:.06;z-index:0;pointer-events:none;text-align:center}
/* product range page */
.pgrid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:9px;margin-top:8px}
.ptile{border:1px solid [[LINE]];border-radius:10px;overflow:hidden;background:#fff}
.ptile .pimg{height:42mm;overflow:hidden;background:[[ICE]];display:flex;align-items:center;justify-content:center;padding:3px}
.ptile .pimg svg{width:100%;height:100%}
.ptile .pimg img{width:100%;height:100%;object-fit:cover;border-radius:4px}
.ptile .pcap{padding:6px 9px 9px}
.ptile .pcat{font-size:6.4pt;font-weight:700;color:[[GREEN]];text-transform:uppercase;letter-spacing:.04em}
.ptile .pname{font-size:8.1pt;font-weight:700;color:[[NAVY]];line-height:1.18;margin-top:2px}

/* tables */
.tbl{width:100%;border-collapse:collapse;margin-top:6px}
.tbl th{background:[[NAVY]];color:#fff;font-size:8.4pt;text-transform:uppercase;letter-spacing:.04em;padding:7px 9px;text-align:left;font-family:'Poppins';font-weight:600}
.tbl td{padding:6px 9px;border-bottom:1px solid [[LINE]];font-size:8.9pt}
.tbl tr:nth-child(even) td{background:[[ICE]]}
.spec2{display:grid;grid-template-columns:1fr 1fr;gap:0 20px}

/* price */
.price{width:100%;border-collapse:collapse;margin-top:6px}
.price thead{display:table-header-group}
.price tr,.tbl tr,.ptile{page-break-inside:avoid}
.price th{background:[[NAVY]];color:#fff;padding:8px 9px;font-size:8.4pt;font-family:'Poppins';font-weight:600;text-transform:uppercase;letter-spacing:.03em;text-align:left}
.price td{border-bottom:1px solid [[LINE]];padding:9px;vertical-align:middle;font-size:9pt}
.price .num{text-align:center;font-weight:700;color:[[NAVY]];width:24px}
.price .img{width:66px}
.price .img .ib{width:66px;height:50px}
.price .nm{font-weight:700;color:[[NAVY]];font-size:9.5pt}
.price .ds{color:[[MUTED]];font-size:8.2pt;margin-top:2px}
.price .qty{text-align:center;white-space:nowrap}
.price .amt{text-align:right;white-space:nowrap;font-weight:700;color:[[NAVY]];font-variant-numeric:tabular-nums}
.totrow td{background:[[SOFT]];font-family:'Poppins';font-weight:800;color:[[NAVY]];font-size:10.5pt}
.subrow td{font-weight:700;color:[[NAVY]];font-size:9.6pt}
.taxrow td{font-size:8.6pt;color:[[MUTED]];border:0;padding-top:6px}
.note{background:[[ICE]];border:1px dashed [[BLUE]];border-radius:8px;padding:9px 12px;font-size:8.4pt;color:[[INK]];margin-top:10px}

ol.terms{margin-left:5mm;margin-top:6px}
ol.terms li{margin-bottom:7px;font-size:8.9pt}
ol.terms li b{color:[[NAVY]]}
.bankgrid{border:1px solid [[LINE]];border-radius:10px;overflow:hidden;margin-top:10px}
.bankgrid .row{display:flex;border-bottom:1px solid [[LINE]]}
.bankgrid .row:last-child{border-bottom:0}
.bankgrid .k{width:38%;background:[[SOFT]];padding:9px 12px;font-weight:700;color:[[NAVY]];font-size:9pt}
.bankgrid .v{padding:9px 12px;font-size:9pt}
.chip{display:inline-block;background:[[NAVY]];color:#fff;border-radius:20px;padding:4px 12px;font-size:8pt;font-weight:600;margin:3px 4px 0 0}
.why{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}
.why .c{border:1px solid [[LINE]];border-radius:10px;padding:12px 14px}
.why .c b{color:[[NAVY]];font-family:'Poppins'}
.why .c p{color:[[MUTED]];font-size:8.6pt;margin-top:3px}
.cta{margin-top:16px;background:linear-gradient(135deg,[[NAVY]],[[BLUE]]);color:#fff;border-radius:14px;padding:20px 22px;text-align:center}
.cta h3{color:#fff;font-size:15pt}.cta p{color:#cfe0f5;margin-top:5px;font-size:9.4pt}
"""
for _k, _v in C.items():
    CSS = CSS.replace(f"[[{_k}]]", _v)


def _header(co):
    return f'''
<div class="hd">
  <div class="hd-row">
    {logo_block(co.get("logo"))}
    <div class="r"><b>{co['name']}</b><br>{co['tag1']}<br>{co['tag2']}
    <div class="gst">GSTIN: {co['gstin']}</div></div>
  </div>
  <div class="hdbar"></div>
</div>'''


def _footer(co):
    return f'''
<div class="ft"><div class="ftbar"></div><div class="in">
  <span>{co['addr']}</span>
  <span><b>{co['phone']}</b> &nbsp;|&nbsp; {co['email']} &nbsp;|&nbsp; {co['web']}</span>
</div></div>'''


def _frame():
    return '<div class="frame"></div>'


def _watermark(co):
    src = co.get("watermark") or co.get("logo")
    if src and os.path.exists(src):
        return f'<div class="pgwm"><img src="{_fileuri(src)}" style="width:120mm"></div>'
    return f'<div class="pgwm">{emblem(150)}</div>'


def _logo_mark(co, size=80):
    """Uploaded logo image if available, else the built-in emblem."""
    src = co.get("logo")
    if src and os.path.exists(src):
        return f'<img src="{_fileuri(src)}" alt="logo" style="height:{size}px;width:auto">'
    return emblem(size)


def _product_range_inner(d):
    prods = d.get("products")
    if not prods:
        if not _pd:
            return ""
        prods = [{"name": n, "cat": c, "key": k, "img": None} for n, c, k in _pd.PRODUCT_RANGE]
    tiles = ""
    for p in prods:
        img = p.get("img")
        if img and os.path.exists(img):
            visual = f'<img src="{_fileuri(img)}" alt="" style="width:100%;height:100%;object-fit:cover">'
        elif _pd and p.get("key") in _pd.SVGS:
            visual = _pd.SVGS[p["key"]]()
        else:
            visual = ""
        tiles += (f'<div class="ptile"><div class="pimg">{visual}</div>'
                  f'<div class="pcap"><div class="pcat">{p.get("cat","")}</div><div class="pname">{p["name"]}</div></div></div>')
    return (f'<div class="ribbon" style="background:{C["BLUE"]}">OUR <i style="color:#fff">PRODUCT RANGE</i></div>'
            f'<div class="h2c">Complete Water Plant &amp; Packaging Machinery</div>'
            f'<p class="muted small" style="text-align:center;margin:-4px 0 6px">A single source for your entire bottling line &mdash; from RO purification to shrink packaging.</p>'
            f'<div class="pgrid">{tiles}</div>')





def _sign(co):
    return (f'<div class="sign"><div class="muted small">For</div>'
            f'<div class="co">{co["name"]}</div>'
            f'<div class="ln">Authorised Signatory</div></div>')


def build_html(d):
    co = d["company"]

    # page 1 - cover
    p1_inner = f'''
<div class="metarow">
  <div class="reftag"><b>Ref No.:</b> {d['meta']['ref']}</div>
  <div class="reftag" style="border-left-color:{C['RED']}"><b>Date:</b> {d['meta']['date']}</div>
</div>
<div class="tobox">
  <div class="b navy">To,</div>
  <div class="b" style="font-size:11pt">{d['customer']['name']}</div>
  <div>{d['customer']['firm']}</div>
  <div class="muted small">{d['customer']['city']} &nbsp;&middot;&nbsp; Mob: {d['customer']['mob']}</div>
</div>
<div class="subj"><b>Subject:</b> {d['subject']}</div>
<p style="margin:10px 0">Dear Sir,</p>
<p style="margin-bottom:10px">{d['intro']}</p>
<p style="margin-bottom:6px">This proposal is organised as follows:</p>
<table class="anx">
  <tr><td class="k">Annexure &ndash; I</td><td>Technical Specifications &amp; Machine Quality Parts</td></tr>
  <tr><td class="k">Annexure &ndash; II</td><td>Price Schedule</td></tr>
  <tr><td class="k">Annexure &ndash; III</td><td>Commercial Terms &amp; Conditions</td></tr>
</table>
<p style="margin-top:10px">We are confident this offer meets your requirement, and we look forward to a strong,
long-term business relationship.</p>
{_sign(co)}'''


    # page 2 - specs + parts
    specs = d["specs"]; half = (len(specs) + 1) // 2
    def spec_tbl(rows):
        return "<table class='tbl'>" + "".join(f"<tr><td class='b navy'>{k}</td><td>{v}</td></tr>" for k, v in rows) + "</table>"
    parts = "".join(f"<tr><td class='b navy'>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in d["parts"])
    p2_inner = f'''
<div class="ribbon">ANNEXURE &ndash; <i>I</i></div>
<div class="h2c">Technical Specifications</div>
<div class="spec2"><div>{spec_tbl(specs[:half])}</div><div>{spec_tbl(specs[half:])}</div></div>
<div class="h2c" style="margin-top:16px">Machine Quality Parts</div>
<table class="tbl"><thead><tr><th style="width:44%">Item / Part</th><th>Make / Company</th><th>Origin</th></tr></thead>
<tbody>{parts}</tbody></table>'''


    # page 3 - price schedule
    rows = ""
    total = 0
    for i, it in enumerate(d["items"], 1):
        pv = it.get("price")
        try:
            fv = float(pv)
            total += int(round(fv))                 # numeric -> added to total
            price_disp = "&#8377; " + inr(fv)
        except Exception:                            # text (e.g. "On Request") -> shown as-is, counts as 0
            price_disp = str(pv) if (pv is not None and str(pv).strip() != "") else "&mdash;"
        rows += f'''<tr>
          <td class="num">{i}</td>
          <td class="img"><div class="ib">{item_image(it.get("img"))}</div></td>
          <td><div class="nm">{it['name']}</div><div class="ds">{it.get('desc','')}</div></td>
          <td class="qty">{it.get('qty','1 Set')}</td>
          <td class="amt">{price_disp}</td>
        </tr>'''
    try:
        pct = float(d.get("gst_percent") or 0)
    except Exception:
        pct = 0.0
    gst_apply = bool(d.get("gst_apply")) and pct > 0
    if gst_apply:
        gst_amt = int(round(total * pct / 100.0))
        grand = total + gst_amt
        pctxt = "%g" % pct
        totals_html = (
            f'<tr class="subrow"><td colspan="4" style="text-align:right">Sub-Total</td><td class="amt">&#8377; {inr(total)}</td></tr>'
            f'<tr class="subrow"><td colspan="4" style="text-align:right">GST @ {pctxt}%</td><td class="amt">&#8377; {inr(gst_amt)}</td></tr>'
            f'<tr class="totrow"><td colspan="4" style="text-align:right">Grand Total (incl. GST)</td><td class="amt" style="font-size:11pt">&#8377; {inr(grand)}</td></tr>'
            f'<tr class="taxrow"><td colspan="5"><b>Transportation Extra</b> (as actual, ex-factory Ghaziabad)</td></tr>')
    else:
        pctxt = ("%g" % pct) if pct else "18"
        totals_html = (
            f'<tr class="totrow"><td colspan="4" style="text-align:right">Total Amount</td><td class="amt" style="font-size:11pt">&#8377; {inr(total)}</td></tr>'
            f'<tr class="taxrow"><td colspan="5"><b>GST @ {pctxt}% Extra</b> &nbsp;&middot;&nbsp; <b>Transportation Extra</b> (as actual, ex-factory Ghaziabad)</td></tr>')
    p3_inner = f'''
<div class="ribbon">ANNEXURE &ndash; <i>II</i></div>
<div class="h2c">Price Schedule</div>
<table class="price">
  <thead><tr><th style="width:24px">#</th><th style="width:72px">Image</th><th>Description</th><th style="text-align:center">Qty</th><th style="text-align:right">Price (INR)</th></tr></thead>
  <tbody>
    {rows}
    {totals_html}
  </tbody>
</table>
<div class="note"><b>Please note:</b> {d.get('note','')}</div>
{_sign(co)}'''


    # page 4 - terms
    lis = "".join(f"<li><b>{t}:</b> {b}</li>" for t, b in d["terms"])
    p4_inner = f'''
<div class="ribbon">ANNEXURE &ndash; <i>III</i></div>
<div class="h2c">Commercial Terms &amp; Conditions</div>
<ol class="terms">{lis}</ol>'''


    # page 5 - bank
    bk = d["bank"]
    p5_inner = f'''
<div class="ribbon" style="background:{C['GREEN']}">PAYMENT <i style="color:#fff">DETAILS</i></div>
<div class="h2c">Bank &amp; Company Details</div>
<p class="muted small" style="margin-bottom:4px">Funds may be transferred via NEFT, RTGS, Cheque or DD.</p>
<div class="bankgrid">
  <div class="row"><div class="k">Company Name</div><div class="v b navy">{co['name']}</div></div>
  <div class="row"><div class="k">GSTIN</div><div class="v">{co['gstin']}</div></div>
  <div class="row"><div class="k">Bank Name</div><div class="v">{bk['name']}</div></div>
  <div class="row"><div class="k">Account No.</div><div class="v">{bk['ac']}</div></div>
  <div class="row"><div class="k">Branch</div><div class="v">{bk['branch']}</div></div>
  <div class="row"><div class="k">IFSC Code</div><div class="v">{bk['ifsc']}</div></div>
</div>
<div style="margin-top:14px"><span class="chip">NEFT</span><span class="chip">RTGS</span><span class="chip">Cheque</span><span class="chip">Demand Draft</span></div>
<div class="note" style="margin-top:16px">Kindly share the transaction reference after payment so we can promptly process your order and proforma invoice.</div>
{_sign(co)}'''


    # page 6 - thank you
    whys = [
        ("In-House Manufacturing", "Complete range built and tested under one roof for reliable quality."),
        ("Turnkey Solutions", "From RO purification to filling, labelling, coding and packaging."),
        ("Installation &amp; Training", "On-site commissioning and operator training included."),
        ("After-Sales Support", "Prompt service and genuine spare-parts support across India."),
    ]
    wh = "".join(f'<div class="c"><b>{t}</b><p>{p}</p></div>' for t, p in whys)
    p6_inner = f'''
<div style="text-align:center;margin-top:4px">{_logo_mark(co, 80)}</div>
<div class="h2c" style="margin-top:8px">Thank You for the Opportunity</div>
<p style="text-align:center;color:{C['MUTED']};max-width:150mm;margin:0 auto">We appreciate your interest in {co['name']}.
Our team is committed to helping you set up and scale a productive, profitable plant.</p>
<div class="h2c" style="margin-top:18px">Why Choose Bharat iON Systems</div>
<div class="why">{wh}</div>
<div class="cta"><h3>Ready to move forward?</h3>
<p>Call or WhatsApp <b>{co['phone']}</b> &nbsp;|&nbsp; {co['email']} &nbsp;|&nbsp; {co['web']}</p></div>
<div class="sign" style="text-align:right"><div class="muted small">For</div>
<div class="co">{co['name']}</div><div class="ln" style="margin-left:auto">Authorised Signatory</div></div>'''
    # assemble pages (product range added before the thank-you page)
    inners = [p1_inner, p2_inner, p3_inner, p4_inner, p5_inner]
    if _pd or d.get("products"):
        inners.append(_product_range_inner(d))
    inners.append(p6_inner)
    # page chrome is declared ONCE and (being position:fixed) repeats on every page;
    # sections then flow and paginate automatically, so long item lists spill cleanly.
    chrome = _watermark(co) + _frame() + _header(co) + _footer(co)
    body = chrome + "".join(f'<section class="section">{inner}</section>' for inner in inners)
    return f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"


# ---------------------------------------------------------------- PDF + lock
def lock_pdf(pdf_bytes):
    """AES-256 encrypt with a random owner password; no user password so the
    file opens freely, but editing / copying / annotating is disabled."""
    pdf = pikepdf.open(io.BytesIO(pdf_bytes))
    perms = pikepdf.Permissions(
        accessibility=True, extract=False, modify_annotation=False,
        modify_assembly=False, modify_form=False, modify_other=False,
        print_lowres=True, print_highres=True,
    )
    out = io.BytesIO()
    pdf.save(out, encryption=pikepdf.Encryption(
        owner=secrets.token_urlsafe(24), user="", R=6, allow=perms))
    return out.getvalue()


def flatten_pdf(pdf_bytes, dpi=150):
    """Rasterise every page (removes the editable text layer entirely)."""
    import fitz
    src = fitz.open(stream=pdf_bytes, filetype="pdf")
    out = fitz.open()
    for page in src:
        pix = page.get_pixmap(dpi=dpi)
        np = out.new_page(width=page.rect.width, height=page.rect.height)
        np.insert_image(page.rect, pixmap=pix)
    buf = out.tobytes()
    return buf


def render_pdf_bytes(data, flatten=False, lock=True):
    pdf = HTML(string=build_html(data)).write_pdf()
    if flatten:
        pdf = flatten_pdf(pdf)
    if lock:
        pdf = lock_pdf(pdf)
    return pdf


# ---------------------------------------------------------------- defaults
def default_data():
    return {
        "company": {
            "name": "Bharat iON Systems Pvt. Ltd.",
            "tag1": "Manufacturer of Water Treatment &amp; Bottle Packaging Machinery",
            "tag2": "Fully &amp; Semi-Automatic PET Blowing Machines &middot; RO Plants &middot; Filling &middot; Labelling &middot; Packaging",
            "addr": "2882, 1st Floor, Karheda, Ghaziabad, Uttar Pradesh &ndash; 201007",
            "phone": "+91 83840 61695",
            "email": "info@bharationsystems.com",
            "web": "www.bharationsystems.com",
            "gstin": "[GSTIN to be added]",
            "logo": None,
            "watermark": None,
        },
        "bank": {"name": "[Bank name]", "ac": "[Account number]", "branch": "[Branch]", "ifsc": "[IFSC code]"},
        "meta": {"ref": "BIS/QT/2026/001", "date": "29/07/2026", "validity": "30 days from date of offer"},
        "customer": {"name": "Mr. Rajesh Kumar", "firm": "M/s Shri Balaji Beverages",
                     "city": "Nagpur, Maharashtra", "mob": "+91 9XXXX XXXXX"},
        "gst_apply": True, "gst_percent": 18,
        "subject": "Quotation for 2-Cavity Semi-Automatic PET Blowing Machine with Accessories",
        "intro": ("Thank you very much for your enquiry. We are pleased to submit our most competitive "
                  "quotation for the Semi-Automatic PET Blowing Machine along with accessories. "
                  "Bharat iON Systems is a manufacturer of world-class machinery for the water treatment, "
                  "beverage and packaging industry."),
        "specs": [
            ("Production Volume", "100 ml &ndash; 2 Ltr"), ("Production Capacity", "1000 &ndash; 1200 Pcs/Hr"),
            ("Working Air Pressure", "10 &ndash; 12 kg/cm&sup2;"), ("Blowing Air Pressure", "18 &ndash; 26 kg/cm&sup2;"),
            ("Clamping Force (Locking)", "8 Ton"), ("High Air Pressure Consumption", "50 &ndash; 55 CFM"),
            ("Tie Bar Distance", "350 mm"), ("Max Mould Opening Stroke", "240 mm"),
            ("Air Compressor", "20 H.P"), ("Mould Cavity", "2 / 1"),
            ("Mould Thickness", "180 &ndash; 250 mm"), ("Neck Diameter", "25 &ndash; 120 mm"),
            ("Operation", "Hydro / Pneumatic"), ("Staff Required", "2 Persons"),
            ("Area Requirement", "Approx. 12 m&sup2;"), ("Heater Power Running Load", "3 &ndash; 10 kW"),
            ("Machine Weight", "1300 kg"), ("Heater Type", "Infrared Conveyor"),
        ],
        "parts": [
            ("Pneumatic Valves", "Mercury", "Mumbai, India"), ("Pneumatic Cylinders", "Mercury", "Mumbai, India"),
            ("PLC Card", "Ultra", "Mumbai, India"), ("PU Pipe", "Janatics", "Coimbatore, India"),
            ("MCB", "Schneider", "France"), ("IR Lamp", "Imported", "Taiwan"),
            ("Hydraulic Pipe", "Dolphin", "India"), ("Wiring", "Havells", "India"),
        ],
        "items": [
            {"img": None, "name": "Semi-Automatic Auto-Drop PET Blowing Machine (2 Cavity)",
             "desc": "With neck settings. 100 ml&ndash;500 ml @ 1000&ndash;1200 bph; 500 ml&ndash;1 Ltr @ 1000&ndash;1100 bph.*",
             "qty": "1 Set", "price": 385000},
            {"img": None, "name": "20 HP Air-Cooled Compressor (High Pressure)",
             "desc": "54 CFM, up to 25 kg/cm&sup2;&middot;g, tank mounted with pressure switch &amp; loading/unloading valve.",
             "qty": "1 Set", "price": 245000},
            {"img": None, "name": "Refrigerated Air Dryer (High Pressure)",
             "desc": "Large condenser, advanced heat exchangers, digital control. Up to 40 kg/cm&sup2;&middot;g, 80&ndash;100 CFM.",
             "qty": "1 Set", "price": 60000},
            {"img": None, "name": "Water Chiller &ndash; 2 TR",
             "desc": "Compact chiller with inbuilt pump motor for consistent cooling.", "qty": "1 Set", "price": 75000},
        ],
        "note": ("*Output depends on preform quality, bottle size, shape &amp; weight. Any mould size can be "
                 "manufactured at additional cost. Prices are valid for 30 days from the date of quotation."),
        "terms": [
            ("Jurisdiction", "All disputes are subject to Ghaziabad (U.P.) jurisdiction. Prices are net, ex-factory and exclusive of packing."),
            ("Erection &amp; Commissioning", "Client to complete plumbing and electrical work before erection. Supervision, commissioning and training are included if completed within 2 days; travel, lodging, food and local conveyance are in the client&rsquo;s scope. Beyond 2 days, &#8377; 2,500 per person per day applies."),
            ("Handing Over", "Machinery will be installed, commissioned and trial-run. The client must ensure consumables for the trial. Delays beyond our scope are chargeable at &#8377; 2,500 per engineer per day."),
            ("Delivery", "Within 4 to 6 weeks from a commercially clear purchase order with advance payment."),
            ("Dispatch", "F.O.R basis (ex-factory), Ghaziabad. Transport charges are in the client&rsquo;s scope, paid as actual."),
            ("Insurance", "Transit insurance is charged extra as actual, or arranged by the client."),
            ("Payment Terms", "50% advance with a technically &amp; commercially clear PO. Balance 50% against proforma invoice prior to dispatch (including taxes)."),
            ("Taxes", "GST @ 18% (as applicable) is payable extra on the total cost of the machine."),
            ("Validity", "Offer valid for 30 days. Cancellation: within 1 week &ndash; 20%, 2 weeks &ndash; 40%, 3 weeks &ndash; 100% of amount paid."),
            ("Guarantee / Warranty", "12 months from dispatch against manufacturing defects of mechanical items. Consumables (IR lamps, electrical &amp; rubber) and transit damage are not covered."),
        ],
    }


if __name__ == "__main__":
    pdf = render_pdf_bytes(default_data(), flatten=False, lock=False)
    with open("../pdf/quotation-sample.pdf", "wb") as f:
        f.write(pdf)
    print("wrote sample")
