#!/usr/bin/env python3
"""Sync nav header, footer, and Google Fonts link across every .html page.

Partials live in /partials/:
  - partials/header.html  →  replaces content between SHELL:HEADER sentinels
  - partials/footer.html  →  replaces content between SHELL:FOOTER sentinels

Google Fonts: replaces any existing Google Fonts <link> or inserts before </head>
with the canonical 3-family line (Inter + Instrument Serif + JetBrains Mono).

Pages that don't yet have sentinels: the script detects the existing
<header class="site-header"> ... </header> and <footer class="footer"> ... </footer>
blocks and wraps the new partial with sentinels, so a re-run becomes a pure
sentinel-to-sentinel swap.

Safe to re-run. Idempotent.

USAGE:
    python3 scripts/sync_shell.py                # dry-run summary
    python3 scripts/sync_shell.py --apply        # actually write changes
"""
from __future__ import annotations
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Directories to skip entirely.
SKIP_DIRS = {".git", ".claude", "deliverables", "scripts", "partials",
             "mockups", "node_modules", "email-sequences", "prompt-packs",
             "prompt-pack-deliverables", "assets", "css", "js"}

HEADER_PARTIAL = ROOT / "partials" / "header.html"
FOOTER_PARTIAL = ROOT / "partials" / "footer.html"

# Canonical Google Fonts line (must match the one in index.html <head>).
FONTS_LINK = (
    '<link href="https://fonts.googleapis.com/css2?'
    'family=Inter:wght@400;500;600;700;800&'
    'family=Instrument+Serif:ital@0;1&'
    'family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />'
)

HEADER_START = "<!-- SHELL:HEADER:START -->"
HEADER_END   = "<!-- SHELL:HEADER:END -->"
FOOTER_START = "<!-- SHELL:FOOTER:START -->"
FOOTER_END   = "<!-- SHELL:FOOTER:END -->"


def read_partial(path: pathlib.Path) -> str:
    if not path.exists():
        sys.exit(f"ERROR: Missing partial: {path}")
    return path.read_text().strip()


def iter_html_files() -> list[pathlib.Path]:
    out: list[pathlib.Path] = []
    for p in ROOT.rglob("*.html"):
        # Skip anything under a skipped directory
        rel = p.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        out.append(p)
    return out


# ---------- HEADER ----------

def replace_header(text: str, partial: str) -> str:
    """Swap or insert the SHELL:HEADER block."""
    wrapped = f"{HEADER_START}\n{partial}\n{HEADER_END}"

    # Case 1: sentinels already present — swap the body.
    re_sentineled = re.compile(
        re.escape(HEADER_START) + r".*?" + re.escape(HEADER_END),
        re.DOTALL,
    )
    if re_sentineled.search(text):
        return re_sentineled.sub(wrapped, text, count=1)

    # Case 2: existing <header class="site-header..."> ... </header>
    # (matches "site-header", "site-header sticky-header", etc.)
    re_old_header = re.compile(
        r'<header\s+class="site-header[^"]*">.*?</header>',
        re.DOTALL,
    )
    if re_old_header.search(text):
        return re_old_header.sub(wrapped, text, count=1)

    # Case 3: new-style <div class="nav-wrap">...</div> that isn't yet sentineled
    # (first top-level nav-wrap only — greedy-close after its matching </div>).
    # Conservative: require id="navWrap" so we don't grab a nested component.
    re_navwrap = re.compile(
        r'<div class="nav-wrap"[^>]*id="navWrap"[^>]*>.*?</div>\s*</div>\s*</div>',
        re.DOTALL,
    )
    if re_navwrap.search(text):
        return re_navwrap.sub(wrapped, text, count=1)

    return text  # no-op if no header found


# ---------- FOOTER ----------

