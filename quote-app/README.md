# Bharat ION Systems — Quotation Generator (backend)

A small web app to create the world-class **6-page A4 quotation** in seconds:
type the changing details, upload a logo and per-item product images, and
**download a locked (non-editable) PDF**.

## Features
- **Editor UI** — type all the changing fields (customer, ref/date, subject, intro,
  price items, specs, parts, terms, bank details).
- **Logo upload** — drops into every page header + watermark (remembered for next time).
- **Per-item image upload** — each price-schedule row shows its product photo.
- **Always A4** — pages are fixed A4 with a decorative border, so the design never breaks.
- **Locked PDF** — the downloaded file is **AES-256 encrypted** with editing, copying and
  annotation **disabled**, so it can't be modified in normal PDF tools (printing is allowed).
- **Extra-lock (flatten)** — optional: rasterises every page so there is no editable text
  layer at all (maximum tamper resistance).
- **Preview** — opens an unlocked PDF in a new tab for a quick check before downloading.

## Run it

### Windows (easiest)
Double-click **`run.bat`**. It installs dependencies on first run, starts the
server and opens `http://localhost:5000` in your browser.
> WeasyPrint needs the **GTK3 runtime** on Windows. If you see a "cannot load
> library / pango / cairo" error, install it from the
> [GTK3 runtime installer](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases)
> and run `run.bat` again.

### Mac / Linux (or manual)
```bash
cd quote-app
pip install -r requirements.txt
python3 app.py
# open http://localhost:5000
```

## Permanent images (no re-uploading)

Free hosts like Render have an **ephemeral disk**, so anything uploaded at runtime
is lost on restart. To avoid re-uploading every time, the fixed images now **ship
with the app** in `quote-app/assets/` and are used automatically:

- **`assets/logo.png`** — company logo (header, watermark, thank-you page).
- **`assets/products/<key>.jpg`** — product-range photos. Keys: `semi`,
  `handblow`, `full`, `ro`, `station`, `fill`, `label`, `shrink`, `ink`.

In the editor you can also pick **"Use machine photo"** on any price-schedule row
to reuse these permanent photos instead of uploading.

**To change a permanent image:** replace the file in `quote-app/assets/` (keep the
same name) and redeploy. Uploading in the editor still works as a one-off override,
and image fields also accept full `https://` URLs.

## How to use
1. Fill in the fields (they come pre-filled with a sample quotation).
2. Upload your **logo** and each item's **image** (optional — a placeholder is used if none).
3. Add/remove price items with **+ Add item** / **Remove**.
4. Click **Preview** to check, then **Download Locked PDF**.
5. Tick **Extra-lock (flatten)** for the most tamper-resistant output.

### Editing formats
- **Technical Specifications** — one per line: `Label: Value`
- **Machine Quality Parts** — one per line: `Item | Make | Origin`
- **Terms & Conditions** — one per line: `Title | Description`

## A note on "non-editable" PDFs
The locked PDF uses the PDF standard's **owner-password encryption** with modification
permissions turned off — every mainstream PDF tool (Acrobat, browsers, editors) will refuse
to edit, copy or extract it. The **flatten** option additionally removes the text layer.
No document format can be made 100% un-alterable against a determined attacker (anyone can
re-type a lookalike), but this makes casual editing effectively impossible, which is the
practical goal.

## Going live
`app.py` uses Flask's development server. For production, run behind a WSGI server, e.g.:
```bash
pip install waitress
waitress-serve --port=5000 app:app
```
The design lives in `quote_render.py` (single source of truth — same engine used for the
sample PDF). Edit colours/layout there and both the app and sample stay in sync.
