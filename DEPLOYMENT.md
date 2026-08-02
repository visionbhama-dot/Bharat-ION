# Deployment Guide — Bharat iON Systems

Everything below uses **free** plans. There are two pieces:

| Piece | What it is | Where we host it |
|-------|-----------|------------------|
| **Website** (`index.html`, `products/`, `blog/`, `admin/`, …) | Static HTML/CSS/JS | **Vercel** (free) |
| **Quotation Generator** (`quote-app/`) | Python/Flask app that makes the PDF | **Render** (free, Docker) |

They are hosted separately because the site is static but the quotation app is a
Python server. The admin panel simply **links** to the quotation app.

> **Do this first:** merge Pull Request #1 into `main`. The deploy buttons and
> importers below read the repository's default branch, so the config files
> (`render.yaml`, `vercel.json`, `Dockerfile`) must be on `main`.

---

## Part A — Backend: quotation app on Render (free)

The repo already contains everything Render needs: `render.yaml` (blueprint) and
`quote-app/Dockerfile` (installs the WeasyPrint system libraries).

**Option 1 — one click**

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/visionbhama-dot/Bharat-ION)

**Option 2 — manual (Blueprint)**
1. Create a free account at <https://render.com> and connect your GitHub.
2. **New +** → **Blueprint** → pick the `Bharat-ION` repo → **Apply**.
3. Render reads `render.yaml`, builds the Docker image and starts the service.
4. When it's live you'll get a URL like `https://bharation-quotation.onrender.com`.
   **Copy this URL** — you'll need it in Part C.

Notes about the free tier:
- The service **sleeps after ~15 min idle**; the first request then takes ~30–50s
  to wake. Fine for occasional quotations.
- The filesystem is **ephemeral** — uploaded logos/images are used for the PDF but
  are not stored permanently (they reset on restart). Re-upload as needed.
- 512 MB RAM is enough for the 6-page PDF (one worker is configured).

_Railway alternative:_ the same `quote-app/Dockerfile` works on Railway
(<https://railway.app> → New → Deploy from repo → it auto-detects the Dockerfile).
Set the service root to `quote-app`.

---

## Part B — Frontend: website on Vercel (free)

1. Create a free account at <https://vercel.com> and connect GitHub.
2. **Add New… → Project** → import the `Bharat-ION` repo.
3. Settings (Vercel auto-detects a static site):
   - **Framework Preset:** Other
   - **Root Directory:** `./` (repo root)
   - **Build Command:** _leave empty_
   - **Output Directory:** _leave empty_
4. **Deploy.** You'll get a URL like `https://bharat-ion.vercel.app`.

`vercel.json` keeps the `.html` URLs (so they match your canonical tags), serves
the custom `404.html`, and adds a `noindex` header on `/admin`. The Flask
`quote-app` is excluded from the frontend via `.vercelignore`.

_GitHub Pages alternative:_ repo **Settings → Pages → Deploy from branch →
`main` / root**. Add a `CNAME` file with your domain if you use Pages. (Vercel is
recommended because it auto-deploys on every push and handles the domain easily.)

---

## Part C — Connect the two (important)

After the backend is live on Render:

1. Open `admin/config.js` and set the quotation app URL:
   ```js
   quoteApp: {
     url: "https://bharation-quotation.onrender.com",   // <- your Render URL
     ...
   }
   ```
2. Commit & push. Vercel redeploys automatically.
3. Now in the site: `/admin/` → **Quotation Maker** → **Open Quotation Generator**
   opens your hosted PDF tool.

---

## Custom domain — `bharationsystems.com`

The site's canonical tags already use `https://bharationsystems.com`.

**On Vercel:** Project → **Settings → Domains** → add `bharationsystems.com` (and
`www`). Vercel shows the exact DNS records (an `A` record / `CNAME`) to set at
your domain registrar. SSL is issued automatically.

Optionally give the quotation app a subdomain (e.g. `quote.bharationsystems.com`)
in Render → Settings → Custom Domains, then use that in `admin/config.js`.

---

## Quick checklist
- [ ] Merge PR #1 into `main`
- [ ] Render: deploy blueprint → copy the service URL
- [ ] Vercel: import repo → deploy
- [ ] Put the Render URL into `admin/config.js` → push
- [ ] Point `bharationsystems.com` DNS at Vercel
- [ ] Test: home page, a product page, `/admin/` (passcode), launch the quotation app

---
Designed & Developed by [Bhama Vision](https://www.bhamavision.com).
