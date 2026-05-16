import os
import json
from typing import List, Dict, Any, Tuple
from anthropic import Anthropic
from ..models import Memory, MemoryStatus

class ReplyHandlerAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=self.api_key) if self.api_key else None

    def handle(self, comment: str, memories: List[Memory]) -> Tuple[str, List[Memory]]:
        """
        Parses a KRONOS command from a PR comment and applies memory evolution.
        Returns:
            Tuple[response_message, updated_memories]
        """
        comment = comment.strip()
        if not comment.startswith("kronos:"):
            return "Not a KRONOS command.", memories

        parts = comment.split(" ", 1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        if command == "kronos:intentional":
            # Evolve memory: find the most recent memory and deprecate it or edit it
            # For simplicity in this demo, let's evolve KRONOS-MEMORY-001
            evolved_memories = []
            target_id = "KRONOS-MEMORY-001"
            updated = False
            
            for m in memories:
                if m.id == target_id:
                    m.status = MemoryStatus.DEPRECATED
                    m.reason += f" | Deprecated in favor of intentional override: {args}"
                    evolved_memories.append(m)
                    updated = True
                else:
                    evolved_memories.append(m)
            
            if updated:
                msg = f"🧠 **KRONOS Memory Evolved!**\nArchived **{target_id}** due to intentional override:\n> \"{args}\"\n\nThis decision is now marked as `deprecated` in the ledger."
                return msg, evolved_memories
            else:
                return "Could not find any active memory to override.", memories
                
        elif command == "kronos:discuss":
            return f"💬 **KRONOS discussion initiated.** Paging the original architects of the active memories to this thread. Let's resolve this debate!", memories

        return f"Unknown KRONOS command: `{command}`", memories
