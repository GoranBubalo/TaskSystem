from fastapi import FastAPI
from Task.app.routes import router as task_router
from Task.app.model.base import Base
from database import engine

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Task Service",
    description="Task management service for TaskFlow",
    version="0.1.0",
)

# Include routers
app.include_router(task_router, prefix="/api/v1")