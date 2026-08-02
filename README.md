# Bharat iON Systems — Website

A fast, mobile-first, **SEO-optimised static website** built to rank on Google and
generate organic leads for Bharat ION Systems Pvt. Ltd. (water plant & packaging machinery).

## Pages (12)
- `index.html` — Home (hero, machinery, turnkey line, why-us, applications, CTA, FAQ)
- `about.html`, `applications.html`, `contact.html` (with enquiry form)
- `products.html` + 7 individual product pages under `products/`

## SEO built in
- Unique `<title>` + meta description + canonical on every page
- Open Graph / Twitter tags, mobile viewport, fast (no heavy frameworks)
- **Structured data (JSON-LD):** Organization, WebSite, FAQPage, Product,
  BreadcrumbList, LocalBusiness, ItemList
- Keyword-focused, descriptive URLs (e.g. `/products/industrial-ro-water-treatment-plant.html`)
- `sitemap.xml` + `robots.txt`
- Semantic headings, alt text, internal linking

## Lead generation
- Enquiry form on Contact + product CTAs (uses **Web3Forms** — free, no backend)
- Floating **WhatsApp** + **Call** buttons on every page
- Click-to-call and pre-filled WhatsApp links throughout

## ✅ Before going live — update these in `build_site.py` (CFG)
1. `PHONE_DISPLAY`, `PHONE_TEL`, `WHATSAPP` — real phone/WhatsApp number
2. `EMAIL`, `ADDR`, `CITY` — real email and full address
3. `DOMAIN` — the live domain (used in canonical + sitemap)
4. `WEB3FORMS_KEY` — get a free access key at web3forms.com so the form emails you
5. Add the real logo as `website/assets/logo.png` (see assets note)

Then rebuild: `python3 build_site.py`

## How to host (any of these — all cheap/free)
- **Netlify / Vercel / Cloudflare Pages:** drag-drop the `website/` folder (instant HTTPS)
- **GitHub Pages:** serve the folder
- **Any cPanel / shared hosting:** upload the contents of `website/` to `public_html`
- Point your domain, then submit `sitemap.xml` in **Google Search Console**

## Rebuild
```bash
pip install weasyprint   # only needed because catalogue.py is imported
python3 build_site.py
```
