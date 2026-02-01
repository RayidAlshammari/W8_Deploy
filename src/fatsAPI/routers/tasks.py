from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Annotated, Optional, List
from sqlalchemy.orm import Session
from ..schemas.models import TaskCreate, TaskResponse
from ..database import get_db
from ..db_models import Task, User

router = APIRouter()


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    status: Annotated[Optional[str], Query(description="Filter by task status")] = None,
    priority: Annotated[Optional[int], Query(ge=1, le=5, description="Filter by priority (1-5)")] = None,
    assigned_to: Annotated[Optional[int], Query(description="Filter by assigned user ID")] = None,
    db: Session = Depends(get_db)
):
    """
    Get all tasks with optional filtering.
    
    Args:
        status: Filter tasks by status (pending, in_progress, completed)
        priority: Filter tasks by priority level (1-5)
        assigned_to: Filter tasks assigned to a specific user ID
        db: Database session
        
    Returns:
        List of tasks matching the filter criteria
    """
    query = db.query(Task)
    
    # Apply filters
    if status:
        query = query.filter(Task.status == status)
    
    if priority is not None:
        query = query.filter(Task.priority == priority)
    
    if assigned_to is not None:
        query = query.filter(Task.assigned_to == assigned_to)
    
    tasks = query.all()
    return tasks


@router.post("/", status_code=201, response_model=TaskResponse)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task.
    
    Args:
        task: Task data conforming to TaskCreate schema
        db: Database session
        
    Returns:
        The created task with assigned ID
        
    Raises:
        HTTPException: 400 if assigned user doesn't exist
        
    Note:
        - The title will be validated to ensure it starts with a capital letter
        - Priority must be between 1 and 5
        - Status must be one of: pending, in_progress, completed
    """
    # Verify assigned user exists if provided
    if task.assigned_to:
        user = db.query(User).filter(User.id == task.assigned_to).first()
        if not user:
            raise HTTPException(
                status_code=400,
                detail=f"User with ID {task.assigned_to} not found"
            )
    
    # Create new task instance
    db_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        status=task.status,
        assigned_to=task.assigned_to
    )
    
    # Add to database
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    return db_task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    Get a specific task by ID.
    
    Args:
        task_id: The unique identifier of the task
        db: Database session
        
    Returns:
        Task details
        
    Raises:
        HTTPException: 404 if task not found
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ID {task_id} not found"
        )
    
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskCreate,
    db: Session = Depends(get_db)
):
    """
    Update an existing task.
    
    Args:
        task_id: The unique identifier of the task to update
        task_update: Updated task data
        db: Database session
        
    Returns:
        The updated task
        
    Raises:
        HTTPException: 404 if task not found
        HTTPException: 400 if assigned user doesn't exist
    """
    # Find the task
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ID {task_id} not found"
        )
    
    # Verify assigned user exists if provided
    if task_update.assigned_to:
        user = db.query(User).filter(User.id == task_update.assigned_to).first()
        if not user:
            raise HTTPException(
                status_code=400,
                detail=f"User with ID {task_update.assigned_to} not found"
            )
    
    # Update task fields
    task.title = task_update.title
    task.description = task_update.description
    task.priority = task_update.priority
    task.status = task_update.status
    task.assigned_to = task_update.assigned_to
    
    # Commit changes
    db.commit()
    db.refresh(task)
    
    return task
