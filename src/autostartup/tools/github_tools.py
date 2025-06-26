#src/autostartup/tools/github_tools.py

import os
import requests
from github import Github, GithubException
from crewai.tools import BaseTool
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class ScaffolderInput(BaseModel):
    """Input schema for the GitHubScaffolderTool."""
    repo_name: str = Field(..., description="The URL-safe name for the new repository.")
    description: str = Field(..., description="A brief description for the repository.")
    files: List[Dict[str, Any]] = Field(..., description="A list of file objects, each with a 'path' and 'content'.")
    
class GitHubScaffolderTool(BaseTool):
    name: str = "GitHub Repository Scaffolder"
    description: str = "Creates and populates a new GitHub repository based on a structured JSON plan."
    args_schema: type[BaseModel] = ScaffolderInput

    def _run(self, **kwargs) -> str:
        # Pydantic v2/crewAI might pass validated args directly
        if 'repo_name' in kwargs and 'description' in kwargs and 'files' in kwargs:
             plan = ScaffolderInput(**kwargs)
        else:
            return "Error: Tool was called with invalid arguments. Expected 'repo_name', 'description', and 'files'."

        try:
            github_token = os.getenv("GITHUB_TOKEN")
            if not github_token:
                return "Error: GITHUB_TOKEN environment variable not set."

            g = Github(github_token)
            user = g.get_user()
            
            print(f"Attempting to create or get repository: {plan.repo_name}")
            try:
                repo = user.create_repo(
                    name=plan.repo_name,
                    description=plan.description,
                    private=False
                )
                print(f"Repository '{plan.repo_name}' created successfully.")
            except GithubException as e:
                if e.status == 422: # Repository already exists
                    print(f"Repository '{plan.repo_name}' already exists. Using it.")
                    repo = user.get_repo(plan.repo_name)
                else:
                    return f"Error creating repository: {e}"

            # Create files
            for file_info in plan.files:
                path = file_info.get('path')
                content = file_info.get('content', '')
                
                if not path:
                    continue

                print(f"Creating file in repo: {path}")
                try:
                    repo.create_file(
                        path=path,
                        message=f"feat: scaffold {path}",
                        content=content
                    )
                except GithubException as e:
                    if e.status == 422: # File already exists
                        print(f"File '{path}' already exists. Skipping.")
                    else:
                        print(f"Failed to create file '{path}': {e}")
            
            return f"✅ Successfully created and populated repository: {repo.html_url}"

        except Exception as e:
            return f"An unexpected error occurred: {e}"