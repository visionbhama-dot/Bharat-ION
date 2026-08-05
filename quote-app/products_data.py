"""Self-contained product illustrations + list for the quotation product-range page (copied from catalogue.py)."""

# ---- Palette (bold water / industrial) ----
NAVY   = "#06305B"
NAVY2  = "#08213F"
BLUE   = "#0E63B3"
AQUA   = "#12B5D8"
AQUAL  = "#7FD6E8"
ICE    = "#EAF6FB"
INK    = "#12222E"
MUTED  = "#5C6E7A"
LINE   = "#DCE7EF"
STEEL  = "#C9D7E1"
STEELD = "#9DB2C1"
WATER  = "#BFE8F4"
WHITE  = "#FFFFFF"


# ============================================================
# SVG BUILDING BLOCKS
# ============================================================
def bottle(x, y, s=1.0, c=WATER):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<rect x="3" y="0" width="6" height="3.5" rx="1" fill="{NAVY}"/>'
            f'<rect x="3.6" y="3.3" width="4.8" height="4" fill="{c}" stroke="{NAVY}" stroke-width="0.6"/>'
            f'<path d="M2 7 h8 v16 q0 3 -3 3 h-2 q-3 0 -3 -3 z" fill="{c}" stroke="{NAVY}" stroke-width="0.8"/>'
            f'<rect x="2" y="12" width="8" height="4" fill="{AQUA}" opacity="0.35"/></g>')


def frame(inner, gid):
    return (f'<svg viewBox="0 0 340 210" xmlns="http://www.w3.org/2000/svg" '
            f'style="width:100%;height:100%;display:block">'
            f'<defs><linearGradient id="bg{gid}" x1="0" y1="0" x2="0" y2="210" gradientUnits="userSpaceOnUse">'
            f'<stop stop-color="#F3FAFD"/><stop offset="1" stop-color="#DCF0F7"/></linearGradient></defs>'
            f'<rect width="340" height="210" rx="14" fill="url(#bg{gid})"/>'
            f'<ellipse cx="170" cy="182" rx="150" ry="10" fill="{NAVY}" opacity="0.06"/>'
            f'{inner}</svg>')


def sv_semi_blow():
    b = "".join(bottle(250 + i * 16, 150, 0.9) for i in range(3))
    inner = f'''
    <rect x="70" y="95" width="120" height="78" rx="6" fill="{STEEL}" stroke="{NAVY}" stroke-width="2"/>
    <rect x="70" y="95" width="120" height="16" fill="{NAVY}"/>
    <rect x="82" y="120" width="60" height="44" rx="4" fill="{ICE}" stroke="{NAVY}" stroke-width="1.5"/>
    <circle cx="94" cy="132" r="3" fill="{AQUA}"/><circle cx="106" cy="132" r="3" fill="{BLUE}"/>
    <rect x="150" y="120" width="30" height="44" rx="3" fill="{NAVY}"/>
    <rect x="156" y="126" width="18" height="14" rx="2" fill="{AQUA}"/>
    <circle cx="159" cy="150" r="2.5" fill="{AQUAL}"/><circle cx="171" cy="150" r="2.5" fill="{AQUAL}"/>
    <!-- two blow-mould clamps -->
    <rect x="92" y="66" width="16" height="30" rx="2" fill="{STEELD}" stroke="{NAVY}" stroke-width="1.5"/>
    <rect x="116" y="66" width="16" height="30" rx="2" fill="{STEELD}" stroke="{NAVY}" stroke-width="1.5"/>
    <path d="M100 66 v-10 M124 66 v-10" stroke="{NAVY}" stroke-width="2"/>
    <circle cx="100" cy="54" r="4" fill="{AQUA}"/><circle cx="124" cy="54" r="4" fill="{AQUA}"/>
    <!-- conveyor out -->
    <rect x="190" y="168" width="120" height="6" rx="3" fill="{NAVY}"/>
    {b}
    <text x="80" y="88" font-family="Poppins,Arial" font-size="9" font-weight="700" fill="{NAVY}">SEMI-AUTO</text>
    '''
    return frame(inner, "semi")