def replace_footer(text: str, partial: str) -> str:
    wrapped = f"{FOOTER_START}\n{partial}\n{FOOTER_END}"

    re_sentineled = re.compile(
        re.escape(FOOTER_START) + r".*?" + re.escape(FOOTER_END),
        re.DOTALL,
    )
    if re_sentineled.search(text):
        return re_sentineled.sub(wrapped, text, count=1)

    # Legacy footer uses <footer class="footer">...</footer>.
    # Some pages may use <footer class="site-footer-v2"> (the new one) or
    # a bare <footer>. Try most specific first.
    for pattern in [
        r'<footer class="footer">.*?</footer>',
        r'<footer class="site-footer-v2">.*?</footer>',
        r'<footer[^>]*>.*?</footer>',
    ]:
        re_footer = re.compile(pattern, re.DOTALL)
        if re_footer.search(text):
            return re_footer.sub(wrapped, text, count=1)

    return text


# ---------- FONTS ----------

# Matches any existing Google Fonts <link ... fonts.googleapis.com/css2 ... />
# (handles both the old Inter-only link and any intermediate variants).
GFONTS_RE = re.compile(
    r'<link[^>]+fonts\.googleapis\.com/css2[^>]*/?>',
)

PRECONNECT_RE = re.compile(
    r'<link[^>]+preconnect[^>]+fonts\.(googleapis|gstatic)\.com[^>]*/?>'
)


def replace_fonts(text: str) -> str:
    """Ensure the canonical Google Fonts link is present. Keep preconnects."""
    if FONTS_LINK in text:
        return text  # already canonical

    # Replace the first Google Fonts link if one exists
    if GFONTS_RE.search(text):
        return GFONTS_RE.sub(FONTS_LINK, text, count=1)

    # Otherwise, insert before </head> with preconnects if missing
    preconnects = (
        '<link rel="preconnect" href="https://fonts.googleapis.com" />\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />\n'
    )
    inject = preconnects + FONTS_LINK + "\n"
    if PRECONNECT_RE.search(text):
        inject = FONTS_LINK + "\n"

    # Insert before </head>, preserving indentation of that line
    m = re.search(r'([ \t]*)</head>', text)
    if not m:
        return text
    indent = m.group(1)
    indented = "\n".join(indent + line if line else line for line in inject.splitlines()) + "\n"
    return text[:m.start()] + indented + text[m.start():]


# ---------- driver ----------

def process(path: pathlib.Path, header: str, footer: str) -> tuple[bool, list[str]]:
    original = path.read_text()
    text = original
    changed: list[str] = []

    new_text = replace_header(text, header)
    if new_text != text:
        changed.append("header")
        text = new_text

    new_text = replace_footer(text, footer)
    if new_text != text:
        changed.append("footer")
        text = new_text

    new_text = replace_fonts(text)
    if new_text != text:
        changed.append("fonts")
        text = new_text

    if text != original:
        return True, changed
    return False, []


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true",
                        help="Actually write changes (default: dry-run).")
    args = parser.parse_args()

    header = read_partial(HEADER_PARTIAL)
    footer = read_partial(FOOTER_PARTIAL)

    files = iter_html_files()
    print(f"Found {len(files)} HTML files. "
          f"{'APPLYING' if args.apply else 'DRY-RUN'}.\n")

    total_changes = 0
    for path in sorted(files):
        rel = path.relative_to(ROOT)
        original = path.read_text()
        will_change, changed = process(path, header, footer)
        if will_change:
            total_changes += 1
            tag = ",".join(changed)
            print(f"  [{tag:22s}]  {rel}")
            if args.apply:
                # Re-run process fresh and actually write
                # (process already applied in-memory; write the result)
                text = original
                text = replace_header(text, header)
                text = replace_footer(text, footer)
                text = replace_fonts(text)
                path.write_text(text)

    print(f"\n{total_changes}/{len(files)} files "
          f"{'updated' if args.apply else 'would be updated'}.")


if __name__ == "__main__":
    main()
