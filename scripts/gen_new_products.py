#!/usr/bin/env python3
"""Generate 12 new AI Gatecrashers product pages from a single template.
Each page gets: warm/cyan palette via css/styles.css, full SEO schema
(Product, Offer, BreadcrumbList, FAQPage), a persona grid, outcomes list,
FAQ accordion, order-bump slot, and a right-rail purchase box.

Run:  python3 scripts/gen_new_products.py
Outputs into /Users/keithkicks/aigatecrashers-store/products/
"""
from __future__ import annotations
import html
import json
import pathlib
import sys
from dataclasses import dataclass, field

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "products"
CACHE_VER = "2026-04-20"


@dataclass
class Product:
    slug: str
    title: str                # Short display name (for <h1>, cards)
    seo_title: str            # Full <title> tag incl. brand suffix
    meta_desc: str
    price: int
    hero_tagline: str
    category: str             # card theme: chatgpt / kits / courses / bundles / premium
    data_tags: str            # outcome tags (comma separated for store filter)
    badge: str = ""           # New | Popular | Best Seller | Best Value | "" (none)
    emoji: str = "⚡"
    whats_inside: list[str] = field(default_factory=list)
    personas: list[dict] = field(default_factory=list)  # {emoji, title, desc}
    outcomes: list[str] = field(default_factory=list)
    faqs: list[dict] = field(default_factory=list)      # {q, a}
    includes: list[str] = field(default_factory=list)   # right-rail bullets
    bump_id: str = ""
    bump_name: str = ""
    bump_desc: str = ""
    bump_price: int = 0


# ============================================================
# THE 12 NEW PRODUCTS
# ============================================================

