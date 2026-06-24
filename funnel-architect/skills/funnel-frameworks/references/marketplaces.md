# Marketplaces — Funnel Patterns

Reference loaded on-demand by the `funnel-frameworks` skill when the user is building or auditing a marketplace.

A marketplace is fundamentally different from a SaaS or DTC funnel: you're building two funnels in parallel that meet at the transaction, and the entire business hinges on a metric most one-sided businesses never have to think about — **liquidity**.

This reference covers: the cold-start problem, concentration strategy, single-player mode, liquidity metrics, supply vs. demand prioritization, channel strategy per side, and the most common ways marketplaces fail.

---

## 1. The cold-start problem

Marketplaces face a chicken-and-egg problem from day one: suppliers won't join without customers, customers won't come without suppliers. This is the defining strategic challenge.

**The wrong move:** launch broadly and hope both sides build simultaneously. This produces a thin marketplace where neither side gets value. Patients can't find a therapist that matches their specialty + location + schedule + insurance. Therapists never get a patient. Both sides churn.

**The right move:** constrain the launch dimensions until you achieve liquidity in one narrow segment, then expand.

### The concentration dimensions

Pick one or two of these to narrow your initial market:

| Dimension | Example narrowing |
|-----------|-------------------|
| **Geography** | One zip code, one neighborhood, one campus |
| **Specialty / vertical** | "Therapists for anxiety" not "all therapists" |
| **Demographic** | LGBTQ+ patients, BIPOC patients, women-only |
| **Price tier** | Cash-pay only, sliding-scale only, premium only |
| **Use case** | "Couples therapy" not "therapy generally" |
| **Time window** | Same-week appointments only |

The rule: narrow enough that you can saturate one side and credibly serve the other. Going national with 30 suppliers is failure. Going to one zip code with 30 suppliers is potentially viable. Going to one zip code AND one specialty with 30 suppliers is even better.

### How to pick the wedge

Three filters:

1. **Where do you have an unfair advantage?** Founder network in one city, an existing community in one vertical, a partner who can introduce supply at scale.
2. **Where is the pain most acute?** Patients who can't find therapists matching X criteria today are highly motivated to use a new solution. Generic "marketplace for therapy" loses to incumbents (Psychology Today, ZocDoc, insurance directories).
3. **Where is supply most constrained?** Counterintuitively, you want to launch where supply is the constraint — because demand-generation is much easier than supply-generation. If you can solve supply in a wedge, demand follows.

---

## 2. The liquidity metric

The single most important metric for any marketplace, regardless of vertical, is **match liquidity**: the percentage of searches that result in a usable match.

**Definition:** % of demand-side searches that surface 3+ relevant supply options within the user's stated constraints (time, price, location, specialty, etc.).

**Why 3+ and not 1?** A single match feels like "the only option" — users don't trust marketplaces that don't show alternatives. Three options creates a sense of marketplace.

**Targets:**

- Below ~60% match liquidity: demand-side churn is catastrophic. Patients search, don't find, leave, don't come back.
- 60–80%: marketplace is viable in the wedge. Can sustain growth.
- 80%+: liquidity moat forming. Network effects starting to compound.

**This is the metric to optimize before anything else.** Not signups. Not GMV. Not revenue. If match liquidity is below 60%, every other metric is borrowed from a marketplace that doesn't actually work yet.

### How to measure match liquidity

For each demand-side session:

1. Capture the user's stated constraints (specialty, location, time, price, etc.).
2. Count the supply options that fully match those constraints.
3. Liquidity rate = % of sessions with 3+ matches.

Segment by constraint dimension to find where liquidity breaks. Often it's one specific constraint (insurance acceptance, evening availability, specific specialty) creating most of the churn.

---

## 3. Supply vs. demand: which side first?

Almost always: **start with the constrained side.**

For most marketplaces, supply is constrained (it requires specific qualifications, inventory, capacity, or willingness to sell). Demand can be generated with paid acquisition. Supply usually cannot.

