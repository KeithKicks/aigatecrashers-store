# Midjourney Cover Art Brief Library — AI Gatecrashers

Use these when you're ready to upgrade the SVG v1 covers to premium v2 Midjourney art. Drop each generated PNG into `assets/covers/{slug}.png`. The site will automatically prefer the PNG if present (fallback to SVG).

**File naming rule:** PNG filenames must match the product slug exactly. Example: `chatgpt-prompts-business.png` for `chatgpt-prompts-business.html`.

**Dimensions:** Generate 2:3 portrait ratio (`--ar 2:3`). Upscale to the largest version, export as PNG. Target file size ≤ 500KB via squoosh.app or similar.

---

## Global brand rules (apply to every Midjourney generation)

- **Primary color:** brand cyan `#0fa4d9`
- **Secondary color:** brand navy `#0f1c3f`
- **Accent:** amber `#f59e0b` (use sparingly for warmth/pop)
- **Background:** warm cream `#fefaf6` for approachable products (≤$17) OR deep navy for premium ($27+)
- **Typography style:** bold condensed sans-serif when overlaying text. But generally **generate without text** and add it in post (Figma/Canva) because MJ typography is unreliable. If you want text baked in, use the `--style raw` flag.
- **Consistent feel:** editorial, confident, "premium-but-approachable" — think Stripe × Notion × Penguin Classics.
- **Avoid:** stock-photo clichés (handshakes, puzzle pieces, lightbulbs, gears), generic tech-bro AI imagery (glowing circuits, floating brains), over-saturated hero shots, anything that looks like clipart or "AI-generated."

---

## The 4 template prompts

Each template has a `[SUBJECT]` placeholder — plug in product-specific keywords from the table at the bottom.

### Template A — Book-style cover (for courses, bundles, roadmaps, playbooks)

**Use for:** chatgpt-accelerator-challenge, 7-figure-ai-roadmap, ai-mega-collection, ultra-ai-builder-kit, nonprofit-ai-playbook, chatgpt-secrets-bundle, mini-course-blueprint, solo-marketers-toolkit, freelancer-ai-client-kit, ai-megaprompt-vault

```
editorial book cover design, [SUBJECT], premium hardcover, bold condensed sans-serif typography, high-contrast composition, warm cream or deep navy background with cyan accent foil, subtle paper texture, clean minimalist layout, Penguin Classics meets modern tech branding, professional studio photography lighting, centered composition with generous negative space, title area at top third, visual motif at center, no clutter, --style raw --ar 2:3 --v 6
```

### Template B — Flat cover / kit box (for prompt packs, kits)

**Use for:** all "500 Prompts for X" packs, 228-phrases-that-sell, ai-starter-pack, grant-writing-with-ai, nonprofit-communications-pack, ai-for-local-service-businesses, ai-for-coaches-and-therapists, ai-for-etsy-shopify-shops, marketing-sops-pack, 75-hard-notion-tracker

```
flat graphic cover for a digital product, [SUBJECT], bold geometric shapes, confident sans-serif typography space, warm cream background #fefaf6 with brand cyan #0fa4d9 accent and navy #0f1c3f deep contrast, subtle paper grain, asymmetric editorial layout, hint of amber warmth in lower third, crisp vector aesthetic, premium SaaS brand feel, no photorealistic people, no clichéd tech imagery, generous negative space, --style raw --ar 2:3 --v 6
```

### Template C — Device / tool mockup (for interactive products, builders, directories)

**Use for:** stop-guessing-prompt-builder, 1-page-funnel-copy-generator, ai-marketing-os, content-repurposing-machine, ai-tool-directory, copywriting-command-center, no-code-empire-prompts, viral-content-toolkit

```
clean device mockup composition, [SUBJECT] shown on a modern laptop or tablet screen, softbox studio lighting, warm cream desk surface, hint of navy shadow, brand cyan accent element (notebook, cup, sticker), minimalist product photography style, shallow depth of field, editorial tech magazine aesthetic (Monocle meets Apple), no people, no clichéd AI imagery, generous negative space above the device for title overlay, --style raw --ar 2:3 --v 6
```

