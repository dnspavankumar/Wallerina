# Wallerina — The Complete Explainer

**Read this if you need to build a slide deck, write documentation, pitch the project,
review its architecture, or just understand what Wallerina is.**

The document has two halves, and they cover the same system at two depths:

| | For | Contains |
|---|---|---|
| **Part One (§1–19)** | Anyone. No crypto, finance or coding knowledge assumed. | What it is, why it exists, what it does, a slide outline, a glossary |
| **Part Two (§20–33)** | Engineers, architects, reviewers | Full stack, architecture, the quant engine, security, **every AWS service justified (§27)**, and **an architectural decision record of every decision with the alternative it rejected (§31)** |

Part One explains every technical word the first time it appears and ends with a
ready-to-use slide outline you can copy almost word for word.

- **Project name:** Wallerina
- **One-line description:** Wallerina looks at a crypto wallet and tells the owner how
  much of it should be sitting in "safe" crypto right now — and why.
- **Category:** Crypto portfolio risk advisor (advice only — it never moves money)
- **Status:** Built and working locally; preparing for public deployment
- **Document last updated:** 18 September 2026

---

## Table of contents

### Part One — for everyone

1. [The 60-second version](#1-the-60-second-version)
2. [The problem Wallerina solves](#2-the-problem-wallerina-solves)
3. [The core idea, explained with an umbrella](#3-the-core-idea-explained-with-an-umbrella)
4. [Key terms in plain English](#4-key-terms-in-plain-english)
5. [How Wallerina works, step by step](#5-how-wallerina-works-step-by-step)
6. [What the user actually sees](#6-what-the-user-actually-sees)
7. [What makes Wallerina different](#7-what-makes-wallerina-different)
8. [The safety promise](#8-the-safety-promise)
9. [How it is built (non-technical architecture)](#9-how-it-is-built-non-technical-architecture)
10. [The technology stack](#10-the-technology-stack)
11. [Features that already exist](#11-features-that-already-exist)
12. [Features being added next](#12-features-being-added-next)
    - [12.1 Drafts in the UI](#121-feature-a--drafts-in-the-ui)
    - [12.2 Email notifications](#122-feature-b--email-notifications-when-a-draft-is-ready)
    - [12.3 Email accounts and watched wallets](#123-supporting-feature--email-accounts-and-watched-wallets)
13. [Numbers worth quoting](#13-numbers-worth-quoting)
14. [Who it is for](#14-who-it-is-for)
15. [Limitations and honest caveats](#15-limitations-and-honest-caveats)
16. [Frequently asked questions](#16-frequently-asked-questions)
17. [Ready-made slide outline](#17-ready-made-slide-outline)
18. [Taglines and one-liners you can reuse](#18-taglines-and-one-liners-you-can-reuse)
19. [Glossary](#19-glossary)

### Part Two — for technical readers

20. [How to read Part Two](#20-how-to-read-part-two)
21. [The full technology stack, with justifications](#21-the-full-technology-stack-with-justifications)
22. [System architecture in detail](#22-system-architecture-in-detail)
23. [Backend internals](#23-backend-internals)
24. [The quantitative engine](#24-the-quantitative-engine)
25. [The agent pipeline](#25-the-agent-pipeline)
26. [Security architecture](#26-security-architecture)
27. [**AWS services — every service and why**](#27-aws-services--every-service-and-why)
28. [Deployment architecture](#28-deployment-architecture)
29. [Frontend architecture](#29-frontend-architecture)
30. [Testing strategy](#30-testing-strategy)
31. [**Architectural decision record — every decision explained**](#31-architectural-decision-record--every-decision-explained)
32. [Technical design of the upcoming features](#32-technical-design-of-the-upcoming-features)
33. [Known technical debt and honest limits](#33-known-technical-debt-and-honest-limits)

---

## 1. The 60-second version

Imagine you own a bag of crypto coins. Some of them — like Bitcoin or Ethereum — jump
around in price every day. Others — called **stablecoins** — are designed to always be
worth about one US dollar, so they barely move at all.

The question every crypto holder faces is: **how much of my money should be in the
jumpy stuff, and how much should be parked in the steady stuff?**

Most people either guess, pick a fixed split like "70% risky, 30% safe" and never change
it, or panic and sell everything when the news looks bad.

Wallerina answers that question properly, and it re-answers it as the world changes. You
paste in your wallet address, tell Wallerina what you are trying to achieve (grow
aggressively? protect what you have?), and it:

1. reads what you own,
2. measures how risky the market is *right now*,
3. imagines **10,000 different versions of the next few months**,
4. and tells you the split that fits your goal — plus a plain-English explanation.

It never touches your money. It only advises.

---

## 2. The problem Wallerina solves

Three problems, stacked on top of each other.

**Problem 1 — A portfolio can become risky without you doing anything.**
You buy your coins on a calm Monday. By Friday the market is in turmoil. You did not
change a thing, but the amount of danger you are carrying has doubled. Your portfolio
did not change; **the risk around it did.**

**Problem 2 — Fixed rules go stale.**
The classic advice is a fixed split, like "60% crypto, 40% stable". That is one answer
for every possible market condition, which means it is the wrong answer most of the
time — too cautious in calm markets, too reckless in stormy ones.

**Problem 3 — The information exists, but nobody can process it.**
Price history, volatility data, and betting-market odds on real-world events are all
publicly available. Reading all of it, doing the maths, and turning it into a decision is
far beyond what a person can do by hand, every day, for free.

Wallerina exists to do that work continuously and hand back one clear answer.

---

## 3. The core idea, explained with an umbrella

Think of stablecoins as an umbrella.

- Carrying a huge umbrella everywhere, all year, is safe but annoying — you also never
  enjoy the sunshine. (That's holding everything in stablecoins: no losses, but no gains.)
- Never carrying one is fun until it pours. (That's holding everything in volatile crypto.)
- A sensible person checks the forecast each morning and decides **how big an umbrella to
  bring today.**

Wallerina is the morning forecast check. It doesn't claim to know whether it will rain.
It looks at the clouds, the humidity, and what the bookmakers think, and tells you how
big an umbrella today deserves.

### The same idea with actual numbers

Say a portfolio holds **$10,000** and the volatile crypto in it drops 40%.

| Setup | What happens | Ending value |
|---|---|---|
| 100% volatile crypto | All $10,000 falls 40% | **$6,000** |
| 60% crypto / 40% stablecoins | $6,000 falls 40% → $3,600; $4,000 stays $4,000 | **$7,600** |

Stablecoins do not eliminate the loss. They mean **less of your money was standing in the
rain**. The hard part is knowing how much cover today calls for — and that is the exact
question Wallerina answers.

> These figures are illustrative examples for explaining the concept. Wallerina is not
> financial advice.

---

## 4. Key terms in plain English

You need roughly six words to understand the whole project.

| Term | Plain meaning |
|---|---|
| **Wallet** | A crypto account. Its address is a public string like `0x3f5c…a91b`. Anyone can look up what a wallet holds — it's public, like a house number on a street. |
| **Volatile crypto** | Coins whose price swings a lot: Bitcoin, Ethereum, and most others. Upside and downside both. |
| **Stablecoin** | A crypto coin engineered to stay worth about $1. Used as a shelter — it's still crypto, so it can be moved and traded instantly, but it doesn't swing. |
| **Allocation** | The split. "65% volatile / 35% stable" is an allocation. |
| **Rebalance** | Changing that split by swapping some coins for others. |
| **Prediction market** | A website where people bet real money on real-world events ("Will interest rates be cut in March?"). The betting odds act as a live, crowd-sourced probability, updated continuously, backed by people with money at stake. |

Two more that appear on the product's own screens:

| Term | Plain meaning |
|---|---|
| **Volatility** | How much something bounces around. High volatility = wild swings. |
| **Monte Carlo simulation** | Rolling the dice thousands of times to see the range of outcomes. Named after the casino. Instead of guessing *one* future, you generate 10,000 of them and look at the spread. |

---

## 5. How Wallerina works, step by step

Wallerina combines three perspectives and then makes one decision.

```
 ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
 │ 1. YOUR      │   │ 2. THE       │   │ 3. YOUR      │
 │    WALLET    │   │    MARKET    │   │    GOAL      │
 │              │   │              │   │              │
 │ what you own │   │ how stormy   │   │ what you're  │
 │ right now    │   │ it is today  │   │ trying to do │
 └──────┬───────┘   └──────┬───────┘   └──────┬───────┘
        └──────────────────┼──────────────────┘
                           ▼
                ┌──────────────────────┐
                │  10,000 SIMULATED    │
                │  POSSIBLE FUTURES    │
                └──────────┬───────────┘
                           ▼
                ┌──────────────────────┐
                │  RECOMMENDED SPLIT   │
                │  + plain-English     │
                │    explanation       │
                └──────────────────────┘
```

### Step 1 — Read the wallet

Wallerina looks up the wallet's public holdings across several blockchain networks. It
sorts every coin into **volatile**, **stable**, or **unknown**.

An important detail worth mentioning in any technical audience: it identifies coins by
their **contract address** (their permanent ID number), not their name. Fake coins can
call themselves "USDC" to trick software. Wallerina checks the ID, and anything it does
not recognise it labels `unknown` rather than guessing.

### Step 2 — Measure the market

Two sources feed in:

- **History:** how much each coin has actually bounced around recently.
- **Prediction markets (Polymarket and Kalshi):** live odds on real-world events. If the
  crowd suddenly prices a big event as much more likely, that shows up as a warning
  signal *before* it shows up in price history.

These are treated as **signals about uncertainty**, not as price forecasts. Wallerina
never claims "Bitcoin will go up."

### Step 3 — Understand the goal

The user picks a goal — for example *preserve capital*, *steady growth*, or *aggressive
growth* — or types their own in free text ("I want to buy a house in two years and can't
afford to lose more than 15%").

The goal changes the answer. A cautious goal and a bold goal looking at the same market
should receive different recommendations, and they do.

### Step 4 — Simulate 10,000 futures

Rather than betting on one prediction, Wallerina generates thousands of possible paths
the market could take over the chosen horizon — good, bad, and boring — and looks at the
**whole distribution**: how bad is a typical bad outcome? How bad is a really bad one?

Crucially, it simulates the portfolio **as it is held today** and **as it would be at the
recommended split**, using the identical set of dice rolls. That's how it can say "this
change removes roughly this much downside" honestly — same dice, different portfolio.

### Step 5 — Decide, then explain

A **deterministic engine** — plain, auditable maths with no AI involved — produces the
recommended stablecoin percentage and lists the named reasons that drove it.

Only *after* that does an AI language model get involved, and only to write the
explanation in readable English. The model is given the numbers; it does not produce them.

### Step 6 — The grounding gate (the honesty check)

This is one of the best things to put on a slide.

AI models sometimes invent numbers. So after the model writes its explanation, Wallerina
**re-reads the text, pulls out every percentage and dollar figure, and checks each one
against the real calculated numbers.** If anything doesn't match, the AI's text is thrown
away and a plain, machine-generated write-up is shown instead.

```
   AI writes the explanation
             │
             ▼
   Extract every % and $ in the text
             │
             ▼
   Do they all match the real engine numbers?
        │                    │
      YES                   NO
        │                    │
        ▼                    ▼
    Show it        Discard it, show the
                   safe machine version
```

**A made-up number cannot reach the user.** That is a rule enforced by code, not a hope.

---

## 6. What the user actually sees

The app is a website with a sidebar. Each section answers one question.

| Section | The question it answers |
|---|---|
| **Dashboard** | "How am I doing overall, and what should I do?" — headline stats, performance over time, the recommended split, and the draft swaps panel. |
| **Portfolio** | "What exactly do I own?" — every holding, across every network, with its classification. |
| **Risk** | "How exposed am I?" — volatility, worst-case measures, which asset contributes most of the risk, and how that has changed over time. |
| **Simulations** | "What could happen?" — run your own Monte Carlo with your own settings and horizon. |
| **Recommendations** | "What should I change, and why?" — the target split, the named drivers behind it, and the written reasoning. |
| **Chat** | "Can I just ask?" — a conversational assistant that answers questions about *your* portfolio, and can run a what-if simulation when asked. |
| **Settings** | "What am I aiming for?" — pick or write your goal. |

### The typical first-time journey

```
Land on the site
      ↓
Connect wallet (or paste any public address)
      ↓
Pick a goal — "protect what I have"
      ↓
Wallerina analyses: holdings → risk → 10,000 simulations
      ↓
See the recommendation:  "Now 25% stable → target 45% stable"
      ↓
Read why:  "volatility up, event risk elevated, goal is conservative"
      ↓
Press "Draft swaps" to see exactly which trades that means
      ↓
Decide for yourself. Wallerina never acts.
```

---

## 7. What makes Wallerina different

Five points. These work well as a single slide.

1. **It adapts instead of using a fixed rule.** The recommendation changes as the world
   changes, not on a calendar.
2. **It uses real-world event odds.** Prediction-market probabilities bring in
   information that price charts alone don't have yet.
3. **The maths decides; the AI only writes.** Every number comes from auditable code. The
   language model is a translator, not a decision-maker.
4. **Invented numbers are blocked automatically.** The grounding gate checks the AI's
   output against reality before anyone sees it.
5. **It never touches your money.** No keys, no trades, no custody. Ever.

---

## 8. The safety promise

Worth its own slide, in big text.

> **Wallerina never holds your keys, never signs a transaction, and never moves a single
> coin — for you or for anyone.**

What that means concretely:

- Reading a wallet needs **no permission and no password** — holdings are public
  information, like a property record. Looking at an address is invisible to its owner.
- The "draft swaps" feature produces a **description** of trades. It is a plan on paper.
  Nothing is submitted anywhere.
- If a user ever wanted to act on a draft, they would do it themselves in their own
  wallet software, reviewing and approving every step with their own hands.
- To *change* anything stored about a wallet (like saving a goal), the user must prove
  they own it by signing a message with their wallet — a cryptographic signature, not a
  password Wallerina stores.

**In short: Wallerina is an advisor, not a broker.**

---

## 9. How it is built (non-technical architecture)

Three pieces, like a restaurant. *(Technical readers: §22 has the real topology.)*

```
  ┌────────────────────────────────────────────────────┐
  │  THE DINING ROOM  —  the website                   │
  │  What the user sees and clicks. Charts, tables,     │
  │  buttons. Runs in the browser.                      │
  └───────────────────────┬────────────────────────────┘
                          │ asks for answers
                          ▼
  ┌────────────────────────────────────────────────────┐
  │  THE KITCHEN  —  the backend service                │
  │  Does all the thinking: fetches data, runs the      │
  │  maths, coordinates the AI agents, decides.         │
  └───────────────────────┬────────────────────────────┘
                          │ fetches ingredients
                          ▼
  ┌────────────────────────────────────────────────────┐
  │  THE SUPPLIERS  —  outside data sources             │
  │  Wallet balances and prices, prediction-market       │
  │  odds, swap price quotes, the AI model.             │
  └────────────────────────────────────────────────────┘

  Alongside all three:
  ┌────────────────────────────────────────────────────┐
  │  THE STOREROOM  —  cloud infrastructure (AWS)       │
  │  Remembers history, caches data so the same work    │
  │  isn't repeated, runs heavy jobs in the background, │
  │  and raises an alarm when something breaks.         │
  └────────────────────────────────────────────────────┘
```

### The "agent pipeline" — a team of specialists

When a recommendation is requested, the work is split across a small team, several of
whom work simultaneously:

| Specialist | Its job |
|---|---|
| **Goal reader** | Turns the user's goal into concrete rules (how much loss is acceptable?). |
| **Data gatherer** | Fetches balances, prices and market odds. The only one allowed to retry, because outside services are unreliable. |
| **Simulator** | Rolls the 10,000 futures. |
| **Allocator** | Decides the target stablecoin percentage. Pure maths. |
| **Wallet analyst** | Comments on what the wallet itself looks like. |
| **Market analyst** | Comments on current conditions. |
| **Stablecoin analyst** | Comments on which shelters are actually safe right now. |
| **Rebalance planner** | Works out which trades the change implies. |
| **Explainer** | The only one that writes prose. Then the grounding gate checks it. |
| **Recorder** | Files the recommendation *together with the inputs that produced it*, so any past recommendation can be audited later. |

### Designed to degrade, not to break

Every outside dependency has a defined fallback. If the AI service is unavailable,
recommendations still ship with a machine-written explanation. If a prediction market is
down, the risk estimate falls back to price history alone. If the entire cloud layer is
absent, the app still runs — it just doesn't remember history. **The product does not
have a single point of failure that produces a blank screen.**

---

## 10. The technology stack

For the one slide where an audience wants to see the tools. Each row has a plain-English
"why it matters". *(Technical readers: §21 gives the same stack with the alternatives that
were rejected and why.)*

| Layer | What is used | Why it matters |
|---|---|---|
| Website | Next.js 15, React 19 | Modern, fast, industry-standard web framework |
| Backend | FastAPI (Python 3.12) | Fast, well-documented API service |
| AI orchestration | LangGraph | Coordinates the team of specialist agents |
| AI model | NVIDIA NIM (hosted open models) | Writes the explanations; no data goes to OpenAI |
| Maths engine | NumPy | Industry-standard scientific computing; runs the simulations |
| Wallet & price data | Alchemy | Reads public blockchain balances and price history |
| Event probabilities | Polymarket, Kalshi | Live real-world odds; Kalshi is US-regulated |
| Swap pricing | 0x | Produces realistic trade descriptions |
| Database | Aurora PostgreSQL | Stores history, goals and past recommendations |
| File storage & queues | Amazon S3, SQS | Caches market data; queues heavy simulation jobs |
| Hosting | AWS (ECS Fargate, Lambda, CloudFront) + Vercel | Runs the service and delivers the site securely |
| Monitoring | Amazon CloudWatch | Logs and alarms when something goes wrong |

---

## 11. Features that already exist

Everything in this list is **built and working**.

**Analysis**
- 👉 **Wallet scan across multiple networks** — finds holdings wherever they sit, filters
  out spam tokens, and classifies each coin by its permanent ID rather than its name.
- 👉 **Risk analysis** — volatility, worst-case loss measures, which asset contributes the
  most risk, and how the holdings move together.
- 👉 **Monte Carlo simulation** — 10,000 possible futures, shown as a fan chart and a
  distribution of outcomes. Large runs are queued in the background so the app stays fast.
- 👉 **Market-implied volatility** — reads prediction-market odds on price levels and works
  backwards to the level of uncertainty the crowd is pricing in, then blends it with
  historical data based on how well it fits.
- 👉 **Performance history** — both *recorded* history (real value over time, captured every
  five minutes) and *backfilled* history (today's holdings valued at past prices, which is
  available instantly for any wallet).

**Recommendations**
- 👉 **Dynamic stablecoin allocation** — a target split that moves with conditions instead
  of a fixed ratio.
- 👉 **Goal-aware advice** — presets, or free text interpreted by the goal agent.
- 👉 **Transparent reasoning** — the named drivers behind each recommendation, in English.
- 👉 **Grounding gate** — invented numbers are automatically blocked.
- 👉 **Risk-aware stablecoin selection** — stablecoins are not assumed to be equally safe.
- 👉 **Audit trail** — every recommendation is stored with the inputs that produced it.

**Interaction**
- 👉 **Draft swaps panel** — turns a recommendation into the concrete same-network swaps it
  implies, clearly labelled as drafts.
- 👉 **Portfolio chat** — ask questions in plain language; the assistant can run a what-if
  simulation, so its only route to a new number is to ask the engine for it.
- 👉 **Wallet sign-in** — prove ownership by signing a message, no password anywhere.

**Operations**
- 👉 **Background refresh every 5 minutes** — market data, prediction odds, and wallet
  snapshots.
- 👉 **Production hardening** — rate limiting, strict origin checks, startup safety checks.
- 👉 **Graceful degradation** — defined fallback behaviour for every external dependency.

---

## 12. Features being added next

Two headline features, plus the account system that makes the second one possible.

The theme connecting them: **today Wallerina answers when you ask. Next, it tells you
when something has changed — even when you aren't looking.**

### 12.1 Feature A — Drafts in the UI

**What it is in one sentence:**
A dedicated place in the app where a recommendation is turned into the exact list of
trades it implies — "sell this, buy that, this much, here's why" — and kept around so you
can come back to it.

**Why it matters:**
A recommendation like *"move from 25% stable to 45% stable"* is still homework. The user
has to work out which coins to sell, on which network, and in what amount. A draft does
that arithmetic and turns the advice into something concrete and checkable.

**What a draft contains:**

| Column | What it shows |
|---|---|
| Network | Which blockchain the swap would happen on |
| Sell | Which coin and how much of it |
| Value | What that's worth in dollars |
| Swap into | Which stablecoin it would become |
| Why | The reason this particular leg exists |

Plus a summary line: current stablecoin share, target share, number of swaps, total
dollar value, when it was drafted, and which goal it was drafted for.

**What it deliberately does *not* do:**
No signing. No sending. No execution. The panel carries the permanent label
*"Drafts only · Wallerina never signs, sends or executes anything."*

**Where it stands today:**

| Piece | Status |
|---|---|
| Draft swaps panel on the dashboard | ✅ Built |
| Works for any wallet, no sign-in needed | ✅ Built |
| "Drafts only" labelling throughout | ✅ Built |
| Sensible handling of tiny or impossible swaps | ✅ Built — trades too small to be worth the fees are suppressed, and the reason is shown |
| Real-wallet testing across every awkward case | ⏳ In progress |
| Saved draft history you can return to | 🔜 Planned |
| Draft change detection (what's different since last time) | 🔜 Planned — also the trigger for emails |

**The clever detail worth mentioning:** a swap that is too small is *not* drafted. Below
roughly $5 — and after reserving about $25 on Ethereum to pay network fees — a trade
costs more to make than it moves. Wallerina suppresses it and tells the user why, rather
than suggesting a trade that loses money by existing.

---

### 12.2 Feature B — Email notifications when a draft is ready

**What it is in one sentence:**
Wallerina watches the wallets you care about in the background and emails you when its
advice has meaningfully changed — so you find out that your portfolio drifted off-target
without having to check the app.

**Why it matters:**
This is the difference between a tool you remember to open and a service that looks after
you. Risk builds up quietly. The moment you most need the advice is exactly the moment
you are least likely to be logged in.

**How it will work:**

```
Every few minutes, in the background
            ↓
For each wallet a user is watching:
  build a fresh draft
            ↓
Compare it to the last one sent
            ↓
   Has it meaningfully changed,
   AND is a rebalance actually needed?
        │                 │
       NO                YES
        │                 │
        ▼                 ▼
   stay silent      send one email
                            ↓
                    at most one per wallet
                    per day, several wallets
                    combined into one digest
```

**What the email will contain:**
- The wallet (shortened, e.g. `0x3f5c…a91b`)
- The goal it was assessed against
- Current stablecoin share vs the recommended target
- The drafted swaps: sell → buy, dollar value, and the reason for each
- A link straight to the dashboard
- The line **"Wallerina never executes trades"**
- A one-click unsubscribe link

**The design rules behind it** (these are the parts that make it a good product rather
than a spam machine):

| Rule | Why |
|---|---|
| **Only email on genuine change** | A draft that is the same as yesterday's is not news. Wallerina stores a fingerprint of the last draft and stays quiet unless it actually moved. |
| **Only when a rebalance is genuinely needed** | No email just to say "you're fine". |
| **At most one email per wallet per day** | Several wallets changing on the same day are combined into a single digest rather than several emails. |
| **One-click unsubscribe, plus a per-wallet switch** | Turn off everything, or just one wallet. No hunting through settings. |
| **Bounces and complaints turn notifications off automatically** | If an address is dead or a user marks a message as spam, Wallerina stops sending — protecting both the user and the service's ability to deliver mail at all. |
| **A hard ceiling on background work** | Producing a draft is genuinely expensive — it runs the full analysis pipeline. Unchanged portfolios are skipped and there is a cap on how much work each cycle may do, so the system cannot quietly run up an enormous bill. |

**What has to happen first:** sending email from a cloud provider requires approval.
Until that is granted, mail can only be sent to pre-verified addresses, so the approval
request is being filed ahead of the work that depends on it.

---

### 12.3 Supporting feature — Email accounts and watched wallets

**Why it's needed:** today the only way to sign in is with a crypto wallet, which only
works for wallets you personally own. To *email* someone, Wallerina needs an email
address — so it needs a lightweight account system.

**How it will work:**
- **No passwords at all.** You enter your email, receive a one-time code or magic link,
  and you're in. Nothing to forget, nothing for Wallerina to leak.
- **Watch any address.** Since holdings are public, you can watch any wallet — your own,
  a cold-storage wallet, or one you simply want to track — and choose per wallet whether
  it should notify you.
- **Wallet sign-in stays.** You can link wallets you own; watching a public address needs
  no proof of ownership.

**The security rules being applied:**
- Codes expire after about ten minutes and can only be used once
- A limited number of guesses before the code is void
- Request limits per email address and per source, to stop brute-force attempts
- The response is identical whether or not an account exists, so the system cannot be used
  to discover who has signed up
- Only a scrambled version of the code is ever stored — never the code itself

**UI impact:** deliberately minimal. A sign-in screen, and a "watch this wallet" toggle.
Nothing else in the app changes.

---

## 13. Numbers worth quoting

Useful when a slide needs a figure.

| Number | What it is |
|---|---|
| **10,000** | Simulated futures behind every recommendation |
| **~46** | Price levels read from a single prediction-market event to infer market-implied uncertainty |
| **5 minutes** | How often market data, event odds and wallet snapshots refresh in the background |
| **312** | Automated tests in the suite, all passing |
| **26** | API endpoints in the backend service |
| **3** | Analysis specialists that run in parallel on every recommendation |
| **2** | Steps in the whole pipeline that involve an AI model — both with a non-AI fallback |
| **0** | Transactions Wallerina has ever signed or sent |

---

## 14. Who it is for

| Audience | What they get from it |
|---|---|
| **The everyday crypto holder** | A straight answer to "should I be worried right now?" without needing to learn finance. |
| **The disciplined investor** | A systematic, repeatable process instead of reacting to headlines. |
| **The multi-wallet user** | One place to see total exposure across several wallets and networks. |
| **The curious analyst** | Full visibility into the reasoning, the drivers, and the simulation behind every recommendation. |

---

## 15. Limitations and honest caveats

Including these builds credibility. Leaving them out invites the questions anyway.

- **It is not financial advice.** It is an analysis tool. Every decision stays with the user.
- **It does not predict prices.** By design, the simulation assumes no built-in upward or
  downward drift, because estimating direction from short crypto history mostly measures
  noise. It models *uncertainty*, not direction.
- **Prediction-market odds are signals, not truths.** They reflect what a crowd with money
  at stake believes, which is useful and often wrong.
- **Stablecoins are not risk-free.** They can lose their peg. Wallerina treats their
  stability as something to assess, not to assume.
- **It depends on outside data providers.** When one is unavailable the answer becomes less
  precise — the system says so rather than hiding it.
- **Unknown tokens are labelled unknown.** Wallerina counts them as volatile for safety
  rather than guessing what they are.

---

## 16. Frequently asked questions

**Can Wallerina steal my crypto?**
No. It never receives your keys and has no mechanism to move funds. It reads public
information, the same way anyone can look up a public address.

**Do I have to connect my wallet?**
No. You can paste any public address and get a full analysis. Connecting is only needed to
*save* settings like your goal.

**Does it place trades for me?**
No. It produces drafts — descriptions of trades. Acting on them is entirely manual, done
by the user in their own wallet software.

**What's the difference between this and a robo-advisor?**
A robo-advisor manages your money. Wallerina advises and hands the decision back to you.

**Is my data sent to OpenAI?**
No. The AI model used is hosted by NVIDIA. (The OpenAI software library appears in the
code, but only as a standard way of talking to any model service — no data goes to OpenAI.)

**How does it avoid the AI making things up?**
The AI never produces numbers — the maths engine does. And every figure in the AI's text
is checked against the real numbers before the user sees it; anything that doesn't match
means the whole explanation is discarded.

**Why stablecoins rather than cashing out to dollars?**
Because cashing out means leaving crypto entirely — slow, often taxable, and hard to
reverse quickly. Stablecoins give you shelter while staying inside the system, so you can
step back in the moment it makes sense.

**How often should I check it?**
Today, whenever you want. Once email notifications ship — you won't have to. It'll tell you.

---

## 17. Ready-made slide outline

A 12-slide deck. Each slide lists its headline, the content to put on it, and the section
of this document to draw from.

| # | Slide | What goes on it | Source |
|---|---|---|---|
| 1 | **Wallerina** | Logo, and the line *"Dynamic crypto portfolio risk management"* | §1 |
| 2 | **The problem** | "Your portfolio didn't change. The risk around it did." Three stacked problems. | §2 |
| 3 | **The umbrella** | The umbrella analogy + the $10,000 table | §3 |
| 4 | **The question we answer** | *"Given what we know right now, how much uncertainty can my portfolio afford?"* | §3 |
| 5 | **How it works** | The three-inputs → 10,000 futures → recommendation diagram | §5 |
| 6 | **10,000 futures** | Explain Monte Carlo; same dice, two portfolios | §5, step 4 |
| 7 | **The maths decides, the AI explains** | The grounding-gate diagram. Strong slide. | §5, step 6 |
| 8 | **The product** | Screenshots of Dashboard / Risk / Recommendations / Chat | §6 |
| 9 | **Safety** | One big line: *never holds keys, never signs, never trades* | §8 |
| 10 | **What's built** | The feature list, grouped | §11 |
| 11 | **What's next** | Drafts in the UI + email notifications, side by side | §12 |
| 12 | **Why it's different** | The five differentiators | §7 |

*Optional extra slides:* the architecture picture (§9), the tech stack table (§10), the
numbers (§13), the honest limitations (§15).

**Presenter tips**
- Lead with the umbrella. Non-technical rooms understand it instantly and everything else
  hangs off it.
- The grounding gate is the single most impressive technical idea to a general audience —
  give it a full slide and say the sentence *"a made-up number physically cannot reach the
  user"* out loud.
- Always say "advice only, never trades" before anyone can ask. It turns the obvious
  worry into a design feature.
- Don't read the tech stack table aloud. Leave it on screen and say "standard, boring,
  proven tools — the interesting part is what we do with them."

---

## 18. Taglines and one-liners you can reuse

- **Dynamic crypto portfolio risk management.**
- Not prediction. Not panic. Not a fixed ratio. **Adaptive risk management.**
- The goal isn't to predict the market. **It's to understand your exposure to it.**
- Your portfolio didn't change. **The risk around it did.**
- Given what we know right now, **how much uncertainty can my portfolio afford?**
- The maths decides. **The model only explains.**
- Ten thousand futures, **one clear answer.**
- **Advice, not custody.** Wallerina never holds your keys.
- We don't check the forecast for you. **We tell you how big an umbrella today deserves.**

---

## 19. Glossary

| Term | Meaning |
|---|---|
| **Agent** | A specialist component in the pipeline with one job (read the goal, analyse the market, write the explanation). |
| **Allocation** | The split between volatile crypto and stablecoins. |
| **API** | The connection between the website and the backend "kitchen" that does the thinking. |
| **Backend** | The part of the software the user never sees, where the work happens. |
| **Blockchain network** | One of several parallel crypto systems (Ethereum, Base, Arbitrum…). A wallet can hold coins on many at once. |
| **Contract address** | A coin's permanent ID number. Unlike a name, it can't be faked. |
| **Deterministic** | Same inputs always give the same output. No randomness, no AI, fully auditable. |
| **Drawdown** | How far a portfolio falls from its peak — the "how much did I lose from the top" number. |
| **Draft (draft swap)** | A written plan of trades. Not an order; nothing is submitted. |
| **Frontend** | The website the user sees and clicks. |
| **Gas** | The fee paid to a blockchain network to process a transaction. |
| **Grounding gate** | The check that every number in the AI's text matches the real calculated numbers. |
| **Monte Carlo simulation** | Generating thousands of random possible futures to see the range of outcomes. |
| **Prediction market** | A market where people bet on real-world events; the prices act as live probabilities. |
| **Rebalance** | Adjusting the split back toward its target. |
| **Stablecoin** | A crypto coin designed to hold a steady value, usually about $1. |
| **Swap** | Trading one coin directly for another. |
| **VaR / CVaR** | *Value at Risk* — a bad-day threshold ("on the worst 5% of days, you'd lose at least this much"). *Conditional VaR* — the average loss when you're in that worst 5%. |
| **Volatility** | How much a price bounces around. |
| **Wallet** | A crypto account, identified by a public address. |
| **Watched wallet** | A wallet a user has asked Wallerina to keep an eye on for notifications. |

---

*Developer-facing notes — session history, deployment decisions, and outstanding
engineering tasks — live in `progress.md`, `todo.md`, and
`docs/dev-context-2026-09-13.md`. This file is the explanatory one.*

---
---

# PART TWO — THE TECHNICAL DOCUMENT

*Everything above is written for a general audience. Everything below is written for
engineers, architects, reviewers and anyone who has to defend a design decision in a
technical Q&A.*

**Sections 20–33.**

| # | Section |
|---|---|
| 20 | [How to read Part Two](#20-how-to-read-part-two) |
| 21 | [The full technology stack, with justifications](#21-the-full-technology-stack-with-justifications) |
| 22 | [System architecture in detail](#22-system-architecture-in-detail) |
| 23 | [Backend internals](#23-backend-internals) |
| 24 | [The quantitative engine](#24-the-quantitative-engine) |
| 25 | [The agent pipeline](#25-the-agent-pipeline) |
| 26 | [Security architecture](#26-security-architecture) |
| 27 | [**AWS services — every service and why**](#27-aws-services--every-service-and-why) |
| 28 | [Deployment architecture](#28-deployment-architecture) |
| 29 | [Frontend architecture](#29-frontend-architecture) |
| 30 | [Testing strategy](#30-testing-strategy) |
| 31 | [**Architectural decision record — every decision explained**](#31-architectural-decision-record--every-decision-explained) |
| 32 | [Technical design of the upcoming features](#32-technical-design-of-the-upcoming-features) |
| 33 | [Known technical debt and honest limits](#33-known-technical-debt-and-honest-limits) |

---

## 20. How to read Part Two

There is one sentence that explains more of this codebase than any other:

> **Deterministic code produces every number. The language model only reads intent and
> writes prose.**

Almost every non-obvious decision in the system is downstream of that rule. Why the quant
package has no framework imports, why the allocation engine is not fault-tolerant while
the analyst agents are, why a grounding gate exists at all, why the chat assistant is given
a tool instead of a bigger prompt — all of it follows from refusing to let a probabilistic
component emit a figure a user might act on.

The second organising rule is:

> **Every piece of infrastructure is optional, and its absence has a defined behaviour.**

The application runs end to end with no AWS account, no database, no model key and no
prediction-market access. Each of those removals degrades one specific capability and
nothing else. That is a deliberate architectural property, not an accident of incremental
development — see §27 and ADR-21.

---

## 21. The full technology stack, with justifications

### 21.1 Frontend

| Component | Choice | Why this, and not the obvious alternative |
|---|---|---|
| Framework | **Next.js 15 (App Router)** | Server components for the static shell, client components only where wallet state and charts need them. Vercel deployment is a single command. Alternative rejected: a plain Vite SPA — would have meant hand-rolling routing, layouts and the auth-shell split. |
| UI library | **React 19** | Required by Next 15; `use` and improved transitions matter on pages that stream. |
| Styling | **CSS Modules**, one file per component | Scoped by default, zero runtime, no build-time CSS-in-JS cost, no utility-class sprawl in the markup. Alternative rejected: Tailwind — faster to write, but the charts and panels here are bespoke enough that the class strings become the layout, and readability suffers. |
| Charts | **Hand-written SVG components** (`LineChart`, `FanChart`, `Histogram`, `Donut`, `Matrix`) | A fan chart of 10,000 simulated paths reduced to percentile bands is not a stock chart type; a correlation matrix heatmap isn't either. Wrapping a charting library to produce them costs more than drawing the SVG. Also: no ~100 kB charting dependency on first load. |
| State | **React state + context** (`WalletProvider`) | The app has exactly one piece of genuinely global state — the connected wallet. Redux/Zustand would be ceremony around a single value. |
| Wallet integration | **Raw EIP-1193 provider** (`window.ethereum`) | Connect, read accounts, `personal_sign`. That is the whole surface needed. Alternative rejected: wagmi/RainbowKit — large dependency trees to replace roughly sixty lines. |
| API client | **One typed module** (`lib/api.js`) with `AbortController` throughout | Every fetch is cancellable, so navigating away mid-analysis doesn't leave work running or race a stale response into state. |

### 21.2 Backend

| Component | Choice | Why |
|---|---|---|
| Language | **Python 3.12** | The quant work is NumPy work, and the agent ecosystem (LangGraph) is Python-first. 3.12 specifically for `StrEnum` and the `datetime.UTC` alias used throughout. |
| Package manager | **uv**, with a committed `uv.lock` | Resolution in seconds rather than minutes, and a lockfile that makes the Docker build reproducible. |
| Web framework | **FastAPI + Uvicorn** | Async-native, which matters because a single analysis fans out to 20+ upstream calls. Pydantic models double as the OpenAPI schema, so the API documents itself. |
| Validation | **Pydantic v2** | Every request and response is a typed model. Address and transaction-hash fields carry regex patterns at the schema level, so malformed input is rejected before it reaches a handler. |
| HTTP client | **httpx.AsyncClient**, one pooled instance for the process lifetime | Connection reuse across all providers, one place to set timeouts, and one place to install the DNS override. |
| Agent orchestration | **LangGraph** | The pipeline is a DAG with a genuine parallel fan-out and a per-node retry policy. Expressing that as hand-written `asyncio.gather` calls works right up until you want per-node retries, partial failure and a typed accumulating state — which is exactly what this pipeline needs. |
| Numerics | **NumPy** | Cholesky factorisation, vectorised path generation, percentile extraction. No pandas: the data is already aligned arrays, and pandas would add a heavy dependency for a convenience the code doesn't use. |
| Model access | **NVIDIA NIM** via the `openai` protocol client | See ADR-9. |
| Database driver | **asyncpg** | Async, fast, and supports the per-connection authentication hook the IAM token flow requires. |
| AWS SDK | **boto3**, lazily constructed and LRU-cached per service | Client construction parses botocore's service model, which is slow enough to matter on a request path. |

### 21.3 External data providers

| Provider | Used for | Why chosen |
|---|---|---|
| **Alchemy** | Token balances across four networks, spot prices, price history | One API covers balances *and* prices *and* history across chains. The alternative is stitching an RPC node together with a separate price API and a separate history source. |
| **Polymarket** | Event probabilities, price-threshold markets | The largest crypto-relevant prediction market; deep liquidity on macro and crypto events. |
| **Kalshi** | Price-level strike ladders | CFTC-regulated, and publishes dense strike ladders (~46 strikes on a single BTC event) rather than scattered thresholds — far more information per event for the implied-volatility fit. It is also reachable on networks where Polymarket is DNS-blocked. Market data needs no authentication. |
| **0x Swap API** | Swap quotes and calldata | Aggregates liquidity across DEXes; the AllowanceHolder flow gives an exact-amount allowance pattern that is safe to validate server-side. |

---

## 22. System architecture in detail

### 22.1 Topology

```
Browser (MetaMask, EIP-1193)
   │
   ├─── static assets ──────────────► Vercel (Next.js)
   │
   └─── API calls ─────────────────► CloudFront (HTTPS, no custom domain needed)
                                         │
                                         ▼
                                     ALB  ── security group accepts ONLY the
                                         │    CloudFront origin-facing prefix list
                                         ▼
                                     ECS Fargate service (the API)
                                         │
              ┌──────────────────────────┼──────────────────────────┐
              ▼                          ▼                          ▼
        Upstream providers        AWS data plane             AI model
     Alchemy · Polymarket       S3 · SQS · Aurora        NVIDIA NIM
     Kalshi · 0x                Secrets · CloudWatch

   EventBridge (rate: 5 min) ──► 3 refresh Lambdas ──► S3 + Aurora
   SQS ──► simulation worker Lambda (≤2 concurrent) ──► Aurora
   SQS failures ×3 ──► DLQ ──► CloudWatch alarm ──► SNS email
```

The browser never sends a private key anywhere. Swap calldata is constructed server-side,
validated server-side, and handed back unsigned for the wallet to sign locally.

### 22.2 The layering rule

Dependencies point downward, only:

```
main.py            FastAPI app · 26 routes · middleware
   ↓
agents/            LangGraph pipeline · goal · analysts · judgement · grounding · llm
   ↓
services/          analysis · chat · execution · swap · auth · history · refresh ·
                   worker · cache · http · dns · wallet/ · polymarket/ · kalshi/
   ↓
quant/             risk · monte_carlo · implied · allocation      ← pure NumPy
   ↓
models/ (Pydantic) · assets/registry.py
   ↓
aws/               client · database · storage · queue · secrets · telemetry · handlers
   ↓
core/              config · ratelimit
```

**Nothing in `quant/` imports FastAPI, boto3, httpx or any framework.** That is enforced by
convention and verified by the fact that every quant test constructs arrays directly and
calls functions — there is no fixture, no mock, no event loop. It is the single most
valuable structural property in the codebase: the part that produces the numbers a user
acts on is the part that is trivially testable in isolation.

### 22.3 Request lifecycle for a cold recommendation

```
1.  GET /api/recommendation/0x…
2.  rate-limit middleware  →  sliding 60s window, keyed on the caller's address
3.  CORS middleware        →  origin checked against an explicit allow-list
4.  handler                →  analysis_cache.get_or_compute(key)
5.      cache miss         →  single-flight lock acquired for this wallet
6.          parallel fetch →  balances · prices · Polymarket · Kalshi
7.          store in cache with a 300s TTL
8.  LangGraph invoked      →  goal → data → simulate → {allocate, wallet, market,
                              stablecoin} → rebalance → explain → record
9.  grounding gate         →  accept or discard the model's prose
10. record node            →  INSERT recommendation + the inputs that produced it
11. response               →  target %, drivers, trades, outlook, reasoning
```

Steps 5–7 are where the single-flight lock matters: a full cold analysis is 20+ sequential
provider calls. Three browser tabs opening the dashboard simultaneously trigger **one**
upstream fetch, not three.

---

## 23. Backend internals

### 23.1 The API surface — 26 routes

| Group | Routes |
|---|---|
| Health | `GET /health`, `GET /health/database` |
| Portfolio | `GET /api/portfolio/{address}`, `GET /api/prices/history` |
| Risk | `GET /api/risk/{address}` |
| Markets | `GET /api/prediction-markets`, `GET /api/market-stress` |
| Simulation | `POST /api/simulate`, `GET /api/simulate/jobs/{job_id}`, `POST /api/simulate/scenarios` |
| Analysis | `GET /api/analysis/{address}` |
| Recommendation | `GET /api/recommendation/{address}`, `GET /api/recommendation/{address}/history` |
| Goals | `GET /api/goals/presets`, `GET /api/goal/{address}`, `PUT /api/goal/{address}` |
| History | `GET /api/history/{address}/performance`, `GET /api/history/{address}/risk` |
| Auth | `GET /api/auth/nonce`, `POST /api/auth/verify` |
| Execution | `POST /api/execution/{address}/plan`, `POST …/quote`, `POST …/transactions`, `GET …/transactions/{tx_hash}` |
| Chat | `POST /api/chat` (streams) |
| Ops | `POST /api/refresh/run` (admin-token gated) |

**Auth posture per route is deliberate:** reading is public because on-chain balances are
public; writing stored state (`PUT /api/goal`) and quoting/recording real transactions
require a signed session; `POST /api/execution/{address}/plan` is deliberately public and
read-only, because a draft is a description and requires nothing from the wallet's owner.

### 23.2 Middleware ordering — a subtle but real decision

The rate limiter is registered **before** `CORSMiddleware`, which in FastAPI means CORS
ends up the *outermost* layer. The reason is specific:

> If the rate limiter sat outside CORS, a 429 response would be emitted without CORS
> headers, and the browser would refuse to let the frontend read it. The user would see a
> generic network failure instead of "you are being rate limited, retry in 20 seconds."

Correct error handling requires the error response to still be readable by the client that
caused it.

### 23.3 Rate limiting

- Sliding 60-second window, in-process, per client key, applied only to the expensive
  routes (model calls, Monte Carlo, full wallet scans, auth, execution planning).
- **Client key resolution is layered and explicitly threat-modelled:**
  - Behind CloudFront, the address comes from `CloudFront-Viewer-Address`. The rightmost
    `X-Forwarded-For` hop would be a CloudFront *edge server*, shared by many callers —
    using it would let one visitor exhaust the limit for everyone behind that edge.
  - Behind a bare load balancer, only the **rightmost** `X-Forwarded-For` entry is trusted:
    the balancer appends it, whereas anything to its left was supplied by the client and
    can be forged to dodge the limit.
  - Both are gated behind `TRUST_PROXY_HEADERS`, so headers are never trusted by default.
- Idle clients are pruned once 10,000 are tracked, bounding memory.
- **Acknowledged limit:** the window is per-process, so *N* API tasks permit up to *N*× the
  configured limit globally. A WAF rate rule is the correct place for a hard global ceiling;
  this layer is a per-task cost guard, and the code says so.

### 23.4 Caching

`services/cache.py` — a TTL cache with three properties that matter:

1. **Single-flight per key.** `get_or_compute` takes a per-key `asyncio.Lock` and re-checks
   the cache after acquiring it, so a burst of concurrent requests for one wallet produces
   one upstream fetch.
2. **Bounded.** 256 entries; expired entries are evicted first, then the entry nearest
   expiry. No unbounded memory growth from a scan of many addresses.
3. **Deliberately process-local.** It is a latency cache, not a datastore. Durable state
   belongs in Aurora, and conflating the two produces a cache you are afraid to clear.

### 23.5 Configuration

`pydantic-settings`, one `Settings` class, `@lru_cache`d. Every credential and tunable is an
environment variable; a local `.env` is picked up automatically and **nothing sensitive is
committed**. Three properties worth calling out:

- **`production_problems(settings)`** — a pre-flight check run in the lifespan hook. In
  production the service **refuses to start** if `CORS_ORIGINS` is empty or `*`, or if
  static AWS keys are present (production must use the task role). A misconfiguration that
  would silently weaken security instead becomes a loud, immediate boot failure.
- **Startup order** — Secrets Manager loads *first*, because it may supply the keys
  everything else needs; then production checks; then HTTP pool, DB migration, refresher and
  worker. Shutdown reverses it.
- **Every timeout, threshold and limit is a named setting with a comment explaining the
  number** — why prediction markets get an 8-second timeout (they are an enrichment; analysis
  must not stall on them), why the portfolio scan is capped at 20 pages (heavily airdropped
  wallets return thousands of spam tokens, but results are *not* value-ordered, so too low a
  cap silently hides real positions — hence `scan_truncated` is reported rather than ignored).

### 23.6 Upstream resilience

- **Circuit breakers.** Polymarket and Kalshi each stop being called after 2 consecutive
  failures and stay off for 120 seconds. Without this, every analysis pays the full 8-second
  timeout on every query while a provider is down.
- **DNS-over-HTTPS override** (`services/dns.py`). Some ISPs return a sinkhole address for
  Polymarket's hosts, so system DNS never connects. Selected hosts are resolved over DoH
  against `1.1.1.1` — addressed **by IP**, so the lookup itself does not depend on local DNS
  — and the connection is opened to the resolved address while TLS still uses the original
  hostname for SNI and `Host`. This is a real-world fix for a real-world failure, and it is
  scoped to named hosts rather than applied globally.
- **Retries only where they belong.** In the pipeline, only the `data` node carries a retry
  policy, because it is the only node that talks to flaky upstreams. Retrying a pure
  computation is pointless; retrying an LLM call is handled by its own fallback path.

---

## 24. The quantitative engine

Four modules, pure NumPy, no I/O.

### 24.1 `quant/risk.py`

Conventions, fixed once and applied everywhere:
- Daily **log** returns.
- Volatility annualised with **365 trading days** — crypto trades every day, so the equity
  convention of 252 would understate annualised volatility by ~20%.
- **Losses are positive fractions.** A VaR of `0.12` means a 12% loss. Sign confusion in risk
  code is a classic source of catastrophic bugs; fixing the convention in the module
  docstring and honouring it everywhere removes the class of error.

Produces: log returns, annualised volatility, correlation matrix, VaR, CVaR (expected
shortfall), per-asset risk contribution, and `nearest_positive_definite` — because an
empirical correlation matrix from short, gappy crypto history can fail Cholesky
factorisation, and the honest fix is to project it to the nearest valid matrix rather than
to silently drop assets.

### 24.2 `quant/monte_carlo.py`

Correlated geometric Brownian motion. Four design notes, each defensible in review:

| Decision | Reasoning |
|---|---|
| **Correlated shocks via Cholesky** | A book of five volatile tokens that all move together is far riskier than its position count suggests. Independent draws would hide exactly the risk the product exists to measure. |
| **Zero drift by default** | Under `DriftMode.ZERO` the expected *simple* return is zero, so log drift is `-σ²/2`. Estimating drift from short crypto history mostly measures noise and would turn the simulator into a trend extrapolator — whatever rose recently gets projected to keep rising. Historical and shrunk modes exist for explicit what-if analysis only. |
| **Batched path generation** | Per-asset paths are generated in batches of 2,000 and immediately collapsed into portfolio value paths, so only a `(simulations, horizon+1)` array is retained. A 50,000 × 365 run costs roughly **150 MB instead of multiple gigabytes**. This is what makes large runs affordable on a Lambda at all. |
| **Antithetic sampling** | Every shock is paired with its negative, reducing the standard error of the mean without biasing the distribution. Free variance reduction. |

### 24.3 `quant/implied.py` — the most distinctive piece of the engine

A binary market on a price level is a probability statement about that level. *"Will ETH dip
to $1,000 by 31 Dec 2026?"* at 6.5¢ says the market puts 6.5% on `price ≤ 1000` at that
date. *"Will ETH reach $8,000"* at 2.15¢ gives `1 − p` on the same curve. A family of these on
one asset at one expiry is therefore a **market-implied cumulative distribution** — priced by
people with money at risk.

The module fits the single σ that best reproduces those observed probabilities, weighted by
liquidity, under the same zero-drift convention the simulator uses:

```
P(S_T ≤ K) = Φ( ( ln(K/S₀) + σ²T/2 ) / ( σ√T ) )
```

The fitted σ is then blended into the historical estimate **weighted by fit quality**, so a
noisy or thin market cannot overwhelm a well-measured historical number.

Quality filters, because a bad quote is worse than no quote:
- strikes quoted wider than `KALSHI_MAX_SPREAD` (0.10) are a guess, not a price — dropped
- strikes with open interest below `KALSHI_MIN_OPEN_INTEREST` (100) carry no information — dropped

**What is deliberately *not* claimed** (this candour is itself a design decision, and it is
written into the module docstring):
- It does **not** make the model fat-tailed. A lognormal fitted to market quantiles is still
  a lognormal, and real crypto returns are more extreme.
- It is **risk-neutral, not real-world** — prediction-market prices carry risk premia and fees.

Both caveats are accepted: a better-centred lognormal is an honest improvement, and
pretending otherwise would not be.

For contrast, `compute_market_stress` — the older, simpler signal — averages every downside
probability into one bounded multiplier, so a 2% chance of catastrophe and a 14% chance of a
mild fall become the same input. `implied.py` exists precisely to stop throwing that
information away.

### 24.4 `quant/allocation.py` — the deterministic decision

This module, and only this module, decides the number.

```
base ratio (from the goal)
    + volatility adjustment      (ref 0.55, sensitivity 0.45, capped ±0.22)
    + concentration adjustment   (threshold 0.35, sensitivity 0.30, capped ±0.12)
    + correlation adjustment     (threshold 0.55, sensitivity 0.28, capped ±0.12)
    + market-stress adjustment   (capped ±0.10)
    = target stablecoin ratio, with a ±0.05 acceptable band
```

Three properties make this auditable:

1. **Every adjustment is named, bounded and recorded** on the result as an
   `AllocationDriver`. No single signal can dominate; the explainer never has to re-derive
   the decision because the drivers are handed to it.
2. **The band (±5%)** prevents advice thrash. Without it, a portfolio one percentage point
   off target would be told to rebalance, and the user would pay fees to chase noise.
3. **It is not fault-tolerant, by design.** The analysis agents degrade to placeholders on
   crash; the allocation engine does not, because without a decision there is nothing to
   recommend. Shipping a "recommendation" with a fabricated or defaulted target would be
   worse than an error.

---

## 25. The agent pipeline

### 25.1 Shape

```
START → goal → data → simulate ─┬─► allocate → rebalance ─┐
                                ├─► wallet agent ─────────┤
                                ├─► market agent ─────────┼─► explain → record → END
                                └─► stablecoin agent ─────┘
```

| Node | Deterministic | Failure behaviour | Why it is where it is |
|---|---|---|---|
| `goal` | preset ✅ / free text 🤖 | falls back to deterministic parsing | Runs **first and exactly once**. Its `AgentContext` is written into graph state; no downstream node re-reads the goal or invents thresholds. A preset **must not** reach an LLM at all. |
| `data` | ✅ | retry policy | The only node touching flaky upstreams, so the only one that retries. |
| `simulate` | ✅ | hard failure | Everything downstream needs the draws. |
| `allocate` | ✅ | hard failure | See §24.4 — no decision means no recommendation. |
| `wallet` / `market` / `stablecoin` | ✅ | placeholder report + warning | A commentary crash must not cost the user their recommendation. |
| `rebalance` | ✅ | hard failure | Simulates the book **as held** and **at target on identical draws**, which is what makes "this removes X of downside" an honest claim rather than two unrelated experiments. |
| `explain` | 🤖 | deterministic write-up | The target ratio is written into the output **by code**, never copied from the model's reply. |
| `record` | ✅ | logged, non-fatal | Persists the recommendation **with the inputs that produced it**. |

**Exactly two nodes call a model. Both have deterministic fallbacks.**

### 25.2 The grounding gate

`agents/grounding.py` runs after `explain`:

1. Regex-extract every percentage and dollar figure from the model's prose.
2. Match each against the figures in the brief the model was given.
3. Allow honest rounding — 80.4% written as "80%", $40,700 written as "$40.7k" (1% relative
   tolerance on dollars, precision-aware on percentages) — and ignore sign, since "a 5% drop"
   and "−5%" describe the same figure.
4. Any figure that cannot be matched makes the whole explanation ungrounded, and the
   deterministic write-up ships instead.

The prompt already instructs the model not to invent numbers. The gate exists because
**a prompt is a request, not a guarantee.** This is the difference between a policy and a
control.

### 25.3 Chat

`POST /api/chat` streams. The model is handed the already-computed portfolio snapshot plus
**exactly one tool** — a what-if simulation. Consequence: its only route to a number it
wasn't given is to ask the engine for it. Conversation history is capped
(`CHAT_MAX_HISTORY = 20`) to bound token cost and latency.

---

## 26. Security architecture

### 26.1 Authentication — Sign-In with Ethereum (EIP-4361)

```
GET  /api/auth/nonce      → single-use nonce, 10-minute TTL, stored in auth_nonces
wallet: personal_sign     → EIP-4361 message containing the nonce
POST /api/auth/verify     → parse, validate, recover signer, burn the nonce
                          → HMAC-signed session token (address + expiry), 24h TTL
```

Decisions inside that flow:

- **No passwords exist anywhere**, so there is no password store to breach.
- **Nonces are single-use with a 10-minute TTL**, defeating replay.
- **A 2-minute clock-skew allowance** on `Issued At` / `Not Before`, because client clocks drift
  and rejecting a valid signature over 30 seconds of skew is a support burden, not security.
- **The `domain` field is validated** against `SIWE_DOMAINS` (defaulting to the hosts of
  `CORS_ORIGINS`), so a signature harvested by a phishing site for its own domain will not
  authenticate here.
- **Sessions are stateless HMACs**, not database rows — no session-store lookup on every
  request. `SESSION_SECRET` must be set wherever more than one API process runs; otherwise
  each process signs with its own random secret and a session only works on the process that
  issued it. The config comment says exactly this, because it is the kind of thing that
  works perfectly in development and fails intermittently in production.
- **Smart-contract wallets are explicitly unsupported** (EIP-1271 needs an on-chain call this
  module does not make). Stated in the docstring rather than failing mysteriously.

### 26.2 Authorisation

`_require_wallet` distinguishes **401 "sign in first"** from **403 "signed in as a different
wallet"** — a meaningful distinction, because the remedies differ. `_require_admin` gates
operational endpoints with a constant-time `hmac.compare_digest` comparison, and in
production those endpoints are **disabled entirely** unless `ADMIN_TOKEN` is set. Unset
config fails closed.

### 26.3 Execution safety — validating, not trusting, the swap provider

Every 0x response is checked before anything reaches the wallet:

| Rule enforced server-side | The attack or accident it prevents |
|---|---|
| An allowance is only ever granted to the **AllowanceHolder** contract, never to the Settler contract a swap may route through | A malicious or compromised response persuading the user to approve an arbitrary contract |
| An allowance may never exceed the amount the swap sells | Unlimited-approval drain, the single most common way crypto users lose funds |
| A transaction may never send more native token than the swap sells | Value siphoning through an inflated `value` field |
| Swaps are same-network only | A swap cannot move value between chains; pretending otherwise would produce an unsignable transaction |
| A gas reserve is withheld ($25 on Ethereum mainnet, $2 on Base) | Sweeping the native balance and leaving a wallet unable to pay for its next transaction |
| Legs worth ≤ $5 are suppressed with an explicit reason | A trade that costs more in gas and slippage than it moves |

**The provider is an untrusted input, not an authority.** That framing is the security
decision; the six rules are its implementation.

### 26.4 Asset classification

Classification is by **contract address on a known chain**, never by token name. A spam token
can call itself `USDC`, and a system that trusts names will happily classify it as a
stablecoin and advise holding it. Anything unrecognised is reported as `unknown` and treated
as volatile for exposure purposes — **failing toward caution**, not toward optimism.

### 26.5 Infrastructure security

- **No static AWS keys in production** — the ECS task role supplies credentials, and the
  service refuses to boot if static keys are present.
- **IAM policies scoped to this stack's own resources** — this queue ARN, this secret ARN,
  this bucket, and `rds-db:connect` for exactly one DB user (§27.3).
- **Database authentication by IAM token, never a password** — so there is no database
  credential to rotate, leak or store, and `KNOWN_KEYS` in `secrets.py` deliberately contains
  no DB credential.
- **The ALB accepts traffic only from CloudFront's origin-facing prefix list**, so the
  balancer cannot be reached directly and CloudFront cannot be bypassed.
- **The container runs as a non-root user (uid 10001)** and the image excludes `.env`.
- **Logs to stdout only** — the awslogs driver forwards them; nothing writes credentials to disk.

---

## 27. AWS services — every service and why

This is the section to read if the question is *"why is AWS in this project at all, and why
these services specifically?"*

**The governing principle, stated once:**

> **AWS is infrastructure *around* the engine, never a dependency *of* it.** Every integration
> is optional, gated behind `AWS_ENABLED`, and has a defined degraded path. The application —
> including the full demo — runs end to end with no AWS account.

That is enforced in code: `aws/client.py` raises `AwsUnavailable` when AWS is off or a call
fails, and **every caller catches it and falls back**. There is no code path where an AWS
outage produces a blank screen.

### 27.1 The services

#### 1. Amazon S3 — historical dataset storage

**Role:** hold the price-history and prediction-market datasets the quant engine reads.

**Why it is needed:** price history is the expensive part of an analysis — one provider
request per asset, every time. Caching each series in S3 turns a repeat analysis into a bulk
read, and gives the scheduled Lambdas somewhere to write.

**Design decisions inside it:**
- **Gzipped JSON.** Price series are highly compressible; storage and transfer both drop
  substantially for one `gzip.compress` call.
- **Date-partitioned keys** (`price-history/2026-09-18/BTC.json.gz`). Lifecycle rules can
  then expire old data by prefix, cheaply, without a scan.
- **Reads log at `debug`, not `warning`.** A miss is the common case, and a cache that fills
  the log with warnings during normal operation trains people to ignore the log.

**Without it:** falls back to the in-process cache. Identical behaviour, only slower across
restarts.

---

#### 2. Amazon SQS (+ dead-letter queue) — the simulation pipeline

**Role:** queue computationally expensive Monte Carlo jobs so the API does not hold an HTTP
request open for them.

**Why it is needed:** a 50,000-path, 365-day run is slow enough that holding a request open
is the wrong shape — it ties up a worker, risks a load-balancer timeout, and gives the user
a spinner with no progress.

**Design decisions inside it:**
- **`should_queue` draws the line in exactly one place**, using `simulations × horizon_days ≥
  5,000,000` as a work proxy. Small interactive runs stay **inline on purpose** — queueing a
  90-day, 5,000-path job would *add* latency rather than remove it. Queue-everything is a
  common and costly mistake.
- **Visibility timeout of 900s per receive, 3600s on the queue** (six times the worker
  timeout, per AWS guidance for Lambda consumers). If visibility expires mid-run, SQS hands
  the same job out again and it is computed twice — the comment in `queue.py` says so.
- **Messages are deleted only after the result is durably stored**, so a crash mid-computation
  results in a redelivery, not a silently lost job.
- **DLQ after 3 receives, 14-day retention**, with a CloudWatch alarm on it. A job that fails
  three times is a bug, and a bug should page someone rather than disappear.
- **Malformed messages are discarded with a warning**, not retried forever.

**Without it:** the run executes inline. Slower for large jobs, but correct.

---

#### 3. Amazon RDS / Aurora PostgreSQL — the application database

**Role:** wallets, portfolio snapshots, risk metrics, simulations, recommendations, goals,
auth nonces, executions.

**Why it is needed:** two things genuinely require durable, queryable state:
1. **Recorded history** — the wallet's real value over time, deposits included, which cannot
   be reconstructed after the fact. (*Backfilled* history — today's book valued at past
   prices — is available instantly for any wallet and needs no database. Keeping the two
   concepts distinct is itself a design decision, because conflating them would silently
   misrepresent performance.)
2. **Auditability** — every recommendation stored **with the inputs that produced it**. A
   recommendation that cannot be reconstructed later cannot be defended later.

**Design decisions inside it:**
- **IAM authentication, no password.** Aurora IAM tokens expire after 15 minutes, so a token
  is *not* generated once and reused: the connection pool's `connect` hook mints a fresh one
  immediately before each new physical connection. Connections already open stay valid past
  expiry, because the token is only checked at authentication time. This is the detail that
  makes passwordless database access actually work under a long-lived pool.
- **Schema created idempotently on boot** (`CREATE TABLE IF NOT EXISTS` in `migrate()`), so
  new tables are additive and deployment needs no separate migration step for this scale.
- **Lazy, fully optional connection.** With no `RDS_HOST` the application runs exactly as
  before, minus persistence. The last pool error is retained for `GET /health/database`, so
  the failure is diagnosable rather than just absent.
- **`JSONB` for holdings**, indexed `(address, captured_at DESC)` — the only access pattern
  that matters is "latest N snapshots for this wallet."

**Without it:** no persistence. Everything else works.

---

#### 4. AWS Secrets Manager — credential storage

**Role:** hold the Alchemy, model and 0x credentials instead of exposing them in application
code or images.

**Design decisions inside it:**
- **One JSON secret**, read once at startup, rather than one API call per credential.
- **An allow-list (`KNOWN_KEYS`)** — anything else in the secret is ignored, so the secret
  cannot be used to inject arbitrary environment variables into the process.
- **Values are layered *under* the process environment**, so a locally exported variable
  always wins. This is what keeps local development working unchanged against the same image.
- **It never raises.** A missing or unreadable secret must not stop the service from
  starting, because the same image runs locally with no AWS at all.
- **No database credential is in it**, because RDS uses IAM.

**Without it:** environment variables, exactly as in local development.

---

#### 5. Amazon CloudWatch — metrics, logs and alarms

**Role:** operational visibility.

**Design decisions inside it:**
- **Logs arrive free via stdout** under ECS and Lambda, so the telemetry module handles only
  **custom metrics** — the numbers no log line gives you: analysis latency, simulation
  duration, upstream failures by provider, recommendation confidence, and how often a
  rebalance is recommended.
- **Every telemetry call swallows its errors.** A monitoring failure must never surface to a
  user. Monitoring that can break the thing it monitors is worse than no monitoring.
- **The `timed` context manager emits on the failure path too**, so a slow *error* is still
  visible — otherwise the latency graph quietly only measures successes.
- **30-day log retention**, because indefinite retention is a bill, not a feature.

**Four alarms, each chosen for a distinct failure mode:**

| Alarm | Trigger | Why this specific alarm |
|---|---|---|
| Dead-lettered jobs | any message in the DLQ | A job failed 3× — a real bug, not a blip |
| API 5xx | > 10 in 5 minutes | Tolerates a single transient failure; catches a genuine outage |
| No healthy task | `HealthyHostCount < 1` for 3 minutes, `TreatMissingData: breaching` | Total outage. *Missing data is treated as breaching* — because "the metric stopped arriving" is itself an outage symptom, and treating it as healthy is how outages go unnoticed |
| Worker errors | any Lambda error | The queue worker fails silently by nature; nobody is watching a response |

Alarms publish to an **SNS topic** with an email subscription (`ALARM_EMAIL`), and the topic
is created only if an address is supplied.

---

#### 6. Amazon ECS on Fargate — running the API

**Why Fargate and not EC2:** no servers to patch, no capacity to manage, and the workload is
a single stateless container. EC2 would add an operational surface for no gain at this scale.

**Why ECS and not Lambda for the API:** a cold analysis is 20+ sequential upstream calls with
an LLM step in the middle. That is a long-running, connection-pool-holding, async-fan-out
workload — the opposite of what a request-scoped Lambda is good at. Lambda would mean cold
starts on the expensive path, a fresh HTTP pool per invocation, and a lost in-process TTL
cache. *The pieces that genuinely fit Lambda are on Lambda — see below.*

**Design decisions:** rolling deployments that replace tasks only once new ones pass health
checks, with automatic rollback if they never do; a container `HEALTHCHECK` hitting `/health`;
non-root user; credentials from the task role.

---

#### 7. AWS Lambda — scheduled jobs and the queue worker

**Why Lambda here but not for the API:** these workloads are short, periodic or bursty, and
idle most of the time. Paying for an always-on task to run three jobs every five minutes, or
to wait for a queue that is usually empty, is waste.

Four functions: three refresh jobs and the simulation worker, the last with
**reserved concurrency ≤ 2** — a deliberate ceiling, because an unbounded worker pool on a
CPU-heavy job is how a queue backlog turns into a surprise invoice.

**The single most important decision in this area:**

> The same handler in `aws/handlers.py` runs as the Lambda consumer in AWS **and** as the
> in-process loop locally. Nothing in `handlers.py` reimplements engine logic — it calls the
> same service code the API calls.

Two code paths for the same job inevitably drift, and the drift is only discovered in
production. One handler, two invocation contexts.

---

#### 8. Amazon EventBridge — the schedule

**Role:** one `rate(5 minutes)` rule triggering the three refresh jobs.

**Why:** the alternative — an in-process `asyncio` loop — is what runs locally, and running
both at once would double-execute every job. `REFRESH_ENABLED` decides which owns the
schedule in each environment. The trap this avoids is explicitly documented in the project's
own TODO: *add new scheduled work to the shared handler, not to one of the two paths, or it
will run twice in one environment and never in the other.*

---

#### 9. Amazon CloudFront — HTTPS for the API

**Why it exists:** browsers refuse mixed content, so an HTTPS frontend on Vercel cannot call
a plain-HTTP ALB. ACM will not issue a certificate for the ALB's own DNS name, and no custom
domain was in scope. CloudFront supplies a trusted certificate on a `*.cloudfront.net` name
with no domain purchase.

**The security decision that comes with it:** the ALB's security group accepts traffic **only
from CloudFront's origin-facing prefix list**, so CloudFront cannot be bypassed. Because that
makes the rightmost `X-Forwarded-For` hop a shared edge server, the rate limiter switches to
`CloudFront-Viewer-Address` under `BEHIND_CLOUDFRONT` (§23.3) — an example of one
infrastructure choice correctly propagating into application logic instead of quietly
breaking it.

**The template supports both topologies:** supply `CertificateArn` and the certificate goes on
the ALB directly with your own domain and no CloudFront; leave it blank and you get
CloudFront. The `ApiUrl` output resolves to whichever applies.

**Known limit:** CloudFront waits at most 60 seconds for the origin (a quota increase allows
up to 180), so a long free-text recommendation can return 504. The quota request is filed
ahead of need.

---

#### 10. Amazon ECR — image registry

Two repositories (`wallerina-api`, `wallerina-jobs`) from **one Dockerfile** with two targets.
Separate repositories keep lifecycle policies and image scanning independent for two things
with different deployment cadences, while one Dockerfile guarantees both run identical
locked dependencies.

---

#### 11. Elastic Load Balancing (ALB) — the entry point

Health-checked target group, so ECS knows what "healthy" means; supports the rolling
deployment and rollback; terminates TLS when a certificate is supplied.

---

#### 12. AWS IAM — the permission model

Three roles, each minimally scoped (§27.3).

---

#### 13. Amazon SNS — alarm delivery

One topic, one email subscription, created only when `ALARM_EMAIL` is supplied. SNS rather
than direct email so more subscribers (a pager, a chat webhook, a Lambda) can be added later
without touching the alarms.

---

#### 14. Amazon SES — *planned*, for the email-notification feature (§32)

Transactional mail only: sign-in codes and opt-in rebalance alerts, with one-click
unsubscribe, and **bounce/complaint handling via SNS that disables notifications for that
address automatically**. Production access must be requested ahead of time because the
sandbox only sends to verified addresses — which is why the request is the first item in the
project's own TODO, filed before any email code is written.

### 27.2 What breaks without each service

| Removed | Behaviour |
|---|---|
| AWS entirely | S3 → in-process cache · SQS → inline run · RDS → no persistence · CloudWatch → no-op. **Full demo path still works.** |
| S3 only | Repeat analyses re-fetch price history. Slower, correct. |
| SQS only | Large simulations run inline. Slower, correct. |
| RDS only | No recorded history, no stored goals, no audit trail. Backfilled history still works for any wallet. |
| Secrets Manager only | Environment variables supply credentials. |
| CloudWatch only | No metrics or alarms; logs still go to stdout. |
| CloudFront only | Supply an ACM certificate on the ALB instead; the template handles both. |

### 27.3 IAM scoping, concretely

| Role | Trusts | May do |
|---|---|---|
| **ApiExecutionRole** | ECS agent | Pull the image, write logs |
| **ApiTaskRole** | `ecs-tasks.amazonaws.com` | `rds-db:connect` for **one** DB user ARN · `s3:GetObject`/`PutObject` on **this** bucket's objects, `ListBucket` on the bucket · `sqs:SendMessage` to **this** queue · `GetSecretValue` on **this** secret · `cloudwatch:PutMetricData` |
| **JobsRole** | `lambda.amazonaws.com` | The same, except **Receive/Delete/ChangeVisibility** on the queue instead of Send |

The API can *send* to the queue but not consume it; the worker can *consume* but not send.
The split is not cosmetic — it means a compromised API task cannot drain the job queue, and
a compromised worker cannot inject jobs. `PutMetricData` is the one `"*"` resource, because
CloudWatch metrics have no resource-level ARN to scope to.

### 27.4 Cost posture

Expected **≈$50–60/month plus Aurora**. The known driver: Aurora rarely pauses, because the
5-minute snapshot job keeps touching it — an accepted trade of cost for the recorded history
that cannot be reconstructed later. Other guards already in place: reserved concurrency ≤ 2
on the worker, 30-day log retention, a queue threshold that avoids paying for queueing small
jobs, and S3 date-partitioned keys so lifecycle expiry is cheap.

---

## 28. Deployment architecture

### 28.1 Two CloudFormation stacks

| Stack | Contains | Why separate |
|---|---|---|
| `wallerina-ecr` | Two ECR repositories | Repositories must exist before an image can be pushed, and they should survive teardown of the application stack. Deleting the app must not delete the images needed to redeploy it. |
| `wallerina` | Everything else — CloudFront, ALB, ECS, 4 Lambdas, SQS + DLQ, Secrets, IAM, log groups, EventBridge, alarms, SNS | One atomic unit with one lifecycle |

**Reused, never modified by the stacks:** the Aurora cluster and the S3 bucket. Both hold
data that must outlive any stack operation — a `Delete` on either during a rollback would be
unrecoverable. They are passed in as parameters.

### 28.2 The Docker build

One Dockerfile, three stages:

```
build    (uv:python3.12-bookworm-slim)  resolve + install from uv.lock
  ├── lambda   (public.ecr.aws/lambda/python:3.12)   ← site-packages copied in
  └── runtime  (python3.12-slim-bookworm, default)   ← venv + src, non-root uid 10001
```

Decisions:
- **Dependencies install in their own layer** before `src` is copied, so an application edit
  does not invalidate the dependency install on every build.
- **`--frozen --no-dev`** — the lockfile is authoritative and test tooling never ships.
- **`--no-editable`** for the final sync, so the image contains a real installation.
- **Multi-stage**, so the runtime layer carries no build toolchain.
- **Non-root user**, `.env` excluded, logs unbuffered to stdout.
- **Lambda images must be built `--provenance=false`** — Lambda rejects multi-manifest images.
  Exactly the sort of thing that costs an afternoon if it is not written down, so it is
  written down in the Dockerfile.

### 28.3 Deployment order

1. IAM user `wallerina-deploy`, `aws configure`, delete root keys, enable root MFA
2. `npx vercel --prod` → obtain the frontend URL
3. `CORS_ORIGINS=<vercel url> ALARM_EMAIL=… ./deploy/deploy.sh`
4. Populate the `wallerina/app` secret with API keys
5. Force a new ECS deployment so tasks pick the secret up
6. Set `NEXT_PUBLIC_API_URL` on Vercel, redeploy
7. Confirm the SNS subscription email
8. Verify `GET /health/database`

The ordering is not arbitrary: CORS needs the frontend URL, which needs the frontend
deployed; the frontend needs the API URL, which needs the stack deployed. The circular
dependency is broken by deploying the frontend first with a placeholder API URL.

---

## 29. Frontend architecture

```
frontend/src/
├── app/
│   ├── page.js              landing · connect wallet          (outside the shell)
│   └── (app)/               authenticated shell — route group
│       ├── dashboard/       overview · performance · draft swaps
│       ├── portfolio/       holdings · asset explorer
│       ├── risk/            metrics · risk history
│       ├── simulations/     Monte Carlo runner
│       ├── recommendations/ allocation + reasoning
│       ├── chat/            streamed portfolio Q&A
│       └── settings/        goal selection
├── components/              WalletProvider · Panel · Table · Chat · charts/ · …
└── lib/                     api.js · chart.js · format.js
```

Decisions:
- **A route group `(app)`** gives the authenticated shell its own layout without adding a URL
  segment, so the landing page can sit outside it with no nested-layout workaround.
- **One CSS module per component.** Styles cannot leak; deleting a component deletes its
  styles.
- **`AbortController` on every request**, with in-flight requests aborted when the wallet or
  goal changes — exactly what `DraftSwapsPanel` does, so a stale draft for a previous wallet
  can never land in state.
- **Panels load expensively-computed data on demand**, not on mount. The draft-swaps panel
  runs a full recommendation pipeline; firing that automatically on every dashboard visit
  would be a cost and latency mistake.
- **A single typed API client** with a custom `ApiError` carrying `status` and `detail`, so
  every page renders a real backend message ("Sign in with this wallet first") rather than a
  generic failure.

---

## 30. Testing strategy

**312 tests across 21 suites**, all passing.

| Suite | Covers |
|---|---|
| `test_risk`, `test_monte_carlo`, `test_implied`, `test_allocation` | The quant engine — pure functions, no mocks needed |
| `test_rebalance`, `test_execution` | Trade construction, gas reserves, the $5 minimum-leg boundary, unsupported networks, unknown decimals |
| `test_agent_context`, `test_grounding`, `test_llm_provider` | Pipeline state, the grounding gate, model-provider behaviour |
| `test_auth`, `test_database_iam` | SIWE parsing/verification, nonce reuse, IAM token refresh in the pool hook |
| `test_aws`, `test_simulation_queue`, `test_goals_and_refresh` | AWS integrations and their degraded paths |
| `test_kalshi`, `test_services`, `test_dns` | Provider clients, circuit breakers, the DNS-over-HTTPS transport override |
| `test_production` | That production **refuses to start** with unsafe configuration |
| `test_chat_presets`, `test_history` | Chat behaviour, backfilled vs recorded history |

The strategy follows from the architecture: because `quant/` has no framework dependencies,
its tests are ordinary function calls with arrays — fast, deterministic, no fixtures. The
mock-heavy tests are confined to the boundary layers, which is where mocks belong.

`test_production` deserves a mention: it tests a *refusal*. Asserting that the service will
not boot with `CORS_ORIGINS=*` or with static AWS keys turns a documented policy into an
enforced one.

---

## 31. Architectural decision record — every decision explained

Each row: the decision, the reasoning, and the alternative that was rejected.

### Core philosophy

| # | Decision | Why | Rejected alternative |
|---|---|---|---|
| 1 | **Deterministic code produces every number; the LLM only writes prose** | A user acts on these figures with real money. A probabilistic component must not be able to emit one. | Letting the model compute the allocation — simpler, and unauditable |
| 2 | **A grounding gate re-checks the model's output** | A prompt is a request, not a guarantee. Policy vs. control. | Trusting the prompt instruction alone |
| 3 | **Advice only — never hold keys, sign or send** | Removes the entire custody threat model, and every regulatory question that comes with it | Executing rebalances automatically |
| 4 | **Zero drift by default in the simulator** | Drift estimated from short crypto history mostly measures noise; the product does not predict prices | Historical drift — makes the simulator a trend extrapolator |
| 5 | **Classify assets by contract address, never by name** | Spam tokens impersonate stablecoins by name | Symbol matching |
| 6 | **Unknown assets count as volatile** | Fail toward caution | Excluding them, which flatters the risk number |

### Engine design

| # | Decision | Why | Rejected alternative |
|---|---|---|---|
| 7 | **`quant/` imports no framework, no network, no AWS** | Makes the part that produces user-facing numbers trivially testable in isolation | Convenient direct calls to providers from the engine |
| 8 | **Correlated shocks via Cholesky, not independent draws** | Correlated tokens are the actual risk; independent draws would hide it | Independent per-asset paths |
| 9 | **Batched path generation, portfolio-collapsed immediately** | 150 MB instead of multiple GB for a 50k × 365 run — what makes large jobs affordable | Retaining the full per-asset cube |
| 10 | **Antithetic sampling** | Free variance reduction, no bias | Plain sampling |
| 11 | **Implied volatility blended by *fit quality*** | A thin or noisy market must not overwhelm a well-measured historical estimate | A fixed blend weight |
| 12 | **Named, bounded allocation drivers** | No single signal can dominate; the decision is auditable and the explainer needs no re-derivation | An opaque scoring function |
| 13 | **A ±5% band around the target** | Prevents advice thrash and fee-churn on noise | Rebalancing at any deviation |
| 14 | **Annualise with 365 days, losses as positive fractions** | Crypto trades daily; a fixed sign convention removes a whole class of bug | The 252-day equity convention |

### Pipeline

| # | Decision | Why | Rejected alternative |
|---|---|---|---|
| 15 | **LangGraph rather than hand-written async** | Genuine parallel fan-out with per-node retry policy and typed accumulating state | `asyncio.gather`, which works until you need per-node retry and partial failure |
| 16 | **Only `data` carries a retry policy** | It is the only node touching flaky upstreams; retrying pure computation is pointless | Blanket retries |
| 17 | **Analyst agents degrade to placeholders; the allocation engine does not** | Losing commentary is survivable; shipping a fabricated target is not | Uniform fault tolerance |
| 18 | **`goal` runs first, exactly once, and its context is written into state** | No downstream node re-reads the goal or invents thresholds | Each agent parsing the goal itself |
| 19 | **A preset goal must never reach an LLM** | Deterministic input deserves a deterministic path — cheaper, faster, and cannot drift | Sending everything through the model |
| 20 | **Chat gets one tool (a what-if simulation), not a larger prompt** | Its only route to a new number is to ask the engine | Feeding more numbers into the prompt and hoping |

### Infrastructure

| # | Decision | Why | Rejected alternative |
|---|---|---|---|
| 21 | **Every AWS integration optional, with a defined degraded path** | Local development and the demo need no AWS account; no single dependency can blank the screen | Hard AWS dependency |
| 22 | **ECS Fargate for the API, Lambda for jobs** | The API is a long-running async fan-out with a connection pool and an in-process cache; the jobs are short and periodic. Each workload on the runtime that fits it. | All-Lambda (cold starts, lost pool and cache) or all-ECS (paying for idle) |
| 23 | **One handler shared by the Lambda consumer and the local loop** | Two code paths for one job drift, and the drift shows up in production | Separate local and cloud implementations |
| 24 | **`should_queue` thresholds the work; small runs stay inline** | Queueing a small job *adds* latency | Queue everything |
| 25 | **IAM database authentication, no password** | No credential to rotate, leak or store; token minted per connection in the pool hook | A password in Secrets Manager |
| 26 | **Secrets layered *under* the process environment** | A local export always wins, so one image works in both environments | Secrets overriding the environment |
| 27 | **CloudFront in front of the ALB, ALB restricted to its prefix list** | Free trusted HTTPS with no domain, and the origin cannot be bypassed | Buying a domain and putting ACM on the ALB (still supported via `CertificateArn`) |
| 28 | **Rate-limit key switches to `CloudFront-Viewer-Address` behind CloudFront** | The rightmost XFF hop is a shared edge server; using it would let one visitor exhaust the limit for everyone behind that edge | Trusting XFF unconditionally |
| 29 | **Rate limiter registered before CORS, so CORS is outermost** | A 429 without CORS headers is unreadable by the browser that caused it | Either ordering, chosen by accident |
| 30 | **Production refuses to boot on unsafe config** | A misconfiguration becomes a loud failure instead of a silent weakening | Warning and continuing |
| 31 | **Aurora and S3 passed in, never created or deleted by the stacks** | A rollback must not be able to delete irreplaceable data | Managing them in the stack |
| 32 | **Reserved concurrency ≤ 2 on the worker** | An unbounded pool on CPU-heavy jobs turns a backlog into an invoice | Default concurrency |
| 33 | **`TreatMissingData: breaching` on the healthy-host alarm** | "The metric stopped arriving" is itself an outage symptom | Treating missing data as healthy |
| 34 | **Circuit breakers on prediction-market clients** | Otherwise every analysis pays a full timeout while a provider is down | Timeout-only |
| 35 | **DNS-over-HTTPS for named hosts only** | Some ISPs sinkhole Polymarket; scoped to named hosts, with SNI and Host preserved | Global DNS override, or accepting the failure |
| 36 | **Single-flight lock in the TTL cache** | Concurrent requests for one wallet trigger one upstream fetch, not N | A plain TTL cache with a thundering herd |
| 37 | **The cache is process-local on purpose** | It is a latency cache, not a datastore; conflating the two produces a cache you are afraid to clear | A shared cache used as durable state |

### Security

| # | Decision | Why | Rejected alternative |
|---|---|---|---|
| 38 | **SIWE (EIP-4361), passwordless** | The wallet is already the identity; no password store to breach | Email + password |
| 39 | **Stateless HMAC sessions** | No session lookup per request; `SESSION_SECRET` requirement documented for multi-process | Server-side session store |
| 40 | **Reads public, writes authenticated** | Balances are public data; stored state is not | Requiring sign-in to view anything, which would break the demo path |
| 41 | **The plan endpoint is public and read-only** | A draft is a description; it requires nothing from the wallet's owner and is invisible to them | Gating drafts behind sign-in |
| 42 | **0x responses are validated, not trusted** | The provider is an untrusted input: allowance target, allowance amount and native value are all checked | Passing the provider's calldata straight through |
| 43 | **Exact-amount allowances to AllowanceHolder only** | Unlimited approvals are the most common way crypto users lose funds | Infinite approval for convenience |
| 44 | **Gas reserve withheld per network** | Never leave a wallet unable to pay for its next transaction | Sweeping the full native balance |
| 45 | **Legs ≤ $5 suppressed, with the reason shown** | Below that, gas and slippage exceed what the trade moves. Boundary made *exclusive* and applied identically in all three comparisons | Drafting a trade that loses money by existing |
| 46 | **Admin endpoints disabled in production unless `ADMIN_TOKEN` is set** | Unset config fails closed | Open by default |
| 47 | **SIWE `domain` validated against an allow-list** | A signature harvested by a phishing site for its own domain will not authenticate here | Accepting any domain |

### Frontend

| # | Decision | Why | Rejected alternative |
|---|---|---|---|
| 48 | **CSS Modules, one per component** | Scoped, zero runtime, no utility-class sprawl | Tailwind or CSS-in-JS |
| 49 | **Hand-written SVG charts** | Fan charts and correlation heatmaps are not stock chart types; avoids a large dependency | A charting library, wrapped |
| 50 | **Raw EIP-1193, no wallet library** | Connect, read accounts, sign — that is the entire surface | wagmi / RainbowKit |
| 51 | **`AbortController` everywhere; abort on wallet or goal change** | A stale response for a previous wallet can never land in state | Ignoring late responses |
| 52 | **Expensive panels load on demand** | The draft panel runs a full pipeline; auto-firing it on every visit is a cost and latency mistake | Loading on mount |

---

## 32. Technical design of the upcoming features

### 32.1 Drafts in the UI

**Already shipped:** `DraftSwapsPanel` on the dashboard; `POST /api/execution/{address}/plan`
public and read-only; the drafts-only labelling; abort-on-change; the `MIN_LEG_USD` boundary
resolved as exclusive and applied identically in all three comparisons in `build_legs`.

**Remaining work:**

1. **Adversarial click-through with real wallets**, covering the cases the code already
   handles but that have not been exercised end to end: no rebalance required; a sale
   entirely inside the gas reserve (`skipped` populated, `legs` empty); an unsupported
   network (`opt-mainnet`); a token with null `decimals`; and a symbol held on several
   networks, confirming the pooled sale is not double-counted.
2. **Draft persistence and history** — store drafts so a user can return to one, which also
   produces the state the notification feature needs.
3. **Change detection** — a fingerprint over the legs, which is the trigger in §32.2.

### 32.2 Email notifications

**Where the work goes — the decision that matters most:**

> The draft step is added to the **shared handler in `aws/handlers.py`**, not to
> `services/refresh.py` or the EventBridge path individually. Two schedulers exist for the
> same three jobs, with `REFRESH_ENABLED` deciding which is live. Adding the step to one path
> means it runs twice in one environment and never in the other.

**Flow:**

```
refresh cycle
  → for each watched wallet with notify=true
      → build draft (full pipeline — expensive, see the cost guard)
      → fingerprint = hash(legs rounded to ~$10)
      → if fingerprint == last_sent AND rebalance_required unchanged → skip
      → if not rebalance_required → skip
      → if a send occurred for this wallet in the last 24h → defer to the digest
      → SES send (template) → store fingerprint + sent_at
```

**Schema additions** (additive `CREATE TABLE IF NOT EXISTS` in `migrate()`, consistent with
the existing boot-time schema approach):

| Table / column | Purpose |
|---|---|
| `users` (email, created_at, verified_at) | Email accounts |
| `login_codes` (hashed code, expiry, attempts) | Passwordless sign-in |
| `watched_wallets` (user_id, address, goal, notify) | Subscriptions |
| `watched_wallets.last_draft_fingerprint`, `.last_notified_at` | Change detection and throttling |

**Controls and their rationale:**

| Control | Rationale |
|---|---|
| Fingerprint on legs rounded to ~$10 | Price noise must not manufacture a "change". The rounding granularity *is* the noise floor. |
| Send only when the fingerprint changes **and** `rebalance_required` | No email to say "you're fine" |
| ≤1 email per wallet per day, digest across wallets | Volume control that survives a volatile day |
| One-click unsubscribe via a signed token | `SESSION_SECRET` HMAC in `services/auth.py` is already exactly this shape — reuse it rather than inventing a second token format |
| SNS bounce/complaint handling disables that address | Protects sender reputation, which once lost degrades delivery for every user |
| Cap on watched wallets per user; skip unchanged portfolios; ceiling on model calls per cycle | **The load arithmetic:** a draft runs the full pipeline including a model call. 100 watched wallets every 5 minutes is **28,800 pipeline runs a day**. Without a ceiling this feature is a cost incident, not a feature. |

**Rate limiting** reuses `core/ratelimit.py` rather than adding a second mechanism — per
email and per IP on code requests.

### 32.3 Email accounts — the load-bearing refactor

> **Generalise the session subject *first*.** `services/auth.py` exposes
> `issue_session(address)` and `read_session(token) -> str | None`, and every authenticated
> route treats the subject as a wallet address. Make the subject a **typed principal**
> (`wallet:0x…` / `user:<id>`) **before** adding a second identity kind.

If a second identity type is introduced without that change, the wallet-vs-user distinction
leaks into every handler and every future route has to re-learn it. It is a small change made
early, or a large one made repeatedly.

Security requirements: codes expire in ~10 minutes, single-use, limited attempts, per-email
and per-IP request limits, **responses identical whether or not an account exists**
(enumeration resistance), and **only a hash of the code is stored**.

SIWE is kept — a user may link wallets they own, while watching a public address needs no
proof of ownership, because public data requires no permission to read.

**Deployment additions:** SES permissions on the task and Lambda roles; sender address in
config; CORS already covers the Vercel origin.

---

## 33. Known technical debt and honest limits

| Item | Status |
|---|---|
| **Per-process rate limiting** | *N* tasks allow *N*× the configured limit. A WAF rate rule is the correct global ceiling; this layer is a per-task cost guard, and the code documents it. |
| **CloudFront 60s origin timeout** | Long free-text recommendations can 504. Quota increase (to 180s) requested. |
| **Aurora rarely pauses** | The 5-minute snapshot job keeps it warm. Accepted: recorded history cannot be reconstructed later. |
| **No frontend ESLint config** | `next lint` is deprecated; migration to flat-config ESLint is outstanding. |
| **Lognormal implied fit is not fat-tailed** | Documented in the module. Real crypto returns are more extreme; a better-centred lognormal is still an improvement. |
| **Implied vol is risk-neutral, not real-world** | Prediction-market prices carry risk premia and fees. Documented, not hidden. |
| **Portfolio scan capped at 20 pages** | Results are not value-ordered, so a low cap could hide real positions. Mitigated by reporting `scan_truncated` rather than silently truncating. |
| **Smart-contract wallets unsupported** | EIP-1271 verification needs an on-chain call `auth.py` does not make. Stated explicitly rather than failing mysteriously. |
| **In-process TTL cache is not shared across tasks** | Deliberate. Durable state belongs in Aurora. |

---

*End of Part Two. Part One (§1–19) covers the same system for a non-technical audience.
Session history and outstanding task lists live in `progress.md`, `todo.md` and
`docs/dev-context-2026-09-13.md`.*
