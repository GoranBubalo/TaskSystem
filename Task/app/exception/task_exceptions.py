from fastapi import HTTPException, status

class TaskNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

class ParentTaskNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parent task not found"
        )

class ForbiddenAccessException(HTTPException):
    def __init__(self, detail: str = "You are not allowed to perform this action"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

class InvalidEnumValueException(HTTPException):
    def __init__(self, field_name: str, expected_values: list):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid {field_name}. Expected values: {expected_values}"
        )
