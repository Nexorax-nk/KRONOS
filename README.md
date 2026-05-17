# KRONOS — Knowledge-driven Real-time Organisational Network Operations Safeguard

**Most AI coding tools help you write code faster. KRONOS prevents you from writing the wrong code in the first place.**

KRONOS is a multi-agent system on the GitHub Actions platform that gives your codebase institutional memory. It captures every architectural decision your team makes — from both code reviews AND the actual diffs — predicts failures before code is written, verifies that developers keep their promises, catches security regressions, enforces coding conventions from past reviews, and generates onboarding briefings for new team members.

Zero manual effort. Powered by Anthropic Claude.

---

## 🤝 AI Partner Acknowledgment: IBM Bob

This project is built and optimized in collaboration with **IBM Bob**, our elite AI development partner. Through high-performance, real-time code generation and autonomous structural refactoring, **IBM Bob** has served as the key co-pilot in engineering KRONOS's 5-layer consensus security architecture and closed-loop evolution ledger.

---

## 🎬 The Production Scenario: Outage at Atlas

Imagine this. You are an engineer at **Atlas**.
Not a toy startup. Atlas is a real-scale financial infrastructure platform.

Every second:
- Thousands of users authenticate to their accounts
- Critical payment flows get authorized
- Complex transactions move across distributed microservices
- High-fidelity telemetry streams across internal systems

#### ⏱️ Six months ago...
The Atlas engineering team faced a **catastrophic authentication outage**.

**WHAT HAPPENED?**
A senior engineer wanted to optimize retry handling during authentication spikes. Intending to reduce retry pressure on the backend authentication servers, he introduced `ExponentialBackoff` inside:
`atlas/security/auth/authenticator.py`

Under high concurrent traffic:
1. Thousands of concurrent client retries synchronized due to lack of jitter.
2. The authentication nodes suffered from a massive thundering herd event and crashed.
3. **Production Impact**: Complete login failures, payment authorization failures, and a partial outage for **2 full hours**.

The team resolved the incident, rolled back the change, decided on **`KRONOS-MEMORY-001`** (enforcing fixed 5-second intervals with jitter instead of backoff), and moved on.

#### ⏱️ Six months later...
A new developer joins Atlas. Tasked with fixing a network latency ticket, he naturally thinks: *"We should add exponential retries to the authenticator module."*
**He introduces the exact same bug.**

And that is the real problem.
Engineering teams don't repeat failures because they are careless. **They repeat them because organizational memory disappears.**

---

## 🛡️ How KRONOS Clears It

When the new developer opens his Pull Request containing `ExponentialBackoff` retry logic, KRONOS's **Memory Guard** agent instantly intercepts the changes via the GitHub Actions triage gateway:

1.  **Passive Detection is Turned into Active Blocking**: 
    - The CLI execution runs `kronos review-pr --repo owner/repo --pr PR_NUMBER --fail-on-conflict`.
    - It matches the diff to `KRONOS-MEMORY-001`'s governed path and detects the rejected code pattern.
2.  **The CI Check Turns RED ❌**:
    - The status check fails, turning the Pull Request triage build **Red (Failed)**, preventing developers from bypassing quality gates.
3.  **Posting the Gatekeeper Comment**:
    - KRONOS comments directly on the PR with a high-fidelity **Institutional Memory Gate** layout detailing the threat, operational impact of the historical outage, and alternative guidelines!
4.  **Evolving Safely**:
    - The merge button remains locked until they either correct the code to `FixedIntervalRetry` or the architectural lead comments `kronos:intentional` to override and evolve the memory ledger.

---

## The Problem

Teams don't break architecture because they're careless. They break it because:

- The people who understood the original decisions leave
- Decisions are buried in PR comment threads nobody can find
- Six months later, someone re-introduces the exact pattern the team rejected
- Reviewer feedback gets repeated on every PR because nobody remembers the last one
- New team members have no way to learn what was decided and why

Every ADR tool requires someone to manually write decisions down. Nobody does. The decisions that matter most — the ones made in passing during code review — are the ones that get lost.

## How KRONOS Works

KRONOS follows your work through the entire development lifecycle — from issue to production — and gets smarter with every merge.