def sv_full_blow():
    b = "".join(bottle(232 + i * 15, 152, 0.85) for i in range(5))
    inner = f'''
    <!-- preform hopper -->
    <path d="M36 70 h44 l-10 26 h-24 z" fill="{STEEL}" stroke="{NAVY}" stroke-width="2"/>
    <rect x="52" y="96" width="12" height="20" fill="{STEELD}" stroke="{NAVY}" stroke-width="1.2"/>
    <!-- heating oven tunnel -->
    <rect x="70" y="104" width="90" height="46" rx="5" fill="{NAVY}"/>
    {''.join(f'<circle cx="{82+i*14}" cy="118" r="4" fill="{AQUAL}"/><circle cx="{82+i*14}" cy="118" r="6" fill="none" stroke="{AQUA}" stroke-width="1" opacity="0.6"/>' for i in range(6))}
    <rect x="74" y="132" width="82" height="14" rx="2" fill="{BLUE}" opacity="0.5"/>
    <!-- rotary blow wheel -->
    <circle cx="196" cy="120" r="38" fill="{STEEL}" stroke="{NAVY}" stroke-width="2.5"/>
    <circle cx="196" cy="120" r="20" fill="{ICE}" stroke="{NAVY}" stroke-width="1.5"/>
    {''.join(f'<rect x="{194}" y="{80}" width="4" height="10" rx="1" fill="{NAVY}" transform="rotate({a} 196 120)"/>' for a in range(0,360,45))}
    <circle cx="196" cy="120" r="5" fill="{AQUA}"/>
    <!-- HMI panel -->
    <rect x="248" y="92" width="34" height="52" rx="3" fill="{NAVY}"/>
    <rect x="254" y="98" width="22" height="16" rx="2" fill="{AQUA}"/>
    <circle cx="259" cy="124" r="2.6" fill="{AQUAL}"/><circle cx="271" cy="124" r="2.6" fill="{AQUAL}"/>
    <!-- conveyor -->
    <rect x="150" y="170" width="160" height="6" rx="3" fill="{NAVY}"/>
    {b}
    '''
    return frame(inner, "full")


def sv_shrink():
    packs = ""
    for px in (44, 250):
        packs += (f'<g transform="translate({px},128)">'
                  f'<rect x="0" y="0" width="52" height="44" rx="4" fill="{AQUA}" opacity="0.25" stroke="{BLUE}" stroke-width="1.5"/>'
                  + "".join(bottle(6 + i * 14, 6, 0.8) for i in range(3)) + '</g>')
    inner = f'''
    <rect x="30" y="172" width="285" height="7" rx="3" fill="{NAVY}"/>
    {''.join(f'<rect x="{40+i*40}" y="179" width="6" height="16" fill="{NAVY}"/>' for i in range(7))}
    <!-- heat tunnel -->
    <path d="M120 150 v-44 a52 30 0 0 1 104 0 v44 z" fill="{NAVY}"/>
    <rect x="132" y="120" width="80" height="30" rx="3" fill="{NAVY2}"/>
    {''.join(f'<rect x="{140+i*22}" y="126" width="12" height="18" rx="2" fill="{AQUA}" opacity="0.7"/>' for i in range(3))}
    <rect x="120" y="150" width="104" height="6" fill="{BLUE}"/>
    <text x="146" y="100" font-family="Poppins,Arial" font-size="9" font-weight="700" fill="{NAVY}">HEAT TUNNEL</text>
    {packs}
    '''
    return frame(inner, "shrink")


def sv_inkjet():
    inner = f'''
    <!-- stand -->
    <rect x="60" y="60" width="10" height="96" fill="{STEELD}"/>
    <rect x="40" y="156" width="50" height="8" rx="3" fill="{NAVY}"/>
    <!-- controller -->
    <rect x="70" y="66" width="70" height="60" rx="6" fill="{NAVY}"/>
    <rect x="78" y="74" width="54" height="30" rx="3" fill="{AQUA}"/>
    <rect x="82" y="80" width="30" height="4" rx="2" fill="{WHITE}" opacity="0.85"/>
    <rect x="82" y="88" width="44" height="3" rx="1.5" fill="{WHITE}" opacity="0.6"/>
    <circle cx="82" cy="116" r="3" fill="{AQUAL}"/><circle cx="94" cy="116" r="3" fill="{AQUAL}"/><circle cx="106" cy="116" r="3" fill="{AQUAL}"/>
    <!-- umbilical + print head -->
    <path d="M140 100 q40 4 52 30" fill="none" stroke="{STEELD}" stroke-width="4"/>
    <rect x="188" y="128" width="16" height="20" rx="2" fill="{NAVY}"/>
    <path d="M196 148 l0 8" stroke="{AQUA}" stroke-width="2"/>
    <!-- conveyor + coded bottle -->
    <rect x="150" y="172" width="165" height="6" rx="3" fill="{NAVY}"/>
    {bottle(224, 150, 1.15)}
    <text x="240" y="160" font-family="monospace" font-size="8" fill="{BLUE}">MFG 04/26</text>
    <text x="240" y="169" font-family="monospace" font-size="8" fill="{BLUE}">B.NO 1245</text>
    '''
    return frame(inner, "ink")


