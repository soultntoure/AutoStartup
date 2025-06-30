# src/autostartup/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from .tools.github_tools import GitHubScaffolderTool


load_dotenv()


@CrewBase
class Autostartup():
    """Autostartup crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    search_tool = SerperDevTool()


    @agent
    def market_researcher(self) -> Agent:
        return Agent(config=self.agents_config['market_researcher'],tools=[self.search_tool], verbose=True)
    
    @agent
    def gap_finder(self) -> Agent:
        return Agent(config=self.agents_config['gap_finder'], verbose=True)

    @agent
    def technical_architect(self) -> Agent:
        return Agent(config=self.agents_config['technical_architect'], verbose=True)
        
    @agent
    def github_builder(self) -> Agent:
        return Agent(
            config=self.agents_config['github_builder'],tools=[GitHubScaffolderTool()],verbose=True)    

 
    @task
    def competitor_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['competitor_analysis_task'],
        )
        
    @task
    def gap_finding_task(self) -> Task:
        return Task(
            config=self.tasks_config['gap_finding_task'],
        )

    @task
    def technical_planning_and_scaffolding_task(self) -> Task:
        return Task(
            config=self.tasks_config['technical_planning_and_scaffolding_task'],
        )
    
    
    @task
    def scaffold_github_repo_task(self) -> Task:
        return Task(
            config=self.tasks_config['scaffold_github_repo_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Autostartup crew"""
        
        manager = Agent(
            config=self.agents_config['manager'],
            allow_delegation=True,
            verbose=True,
        )
        
        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            process=Process.hierarchical,
            verbose=True,
            manager_agent=manager,
        )