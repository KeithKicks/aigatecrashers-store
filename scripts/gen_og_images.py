#!/usr/bin/env python3
"""Generate 1200x630 Open Graph images with headless Chromium.

  assets/og/site.png          site-wide card (home, store, blog)
  assets/og/<slug>.png        one per product page (title, kicker, price)

Reads each products/<slug>.html for its <h1>, price and cover kicker
(PROMPT PACK / AI TOOLKIT / AI SYSTEM from assets/covers/<slug>.svg).
No emoji are used on purpose: the render box has no color-emoji font.

USAGE:
    python3 scripts/gen_og_images.py            # all products + site
    python3 scripts/gen_og_images.py slug1 ...  # just these slugs

Chromium is found via $CHROME, then common install paths (Playwright's
headless shell preferred). PNGs are palette-compressed with node when
node_modules/upng-js is present (run `npm install` once).
"""
from __future__ import annotations
import glob, html, os, pathlib, re, shutil, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "og"

CANDIDATES = [os.environ.get("CHROME", ""), "google-chrome", "chromium", "chromium-browser",
              "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
QUANTIZE = ROOT / "scripts" / "og_quantize.js"


def find_chrome() -> str:
    for c in CANDIDATES:
        if not c:
            continue
        p = shutil.which(c) or (c if os.path.exists(c) else None)
        if p:
            return p
    # Playwright installs: the headless shell captures exactly --window-size.
    for pat in ("/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell",
                os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-*/chrome-linux/headless_shell"),
                "/opt/pw-browsers/chromium-*/chrome-linux/chrome",
                os.path.expanduser("~/.cache/ms-playwright/chromium-*/chrome-linux/chrome")):
        for p in sorted(glob.glob(pat)):
            return p
    sys.exit("Chromium not found. Set CHROME=/path/to/chrome")


TEMPLATE = """<!doctype html><html><head><meta charset="utf-8"><style>
  html,body{{margin:0;width:1200px;height:630px;overflow:hidden}}
  body{{font-family:Inter,'Liberation Sans','DejaVu Sans',Helvetica,Arial,sans-serif;color:#fff;
       background:radial-gradient(ellipse 70% 60% at 78% 35%, rgba(15,164,217,.35) 0%, transparent 65%),
                  linear-gradient(180deg,#0f1c3f 0%,#050c1f 100%)}}
  .stripe{{position:absolute;top:0;left:0;right:0;height:12px;background:linear-gradient(90deg,#4cc9f0,#0fa4d9)}}
  .brand{{position:absolute;top:56px;left:72px;font-size:26px;font-weight:900;letter-spacing:6px;color:#4cc9f0}}
  .kicker{{position:absolute;top:150px;left:72px;font-size:22px;font-weight:800;letter-spacing:6px;color:#0fa4d9}}
  .title{{position:absolute;top:196px;left:72px;width:760px;font-size:{size}px;line-height:1.08;font-weight:900;letter-spacing:-1.5px}}
  .price{{position:absolute;left:72px;bottom:84px;display:inline-block;padding:14px 34px;border-radius:999px;background:#0fa4d9;font-size:44px;font-weight:900}}
  .by{{position:absolute;left:72px;bottom:40px;font-size:20px;color:#c9d1e3}}
  .ring{{position:absolute;right:-80px;top:120px;width:420px;height:420px;border-radius:50%;border:6px solid #0fa4d9;background:rgba(255,255,255,.06)}}
  .ring2{{position:absolute;right:-56px;top:144px;width:372px;height:372px;border-radius:50%;border:2px solid rgba(76,201,240,.45)}}
  .mark{{position:absolute;right:96px;top:262px;font-size:120px;font-weight:900;color:#fff;letter-spacing:-6px}}
  .mark span{{color:#4cc9f0}}
</style></head><body>
  <div class="stripe"></div>
  <div class="brand">AI GATECRASHERS</div>
  <div class="ring"></div><div class="ring2"></div><div class="mark"><span>Ai</span>GC</div>
  <div class="kicker">{kicker}</div>
  <div class="title">{title}</div>
  {price}
  <div class="by">By Keith Allen Schuh · aigatecrashers.com</div>
</body></html>"""


def render(chrome: str, html_text: str, out: pathlib.Path) -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as fh:
        fh.write(html_text)
        src = fh.name
    try:
        subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=1", "--window-size=1200,630",
                        f"--screenshot={out}", f"file://{src}"],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90)
    finally:
        os.unlink(src)
    quantize(out)


def quantize(png: pathlib.Path) -> None:
    """Palette-compress the screenshot in place (needs `npm install` once)."""
    if not (ROOT / "node_modules" / "upng-js").exists() or not shutil.which("node"):
        if not getattr(quantize, "warned", False):
            print("  (node_modules missing: run `npm install` to shrink PNGs ~4x)")
            quantize.warned = True  # type: ignore[attr-defined]
        return
    tmp = png.with_suffix(".q.png")
    subprocess.run(["node", str(QUANTIZE), str(png), str(tmp), "256"], check=True, timeout=120)
    tmp.replace(png)


def product_meta(slug: str) -> tuple[str, str, str]:
    page = (ROOT / "products" / f"{slug}.html").read_text()
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", page, re.S).group(1)
    title = html.unescape(re.sub(r"<[^>]+>", "", h1)).strip()
    m = re.search(r'data-product-price="(\d+)"', page)
    price = m.group(1) if m else ""
    kicker = "PROMPT PACK"
    cover = ROOT / "assets" / "covers" / f"{slug}.svg"
    if cover.exists():
        k = re.search(r'fill="#0fa4d9">([A-Z &;]+)</text>', cover.read_text())
        if k:
            kicker = html.unescape(k.group(1))
    return title, price, kicker


def main(argv: list[str]) -> int:
    chrome = find_chrome()
    OUT.mkdir(parents=True, exist_ok=True)
    slugs = argv or sorted(p.stem for p in (ROOT / "products").glob("*.html"))
    if not argv:
        render(chrome, TEMPLATE.format(size=76, kicker="AI FOR HUMANS, NOT HYPE",
               title="Prompt packs, playbooks &amp; plain-English AI training for small business",
               price=""), OUT / "site.png")
        print("  site.png")
    for slug in slugs:
        title, price, kicker = product_meta(slug)
        size = 74 if len(title) <= 34 else 62 if len(title) <= 50 else 52
        price_html = f'<div class="price">${price}</div>' if price else ""
        render(chrome, TEMPLATE.format(size=size, kicker=html.escape(kicker), title=html.escape(title), price=price_html),
               OUT / f"{slug}.png")
        print(f"  {slug}.png")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
