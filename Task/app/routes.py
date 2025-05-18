from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from Task.app.dto.task_dto import TaskCreate, TaskUpdate, TaskResponse, TaskList
from Task.app.service.task_service import TaskService
from oauth2.auth import get_current_active_user
from User.app.model.user import User


router = APIRouter(tags=["tasks"])
task_service = TaskService()


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new task"""
    return task_service.create_task(db, task, current_user.id)


@router.get("/tasks", response_model=TaskList)
def read_tasks(
    skip: int = 0,
    limit: int = 10,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get list of user's tasks with filtering and pagination"""
    return task_service.get_user_tasks(
        db, current_user.id, skip, limit, status, priority
    )


@router.get("/tasks/assigned", response_model=TaskList)
def read_assigned_tasks(
    skip: int = 0,
    limit: int = 10,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get list of tasks assigned to the user"""
    return task_service.get_assigned_tasks(
        db, current_user.id, skip, limit, status
    )


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific task"""
    return task_service.get_task(db, task_id, current_user.id)


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a task"""
    return task_service.update_task(db, task_id, task_update, current_user.id)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a task"""
    task_service.delete_task(db, task_id, current_user.id)
    return {"status": "success"}