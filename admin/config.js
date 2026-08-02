/* =============================================================
   Bharat iON Systems - Admin Panel configuration
   -------------------------------------------------------------
   Edit the values below. Everything works WITHOUT a backend
   (data is saved in your browser). If you have a backend API,
   set apiBaseUrl and the tools will also sync to it.
   ============================================================= */
window.ADMIN_CONFIG = {

  /* ---- Company details (used on quotations & generated pages) ---- */
  company: {
    name: "Bharat ION Systems Pvt. Ltd.",
    tagline: "Water Treatment & Bottle Packaging Machinery",
    phone: "+91 83840 61695",
    email: "info@bharationsystems.com",
    website: "https://bharationsystems.com",
    address: "2882, 1st Floor, Karheda, Ghaziabad, Uttar Pradesh 201007",
    gstin: "",            // add your GSTIN to show it on quotations
    logoPath: "../assets/images/logo/logo.png"
  },

  /* ---- Quotation defaults ---- */
  quotation: {
    currency: "INR",
    currencySymbol: "\u20B9",
    gstPercent: 18,
    prefix: "BIS",        // quote number prefix, e.g. BIS-2026-0001
    validityDays: 15,
    terms: "Prices are ex-works and valid for the period stated above. Taxes as applicable. Delivery and installation timelines confirmed on order."
  },

  /* ---- Soft access gate (client-side only, NOT real security) ----
     Leave passcode empty ("") to disable the gate. For real
     protection, use your backend authentication.                     */
  auth: {
    passcode: "bharat@2026"
  },

  /* ---- Quotation Generator (the Flask "quote-app" in this repo) ----
     The quote-app produces the professional, locked 6-page A4 PDF. It is a
     Python/Flask app, so it runs separately from this static site.
     - Locally: run quote-app/run.bat (Windows) or `python3 app.py`, then it
       serves at http://localhost:5000 (default below).
     - Hosted: after deploying with the included render.yaml, Render gives you a
       URL like  https://bharation-quotation.onrender.com  — paste it below and
       the admin "Launch" button will open it. (See DEPLOYMENT.md.)                */
  quoteApp: {
    // For local use keep localhost; after deploying to Render, replace with your
    // Render URL, e.g. "https://bharation-quotation.onrender.com"
    url: "http://localhost:5000",
    startHint: "Locally: run quote-app/run.bat (Windows) or 'python3 app.py'. Hosted: set this to your Render URL."
  },

  /* ---- Optional backend API ----
     If you host the backend (your separate repo / "quote-app"),
     put its base URL here, e.g. "https://api.yourdomain.com".
     Endpoints the tools will call when this is set:
       POST {apiBaseUrl}/quotations        (save a quotation)
       POST {apiBaseUrl}/blog              (save a blog post)
       POST {apiBaseUrl}/upload            (multipart image upload; field: "file", "slot")
     Leave "" to run fully offline in the browser.                    */
  apiBaseUrl: "",

  /* Product catalogue used by the quotation & blog tools.
     slug must match the file name in /products/ and /assets/images/products/. */
  products: [
    { slug: "industrial-ro-water-treatment-plant",            name: "Industrial RO Water Treatment Plant" },
    { slug: "semi-automatic-pet-blowing-machine",             name: "Semi-Automatic PET Blowing Machine" },
    { slug: "hand-feed-automatic-pet-blowing-machine",        name: "Hand-Feed Automatic PET Blowing Machine" },
    { slug: "fully-automatic-pet-blowing-machine",            name: "Fully Automatic PET Blowing Machine" },
    { slug: "station-filler-bottle-filling-machine",          name: "Station Filler (Bottle Filling Machine)" },
    { slug: "fully-automatic-rinsing-filling-capping-machine", name: "Fully Automatic Rinsing, Filling & Capping Machine" },
    { slug: "automatic-sticker-labelling-machine",            name: "Automatic Sticker Labelling Machine" },
    { slug: "automatic-shrink-wrapping-machine",              name: "Automatic Shrink Wrapping Machine" },
    { slug: "batch-coding-machine",                           name: "Batch Coding Machine" }
  ],

  blogCategories: ["Business Guide", "Technical", "Buying Guide", "News"]
};
