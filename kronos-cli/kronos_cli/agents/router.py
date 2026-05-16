import os
from enum import Enum
from typing import Optional
from anthropic import Anthropic
from pydantic import BaseModel

class AgentType(str, Enum):
    PRE_MORTEM = "pre_mortem"
    MR_REVIEW = "mr_review"
    REPLY_HANDLER = "reply_handler"
    DECISION_EXTRACTOR = "decision_extractor"
    HEALTH_AUDITOR = "health_auditor"
    ONBOARDING = "onboarding"
    COMMIT_KEEPER = "commit_keeper"
    NONE = "none"

class TriageResult(BaseModel):
    agent: AgentType
    reasoning: str
    priority: int = 1

class TriageRouter:
    def __init__(self, api_key: Optional[str] = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    def route(self, context: str) -> TriageResult:
        """
        Classifies the incoming GitHub event context and routes to the appropriate agent.
        """
        prompt = f"""
        You are the KRONOS Triage Router. Your job is to inspect the GitHub event context and dispatch it to the correct specialized agent.

        AGENT TYPES:
        - pre_mortem: Triggered when a new issue is created or assigned. Purpose: Failure prediction and engineering spec generation.
        - mr_review: Triggered when a Pull Request is opened or updated. Purpose: 5-layer analysis (Memory, Promises, Security, Architecture, Patterns).
        - reply_handler: Triggered when a user replies with a "kronos:" command (e.g., kronos: intentional, kronos: discuss).
        - decision_extractor: Triggered when a PR is merged. Purpose: Extracting decisions and updating memory.
        - health_auditor: Triggered by a "health audit" command or schedule.
        - onboarding: Triggered by an "onboard" command for new members.
        - commit_keeper: Triggered by a push event.

        CONTEXT:
        {context}

        Return your decision in JSON format with 'agent', 'reasoning', and 'priority'.
        """

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )

        # Basic parsing logic (in a real tool, we'd use a more robust JSON extractor)
        content = response.content[0].text
        try:
            # Attempt to find JSON block if it exists
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            import json
            data = json.loads(content)
            return TriageResult(**data)
        except Exception:
            # Fallback to NONE if parsing fails
            return TriageResult(agent=AgentType.NONE, reasoning="Failed to parse triage response", priority=0)
