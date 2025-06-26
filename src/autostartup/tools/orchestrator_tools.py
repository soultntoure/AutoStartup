# src/autostartup/tools/orchestrator_tools.py
from crewai.tools import BaseTool
from typing import Type
from pydantic.v1 import BaseModel, Field

# --- Tool for Triggering Software Workflow ---
class TriggerSoftwareWorkflowTool(BaseTool):
    name: str = "Trigger Software Workflow"
    description: str = (
        "Triggers the specialized software development workflow for a classified software idea. "
        "This will initiate competitive analysis, MVP architecture design, and GitHub scaffolding."
    )

    def _run(self, idea_description: str) -> str:
        """The actual logic for the tool."""
        return f"Initiating software workflow for idea: {idea_description}. Specialists will proceed."

# --- Tool for Triggering Strategic Workflow ---
class TriggerStrategicWorkflowTool(BaseTool):
    name: str = "Trigger Strategic Workflow"
    description: str = (
        "Triggers the specialized strategic analysis workflow for a classified strategic idea. "
        "This will initiate competitive analysis and business model review."
    )

    def _run(self, idea_description: str) -> str:
        """The actual logic for the tool."""
        return f"Initiating strategic workflow for idea: {idea_description}. Specialists will proceed."

# --- Tool for Handling Vague Ideas ---
class HandleVagueIdeaTool(BaseTool):
    name: str = "Handle Vague Idea"
    description: str = "Handles ideas classified as vague, prompting the user for more clarification."

    def _run(self, idea_description: str) -> str:
        """The actual logic for the tool."""
        return f"Idea '{idea_description}' is too vague. Please provide more details."

# --- Tool for Bypassing Competitive Analysis ---
class BypassCompetitiveAnalysisTool(BaseTool):
    name: str = "Bypass Competitive Analysis"
    description: str = "Indicates that competitive analysis is not required for the current idea based on the classification."

    def _run(self, reason: str) -> str:
        """The actual logic for the tool."""
        return f"Competitive analysis bypassed: {reason}"

# --- Instantiate your tools ---
# Your crew.py will import these instances
trigger_software_workflow_tool = TriggerSoftwareWorkflowTool()
trigger_strategic_workflow_tool = TriggerStrategicWorkflowTool()
handle_vague_idea_tool = HandleVagueIdeaTool()
bypass_competitive_analysis_tool = BypassCompetitiveAnalysisTool()