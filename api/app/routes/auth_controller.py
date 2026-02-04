from flask import Blueprint

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register_route():
    ...

@auth_bp.route("/login", methods=["POST"])
def login_route():
    ...