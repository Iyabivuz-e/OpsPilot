from fastapi import HTTPException

class AppExceptions(Exception):
    def __init__(self, message:str, code:str, status_code: int):
        
        self.message = message
        self.code = code
        self.status_code = status_code
        

class UserNotFoundError(AppExceptions):
    def __init__(self):
        super().__init__(
            message="User not found",
            code="USER_NOT_FOUND",
            status_code=404
        )
class InvalidCredentialsError(AppExceptions):
    def __init__(self):
        super().__init__(
            message="Invalid credentials",
            code="INVALID_CREDENTIALS",
            status_code=401
        )
        
class BadRequestError(AppExceptions):
    def __init__(self, message: str = "Bad request"):
        super().__init__(
            message=message,
            code="BAD_REQUEST",
            status_code=400
        )
        
class NotFoundError(AppExceptions):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(
            message=message,
            code="NOT_FOUND",
            status_code=404
        )