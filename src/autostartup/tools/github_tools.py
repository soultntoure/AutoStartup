#src/autostartup/tools/github_tools.py

import os
import requests
from github import Github, GithubException
from crewai.tools import BaseTool
from dotenv import load_dotenv
from textwrap import dedent

class GitHubScaffolderTool(BaseTool):
    name: str = "GitHub Repository Scaffolder"
    description: str = dedent("""
        This tool creates a new GitHub repository and populates it with a specified
        directory structure and file content. It is the primary tool for setting up
        the foundational codebase for a project.

        Input to this tool should be a JSON object with two keys:
        - 'repo_name': The URL-safe name for the new repository.
        - 'architecture_plan': A string detailing the complete MVP architecture,
          including the folder structure and content for each file.
    """)

    def _run(self, **kwargs) -> str:
        # For Pydantic v1 compatibility with crewAI, we get kwargs
        repo_name = kwargs.get('repo_name')
        architecture_plan = kwargs.get('architecture_plan')

        if not repo_name or not architecture_plan:
            return "Error: 'repo_name' and 'architecture_plan' must be provided in the input."

        try:
            github_token = os.getenv("GITHUB_TOKEN")
            if not github_token:
                return "Error: GITHUB_TOKEN environment variable not set. Please set it to your GitHub personal access token."

            g = Github(github_token)
            user = g.get_user()

            # Check if repo already exists
            try:
                repo = user.get_repo(repo_name)
                print(f"Repository '{repo_name}' already exists. Skipping creation.")
            except GithubException as e:
                if e.status == 404:
                    # Create the repository if it does not exist
                    print(f"Creating new repository: {repo_name}")
                    repo = user.create_repo(
                        name=repo_name,
                        description=f"Repository for {repo_name}",
                        private=False
                    )
                else:
                    raise e
        except Exception as e:
            return f"An error occurred: {e}"     