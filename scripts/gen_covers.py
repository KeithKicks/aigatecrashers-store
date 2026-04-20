#!/usr/bin/env python3
"""Generate branded SVG cover art for every product on AI Gatecrashers.

Data source: parses store/index.html to extract the authoritative slug,
title, price, card category theme, emoji, and optional badge for each of
the 46 product cards. Emits one SVG per product into assets/covers/.

Design system:
- 1200x1500 SVG (book-proportional cover, works as product hero + og-image)
- Brand palette: cream #fefaf6, cyan #0fa4d9, bright cyan #4cc9f0, navy #0f1c3f, amber #f59e0b
- Two base treatments:
    LIGHT (cream bg)  -> used for $7-$17 prompt packs, kits (approachable)
    DARK  (navy bg)   -> used for $27+ bundles and courses (premium)
- Each cover gets a category-accent color applied to the emoji medallion +
  top stripe + price pill.

Run: python3 scripts/gen_covers.py
"""
from __future__ import annotations
import html
import pathlib
import re
import textwrap

ROOT = pathlib.Path(__file__).resolve().parent.parent
STORE = ROOT / "store" / "index.html"
OUT = ROOT / "assets" / "covers"


# ============================================================
# Brand palette
# ============================================================

CREAM = "#fefaf6"
CREAM_DEEP = "#fff1e0"
NAVY = "#0f1c3f"
NAVY_DEEP = "#050c1f"
CYAN = "#0fa4d9"
CYAN_BRIGHT = "#4cc9f0"
AMBER = "#f59e0b"
GREEN = "#16a34a"
PURPLE = "#7c3aed"
ORANGE = "#ff6b35"
WHITE = "#ffffff"
TEXT_BODY = "#3a4258"
TEXT_MUTED = "#6b7280"

# Category theme: (accent_color, secondary_accent)
THEMES = {
    "chatgpt":    (CYAN,   CYAN_BRIGHT),
    "midjourney": (PURPLE, "#a855f7"),
    "courses":    (GREEN,  "#22c55e"),
    "kits":       (ORANGE, AMBER),
    "bundles":    (AMBER,  CYAN_BRIGHT),
    "premium":    (CYAN,   AMBER),
}
DEFAULT_THEME = (CYAN, CYAN_BRIGHT)


# ============================================================
# Slug → relevant emoji for the medallion.
# Picked to reflect what each product actually is/does.
# ============================================================
SLUG_EMOJI = {
    # Funnels / copy / sales
    "1-page-funnel-copy-generator":   "🎯",
    "228-phrases-that-sell":          "💬",
    "copywriting-command-center":     "✍️",
    "chatgpt-prompts-sales-funnels":  "🔻",
    "chatgpt-prompts-b2b-sales":      "🤝",
    "stop-guessing-prompt-builder":   "🧩",

    # Money / hustles / monetization
    "300-ways-make-money-chatgpt":    "💰",
    "ai-side-hustle-starter-kit":     "🚀",
    "chatgpt-prompts-side-hustles":   "💡",
    "no-code-empire-prompts":         "🏗️",

    # Big kits / bundles / ladders
    "7-figure-ai-roadmap":            "🗺️",
    "ai-starter-pack":                "🎒",
    "ai-mega-collection":             "📚",
    "ai-megaprompt-vault":            "🗝️",
    "ultra-ai-builder-kit":           "🛠️",
    "chatgpt-secrets-bundle":         "🔐",
    "ai-marketing-os":                "⚙️",

    # Habit / productivity
    "75-hard-notion-tracker":         "🏋️",
    "chatgpt-prompts-productivity":   "⏱️",
    "chatgpt-prompts-act-as":         "🎭",

    # Niche / vertical
    "ai-for-coaches-and-therapists":  "💙",
    "ai-for-etsy-shopify-shops":      "🛍️",
    "ai-for-local-service-businesses":"🏪",
    "chatgpt-prompts-saas-tech":      "💻",
    "chatgpt-prompts-crypto":         "🪙",
    "chatgpt-prompts-ecommerce":      "🛒",
    "chatgpt-prompts-creators":       "🎨",
    "chatgpt-prompts-business":       "📊",
    "freelancer-ai-client-kit":       "💼",

    # Non-profit
    "nonprofit-ai-playbook":          "🫶",
    "nonprofit-communications-pack":  "✉️",
    "grant-writing-with-ai":          "📝",

    # Courses / trainings
    "chatgpt-accelerator-challenge":  "🏆",
    "mini-course-blueprint":          "🎓",

    # Marketing sub-niches
    "chatgpt-prompts-marketing":      "📣",
    "chatgpt-prompts-email-marketing":"📧",
    "chatgpt-prompts-social-media":   "📱",
    "chatgpt-prompts-seo":            "🔍",
    "marketing-sops-pack":            "📋",
    "solo-marketers-toolkit":         "🧰",
    "viral-content-toolkit":          "🔥",
    "content-repurposing-machine":    "♻️",

    # Midjourney / image
    "midjourney-prompts-cyberpunk":   "🌃",
    "midjourney-prompts-fantasy":     "🐉",
    "midjourney-prompts-photography": "📸",

    # Meta tools
    "ai-tool-directory":              "🧭",
}


