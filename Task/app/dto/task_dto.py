from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from Task.app.enum.task_priority import TaskPriority
from Task.app.enum.task_status import TaskStatus


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.PENDING
    priority: Optional[TaskPriority] = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    assigned_to: Optional[str] = None
    parent_id: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = None
    is_completed: Optional[bool] = None


class TaskInDB(TaskBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    assigned_to: Optional[str] = None
    parent_id: Optional[str] = None
    is_completed: bool
    completed_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class TaskResponse(TaskInDB):
    class Config:
        orm_mode = True


class TaskList(BaseModel):
    tasks: List[TaskResponse]
    total: int
    page: int
    size: int