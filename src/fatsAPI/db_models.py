"""
SQLAlchemy ORM models for database tables.
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    """
    User model for storing user information.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False)  # admin, manager, team_member
    
    # Profile information
    email = Column(String(100), nullable=False)
    phone = Column(String(20))
    address = Column(String(200))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship with tasks
    tasks = relationship("Task", back_populates="assigned_user")


class Task(Base):
    """
    Task model for storing task information.
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(1000))
    priority = Column(Integer, nullable=False)  # 1-5
    status = Column(String(20), nullable=False)  # pending, in_progress, completed
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship with user
    assigned_user = relationship("User", back_populates="tasks")
