---
name: channel-playbooks
description: Use this skill whenever the user is selecting, evaluating, or designing tactics for a specific marketing channel — paid search, paid social (Meta/LinkedIn/TikTok/X), SEO, content, email, webinars, outbound sales, partnerships, affiliate, influencer, direct mail, podcast, community, events. Triggers on channel names, "where should I advertise", "best channel for X", "should I do Google Ads or Meta", "outbound vs inbound", "channel mix", "we tried X and it didn't work". Provides the per-channel playbook when it works, when it doesn't, expected CACs/CPLs, key creative patterns, measurement approach, and common failure modes. Use this BEFORE recommending any channel — never recommend a channel without checking it against the channel-fit matrix.
---

# Channel Playbooks

The job of this skill is to match channels to businesses. The wrong channel can waste a year of runway. The right one compounds. Most channel mistakes come from copying what worked for a different business at a different stage with a different ACV.

## When to invoke

- The user asks "what channel should I use"
- The user has tried channels that didn't work and wants to understand why
- The user wants to add a new channel
- You're designing a funnel and need to pick the channels that connect each stage
- The user names a channel and you need to validate fit

## The first-principles rule

**The right channel for a business is determined by three variables:**

1. **ACV / AOV** (annual contract value or average order value) — determines how much you can spend to acquire a customer
2. **Sales cycle length** — determines how patient the channel needs to be
3. **Where the audience already is** — determines reach feasibility

Cheaper customers need cheaper channels. Longer cycles need nurture-capable channels. Niche audiences need precision channels.

If a user is doing cold outbound for a $9/month consumer app, the math doesn't work — say so. If a user is doing TikTok for a $250K enterprise contract, the audience isn't there — say so.

## Channel-fit matrix

| Channel | ACV sweet spot | Cycle length | Where the audience is | Best for |
|---------|----------------|--------------|----------------------|----------|
| **Paid search (Google/Bing)** | $50+ AOV / $500+ ACV | Any | Active searchers — high intent | Capturing existing demand. Solution-aware audience. |
| **Paid social — Meta (FB/IG)** | $20+ AOV / $200+ ACV | Short to medium | Broad consumer + SMB | DTC, B2C apps, mass-market SaaS |
| **Paid social — LinkedIn** | $5K+ ACV minimum | Medium to long | Working professionals, decision-makers | B2B sales-led, mid-market+, recruiting |
| **Paid social — TikTok** | $20+ AOV / $200+ ACV | Short | Gen Z + millennial consumer | DTC consumer, B2C apps, creator-friendly products |
| **Paid social — X (Twitter)** | Variable | Variable | Tech, finance, niche professional | Tech B2B brand building, niche audiences |
| **Paid social — Reddit** | $20+ AOV / $500+ ACV | Variable | Niche enthusiasts, technical audiences | Dev tools, hobbyist products, gaming |
| **SEO / content marketing** | $500+ ACV (math breaks below) | Long (6–18mo to payoff) | Searchers + ongoing readers | B2B SaaS, services, info products. NOT for high-velocity DTC. |
| **Email (owned list)** | Any | Any | Your existing list | Nurture, retention, expansion. Not a top-of-funnel channel. |
| **Email — cold outbound** | $20K+ ACV minimum | Medium to long | Decision-makers at named accounts | Enterprise B2B, high-ticket services |
| **Outbound calling** | $50K+ ACV minimum | Long | Decision-makers at named accounts | Enterprise B2B, complex sales |
| **Webinars** | $1K+ ACV | Medium | Existing audience + paid traffic | B2B mid-market, courses, high-ticket info |
| **Podcast (host)** | $500+ ACV / brand-driven | Long (brand play) | Your future audience | Brand building, thought leadership. Not a direct-response channel. |
| **Podcast (guest/sponsor)** | $100+ AOV / $1K+ ACV | Medium | Niche communities | DTC with story, B2B targeting specific roles |
| **Influencer / creator** | $20+ AOV / $200+ ACV | Short | Their audience | DTC consumer, lifestyle, mass B2C apps |
| **Affiliate / partner referral** | $50+ AOV / $500+ ACV | Variable | Adjacent product audiences | DTC, SaaS, courses |
| **Community-led** | $500+ ACV / brand-driven | Long | Existing community you build or join | Dev tools, niche SaaS, info products |
| **Events (own or sponsor)** | $25K+ ACV | Long | Industry concentration | Enterprise B2B, high-touch services |
| **Direct mail** | $5K+ ACV / luxury DTC | Medium | Named accounts or high-value lists | ABM enterprise, luxury, real estate |
| **PR / earned media** | Variable / brand-driven | Long | Mass audience | Launches, repositioning. Not a steady-state channel. |
| **Referral program (customer-driven)** | Any | Short | Existing customers' networks | Any product with delighted customers |
| **Marketplaces (App Store, Shopify, etc.)** | Variable | Short | Marketplace browsers | Apps, plugins, ecommerce |