def sv_filling():
    noz = "".join(f'<rect x="136" y="66" width="4" height="9" rx="1" fill="{NAVY}" transform="rotate({a} 140 112)"/>' for a in range(0, 360, 30))
    binq = "".join(bottle(40 + i * 15, 150, 0.85) for i in range(4))
    bout = "".join(bottle(232 + i * 15, 150, 0.85) for i in range(4))
    inner = f'''
    <rect x="30" y="170" width="285" height="6" rx="3" fill="{NAVY}"/>
    <!-- rotary carousel -->
    <circle cx="140" cy="112" r="60" fill="{STEEL}" stroke="{NAVY}" stroke-width="2.5"/>
    <circle cx="140" cy="112" r="60" fill="none" stroke="{AQUA}" stroke-width="3" opacity="0.5"/>
    <circle cx="140" cy="112" r="34" fill="{ICE}" stroke="{NAVY}" stroke-width="1.5"/>
    {noz}
    <circle cx="140" cy="112" r="10" fill="{NAVY}"/>
    <circle cx="140" cy="112" r="4" fill="{AQUA}"/>
    <text x="118" y="116" font-family="Poppins,Arial" font-size="8" font-weight="700" fill="{NAVY}">3-in-1</text>
    <!-- guard posts -->
    <rect x="80" y="120" width="4" height="52" fill="{STEELD}"/><rect x="196" y="120" width="4" height="52" fill="{STEELD}"/>
    <!-- water drops -->
    <path d="M258 60 q6 10 0 14 a4 4 0 0 1 -6 -3 q0 -6 6 -11 z" fill="{AQUA}"/>
    <path d="M276 74 q5 8 0 11 a3 3 0 0 1 -5 -2 q0 -5 5 -9 z" fill="{AQUAL}"/>
    {binq}{bout}
    '''
    return frame(inner, "fill")


def sv_ro():
    tanks = ""
    for i, x in enumerate((44, 78, 112)):
        tanks += (f'<path d="M{x} 80 q13 -14 26 0 v78 h-26 z" fill="{BLUE}" stroke="{NAVY}" stroke-width="2"/>'
                  f'<rect x="{x}" y="150" width="26" height="8" fill="{NAVY}"/>'
                  f'<rect x="{x+5}" y="96" width="16" height="30" rx="2" fill="{AQUA}" opacity="0.4"/>')
    membranes = ""
    for j, y in enumerate((104, 128)):
        membranes += (f'<rect x="176" y="{y}" width="120" height="18" rx="9" fill="{STEEL}" stroke="{NAVY}" stroke-width="2"/>'
                      f'<rect x="176" y="{y}" width="12" height="18" rx="6" fill="{AQUA}"/>'
                      f'<rect x="284" y="{y}" width="12" height="18" rx="6" fill="{AQUA}"/>')
    inner = f'''
    <!-- skid frame -->
    <rect x="34" y="74" width="276" height="92" rx="4" fill="none" stroke="{NAVY}" stroke-width="2.5"/>
    <rect x="34" y="160" width="276" height="8" fill="{NAVY}"/>
    {tanks}
    {membranes}
    <!-- pipes + gauges -->
    <path d="M150 90 h140 M160 158 h120" stroke="{STEELD}" stroke-width="3" fill="none"/>
    <circle cx="230" cy="90" r="7" fill="{WHITE}" stroke="{NAVY}" stroke-width="2"/>
    <path d="M230 90 l4 -4" stroke="{NAVY}" stroke-width="1.5"/>
    <circle cx="260" cy="90" r="7" fill="{WHITE}" stroke="{NAVY}" stroke-width="2"/>
    <path d="M260 90 l3 -5" stroke="{NAVY}" stroke-width="1.5"/>
    <text x="182" y="98" font-family="Poppins,Arial" font-size="8" font-weight="700" fill="{NAVY}">RO MEMBRANES</text>
    '''
    return frame(inner, "ro")


