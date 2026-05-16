import os
import sys
import json

# pyrefly: ignore [missing-import]
from kronos_cli.agents.reviewer import MRReviewAgent
# pyrefly: ignore [missing-import]
from kronos_cli.models import Memory
sys.path.append(os.path.join(os.path.dirname(__file__), "kronos-cli"))



def sim_review():
    # 1. Load our 'Institutional Memory'
    with open(".kronos/memory-001.json", "r") as f:
        memory = Memory(**json.load(f))

    # 2. Simulate a "Bad" PR Diff (Trying to use Exponential Backoff which was rejected)
    bad_diff = """
    --- a/src/api/auth.py
    +++ b/src/api/auth.py
    @@ -10,5 +10,10 @@ def login():
    +    # Adding retry logic with exponential backoff
    +    retry_strategy = ExponentialBackoff(base=2, factor=5)
    +    return attempt_login(retry_strategy)
    """

    print("[KRONOS] is analyzing the Pull Request...")
    
    agent = MRReviewAgent()
    result = agent.analyze(
        diff=bad_diff, 
        memories=[memory], 
        pr_metadata={"title": "Add retry logic", "author": "new_dev"}
    )
    
    print("\n--- KRONOS'S PR COMMENT ---")
    # Configure stdout to handle emojis safely on Windows
    sys.stdout.reconfigure(encoding='utf-8')
    print(result)

if __name__ == "__main__":
    sim_review()