# ============================================================
# Parse store/index.html for all product records
# ============================================================

def parse_store() -> list[dict]:
    """Extract product metadata from each .product-card anchor in store/index.html."""
    text = STORE.read_text()
    # Each card is an <a class="product-card">...</a>
    card_re = re.compile(
        r'<a href="\.\./products/([^"]+)\.html"\s+class="product-card"[^>]*data-price="(\d+)"[^>]*>'
        r'(?P<body>.*?)</a>',
        re.DOTALL,
    )
    cards = []
    for m in card_re.finditer(text):
        slug = m.group(1)
        price = int(m.group(2))
        body = m.group("body")
        # Card-image class (chatgpt|midjourney|courses|kits|bundles|premium)
        cat_m = re.search(r'<div class="card-image\s+([^"]+)"', body)
        category = cat_m.group(1).strip() if cat_m else "chatgpt"
        # Emoji
        # Emoji: prefer a curated slug-specific one (see SLUG_EMOJI map),
        # then fall back to whatever the legacy markup had, then to ⚡.
        emoji_m = re.search(r'<span class="emoji">([^<]+)</span>', body)
        legacy_emoji = emoji_m.group(1).strip() if emoji_m else ""
        emoji = SLUG_EMOJI.get(slug) or legacy_emoji or "⚡"
        # Title
        title_m = re.search(r'<h3 class="card-title">(.+?)</h3>', body, re.DOTALL)
        title = html.unescape(title_m.group(1).strip()) if title_m else slug.replace("-", " ").title()
        title = re.sub(r"\s+", " ", title)
        # Badge (optional)
        badge_m = re.search(r'<span class="card-badge\s+(\w+)">([^<]+)</span>', body)
        badge_text = badge_m.group(2).strip() if badge_m else ""
        badge_cls = badge_m.group(1).strip() if badge_m else ""

        cards.append({
            "slug": slug,
            "title": title,
            "price": price,
            "category": category,
            "emoji": emoji,
            "badge_text": badge_text,
            "badge_cls": badge_cls,
        })
    return cards


# ============================================================
# Text-wrapping helper (SVG has no word-wrap)
# ============================================================

def wrap_title(title: str, max_line_chars: int = 22) -> list[str]:
    """Wrap the product title into at most 3 lines that fit the cover width."""
    # Smart wrap: prefer breaking at natural boundaries like ":" and "—"
    # Split on those first, then word-wrap within each segment.
    lines: list[str] = []
    for seg in re.split(r'\s*[:—]\s*', title):
        wrapped = textwrap.wrap(seg, width=max_line_chars, break_long_words=False) or [""]
        lines.extend(wrapped)
    # Cap at 3 lines — if more, join the tail with an ellipsis
    if len(lines) > 3:
        lines = lines[:2] + [lines[2] + "…"]
    return lines


def category_kicker(category: str, price: int) -> str:
    """Short uppercase kicker shown above/below the title."""
    if category == "midjourney":
        return "MIDJOURNEY PROMPTS"
    if category == "courses":
        return "COURSE · PLAYBOOK"
    if category == "kits":
        return "KIT · TEMPLATES"
    if category == "bundles":
        return "BUNDLE · BEST VALUE"
    if category == "premium":
        return "PREMIUM COLLECTION"
    # chatgpt (default) — differentiate by price tier
    if price >= 47:
        return "AI SYSTEM"
    if price >= 17:
        return "AI TOOLKIT"
    return "PROMPT PACK"


# ============================================================
# Cover template
# ============================================================

FONT_STACK = "'Inter', system-ui, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"


