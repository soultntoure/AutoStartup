from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


@CrewBase
class Autostartup():
    """Autostartup crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'



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
            verbose=True
        )

    @task
    def competitive_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['competitive_analysis_task'], 
        )


    @crew
    def crew(self) -> Crew:
        """Creates the Autostartup crew"""
       
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
