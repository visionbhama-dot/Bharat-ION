# Bharat iON Systems — Admin Panel

A lightweight, self-contained admin panel for the website. It runs entirely in
the browser (no server required) and lives at **`/admin/`**.

Open it at: `https://bharationsystems.com/admin/` (or your host) and enter the
passcode set in `config.js`.

## What's inside

| Tool | File | What it does |
|------|------|--------------|
| **Dashboard** | `index.html` | Overview + recent quotations / drafts |
| **Quotation Maker** | `quotation.html` | Launches the `quote-app` PDF generator; also has a quick in-browser quote (print / save as PDF, save & reload) |
| **Blog Composer** | `blog.html` | Write posts and generate a ready-to-publish HTML file matching the site, plus card + sitemap snippets |
| **Image Manager** | `images.html` | Preview every image slot and prepare correctly-named files (logo, favicon, banners, product photos) |

Data (quotations, blog drafts) is stored in the browser via `localStorage` on
the device you use — nothing leaves your computer unless you connect a backend.

## Configuration — `config.js`

Edit `admin/config.js` to change:

- **Company details** (shown on quotations & generated pages)
- **Quotation defaults** (currency, GST %, quote-number prefix, validity, terms)
- **Access passcode** — `auth.passcode`. Set to `""` to disable the gate.
  > This is a *soft* client-side gate only. For real protection use your backend.
- **Product catalogue** — used by the quotation & blog tools.

## The Quotation Generator — `quote-app/`

The professional, locked **6-page A4 PDF** quotation is produced by the Flask
app in the repo's `quote-app/` folder (WeasyPrint + pikepdf). It is a Python
server, so it runs **separately** from this static website.

**Run it locally**
- Windows: double-click `quote-app/run.bat` (installs deps on first run).
- Mac/Linux: `cd quote-app && pip install -r requirements.txt && python3 app.py`
- It serves at `http://localhost:5000`.

**Use it from the admin panel**
- Open **Quotation Maker** and click **Open Quotation Generator** — it opens the
  address in `config.js` → `quoteApp.url` (default `http://localhost:5000`).

**Host it (so it's available without your PC)**
Deploy `quote-app/` to any Python host (Render, Railway, PythonAnywhere, a VPS…)
and put its public URL in `config.js` → `quoteApp.url`. That's the only change
needed here.

> Note: a page served over **https** can't embed an **http://localhost** page in
> an iframe (browser mixed-content rule), which is why the admin *opens* the
> generator in a new tab instead of embedding it.

## Optional generic backend (`apiBaseUrl`)

Independently of the quote-app, you can point the tools at a JSON/upload API by
setting `apiBaseUrl` in `config.js`. When set, they also call:

| Action | Request |
|--------|---------|
| Save a quotation (quick tool) | `POST {apiBaseUrl}/quotations` — JSON body |
| Save a blog post | `POST {apiBaseUrl}/blog` — JSON `{ post, html }` |
| Upload an image | `POST {apiBaseUrl}/upload` — `multipart/form-data`, fields `file` and `slot` |

Leave it `""` to run fully offline in the browser.

## Publishing blog posts (static workflow)

Because the main site is static:
1. In **Blog Composer**, fill the fields and click **Generate HTML**.
2. **Download** the post file and place it in `/blog/`.
3. Paste the **card snippet** into `blog.html` (inside `.blogwrap`) and add the
   **sitemap entry** to `sitemap.xml`.

With a backend connected, step 2–3 can be automated on your server instead.

---
Designed & Developed by [Bhama Vision](https://www.bhamavision.com).
