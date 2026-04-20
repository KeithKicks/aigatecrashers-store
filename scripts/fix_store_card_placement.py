#!/usr/bin/env python3
"""One-shot fix: move product cards that were injected outside the .product-grid
container back inside their respective grids.

The prior injection script inserted cards after `</div>` of the grid
instead of before it, breaking the 3-column CSS grid layout.
"""
from __future__ import annotations
import pathlib
import re

STORE = pathlib.Path(__file__).resolve().parent.parent / "store" / "index.html"

# The 4 sections that received injected cards (and are therefore broken)
SECTIONS = ["get-customers", "run-business", "content", "bundles"]


def fix_section(text: str, section: str) -> tuple[str, int]:
    """Find orphan <a class="product-card"> blocks that sit between the grid
    close `</div>` and the container close, and re-insert them just before
    the grid close.

    Returns (new_text, number_of_cards_moved).
    """
    # Match the grid-open line
    grid_open_re = re.compile(
        r'(<div class="product-grid" data-category-grid="' + re.escape(section) + r'">)'
    )
    m = grid_open_re.search(text)
    if not m:
        return text, 0

    # Walk forward from the grid-open, looking for the FIRST `      </div>` at
    # 6-space outer indent that closes the grid. That close is followed by
    # (in the broken state) 0+ orphan product-card anchors, then the container
    # close `\n    </div><!-- /.container -->` or similar.
    start = m.end()
    # The grid body consists of `        <a class="product-card" ...>...</a>`
    # blocks indented at 8 spaces. The grid-close `</div>` is at 6 spaces.
    # Pattern: newline + exactly 6 spaces + `</div>`
    grid_close_re = re.compile(r"\n      </div>")
    close_m = grid_close_re.search(text, start)
    if not close_m:
        return text, 0
    grid_close_pos = close_m.start()
    grid_close_end = close_m.end()  # points to char AFTER `</div>`

    # Now capture orphan product cards after the grid close.
    # Orphan pattern: one-or-more `\n        <a href="../products/...` blocks
    # followed by a closing `</a>` at 8-space indent.
    # A safer approach: greedy-match from grid_close_end to the NEXT `\n    </div>`
    # (4 spaces — the .container close), then extract all `<a class="product-card"`
    # anchors inside that span.
    container_close_re = re.compile(r"\n    </div>")
    container_close_m = container_close_re.search(text, grid_close_end)
    if not container_close_m:
        return text, 0
    span_start = grid_close_end
    span_end = container_close_m.start()
    orphan_span = text[span_start:span_end]

    # Extract all product-card anchors from the orphan span.
    anchor_re = re.compile(
        r"\n?\s*<a href=\"\.\./products/[^\"]+\" class=\"product-card\"[\s\S]*?</a>",
        re.MULTILINE,
    )
    orphans = anchor_re.findall(orphan_span)
    if not orphans:
        return text, 0

    # Normalize each orphan to the canonical 8-space indentation used inside grids.
    # Strip leading newlines/whitespace, then prepend a single newline + 8-space indent.
    normalized = []
    for o in orphans:
        stripped = o.lstrip("\n").lstrip()  # drop any existing leading whitespace
        normalized.append("\n        " + stripped)
    cards_block = "".join(normalized) + "\n"

    # Build the new text:
    # 1) Everything up to (but not including) the grid close `</div>` (preserving the
    #    `\n      ` prefix), plus the cards block, plus the original grid-close line,
    #    plus the original text AFTER the grid close MINUS the orphan anchors.
    before_grid_close = text[:grid_close_pos]
    # The grid_close match started at the `\n` — we want to keep one blank line
    # of breathing room before the inserted cards? No — product cards in the grid
    # already live at 8-space indent directly after each other with no blank
    # line. So: insert the cards just before the grid-close's `\n      </div>`.
    after_grid_close_including_it = text[grid_close_pos:grid_close_end]
    after_close = text[grid_close_end:]

    # Remove the orphan anchors from `after_close` (only inside the span we measured)
    # Since span_start == grid_close_end, we operate on after_close.
    span_in_after = after_close[: span_end - grid_close_end]
    remainder = after_close[span_end - grid_close_end:]
    span_cleaned = anchor_re.sub("", span_in_after)
    # Collapse any triple newlines left behind by removal
    span_cleaned = re.sub(r"\n{3,}", "\n\n", span_cleaned)

    new_text = (
        before_grid_close
        + cards_block
        + after_grid_close_including_it
        + span_cleaned
        + remainder
    )
    return new_text, len(orphans)


def main() -> int:
    text = STORE.read_text()
    total = 0
    for section in SECTIONS:
        text, moved = fix_section(text, section)
        print(f"section #{section}: moved {moved} card(s) inside the grid")
        total += moved

    # Verify: no more orphan anchors immediately after a grid close
    orphan_check = re.findall(
        r"</div>\s*\n\s*<a[^>]*class=\"product-card\"", text
    )
    print(f"\norphan anchors after fix: {len(orphan_check)}")

    STORE.write_text(text)
    print(f"wrote store/index.html ({total} cards relocated)")
    return 0 if len(orphan_check) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