If the user is in the wrong quadrant, surface the math. Don't just say "this won't work" — show why.

## The channel concentration principle

Most early-stage businesses fail by spreading across too many channels too soon. The rule:

> **Pick 1–2 channels. Get to $X MRR/revenue from those before adding a third.**

Where $X is roughly:

- $50K MRR for SaaS
- $50K/mo revenue for DTC
- 10 customers / $100K ARR for high-ticket B2B

Why this matters:

- Each channel has a learning curve (creative, audience targeting, measurement, optimization). Splitting attention adds runtime cost.
- Most channels need a minimum spend to evaluate (Meta needs ~$5K to learn an audience; SEO needs 6 months of consistent content).
- "Multi-channel testing" early = "everything sucked because nothing got enough investment."

When the user asks "what should I add?", ask back: "What's the current concentration? If you're under the threshold, the answer is 'don't add — double down on the existing channel.'"

## Per-channel mini-playbooks

For each channel below: when it works, when it doesn't, expected economics, key creative patterns, measurement, top failure modes. For deeper playbooks see `references/channels/[name].md`.

### Paid search (Google Ads)

**When it works:** there is existing search demand for the problem you solve. Your prospects use specific search terms when triggered. **When it doesn't:** category is too new to have search volume. Or: you're competing against incumbents with 10x your budget on the same keywords. **Economics:** CPC varies wildly ($0.50–$100+). CAC = CPC ÷ visit-to-customer conversion. Profitable if `LTV > 3× CAC` and payback < 12 months. **Creative patterns:** Match user intent precisely. High-intent keywords ("[competitor] alternative", "[problem] software") convert 3–10× better than broad keywords. Landing page must match the ad headline word-for-word. **Measurement:** track to conversion, not just clicks. Use offline conversion import for B2B (Google sees pipeline, not just leads). **Top failures:** broad-match keywords burning budget on irrelevant traffic. Optimizing for clicks instead of conversions. Sending all traffic to homepage.

### Paid social — Meta (Facebook/Instagram)

**When it works:** broad, visual-friendly products with strong creative angles. Audiences trackable via interests or lookalikes. **When it doesn't:** B2B with narrow ICP (LinkedIn is better). Pure direct-response with no creative variation (you'll burn audiences in weeks). **Economics:** $5–$50 CPM, $0.50–$10 CPC, CAC = depends entirely on creative + offer fit. Plan for $3K–$10K to test a new audience. **Creative patterns:** UGC-style video outperforms polished brand creative 2–5×. New creative every 7–14 days; ad fatigue is real. Test angles, not just visuals (problem-led vs. result-led vs. social-proof-led). **Measurement:** trust 7-day click + 1-day view attribution for direct response. Server-side conversions (CAPI) since iOS 14. Watch for CAC inflation as scale increases. **Top failures:** scaling spend before nailing creative. One ad set with 50 audiences (kills the algorithm). Ignoring creative refresh rate.

### Paid social — LinkedIn

**When it works:** B2B with ACV > $5K targeting specific roles or industries. Job-change triggers, company-growth triggers. **When it doesn't:** low-ACV products (LinkedIn CPMs are 3–10× Meta). Vague targeting. **Economics:** $30–$150 CPM, $5–$25 CPC. CACs commonly $300–$2000 for cold lead. Document downloads cheaper than demos. **Creative patterns:** thought leadership posts boosted as ads outperform pure ad creative. Document ads (carousels) for lead gen. Conversation ads for demo bookings (use sparingly — high CPM). **Measurement:** lead quality matters more than lead volume. Track to opportunity, not lead. **Top failures:** broad targeting (Job Title alone is too wide). Sending leads to gated PDFs that nobody downloads. Optimizing for clicks instead of qualified pipeline.

