from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Annotated, Optional, List
from sqlalchemy.orm import Session
from ..schemas.models import UserCreate, UserResponse
from ..database import get_db
from ..db_models import User

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def get_users(
    role: Annotated[Optional[str], Query(description="Filter users by role")] = None,
    db: Session = Depends(get_db)
):
    """
    Get all users or filter by role.
    
    Args:
        role: Optional filter to get users with a specific role
        db: Database session
        
    Returns:
        List of users matching the criteria
    """
    query = db.query(User)
    
    if role:
        query = query.filter(User.role == role)
    
    users = query.all()
    return users


@router.post("/", status_code=201, response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    
    Args:
        user: User data conforming to UserCreate schema
        db: Database session
        
    Returns:
        The created user with assigned ID
        
    Raises:
        HTTPException: 400 if username already exists
        
    Note:
        The role field will automatically be validated by Pydantic
        to ensure it's one of: admin, manager, team_member
    """
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail=f"Username '{user.username}' already exists"
        )
    
    # Create new user instance
    db_user = User(
        username=user.username,
        full_name=user.full_name,
        role=user.role,
        email=user.profile.email,
        phone=user.profile.phone,
        address=user.profile.address
    )
    
    # Add to database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a specific user by ID.
    
    Args:
        user_id: The unique identifier of the user
        db: Database session
        
    Returns:
        User details
        
    Raises:
        HTTPException: 404 if user not found
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID {user_id} not found"
        )
    
    return user