```
                         ┌──────────────┐
    Event arrives ──────>│ TRIAGE ROUTER │
    (issue, PR, merge,   └──────┬───────┘
     mention, schedule)         │ dispatches to specialized agent
          ┌─────────┬───────────┼───────────┬──────────┬────────┐
          v         v           v           v          v        v
   ┌──────────┐┌──────────┐┌──────────┐┌─────────┐┌───────┐┌────────┐
   │ PRE-     ││ PR       ││ DECISION ││ HEALTH  ││ONBOARD││ COMMIT │
   │ MORTEM   ││ REVIEW   ││ EXTRACT  ││ AUDIT   ││  ING  ││ LEDGER │
   │ + SPEC   ││ 5 Layers ││ + Carbon ││ + Graph ││       ││        │
   └──────────┘└──────────┘└──────────┘└─────────┘└───────┘└────────┘

   Standalone Agents:
   ┌──────────────┐  ┌──────────────┐
   │ KRONOS ASK   │  │ KRONOS MIGRATE│
   │ Q&A from     │  │ Import past  │
   │ memory       │  │ decisions    │
   └──────────────┘  └──────────────┘
```

### 1. Issue Created — Failure Prediction

When KRONOS is assigned to an issue, it searches your team's entire history for every time someone tried something similar. It finds the failures, predicts what will go wrong, asks hard technical questions, and generates a full engineering spec:

> *"Your team made a decision about this exact pattern. It was September 2025. A 2-hour auth bypass incident. Here's what happened, and here's what will go wrong again if you don't address it."*

When the developer replies, KRONOS evaluates: vague answers get pushback with references to past incidents. Specific answers get a risk level. Every technical promise is recorded — because KRONOS will check the actual code against these exact words.

### 2. PR Opened — Five-Layer Review

Every open PR gets five layers of scrutiny in a single comment:

**Layer 1: Memory Conflicts** — Semantic analysis of the diff against all stored decisions. Not keyword matching — KRONOS recognizes that "in-memory dict caching" IS "Redis caching on auth tokens" because the failure mode is identical. Cascading impact analysis when overriding a decision that other decisions depend on.

**Layer 2: Promise Verification** — Reads the linked issue thread, extracts every specific technical claim the developer made, and verifies each one against the actual code. "You said 30-second TTL. Your code says 30 minutes. You promised pub/sub invalidation. I don't see it."

**Layer 3: Security Sentinel** — Scans for security-sensitive patterns (auth, crypto, tokens, SQL, XSS, CORS, secrets). Catches SQL injection via string concatenation, MD5 for password hashing, `eval()` on untrusted data. Cross-references against past security decisions and flags regressions.

**Layer 4: Code Intelligence** — Analyzes the actual diff for architectural patterns: new dependencies, API endpoints, schema changes, caching strategies. Cross-references against existing code-sourced memories and flags technology drift.

**Layer 5: Code Pattern Enforcement** — Checks the diff against coding convention rules captured from past reviews. If a reviewer once said "don't use `Optional`, use `X | None`", KRONOS remembers and enforces it automatically. Reviewers never repeat themselves.

Then KRONOS gives the developer three options:

| Reply | What happens |
|---|---|
| `kronos: intentional — [reasoning]` | Override recorded. Memory updated with new reasoning. |
| `kronos: accidental` | Original decision stays. Developer revises code. |
| `kronos: discuss` | Original decision makers brought into the conversation. |

KRONOS doesn't block the merge by default, but with `--fail-on-conflict` enabled, it blocks the PR check completely! And it doesn't forget you saw the warning.

### 3. PR Merged — Decision Extraction

After merge, KRONOS runs four extraction phases:

- **Code Intelligence** — Reads the actual diff for structural changes, new patterns, and removals. Most architectural decisions are never discussed — someone just writes the code. KRONOS catches both.
- **Discussion Extraction** — Captures confirmed decisions from PR comments with carbon impact estimates, incident type tags, and dependency links.
- **Code Pattern Extraction** — Turns reviewer corrections into enforceable rules. "Don't use MD5" becomes a rule that's automatically checked on every future PR.
- **Feature Changelog** — Generates a human-readable entry: what was built, files affected, dependencies changed. A living record of what was actually built.

### 4. Memory Evolution

Decisions aren't static. When a developer overrides a decision with `kronos: intentional`, KRONOS doesn't argue — it updates. The old decision is superseded. The new one is active with the developer's reasoning on record. Dependency links transfer. And KRONOS checks whether the code actually matches the commitments — if you promise bcrypt but ship MD5, the memory records what you said versus what you did.

### 5. Health Audit

On demand: decision health report, sustainability report with carbon impact (kWh/month, CO2 equivalent, trees equivalent), ASCII knowledge graph of decision dependencies, security inventory with staleness warnings, and coverage gaps for files with no governing decisions.

### 6. Onboarding

Generates a complete briefing for new team members: security decisions first (non-negotiable), architecture decisions by file, performance decisions with carbon data, top 3 past incidents, key people table, and the last 10 changelog entries so new members see what was actually built.

### 7. Conversational Search

