from fastapi import FastAPI, HTTPException, Depends, Security, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import os
from typing import Dict, Any, Optional
from .task_manager import TaskManager
from .models import StartupAnalysisRequest, JobStatusResponse, TaskResult

app = FastAPI(
    title="CrewAI Startup Analyzer API",
    description="API for analyzing startup ideas using AI agents",
    version="1.0.0"
)

# CORS middleware for frontend integration later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple API key authentication
API_KEY = os.getenv("API_KEY", "92013b1783117dce8440736634d9953ad09887b6")  # Default for development, change in production

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


# In-memory storage for job results
task_manager = TaskManager()

@app.get("/")
async def root():
    return {"message": "CrewAI Startup Analyzer API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.post("/api/startup/analyze", response_model=dict)
async def start_startup_analysis(
    request: StartupAnalysisRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Start analyzing a startup idea with CrewAI agents.
    Returns job_id immediately for tracking progress.
    """
    job_id = str(uuid.uuid4())
    
    # Start the background task
    success = task_manager.start_analysis(job_id, request.idea)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to start analysis")
    
    return {
        "job_id": job_id,
        "status": "started",
        "message": "Startup analysis started. Use job_id to track progress.",
        "estimated_duration": "4-6 minutes"
    }

@app.get("/api/startup/status/{job_id}", response_model=JobStatusResponse)
async def get_job_status(
    job_id: str,
    api_key: str = Depends(verify_api_key)
):
    """
    Get the current status of a startup analysis job.
    Shows which agent is currently working and completed tasks.
    """
    status = task_manager.get_job_status(job_id)
    
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return status

@app.get("/api/startup/results/{job_id}")
async def get_job_results(
    job_id: str,
    api_key: str = Depends(verify_api_key)
):
    """
    Get all completed results for a job.
    Only returns results for completed tasks.
    """
    results = task_manager.get_job_results(job_id)
    
    if results is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return results

@app.get("/api/startup/results/{job_id}/task/{task_name}")
async def get_task_result(
    job_id: str,
    task_name: str,
    api_key: str = Depends(verify_api_key)
):
    """
    Get result for a specific task.
    Available tasks: competitor_analysis, gap_finding, technical_planning, github_scaffolding
    """
    result = task_manager.get_task_result(job_id, task_name)
    
    if result is None:
        raise HTTPException(status_code=404, detail="Job or task not found")
    
    return result

@app.delete("/api/startup/jobs/{job_id}")
async def delete_job(
    job_id: str,
    api_key: str = Depends(verify_api_key)
):
    """
    Delete a job and its results from memory.
    """
    success = task_manager.delete_job(job_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {"message": "Job deleted successfully"}

@app.get("/api/startup/jobs")
async def list_jobs(api_key: str = Depends(verify_api_key)):
    """
    List all jobs in memory (for debugging).
    """
    return task_manager.list_jobs()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)