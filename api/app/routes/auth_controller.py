from flask import Blueprint, jsonify, request
from flask_login import login_user
from services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register_route():

    data = request.json
    new_user = AuthService.create_user_service(data)

    return jsonify({
        "id": new_user.id,
        "username": new_user.username,
        }), 201

@auth_bp.route("/login", methods=["POST"])
def login_route():
    data = request.json

    user = AuthService.login_service(data)

    login_user(user)
    
    return jsonify({"message": "Logged in successfully"})