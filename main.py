from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from database import engine

# Import sub-applications
from User.app import app as user_app
from Task.app import app as task_app

from User.app.model.base import Base as UserBase
from Task.app.model.base import Base as TaskBase



# Load environment variables based on ENV
ENV = os.getenv("ENV", "dev")  # Default to 'dev'
env_files = {
    "dev": ".env.dev",
    "test": ".env.test",
    "prod": ".env.prod"
}
env_file = env_files.get(ENV, ".env.dev")
load_dotenv(env_file)

# Application settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
PORT = int(os.getenv("PROD_PORT", "8000")) if os.getenv("STATUS", "development") == "production" else int(os.getenv("DEV_PORT", "7000"))

# Create main application
app = FastAPI(
    title="TaskFlow",
    description="Distributed task management system",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount sub-applications
app.mount("/user", user_app)
app.mount("/task", task_app)

# Create database tables
UserBase.metadata.create_all(bind=engine)
TaskBase.metadata.create_all(bind=engine)

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to TaskFlow API",
        "version": "0.1.0",
        "services": {
            "user": "/user/api/v1",
            "task": "/task/api/v1"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)