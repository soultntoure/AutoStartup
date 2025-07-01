from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running" 
    COMPLETED = "completed"
    FAILED = "failed"

class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class StartupAnalysisRequest(BaseModel):
    idea: str = Field(..., description="The startup idea to analyze", min_length=10)
    
    class Config:
        json_schema_extra = {
            "example": {
                "idea": "An app that helps people find and book local fitness classes easily"
            }
        }

class TaskResult(BaseModel):
    task_name: str
    agent: str
    status: TaskStatus
    result: Optional[str] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[float] = None

class JobStatusResponse(BaseModel):
    job_id: str
    status: JobStatus
    current_task: Optional[str] = None
    current_agent: Optional[str] = None
    progress_percentage: int = Field(default=0, ge=0, le=100)
    completed_tasks: List[TaskResult] = []
    total_tasks: int = 4
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    estimated_completion: Optional[datetime] = None
    error: Optional[str] = None
    
class JobResultsResponse(BaseModel):
    job_id: str
    status: JobStatus
    results: Dict[str, TaskResult]
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    total_duration_seconds: Optional[float] = None