### SEO / content marketing

**When it works:** category with search volume. Long-term play with 6–18 month payoff. ACV high enough to justify content investment ($500+ ACV minimum, $5K+ ACV ideal). **When it doesn't:** category too new (no search volume yet). Short patience (founder needs revenue this quarter). Hyper-competitive established category without distribution advantage. **Economics:** content has near-zero marginal cost per visitor, but high upfront cost. Realistic: $50K–$200K invested before meaningful pipeline. Math works when LTV is high and competition is moderate. **Creative patterns:** topic clusters around a pillar (one big guide + 10 supporting articles). Original research and tools outperform listicles. "Comparison" content ([you] vs [competitor]) converts BOFU traffic. **Measurement:** rankings → organic traffic → conversion to email/trial → pipeline. 6-month minimum before judging. **Top failures:** publishing without distribution. Targeting impossible keywords (DR 50 site competing on "CRM" doesn't work). Optimizing for traffic that doesn't convert.

### Email (owned list)

**When it works:** you have a list. Nurture, retention, expansion, win-back. **When it doesn't:** as a top-of-funnel channel. Email is not for acquiring strangers — it's for converting and retaining people who opted in elsewhere. **Economics:** highest ROI of any channel (often $30–$50 per $1 spent) IF the list is healthy. List decay is real (~20–30%/year). **Creative patterns:** plain-text outperforms heavily designed email for B2B. Specific subject lines beat clever ones. Segment by behavior, not demographics. Drip sequences over batch sends. **Measurement:** open rate is increasingly unreliable (Apple MPP). Track click → conversion. Engagement-based deliverability matters more than ever. **Top failures:** sending the same email to everyone. Optimizing for opens instead of conversions. Buying or scraping lists (kills domain reputation).

### Cold outbound (email + LinkedIn)

**When it works:** ACV > $20K, named target accounts, decision-makers reachable, clear trigger to reference. **When it doesn't:** ACV < $20K (math doesn't work). Mass blasting (kills sender reputation, response rates collapse). Generic templates. **Economics:** 1–3% reply rate on good campaigns. 10–20% of replies → meetings. Need 500–1000 contacted to fill a week of meetings for one SDR. **Creative patterns:** trigger-based ("just saw you raised your Series B"). Specificity wins (a sentence proving you researched the account). Short messages (< 75 words). Multi-touch sequences (email → LinkedIn → email). **Measurement:** meetings booked → opportunities → revenue. Reply rate alone is vanity. **Top failures:** spray-and-pray volume. Generic personalization ("I see you work at {{company}}"). Pitching in the first message. Ignoring deliverability hygiene.

### Webinars

**When it works:** B2B mid-market+, complex products needing education, high-ticket info products and courses. **When it doesn't:** simple products that don't need 30+ min of explanation. Audiences with low attention budgets. **Economics:** typically 25–40% show-up rate from registrants. 5–15% of attendees → meaningful next step. Best when paired with paid traffic. **Creative patterns:** taught content > pitchy content. Promise a specific outcome in the title ("How to cut your CAC by 30% in Q1"). Live > recorded for engagement; on-demand for scale. **Measurement:** registrants → attendees → next-step conversions → pipeline. **Top failures:** pitch slap at the end (kills trust). Too-broad topics. No follow-up sequence for no-shows.

### Influencer / creator partnerships

**When it works:** consumer products with visual or storytelling angles. Audiences concentrated on creator platforms. **When it doesn't:** B2B (with rare exceptions). Generic "promote my product" deals — only authentic integrations work now. **Economics:** ranges from $0 (gifted) to $100K+ (top creators). Micro-influencers (10K–100K followers) often outperform mega-influencers on ROAS. **Creative patterns:** creator-led content > brand-supplied scripts. Long-term partnerships > one-off posts. Affiliate code or unique URL for attribution. **Measurement:** unique codes, dedicated landing pages. Track to first purchase, then to LTV. **Top failures:** giving creators a script (kills authenticity). One-and-done partnerships. No attribution mechanism.

