from flask import Flask, jsonify
from dotenv import load_dotenv
from app.routes.auth_controller import auth_bp
from app.routes.cart_controller import cart_bp
from app.routes.product_controller import product_bp
from app.models.user import User
from app.extensions import login_manager, db, migrate
from app.exceptions import ApiError
import os

load_dotenv(".env")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI")

db.init_app(app)

login_manager.init_app(app)

migrate.init_app(app, db)

app.register_blueprint(auth_bp)
app.register_blueprint(cart_bp, url_prefix="/api/cart")
app.register_blueprint(product_bp, url_prefix="/api/products")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.errorhandler(ApiError)
def handle_api_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == '__main__':
    app.run(debug=True)