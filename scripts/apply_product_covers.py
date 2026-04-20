#!/usr/bin/env python3
"""Inject the generated SVG cover into every product page hero using the
appropriate mockup frame (book / notion / device / flat) auto-assigned by
product type.

Safe to run multiple times: skips files that already contain `data-mockup=`.

Run: python3 scripts/apply_product_covers.py
"""
from __future__ import annotations
import pathlib
import re
from glob import glob

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Product-type → mockup mapping. Anything not listed defaults to "notion".
MOCKUP_BOOK = {
    "chatgpt-accelerator-challenge",
    "7-figure-ai-roadmap",
    "ai-mega-collection",
    "ultra-ai-builder-kit",
    "nonprofit-ai-playbook",
    "chatgpt-secrets-bundle",
    "mini-course-blueprint",
    "solo-marketers-toolkit",
    "freelancer-ai-client-kit",
    "ai-megaprompt-vault",
}
MOCKUP_DEVICE = {
    "stop-guessing-prompt-builder",
    "1-page-funnel-copy-generator",
    "ai-marketing-os",
    "content-repurposing-machine",
    "ai-tool-directory",
    "75-hard-notion-tracker",
    "copywriting-command-center",
    "no-code-empire-prompts",
    "viral-content-toolkit",
}
MOCKUP_FLAT = {
    "midjourney-prompts-fantasy",
    "midjourney-prompts-cyberpunk",
    "midjourney-prompts-photography",
}


def mockup_for(slug: str) -> str:
    if slug in MOCKUP_BOOK:
        return "book"
    if slug in MOCKUP_DEVICE:
        return "device"
    if slug in MOCKUP_FLAT:
        return "flat"
    return "notion"


def cover_block(slug: str, mockup: str, alt: str) -> str:
    # Book mockup needs the .cover-inner wrapper for the 3D transform
    if mockup == "book":
        inner = (
            f'<div class="cover-inner">'
            f'<img src="../assets/covers/{slug}.svg" alt="{alt}" loading="lazy">'
            f'</div>'
        )
    else:
        inner = f'<img src="../assets/covers/{slug}.svg" alt="{alt}" loading="lazy">'
    return (
        f'      <div class="product-cover" data-mockup="{mockup}">\n'
        f'        {inner}\n'
        f'      </div>\n'
    )


def patch_product(path: pathlib.Path) -> bool:
    text = path.read_text()
    slug = path.stem

    if 'data-mockup=' in text:
        return False  # already patched

    mockup = mockup_for(slug)
    alt = f"{slug.replace('-', ' ').title()} — AI Gatecrashers product cover"

    # Find the hero's inner container. Two patterns to match across templates:
    #   <div class="container product-hero-inner">
    # We want to add `with-cover` class to it AND append the cover block
    # just before the section's closing </section>.
    inner_open_re = re.compile(
        r'(<div class="container product-hero-inner"[^>]*>)'
    )
    m = inner_open_re.search(text)
    if not m:
        # Alternate: some pages use `<div class="container">` inside the hero.
        # Fall back to wrapping more loosely.
        hero_re = re.compile(r'(<section[^>]*class="[^"]*product-hero[^"]*"[^>]*>)')
        hm = hero_re.search(text)
        if not hm:
            return False
        # Can't safely inject without known container — skip and warn later
        print(f"  WARN: no product-hero-inner container in {path.name}")
        return False

    # 1) Add with-cover class to inner container
    old_open = m.group(1)
    new_open = old_open.replace(
        'class="container product-hero-inner"',
        'class="container product-hero-inner with-cover"',
    )

    # 2) Find the matching closing </section> for the hero
    # Search forward from the inner open
    section_close_pos = text.find('</section>', m.end())
    if section_close_pos == -1:
        return False

    # Find the inner container close: the </div> that closes `.container product-hero-inner`.
    # Simplest approach: find the LAST `    </div>` (4-space indent) before </section>.
    # But more reliable: regex for `</div>\s*</section>` and work backward.
    # Actually we'll insert the cover block right BEFORE the </section> is fine
    # structurally (inside .container), and let the CSS grid handle layout.

    # We'll insert the cover block before the last </div> that closes .container
    # which is the </div> at 4-space indent immediately before </section>.
    # Search backward from section_close_pos for `\n    </div>`
    last_div_re = re.compile(r"\n    </div>")
    matches = list(last_div_re.finditer(text, m.end(), section_close_pos))
    if not matches:
        return False
    # The LAST such </div> closes the .container. Insert cover before it.
    insert_pos = matches[-1].start() + 1  # after the leading \n

    cb = cover_block(slug, mockup, alt)

    # Also add a `has-cover` class on the hero's <section> for CSS hook
    section_open_re = re.compile(r'(<section[^>]*class=")([^"]*product-hero[^"]*)(")')
    sm = section_open_re.search(text)
    if sm and 'has-cover' not in sm.group(2):
        old_sec = sm.group(0)
        new_sec = f'{sm.group(1)}{sm.group(2)} has-cover{sm.group(3)}'
    else:
        old_sec = sm.group(0) if sm else None
        new_sec = old_sec

    # Apply all 3 edits in reverse-position order so indexes stay valid
    new_text = text
    # Edit 3 (latest in file): insert cover block before last </div>
    new_text = new_text[:insert_pos] + cb + new_text[insert_pos:]
    # Edit 2: swap container class
    new_text = new_text.replace(old_open, new_open, 1)
    # Edit 1: add has-cover to section (if changed)
    if old_sec and new_sec and old_sec != new_sec:
        new_text = new_text.replace(old_sec, new_sec, 1)

    path.write_text(new_text)
    return True


def main() -> int:
    pages = sorted(glob(str(ROOT / "products" / "*.html")))
    patched = 0
    skipped = 0
    by_mockup = {"book": 0, "notion": 0, "device": 0, "flat": 0}
    for f in pages:
        p = pathlib.Path(f)
        if patch_product(p):
            patched += 1
            by_mockup[mockup_for(p.stem)] += 1
        else:
            skipped += 1
    print(f"Patched: {patched}   Skipped (already patched / failed): {skipped}")
    print(f"  by mockup: {by_mockup}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
