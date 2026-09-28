# Store audit (2026-09-28)

What was checked: every HTML page in this repo (66 pages), the JS and CSS, the
build scripts, the ClickFunnels workspace "AI Gatecrashers" (products, prices,
orders), and the open pull request from April.

## 1. What was actually broken

| # | Problem | Impact | Status |
|---|---------|--------|--------|
| 1 | **No product could be bought.** All 46 product pages had `data-checkout-url=""` or no attribute at all. The Checkout button showed an alert telling people to email support. No Stripe, Gumroad or ClickFunnels link existed anywhere in the repo. | Zero revenue from the static site | **Fixed.** Every Buy button now links to its ClickFunnels product (see section 3). |
| 2 | **Mobile menu did nothing.** The burger button had no JS and the dropdown had no CSS. | Phone visitors could not navigate | **Fixed** (same fix as PR #1, ported into nav.js and styles.css). |
| 3 | **Cart total never updated** on 30 product pages (markup used `js-cart-total`, JS looked for `cart-total-amount`). | Cart showed $0.00 | **Fixed** in store.js. |
| 4 | **Every social share image 404'd.** 46 product pages referenced `og-*.png` files that do not exist; blog, store and schema referenced `og-image.jpg` and `logo.png`, also missing. | Links shared on X, Facebook, LinkedIn, Slack, iMessage showed no preview | **Fixed.** 47 real 1200x630 PNGs generated into `assets/og/`, all references updated. |
| 5 | No `sitemap.xml`, `robots.txt`, `404.html` or favicon. | Slower indexing, no crawl hints, ugly 404s | **Fixed.** All four added. |
| 6 | Two store cards showed the wrong price: Copywriting Command Center ($17 on card, $27 on page and in ClickFunnels) and AI Megaprompt Vault ($27 vs $47). | Bait-and-switch feel, possible chargebacks | **Fixed** to match ClickFunnels. |
| 7 | Breadcrumbs on all 46 product pages (HTML and JSON-LD) linked to `/#products`, an anchor that no longer exists since products moved to `/store/`. | Broken breadcrumb rich results | **Fixed** to `/store/`. |
| 8 | Homepage linked to a blog post that does not exist (`ai-grant-writing-without-sounding-like-a-robot`). | Dead link on the homepage | **Fixed** to the real grant-writing guide. |
| 9 | Homepage "See SMB tools" and the three other use-case links pass `?filter=` to the store, and the WebSite schema advertises `/store/?q=`. store.js ignored both. | Dead links, invalid SearchAction | **Fixed.** `?filter=<section>` scrolls to that section, `?q=` pre-fills search. |
| 10 | 16 blog author bios link to `/about`, which does not exist. | Dead link on every post, weak E-E-A-T signal for AEO | **Not fixed.** Needs real content. See section 4. |
| 11 | Newsletter form is fake: it shows a success message and stores nothing. | "Get 50 free prompts" collects no leads | **Not fixed.** Needs a ClickFunnels form or workflow. See section 4. |
| 12 | Order bumps on product pages add an item with no checkout URL and no matching ClickFunnels product. | Bump revenue is silently dropped | **Not fixed.** Configure bumps inside ClickFunnels checkout instead. |

## 2. What ClickFunnels shows

* Workspace: **AI Gatecrashers** (`aigatecrashers.myclickfunnels.com`), 46 products created 2026-04-29 that match the 46 static pages one-to-one, plus older coaching and membership products.
* Prices in ClickFunnels match the product pages for all 46 (the only mismatches were the two store cards above).
* Orders: 40 orders on 2026-06-29 and 2026-07-06, **38 abandoned, 2 paid ($9 Viral Content Toolkit), 1 disputed**. Almost all came in within one day and every abandoned checkout is the same $9 product, which looks like bot or card-testing traffic rather than real buyers. The checkout also collects a full shipping address for a digital download, which hurts conversion on real traffic.

## 3. How checkout is wired now

`data/clickfunnels-products.json` is the single source of truth: slug, ClickFunnels product ID, variant ID, price and `cf_path`.

```
checkout_base + cf_path  ->  data-checkout-url on every Buy button
```

`python3 scripts/wire_checkout.py --apply` rewrites all 46 pages from that file (dry run without `--apply`). It also warns if a page price drifts from the ClickFunnels price.

**One thing to verify before merging:** `checkout_base` is set to `https://aigatecrashers.myclickfunnels.com/store/products`. The exact product URL format could not be confirmed from inside this session (the ClickFunnels domain is blocked here). Open any product in your ClickFunnels store, copy the URL, and if the part before the product path differs, change `checkout_base` in the JSON and re-run the script. If your store is on the custom domain, use that instead so buyers never see `myclickfunnels.com`.

## 4. Recommended next steps, in order

1. **Confirm the checkout URL format** (above) and merge this PR. Then merge or close PR #1 from April, which overlaps with the mobile-menu fix here. PR #1 also swaps the homepage product links to a single JavaScript product page (`/product/?id=...`). That is bad for SEO and AEO: one URL, no per-product title, description or schema for crawlers. Keep the static pages; drop that part of PR #1.
2. **Turn off the shipping address** on the ClickFunnels checkout for digital products, and enable ClickFunnels' abandoned-cart email.
3. **Create `/about`** (Keith's bio, credentials, photo, contact) and add `Person` schema. Every blog post already links to it; AI answer engines weigh author pages heavily.
4. **Wire the newsletter** form to a ClickFunnels form or a workflow that tags the contact and sends the 50 prompts. That is also the entry point for low-ticket upsell emails.
5. **Point the "Sign in" link** at the ClickFunnels customer center instead of `mailto:`.
6. **Move bumps into ClickFunnels.** Order bumps and one-click upsells belong on the checkout page. The static-site bumps should be removed or link to real products.
7. **Trim titles.** 51 pages have `<title>` tags over 70 characters, so Google truncates them. Meta descriptions over 165 characters on 14 pages have the same problem.
8. **Generation pipeline.** `scripts/gen_new_products.py` holds product copy inline. Move the product data into `data/` (next to the ClickFunnels map) so one file drives the page, the store card, the OG image, the sitemap and the checkout link. Until then, run these after adding a product:

```
python3 scripts/wire_checkout.py --apply   # after adding the product to data/clickfunnels-products.json
python3 scripts/gen_og_images.py <slug>    # needs Chromium; `npm install` once to shrink PNGs
python3 scripts/gen_sitemap.py
python3 scripts/sync_shell.py --apply
```

## 5. Open question: where is the site deployed?

This repo has no deploy config (no GitHub Pages branch, Netlify, Vercel or workflow). PR #1 adds an Apache `.htaccess`, so the site is probably uploaded to shared hosting by hand. Until that is confirmed, none of these fixes reach visitors just by merging. If it is Apache, add this line to `.htaccess` so the new 404 page is used:

```
ErrorDocument 404 /404.html
```
