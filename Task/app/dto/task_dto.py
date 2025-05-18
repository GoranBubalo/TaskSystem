from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "pending"
    priority: Optional[str] = "medium"
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    assigned_to: Optional[int] = None
    parent_id: Optional[int] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    assigned_to: Optional[int] = None
    is_completed: Optional[bool] = None


class TaskInDB(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    assigned_to: Optional[int] = None
    parent_id: Optional[int] = None
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