PRODUCTS: list[Product] = [
    # --- Theme 1: Easy Wins (repackage) ---
    Product(
        slug="ai-starter-pack",
        title="The AI Starter Pack for Small Business",
        seo_title="AI Starter Pack for Small Business — 50 Beginner Prompts + Quick-Start | AI Gatecrashers",
        meta_desc="The no-jargon starter pack for small business owners new to AI. 50 copy-paste prompts, a 1-page quick-start, and a 7-day plan. Instant download — $9.",
        price=9,
        hero_tagline="New to AI? Start here. Fifty copy-paste prompts, a 1-page quick-start, and a 7-day plan to get real work done this week.",
        category="kits",
        data_tags="run-business,get-customers,content",
        badge="New",
        emoji="🧭",
        whats_inside=[
            "50 beginner-friendly AI prompts organized by daily task — emails, descriptions, research, planning",
            "A 1-page quick-start that takes you from zero to your first useful AI output in 15 minutes",
            "7-day 'Use this first' plan that builds AI into one workflow per day",
            "The 10 mistakes beginners make (and how to skip them)",
            "Plain-English glossary — 'temperature,' 'context window,' 'hallucination' — translated",
            "Works with ChatGPT, Claude, or Gemini (free tiers included)",
            "Notion page with everything in one place, plus PDF backup",
        ],
        personas=[
            {"emoji":"🛒","title":"First-time AI users","desc":"You've opened ChatGPT or Claude once, got overwhelmed, and closed it. This pack assumes nothing."},
            {"emoji":"🏪","title":"SMB owners","desc":"You run a shop, service, or solo practice. You don't have time to 'learn AI.' You have time to save 4 hours this week."},
            {"emoji":"🤝","title":"Non-profit staff","desc":"Small budget, big mission. Use AI on grants, newsletters, and donor thank-yous without writing from scratch."},
        ],
        outcomes=[
            "Write your next 10 emails in half the time",
            "Draft a one-page overview of anything in under 5 minutes",
            "Get unstuck on tasks you've been avoiding for weeks",
            "Build a small prompt library you actually use",
        ],
        faqs=[
            {"q":"I've never used AI before — is this really beginner-friendly?","a":"Yes. This is literally the starter pack. It assumes you haven't used ChatGPT or Claude before. If you can send an email, you can use these prompts."},
            {"q":"Do I need a paid AI subscription?","a":"No. The free tier of ChatGPT, Claude, or Gemini handles everything in this pack. A paid plan gives you more capacity, but you don't need one to see real results."},
            {"q":"Is this the same as the free 50 prompts from the newsletter?","a":"It's an expanded, paid edition. The free version is 50 raw prompts. This paid version adds the quick-start, the 7-day plan, the beginner mistakes guide, and the glossary — the full 'start here' kit."},
            {"q":"What format does it come in?","a":"You'll get access to a Notion page (read-only, clone-it-to-your-workspace) plus a PDF backup. No software to install."},
            {"q":"Refund?","a":"7-day no-questions refund. Email Support@aigatecrashers.com and we'll refund within 24 hours."},
        ],
        includes=[
            "50 beginner AI prompts (ChatGPT, Claude, or Gemini)",
            "1-page quick-start guide",
            "7-day workflow plan",
            "Delivered as Notion page + PDF",
            "7-day money-back guarantee",
        ],
        bump_id="bump-prompt-builder",
        bump_name="The Stop Guessing Prompt Builder",
        bump_desc="A master prompt that writes better prompts for you. Type what you want, get a working AI prompt back (works in ChatGPT, Claude, or Gemini).",
        bump_price=3,
    ),

    Product(
        slug="solo-marketers-toolkit",
        title="The Solo Marketer's Toolkit",
        seo_title="The Solo Marketer's Toolkit — Marketing, Social & Email Prompts Bundle | AI Gatecrashers",
        meta_desc="Everything a 1-person marketing team needs. 1,500+ prompts for marketing, social, and email — pre-bundled. Instant download — $27.",
        price=27,
        hero_tagline="Everything a one-person marketing team needs. Marketing, social, and email prompts — pre-bundled so you stop cobbling.",
        category="bundles",
        data_tags="get-customers,content",
        badge="Popular",
        emoji="🎯",
        whats_inside=[
            "500 ChatGPT Prompts for Marketing & Growth — the full pack",
            "500 ChatGPT Prompts for Social Media — the full pack",
            "500 ChatGPT Prompts for Email Marketing — the full pack",
            "Cross-pack index: when to use which prompt (organized by campaign type)",
            "5 sample multi-step workflows (e.g., 'Product launch in one day')",
            "Delivered as a single Notion page with all three packs + the index",
        ],
        personas=[
            {"emoji":"💼","title":"Solo marketers","desc":"You're the entire marketing team at a 2-20 person company. You need depth in every channel without hiring."},
            {"emoji":"🎨","title":"Founder-marketers","desc":"You built the product, now you have to sell it. This gives you the messaging, social, and email engine in one."},
            {"emoji":"📣","title":"Freelance marketers","desc":"You bounce between client niches. One bundle that covers every marketing motion you'll need to deliver."},
        ],
        outcomes=[
            "Run a full product launch with a clear day-by-day content plan",
            "Stop re-writing the same email welcome flow for every client",
            "Generate a month of social content in one sitting",
            "Quote higher on marketing projects because you deliver faster",
        ],
        faqs=[
            {"q":"Can I just buy these separately?","a":"Yes — each pack is $7 individually ($21 total if you buy them one at a time). The bundle is $27 but includes the cross-pack index and workflows, which aren't sold elsewhere."},
            {"q":"Are these the same prompts as the individual packs?","a":"Identical core content, plus the bundle-only workflow index and multi-step campaign guides."},
            {"q":"Do I need a paid AI subscription?","a":"No. Works on free tiers of ChatGPT, Claude, or Gemini. Paid plans give you more capacity, not better output for these prompts."},
            {"q":"Is there a refund policy?","a":"7-day no-questions refund. If the bundle doesn't save you 3+ hours in your first week, email Support@aigatecrashers.com."},
            {"q":"Can I use these for client work?","a":"Yes. Unlimited-use license for your own projects and client deliverables."},
        ],
        includes=[
            "1,500+ marketing prompts in one Notion page",
            "Cross-pack workflow index",
            "5 multi-step campaign guides",
            "Works with all major AI tools",
            "7-day money-back guarantee",
        ],
        bump_id="bump-228-phrases",
        bump_name="228 Phrases That Sell",
        bump_desc="Scroll-stopping power phrases to drop into any headline, ad, or CTA. Pairs perfectly with the marketing packs.",
        bump_price=5,
    ),

    Product(
        slug="freelancer-ai-client-kit",
        title="The Freelancer's AI Client Kit",
        seo_title="The Freelancer's AI Client Kit — Win Clients, Deliver Faster | AI Gatecrashers",
        meta_desc="For freelancers using AI to win more clients and deliver faster. Business + copywriting prompts + 228 phrases that sell. Instant download — $27.",
        price=27,
        hero_tagline="Win more clients. Deliver faster. Quote higher. The AI kit for freelancers who are done doing everything twice.",
        category="bundles",
        data_tags="side-business,get-customers",
        badge="New",
        emoji="💼",
        whats_inside=[
            "500 ChatGPT Prompts for Business — proposals, scopes, pricing, client comms",
            "228 Phrases That Sell — for headlines, landing pages, and cold outreach",
            "Copywriting essentials extracted from the Copywriting Command Center",
            "Client-discovery call prompts (ask better questions, close faster)",
            "Proposal templates in 3 formats (hourly, fixed-price, retainer)",
            "Scope-creep scripts (what to say when a client asks for free work)",
        ],
        personas=[
            {"emoji":"✍️","title":"Freelance writers","desc":"You want to double your output without doubling your hours. AI handles the first 70%; you polish the last 30%."},
            {"emoji":"🎨","title":"Designers & marketers","desc":"Your client brief is always thin. These prompts turn vague input into sharp creative direction."},
            {"emoji":"💬","title":"Consultants","desc":"You charge for thinking, not typing. Use AI for the typing so you get the thinking done faster."},
        ],
        outcomes=[
            "Write a $3K proposal in 30 minutes instead of 3 hours",
            "Respond to cold inquiries with templates that close",
            "Stop staring at blank docs on client deliverables",
            "Raise your hourly rate because you deliver in half the time",
        ],
        faqs=[
            {"q":"Will this replace my voice?","a":"No — and we don't want it to. These are prompts, not outputs. You still drive the point of view and edit the final copy. The prompts just get you to 'decent draft' faster so you can spend time on the parts that matter."},
            {"q":"Are these industry-specific?","a":"They're written for general freelance/consulting work — writing, design, marketing, strategy. Not specialized legal, medical, or financial work."},
            {"q":"I already own the Business prompts. Worth upgrading?","a":"If you already own one of the three packs included, email Support@aigatecrashers.com for a $7 credit toward the kit."},
            {"q":"Do I need a paid AI subscription?","a":"No. Free tiers of ChatGPT, Claude, or Gemini all handle this."},
            {"q":"Refund?","a":"7-day no-questions. Email Support@aigatecrashers.com."},
        ],
        includes=[
            "3 full prompt libraries in one pack",
            "Proposal templates + scope-creep scripts",
            "Delivered as Notion + PDF",
            "Unlimited client-work license",
            "7-day money-back guarantee",
        ],
        bump_id="bump-funnel-copy",
        bump_name="1-Page Funnel Copy Generator",
        bump_desc="One prompt → a complete sales page for your freelance service. Pairs with the client kit.",
        bump_price=7,
    ),

    # --- Theme 2: Non-Profit On-Ramp ---
    Product(
        slug="grant-writing-with-ai",
        title="Grant Writing with AI: 80 Prompts + Templates",
        seo_title="Grant Writing with AI — 80 Prompts + 3 Templates for Non-Profits | AI Gatecrashers",
        meta_desc="Draft grants 3x faster. 80 prompts for LOIs, case statements, budget narratives, and impact reports, plus 3 fillable templates. $17.",
        price=17,
        hero_tagline="Draft grant applications three times faster. Eighty prompts plus three fillable templates — built for non-profit teams of 1 to 10.",
        category="kits",
        data_tags="run-business,get-customers",
        badge="New",
        emoji="📝",
        whats_inside=[
            "20 prompts for Letters of Inquiry (LOIs) — first contact with funders",
            "25 prompts for case statements + need narratives",
            "15 prompts for program descriptions and theory-of-change",
            "10 prompts for budget narratives (the part most EDs dread)",
            "10 prompts for impact reports and post-award follow-up",
            "3 fillable grant templates: LOI, mid-size foundation grant, federal format",
        ],
        personas=[
            {"emoji":"🎯","title":"Executive Directors","desc":"You're running the org and writing grants at midnight. Cut draft time in half so you can sleep and still ship."},
            {"emoji":"📋","title":"Development coordinators","desc":"You write 15-30 grants a year across funders with different voices. These prompts speed up the first draft so you can spend time on the nuance."},
            {"emoji":"🙋","title":"Volunteer grant writers","desc":"You agreed to help a small org with a grant and immediately regretted it. Start here instead of staring at a blank doc."},
        ],
        outcomes=[
            "Turn a program outline into a 3-paragraph LOI in 20 minutes",
            "Translate your impact data into funder-ready narrative",
            "Customize one case statement for five different foundations without rewriting from scratch",
            "Write a budget narrative that funders actually read",
        ],
        faqs=[
            {"q":"Is this just generic AI output? Funders can tell.","a":"The prompts are built to pull YOUR program specifics into the draft — they force you to input your own data, story, and theory-of-change. The AI structures it; your org's actual story is still the content. No generic output."},
            {"q":"Does this work for federal grants?","a":"Yes for the narrative sections. Federal grants have strict formatting we can't automate (SF-424 etc.), but the written sections — problem statement, methodology, eval plan — are covered. Template 3 is a federal-format skeleton."},
            {"q":"Can I use this for client work (I'm a grant consultant)?","a":"Yes — unlimited client-work license."},
            {"q":"What AI tool do I need?","a":"Free ChatGPT, Claude, or Gemini all work. Claude tends to write more naturally for grant narrative — worth trying both."},
            {"q":"Refund?","a":"7-day no-questions. Email Support@aigatecrashers.com."},
        ],
        includes=[
            "80 grant-writing prompts in Notion",
            "3 fillable grant templates",
            "LOI quick-start guide",
            "Unlimited client-work license",
            "7-day money-back guarantee",
        ],
        bump_id="bump-nonprofit-comms",
        bump_name="Non-Profit Communications Pack",
        bump_desc="Donor thank-yous, volunteer recruitment, board reports. The pack every grant writer also needs.",
        bump_price=9,
    ),

    Product(
        slug="nonprofit-communications-pack",
        title="The Non-Profit Communications Pack",
        seo_title="Non-Profit Communications Pack — Donor, Volunteer & Board Templates | AI Gatecrashers",
        meta_desc="Donor thank-yous, volunteer recruitment, newsletters, board reports. 60+ templates for non-profits of 1–10 people. Instant download — $17.",
        price=17,
        hero_tagline="The templates every small non-profit team wishes they had. Donor thank-yous, volunteer recruitment, board reports, newsletters — all ready to adapt.",
        category="kits",
        data_tags="get-customers,run-business",
        badge="New",
        emoji="💌",
        whats_inside=[
            "8 donor thank-you templates — graduated by gift size ($25 → $25K+)",
            "12 volunteer recruitment posts for Facebook, LinkedIn, and Nextdoor",
            "6 volunteer onboarding email sequences",
            "10 newsletter frameworks (monthly, quarterly, campaign, annual)",
            "8 board-report templates with KPI placeholders",
            "5 post-event recap templates (for donors, volunteers, and board)",
            "10 social captions for gratitude, milestones, and asks",
        ],
        personas=[
            {"emoji":"💌","title":"Development staff","desc":"Write in your org's voice without burning 3 hours on each donor letter."},
            {"emoji":"🙋","title":"Volunteer coordinators","desc":"Recruitment, onboarding, and retention content — drafted in minutes, not days."},
            {"emoji":"📊","title":"Executive Directors","desc":"Board reports and recaps that read as well as your org does good work."},
        ],
        outcomes=[
            "Personalize 50 donor thank-yous in the time it used to take to write 5",
            "Fill your next volunteer shift without calling a favor",
            "Write a board report that the board actually reads",
            "Turn one event into 3 weeks of grateful, on-brand social posts",
        ],
        faqs=[
            {"q":"Will the templates sound generic?","a":"They pull in your org's name, mission phrase, and program details as variables. The templates structure the message; the personality comes from what you put in."},
            {"q":"Do these work for faith-based / arts / advocacy orgs?","a":"Yes — the voice is neutral by default with guidance on how to adapt tone for different org types. Tested across direct-service, arts, advocacy, and religious orgs."},
            {"q":"Do I need any specific CRM?","a":"No. These work in any CRM, email platform, or Google Docs. No integrations required."},
            {"q":"Can I customize them once and reuse?","a":"Yes. The templates are designed to be customized once per template, then reused with small per-person variables."},
            {"q":"Refund?","a":"7-day no-questions. Email Support@aigatecrashers.com."},
        ],
        includes=[
            "60+ non-profit communications templates",
            "Donor, volunteer, board, and event content",
            "Notion + Google Docs formats",
            "Unlimited-use license for your org and clients",
            "7-day money-back guarantee",
        ],
        bump_id="bump-grants",
        bump_name="Grant Writing with AI",
        bump_desc="80 prompts + 3 templates for grant applications. Pairs with the communications pack.",
        bump_price=9,
    ),

    Product(
        slug="nonprofit-ai-playbook",
        title="AI for Mission-Led Orgs: The Full Playbook",
        seo_title="AI for Mission-Led Orgs — The Full Non-Profit Playbook | AI Gatecrashers",
        meta_desc="The complete AI playbook for non-profits of 1–10 staff. Grant writing + communications + 30-day rollout plan. Instant download — $47.",
        price=47,
        hero_tagline="The full AI playbook for non-profits running lean. Grant writing, donor communications, board reporting, and a 30-day team rollout plan — one bundle, one price.",
        category="courses",
        data_tags="run-business,get-customers",
        badge="Best Value",
        emoji="🎯",
        whats_inside=[
            "Grant Writing with AI — 80 prompts + 3 templates (normally $17)",
            "Non-Profit Communications Pack — 60+ templates (normally $17)",
            "30-Day Rollout Plan — week-by-week guide to onboarding your team",
            "ED Quick-Start — the 3 workflows that save the most time, ranked",
            "Volunteer AI Onboarding — a 2-page doc you can hand to any volunteer",
            "Board FAQ — answers the 5 questions your board will ask about AI",
            "Data & Privacy 1-pager — what to put in AI and what to keep out",
        ],
        personas=[
            {"emoji":"🎯","title":"Executive Directors","desc":"You're the strategist, fundraiser, and comms team. This is the full kit so you can hand pieces to staff and volunteers."},
            {"emoji":"📋","title":"Operations managers","desc":"You run everything that isn't programs. Standardize the internal comms that eat 8 hours a week."},
            {"emoji":"🤝","title":"Board chairs & advisors","desc":"You're asked 'how can we use AI?' — this is the answer you hand to the ED."},
        ],
        outcomes=[
            "Ship your next grant draft 3x faster than the last one",
            "Run a 30-day team rollout without derailing current work",
            "Answer board questions about AI with a clear, conservative playbook",
            "Save 8–12 hours a week across your team, starting week 2",
        ],
        faqs=[
            {"q":"How is this different from just buying the two smaller packs?","a":"The two smaller packs are $34 together. This is $47 and adds the 30-day rollout plan, ED quick-start, volunteer onboarding, board FAQ, and data-privacy doc. The rollout plan alone is what most EDs need most — the packs are useless if nobody uses them."},
            {"q":"We're 2 people. Too much?","a":"No. The 30-day plan is designed to scale down. A 2-person team finishes it in 10-14 days by skipping the delegation steps."},
            {"q":"We have privacy concerns about putting donor data in AI tools.","a":"Good. The Data & Privacy 1-pager covers exactly what to input and what to keep out. The short answer: never input PII, SSNs, or full donor records — only program specifics and drafting content."},
            {"q":"Refund?","a":"7-day no-questions. Email Support@aigatecrashers.com with your order number."},
            {"q":"Is there a team license?","a":"The license is per-org, unlimited staff. Hand it to volunteers, board members, contractors — it's covered."},
        ],
        includes=[
            "Full Grant Writing kit + Communications Pack",
            "30-day team rollout plan",
            "Board FAQ + Data & Privacy 1-pager",
            "Org-wide unlimited-use license",
            "7-day money-back guarantee",
        ],
        bump_id="bump-sops",
        bump_name="55 Digital Marketing SOPs",
        bump_desc="Plug-and-play marketing SOPs. Many non-profits use these for donor and member campaigns.",
        bump_price=12,
    ),

    # --- Theme 3: SMB Vertical Kits ---
    Product(
        slug="ai-for-local-service-businesses",
        title="AI for Local Service Businesses",
        seo_title="AI for Local Service Businesses — Plumbers, Electricians, Cleaners | AI Gatecrashers",
        meta_desc="AI prompt kit for plumbers, electricians, contractors, and cleaners. Quotes, reviews, Google Business, and nurture emails. $17.",
        price=17,
        hero_tagline="Built for the trades. Quote faster, respond to reviews like a pro, and keep your calendar full — without hiring a marketer.",
        category="kits",
        data_tags="get-customers,run-business",
        badge="New",
        emoji="🔧",
        whats_inside=[
            "Quote-writing prompts — 15 variants for common job types",
            "Review-response templates — 20 formats (good, bad, and silent reviews)",
            "Google Business Profile copy — headlines, service descriptions, updates",
            "Seasonal promo prompts — 12 templates for busy and slow seasons",
            "10 customer-nurture email flows (after-service, winterization, referrals)",
            "Facebook post templates that don't look like Facebook posts",
            "Text-message templates for appointment reminders and follow-ups",
        ],
        personas=[
            {"emoji":"🔧","title":"Trades & home-service owners","desc":"Plumber, electrician, HVAC, roofer, cleaner. You built a business; you did not sign up to write 40 marketing emails a year."},
            {"emoji":"📍","title":"Local contractors","desc":"Landscapers, painters, handymen. Google Business + reviews drive your pipeline. This makes both easier."},
            {"emoji":"🚚","title":"Mobile service businesses","desc":"Mobile detailers, groomers, tutors. You need systems that work from a truck or phone."},
        ],
        outcomes=[
            "Send a quote an hour after the site visit, not three days later",
            "Respond to every Google review in 10 minutes (not days)",
            "Fill your slow season with a nurture email that actually works",
            "Stop dreading the 'write a Facebook post' task",
        ],
        faqs=[
            {"q":"Will this actually help a 1-truck operation?","a":"That's who it's built for. 1–5 person shops who do good work but lose leads because their follow-up is manual and slow."},
            {"q":"I don't have time to learn a new tool.","a":"You don't need one. Every prompt works in free ChatGPT or Claude. If you can copy-paste a text message, you can use this."},
            {"q":"Do the review-response templates work for bad reviews?","a":"Yes — there are 8 variants specifically for bad/unfair reviews, written to de-escalate and protect your rating."},
            {"q":"Is this different from the general business prompt pack?","a":"Yes. This is 100% trades-and-service focused. General pack is broad. This one uses the actual language your customers use."},
            {"q":"Refund?","a":"7-day no-questions. Email Support@aigatecrashers.com."},
        ],
        includes=[
            "Quote + review + GBP + promo templates",
            "10 customer nurture email flows",
            "SMS and social post templates",
            "Notion + plain-text formats (works on any phone)",
            "7-day money-back guarantee",
        ],
        bump_id="bump-marketing-sops",
        bump_name="55 Digital Marketing SOPs",
        bump_desc="Plug-and-play SOPs for email, social, ads. Scales anything in the local-service kit.",
        bump_price=10,
    ),

    Product(
        slug="ai-for-coaches-and-therapists",
        title="AI for Coaches & Therapists",
        seo_title="AI for Coaches & Therapists — Session Notes, Intake, Marketing | AI Gatecrashers",
        meta_desc="AI prompt kit for coaches and therapists. Intake forms, session notes, liability-safe marketing copy, and newsletter prompts. $17.",
        price=17,
        hero_tagline="For coaches and therapists building a sustainable practice. Intake, notes, and marketing copy — plus a liability-safe language library.",
        category="kits",
        data_tags="run-business,get-customers",
        badge="New",
        emoji="🧠",
        whats_inside=[
            "Intake form prompts — 10 variants by specialty (life, exec, mental-health adjacent, career)",
            "Session-note structure prompts — SOAP-style, narrative, and goal-tracking formats",
            "Marketing copy prompts — website bio, service descriptions, booking page",
            "Content ideas — 30 newsletter and social post prompts for ongoing audience-building",
            "Liability-safe language library — how to describe services without overclaiming",
            "Client email templates — onboarding, rescheduling, boundaries, and closeouts",
            "Testimonial-request prompts that get you real testimonials without being weird",
        ],
        personas=[
            {"emoji":"🧠","title":"Life & career coaches","desc":"You coach 1-on-1 and want more clients without 6 hours a week on content."},
            {"emoji":"💬","title":"Therapists in private practice","desc":"You need language that's warm, accurate, and legally careful. This handles all three."},
            {"emoji":"📈","title":"Executive coaches","desc":"You charge premium rates. Your marketing should sound like it. These prompts get you there."},
        ],
        outcomes=[
            "Build a full intake form for a new specialty in 30 minutes",
            "Cut session-note time in half without losing clinical detail",
            "Write a website that doesn't sound like every other coach's",
            "Publish a newsletter monthly without dreading it",
        ],
        faqs=[
            {"q":"Is this HIPAA-safe?","a":"The prompts themselves are HIPAA-neutral — you never put PHI into them. The kit includes a 1-pager on what to input and what to never input. For full HIPAA-compliant session notes, use a BAA-covered AI tool (not free ChatGPT). We tell you which tools have BAAs."},
            {"q":"Does this work for therapists who don't take insurance?","a":"Especially. Cash-pay practices need marketing more than insurance-only practices. Most of the kit is marketing-focused."},
            {"q":"Can I customize the session-note templates?","a":"Yes. The prompts build the skeleton; you always edit. Never paste AI-generated notes without review."},
            {"q":"Is there a license for group practices?","a":"Yes — the license is per-practice, unlimited staff. Pass it to associates."},
            {"q":"Refund?","a":"7-day no-questions. Email Support@aigatecrashers.com."},
        ],
        includes=[
            "Intake, notes, marketing, and email templates",
            "Liability-safe language library",
            "Notion + Google Docs formats",
            "Per-practice unlimited-use license",
            "7-day money-back guarantee",
        ],
        bump_id="bump-228-phrases",
        bump_name="228 Phrases That Sell",
        bump_desc="Power phrases for your website, booking page, and social. Pairs with the practice kit.",
        bump_price=5,
    ),

    Product(
        slug="ai-for-etsy-shopify-shops",
        title="AI for Etsy & Shopify Shop Owners",
        seo_title="AI for Etsy & Shopify Shop Owners — Listings, Ads, Customer Service | AI Gatecrashers",
        meta_desc="AI prompt kit for Etsy and Shopify shop owners. Listings, tags, ad copy, and customer-service templates. $17.",
        price=17,
        hero_tagline="Built for shop owners juggling listings, customer service, and marketing solo. Listings that rank, emails that convert, replies that save time.",
        category="kits",
        data_tags="get-customers,side-business",
        badge="New",
        emoji="🛍️",
        whats_inside=[
            "Listing-copy prompts — titles, descriptions, and bullet points for 15+ product categories",
            "Tag optimization prompts — Etsy SEO tags by seasonality and niche",
            "10 customer-service reply templates (refunds, shipping delays, custom orders)",
            "12 email-flow templates (welcome, abandon cart, post-purchase, win-back)",
            "Ad copy templates — 8 formats for Etsy ads, Pinterest, and Meta",
            "Brand voice worksheet — lock in your shop's tone so AI outputs stay on-brand",
            "Seasonal content calendar — 12 months of prompts for holidays and sales events",
        ],
        personas=[
            {"emoji":"🛍️","title":"Etsy shop owners","desc":"You know your craft. You don't know SEO or funnels. This fills the gap."},
            {"emoji":"🛒","title":"Solo Shopify operators","desc":"You're listing products at 10pm. Cut the writing time without cutting quality."},
            {"emoji":"🎁","title":"Print-on-demand sellers","desc":"You have 200+ listings and no time to write each one. Scale with templates."},
        ],
        outcomes=[
            "Write a full Etsy listing in 10 minutes instead of 40",
            "Respond to customer DMs without losing tone or patience",
            "Launch a new product with a 4-email flow ready from day one",
            "Build a year of seasonal content without the weekly scramble",
        ],
        faqs=[
            {"q":"I already own the e-commerce prompt pack. Is this redundant?","a":"Overlapping but not identical. This is Etsy/Shopify-specific with platform-native formats (Etsy tags, Shopify product descriptions). The general pack is broader but not platform-tuned."},
            {"q":"Does it work for print-on-demand?","a":"Yes — especially. Scaling POD requires templated listing copy. This kit is built for that."},
            {"q":"Will AI-generated listings get penalized by Etsy?","a":"Etsy's policy is about spam and keyword stuffing, not AI per se. These prompts produce natural-language listings, not keyword lists."},
            {"q":"Do I need a paid AI subscription?","a":"No. Free ChatGPT, Claude, or Gemini all work."},
            {"q":"Refund?","a":"7-day no-questions."},
        ],
        includes=[
            "Listing + tag + ad copy + email templates",
            "Brand voice worksheet",
            "12-month seasonal calendar",
            "Works for Etsy, Shopify, and POD",
            "7-day money-back guarantee",
        ],
        bump_id="bump-viral",
        bump_name="Viral Content Toolkit",
        bump_desc="Hook templates and multi-platform adapters. Perfect for shop marketing outside your storefront.",
        bump_price=7,
    ),

    # --- Theme 4: Price-Gap Fillers ($37–$47) ---
    Product(
        slug="ai-marketing-os",
        title="The AI Marketing OS",
        seo_title="The AI Marketing OS — Notion System + SOPs + Walkthrough | AI Gatecrashers",
        meta_desc="A marketing operating system in Notion: SOPs, prompts, workflows, and a 20-min walkthrough. For small teams running marketing on a shoestring. $37.",
        price=37,
        hero_tagline="A marketing operating system you can actually run. Notion database, 10 linked SOPs, prompt workflows, and a 20-minute walkthrough to set it up this week.",
        category="premium",
        data_tags="get-customers,run-business",
        badge="New",
        emoji="⚙️",
        whats_inside=[
            "A linked Notion database: campaigns, content, channels, and metrics in one view",
            "10 SOPs (email campaigns, social cadence, paid ads, SEO audits, launches)",
            "Prompt-chain workflows for each SOP (how to use AI at each step)",
            "A 20-minute walkthrough video where Keith sets up the system end-to-end",
            "Templates for weekly marketing stand-ups and monthly reviews",
            "A 'first 7 days' setup checklist so you're running it in a week, not a month",
        ],
        personas=[
            {"emoji":"💼","title":"Solo marketers in small cos","desc":"You need a system, not more tools. This is the system."},
            {"emoji":"🎯","title":"Agency owners","desc":"Standardize how you run client marketing. White-label the SOPs; keep the system."},
            {"emoji":"🧑‍💻","title":"Founders doing their own marketing","desc":"You've got product-market fit-ish. Now you need to market it without hiring 3 people."},
        ],
        outcomes=[
            "Run every marketing channel from one Notion view",
            "Onboard a new team member to your marketing in 2 hours",
            "Stop losing track of which campaign is running where",
            "Run a full launch (email + social + paid) with one system instead of five docs",
        ],
        faqs=[
            {"q":"How is this different from the Marketing SOPs pack?","a":"The SOPs pack is the content. The OS is the system — a Notion database that ties the SOPs together, adds prompts at each step, and links to a weekly operating rhythm. The walkthrough video shows you how to wire it up."},
            {"q":"Do I need Notion?","a":"Yes — Notion free tier is fine. The OS is built native to Notion and wouldn't translate well to another tool."},
            {"q":"Is the video gated? Can I share it with my team?","a":"Delivered as a Loom link with an org-wide view permission. Share with your team; don't repost publicly."},
            {"q":"What if I already own the SOPs pack?","a":"Email Support@aigatecrashers.com for a $12 credit toward the OS."},
            {"q":"Refund?","a":"7-day no-questions. Email Support@aigatecrashers.com."},
        ],
        includes=[
            "Notion marketing OS database + 10 SOPs",
            "Prompt-chain workflows for each SOP",
            "20-min video walkthrough by Keith",
            "Stand-up + monthly review templates",
            "7-day money-back guarantee",
        ],
        bump_id="bump-content-repurposing",
        bump_name="The Content Repurposing Machine",
        bump_desc="Turn 1 blog into 12 social posts, 3 emails, 1 newsletter. Plugs into the Marketing OS.",
        bump_price=15,
    ),

    Product(
        slug="content-repurposing-machine",
        title="The Content Repurposing Machine",
        seo_title="The Content Repurposing Machine — 1 Blog → 12 Posts, 3 Emails, 1 Newsletter | AI Gatecrashers",
        meta_desc="Turn one long piece of content into a full content stack. Prompt chain, workflow, and 2 real examples. $47.",
        price=47,
        hero_tagline="Write it once. Ship it twelve ways. Turn one blog or video into 12 social posts, 3 emails, a newsletter, and more — with a prompt chain that runs in one session.",
        category="premium",
        data_tags="content,get-customers",
        badge="New",
        emoji="🔁",
        whats_inside=[
            "The master prompt chain — 7 linked prompts that take 1 source piece → 12 derivative outputs",
            "Platform-specific adapters: LinkedIn, X, Instagram, TikTok captions, email, newsletter",
            "Two worked examples (one from a blog post, one from a YouTube video) so you see the system end-to-end",
            "A 30-minute walkthrough video showing Keith running the chain live",
            "Weekly repurposing rhythm template — what to ship Monday through Friday",
            "Recovery prompts — what to do when the output sounds flat",
        ],
        personas=[
            {"emoji":"✍️","title":"Writers + creators","desc":"You produce long-form content. You should not also be rewriting it 12 ways manually."},
            {"emoji":"🎥","title":"Podcasters + YouTubers","desc":"One episode → a month of social. The repurposing gap is why most shows plateau."},
            {"emoji":"💼","title":"Founders building personal brand","desc":"You have no time. One long piece per month, twelve outputs. That's the deal."},
        ],
        outcomes=[
            "Turn one blog into a month of social content in one sitting",
            "Give a podcast episode a real second life on social and email",
            "Build a personal brand without being online 4 hours a day",
            "Stop 'starting from scratch' on every channel",
        ],
        faqs=[
            {"q":"Will the outputs all sound the same?","a":"No — the chain is designed to voice-shift for each platform. The LinkedIn output reads like LinkedIn; the TikTok caption reads like TikTok. Same source idea, different voice."},
            {"q":"What source content works best?","a":"Blog posts over 800 words, podcast transcripts, and long YouTube videos. Short-form source (tweets, captions) doesn't give the chain enough to work with."},
            {"q":"How long does one run take?","a":"About 40-60 minutes end-to-end on your first try. 20-30 minutes once you've done it twice."},
            {"q":"Do I need a paid AI subscription?","a":"Recommended but not required. The chain runs on free tier of ChatGPT, Claude, or Gemini. Paid plans give you more capacity for the 12-output batch."},
            {"q":"Refund?","a":"7-day no-questions. Email Support@aigatecrashers.com."},
        ],
        includes=[
            "Master prompt chain — 7 linked prompts",
            "Platform adapters for 6 channels",
            "2 worked examples + 30-min walkthrough",
            "Weekly repurposing rhythm template",
            "7-day money-back guarantee",
        ],
        bump_id="bump-viral",
        bump_name="Viral Content Toolkit",
        bump_desc="31 viral hook templates to feed the machine with better openers.",
        bump_price=7,
    ),

    # --- Theme 5: Tripwire ---
    Product(
        slug="stop-guessing-prompt-builder",
        title="The Stop Guessing Prompt Builder",
        seo_title="The Stop Guessing Prompt Builder — A Master Prompt That Writes Your Prompts | AI Gatecrashers",
        meta_desc="One master prompt that writes better prompts for you. Tell it what you want; get a working ChatGPT prompt back. $3.",
        price=3,
        hero_tagline="Stop guessing what to type into your AI. One master prompt that writes better prompts for you — tell it what you want, get a working prompt back. Works with ChatGPT, Claude, or Gemini.",
        category="chatgpt",
        data_tags="run-business,content,get-customers",
        badge="New",
        emoji="🧩",
        whats_inside=[
            "The master 'prompt-writing prompt' — paste once, reuse forever",
            "10 fillable example conversations showing it in action",
            "A cheat sheet: what makes a great prompt vs. a weak one",
            "Troubleshooting guide — what to do when the output feels flat",
        ],
        personas=[
            {"emoji":"🧩","title":"Everyone who's ever stared at a blank AI chat window","desc":"If you've typed something into ChatGPT, Claude, or Gemini, hit enter, and thought 'that's not what I wanted,' this fixes it."},
            {"emoji":"🏪","title":"SMB owners new to AI","desc":"The fastest on-ramp. You don't need 500 prompts — you need one prompt that writes the prompt."},
            {"emoji":"✍️","title":"Creators and writers","desc":"Skip the prompt-engineering rabbit hole. Delegate the prompt-writing to AI."},
        ],
        outcomes=[
            "Turn any rough idea into a working prompt in 30 seconds",
            "Stop scrolling prompt lists looking for 'the right one'",
            "Get outputs that match what's in your head, not what the AI guesses",
            "Teach a team member to use AI in about 5 minutes",
        ],
        faqs=[
            {"q":"Just $3? Is this actually useful?","a":"Yes. It's short because good tools are short. One prompt, a few examples, a cheat sheet. Takes 10 minutes to use and saves hours per week."},
            {"q":"Do I need a paid AI plan?","a":"No. Works on free tiers of ChatGPT, Claude, and Gemini."},
            {"q":"Is this the same thing as 'meta-prompting'?","a":"Yes, that's the technical term. This is the practical version with examples and troubleshooting."},
            {"q":"Can I use this for client work?","a":"Unlimited-use license. Yes."},
            {"q":"Refund?","a":"7-day no-questions."},
        ],
        includes=[
            "The master prompt-writing prompt",
            "10 fillable examples",
            "Cheat sheet + troubleshooting guide",
            "Delivered as a single Notion page",
            "7-day money-back guarantee",
        ],
        bump_id="bump-starter-pack",
        bump_name="The AI Starter Pack for Small Business",
        bump_desc="50 beginner prompts + quick-start + 7-day plan. The natural next step.",
        bump_price=6,
    ),
]


