import threading
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
import traceback
import os
from ..crew import Autostartup
from .models import JobStatus, TaskStatus, TaskResult, JobStatusResponse

class TaskManager:
    def __init__(self):
        # In-memory storage for job data
        self.jobs: Dict[str, Dict[str, Any]] = {}
        self.lock = threading.Lock()
        
        # Task configuration - maps task names to agents
        self.task_config = {
            "competitor_analysis": "market_researcher",
            "gap_finding": "gap_finder", 
            "technical_planning": "technical_architect",
            "github_scaffolding": "github_builder"
        }
    
    def start_analysis(self, job_id: str, idea: str) -> bool:
        """Start a new startup analysis job in background"""
        try:
            with self.lock:
                self.jobs[job_id] = {
                    "job_id": job_id,
                    "idea": idea,
                    "status": JobStatus.PENDING,
                    "current_task": None,
                    "current_agent": None,
                    "progress_percentage": 0,
                    "completed_tasks": [],
                    "started_at": datetime.now(),
                    "estimated_completion": datetime.now() + timedelta(minutes=6),
                    "error": None,
                    "results": {}
                }
            
            # Start background thread
            thread = threading.Thread(target=self._run_crew_analysis, args=(job_id, idea))
            thread.daemon = True
            thread.start()
            
            return True
            
        except Exception as e:
            print(f"Error starting analysis: {e}")
            return False
    
    def _run_crew_analysis(self, job_id: str, idea: str):
        """Run the CrewAI analysis in background thread"""
        try:
            self._update_job_status(job_id, JobStatus.RUNNING)
            
            # Initialize CrewAI
            crew = Autostartup().crew()
            inputs = {'idea': idea}
            
            # Track each task completion
            self._track_task_progress(job_id, "competitor_analysis", "market_researcher")
            
            # Execute the crew
            result = crew.kickoff(inputs=inputs)
            
            # Parse results from output files
            self._parse_and_store_results(job_id)
            
            # Mark as completed
            with self.lock:
                self.jobs[job_id]["status"] = JobStatus.COMPLETED
                self.jobs[job_id]["completed_at"] = datetime.now()
                self.jobs[job_id]["progress_percentage"] = 100
                self.jobs[job_id]["current_task"] = None
                self.jobs[job_id]["current_agent"] = None
            
            print(f"Job {job_id} completed successfully")
            
        except Exception as e:
            error_msg = f"Crew execution failed: {str(e)}"
            print(f"Job {job_id} failed: {error_msg}")
            print(traceback.format_exc())
            
            with self.lock:
                self.jobs[job_id]["status"] = JobStatus.FAILED
                self.jobs[job_id]["error"] = error_msg
                self.jobs[job_id]["completed_at"] = datetime.now()
    
    def _track_task_progress(self, job_id: str, task_name: str, agent: str):
        """Update progress when a task starts"""
        with self.lock:
            self.jobs[job_id]["current_task"] = task_name
            self.jobs[job_id]["current_agent"] = agent
            
            # Calculate progress percentage
            completed_count = len(self.jobs[job_id]["completed_tasks"])
            self.jobs[job_id]["progress_percentage"] = (completed_count / 4) * 100
    
    def _parse_and_store_results(self, job_id: str):
        """Parse results from output files and store in memory"""
        results = {}
        
        # File mappings
        file_mappings = {
            "competitor_analysis": "outputs/competitive_analysis.md",
            "gap_finding": "outputs/gap_analysis.md", 
            "technical_planning": "outputs/scaffolding_plan.json",
            "github_scaffolding": "outputs/github_repo_url.md"
        }
        
        for task_name, file_path in file_mappings.items():
            try:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    task_result = TaskResult(
                        task_name=task_name,
                        agent=self.task_config[task_name],
                        status=TaskStatus.COMPLETED,
                        result=content,
                        completed_at=datetime.now()
                    )
                    
                    results[task_name] = task_result
                    
                    # Add to completed tasks
                    with self.lock:
                        self.jobs[job_id]["completed_tasks"].append(task_result.dict())
                        
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                
                task_result = TaskResult(
                    task_name=task_name,
                    agent=self.task_config[task_name],
                    status=TaskStatus.FAILED,
                    error=str(e)
                )
                results[task_name] = task_result
        
        with self.lock:
            self.jobs[job_id]["results"] = results
    
    def _update_job_status(self, job_id: str, status: JobStatus):
        """Update job status thread-safely"""
        with self.lock:
            if job_id in self.jobs:
                self.jobs[job_id]["status"] = status
    
    def get_job_status(self, job_id: str) -> Optional[JobStatusResponse]:
        """Get current status of a job"""
        with self.lock:
            if job_id not in self.jobs:
                return None
            
            job_data = self.jobs[job_id].copy()
            
            return JobStatusResponse(
                job_id=job_data["job_id"],
                status=job_data["status"],
                current_task=job_data.get("current_task"),
                current_agent=job_data.get("current_agent"),
                progress_percentage=job_data["progress_percentage"],
                completed_tasks=[TaskResult(**task) for task in job_data["completed_tasks"]],
                started_at=job_data["started_at"],
                completed_at=job_data.get("completed_at"),
                estimated_completion=job_data.get("estimated_completion"),
                error=job_data.get("error")
            )
    
    def get_job_results(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get all results for a completed job"""
        with self.lock:
            if job_id not in self.jobs:
                return None
            
            job_data = self.jobs[job_id]
            return {
                "job_id": job_id,
                "status": job_data["status"],
                "results": job_data.get("results", {}),
                "started_at": job_data["started_at"],
                "completed_at": job_data.get("completed_at")
            }
    
    def get_task_result(self, job_id: str, task_name: str) -> Optional[Dict[str, Any]]:
        """Get result for a specific task"""
        with self.lock:
            if job_id not in self.jobs:
                return None
            
            results = self.jobs[job_id].get("results", {})
            if task_name not in results:
                return None
            
            return results[task_name].dict() if hasattr(results[task_name], 'dict') else results[task_name]
    
    def delete_job(self, job_id: str) -> bool:
        """Delete a job from memory"""
        with self.lock:
            if job_id in self.jobs:
                del self.jobs[job_id]
                return True
            return False
    
    def list_jobs(self) -> Dict[str, Any]:
        """List all jobs (for debugging)"""
        with self.lock:
            return {
                "total_jobs": len(self.jobs),
                "jobs": {
                    job_id: {
                        "status": job_data["status"],
                        "started_at": job_data["started_at"],
                        "progress": job_data["progress_percentage"]
                    }
                    for job_id, job_data in self.jobs.items()
                }
            }