### Affiliate / partner programs

**When it works:** AOV/ACV high enough to pay 20–30% commission. Adjacent products with overlapping audiences. **When it doesn't:** thin margins. Low-trust products. No clear partner profile. **Economics:** pay per sale, so ROI is favorable by definition — but recruiting and managing partners has real cost. **Creative patterns:** the partner does the selling. Provide swipe copy, landing pages, sometimes co-branded content. Make the program dead simple to join. **Measurement:** affiliate-attributed revenue, partner LTV, partner activation rate (% of signups who drive a sale). **Top failures:** expecting partners to figure it out alone. No assets provided. Slow payouts (kills the program).

### Community-led

**When it works:** dev tools, niche SaaS, info products, anything where users teach each other. Long-term moat. **When it doesn't:** transactional products with no shared interest. Founders who don't have time to invest in community. **Economics:** hard to measure short-term; large compounding returns long-term. Lower CAC over time; higher retention. **Creative patterns:** be in communities before launching one of your own. Slack/Discord/forum + content + events. Spotlight community members, not your product. **Measurement:** member count is vanity; active engagement, attributable signups, retention lift among community members matter. **Top failures:** launching a Slack and waiting. Over-promoting your product. Letting toxic dynamics emerge.

### Referral (customer-driven)

**When it works:** any product with delighted customers. Especially services, high-touch B2B, products with strong NPS. **When it doesn't:** products customers are embarrassed to use, single-purchase ecommerce with no social context, anything with neutral-or-worse NPS. **Economics:** the cheapest channel ever. CAC is the referral incentive (often $0–$200) plus the program cost. Conversion rate of referred leads is typically 3–10× cold.

**The critical insight for service businesses and B2B SaaS:** if you're already getting referrals organically, formalizing the referral channel is almost always the highest-leverage move you can make — higher than adding a new acquisition channel. Most founders skip this because referrals "just happen." That's exactly why they're underexploited.

**Formalization playbook (in order):**

1. **Track referrals by source.** For the last 12 months, who referred whom? Group by referrer type (customer, partner, advisor, investor, ex-colleague). The top 3 sources usually account for 60%+ of referrals.
2. **Quantify the value.** What's the CAC, close rate, and LTV of referred customers vs. cold-acquired? Referred customers almost always show 2–5× better economics. Put a dollar number on this so it's visible.
3. **Design the ask cadence.** Most customers will refer if asked — at the right time. The right times: post-success-moment (deal closed, milestone hit, "this changed my workflow" reaction), 90-day post-onboarding (they have results to share), and at renewal (their endorsement of the renewal commits them socially).
4. **Make the ask specific.** "Do you know anyone else dealing with [their specific problem]?" outperforms "any referrals?" by 5–10×. Pre-write the introduction email they can forward.
5. **Reward the referrer, not just the referred.** $200 credit, a donation in their name, a public thank-you, or a meaningful gift. Tangible reciprocity reinforces the behavior.
6. **Instrument it.** Tag every referral in CRM. Report referral-attributed pipeline monthly. What you measure, you grow.

**For service businesses specifically:** add structured partner referrals (VCs, accountants, consultants, complementary services) to the customer referrals above. A formal partner program with 10 active partners typically produces 3–5× the volume of ad-hoc referral asks.

**Top failures:** waiting for referrals instead of asking. No tracking (so no insight into what works). Rewarding the referred customer but not the referrer (misaligned incentive). Generic "refer us!" emails (low signal).

For all other channels (events, PR, direct mail, podcasts, marketplaces, etc.) see the relevant `references/channels/[name].md` file.

## Channel mix recommendations by business type

### Early B2B SaaS (pre-$1M ARR)

1. Cold outbound (if ACV > $20K) OR content + SEO (if ACV $5K–$20K) OR paid search (if ACV $1K–$5K)
2. LinkedIn organic + selective paid
3. Founder-led: podcast guesting, community participation
4. _Avoid until later_: paid Meta, events, PR, broad SEO

### Growth-stage B2B SaaS ($1M–$10M ARR)

1. Whatever channel got you to $1M — double down
2. Add one adjacent: content+SEO if you started with outbound; outbound if you started with inbound
3. LinkedIn ads for ABM
4. Affiliate / partner program

