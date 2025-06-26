# src/autostartup/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tasks.task_output import TaskOutput
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

from .tools.github_tools import GitHubScaffolderTool
# Updated import for the new tool objects
from .tools.orchestrator_tools import (
    trigger_software_workflow_tool,
    trigger_strategic_workflow_tool,
    handle_vague_idea_tool,
    bypass_competitive_analysis_tool
)
from .models import IdeaClassification

load_dotenv()

@CrewBase
class Autostartup():
    """Autostartup crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    search_tool = SerperDevTool()
    # The OrchestratorTools() instantiation is no longer needed

    @agent
    def orchestrator(self) -> Agent:
        return Agent(
            config=self.agents_config['orchestrator'],
            # Pass the imported Tool objects directly
            tools=[
                trigger_software_workflow_tool,
                trigger_strategic_workflow_tool,
                handle_vague_idea_tool,
                bypass_competitive_analysis_tool
            ],
            verbose=True
        )

    @agent
    def market_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['market_analyst'],
            tools=[self.search_tool],
            verbose=True
        )
        
    @agent
    def mvp_architect(self) -> Agent:
        return Agent(
            config=self.agents_config['mvp_architect'],
            tools=[GitHubScaffolderTool()],
            verbose=True
        )

    @task
    def classify_idea_task(self) -> Task:
        return Task(
            config=self.tasks_config['classify_idea_task'],
            output_pydantic=IdeaClassification
        )
    
    @task
    def orchestrate_next_steps_task(self) -> Task:
        return Task(
            config=self.tasks_config['orchestrate_next_steps_task'],
        )

    @task
    def competitive_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['competitive_analysis_task'],
        )
        
    @task
    def propose_mvp_architecture_task(self) -> Task:
        return Task(
            config=self.tasks_config['propose_mvp_architecture_task'],
        )

    @task
    def extract_scaffolding_plan_task(self) -> Task:
        return Task(
            config=self.tasks_config['extract_scaffolding_plan_task'],
        )
    
    
    @task
    def scaffold_github_repo_task(self) -> Task:
        return Task(
            config=self.tasks_config['scaffold_github_repo_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Autostartup crew"""
        return Crew(
            agents=self.agents,
            tasks=[
                self.classify_idea_task(),
                self.orchestrate_next_steps_task(),
                # These tasks would be part of sub-workflows triggered based on the orchestrator
                self.competitive_analysis_task(), 
                self.propose_mvp_architecture_task(),
                self.extract_scaffolding_plan_task(),
                self.scaffold_github_repo_task()
            ],
            process=Process.sequential,
            verbose=True
        )