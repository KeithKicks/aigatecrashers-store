#!/usr/bin/env python3
"""Wire every product page's Buy button to its ClickFunnels checkout URL.

Source of truth: data/clickfunnels-products.json
  checkout_base + cf_path  ->  data-checkout-url on every .js-add-to-cart
  button whose data-product-id belongs to that page.

Also checks that the page's data-product-price matches the ClickFunnels
price and prints a warning if not (it does not change prices).

Safe to re-run. Idempotent.

USAGE:
    python3 scripts/wire_checkout.py            # dry-run
    python3 scripts/wire_checkout.py --apply    # write changes
"""
from __future__ import annotations
import argparse, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "clickfunnels-products.json"

BTN_RE = re.compile(r'<button\b[^>]*\bjs-add-to-cart\b[^>]*>', re.S)


def set_attr(tag: str, name: str, value: str) -> str:
    attr_re = re.compile(r'\s' + re.escape(name) + r'="[^"]*"')
    if attr_re.search(tag):
        return attr_re.sub(f' {name}="{value}"', tag, count=1)
    # insert before the closing '>' of the opening tag
    return tag[:-1].rstrip() + f'\n            {name}="{value}"' + '>' if '\n' in tag else tag[:-1] + f' {name}="{value}">'


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    cfg = json.loads(DATA.read_text())
    base = cfg["checkout_base"].rstrip("/")
    changed = 0
    for p in cfg["products"]:
        page = ROOT / "products" / f'{p["slug"]}.html'
        if not page.exists():
            print(f"  MISSING PAGE  {page.name}")
            continue
        url = base + p["cf_path"]
        text = page.read_text()
        prices = set(re.findall(r'data-product-price="([^"]+)"', text))
        if prices and str(p["price"]) not in prices:
            print(f"  PRICE WARNING {page.name}: page {prices} vs ClickFunnels ${p['price']}")

        def repl(m: re.Match) -> str:
            return set_attr(m.group(0), "data-checkout-url", url)

        new = BTN_RE.sub(repl, text)
        if new != text:
            changed += 1
            n = len(BTN_RE.findall(text))
            print(f"  [{n} buttons] {page.name} -> {url}")
            if args.apply:
                page.write_text(new)
    print(f"\n{changed} pages {'updated' if args.apply else 'would be updated'}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
