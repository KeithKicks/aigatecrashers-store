#!/usr/bin/env python3
"""Build sitemap.xml from the HTML pages in this repo.

Includes: /, /store/, /blog/, every blog post and product page.
Excludes: thank-you.html (noindex), 404.html, partials/, anything with
<meta name="robots" content="noindex">.
lastmod = last git commit date for the file (falls back to today).

USAGE:  python3 scripts/gen_sitemap.py
"""
from __future__ import annotations
import datetime, pathlib, re, subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://aigatecrashers.com"
SKIP = {"thank-you.html", "404.html"}
PRIORITY = {"/": "1.0", "/store/": "0.9", "/blog/": "0.7"}


def url_for(p: pathlib.Path) -> str:
    rel = p.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def lastmod(p: pathlib.Path) -> str:
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", str(p)], cwd=ROOT,
                             capture_output=True, text=True, timeout=20).stdout.strip()
        if out:
            return out
    except Exception:
        pass
    return datetime.date.today().isoformat()


def main() -> None:
    entries = []
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT)
        if rel.parts[0] in {"partials", "scripts", "assets", ".git", "node_modules"} or p.name in SKIP:
            continue
        text = p.read_text(errors="replace")
        if re.search(r'<meta name="robots" content="[^"]*noindex', text):
            continue
        u = url_for(p)
        pri = PRIORITY.get(u, "0.8" if u.startswith("/products/") else "0.6")
        entries.append((u, lastmod(p), pri))
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, lm, pri in entries:
        xml.append(f"  <url><loc>{BASE}{u}</loc><lastmod>{lm}</lastmod><priority>{pri}</priority></url>")
    xml.append("</urlset>\n")
    (ROOT / "sitemap.xml").write_text("\n".join(xml))
    print(f"sitemap.xml: {len(entries)} URLs")


if __name__ == "__main__":
    main()
