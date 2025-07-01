import threading
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, Any, List
import traceback
import os
from ..crew import Autostartup
from .models import JobStatus, TaskStatus, TaskResult, JobStatusResponse

class TaskManager:
    def __init__(self):
        self.jobs: Dict[str, Dict[str, Any]] = {}
        self.lock = threading.Lock()
        
        # Ordered list of tasks and their agents for progress tracking
        self.task_sequence = [
            {"name": "competitor_analysis", "agent": "Market Researcher"}, # Agent role as in config
            {"name": "gap_finding", "agent": "Gap Finder"},
            {"name": "technical_planning", "agent": "Technical Architect"},
            {"name": "github_scaffolding", "agent": "GitHub Builder"}
        ]
        self.total_tasks = len(self.task_sequence)

    def start_analysis(self, job_id: str, idea: str) -> bool:
        try:
            with self.lock:
                self.jobs[job_id] = {
                    "job_id": job_id,
                    "idea": idea,
                    "status": JobStatus.PENDING,
                    "current_task_description": "Initializing...", # More descriptive
                    "current_agent_name": None,
                    "progress_percentage": 0,
                    "completed_task_results": [], # Store TaskResult objects
                    "started_at": datetime.now(),
                    "estimated_completion": datetime.now() + timedelta(minutes=6), # Rough estimate
                    "error": None,
                    "raw_results_storage": {} # To store raw outputs from tasks
                }
            
            thread = threading.Thread(target=self._run_crew_analysis, args=(job_id, idea))
            thread.daemon = True
            thread.start()
            return True
        except Exception as e:
            print(f"Error starting analysis: {e}")
            # Potentially update job status to FAILED here if self.jobs[job_id] was set
            return False

    def _run_crew_analysis(self, job_id: str, idea: str):
        try:
            self._update_job_status_safe(job_id, JobStatus.RUNNING)
            # Set initial task (e.g., competitor_analysis) as current
            self.update_task_progress(job_id, self.task_sequence[0]["name"], self.task_sequence[0]["agent"], task_output=None, starting=True)

            # Pass `self` (task_manager instance) and `job_id` to Autostartup
            autostartup_crew_builder = Autostartup(task_manager=self, job_id=job_id)
            crew = autostartup_crew_builder.crew()
            inputs = {'idea': idea}
            
            # Kickoff the crew. Callbacks within Autostartup tasks will call update_task_progress.
            crew_result = crew.kickoff(inputs=inputs) # crew_result might contain final outputs
            
            # Finalize job state
            with self.lock:
                if self.jobs[job_id]["status"] not in [JobStatus.FAILED, JobStatus.COMPLETED]: # Ensure not already failed
                    self.jobs[job_id]["status"] = JobStatus.COMPLETED
                    self.jobs[job_id]["completed_at"] = datetime.now()
                    self.jobs[job_id]["progress_percentage"] = 100
                    self.jobs[job_id]["current_task_description"] = "All tasks completed."
                    self.jobs[job_id]["current_agent_name"] = None
                # Store final crew result if needed, though individual task results are preferred
                self.jobs[job_id]["raw_results_storage"]["final_crew_output"] = crew_result

            print(f"Job {job_id} processing finished. Status: {self.jobs[job_id]['status']}")

        except Exception as e:
            error_msg = f"Crew execution failed: {str(e)}"
            print(f"Job {job_id} failed: {error_msg}")
            print(traceback.format_exc())
            with self.lock:
                self.jobs[job_id]["status"] = JobStatus.FAILED
                self.jobs[job_id]["error"] = error_msg
                self.jobs[job_id]["completed_at"] = datetime.now()
                self.jobs[job_id]["current_task_description"] = "Analysis failed."

    def update_task_progress(self, job_id: str, task_name: str, agent_name: str, task_output: Optional[Any] = None, starting: bool = False):
        """
        Update job progress. Called by task callbacks upon completion,
        or at the start of the first task.
        """
        with self.lock:
            if job_id not in self.jobs:
                return

            job_data = self.jobs[job_id]
            
            if starting:
                # This is called before the first task begins
                job_data["current_task_description"] = task_name.replace('_', ' ').title()
                job_data["current_agent_name"] = agent_name
                job_data["progress_percentage"] = 0 # Initial state
                return

            # Task has completed (task_output is not None)
            if task_output is not None:
                # Create TaskResult for the completed task
                completed_task_result = TaskResult(
                    task_name=task_name,
                    agent=agent_name, # This should be the agent's role/name
                    status=TaskStatus.COMPLETED, # Assuming success if callback is hit with output
                    result=str(task_output), # Store output as string
                    completed_at=datetime.now()
                )
                job_data["completed_task_results"].append(completed_task_result)
                job_data["raw_results_storage"][task_name] = str(task_output)


            completed_tasks_count = len(job_data["completed_task_results"])
            job_data["progress_percentage"] = int((completed_tasks_count / self.total_tasks) * 100)

            # Determine next task to set as current for frontend display
            if completed_tasks_count < self.total_tasks:
                next_task_info = self.task_sequence[completed_tasks_count]
                job_data["current_task_description"] = next_task_info["name"].replace('_', ' ').title()
                job_data["current_agent_name"] = next_task_info["agent"]
            else:
                # All tasks are complete
                job_data["current_task_description"] = "Finalizing results..."
                job_data["current_agent_name"] = None
                job_data["status"] = JobStatus.COMPLETED # Should be set in _run_crew_analysis too
                job_data["progress_percentage"] = 100


    def _parse_and_store_results(self, job_id: str):
        """
        This method was originally for parsing from files.
        Now, results are stored via callbacks. This method might be redundant
        or repurposed if direct file parsing is still a fallback.
        For now, results are handled by `update_task_progress`.
        """
        pass # Results are now primarily handled by callbacks.

    def _update_job_status_safe(self, job_id: str, status: JobStatus):
        with self.lock:
            if job_id in self.jobs:
                self.jobs[job_id]["status"] = status

    def get_job_status(self, job_id: str) -> Optional[JobStatusResponse]:
        with self.lock:
            if job_id not in self.jobs:
                return None
            
            job_data = self.jobs[job_id]
            
            # Ensure completed_tasks are TaskResult instances for the response model
            completed_tasks_for_response: List[TaskResult] = []
            for res in job_data.get("completed_task_results", []):
                if isinstance(res, TaskResult):
                    completed_tasks_for_response.append(res)
                elif isinstance(res, dict): # Should not happen with new logic
                    completed_tasks_for_response.append(TaskResult(**res))

            return JobStatusResponse(
                job_id=job_data["job_id"],
                status=job_data["status"],
                current_task=job_data.get("current_task_description"), # Updated field name
                current_agent=job_data.get("current_agent_name"),     # Updated field name
                progress_percentage=job_data.get("progress_percentage", 0),
                completed_tasks=completed_tasks_for_response,
                total_tasks=self.total_tasks,
                started_at=job_data["started_at"],
                completed_at=job_data.get("completed_at"),
                estimated_completion=job_data.get("estimated_completion"), # Could be updated dynamically
                error=job_data.get("error")
            )

    def get_job_results(self, job_id: str) -> Optional[Dict[str, Any]]:
        with self.lock:
            if job_id not in self.jobs or self.jobs[job_id]["status"] != JobStatus.COMPLETED:
                # Only return full results if job is completed and exists
                # Consider if partial results should be available for running/failed jobs
                status_val = self.jobs[job_id]["status"] if job_id in self.jobs else "not_found"
                print(f"Job {job_id} results requested but status is {status_val}")
                return None
            
            job_data = self.jobs[job_id]

            # Format results according to expected frontend structure if necessary
            # The frontend expects results like: {"competitor_analysis": {"result": "..."}}
            formatted_results: Dict[str, Dict[str, Any]] = {}
            for task_result_obj in job_data.get("completed_task_results", []):
                if isinstance(task_result_obj, TaskResult):
                    formatted_results[task_result_obj.task_name] = {
                        "result": task_result_obj.result,
                        # Potentially add other TaskResult fields if frontend needs them
                    }

            return {
                "job_id": job_id,
                "status": job_data["status"],
                "results": formatted_results, # Use the formatted results
                "started_at": job_data["started_at"],
                "completed_at": job_data.get("completed_at"),
                # "total_duration_seconds": (job_data["completed_at"] - job_data["started_at"]).total_seconds() if job_data.get("completed_at") else None
            }

    def get_task_result(self, job_id: str, task_name: str) -> Optional[Dict[str, Any]]:
        with self.lock:
            if job_id not in self.jobs:
                return None
            
            # Results are now stored in completed_task_results as TaskResult objects
            for task_res_obj in self.jobs[job_id].get("completed_task_results", []):
                if isinstance(task_res_obj, TaskResult) and task_res_obj.task_name == task_name:
                    return task_res_obj.dict() # Return as dict
            return None

    def delete_job(self, job_id: str) -> bool:
        with self.lock:
            if job_id in self.jobs:
                del self.jobs[job_id]
                return True
            return False

    def list_jobs(self) -> Dict[str, Any]:
        with self.lock:
            job_list_summary = {}
            for job_id_key, job_data_val in self.jobs.items():
                job_list_summary[job_id_key] = {
                    "status": job_data_val["status"],
                    "started_at": job_data_val["started_at"].isoformat() if job_data_val.get("started_at") else None,
                    "progress": job_data_val.get("progress_percentage", 0),
                    "current_task": job_data_val.get("current_task_description", "N/A")
                }
            return {
                "total_jobs": len(self.jobs),
                "jobs": job_list_summary
            }