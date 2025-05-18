from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Tuple, Dict, Any

from Task.app.repository.task_repository import TaskRepository
from Task.app.dto.task_schema import TaskCreate, TaskUpdate, TaskResponse, TaskList


class TaskService:
    def __init__(self):
        self.task_repository = TaskRepository()

    def create_task(self, db: Session, task: TaskCreate, user_id: int) -> TaskResponse:
        """Create a new task"""
        # Validate parent task if provided
        if task.parent_id:
            parent_task = self.task_repository.get_task_by_id(db, task.parent_id)
            if not parent_task:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Parent task not found"
                )
            # Check if the parent task belongs to the user
            if parent_task.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not allowed to create subtask for this parent task"
                )
        
        # Create new task
        return self.task_repository.create_task(db, task, user_id)

    def get_task(self, db: Session, task_id: int, user_id: int) -> TaskResponse:
        """Get a task by ID, ensuring it belongs to the user"""
        db_task = self.task_repository.get_task_by_id(db, task_id)
        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        # Check if the task belongs to the user or is assigned to them
        if db_task.user_id != user_id and db_task.assigned_to != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed to access this task"
            )
        
        return db_task

    def get_user_tasks(
        self, 
        db: Session, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 10, 
        status: Optional[str] = None,
        priority: Optional[str] = None
    ) -> TaskList:
        """Get tasks for a user with filtering and pagination"""
        tasks, total = self.task_repository.get_tasks_by_user(
            db, user_id, skip, limit, status, priority
        )
        
        return TaskList(
            tasks=tasks,
            total=total,
            page=(skip // limit) + 1,
            size=limit
        )

    def get_assigned_tasks(
        self, 
        db: Session, 
        user_id: int,
        skip: int = 0, 
        limit: int = 10, 
        status: Optional[str] = None
    ) -> TaskList:
        """Get tasks assigned to a user"""
        tasks, total = self.task_repository.get_assigned_tasks(
            db, user_id, skip, limit, status
        )
        
        return TaskList(
            tasks=tasks,
            total=total,
            page=(skip // limit) + 1,
            size=limit
        )

    def update_task(self, db: Session, task_id: int, task_update: TaskUpdate, user_id: int) -> TaskResponse:
        """Update a task, ensuring it belongs to the user"""
        db_task = self.task_repository.get_task_by_id(db, task_id)
        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        # Check if the task belongs to the user or is assigned to them
        if db_task.user_id != user_id and db_task.assigned_to != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed to update this task"
            )
        
        # If assigned_to is being changed, verify the user exists (would be done in a real app)
        # This would require importing and using the user repository
        
        return self.task_repository.update_task(db, task_id, task_update)

    def delete_task(self, db: Session, task_id: int, user_id: int) -> bool:
        """Delete a task, ensuring it belongs to the user"""
        db_task = self.task_repository.get_task_by_id(db, task_id)
        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        # Only the owner can delete a task
        if db_task.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed to delete this task"
            )
        
        return self.task_repository.delete_task(db, task_id)