def sv_label():
    inner = f'''
    <rect x="30" y="170" width="285" height="6" rx="3" fill="{NAVY}"/>
    <!-- big label reel -->
    <circle cx="96" cy="104" r="46" fill="{ICE}" stroke="{NAVY}" stroke-width="2.5"/>
    <circle cx="96" cy="104" r="46" fill="none" stroke="{AQUA}" stroke-width="6" opacity="0.5"/>
    <circle cx="96" cy="104" r="30" fill="none" stroke="{STEELD}" stroke-width="2"/>
    <circle cx="96" cy="104" r="16" fill="none" stroke="{STEELD}" stroke-width="2"/>
    <circle cx="96" cy="104" r="7" fill="{NAVY}"/>
    <!-- label web feeding out -->
    <path d="M140 96 h60" stroke="{AQUA}" stroke-width="6" opacity="0.6"/>
    <rect x="150" y="90" width="14" height="9" fill="{BLUE}" opacity="0.6"/>
    <rect x="172" y="90" width="14" height="9" fill="{BLUE}" opacity="0.6"/>
    <!-- rewind reel -->
    <circle cx="212" cy="80" r="18" fill="{ICE}" stroke="{NAVY}" stroke-width="2"/>
    <circle cx="212" cy="80" r="6" fill="{NAVY}"/>
    <!-- dispenser + bottle -->
    <rect x="196" y="112" width="10" height="40" fill="{STEELD}" stroke="{NAVY}" stroke-width="1"/>
    {bottle(236, 138, 1.6)}
    <rect x="240" y="150" width="19" height="16" rx="1" fill="{WHITE}" stroke="{BLUE}" stroke-width="1.4"/>
    <rect x="242" y="154" width="15" height="2.5" fill="{AQUA}"/>
    '''
    return frame(inner, "label")


def cover_hero():
    b = "".join(bottle(150 + i * 20, 250, 1.6, WATER) for i in range(8))
    return f'''
    <svg viewBox="0 0 620 340" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block">
      <ellipse cx="310" cy="312" rx="300" ry="16" fill="#000" opacity="0.18"/>
      <!-- filling carousel -->
      <circle cx="120" cy="180" r="86" fill="#0B3F70" stroke="{AQUA}" stroke-width="4"/>
      <circle cx="120" cy="180" r="52" fill="#0A3260" stroke="{AQUAL}" stroke-width="2"/>
      {''.join(f'<rect x="116" y="98" width="7" height="16" rx="2" fill="{AQUAL}" transform="rotate({a} 120 180)"/>' for a in range(0,360,30))}
      <circle cx="120" cy="180" r="16" fill="{AQUA}"/>
      <!-- conveyor -->
      <rect x="150" y="286" width="440" height="10" rx="5" fill="#0B3F70"/>
      {b}
      <!-- RO tanks right -->
      <path d="M470 120 q22 -22 44 0 v150 h-44 z" fill="#0B3F70" stroke="{AQUA}" stroke-width="3"/>
      <path d="M524 120 q22 -22 44 0 v150 h-44 z" fill="#0A3260" stroke="{AQUAL}" stroke-width="3"/>
      <rect x="478" y="150" width="28" height="46" rx="3" fill="{AQUA}" opacity="0.4"/>
      <!-- water splash -->
      <path d="M300 70 q10 18 0 24 a7 7 0 0 1 -11 -5 q0 -10 11 -19 z" fill="{AQUA}"/>
      <circle cx="330" cy="60" r="6" fill="{AQUAL}"/><circle cx="352" cy="78" r="4" fill="{AQUA}"/>
    </svg>'''