| Marketplace type | Constrained side (start here) | Why |
|------------------|-------------------------------|-----|
| Healthcare (therapists, doctors) | Supply (providers) | Licensure, credentialing, capacity |
| Home services (cleaners, plumbers) | Supply (workers) | Local concentration, trust, vetting |
| Freelance work (designers, devs) | Demand (clients) | Workers are abundant on existing platforms |
| Rentals (Airbnb-like) | Supply (hosts) | Asset ownership required |
| Local food (restaurants delivery) | Supply (restaurants) | Geographic concentration |
| Consumer goods (eBay-like) | Demand (buyers) | Sellers are abundant; need to prove the buyer audience |

When **demand** is the constrained side (rarer, but real for freelance/consumer goods), the playbook flips: build a demand audience first (content, community, paid acquisition) and then onboard supply to serve them.

### "Build supply first" tactics

The standard supply-side cold-start moves:

1. **Manual onboarding at extreme cost.** Founders personally recruit, vet, and onboard the first 20–100 suppliers. Cost per supplier acquisition can be $500–$5000 at this stage; that's fine because each supplier is worth more than the cost.
2. **Concierge service.** Manually match the first dozen demand-side users to supply, before any matching system exists. Builds the dataset for automated matching later.
3. **Acquire from adjacent platforms.** Cold outreach to supply listed on Yelp, LinkedIn, ZocDoc, etc. Open with a clear value prop ("you'll get patients matching your specialty without paying to be listed").
4. **Become a tool for the supply side first.** Give suppliers value even when there's no demand — scheduling, payments, client management. This is "single-player mode" (see next section).

### "Build demand first" tactics (when demand is constrained)

1. **Build the demand audience before the marketplace exists.** Content, community, email list, newsletter. Prove you can reach demand before promising it to supply.
2. **Run the marketplace manually for the first cohort.** Match demand to supply by hand. Validate the match works before automating.
3. **Use scarcity / curation as a marketing angle.** "Hand-picked X" or "exclusive access to Y" reframes low supply as a feature.

---

## 4. Single-player mode

**The most important pattern in marketplace strategy.**

The idea: build a product that gives the constrained side value even when the other side is empty. Then the marketplace emerges as the constrained side's natural network grows.

### Examples

