from datetime import datetime
from sqlalchemy.orm import Session
from typing import List, Optional

from User.app.model.user import User
from User.app.dto.user_dto import UserCreate, UserUpdate
from oauth2.auth import get_password_hash


class UserRepository:
    def create_user(self, db: Session, user: UserCreate) -> User:
        """Create a new user in the database"""
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=get_password_hash(user.password),
            full_name=user.full_name,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def get_user_by_id(self, db: Session, user_id: str) -> Optional[User]:
        """Get a user by ID"""
        return db.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, db: Session, username: str) -> Optional[User]:
        """Get a user by username"""
        return db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        """Get a user by email"""
        return db.query(User).filter(User.email == email).first()

    def get_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Get a list of users"""
        return db.query(User).offset(skip).limit(limit).all()

    def update_user(self, db: Session, user_id: str, user_update: UserUpdate) -> Optional[User]:
        """Update a user"""
        db_user = self.get_user_by_id(db, user_id)
        if not db_user:
            return None
        
        update_data = user_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        
        db.commit()
        db.refresh(db_user)
        return db_user

    def delete_user(self, db: Session, user_id: str) -> bool:
        """Delete a user"""
        db_user = self.get_user_by_id(db, user_id)
        if not db_user:
            return False
        
        db.delete(db_user)
        db.commit()
        return True

    def update_last_login(self, db: Session, user_id: str) -> Optional[User]:
        """Update the last login timestamp"""
        db_user = self.get_user_by_id(db, user_id)
        if not db_user:
            return None
        
        db_user.last_login = datetime.utcnow()
        db.commit()
        db.refresh(db_user)
        return db_user