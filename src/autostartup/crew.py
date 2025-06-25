# src/autostartup/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tasks.conditional_task import ConditionalTask
from crewai.tasks.task_output import TaskOutput
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
from .tools.github_tools import CreateGitHubRepoTool
from .models import IdeaClassification

load_dotenv()

# Enhanced condition functions with confidence thresholds
def is_software_idea(output: TaskOutput) -> bool:
    """Check if the classified idea is 'software' with sufficient confidence"""
    if hasattr(output, 'pydantic') and output.pydantic:
        classification: IdeaClassification = output.pydantic
        return (classification.classification == "software" and 
                classification.confidence >= 0.7)  # Only proceed if confident
    
    # Fallback to raw text analysis
    return "software" in output.raw.lower()

def is_strategic_idea(output: TaskOutput) -> bool:
    """Check if the classified idea is 'strategic' with sufficient confidence"""
    if hasattr(output, 'pydantic') and output.pydantic:
        classification: IdeaClassification = output.pydantic
        return (classification.classification == "strategic" and 
                classification.confidence >= 0.7)
    
    return "strategic" in output.raw.lower()

def should_analyze_market(output: TaskOutput) -> bool:
    """Check if market analysis should be performed"""
    if hasattr(output, 'pydantic') and output.pydantic:
        classification: IdeaClassification = output.pydantic
        return (classification.classification in ["software", "strategic"] and 
                classification.confidence >= 0.6)
    
    # Fallback
    raw_lower = output.raw.lower()
    return "software" in raw_lower or "strategic" in raw_lower

@CrewBase
class Autostartup():
    """Autostartup crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    search_tool = SerperDevTool()

    @agent
    def orchestrator(self) -> Agent:
        return Agent(
            config=self.agents_config['orchestrator'],
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
            tools=[CreateGitHubRepoTool()],
            verbose=True
        )

    @task
    def classify_idea_task(self) -> Task:
        return Task(
            config=self.tasks_config['classify_idea_task'],
            output_pydantic=IdeaClassification
        )
    
    @task
    def competitive_analysis_task(self) -> Task:
        return ConditionalTask(
            config=self.tasks_config['competitive_analysis_task'],
            condition=should_analyze_market
        )
        
    @task
    def propose_mvp_architecture_task(self) -> Task:
        return ConditionalTask(
            config=self.tasks_config['propose_mvp_architecture_task'],
            condition=is_software_idea
        )

    @task
    def scaffold_github_repo_task(self) -> Task:
        return ConditionalTask(
            config=self.tasks_config['scaffold_github_repo_task'],
            condition=is_software_idea
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Autostartup crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )