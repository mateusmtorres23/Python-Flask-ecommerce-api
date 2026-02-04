from werkzeug.security import generate_password_hash, check_password_hash

from exceptions import BadRequest, UserAlreadyExists, InvalidUsernamePassword
from extensions import db
from models.user import User

class AuthService:
    
    @staticmethod
    def create_user_service(request):
        if "username" in request and "password" in request:

            if User.query.filter_by(username=request["username"]).first():
                raise UserAlreadyExists()
            
            password_hash = generate_password_hash(request["password"])

            new_user = User(username=request["username"], password=password_hash)

            db.session.add(new_user)
            db.session.commit()

            return new_user
        
        raise BadRequest(message="Username and password are required fields")

    @staticmethod
    def login_service(request):
        if "username" in request and "password" in request:
            user = User.query.filter_by(username=request["username"]).first()

            if user and check_password_hash(user.password, request["password"]):
                return user

            raise InvalidUsernamePassword()

        raise BadRequest(message="Invalid login data")