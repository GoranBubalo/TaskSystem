# Task/app/service/celery_tasks.py
from celery import shared_task
from sqlalchemy.orm import Session
from database import SessionLocal
from Task.app.model.task import Task
from Task.app.enum.task_status import TaskStatus
from datetime import datetime

@shared_task
def check_due_tasks():
    db = SessionLocal()
    try:
        tasks = db.query(Task).filter(
            Task.due_date <= datetime.utcnow(),
            Task.status != TaskStatus.COMPLETED
        ).all()
        for task in tasks:
            # Example: Send notification (implement your logic)
            print(f"Task {task.title} is overdue!")
    finally:
        db.close()