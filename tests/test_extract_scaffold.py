from src.autostartup.crew import Autostartup

crew = Autostartup()

# Simulate a previous idea input and run extract scaffolding
crew_instance = crew.crew()

# You can directly call the task object like this:
scaffold_task = crew.extract_scaffolding_plan_task()
output = scaffold_task.execute(context=[
    TaskOutput(name="propose_mvp_architecture_task", output="Fake plan with folder structure and README... etc")
])

print(output)
