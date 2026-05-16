import os
from anthropic import Anthropic

class ArchitectureInsightAgent:
    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    def analyze(self, diff: str) -> str:
        prompt = f"""
        You are the KRONOS Architecture Insight Agent. 
        Your job is to detect technology drift, new dependencies, and new architectural patterns introduced in the PR.
        
        PR DIFF:
        {diff}
        
        INSTRUCTIONS:
        Identify any new external libraries, new design patterns (e.g., adding a singleton, introducing a new caching layer), or tech drift.
        If found, output:
        Detected architectural changes: [List them].
        
        If no significant architecture changes, output exactly:
        No significant architectural drift or new dependencies detected.
        
        Keep it under 3 sentences. No pleasantries.
        """
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=300,
            temperature=0.1,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()