### Template D — Image / creative cover (for Midjourney prompt packs)

**Use for:** midjourney-prompts-fantasy, midjourney-prompts-cyberpunk, midjourney-prompts-photography

```
gallery-quality [SUBJECT] sample image that showcases the style the prompt pack produces, museum-print composition, rich color grading, dramatic lighting, editorial magazine cover feel, one dominant subject with cinematic framing, premium art-book aesthetic, --style raw --ar 2:3 --v 6
```

For this category, the cover IS the art — let the Midjourney output speak for itself. Post-production: thin frame, brand wordmark in corner.

---

## Per-product `[SUBJECT]` lines

Copy the right template above, replace `[SUBJECT]` with the line below that matches the product. Then generate.

### ChatGPT Prompt Packs (Template B)

| Slug | `[SUBJECT]` replacement |
|---|---|
| chatgpt-prompts-business | a stylized compass or strategy chart motif, business growth ascending, confident and grounded |
| chatgpt-prompts-marketing | megaphone or signal-wave graphic, upward growth, audience ripple effect |
| chatgpt-prompts-creators | open notebook with floating content blocks, flowing lines, creative ideation |
| chatgpt-prompts-productivity | stacked task cards cascading into focus, clean geometry, organized energy |
| chatgpt-prompts-side-hustles | rising sun over a small shop, entrepreneurial, hopeful, not hypey |
| chatgpt-prompts-email-marketing | stylized envelope with cyan glow, sent-message motif, marketing-ops feel |
| chatgpt-prompts-sales-funnels | abstract funnel shape with descending gradients, conversion-focused, analytical |
| chatgpt-prompts-social-media | clustered chat bubbles in brand colors, social energy, connected |
| chatgpt-prompts-ecommerce | shopping cart silhouette with rising trend graph, commerce motif |
| chatgpt-prompts-saas-tech | modular grid with interlocking blocks, SaaS dashboard abstraction |
| chatgpt-prompts-b2b-sales | handshake abstracted into geometric shapes, pipeline motif |
| chatgpt-prompts-seo | stylized search magnifier with upward arrow, organic-ranking motif |
| chatgpt-prompts-crypto | abstract blockchain nodes, subtle gold/navy contrast (NOT bitcoin hype imagery) |
| chatgpt-prompts-act-as | theatrical mask motif, role-play, character voices, editorial |

### New Products (Template B unless noted)

| Slug | `[SUBJECT]` replacement |
|---|---|
| ai-starter-pack | compass rose, first-steps journey, welcome mat, approachable onboarding |
| 228-phrases-that-sell | speech-bubble typography cluster, bold words floating, copywriting energy |
| 1-page-funnel-copy-generator (Template C) | single-page scroll unrolling on a laptop screen, sales page preview, blue-cyan accents |
| 300-ways-make-money-chatgpt | stylized ledger with stacked income streams, diverse, anti-hype |
| 75-hard-notion-tracker (Template C) | tablet showing a Notion habit tracker, pen beside, morning light, discipline aesthetic |
| viral-content-toolkit (Template C) | laptop screen showing viral content editor, hook-generator UI, cyan notification badges |
| ai-tool-directory (Template C) | tablet showing searchable AI tool directory, clean rows of cards, brand cyan accents |
| grant-writing-with-ai | stack of paper grant applications bound with ribbon, cyan highlight marker, warm office desk |
| nonprofit-communications-pack | folded thank-you letter and envelope tied with ribbon, community-feel, mission-led warmth |
| ai-for-local-service-businesses | toolbox silhouette with cyan accent tag, blue-collar honest craftsmanship |
| ai-for-coaches-and-therapists | two simple chairs facing each other, warm room, confidential, professional |
| ai-for-etsy-shopify-shops | packed craft shipping boxes stacked neatly, artisan maker energy, cream-and-cyan |
| ai-marketing-os (Template C) | operating system dashboard on a laptop, marketing metrics, clean cyan UI |
| content-repurposing-machine (Template C) | one blog post exploding into 12 derivative formats on a laptop screen, content atoms |
| stop-guessing-prompt-builder (Template C) | laptop screen showing a single text input and a generated prompt below, elegantly simple |

