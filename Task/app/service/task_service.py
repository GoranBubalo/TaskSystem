from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from Task.app.enum import TaskStatus, TaskPriority
from Task.app.repository.task_repository import TaskRepository
from Task.app.dto.task_dto import TaskCreate, TaskUpdate, TaskResponse, TaskList
from Task.app.exception.task_exceptions import (
    TaskNotFoundException,
    ParentTaskNotFoundException,
    ForbiddenAccessException,
    InvalidEnumValueException,
)

class TaskService:
    def __init__(self):
        self.task_repository = TaskRepository()

    def create_task(self, db: Session, task: TaskCreate, user_id: str) -> TaskResponse:
        """Create a new task"""
        if task.parent_id:
            parent_task = self.task_repository.get_task_by_id(db, task.parent_id)
            if not parent_task:
                raise ParentTaskNotFoundException()
            if parent_task.user_id != user_id:
                raise ForbiddenAccessException("Not allowed to create subtask for this parent task")

        return self.task_repository.create_task(db, task, user_id)

    def get_task(self, db: Session, task_id: str, user_id: str) -> TaskResponse:
        """Get a task by ID, ensuring it belongs to the user"""
        db_task = self.task_repository.get_task_by_id(db, task_id)
        if not db_task:
            raise TaskNotFoundException()
        if db_task.user_id != user_id and db_task.assigned_to != user_id:
            raise ForbiddenAccessException("Not allowed to access this task")
        return db_task

    def get_user_tasks(
        self, 
        db: Session, 
        user_id: str, 
        skip: int = 0, 
        limit: int = 10, 
        status: Optional[str] = None,
        priority: Optional[str] = None,
    ) -> TaskList:
        """Get tasks for a user with filtering and pagination"""
        self.validate_enum(status, TaskStatus, "status")
        self.validate_enum(priority, TaskPriority, "priority")

        tasks, total = self.task_repository.get_tasks_by_user(
            db, user_id, skip, limit, status, priority
        )
        return TaskList(
            tasks=tasks,
            total=total,
            page=(skip // limit) + 1,
            size=limit,
        )

    def get_assigned_tasks(
        self, 
        db: Session, 
        user_id: str, 
        skip: int = 0, 
        limit: int = 10, 
        status: Optional[str] = None
    ) -> TaskList:
        """Get tasks assigned to a user"""
        self.validate_enum(status, TaskStatus, "status")
        
        tasks, total = self.task_repository.get_assigned_tasks(
            db, user_id, skip, limit, status
        )
        return TaskList(
            tasks=tasks,
            total=total,
            page=(skip // limit) + 1,
            size=limit,
        )

    def update_task(self, db: Session, task_id: str, task_update: TaskUpdate, user_id: str) -> TaskResponse:
        """Update a task, ensuring it belongs to the user"""
        db_task = self.task_repository.get_task_by_id(db, task_id)
        if not db_task:
            raise TaskNotFoundException()
        if db_task.user_id != user_id and db_task.assigned_to != user_id:
            raise ForbiddenAccessException("Not allowed to update this task")

        # Validate enum fields in task update
        self.validate_enum(task_update.status, TaskStatus, "status")
        self.validate_enum(task_update.priority, TaskPriority, "priority")

        return self.task_repository.update_task(db, task_id, task_update)

    def delete_task(self, db: Session, task_id: str, user_id: str) -> bool:
        """Delete a task, ensuring it belongs to the user"""
        db_task = self.task_repository.get_task_by_id(db, task_id)
        if not db_task:
            raise TaskNotFoundException()
        if db_task.user_id != user_id:
            raise ForbiddenAccessException("Not allowed to delete this task")
        
        return self.task_repository.delete_task(db, task_id)

    def validate_enum(self, value: Optional[str], enum_class: type, field_name: str):
        """Helper method to validate enums"""
        if value and value not in [e.value for e in enum_class]:
            raise InvalidEnumValueException(field_name, [e.value for e in enum_class])
