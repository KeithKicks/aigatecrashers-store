#!/usr/bin/env python3
"""Unify the navigation bar across all pages.

Canonical nav (used on every page):
  Start Here · Trainings · Store · Blog  +  Cart button  +  mobile-menu-toggle

Implementation:
- Homepage: replace `.hp-header` + related inline block with `.site-header` structure
  (same classes the rest of the site uses). Keeps the homepage's logo gradient.
- Product pages (products/*.html): rewrite `<nav class="main-nav">` links to the
  canonical set. Remove outdated `#products` / `#courses` hash targets that don't
  exist on the new homepage. Add cart button if missing.
- Blog pages (blog/*.html): same as product pages.

Safe to re-run.
"""
from __future__ import annotations
import pathlib
import re
from glob import glob

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Canonical nav items shared across every page
# href_prefix is relative (..) for pages in products/ or blog/; "" for homepage.
NAV_ITEMS = [
    ("Start Here", "{prefix}index.html#start-here"),
    ("Trainings", "{prefix}index.html#trainings"),
    ("Store",    "{prefix}store/"),
    ("Blog",     "{prefix}blog/"),
]


def canonical_main_nav(prefix: str) -> str:
    """Return the <nav class="main-nav"> block for product + blog pages."""
    links = "\n        ".join(
        f'<a href="{href.format(prefix=prefix)}">{label}</a>'
        for label, href in NAV_ITEMS
    )
    return f'<nav class="main-nav">\n        {links}\n      </nav>'


def canonical_mobile_nav(prefix: str) -> str:
    links = "\n      ".join(
        f'<a href="{href.format(prefix=prefix)}">{label}</a>'
        for label, href in NAV_ITEMS
    )
    return f'<nav class="mobile-nav js-mobile-nav">\n      {links}\n    </nav>'


# =======================================================================
# PRODUCT + BLOG PAGES
# =======================================================================

def patch_product_or_blog(path: pathlib.Path, prefix: str) -> bool:
    """Replace the existing <nav class="main-nav">...</nav> block and the
    mobile-nav block. Returns True if the file changed."""
    text = path.read_text()
    original = text

    # Match <nav class="main-nav"> ... </nav> (greedy close, but main-nav is only opened once per file)
    # Preserve the lead whitespace so surrounding indentation is unchanged.
    main_nav_re = re.compile(
        r'<nav class="main-nav">.*?</nav>',
        re.DOTALL,
    )
    text = main_nav_re.sub(canonical_main_nav(prefix), text, count=1)

    # Match <nav class="mobile-nav..."> ... </nav> (some pages use js-mobile-nav too)
    mobile_nav_re = re.compile(
        r'<nav class="mobile-nav[^"]*">.*?</nav>',
        re.DOTALL,
    )
    text = mobile_nav_re.sub(canonical_mobile_nav(prefix), text, count=1)

    if text != original:
        path.write_text(text)
        return True
    return False


# =======================================================================
# HOMEPAGE — rewrite the whole header block
# =======================================================================

HOMEPAGE_HEADER_HTML = '''  <!-- ===================== HEADER (shared .site-header) ===================== -->
  <header class="site-header">
    <div class="header-inner container">
      <a href="index.html" class="logo">AI Gatecrashers</a>
      <nav class="main-nav">
        <a href="#start-here">Start Here</a>
        <a href="#trainings">Trainings</a>
        <a href="store/">Store</a>
        <a href="blog/">Blog</a>
      </nav>
      <button class="cart-btn js-toggle-cart" aria-label="Open cart">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>
        Cart <span class="cart-count">0</span>
      </button>
      <button class="mobile-menu-toggle" aria-label="Toggle menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
    <nav class="mobile-nav js-mobile-nav">
      <a href="#start-here">Start Here</a>
      <a href="#trainings">Trainings</a>
      <a href="store/">Store</a>
      <a href="blog/">Blog</a>
    </nav>
  </header>'''


def patch_homepage(path: pathlib.Path) -> bool:
    text = path.read_text()
    original = text

    # 1) Replace the entire <header class="hp-header">...</header> block with canonical
    header_re = re.compile(
        r'  <!-- =====================\s*HEADER.*?===================== -->\s*'
        r'<header class="hp-header">.*?</header>',
        re.DOTALL,
    )
    text, n = header_re.subn(HOMEPAGE_HEADER_HTML, text, count=1)
    if n == 0:
        # Fallback — just match the header tag itself
        header_re2 = re.compile(r'<header class="hp-header">.*?</header>', re.DOTALL)
        text, n = header_re2.subn(HOMEPAGE_HEADER_HTML.lstrip(), text, count=1)
        if n == 0:
            print("  WARN: homepage header block not found (may already be patched)")

    # 2) Remove the inline .hp-header / .hp-logo / .hp-nav / .hp-hamburger / .hp-mobile-nav
    #    CSS blocks from the <style>. Leave any other .hp-* rules (hero, values, etc.) alone.
    hp_header_css_re = re.compile(
        r'    /\* Header \*/.*?@media \(max-width: 768px\) \{\s*\.hp-nav \{ display: none; \} \.hp-hamburger \{ display: flex; \}\s*\}\s*\n',
        re.DOTALL,
    )
    text, n_css = hp_header_css_re.subn('    /* Header styles live in css/styles.css (.site-header) */\n', text, count=1)

    if text != original:
        path.write_text(text)
        return True
    return False


# =======================================================================
# RUN
# =======================================================================

def main() -> int:
    total = 0

    # Homepage
    hp = ROOT / "index.html"
    if hp.exists():
        if patch_homepage(hp):
            print(f"✓ homepage: {hp.name}")
            total += 1

    # Product pages
    for f in sorted(glob(str(ROOT / "products" / "*.html"))):
        p = pathlib.Path(f)
        if patch_product_or_blog(p, "../"):
            print(f"✓ product:  {p.name}")
            total += 1

    # Blog pages (including blog index)
    for f in sorted(glob(str(ROOT / "blog" / "*.html"))):
        p = pathlib.Path(f)
        if patch_product_or_blog(p, "../"):
            print(f"✓ blog:     {p.name}")
            total += 1

    print(f"\nTotal pages patched: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
