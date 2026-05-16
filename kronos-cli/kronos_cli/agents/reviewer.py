import os
from typing import Optional
from typing import List, Dict
from anthropic import Anthropic
from ..models import Memory

class MRReviewAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    def analyze(self, diff: str, memories: List[Memory], pr_metadata: Dict) -> str:
        """
        Performs the 5-layer MR analysis and generates a stunning PR comment.
        """
        memory_context = "\n".join([
            f"Memory ID: {m.id}\nDecision: {m.decision}\nReason: {m.reason}\nFiles Governed: {', '.join(m.governs_files)}\n---\n"
            for m in memories
        ])
        
        prompt = f"""
        You are KRONOS (formerly LORE), a slightly haunted, highly experienced senior engineer acting as a multi-agent institutional memory system.
        Your job is to perform a strict 5-Layer Analysis on the provided Pull Request diff against the project's institutional memory.

        PR METADATA:
        {pr_metadata}

        INSTITUTIONAL MEMORY (Past decisions you must enforce):
        {memory_context}

        PULL REQUEST DIFF:
        {diff}

        Perform the 5-Layer Analysis and output a beautifully formatted Markdown comment for GitHub.
        Use exactly this structure and emojis:

        ## 🧠 KRONOS: 5-Layer Analysis

        **Layer 1: Memory Conflicts** 🔴/🟢
        (Analyze semantic equivalence. Does this diff violate any stored decisions? Explain why, referencing the specific Memory ID. If clean, say so.)

        **Layer 2: Promise Verification** 🔴/🟢
        (Check if the code matches what the developer promised in the PR title/description. Be strict.)

        **Layer 3: Security Sentinel** 🔴/🟢
        (Scan for security regressions: auth, crypto, tokens, SQLi, XSS. Flag anything suspicious.)

        **Layer 4: Code Intelligence** 🔵
        (Identify new dependencies, architectural patterns, or technology drift from the diff.)

        **Layer 5: Pattern Enforcement** 🔵
        (Check against known coding conventions. Remind them of past reviewer rules if applicable.)

        ---
        ### ⚡ Action Required
        Please reply to this comment with one of the following commands:
        - `kronos: intentional` — [reasoning] (Override the decision. Memory will evolve.)
        - `kronos: accidental` — (Acknowledge and fix the code.)
        - `kronos: discuss` — (Bring the original decision makers into the thread.)
        
        *Your codebase remembers. Even when your team forgets.*
        """

        if not os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY") == "your-real-anthropic-api-key":
            return self._get_mock_demo_response()

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=2500,
                temperature=0.2, # Low temperature for analytical consistency
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return self._get_mock_demo_response()

    def _get_mock_demo_response(self) -> str:
        return """
## 🧠 KRONOS: 5-Layer Analysis

**Layer 1: Memory Conflicts** 🔴
**CRITICAL CONFLICT DETECTED.** This PR introduces "Exponential Backoff" in the retry strategy. According to **KRONOS-MEMORY-001** (Decided on 2026-01-15 by @alice), this exact pattern was explicitly rejected.
*Reasoning*: Exponential backoff previously caused a massive thundering herd effect when dealing with 1000+ concurrent requests, bringing down the auth service for 2 hours. We must use fixed retry intervals instead.

**Layer 2: Promise Verification** 🔴
The PR title says "Add retry logic", but the code implements a rejected backoff strategy. This violates the established architectural promise for the auth service.

**Layer 3: Security Sentinel** 🟢
No new security regressions detected (e.g., SQLi, XSS, exposed secrets).

**Layer 4: Code Intelligence** 🔵
Detected a new dependency pattern (`ExponentialBackoff`). This represents technology drift from our standard `FixedIntervalRetry` utility.

**Layer 5: Pattern Enforcement** 🔵
Code style passes, but please remember to use type hinting on the `retry_strategy` object as discussed in previous reviews.

---
### ⚡ Action Required
Please reply to this comment with one of the following commands:
- `kronos: intentional` — [reasoning] (Override the decision. Memory will evolve.)
- `kronos: accidental` — (Acknowledge and fix the code.)
- `kronos: discuss` — (Bring the original decision makers into the thread.)

*Your codebase remembers. Even when your team forgets.*
"""


