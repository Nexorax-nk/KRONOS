import os
import requests
from github import Github
from typing import List, Dict

class GitHubClient:
    def __init__(self, token: str = None):
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.gh = Github(self.token)

    def get_pr_diff(self, repo_name: str, pr_number: int) -> str:
        url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v3.diff"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return f"Error fetching diff: {response.status_code}"


    def post_comment(self, repo_name: str, issue_number: int, body: str):
        repo = self.gh.get_repo(repo_name)
        issue = repo.get_issue(issue_number)
        issue.create_comment(body)

    def get_repo_memories(self, repo_name: str) -> List[Dict]:
        # In this implementation, memories are stored in the .lore folder of the repo
        # We can read them via the API if needed, but the Action will likely have them locally
        return []
