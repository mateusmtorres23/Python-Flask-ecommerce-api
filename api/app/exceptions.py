class ApiError(Exception):

    status_code = 500
    message = "A server error ocurred"

    def __init__(self, status_code=None, message=None):
        super().__init__()
        if status_code:
            self.status_code = status_code
        if message:
            self.message = message
        
    def to_dict(self):
        return {
            "status_code": self.status_code,
            "error": self.message
        }

class UserAlreadyExists(ApiError):
    status_code = 409
    message = "A user with this username already exists"

class BadRequest(ApiError):
    status_code = 400
    message = "Bad request"

class InvalidUsernamePassword(ApiError):
    status_code = 401
    message = "Invalid username or password"

class ProductNotFound(ApiError):
    status_code = 404
    message = "This product doesn't exist"
