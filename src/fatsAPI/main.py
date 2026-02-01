from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .routers import users, tasks
from .database import engine
from . import db_models
from pathlib import Path
import os

#Create database tables
db_models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Management System",
    description="A comprehensive task management API built with FastAPI demonstrating modular routing, Pydantic validation, and best practices",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "users",
            "description": "User management operations - create users, assign roles, and manage profiles"
        },
        {
            "name": "tasks",
            "description": "Task management operations - create, update, and track tasks with priorities and assignments"
        }
    ]
)

# Configure CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers with prefixes and tags
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

# Mount static files for frontend
frontend_path = Path(__file__).parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")


@app.get("/", include_in_schema=False)
async def root():
    """
    Serve the frontend application.
    """
    from fastapi.responses import FileResponse
    index_path = frontend_path / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    
    # Fallback if frontend not yet created
    return {
        "message": "Welcome to the Task Management API",
        "docs": "/docs",
        "description": "A FastAPI-based task management system for teams and individuals",
        "endpoints": {
            "users": "/users",
            "tasks": "/tasks"
        }
    }


@app.get("/health", include_in_schema=False)
async def health_check():
    """
    Health check endpoint for Railway deployment.
    """
    return {"status": "healthy", "database": "connected"}

