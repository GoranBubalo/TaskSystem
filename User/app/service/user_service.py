from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from User.app.repository.user_repository import UserRepository
from User.app.dto.user_schema import UserCreate, UserUpdate, UserResponse


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def create_user(self, db: Session, user: UserCreate) -> UserResponse:
        """Create a new user"""
        # Check if username already exists
        db_user = self.user_repository.get_user_by_username(db, user.username)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Check if email already exists
        db_user = self.user_repository.get_user_by_email(db, user.email)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        return self.user_repository.create_user(db, user)

    def get_user(self, db: Session, user_id: int) -> UserResponse:
        """Get a user by ID"""
        db_user = self.user_repository.get_user_by_id(db, user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return db_user

    def get_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """Get a list of users"""
        return self.user_repository.get_users(db, skip, limit)

    def update_user(self, db: Session, user_id: int, user_update: UserUpdate) -> UserResponse:
        """Update a user"""
        # Check if username is being updated and if it already exists
        if user_update.username:
            db_user = self.user_repository.get_user_by_username(db, user_update.username)
            if db_user and db_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )
        
        # Check if email is being updated and if it already exists
        if user_update.email:
            db_user = self.user_repository.get_user_by_email(db, user_update.email)
            if db_user and db_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        
        # Update user
        db_user = self.user_repository.update_user(db, user_id, user_update)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return db_user

    def delete_user(self, db: Session, user_id: int) -> bool:
        """Delete a user"""
        result = self.user_repository.delete_user(db, user_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return True