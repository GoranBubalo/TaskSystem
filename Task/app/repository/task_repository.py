from datetime import datetime
from sqlalchemy.orm import Session
from typing import List, Optional, Tuple

from Task.app.enum.task_priority import TaskPriority
from Task.app.enum.task_status import TaskStatus
from Task.app.model.task import Task
from Task.app.dto.task_dto import TaskCreate, TaskUpdate


class TaskRepository:
    def create_task(self, db: Session, task: TaskCreate, user_id: str) -> Task:
        """Create a new task"""
        db_task = Task(
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            due_date=task.due_date,
            user_id=user_id,
            assigned_to=task.assigned_to,
            parent_id=task.parent_id,
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    def get_task_by_id(self, db: Session, task_id: str) -> Optional[Task]:
        """Get a task by ID"""
        return db.query(Task).filter(Task.id == task_id).first()

    def get_tasks_by_user(
        self,
        db: Session,
        user_id: str,
        skip: int = 0,
        limit: int = 100,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
    ) -> Tuple[List[Task], int]:
        """Get tasks by user ID with optional filters"""
        query = db.query(Task).filter(Task.user_id == user_id)

        if status:
            query = query.filter(Task.status == status)
        if priority:
            query = query.filter(Task.priority == priority)

        total = query.count()
        tasks = query.order_by(Task.created_at.desc()).offset(skip).limit(limit).all()

        return tasks, total

    def get_assigned_tasks(
        self,
        db: Session,
        assigned_to: str,
        skip: int = 0,
        limit: int = 100,
        status: Optional[TaskStatus] = None,
    ) -> Tuple[List[Task], int]:
        """Get tasks assigned to a user"""
        query = db.query(Task).filter(Task.assigned_to == assigned_to)

        if status:
            query = query.filter(Task.status == status)

        total = query.count()
        tasks = query.order_by(Task.created_at.desc()).offset(skip).limit(limit).all()

        return tasks, total

    def update_task(self, db: Session, task_id: str, task_update: TaskUpdate) -> Optional[Task]:
        """Update a task"""
        db_task = self.get_task_by_id(db, task_id)
        if not db_task:
            return None

        update_data = task_update.dict(exclude_unset=True)

        # Special handling for completion status
        if 'is_completed' in update_data and update_data['is_completed'] != db_task.is_completed:
            db_task.is_completed = update_data['is_completed']
            if update_data['is_completed']:
                db_task.completed_at = datetime.utcnow()
                db_task.status = TaskStatus.COMPLETED
            else:
                db_task.completed_at = None
                if db_task.status == TaskStatus.COMPLETED:
                    db_task.status = TaskStatus.IN_PROGRESS

            # Remove from update_data to avoid overwriting twice
            update_data.pop('is_completed', None)
            if 'status' in update_data and update_data['status'] == TaskStatus.COMPLETED:
                update_data.pop('status', None)

        # Apply remaining updates
        for key, value in update_data.items():
            setattr(db_task, key, value)

        db.commit()
        db.refresh(db_task)
        return db_task

    def delete_task(self, db: Session, task_id: str) -> bool:
        """Delete a task"""
        db_task = self.get_task_by_id(db, task_id)
        if not db_task:
            return False

        db.delete(db_task)
        db.commit()
        return True

    def get_subtasks(self, db: Session, parent_id: str) -> List[Task]:
        """Get all subtasks of a task"""
        return db.query(Task).filter(Task.parent_id == parent_id).all()