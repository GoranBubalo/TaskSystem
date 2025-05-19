from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import sub-applications
from User.app import app as user_app
from Task.app import app as task_app

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
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)