#!/usr/bin/env python3
"""Remove em-dashes from blog HTML files using context-aware rules.

Rules applied in order:
1. Protect <pre>...</pre> and <code>...</code> blocks (em-dashes stay inside
   actual code/prompt examples).
2. Replace em-dashes (— and &mdash;) based on what follows:
   - "word — Capital"  -> "word. Capital"   (new sentence)
   - "word — lowercase" -> "word, lowercase" (comma)
   - "word—word"        -> "word, word"     (no-space form)
   - any remaining      -> ", "              (conservative fallback)
3. Restore code blocks.

Run: python3 scripts/de_em_dash.py [file_or_glob ...]
     or with no args to process all blog/*.html
"""
from __future__ import annotations
import pathlib
import re
import sys
from glob import glob

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_TARGETS = sorted(glob(str(ROOT / "blog" / "*.html")))

EM = "\u2014"  # U+2014 em dash


def protect_code_blocks(text: str) -> tuple[str, dict[str, str]]:
    """Replace <pre>...</pre> and <code>...</code> blocks with placeholders.
    Returns (new_text, placeholder_map).
    """
    placeholders: dict[str, str] = {}

    def save(match: re.Match) -> str:
        key = f"\x00CODE_{len(placeholders)}\x00"
        placeholders[key] = match.group(0)
        return key

    # Order matters: <pre> first (which may contain <code> inside)
    text = re.sub(r"<pre\b[^>]*>.*?</pre>", save, text, flags=re.DOTALL)
    text = re.sub(r"<code\b[^>]*>.*?</code>", save, text, flags=re.DOTALL)
    return text, placeholders


def restore_code_blocks(text: str, placeholders: dict[str, str]) -> str:
    for key, original in placeholders.items():
        text = text.replace(key, original)
    return text


def transform_em_dashes(text: str) -> tuple[str, int]:
    """Apply the em-dash swap rules. Returns (new_text, replacements_made)."""
    before = text.count(EM) + text.count("&mdash;")

    # Normalize &mdash; to actual em-dash for uniform processing, then back.
    text = text.replace("&mdash;", EM)

    # Rule A: "word [space] — [space] Capital letter" -> "word. Capital"
    # Keep any existing terminal punctuation (comma, etc.) before the em-dash
    # unchanged, but strip it if it's a trailing space only.
    # Example: "launch — Starting" -> "launch. Starting"
    def rule_a(m: re.Match) -> str:
        left = m.group(1).rstrip(" ,")
        # If left already ends with a sentence terminator, just use space
        if left and left[-1] in ".!?":
            return f"{left} {m.group(2)}"
        return f"{left}. {m.group(2)}"

    text = re.sub(r"([^\s—][^—]*?)\s*" + EM + r"\s*([A-Z])", rule_a, text)

    # Rule B: "word [space] — [space] lowercase" -> "word, lowercase"
    def rule_b(m: re.Match) -> str:
        left = m.group(1).rstrip(" ,")
        return f"{left}, {m.group(2)}"

    text = re.sub(r"([^\s—][^—]*?)\s*" + EM + r"\s*([a-z])", rule_b, text)

    # Rule C: "word—word" (no spaces) -> "word, word"
    text = re.sub(r"(\w)" + EM + r"(\w)", r"\1, \2", text)

    # Rule D: any remaining em-dash (surrounded by odd whitespace or at
    # start/end of a phrase) -> replace with comma-space to be safe.
    text = re.sub(r"\s*" + EM + r"\s*", ", ", text)

    # Final safety net: any stragglers get removed.
    text = text.replace(EM, "")

    after = text.count(EM) + text.count("&mdash;")
    return text, before - after


def process_file(path: pathlib.Path) -> tuple[int, int]:
    original = path.read_text()
    protected, codes = protect_code_blocks(original)
    swapped, removed = transform_em_dashes(protected)
    final = restore_code_blocks(swapped, codes)
    if final != original:
        path.write_text(final)
    # Verify: count em-dashes in FINAL (should be 0 in prose, possibly >0 inside code blocks)
    remaining_all = final.count(EM) + final.count("&mdash;")
    # Count em-dashes only OUTSIDE code blocks
    bare, _ = protect_code_blocks(final)
    remaining_prose = bare.count(EM) + bare.count("&mdash;")
    return removed, remaining_prose


def main() -> int:
    targets = [pathlib.Path(p) for p in (sys.argv[1:] or DEFAULT_TARGETS)]
    total_removed = 0
    total_remaining = 0
    for p in targets:
        if not p.exists():
            print(f"SKIP (missing): {p}")
            continue
        removed, remaining = process_file(p)
        total_removed += removed
        total_remaining += remaining
        print(f"{p.name:55s}  removed {removed:3d}   prose-remaining {remaining}")
    print(f"\nTotal removed: {total_removed}")
    print(f"Total still in prose: {total_remaining}  (all inside code blocks if >0)")
    return 0 if total_remaining == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
