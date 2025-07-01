# Autostartup Crew

Welcome to the Autostartup Crew project! This project, powered by [crewAI](https://crewai.com), is designed to take your startup idea and transform it into a fully scaffolded GitHub repository, complete with a technical plan and initial project structure.

## Problem Solved

Starting a new software project involves several time-consuming initial steps: market research, identifying a unique value proposition, creating a technical plan, and setting up the initial code repository. Autostartup Crew automates this entire workflow, allowing you to quickly move from idea to a structured project foundation.

## How It Works: The CrewAI Logic

Autostartup Crew utilizes a team of specialized AI agents, orchestrated by a manager agent, to perform the necessary tasks in a hierarchical process:

1.  **User Input**: You provide a startup idea.
2.  **Market Research**: The `Market Researcher` agent analyzes the idea, identifies 2-3 direct competitors, and reports on their strengths and weaknesses.
3.  **Gap Analysis**: The `Gap Finder` agent takes the competitor analysis and identifies strategic market gaps or unmet needs that your startup could target.
4.  **Technical Planning**: The `Technical Architect` agent designs a technical blueprint based on the identified gap. This includes recommending a technology stack, designing a project structure, and drafting an initial `README.md` for the new project. This plan is formulated as a structured JSON output.
5.  **GitHub Scaffolding**: The `GitHub Builder` agent takes the JSON blueprint and programmatically creates a new GitHub repository, including all specified directories and files.

The entire process is overseen by a `Manager` agent, which delegates tasks to the appropriate specialist agent, ensuring a smooth workflow from idea to repository.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

```bash
uv pip sync -r requirements_api.txt
```

### API Keys

**Add your `OPENAI_API_KEY`, `SERPER_API_KEY` (for the search tool), and `GITHUB_TOKEN` into a `.env` file in the project root.** Create the `.env` file if it doesn't exist.

```
OPENAI_API_KEY="your_openai_api_key_here"
SERPER_API_KEY="your_serper_api_key_here"
GITHUB_TOKEN="your_github_personal_access_token_here"
```

## Running the Project

To kickstart your Autostartup Crew and generate a new project:

1.  **Configure the Idea**: Modify the `inputs` dictionary in `src/autostartup/main.py` with your startup idea if running locally:
    ```python
    # src/autostartup/main.py
    def run():
        inputs = {
            'idea': 'YOUR_AWESOME_STARTUP_IDEA_HERE',
        }
        # ... rest of the code
    ```
2.  **Run the Crew**:
    *   **Locally via script**: Execute the following command from the root folder of your project:
        ```bash
        python src/autostartup/main.py
        ```
    *   **Via API service**:
        First, start the API:
        ```bash
        uvicorn run_api:app --reload --port 8000
        ```
        Then, send a POST request to the `http://localhost:8000/start_analysis/` endpoint with a JSON body like:
        ```json
        {
            "idea": "Your awesome startup idea here"
        }
        ```

Upon completion, the `GitHub Builder` agent will output the URL of the newly created and scaffolded GitHub repository to `outputs/github_repo_url.md`. Other intermediate outputs like competitive analysis (`outputs/competitive_analysis.md`) and gap analysis (`outputs/gap_analysis.md`) will also be saved in the `outputs/` directory. The scaffolding plan itself is saved to `outputs/scaffolding_plan.json`.

## Understanding Your Crew

The Autostartup Crew is composed of the following AI agents and tasks:

*   **Agents (`src/autostartup/config/agents.yaml`):**
    *   `market_researcher`: Conducts competitive analysis.
    *   `gap_finder`: Identifies market opportunities.
    *   `technical_architect`: Designs the technical blueprint and project structure.
    *   `github_builder`: Scaffolds the GitHub repository using a custom tool.
    *   `manager`: Oversees the process and delegates tasks.
*   **Tasks (`src/autostartup/config/tasks.yaml`):**
    *   `competitor_analysis_task`: Researches competitors.
    *   `gap_finding_task`: Finds market gaps.
    *   `technical_planning_and_scaffolding_task`: Creates the technical plan (JSON output).
    *   `scaffold_github_repo_task`: Creates the GitHub repository.

You can customize the behavior of these agents and tasks by modifying their respective configuration files. The core logic, tools, and agent interactions are defined in `src/autostartup/crew.py`.

## Support

For support, questions, or feedback regarding the Autostartup Crew or crewAI:
- Visit crewAI [documentation](https://docs.crewai.com)
- Reach out via their [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join their Discord](https://discord.com/invite/X4JWnZnxPb)

Let's automate the startup grind with the power and simplicity of crewAI!
