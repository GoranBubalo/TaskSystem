from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from User.app.repository.user_repository import UserRepository
from oauth2.utils import verify_password, create_access_token
from database import get_db

class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()

    def authenticate_user(self, db: Session, username: str, password: str):
        """Authenticate a user by username and password"""
        user = self.user_repository.get_user_by_username(db, username)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user

    def login_for_access_token(self, db: Session, form_data: OAuth2PasswordRequestForm):
        """Login and return access token"""
        user = self.authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Update last login timestamp
        self.user_repository.update_last_login(db, user.id)
        
        # Create access token
        access_token_expires = timedelta(minutes=30)  # Adjust as needed
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}