- **OpenTable** started as a reservation management tool for restaurants. The diner-facing marketplace came later, once restaurants were already using the tool.
- **Practice Better, SimplePractice, Headway** built scheduling/billing/notes tools for therapists. Therapists onboarded for the tool. The patient-facing match layer came later.
- **Shopify** started by giving merchants the storefront tool, not by being a marketplace for buyers. (Shopify isn't a marketplace, but the pattern is identical.)
- **DoorDash** started by giving restaurants logistics for their existing delivery orders before building demand-side discovery.

### Why it works

Single-player mode solves the cold-start problem by giving the constrained side standalone value. Supply onboards because the tool is useful, not because of demand promises. Then as supply scales, demand emerges naturally from supply's own networks (patients refer to therapists who use the platform, restaurants tell diners to book through OpenTable).

### How to design single-player mode

Ask: what's the standalone tool the constrained side would pay for, marketplace or no marketplace?

For therapy: scheduling, billing, intake forms, notes, insurance handling. For local services: scheduling, invoicing, customer management. For freelancers: portfolio hosting, proposal templates, contracts, payments. For restaurants: reservations, table management, customer database.

Build that. Charge for it (or give it free as a wedge). Marketplace dynamics follow naturally as you scale supply usage.

---

## 5. Two parallel funnels

Once liquidity is achieved (or while building toward it), the marketplace funnel structure has two sides:

### Supply funnel

```
Discovery → Signup → Profile complete → First match → Active (taking orders/clients)
```

Key stages and metrics:

- **Discovery → Signup:** marketing-driven. Outbound, content, partnerships.
- **Signup → Profile complete:** onboarding quality. Aim for >70% completion. Lower = friction problem.
- **Profile complete → First match:** depends on demand-side liquidity. If this is slow, the marketplace isn't yet viable for this supplier.
- **First match → Active:** the activation metric for supply. Defined as: completed N transactions in M days.
- **Active → Long-term active:** retention. Highly correlated with earnings/value received.

### Demand funnel

```
Awareness → Visit → Search/assessment → Match shown → Booked/transacted → Repeat
```

Key stages and metrics:

- **Awareness → Visit:** marketing acquisition. Same playbook as any SaaS/DTC.
- **Visit → Search:** product friction. Should be near-instant.
- **Search → Match shown:** this is where liquidity manifests. A bad search experience or thin supply kills the funnel here.
- **Match shown → Booked:** conversion to transaction. Depends on listing quality, social proof, pricing transparency, ease of booking.
- **Booked → Repeat:** retention. Recurring need (therapy, home services) has different dynamics than one-time (special-event services).

### Where the funnels join

The transaction. Every marketplace funnel funnels into a single common event: the successful match + transaction. Both sides' funnels should be instrumented to track the same transaction event with both supply ID and demand ID attached.

---

## 6. Channel strategy per side

### Supply-side channels

The constrained side. Channels need to be high-touch and high-intent.

1. **Direct outreach / cold outbound.** Almost always the dominant early-stage channel. Personal LinkedIn, cold email, in-person where geographically dense.
2. **Existing platform poaching.** Cold-outreach to supply already listed on competitors. Value prop must be specific (better match quality, lower fees, better tools).
3. **Partnerships with supply aggregators.** Industry associations, supply-side training schools, certification bodies.
4. **Referral programs (supply-to-supply).** Once you have 50+ active suppliers, they know each other. Pay generously for supply referrals.
5. **Content for supply.** Content addressing supply's business problems (how to manage clients, how to price, how to scale). This is a long-term play.

**Avoid:** broad paid ads to supply. Even when LinkedIn or Meta can reach them, the targeting is rarely tight enough at the volumes you need. Direct is cheaper at this scale.

### Demand-side channels

Usually higher-volume, lower-intent. Standard digital-acquisition playbook applies once liquidity is proven.

1. **SEO for high-intent search terms.** "[Specialty] [city]", "[Service] near me" — these queries indicate active demand. Get the SEO right before paid.
2. **Paid search.** Once SEO is producing leads, paid search captures the rest of the high-intent audience.
3. **Paid social.** Works once you have category awareness; brutal as a primary acquisition channel for a new category.
4. **Content / category-creation.** If you're creating a new category (or repositioning an existing one), content becomes critical.
5. **PR and partnerships.** Press coverage, partnerships with adjacent demand-side audiences (parenting communities, employer benefits, insurance plans, etc.).

**Avoid until liquidity proven:** paid demand acquisition at scale. If you spend $50K on Meta ads to drive demand and your match liquidity is 40%, you're paying to churn 60% of the audience and they don't come back.

---

## 7. Marketplace-specific KPIs

In addition to standard funnel metrics, marketplaces should track:

| Metric | Definition | Target / threshold |
|--------|------------|-------------------|
| **Match liquidity** | % of searches with 3+ usable matches | 60% floor; 80% strong |
| **Supply utilization** | % of suppliers transacting per period | 30%+ monthly = healthy |
| **Demand fill rate** | % of demand requests that result in transaction | 25%+ in active categories |
| **Time-to-first-transaction (supply)** | Days from signup to first transaction | <14 days = good supply experience |
| **Take rate** | Marketplace revenue % of GMV | varies wildly: 5–25% typical |
| **Liquidity by segment** | Match liquidity sliced by city, specialty, time-of-day, etc. | identify weak segments |
| **Cross-side network effect strength** | Correlation between supply count and demand conversion | should be strongly positive |
| **Repeat rate (demand)** | % of demand-side users returning within N days | depends on use-case frequency |
| **Disintermediation rate** | % of matched transactions completing off-platform | <5% = healthy; >10% = product problem |

### Disintermediation — the marketplace's existential risk

Once two parties have matched, what stops them from transacting directly off the platform and avoiding your take rate? Disintermediation is the slow death of any marketplace where the transaction can move off-platform.

Defenses (in order of strength):

1. **Payment lock-in.** The platform processes payment; off-platform requires effort and breaks trust mechanisms.
2. **Communication lock-in.** The platform mediates communication until after first transaction.
3. **Trust / dispute mechanisms.** Reviews, ratings, refund guarantees that only apply on-platform.
4. **Ongoing value-add.** Scheduling, reminders, billing, dispute resolution — value beyond the initial match.
5. **Multi-supplier discovery.** Customers come back for the next supplier, not the same one.

The best defense is making the platform genuinely more useful than the off-platform alternative. The worst defense is contractual lock-in (rarely enforceable, breeds resentment).

---

## 8. Common marketplace failure modes

### "Marketplace that's actually a directory"

You list supply but don't facilitate the transaction. No payment, no booking, no quality signals. Demand uses you to find supply, then transacts off-platform. Symptom: high traffic, no take rate. Fix: own the transaction.

### "Liquidity death spiral"

Demand grows faster than supply. Match liquidity drops. Demand churns. You add paid acquisition to replace churned demand. CAC inflates because conversion drops. Eventually unit economics break. Fix: throttle demand growth until supply catches up. Yes, intentionally.

### "Premature geographic expansion"

The wedge city worked. You expand to 10 cities at once. Each city has 30 suppliers (insufficient for liquidity), demand acquisition burns capital, no city achieves the moat. Fix: expand to city N+1 only when city N has reached liquidity targets.

### "Trying to be everything to everyone"

Generic "marketplace for X" with no specialization. Loses to incumbents on every specific use case. Fix: pick a wedge segment and dominate it before broadening.

### "Wrong side first"

Builds demand-side acquisition before supply is in place. Demand arrives, finds nothing, leaves, never returns. Fix: get supply > demand → flip the order if you started wrong.

### "Take-rate too aggressive too early"

Charges 20% take rate before liquidity is proven. Supply churns to competitors. Fix: subsidize supply early (lower or zero take rate) until you're the obvious place to be.

### "No quality signal"

All supply looks equivalent to demand-side users. Demand can't make confident choices. Conversion stalls. Fix: introduce ratings, reviews, vetting badges, or curated lists. Make quality visible.

---

## 9. Output checklist for marketplace funnel work

When the `funnel-frameworks` skill identifies the user has a marketplace, the agent should:

- [ ] Confirm wedge dimensions (geography, specialty, demographic, etc.)
- [ ] Identify the constrained side (supply or demand)
- [ ] Define match liquidity for this specific marketplace, with the constraint dimensions that matter
- [ ] Map TWO parallel funnels (supply + demand), not one
- [ ] Specify supply-side acquisition channels separately from demand-side
- [ ] Flag whether single-player mode is viable as a wedge
- [ ] Identify the disintermediation defense strategy
- [ ] Set liquidity threshold before any major paid acquisition spend

## 10. Anti-patterns specific to marketplace funnel design

- **Single funnel.** Drawing the marketplace as one funnel hides the two-sided dynamic. Always two funnels.
- **GMV as primary KPI.** GMV grows in death spirals; it grows in healthy marketplaces. Use liquidity and unit economics as the primary signals.
- **Same channels for both sides.** Supply and demand rarely respond to the same channels. Don't reuse a single acquisition stack.
- **Skipping the manual phase.** Every marketplace that worked started with manual concierge matching for the first cohort. Trying to automate from day one almost always fails.
- **Equating signups with supply.** A signed-up supplier is not an active supplier. Track active utilization, not registration count.