@mention KRONOS Ask and ask in natural language: "What decisions govern authentication?" KRONOS doesn't return search results. It answers like a teammate who was there — with specific decisions, dates, people, and reasoning.

### 8. Cold-Start Import

The biggest problem with any memory system: it's empty on day one. KRONOS Migrate scans your project's past pull requests, extracts architectural decisions from discussion threads, and writes them as KRONOS memories. One command, and your project has institutional memory from day one.

## The Python CLI

KRONOS includes `kronos-cli`, a Python package with real engineering beyond prompts:

```bash
kronos validate    # Check memory format, field values, dependency integrity, circular deps
kronos stats       # JSON output: memory counts, carbon totals, security inventory, coverage
kronos sync        # Read memories from issue store, write to wiki pages, build KRONOS-INDEX
kronos dashboard   # Generate visual HTML dashboard with decision graphs and carbon tables
```

**43 passing tests** covering validation logic, carbon math, dependency graph traversal (DFS cycle detection), and dashboard generation.

### Visual Dashboard

`kronos dashboard` generates a self-contained HTML page with:
- Summary cards: total memories, security count, carbon impact, pattern rules
- Mermaid.js decision graph showing memory dependencies and blocks
- Carbon impact table with savings/costs and CO2 equivalent
- File coverage map showing which files have governing decisions
- Security inventory with staleness warnings
- Code pattern rules with bad/good examples

## CI/CD Pipeline

```yaml
stages:
  - validate    # YAML syntax + 64 KiB catalog size check
  - test        # pytest on kronos-cli (43 tests)
  - sync        # Publish to AI Catalog + sync memories to wiki
  - pages       # Generate and deploy dashboard to GitHub Pages
```

## Architecture

KRONOS uses a multi-component router architecture on the GitHub Actions platform. A triage router inspects context (issue, PR state, keywords, reply commands) using read-only tools and dispatches to one of eight specialized agents:

| Component | Purpose |
|---|---|
| Triage Router | Context classification and dispatch |
| Pre-Mortem Agent | Issue analysis, failure prediction, spec generation |
| MR Review Agent | Five-layer merge request analysis |
| Reply Handler | Memory evolution via `kronos:` commands |
| Decision Extractor | Post-merge decision + pattern + changelog extraction |
| Health Auditor | Decision health, carbon, knowledge graph |
| Onboarding Agent | New member briefing generation |
| Commit Keeper | Commit-level intelligence and ledger |

Plus two standalone agents: **KRONOS Ask** (conversational search) and **KRONOS Migrate** (retroactive decision import).

## Carbon & Sustainability Tracking

Every decision includes a carbon impact estimate. KRONOS uses Anthropic Claude to reason about the compute implications of architectural decisions — a caching layer that eliminates database round-trips, a batch strategy that replaces individual queries, fixed retry intervals that prevent thundering herd cascades.

Aggregated into sustainability reports: total kWh/month, CO2 equivalent (using IEA global average grid intensity of ~0.4 kg CO2/kWh), and trees equivalent (using EPA figure of ~21 kg CO2 absorbed per mature tree per year).

These are order-of-magnitude estimates — not accounting-grade measurements. The goal is making energy cost visible in architectural decisions so teams can factor sustainability into trade-offs they're already making.

## Why Anthropic Claude?

This isn't "plug in any LLM." Every core KRONOS capability depends on things Claude specifically does well:

- **Semantic conflict detection** — KRONOS doesn't keyword-match. When a dev introduces "in-memory dict caching," Claude recognizes this IS the same pattern as "Redis caching on auth tokens" because the failure mode is identical. No embedding similarity threshold gets this right.
- **Long-context cross-PR pattern recognition** — Claude reads 50+ PR discussion threads in a single pass and spots that three different teams hit the same retry failure.
- **Decision vs. noise discrimination** — PR threads are 90% "LGTM" and "nit: spacing." Claude distinguishes "we chose X because Y" from drive-by approvals.
- **Promise verification** — Claude reads a developer's commitments on an issue ("we'll use 30-second TTL with pub/sub invalidation") and checks the actual code, line by line, against those exact promises.
- **Security regression detection** — When someone replaces JWT validation with a "simpler" token check, Claude understands these are not equivalent security patterns.
- **Opinionated voice** — Claude's instruction-following lets LORE speak as a slightly haunted senior engineer who has seen things break. The persona makes developers actually read the warnings.

## Project Structure

This project has been carefully organized to reflect a production-grade enterprise microservice repository:

