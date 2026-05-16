import os
from typing import List
from anthropic import Anthropic
from ..models import Memory

class MemoryGuardAgent:
    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    def analyze(self, diff: str, memories: List[Memory]) -> str:
        memory_context = "\n".join([
            f"ID: {m.id} | Decision: {m.decision} | Reason: {m.reason}"
            for m in memories
        ])
        
        prompt = f"""
        You are the KRONOS Memory Guard Agent. Your *only* job is to detect if a PR diff violates past architectural decisions.
        
        INSTITUTIONAL MEMORY:
        {memory_context}
        
        PR DIFF:
        {diff}
        
        INSTRUCTIONS:
        Analyze the diff against the memory. 
        If there is a conflict, output EXACTLY this format:
        **CRITICAL CONFLICT DETECTED.** [Explain the conflict briefly]. According to **[MEMORY-ID]**, this was explicitly rejected because [Reason].
        
        If there is no conflict, output exactly:
        No memory conflicts detected. The architecture remains stable.
        
        Keep it under 3 sentences. No pleasantries.
        """
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=300,
            temperature=0.1,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()
