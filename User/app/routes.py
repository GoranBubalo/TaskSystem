from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from User.app.dto.user_dto import UserCreate, UserUpdate, UserResponse
from User.app.service.user_service import UserService
from User.app.model.user import User

router = APIRouter(tags=["users"])

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    user_service = UserService()
    return user_service.create_user(db, user)

@router.get("/users", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of users (no auth restriction)"""
    user_service = UserService()
    return user_service.get_users(db, skip, limit)

@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: str, db: Session = Depends(get_db)):
    """Get user by ID (no auth restriction)"""
    user_service = UserService()
    user = user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/me", response_model=UserResponse)
def update_current_user(user_update: UserUpdate, db: Session = Depends(get_db)):
    """Update user info (no auth, use user_id from request if needed later)"""
    user_service = UserService()
    # Pretpostavljam da želiš ažurirati prvu pronađenu korisnika (za testiranje)
    users = user_service.get_users(db, skip=0, limit=1)
    if not users:
        raise HTTPException(status_code=404, detail="No user to update")
    return user_service.update_user(db, users[0].id, user_update)

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    """Delete user (no auth restriction)"""
    user_service = UserService()
    user_service.delete_user(db, user_id)
    return {"status": "success"}