```
KRONOS/
├── .github/
│   └── workflows/
│       └── kronos.yml             # GitHub Actions CI/CD workflows
├── .kronos/                       # Git-native Institutional Memory ledgers
│   ├── kronos-memory-001.json
│   ├── kronos-memory-002.json
│   ├── kronos-memory-003.json
│   ├── kronos-memory-004.json
│   ├── kronos-memory-005.json
│   ├── kronos-memory-006.json
│   └── kronos-memory-007.json
├── .vscode/
│   └── settings.json
├── atlas/                         # Production microservices workspace
│   ├── core/
│   │   ├── payments/
│   │   │   └── gateway.py         # Payments Tokenization microservice
│   │   └── telemetry/
│   │       └── logger.py          # Secure telemetry & logging utilities
│   ├── database/
│   │   └── infrastructure/
│   │       └── connector.py       # Pooled SSL database connections
│   └── security/
│       └── auth/
│           └── authenticator.py   # Critical authentication entrypoint
├── dashboard/                     # Telemetry Dashboard resources
├── docs/                          # Architecture & API documentation
├── examples/                      # Dummy memories & integration mocks
├── kronos-cli/                    # Python package command line suite
│   ├── kronos_cli/
│   │   ├── agents/                # 8 Dedicated coordinator review agents
│   │   │   ├── architecture_insight.py
│   │   │   ├── decision_extractor.py
│   │   │   ├── doctrine_engine.py
│   │   │   ├── kronos_ask.py
│   │   │   ├── memory_guard.py
│   │   │   ├── promise_audit.py
│   │   │   ├── reply_handler.py
│   │   │   ├── reviewer.py
│   │   │   ├── router.py
│   │   │   └── security_shield.py
│   │   ├── templates/             # Jinja2 dashboard web templates
│   │   ├── cli.py                 # Click entrypoint commands
│   │   ├── dashboard.py           # Telemetry HTML telemetry compiler
│   │   ├── github_client.py       # Octokit PR diff & comments fetcher
│   │   └── models.py              # Pydantic core memory schemas
│   ├── kronos_cli.egg-info/       # Python build distribution specs
│   ├── lore_cli.egg-info/         # Legacy egg-info specifications
│   └── pyproject.toml             # CLI build & module dependencies
├── .gitignore
├── dashboard.html                 # Compiled dark-mode visual telemetry dashboard
├── IBM BOB REPORT.md              # IBM Bob AI partner report
├── README.md                      # High-end technical documentation
└── test_kronos.py                 # Multi-agent simulation testing script
```

## Tech Stack

- **GitHub Actions Platform** — Flow orchestration, triggers, event routing
- **Anthropic Claude** — Semantic reasoning across all 8 agents
- **GitHub Wiki** — Persistent memory storage (KRONOS-INDEX + memory pages)
- **GitHub API** — PR diffs, discussions, issues, wiki, search
- **Python** — CLI tools (sync, validate, stats, dashboard)
- **Mermaid.js** — Decision graph visualization
- **GitHub Pages** — Dashboard deployment

## Setup

### Prerequisites

- GitHub repository with Actions enabled
- Secrets configured (`GITHUB_TOKEN` and `ANTHROPIC_API_KEY`)

### Quick Start

```bash
# 1. Push and tag
git add . && git commit -m "KRONOS" && git tag v1.0.0
git push origin main --tags

# 2. Install CLI
pip install ./kronos-cli

# 3. Seed initial memory (or use KRONOS Migrate to scan past PRs)
# Create wiki pages KRONOS-INDEX and KRONOS-MEMORY-001

# 4. Generate local dashboard
kronos dashboard --path .kronos --output dashboard.html
```

## Memory Format

```
KRONOS Memory #001
Source PR: #42 — Add retry logic
Date: 2026-01-15
Governs files: atlas/security/auth/authenticator.py
Decision: Use fixed retry intervals
Rejected: Exponential backoff
Reason: Thundering herd at 1000+ concurrent requests
Future implication: No exponential backoff in retry logic
Decided by: @alice, @bob
Confidence: HIGH
Status: Active
Carbon impact: ~300 kWh/month saved
Incident type: retry
Depends on: N/A
Blocks: Memory #003
Source type: discussion
Security relevant: no
```

## Built for the GitHub AI Hackathon 2026

Most submissions will be "AI writes better code." KRONOS is "AI prevents you from repeating your own mistakes."

It doesn't just remember decisions. It reads your code, catches your mistakes, checks your promises, enforces your reviewers' feedback, tracks your carbon footprint, and speaks like a senior engineer who has seen things break.

Powered by Anthropic Claude for semantic reasoning, failure prediction, security analysis, and sustainability tracking.

Co-developed in alliance with our AI coding partner **IBM Bob**.

## License

MIT — see [LICENSE](LICENSE)