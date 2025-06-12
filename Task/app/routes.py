from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from Task.app.dto.task_dto import TaskCreate, TaskUpdate, TaskResponse, TaskList
from Task.app.service.task_service import TaskService

router = APIRouter(tags=["tasks"])
task_service = TaskService()

@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task"""
    return task_service.create_task(db, task, None)  # Pretpostavi None za user_id (prilagodi u service-u)

@router.get("/tasks", response_model=TaskList)
def read_tasks(
    skip: int = 0,
    limit: int = 10,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of tasks with filtering and pagination (no auth restriction)"""
    return task_service.get_user_tasks(db, None, skip, limit, status, priority)  # Pretpostavi None za user_id

@router.get("/tasks/assigned", response_model=TaskList)
def read_assigned_tasks(
    skip: int = 0,
    limit: int = 10,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of tasks (no auth restriction, prilagođeno)"""
    return task_service.get_assigned_tasks(db, None, skip, limit, status)  # Pretpostavi None za user_id

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(task_id: str, db: Session = Depends(get_db)):
    """Get a specific task (no auth restriction)"""
    return task_service.get_task(db, task_id, None)  # Pretpostavi None za user_id

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, task_update: TaskUpdate, db: Session = Depends(get_db)):
    """Update a task (no auth restriction)"""
    return task_service.update_task(db, task_id, task_update, None)  # Pretpostavi None za user_id

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session = Depends(get_db)):
    """Delete a task (no auth restriction)"""
    task_service.delete_task(db, task_id, None)  # Pretpostavi None za user_id
    return {"status": "success"}