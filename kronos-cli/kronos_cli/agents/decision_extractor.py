import os
import json
from typing import Dict, Any, Optional
from anthropic import Anthropic
from ..models import Memory, MemoryStatus

class DecisionExtractorAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=self.api_key) if self.api_key else None

    def extract(self, diff: str, pr_metadata: Dict[str, Any]) -> Memory:
        """
        Parses a merged PR and extracts architectural decisions into a Memory object.
        """
        # MOCK DEMO MODE
        if not self.api_key or self.api_key == "your-real-anthropic-api-key":
            return self._get_mock_memory(pr_metadata)

        prompt = f"""
        You are the KRONOS Decision Extractor Agent. 
        Your job is to read a merged Pull Request diff and metadata and extract a permanent, structured architectural decision (Memory).
        
        PR METADATA:
        {pr_metadata}
        
        PR DIFF:
        {diff}
        
        INSTRUCTIONS:
        1. Formulate a clear, concise architectural decision based on this merged PR.
        2. Provide the technical reasoning.
        3. Identify the files or file globs this decision governs.
        4. Choose one of the decided_by authors.
        5. Output ONLY a valid JSON object matching this schema:
        {{
            "id": "KRONOS-MEMORY-XXX", (Make a unique ID like KRONOS-MEMORY-002)
            "source_pr": "URL or PR Number",
            "decision": "The clear rule or decision",
            "reason": "The architectural explanation",
            "governs_files": ["list", "of", "file/paths/or/globs"],
            "decided_by": ["author_name"],
            "rejected": false,
            "status": "active"
        }}
        
        Do not add any explanations, markdown code blocks, or text. Output ONLY raw JSON.
        """

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=600,
                temperature=0.2,
                messages=[{"role": "user", "content": prompt}]
            )
            raw_text = response.content[0].text.strip()
            # Clean JSON if LLM returned markdown code blocks
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            data = json.loads(raw_text.strip())
            return Memory(**data)
        except Exception:
            return self._get_mock_memory(pr_metadata)

    def _get_mock_memory(self, pr_metadata: Dict[str, Any]) -> Memory:
        import datetime
        pr_num = pr_metadata.get("number", "42")
        author = pr_metadata.get("author", "alice")
        return Memory(
            id=f"KRONOS-MEMORY-00{pr_num}",
            source_pr=f"https://github.com/Nexorax-nk/KRONOS/pull/{pr_num}",
            date=datetime.datetime.now(),
            governs_files=["src/api/auth.py"],
            decision="All auth-related operations must use fixed retry intervals (default 5 seconds).",
            reason="Avoid thundering herd effects that take the database offline under load.",
            decided_by=[author],
            rejected="false",
            status=MemoryStatus.ACTIVE
        )
