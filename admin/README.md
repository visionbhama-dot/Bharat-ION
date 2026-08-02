# Bharat iON Systems — Admin Panel

A lightweight, self-contained admin panel for the website. It runs entirely in
the browser (no server required) and lives at **`/admin/`**.

Open it at: `https://bharationsystems.com/admin/` (or your host) and enter the
passcode set in `config.js`.

## What's inside

| Tool | File | What it does |
|------|------|--------------|
| **Dashboard** | `index.html` | Overview + recent quotations / drafts |
| **Quotation Maker** | `quotation.html` | Build GST-ready quotations, print / save as PDF, save & reload |
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

## Connecting your backend (optional)

You mentioned you already have a backend (in a separate repo / a `quote-app`
folder). To use it, set `apiBaseUrl` in `config.js`:

```js
apiBaseUrl: "https://api.your-domain.com"
```

When set, the tools also call these endpoints (in addition to working locally):

| Action | Request |
|--------|---------|
| Save a quotation | `POST {apiBaseUrl}/quotations` — JSON body |
| Save a blog post | `POST {apiBaseUrl}/blog` — JSON `{ post, html }` |
| Upload an image | `POST {apiBaseUrl}/upload` — `multipart/form-data`, fields `file` and `slot` |

If your backend uses different routes, tell me the API contract (or share the
`quote-app` folder in this repo) and I'll wire the calls to match exactly. The
endpoint names above are placeholders chosen to be easy to implement.

## Publishing blog posts (static workflow)

Because the main site is static:
1. In **Blog Composer**, fill the fields and click **Generate HTML**.
2. **Download** the post file and place it in `/blog/`.
3. Paste the **card snippet** into `blog.html` (inside `.blogwrap`) and add the
   **sitemap entry** to `sitemap.xml`.

With a backend connected, step 2–3 can be automated on your server instead.

---
Designed & Developed by [Bhama Vision](https://www.bhamavision.com).
