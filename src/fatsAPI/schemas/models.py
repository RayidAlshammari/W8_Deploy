from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Literal, Annotated, Optional
from datetime import datetime


class Profile(BaseModel):
    """
    Nested model representing user contact information and profile details.
    
    Attributes:
        email: User's email address
        phone: Contact phone number
        address: Physical or mailing address
    """
    email: Annotated[str, Field(description="User's email address", example="user@example.com")]
    phone: Annotated[str, Field(description="Contact phone number", example="+966501234567")]
    address: Annotated[str, Field(description="User's address", example="Riyadh, Saudi Arabia")]


class UserCreate(BaseModel):
    """
    Model for creating a new user in the system.
    
    Attributes:
        username: Unique username for the user
        full_name: User's full name
        role: User role - must be one of: admin, manager, team_member
        profile: Nested profile information containing contact details
    """
    username: Annotated[str, Field(min_length=3, max_length=50, description="Unique username")]
    full_name: Annotated[str, Field(min_length=1, description="User's full name")]
    role: Literal["admin", "manager", "team_member"]
    profile: Profile
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "john_doe",
                    "full_name": "John Doe",
                    "role": "manager",
                    "profile": {
                        "email": "john@example.com",
                        "phone": "+966501234567",
                        "address": "Riyadh, Saudi Arabia"
                    }
                }
            ]
        }
    }


class UserResponse(BaseModel):
    """
    Model for user responses from the database.
    """
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    username: str
    full_name: str
    role: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    created_at: datetime


class TaskCreate(BaseModel):
    """
    Model for creating a new task in the system.
    
    Attributes:
        title: Task title - must start with a capital letter
        description: Detailed task description
        priority: Priority level from 1 (lowest) to 5 (highest)
        status: Current task status
        assigned_to: Optional user ID to whom the task is assigned
    """
    title: Annotated[str, Field(min_length=1, description="Task title (must be capitalized)")]
    description: Annotated[str, Field(description="Detailed task description")]
    priority: Annotated[int, Field(ge=1, le=5, description="Priority level: 1 (lowest) to 5 (highest)")]
    status: Literal["pending", "in_progress", "completed"]
    assigned_to: Annotated[Optional[int], Field(default=None, description="ID of user assigned to this task")]
    
    @field_validator('title')
    @classmethod
    def title_must_be_capitalized(cls, v: str) -> str:
        """
        Validates that the task title starts with a capital letter.
        
        Args:
            v: The title string to validate
            
        Returns:
            The validated title string
            
        Raises:
            ValueError: If the title doesn't start with a capital letter
        """
        if not v or not v[0].isupper():
            raise ValueError('Title must start with a capital letter')
        return v
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Implement user authentication",
                    "description": "Add JWT-based authentication to the API",
                    "priority": 5,
                    "status": "in_progress",
                    "assigned_to": 1
                }
            ]
        }
    }


class TaskResponse(BaseModel):
    """
    Model for task responses from the database.
    """
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    description: str
    priority: int
    status: str
    assigned_to: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

