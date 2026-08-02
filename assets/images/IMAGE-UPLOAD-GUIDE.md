# Image Upload Guide — Bharat iON Systems

Drop your images into the folders below using the **exact file names** listed.
The website picks them up automatically — no code changes needed. If a file is
missing, the site keeps using its built-in design (illustrations / text logo),
so nothing ever looks broken.

Accepted formats for every slot: **.jpg, .jpeg, .png, .webp** (logo & favicon
also accept **.svg**). Use the recommended name; only the folder + base name
matter, the extension can be any of the accepted ones.

---

## 1. Logo  →  `assets/images/logo/`
| File name | Used for | Recommended |
|-----------|----------|-------------|
| `logo.png` | Header (top-left) and footer logo | Transparent PNG, ~400×160 px (wide) or square. Shown ~48 px tall. |

When a logo is present the built-in text wordmark is hidden automatically.

## 2. Favicon  →  `assets/images/favicon/`
| File name | Used for | Recommended |
|-----------|----------|-------------|
| `favicon.png` | Browser tab icon | Square PNG, 512×512 px (or 32×32 / .ico). |

## 3. Backgrounds  →  `assets/images/banner/`
| File name | Used for | Recommended |
|-----------|----------|-------------|
| `hero-banner.jpg` | Home page hero background | Wide landscape photo, ~1920×1080 px. A dark blue overlay is applied automatically so the white headline stays readable. |
| `process-bg.jpg` | "The Complete Line" process section background | Wide landscape photo, ~1920×760 px. A dark blue overlay is applied automatically. |

## 4. Product photos  →  `assets/images/products/`
Use these exact base names (one photo per machine). They appear on the product
cards (home + Products page) and on each product detail page.

| File name | Machine |
|-----------|---------|
| `semi-automatic-pet-blowing-machine.jpg` | Semi-Automatic PET Blowing Machine |
| `hand-feed-automatic-pet-blowing-machine.jpg` | Hand-Feed Automatic PET Blowing Machine |
| `fully-automatic-pet-blowing-machine.jpg` | Fully Automatic PET Blowing Machine |
| `industrial-ro-water-treatment-plant.jpg` | Industrial RO Water Treatment Plant |
| `station-filler-bottle-filling-machine.jpg` | Station Filler (Bottle Filling Machine) |
| `fully-automatic-rinsing-filling-capping-machine.jpg` | Fully Automatic Rinsing, Filling & Capping Machine |
| `automatic-sticker-labelling-machine.jpg` | Automatic Sticker Labelling Machine |
| `automatic-shrink-wrapping-machine.jpg` | Automatic Shrink Wrapping Machine |
| `batch-coding-machine.jpg` | Batch Coding Machine |

Recommended: landscape photos around 800×600 px (4:3). They are cropped to fill
the card, so keep the machine centred.

---

### Notes
- **Demo images are already included** in every folder so you can see the layout
  immediately. To use your own, just overwrite each file with the **same file
  name** (any accepted extension works — the site auto-detects it).
- Paths are resolved relative to the site, so images work on the live domain,
  on GitHub Pages, and in local preview — regardless of which page they appear on.
- The logo and favicon are also picked up from the legacy `assets/` folder
  (`assets/logo.png`) if you happen to drop them there, but the folders above are
  the recommended location.
- After adding or replacing images, just refresh the page. If an image seems
  cached, do a hard refresh (Ctrl/Cmd + Shift + R).
- `.gitkeep` files only keep empty folders in git — you can ignore/leave them.
