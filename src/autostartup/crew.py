# src/autostartup/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
# from pydantic import BaseModel, Field # BaseModel, Field not used
from dotenv import load_dotenv
from .tools.github_tools import GitHubScaffolderTool
# Import TaskManager for type hinting if possible, or Any
# from .api.task_manager import TaskManager # This would cause circular import

load_dotenv()

# Define a simple callback function structure
def create_task_callback(task_manager, job_id, task_name, agent_name):
    def callback(task_output):
        # This callback is executed when the task is completed.
        # We need to signal *before* task execution for progress.
        # CrewAI's current callback system might be for post-execution.
        # For simplicity, we'll update progress here, implying the task *just finished*.
        # A more ideal solution would be a pre-execution hook.
        # print(f"Task {task_name} completed. Output: {task_output}")
        # task_manager.update_task_progress(job_id, task_name, agent_name, completed=True)
        pass # Callbacks are post-execution, we need pre-execution updates.
    return callback

@CrewBase
class Autostartup():
    """Autostartup crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    search_tool = SerperDevTool()

    # Add task_manager and job_id to store them
    def __init__(self, task_manager=None, job_id=None):
        super().__init__() # Ensure CrewBase is initialized if it has its own __init__
        self.task_manager = task_manager
        self.job_id = job_id
        # The @agent and @task decorators instantiate agents and tasks when the class is defined,
        # not when an instance is created. So, self.task_manager and self.job_id won't be available
        # directly in those decorated methods in the way we might expect for instance-specific callbacks.
        # We will need to pass them when the crew is created.

    @agent
    def market_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['market_researcher'],
            tools=[self.search_tool],
            verbose=True,
            allow_delegation=False
            )
    
    @agent
    def gap_finder(self) -> Agent:
        return Agent(config=self.agents_config['gap_finder'], verbose=True, allow_delegation=False)

    @agent
    def technical_architect(self) -> Agent:
        return Agent(config=self.agents_config['technical_architect'], verbose=True, allow_delegation=False)
        
    @agent
    def github_builder(self) -> Agent:
        return Agent(
            config=self.agents_config['github_builder'],tools=[GitHubScaffolderTool()],verbose=True, allow_delegation=False)

    # Tasks will be configured with callbacks in the crew() method
    @task
    def competitor_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['competitor_analysis_task'],
            agent=self.market_researcher()
            # Callback will be added in crew()
        )
        
    @task
    def gap_finding_task(self) -> Task:
        return Task(
            config=self.tasks_config['gap_finding_task'],
            agent=self.gap_finder()
            # Callback will be added in crew()
        )

    @task
    def technical_planning_and_scaffolding_task(self) -> Task:
        # This task seems to be a single task for technical planning and scaffolding
        # but the agent is technical_architect. The github_builder agent handles scaffolding.
        # Assuming this task is for planning, and a separate task uses github_builder.
        return Task(
            config=self.tasks_config['technical_planning_and_scaffolding_task'],
            agent=self.technical_architect()
            # Callback will be added in crew()
        )
    
    @task
    def scaffold_github_repo_task(self) -> Task:
        return Task(
            config=self.tasks_config['scaffold_github_repo_task'],
            agent=self.github_builder()
            # Callback will be added in crew()
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Autostartup crew and configures tasks with progress callbacks."""

        # Ensure task_manager and job_id are available
        if not self.task_manager or not self.job_id:
            # This might happen if Autostartup is instantiated without these args.
            # Consider raising an error or handling this case.
            # For now, we'll assume they are passed correctly from TaskManager.
            pass

        # Get the tasks
        # Note: The @task decorator makes these methods return Task instances.
        # We need to re-assign them or create new ones if we want to add callbacks
        # specific to this instance of the crew.
        
        # Retrieve agents
        mr_agent = self.market_researcher()
        gf_agent = self.gap_finder()
        ta_agent = self.technical_architect()
        gb_agent = self.github_builder()

        # Define tasks with callbacks that update progress
        # CrewAI task callbacks are typically for post-execution.
        # To update progress *before* a task starts, we'd ideally need a feature
        # in CrewAI like `task.on_start(callback_fn)`.
        # Lacking that, we'll have to modify how tasks are kicked off if possible,
        # or call the progress update just before `crew.kickoff` for the first task,
        # and then rely on task completion for subsequent updates (which isn't ideal for live progress).

        # The current structure of CrewAI (v0.28.8 and similar) using @task and @agent
        # primarily configures the crew structure at class definition time.
        # For runtime modifications like adding dynamic callbacks that depend on instance variables (job_id),
        # it's often cleaner to construct tasks and agents directly within the @crew method
        # or pass necessary data through task inputs if the framework supports it.

        # Let's try a different approach:
        # We will override the kickoff method of the Crew or individual tasks if possible,
        # or more simply, call the update method from within the TaskManager *around* the `crew.kickoff()` call.

        # For now, let's focus on what we can do within this file.
        # The `Task` object has a `callback` parameter in its constructor.
        # This callback is executed *after* the task is done.
        # To update progress *before* each task, we need to modify the `TaskManager._run_crew_analysis`
        # to call `_track_task_progress` before each task is handed to an agent.
        # This is not possible with `crew.kickoff()` which runs the whole sequence.

        # A practical way to handle this without deep CrewAI modification is to make the tasks
        # themselves call the progress update as their very first action.
        # This means the `execute` method of a custom tool or the beginning of a task's defined action.
        # This is more invasive.

        # Let's reconsider the plan:
        # The TaskManager will call `_track_task_progress` just before `crew.kickoff()`. This sets the first task.
        # For subsequent tasks, we need a way for the crew to signal back.
        # CrewAI's hierarchical process with a manager agent might offer a way.
        # The manager agent could be given a tool to report progress.

        # Simpler approach: The `TaskManager` will iterate through tasks. This is a significant change.
        # The original code runs `crew.kickoff()` and lets it manage the sequence.

        # Let's stick to the plan of modifying `TaskManager` to call `_track_task_progress`
        # more frequently. This file, `crew.py`, might not need `task_manager` and `job_id`
        # if `TaskManager` handles the orchestration of progress updates between tasks.

        # The original plan was:
        # 1. Autostartup gets task_manager, job_id.
        # 2. Before each task's execution, call task_manager.update_task_progress.

        # If `crew.kickoff()` is a black box for the sequence, we can't intercept between tasks
        # from *outside* the crew. We need to do it from *inside*.
        # This implies tasks themselves need to be aware of the progress update mechanism.

        # Let's assume tasks can take `task_manager` and `job_id` as context or parameters.
        # The `Task` constructor has a `context` parameter.

        # New approach for this step:
        # - The `Autostartup` class's `crew` method will instantiate tasks and provide them
        #   with a callback function. This callback will be linked to the `task_manager`.
        # - The `task_manager` and `job_id` will be passed to `Autostartup` when it's instantiated.

        # Task definitions:
        comp_task = Task(
            description=self.tasks_config['competitor_analysis_task']['description'].format(idea="{idea}"),
            expected_output=self.tasks_config['competitor_analysis_task']['expected_output'],
            agent=mr_agent,
            callback=lambda output: self.task_manager.update_task_progress(
                self.job_id, "competitor_analysis", mr_agent.role, task_output=output
            ) if self.task_manager else None
        )
        gap_task = Task(
            description=self.tasks_config['gap_finding_task']['description'].format(idea="{idea}"),
            expected_output=self.tasks_config['gap_finding_task']['expected_output'],
            agent=gf_agent,
            dependencies=[comp_task], # Explicitly define dependency
            callback=lambda output: self.task_manager.update_task_progress(
                self.job_id, "gap_finding", gf_agent.role, task_output=output
            ) if self.task_manager else None
        )
        tech_plan_task = Task(
            description=self.tasks_config['technical_planning_and_scaffolding_task']['description'].format(idea="{idea}"),
            expected_output=self.tasks_config['technical_planning_and_scaffolding_task']['expected_output'],
            agent=ta_agent,
            dependencies=[gap_task], # Explicitly define dependency
            callback=lambda output: self.task_manager.update_task_progress(
                self.job_id, "technical_planning", ta_agent.role, task_output=output # task name adjusted
            ) if self.task_manager else None
        )
        scaffold_task = Task(
            description=self.tasks_config['scaffold_github_repo_task']['description'].format(idea="{idea}"),
            expected_output=self.tasks_config['scaffold_github_repo_task']['expected_output'],
            agent=gb_agent,
            dependencies=[tech_plan_task], # Explicitly define dependency
            # context={"plan_file": "outputs/scaffolding_plan.json"}, # Removed: Caused Pydantic error. Tool should get plan from task output.
            callback=lambda output: self.task_manager.update_task_progress(
                self.job_id, "github_scaffolding", gb_agent.role, task_output=output
            ) if self.task_manager else None
        )

        # The manager agent
        manager = Agent(
            config=self.agents_config['manager'],
            allow_delegation=True, # Manager delegates to other agents
            verbose=True,
        )
        
        # The tasks list for the crew
        crew_tasks = [comp_task, gap_task, tech_plan_task, scaffold_task]

        return Crew(
            agents=[mr_agent, gf_agent, ta_agent, gb_agent], # Explicitly list agents involved in these tasks
            tasks=crew_tasks,
            process=Process.hierarchical, # Using hierarchical process with a manager
            verbose=True,
            manager_agent=manager,
            # memory=True # If you want to enable memory for the crew
        )