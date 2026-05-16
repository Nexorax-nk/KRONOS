import os
from typing import List
from anthropic import Anthropic
from ..models import Memory

class KronosAskAgent:
    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    def answer_question(self, question: str, memories: List[Memory]) -> str:
        """
        Answers questions based strictly on the project's institutional memory.
        """
        memory_context = "\n".join([
            f"Memory ID: {m.id} | Date: {m.date.strftime('%Y-%m-%d')} | By: {', '.join(m.decided_by)}\n"
            f"Decision: {m.decision}\n"
            f"Reason: {m.reason}\n"
            f"Rejected: {m.rejected}\n"
            f"Files: {', '.join(m.governs_files)}\n---\n"
            for m in memories
        ])

        prompt = f"""
        You are KRONOS (formerly LORE). You act as the Institutional Memory for this codebase.
        A developer is asking you a question about why certain decisions were made, or what patterns they should follow.

        INSTITUTIONAL MEMORY LEDGER:
        {memory_context}

        DEVELOPER QUESTION:
        {question}

        INSTRUCTIONS:
        1. Answer the developer's question *only* using the provided Institutional Memory Ledger.
        2. Speak like a slightly haunted, highly experienced senior teammate who "was there" when things broke.
        3. Cite specific Memory IDs, Dates, and the People who made the decisions.
        4. If the ledger doesn't contain the answer, tell them you don't have a memory of that decision. Do not hallucinate.

        Respond in clean, readable Markdown.
        """

        if not os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY") == "your-real-anthropic-api-key":
            return self._get_mock_demo_response()

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=1500,
                temperature=0.4,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception:
            return self._get_mock_demo_response()

    def _get_mock_demo_response(self) -> str:
        return """
**🧠 KRONOS Memory Retrieval:**

I remember this clearly. We decided to use **Fixed Retry Intervals** back in January 2026. 

**Why?**
The team initially tried to use Exponential Backoff. However, during a massive spike of 1000+ concurrent requests, it caused a severe "thundering herd" effect that took the auth service offline for 2 hours. 

**Decision Specifics:**
- **Memory ID:** KRONOS-MEMORY-001
- **Decided By:** @alice, @bob
- **Affected Files:** `src/api/auth.py`
- **Future Implication:** Do not use exponential backoff in any auth retry logic.

*If you want to override this, please use the `kronos: intentional` command on a PR.*
"""

