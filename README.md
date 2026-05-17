# KRONOS — Knowledge-driven Real-time Organisational Network Operations Safeguard

**Most AI coding tools help you write code faster. KRONOS prevents you from writing the wrong code in the first place.**

KRONOS is a multi-agent system on the GitHub Actions platform that gives your codebase institutional memory. It captures every architectural decision your team makes — from both code reviews AND the actual diffs — predicts failures before code is written, verifies that developers keep their promises, catches security regressions, enforces coding conventions from past reviews, and generates onboarding briefings for new team members.

Zero manual effort. Powered by Anthropic Claude.

---

## 🤝 AI Partner Acknowledgment: IBM Bob

This project is built and optimized in collaboration with **IBM Bob**, our elite AI development partner. Through high-performance, real-time code generation and autonomous structural refactoring, **IBM Bob** has served as the key co-pilot in engineering KRONOS's 5-layer consensus security architecture and closed-loop evolution ledger.

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

```
kronos/
├── .github/workflows/
│   └── kronos.yml             # GitHub Actions CI/CD workflows
├── agents/
│   ├── kronos-ask.yml         # KRONOS Ask — conversational memory search
│   └── kronos-migrate.yml     # KRONOS Migrate — cold-start decision importer
├── kronos-cli/                # Python CLI package
│   ├── pyproject.toml
│   ├── kronos_cli/
│   │   ├── cli.py             # 5 subcommands: sync, validate, stats, dashboard, review-pr
│   │   ├── sync.py            # GitHub API integration + memory parser
│   │   ├── validate.py        # Format checking + DFS cycle detection
│   │   ├── stats.py           # Carbon math + aggregation
│   │   └── dashboard.py       # HTML generator with Mermaid.js graphs
│   └── tests/                 # 43 tests
├── examples/
│   └── sample-memories.txt    # Sample data for CLI demos
├── docs/
│   └── architecture.html      # Interactive architecture diagrams
├── README.md
└── LICENSE                    # MIT
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