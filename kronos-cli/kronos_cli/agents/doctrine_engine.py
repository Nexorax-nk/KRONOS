import os
from anthropic import Anthropic

class DoctrineEngineAgent:
    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    def analyze(self, diff: str) -> str:
        prompt = f"""
        You are the KRONOS Doctrine Engine Agent.
        Your job is to enforce coding conventions, style guides, and structural rules (e.g., "always use type hints", "no magic numbers", "handle exceptions explicitly").
        
        PR DIFF:
        {diff}
        
        INSTRUCTIONS:
        If you see style violations, bad naming, or missing type hints, call them out.
        If the code looks clean, output exactly:
        Code style passes. Structural conventions are maintained.
        
        Keep it under 3 sentences. No pleasantries.
        """
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=300,
            temperature=0.1,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()