### Courses / Bundles (Template A — book-style)

| Slug | `[SUBJECT]` replacement |
|---|---|
| chatgpt-accelerator-challenge | stopwatch + sprint motif, 10-day challenge energy, confident navy + cyan |
| 7-figure-ai-roadmap | stylized roadmap/path with milestone markers, business horizon, ambitious |
| ai-mega-collection | treasure-trove vault motif (not gaudy), curated-collection aesthetic, cream-navy |
| ultra-ai-builder-kit | industrial builder's kit with AI elements, craftsman meets futurist |
| nonprofit-ai-playbook | field manual aesthetic, mission-led, warm cream with cyan foil |
| chatgpt-secrets-bundle | stack of sealed reports, editorial investigative feel, Monocle magazine vibe |
| mini-course-blueprint | architectural blueprint of a course structure, scaffold motif |
| solo-marketers-toolkit | marketer's toolbox with three pack spines visible, kit-box feel |
| freelancer-ai-client-kit | briefcase opened showing contract, pen, phone — deal-closer energy |
| ai-megaprompt-vault | vault door opening to reveal light, curated premium feel |
| copywriting-command-center (Template C alternative) | command center workstation, multiple screens showing copy, focused operator |
| no-code-empire-prompts (Template C alternative) | building blocks assembling into an app on screen, modular, empowering |

### Midjourney Packs (Template D — the cover IS the art)

| Slug | `[SUBJECT]` replacement |
|---|---|
| midjourney-prompts-fantasy | a single dramatic fantasy hero portrait or epic landscape, museum-quality, no text overlay |
| midjourney-prompts-cyberpunk | a neon-soaked cyberpunk cityscape at night, rich color grading, signature style shot |
| midjourney-prompts-photography | a photorealistic editorial portrait or landscape, National Geographic cover-quality |

---

## Post-production checklist

After Midjourney generation:

1. **Add title overlay in Figma/Canva** using Inter font (same as site). Match the SVG v1 layout: wordmark top-left, title center-bottom, price pill below.
2. **Consistency check:** all 46 covers should feel like siblings, not 46 one-offs. If one looks wildly off, regenerate.
3. **Export PNG** at 1200×1800 (2:3 ratio at web-HD resolution). Compress to ≤ 400KB via squoosh.app.
4. **Save to:** `assets/covers/{slug}.png` (exact slug match).
5. **Deploy:** your standard rsync — my deploy commands already include `assets/covers/`.
6. **HTML update:** none needed. Product pages reference `../assets/covers/{slug}.svg`. If you want the PNG to take over, either:
   - Rename the SVG to `.svg.backup` and upload the PNG as `{slug}.svg` (hacky but works), OR
   - Run a script to swap the extension in all product pages: `find products -name '*.html' | xargs sed -i '' 's|covers/\(.*\)\.svg|covers/\1.png|g'` (only do this once you have PNGs for ALL 46 — don't mix).

Want an auto-prefer-PNG swap script? Say the word and I'll write it.

---

## Workflow recommendation

Generate in batches of 4-6 products at a time. The first batch sets the visual tone — nail that before scaling. Categories in order of impact:

1. **Batch 1 (4 covers):** the top revenue products — 7-figure-roadmap, ai-mega-collection, chatgpt-accelerator-challenge, ai-starter-pack. These get the most views.
2. **Batch 2 (6 covers):** non-profit set — grant-writing, nonprofit-comms, nonprofit-playbook, ai-for-nonprofits blog thumb — plus 2 high-volume prompt packs.
3. **Batch 3 (remaining $17+ products):** vertical kits (coaches, contractors, etsy) + premium tools.
4. **Batch 4 (remaining $7-$12 prompt packs):** in bulk, using Template B.

Total Midjourney budget for 46 covers at ~5 generations each + 1-2 upscales: roughly 300-500 MJ generations, 4-6 hours of focused work.

---

## Want me to pre-write full MJ prompts (not just `[SUBJECT]`) for the top 10?

If it'd save you time, ping me and I'll generate the full Midjourney paste-ready prompt for each of those 10 — so you just copy, paste, and hit generate. 10 takes about 15 minutes of my time.
