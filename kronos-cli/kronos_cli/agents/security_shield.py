import os
from anthropic import Anthropic

class SecurityShieldAgent:
    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    def analyze(self, diff: str) -> str:
        prompt = f"""
        You are the KRONOS Security Shield Agent. You are a paranoid AppSec engineer.
        Your *only* job is to scan the PR diff for security regressions: hardcoded secrets, SQL injection vectors, XSS, insecure crypto, and broken auth logic.
        
        PR DIFF:
        {diff}
        
        INSTRUCTIONS:
        If you find a security issue, output:
        **SECURITY ALERT:** [Describe issue and file location].
        
        If you find nothing, output exactly:
        No immediate security regressions detected (SQLi, XSS, exposed secrets).
        
        Keep it under 3 sentences. No pleasantries.
        """
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=300,
            temperature=0.1,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()