def sv_hand_blow():
    b = "".join(bottle(252 + i * 15, 150, 0.85) for i in range(3))
    tray = "".join(
        f'<rect x="{34+i*12}" y="{64-i*2}" width="6" height="12" rx="2" fill="{STEELD}" stroke="{NAVY}" stroke-width="0.7" transform="rotate(-16 {37+i*12} 70)"/>'
        for i in range(4))
    inner = f'''
    <!-- hand-feed tray with preforms -->
    <path d="M26 74 l54 -14 l4 12 l-54 14 z" fill="{STEEL}" stroke="{NAVY}" stroke-width="1.6"/>
    {tray}
    <!-- cabinet -->
    <rect x="72" y="92" width="126" height="80" rx="6" fill="{STEEL}" stroke="{NAVY}" stroke-width="2"/>
    <rect x="72" y="92" width="126" height="15" fill="{NAVY}"/>
    <rect x="84" y="120" width="54" height="44" rx="4" fill="{ICE}" stroke="{NAVY}" stroke-width="1.4"/>
    <circle cx="96" cy="132" r="3" fill="{AQUA}"/><circle cx="108" cy="132" r="3" fill="{BLUE}"/>
    <rect x="150" y="118" width="34" height="46" rx="3" fill="{NAVY}"/>
    <rect x="156" y="124" width="22" height="15" rx="2" fill="{AQUA}"/>
    <!-- mould clamps -->
    <rect x="150" y="66" width="14" height="28" rx="2" fill="{STEELD}" stroke="{NAVY}" stroke-width="1.4"/>
    <rect x="172" y="66" width="14" height="28" rx="2" fill="{STEELD}" stroke="{NAVY}" stroke-width="1.4"/>
    <circle cx="157" cy="58" r="3.5" fill="{AQUA}"/><circle cx="179" cy="58" r="3.5" fill="{AQUA}"/>
    <rect x="198" y="168" width="112" height="6" rx="3" fill="{NAVY}"/>
    {b}
    <text x="28" y="98" font-family="Poppins,Arial" font-size="8" font-weight="700" fill="{NAVY}">HAND FEED</text>
    '''
    return frame(inner, "handblow")


def sv_station():
    bs = "".join(bottle(94 + i * 34, 130, 1.15) for i in range(5))
    noz = "".join(f'<rect x="{100+i*34}" y="106" width="5" height="18" fill="{NAVY}"/>' for i in range(5))
    drops = "".join(f'<circle cx="{102+i*34}" cy="128" r="2.4" fill="{AQUA}"/>' for i in range(5))
    inner = f'''
    <!-- support frame -->
    <rect x="60" y="58" width="230" height="10" rx="3" fill="{NAVY}"/>
    <rect x="66" y="68" width="8" height="44" fill="{STEELD}"/><rect x="276" y="68" width="8" height="44" fill="{STEELD}"/>
    <!-- overhead tank -->
    <rect x="118" y="34" width="114" height="26" rx="6" fill="{STEEL}" stroke="{NAVY}" stroke-width="2"/>
    <rect x="126" y="40" width="98" height="8" rx="3" fill="{AQUA}" opacity="0.5"/>
    <!-- nozzle beam + nozzles -->
    <rect x="80" y="98" width="200" height="9" rx="3" fill="{STEELD}" stroke="{NAVY}" stroke-width="1"/>
    {noz}{drops}
    <!-- conveyor + bottles -->
    <rect x="68" y="170" width="234" height="7" rx="3" fill="{NAVY}"/>
    {bs}
    <text x="122" y="52" font-family="Poppins,Arial" font-size="8" font-weight="700" fill="{NAVY}">FILLING STATIONS</text>
    '''
    return frame(inner, "station")


SVGS = {
    "semi": sv_semi_blow, "handblow": sv_hand_blow, "full": sv_full_blow,
    "ro": sv_ro, "station": sv_station, "fill": sv_filling,
    "label": sv_label, "shrink": sv_shrink, "ink": sv_inkjet,
    "nozfill4": sv_station, "rfc4": sv_filling,
}

# name, category, svg-key  (the 9 machines, same as the website)
PRODUCT_RANGE = [
    ("Semi-Automatic PET Blowing Machine", "PET Bottle Manufacturing", "semi"),
    ("Hand-Feed Automatic PET Blowing Machine", "PET Bottle Manufacturing", "handblow"),
    ("Fully Automatic PET Blowing Machine", "PET Bottle Manufacturing", "full"),
    ("Industrial RO Water Treatment Plant", "Water Treatment", "ro"),
    ("Station Filler (Bottle Filling Machine)", "Filling & Capping", "station"),
    ("Fully Automatic Rinsing, Filling & Capping Machine", "Filling & Capping", "fill"),
    ("Automatic Sticker Labelling Machine", "Labelling", "label"),
    ("Automatic Shrink Wrapping Machine", "Secondary Packaging", "shrink"),
    ("Batch Coding Machine", "Coding & Marking", "ink"),
    ("4-Nozzle Semi-Automatic Filler", "Filling & Capping", "nozfill4"),
    ("Semi-Automatic RFC Filling 4-Head Machine", "Filling & Capping", "rfc4"),
]
