from sqlalchemy.orm import Session
from typing import List

from User.app.repository.user_repository import UserRepository
from User.app.dto.user_dto import UserCreate, UserUpdate, UserResponse
from User.app.exception.user_exceptions import (
    UserNotFoundException,
    UsernameAlreadyExistsException,
    EmailAlreadyExistsException,
    UsernameTakenException,
)

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def create_user(self, db: Session, user: UserCreate) -> UserResponse:
        if self.user_repository.get_user_by_username(db, user.username):
            raise UsernameAlreadyExistsException()
        
        if self.user_repository.get_user_by_email(db, user.email):
            raise EmailAlreadyExistsException()
        
        return self.user_repository.create_user(db, user)

    def get_user(self, db: Session, user_id: int) -> UserResponse:
        db_user = self.user_repository.get_user_by_id(db, user_id)
        if not db_user:
            raise UserNotFoundException()
        return db_user

    def get_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        return self.user_repository.get_users(db, skip, limit)

    def update_user(self, db: Session, user_id: int, user_update: UserUpdate) -> UserResponse:
        if user_update.username:
            db_user = self.user_repository.get_user_by_username(db, user_update.username)
            if db_user and db_user.id != user_id:
                raise UsernameTakenException()

        if user_update.email:
            db_user = self.user_repository.get_user_by_email(db, user_update.email)
            if db_user and db_user.id != user_id:
                raise EmailAlreadyExistsException()

        db_user = self.user_repository.update_user(db, user_id, user_update)
        if not db_user:
            raise UserNotFoundException()
        return db_user

    def delete_user(self, db: Session, user_id: int) -> bool:
        result = self.user_repository.delete_user(db, user_id)
        if not result:
            raise UserNotFoundException()
        return True
