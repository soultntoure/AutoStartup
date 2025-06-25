#src/autostartup/tools/github_tools.py

import os
import requests
from crewai.tools import BaseTool
from dotenv import load_dotenv

load_dotenv()  # Loads GITHUB_TOKEN from .env

class CreateGitHubRepoTool(BaseTool):
    name: str = "create_github_repo"  # Add type annotation
    description: str = "Creates a GitHub repository under the authenticated user's account" # Add type annotation

    def _run(self, repo_name: str, description: str = ""):
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            return "❌ GITHUB_TOKEN not set."

        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json"
        }
        data = {
            "name": repo_name,
            "description": description,
            "private": False,
            "auto_init": True
        }

        response = requests.post("https://api.github.com/user/repos", headers=headers, json=data)

        if response.status_code == 201:
            return f"✅ Repo created: https://github.com/YOUR_USERNAME/{repo_name}"
        else:
            return f"❌ Failed to create repo: {response.status_code} - {response.text}"