def render_cover(p: dict) -> str:
    """Render one SVG cover string from a product record."""
    accent, accent2 = THEMES.get(p["category"], DEFAULT_THEME)
    price = p["price"]
    slug = p["slug"]

    # All covers use the dark treatment — unifies the store visual language
    # (prior behavior: `dark = price >= 27` split by tier, but it looked mixed).
    dark = True
    bg_top = NAVY if dark else CREAM
    bg_bot = NAVY_DEEP if dark else CREAM_DEEP
    heading_color = WHITE if dark else NAVY
    kicker_color = accent if dark else accent
    body_color = "#c9d1e3" if dark else TEXT_BODY
    medallion_fill = WHITE if dark else WHITE
    medallion_stroke = accent
    brand_color = accent2 if dark else NAVY

    # Title wrap (smaller lines for readability on 1200px wide)
    lines = wrap_title(p["title"], max_line_chars=20)
    title_lines_svg = []
    # We draw 1-3 lines centered around y=950-1100
    n = len(lines)
    line_h = 88
    start_y = 970 - (n - 1) * (line_h / 2)
    for i, line in enumerate(lines):
        y = start_y + i * line_h
        safe = html.escape(line)
        title_lines_svg.append(
            f'  <text x="600" y="{y:.0f}" font-family="{FONT_STACK}" '
            f'font-size="70" font-weight="900" letter-spacing="-1.5" '
            f'text-anchor="middle" fill="{heading_color}">{safe}</text>'
        )
    title_block = "\n".join(title_lines_svg)

    kicker = category_kicker(p["category"], price)
    badge_svg = ""
    if p["badge_text"]:
        badge_color = {
            "new": accent,
            "popular": PURPLE,
            "bestseller": GREEN,
            "value": AMBER,
        }.get(p["badge_cls"], accent)
        badge_svg = f'''
  <g>
    <rect x="960" y="52" width="180" height="48" rx="24" fill="{badge_color}"/>
    <text x="1050" y="84" font-family="{FONT_STACK}" font-size="20" font-weight="800"
          letter-spacing="3" text-anchor="middle" fill="{WHITE}">{html.escape(p["badge_text"].upper())}</text>
  </g>'''

    # Build SVG
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1500" role="img" aria-label="{html.escape(p["title"])} — AI Gatecrashers">
  <title>{html.escape(p["title"])}</title>
  <desc>AI Gatecrashers product cover — {html.escape(p["title"])}, ${price}</desc>
  <defs>
    <linearGradient id="bg-{slug}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{bg_top}"/>
      <stop offset="100%" stop-color="{bg_bot}"/>
    </linearGradient>
    <linearGradient id="medallion-{slug}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{accent2}"/>
      <stop offset="100%" stop-color="{accent}"/>
    </linearGradient>
    <radialGradient id="glow-{slug}" cx="50%" cy="40%" r="55%">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <!-- Background -->
  <rect width="1200" height="1500" fill="url(#bg-{slug})"/>
  <rect width="1200" height="1500" fill="url(#glow-{slug})"/>

  <!-- Top accent stripe -->
  <rect x="0" y="0" width="1200" height="10" fill="url(#medallion-{slug})"/>

  <!-- Brand wordmark -->
  <text x="60" y="78" font-family="{FONT_STACK}" font-size="28" font-weight="900"
        letter-spacing="6" fill="{brand_color}">AI GATECRASHERS</text>
{badge_svg}

  <!-- Emoji medallion -->
  <circle cx="600" cy="520" r="200" fill="{medallion_fill}" stroke="{medallion_stroke}" stroke-width="6"/>
  <circle cx="600" cy="520" r="180" fill="none" stroke="{accent2}" stroke-width="2" opacity="0.45"/>
  <text x="600" y="610" font-size="220" text-anchor="middle"
        style="font-family:'Apple Color Emoji','Segoe UI Emoji','Noto Color Emoji',sans-serif;">{html.escape(p["emoji"])}</text>

  <!-- Kicker (small uppercase above title) -->
  <text x="600" y="830" font-family="{FONT_STACK}" font-size="26" font-weight="800"
        letter-spacing="6" text-anchor="middle" fill="{kicker_color}">{html.escape(kicker)}</text>

  <!-- Title (1-3 lines) -->
{title_block}

  <!-- Subtitle line / price -->
  <g>
    <rect x="{600 - (60 if price >= 100 else (50 if price >= 10 else 40))}" y="1240"
          width="{120 if price >= 100 else (100 if price >= 10 else 80)}"
          height="96" rx="48" fill="{accent}"/>
    <text x="600" y="1306" font-family="{FONT_STACK}" font-size="56" font-weight="900"
          text-anchor="middle" fill="{WHITE}">${price}</text>
  </g>

  <!-- Byline -->
  <text x="600" y="1420" font-family="{FONT_STACK}" font-size="22" font-weight="500"
        text-anchor="middle" fill="{body_color}">By Keith Allen Schuh · aigatecrashers.com</text>
</svg>
'''
    return svg


# ============================================================
# Run
# ============================================================

def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    products = parse_store()
    print(f"Parsed {len(products)} products from store/index.html")
    if not products:
        print("No products found — aborting")
        return 1
    written = 0
    for p in products:
        path = OUT / f"{p['slug']}.svg"
        svg = render_cover(p)
        path.write_text(svg, encoding="utf-8")
        written += 1
    print(f"Wrote {written} covers to {OUT}")
    # Quick sample print
    sample = products[0]
    print(f"Sample: {sample['slug']}  cat={sample['category']}  price=${sample['price']}  emoji={sample['emoji']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
