import os
from anthropic import Anthropic

class PromiseAuditAgent:
    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    def analyze(self, diff: str, pr_metadata: dict) -> str:
        title = pr_metadata.get("title", "")
        desc = pr_metadata.get("description", "")
        
        prompt = f"""
        You are the KRONOS Promise Audit Agent. 
        Your job is to compare the PR Title/Description against the actual code changes to ensure the developer did what they promised, and ONLY what they promised.
        
        PR TITLE: {title}
        PR DESCRIPTION: {desc}
        
        PR DIFF:
        {diff}
        
        INSTRUCTIONS:
        Check if the code fulfills the title/description. Check for undocumented "hidden" changes.
        If there is a mismatch or hidden change, call it out directly.
        If it matches perfectly, say: "The code changes align perfectly with the PR description."
        
        Keep it under 3 sentences. No pleasantries.
        """
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=300,
            temperature=0.1,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()