# ============================================================
# PAGE TEMPLATE
# ============================================================

def render_page(p: Product) -> str:
    canonical = f"https://aigatecrashers.com/products/{p.slug}.html"
    # Escape values for HTML attributes
    t_esc = lambda s: html.escape(s, quote=True)

    # JSON-LD payloads
    product_ld = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": p.title,
        "description": p.meta_desc,
        "brand": {"@type": "Brand", "name": "AI Gatecrashers"},
        "offers": {
            "@type": "Offer",
            "price": f"{p.price:.2f}",
            "priceCurrency": "USD",
            "availability": "https://schema.org/InStock",
            "url": canonical,
        },
    }
    breadcrumb_ld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://aigatecrashers.com/"},
            {"@type": "ListItem", "position": 2, "name": "Store", "item": "https://aigatecrashers.com/store/"},
            {"@type": "ListItem", "position": 3, "name": p.title, "item": canonical},
        ],
    }
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq["q"],
                "acceptedAnswer": {"@type": "Answer", "text": faq["a"]},
            }
            for faq in p.faqs
        ],
    }

    whats_inside_html = "\n".join(
        f'            <li><span class="check">✓</span> {html.escape(item)}</li>'
        for item in p.whats_inside
    )

    personas_html = "\n".join(
        f'''            <div class="persona-card">
              <div class="persona-emoji">{persona["emoji"]}</div>
              <h3>{html.escape(persona["title"])}</h3>
              <p>{html.escape(persona["desc"])}</p>
            </div>'''
        for persona in p.personas
    )

    outcomes_html = "\n".join(
        f"            <li>{html.escape(out)}</li>" for out in p.outcomes
    )

    faqs_html = "\n".join(
        f'''          <details class="faq-item">
            <summary>{html.escape(faq["q"])}</summary>
            <p>{html.escape(faq["a"])}</p>
          </details>'''
        for faq in p.faqs
    )

    includes_html = "\n".join(
        f"            <li>✓ {html.escape(item)}</li>" for item in p.includes
    )

    bump_block = ""
    if p.bump_id:
        bump_block = f'''
          <div class="order-bump">
            <label>
              <input type="checkbox" data-bump-id="{p.bump_id}" data-bump-name="{t_esc(p.bump_name)}" data-bump-price="{p.bump_price}">
              <div class="bump-label-content">
                <div class="bump-title">Add: {html.escape(p.bump_name)}</div>
                <p class="bump-desc">{html.escape(p.bump_desc)}</p>
                <span class="bump-price">+ ${p.bump_price}</span>
              </div>
            </label>
          </div>'''

    badge_html = (
        f'<div class="product-badge">{html.escape(p.badge)}</div>' if p.badge else ""
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{t_esc(p.seo_title)}</title>
  <meta name="description" content="{t_esc(p.meta_desc)}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{t_esc(p.seo_title)}">
  <meta property="og:description" content="{t_esc(p.meta_desc)}">
  <meta property="og:type" content="product">
  <meta property="og:url" content="{canonical}">
  <meta property="og:site_name" content="AI Gatecrashers">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@aigatecrashers">
  <meta name="twitter:title" content="{t_esc(p.seo_title)}">
  <meta name="twitter:description" content="{t_esc(p.meta_desc)}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/styles.css?v={CACHE_VER}">

  <script type="application/ld+json">
{json.dumps(product_ld, indent=2)}
  </script>
  <script type="application/ld+json">
{json.dumps(breadcrumb_ld, indent=2)}
  </script>
  <script type="application/ld+json">
{json.dumps(faq_ld, indent=2)}
  </script>
</head>
<body>

  <!-- HEADER -->
  <header class="site-header sticky-header">
    <div class="header-inner container">
      <a href="../index.html" class="logo">AI Gatecrashers</a>
      <nav class="main-nav">
        <a href="../index.html#start-here">Start Here</a>
        <a href="../store/">Store</a>
        <a href="../blog/">Blog</a>
      </nav>
      <button class="cart-btn js-toggle-cart" aria-label="Open cart">
        Cart <span class="cart-count">0</span>
      </button>
    </div>
  </header>

  <!-- CART PANEL -->
  <div class="cart-overlay"></div>
  <aside class="cart-panel" aria-label="Shopping cart">
    <div class="cart-panel-header">
      <h2>Your Cart</h2>
      <button class="cart-close js-toggle-cart" aria-label="Close cart">×</button>
    </div>
    <div class="cart-items"><div class="cart-empty"><p>Your cart is empty.</p></div></div>
    <div class="cart-footer">
      <div class="cart-total">Total: <span class="cart-total-amount">$0.00</span></div>
      <button class="cart-checkout js-checkout">Checkout</button>
    </div>
  </aside>

  <!-- BREADCRUMBS -->
  <nav class="breadcrumbs container" aria-label="Breadcrumb" style="margin-top: 24px;">
    <a href="../index.html">Home</a>
    <span class="breadcrumb-sep">›</span>
    <a href="../store/">Store</a>
    <span class="breadcrumb-sep">›</span>
    <span class="current">{html.escape(p.title)}</span>
  </nav>

  <!-- HERO -->
  <section class="product-hero product-hero--{p.category}">
    <div class="container product-hero-inner">
      <div class="product-hero-text">
        {badge_html}
        <h1>{html.escape(p.title)}</h1>
        <p class="product-tagline">{html.escape(p.hero_tagline)}</p>
        <div class="product-hero-price">
          <span class="price-main">${p.price}</span>
          <span class="price-note">One-time. Instant access.</span>
        </div>
      </div>
    </div>
  </section>

  <!-- MAIN -->
  <main class="product-main container">
    <div class="product-layout">

      <div class="product-content">

        <section class="content-section">
          <h2>What's inside</h2>
          <ul class="checklist">
{whats_inside_html}
          </ul>
        </section>

        <section class="content-section">
          <h2>Who this is for</h2>
          <div class="persona-grid">
{personas_html}
          </div>
        </section>

        <section class="content-section">
          <h2>What you'll be able to do</h2>
          <ul class="outcomes-list">
{outcomes_html}
          </ul>
        </section>

        <section class="content-section faq-section">
          <h2>Frequently asked questions</h2>
{faqs_html}
        </section>

      </div>

      <aside class="product-purchase-box">
        <div class="purchase-box-inner">
          <div class="purchase-price">
            <span class="purchase-price-main">${p.price}</span>
            <div class="purchase-price-note">One-time — Instant access</div>
          </div>
          <ul class="purchase-includes">
{includes_html}
          </ul>
          <button
            class="cta-button cta-button-lg js-add-to-cart"
            data-product-id="{p.slug}"
            data-product-name="{t_esc(p.title)}"
            data-product-price="{p.price}"
            data-checkout-url=""
            style="width:100%;">
            Add to Cart — ${p.price}
          </button>
          <div class="purchase-guarantee">
            <span class="guarantee-icon">🛡️</span>
            7-Day Money-Back Guarantee
          </div>
{bump_block}
        </div>
      </aside>

    </div>
  </main>

  <!-- BOTTOM CTA -->
  <section class="product-cta-section">
    <div class="product-cta-inner">
      <h2>{html.escape(p.title)} — ${p.price}</h2>
      <p>{html.escape(p.hero_tagline)}</p>
      <button
        class="cta-button cta-button-lg js-add-to-cart"
        data-product-id="{p.slug}"
        data-product-name="{t_esc(p.title)}"
        data-product-price="{p.price}"
        data-checkout-url="">
        Get Instant Access — ${p.price}
      </button>
      <p class="cta-sub">Instant delivery · 7-day guarantee · Works with free AI tools</p>
    </div>
  </section>

  <!-- FOOTER -->
  <footer class="site-footer">
    <div class="container footer-grid">
      <div class="footer-col footer-brand">
        <a href="../index.html" class="footer-logo">AI Gatecrashers</a>
        <p>Plain-English AI training, prompt packs, and playbooks for small businesses, non-profits, and first-time AI users. Built by Keith Allen Schuh.</p>
      </div>
      <div class="footer-col">
        <h4>Store</h4>
        <a href="../store/#get-customers">Get customers</a>
        <a href="../store/#run-business">Run your business</a>
        <a href="../store/#side-business">Start something new</a>
        <a href="../store/#bundles">Bundles &amp; courses</a>
      </div>
      <div class="footer-col">
        <h4>Resources</h4>
        <a href="../index.html#start-here">Start Here</a>
        <a href="../blog/">Blog</a>
      </div>
      <div class="footer-col">
        <h4>Connect</h4>
        <a href="mailto:Support@aigatecrashers.com">Support@aigatecrashers.com</a>
      </div>
    </div>
    <div class="footer-bottom container">
      <p>&copy; 2026 AI Gatecrashers. Built by one human, with care.</p>
    </div>
  </footer>

  <script src="../js/store.js"></script>
</body>
</html>
"""


# ============================================================
# RUN
# ============================================================

def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    written = 0
    for p in PRODUCTS:
        path = OUT / f"{p.slug}.html"
        if path.exists():
            # Safety: don't overwrite an existing product page.
            # (Unlikely for our new slugs, but defensive.)
            print(f"SKIP (exists): {path.name}")
            continue
        path.write_text(render_page(p), encoding="utf-8")
        written += 1
        print(f"wrote  {path.name}  (${p.price}  tags={p.data_tags}  cat={p.category})")
    print(f"\nTotal new products written: {written} of {len(PRODUCTS)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
