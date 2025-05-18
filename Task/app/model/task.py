from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from Task.app.model.base import Base


class Task(Base):
    __tablename__ = "tasks"
    # TODO : Refactor code to add UUID, Enums
    id = Column(Integer, primary_key=True, index=True) # UUID
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, default="pending")  # Enum
    priority = Column(String, default="medium")  # Enum
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Foreign key relationship with User
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="tasks")
    
    # If you want to implement task dependencies (optional)
    parent_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    subtasks = relationship("Task", backref="parent", remote_side=[id])
    
    # For task assignment to other users (optional)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    assignee = relationship("User", foreign_keys=[assigned_to], backref="assigned_tasks")
    
    # For task completion tracking
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)