#!/usr/bin/env python3
"""
FastAPI Server Startup Script for CrewAI Startup Analyzer
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", "8000"))
    reload = os.getenv("API_RELOAD", "True").lower() == "true"
    
    print(f"Starting CrewAI Startup Analyzer API...")
    print(f"Server will be available at: http://{host}:{port}")
    print(f"API Documentation: http://{host}:{port}/docs")
    print(f"Alternative docs: http://{host}:{port}/redoc")
    
    # Run the FastAPI server
    uvicorn.run(
        "src.autostartup.api.main:app",
        host=host,
        port=port,
        reload=reload,
        reload_dirs=["src"] if reload else None
    )