### Pre-traction DTC (< $5K/mo marketing budget)

**Critical:** at this budget level with AOV under ~$30, paid ads are usually the wrong starting move. The math: a single Meta audience needs ~$5K to learn before producing reliable signal. Below that, you're buying noise. Worse: at low AOV, even $20 CACs from paid eat the entire first-purchase margin.

The right starting stack:

1. **Organic content + founder narrative** — Instagram, TikTok, or wherever the audience is. Founder-led content has zero CAC and builds the brand assets you'll need to make paid ads work later.
2. **UGC + micro-influencer gifting** — give product to 20–50 micro-creators (<50K followers) in exchange for content rights. Build the creative library before spending on paid.
3. **Email/SMS list capture from day 1** — pop-up, lead magnet, post-purchase. Your list will be the cheapest channel you ever have.
4. **Then** — once organic traction proves the product resonates AND you have a creative library AND your AOV/margin math works — graduate to paid (Meta first).

**Avoid until graduated:** any paid ads, agency retainers, PR firms, paid influencer deals.

**Signal you're ready to spend on paid:** organic followers growing 10%+/mo, repeat purchase rate >25%, gross margin per order ≥ 2× your projected paid CAC, AND you have 10+ distinct creative angles tested organically.

### DTC ecommerce (pre-$1M revenue)

1. Meta + Instagram ads (creative-driven)
2. Email/SMS retention
3. Influencer / UGC partnerships
4. _Avoid_: search ads on competitive terms, traditional PR

### Growth-stage DTC ($1M–$10M)

1. Meta scaled with creative production engine
2. Add: TikTok, YouTube
3. Add: SEO for branded + category terms
4. Add: affiliate / influencer at scale

### High-ticket services / consulting

1. Founder content (LinkedIn, podcast)
2. Referral / partner network
3. Targeted ABM outbound
4. _Avoid_: paid search (CPCs unsustainable), broad social

### Info products / courses

1. Long-form content (YouTube, podcast, email list)
2. Webinar + email funnel
3. Affiliate program with content creators
4. Add later: paid (FB/YT) once funnel is proven

## Common channel mistakes

1. **Adding channels before nailing one** — see concentration principle above
2. **Copying competitors blindly** — they have different unit economics, audience saturation, brand recognition
3. **"We tried it for a month"** — most channels need a quarter minimum to evaluate fairly
4. **Confusing channel and creative** — when a channel "fails", it's usually the creative, the offer, or the targeting, not the channel itself
5. **Ignoring channel-stage fit** — Meta works for awareness/consideration; for high-intent purchase, search wins
6. **Optimizing for the wrong metric** — clicks ≠ leads ≠ customers ≠ revenue. Always measure to revenue.
7. **Underspending the floor** — channels need a minimum learning budget. Below it, you'll get noise.
8. **Vanity audience reach** — "we got X impressions" without conversion doesn't move the business

## Output checklist

Before handing off, this skill must produce:

- [ ] Recommended primary channel(s) — 1 or 2 max for early stage
- [ ] Justification tied to ACV/AOV, cycle length, audience location
- [ ] Expected economics range (CAC band, learning budget)
- [ ] Top 3 creative angles for the channel
- [ ] Top 3 failure modes to watch for
- [ ] Measurement plan (what to track and when to make decisions)

## Reference files

One per channel, loaded on demand:

- `references/channels/paid-search.md`
- `references/channels/meta-ads.md`
- `references/channels/linkedin-ads.md`
- `references/channels/tiktok-ads.md`
- `references/channels/seo-content.md`
- `references/channels/email.md`
- `references/channels/cold-outbound.md`
- `references/channels/webinars.md`
- `references/channels/influencer.md`
- `references/channels/affiliate.md`
- `references/channels/community.md`
- `references/channels/podcast.md`
- `references/channels/events.md`
- `references/channels/direct-mail.md`
- `references/channels/referral.md`

## Final guidance to the agent

If the user asks "what channel should I use" without giving you ACV, audience, and stage info, do NOT answer. Bounce back: "I can answer this well with three numbers — your AOV or ACV, your sales cycle length, and where your audience already spends time. What are those?" Channel advice without those inputs is malpractice.
