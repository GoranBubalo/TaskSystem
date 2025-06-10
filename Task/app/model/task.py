from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import Enum as SqlEnum

from Task.app.enum.task_priority import TaskPriority
from Task.app.enum.task_status import TaskStatus
from Task.app.model.base import Base
from uuid_generator.v4_generator import generate_uuid


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True,  default=generate_uuid, index=True) 
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(SqlEnum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    priority = Column(SqlEnum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)  
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Foreign key relationship with User
    user_id = Column(String, ForeignKey("users.id"))
    user = relationship("User", back_populates="tasks")
    
    # If you want to implement task dependencies (optional)
    parent_id = Column(String, ForeignKey("tasks.id"), nullable=True)
    subtasks = relationship("Task", backref="parent", remote_side=[id])
    
    # For task assignment to other users (optional)
    assigned_to = Column(String, ForeignKey("users.id"), nullable=True)
    assignee = relationship("User", foreign_keys=[assigned_to], back_populates="assigned_tasks")
    
    # For task completion tracking
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)