from fastapi import FastAPI
from User.app.routes import router as user_router
from User.app.model.base import Base


# Initialize FastAPI app
app = FastAPI(
    title="User Service",
    description="User management service for TaskFlow",
    version="0.1.0",
)

# Include routers
app.include_router(user_router, prefix="/api/v1")