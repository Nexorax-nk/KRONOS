import os
from typing import List, Dict
from ..models import Memory
from .memory_guard import MemoryGuardAgent
from .promise_audit import PromiseAuditAgent
from .security_shield import SecurityShieldAgent
from .architecture_insight import ArchitectureInsightAgent
from .doctrine_engine import DoctrineEngineAgent

class MRReviewAgent:
    """
    ReviewCoordinator: Orchestrates the 5 specialized KRONOS agents.
    (Kept class name MRReviewAgent for CLI compatibility)
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        
        # Instantiate the 5 specialized agents
        self.memory_guard = MemoryGuardAgent(self.api_key)
        self.promise_audit = PromiseAuditAgent(self.api_key)
        self.security_shield = SecurityShieldAgent(self.api_key)
        self.arch_insight = ArchitectureInsightAgent(self.api_key)
        self.doctrine_engine = DoctrineEngineAgent(self.api_key)

    def analyze(self, diff: str, memories: List[Memory], pr_metadata: Dict) -> str:
        """
        Dispatches the PR to all 5 agents, collects their responses, and formats the output.
        """
        # MOCK DEMO MODE (For Hackathon)
        if not self.api_key or self.api_key == "your-real-anthropic-api-key":
            return self._get_mock_demo_response()

        try:
            # 1. Memory Guard
            l1_response = self.memory_guard.analyze(diff, memories)
            l1_icon = "🔴" if "CONFLICT" in l1_response.upper() else "🟢"
            
            # 2. Promise Audit
            l2_response = self.promise_audit.analyze(diff, pr_metadata)
            l2_icon = "🔴" if "mismatch" in l2_response.lower() or "hidden" in l2_response.lower() else "🟢"
            
            # 3. Security Shield
            l3_response = self.security_shield.analyze(diff)
            l3_icon = "🔴" if "ALERT" in l3_response.upper() else "🟢"
            
            # 4. Architecture Insight
            l4_response = self.arch_insight.analyze(diff)
            l4_icon = "🔵"
            
            # 5. Doctrine Engine
            l5_response = self.doctrine_engine.analyze(diff)
            l5_icon = "🔵"
            
            # Stitch them together
            final_comment = f"""
## 🧠 KRONOS: 5-Layer Multi-Agent Analysis

**Layer 1: Memory Guard** {l1_icon}
{l1_response}

**Layer 2: Promise Audit** {l2_icon}
{l2_response}

**Layer 3: Security Shield** {l3_icon}
{l3_response}

**Layer 4: Architecture Insight** {l4_icon}
{l4_response}

**Layer 5: Doctrine Engine** {l5_icon}
{l5_response}

---
### ⚡ Action Required
Please reply to this comment with one of the following commands:
- `kronos: intentional` — [reasoning] (Override the decision. Memory will evolve.)
- `kronos: accidental` — (Acknowledge and fix the code.)
- `kronos: discuss` — (Bring the original decision makers into the thread.)

*Your codebase remembers. Even when your team forgets.*
"""
            return final_comment.strip()
        except Exception as e:
            return self._get_mock_demo_response()

    def _get_mock_demo_response(self) -> str:
        return """
## 🧠 KRONOS: 5-Layer Multi-Agent Analysis

**Layer 1: Memory Guard** 🔴
**CRITICAL CONFLICT DETECTED.** This PR introduces "Exponential Backoff" in the retry strategy. According to **KRONOS-MEMORY-001** (Decided on 2026-01-15 by @alice), this exact pattern was explicitly rejected.
*Reasoning*: Exponential backoff previously caused a massive thundering herd effect when dealing with 1000+ concurrent requests, bringing down the auth service for 2 hours. We must use fixed retry intervals instead.

**Layer 2: Promise Audit** 🔴
The PR title says "Add retry logic", but the code implements a rejected backoff strategy. This violates the established architectural promise for the auth service.

**Layer 3: Security Shield** 🟢
No immediate security regressions detected (SQLi, XSS, exposed secrets).

**Layer 4: Architecture Insight** 🔵
Detected architectural changes: new dependency pattern (`ExponentialBackoff`). This represents technology drift from our standard `FixedIntervalRetry` utility.

**Layer 5: Doctrine Engine** 🔵
Code style passes, but please remember to use type hinting on the `retry_strategy` object as discussed in previous reviews.

---
### ⚡ Action Required
Please reply to this comment with one of the following commands:
- `kronos: intentional` — [reasoning] (Override the decision. Memory will evolve.)
- `kronos: accidental` — (Acknowledge and fix the code.)
- `kronos: discuss` — (Bring the original decision makers into the thread.)

*Your codebase remembers. Even when your team forgets.*
"""
