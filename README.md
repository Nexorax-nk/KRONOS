# LORE: Institutional Memory for GitHub

LORE is a multi-agent system that gives your codebase "Institutional Memory." It tracks architectural decisions, predicts failures, and enforces patterns based on historical context.

## Key Features

- **🧠 Institutional Memory**: Your codebase remembers decisions even when the team forgets.
- **🛡️ 5-Layer PR Review**: Automatically scans every Pull Request for memory conflicts, security regressions, and pattern violations.
- **🔮 Pre-Mortem Agent**: Predicts failures on new issues based on past incidents.
- **🌿 Sustainability Tracking**: Estimates carbon impact savings from architectural decisions.
- **📊 Premium Dashboard**: Visualizes decision graphs and project health.

## Installation

```bash
pip install ./lore-cli
```

## Usage

### Local CLI
```bash
# Validate your memory ledger
lore validate --path .lore

# Generate the visual dashboard
lore dashboard --path .lore --output dashboard.html
```

### GitHub Actions
LORE runs automatically on:
- Pull Request creation/update (5-layer review)
- Issue creation (Pre-mortem)
- PR Merge (Decision extraction)

## Memory Format
Memories are stored in `.lore/*.json`. Example:
```json
{
    "id": "LORE-MEMORY-001",
    "decision": "Use fixed retry intervals",
    "reason": "Thundering herd at 1000+ concurrent requests",
    "governs_files": ["src/api/auth.py"],
    "decided_by": ["@alice"]
}
```

## Tech Stack
- **AI**: Anthropic Claude 3.5 Sonnet
- **CLI**: Python (Click, Rich, Pydantic)
- **Integration**: GitHub Actions, PyGitHub
- **Visualization**: Mermaid.js, Vanilla CSS (Glassmorphism)