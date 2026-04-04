import os
import requests
from typing import List, Dict, Any

GITHUB_API_URL = os.getenv("GITHUB_API_URL", "https://api.github.com")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")

class GitHubAPI:
    """Interacts with GitHub repository and workflows via REST API."""
    
    @staticmethod
    def _headers() -> Dict[str, str]:
        if not GITHUB_TOKEN:
            return {}
        return {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }

    @staticmethod
    def get_recent_commits(count: int = 5) -> List[Dict[str, Any]]:
        """Get the most recent commits from the configured GitHub repository via API."""
        if os.getenv("MOCK_GITHUB") == "true" or not GITHUB_REPOSITORY or not GITHUB_TOKEN:
            print("GitHubAPI: MOCK_GITHUB enabled or missing token/repo. Returning mock commit.")
            return [{
                "commit_id": "a82bcf",
                "author": "developer",
                "timestamp": "10 minutes ago",
                "message": "Update database connection pooling",
                "files_changed": ["paymentService.js", "db.config"]
            }]

        try:
            url = f"{GITHUB_API_URL}/repos/{GITHUB_REPOSITORY}/commits?per_page={count}"
            response = requests.get(url, headers=GitHubAPI._headers())
            response.raise_for_status()
            commits_data = response.json()
            
            commits = []
            for item in commits_data:
                commit_id = item.get("sha", "")[:7]
                author = item.get("commit", {}).get("author", {}).get("name", "Unknown")
                timestamp = item.get("commit", {}).get("author", {}).get("date", "")
                message = item.get("commit", {}).get("message", "")
                
                # To get files changed, we need to query the specific commit
                # Let's do this efficiently or just get the first one if we can
                commit_url = f"{GITHUB_API_URL}/repos/{GITHUB_REPOSITORY}/commits/{item.get('sha')}"
                commit_resp = requests.get(commit_url, headers=GitHubAPI._headers())
                files_changed = []
                if commit_resp.status_code == 200:
                    files_info = commit_resp.json().get("files", [])
                    files_changed = [f.get("filename") for f in files_info if f.get("filename")]

                commits.append({
                    "commit_id": commit_id,
                    "author": author,
                    "timestamp": timestamp,
                    "message": message,
                    "files_changed": files_changed
                })
            return commits
        except Exception as e:
            print(f"GitHub API Error: {e}")
            return []

    @staticmethod
    def revert_commit(commit_id: str) -> bool:
        """Instruction placeholder for reverting a commit.
        In a real GitHub Action, we would either create a revert PR or push a revert commit.
        """
        print(f"GitHubAPI: Would trigger a revert for {commit_id} on {GITHUB_REPOSITORY}")
        return True

    @staticmethod
    def dispatch_workflow(workflow_id: str, inputs: Dict[str, str]) -> bool:
        """Trigger another GitHub Action (e.g., to run a deployment)."""
        if not GITHUB_REPOSITORY or not GITHUB_TOKEN:
            return False
            
        url = f"{GITHUB_API_URL}/repos/{GITHUB_REPOSITORY}/actions/workflows/{workflow_id}/dispatches"
        try:
            response = requests.post(url, headers=GitHubAPI._headers(), json={
                "ref": "main",
                "inputs": inputs
            })
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"GitHub API Dispatch Error: {e}")
            return False
