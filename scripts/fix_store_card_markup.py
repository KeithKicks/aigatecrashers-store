#!/usr/bin/env python3
"""Fix broken store card markup caused by the earlier cover-injection script.

Each .product-card's .card-image div currently has:
  - Duplicate <span class="emoji"> (one pre-existing, one we left)
  - Duplicate <span class="card-badge"> when a badge exists
  - Missing closing </div> before .card-body
  - Emoji rendered ON TOP of the SVG cover (useless since cover shows the glyph)

After this script:
  - One <img> (the cover), one <span class="card-badge"> if applicable, nothing else
  - Properly closed </div> before .card-body
"""
from __future__ import annotations
import pathlib
import re

STORE = pathlib.Path(__file__).resolve().parent.parent / "store" / "index.html"


def main() -> int:
    t = STORE.read_text()

    # Pattern 1: cards WITH a badge (duplicate emoji + duplicate badge sandwich)
    # Matches:
    #   <div class="card-image CAT has-cover"><img ATTRS><span class="emoji">E</span>
    #       <span class="card-badge CLS">TXT</span><span class="emoji">E</span>
    #       <span class="card-badge CLS">TXT</span>
    #   <div class="card-body">
    pat_badge = re.compile(
        r'<div class="card-image ([\w ]*has-cover)"><img ([^>]+)>'
        r'<span class="emoji">[^<]+</span>\s*'
        r'<span class="card-badge (\w+)">([^<]+)</span>'
        r'<span class="emoji">[^<]+</span>\s*'
        r'<span class="card-badge \w+">[^<]+</span>\s*'
        r'<div class="card-body">',
        re.DOTALL,
    )

    def sub_badge(m: re.Match) -> str:
        cls = m.group(1)
        img_attrs = m.group(2)
        badge_cls = m.group(3)
        badge_txt = m.group(4)
        return (
            f'<div class="card-image {cls}">'
            f'<img {img_attrs}>'
            f'<span class="card-badge {badge_cls}">{badge_txt}</span>'
            f'</div>\n'
            f'          <div class="card-body">'
        )

    t, n_badge = pat_badge.subn(sub_badge, t)

    # Pattern 2: cards WITHOUT a badge (only duplicate emoji)
    pat_no_badge = re.compile(
        r'<div class="card-image ([\w ]*has-cover)"><img ([^>]+)>'
        r'<span class="emoji">[^<]+</span>'
        r'<span class="emoji">[^<]+</span>\s*'
        r'<div class="card-body">',
        re.DOTALL,
    )

    def sub_no_badge(m: re.Match) -> str:
        cls = m.group(1)
        img_attrs = m.group(2)
        return (
            f'<div class="card-image {cls}">'
            f'<img {img_attrs}>'
            f'</div>\n'
            f'          <div class="card-body">'
        )

    t, n_no_badge = pat_no_badge.subn(sub_no_badge, t)

    # Safety check: any remaining `<span class="emoji">` inside a card-image
    # that also has `has-cover`? Those would be lone leftovers.
    stragglers = len(
        re.findall(
            r'<div class="card-image [\w ]*has-cover"[^>]*>[^<]*<img[^>]+>[^<]*<span class="emoji">',
            t,
            re.DOTALL,
        )
    )

    STORE.write_text(t)
    print(f"Fixed cards with badge:    {n_badge}")
    print(f"Fixed cards without badge: {n_no_badge}")
    print(f"Total fixed:               {n_badge + n_no_badge}")
    print(f"Stragglers (emoji still inside has-cover): {stragglers}")
    return 0 if stragglers == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
