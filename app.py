from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv(".env")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI")

db = SQLAlchemy(app)

migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price_in_cents = db.Column(db.Integer, nullable=False) # R$ 1.00 = 100
    description = db.Column(db.Text, nullable=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if "username" in data and "password" in data:
        user = User.query.filter_by(username=data["username"]).first()

        if user and user.password == data["password"]:
            login_user(user)
            return jsonify({"message": "Logged in successfully"}), 200

        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({"error": "Invalid login data"}), 400


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successfully"})


@app.route("/api/products", methods=["GET"])
def get_products():

    products = Product.query.all()
 
    return jsonify([{
        "id": product.id,
        "name": product.name,
        "price": f"R$ {product.price_in_cents/100:.2f}",
        "description": product.description
    } for product in products])
    

@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": f"R$ {product.price_in_cents/100:.2f}",
            "description": product.description
        }), 200
    return jsonify({"error": "Product not found"}), 404


@app.route("/api/products/add", methods=["POST"])
@login_required
def add_product():
    data = request.json
    if "name" in data and "price_in_cents" in data:
        product = Product(
            name=data["name"], 
            price_in_cents=data["price_in_cents"], 
            description=data.get("description", "")
        )
        db.session.add(product)
        db.session.commit()

        return jsonify({"message": "Product added successfully"}), 201
    
    return jsonify({"error": "Invalid Product data"}), 400


@app.route("/api/products/delete/<int:product_id>", methods=["DELETE"])
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200
    return jsonify({"error": "Product not found"}), 404


@app.route("/api/products/update/<int:product_id>", methods=["PUT"])
@login_required
def update_product(product_id):
    data = request.json

    if "name" in data and "price_in_cents" in data:
        product = Product.query.get(product_id)

        if product:
            product.name = data["name"]
            product.price_in_cents = data["price_in_cents"]
            product.description = data.get("description", "")
            db.session.commit()
            return jsonify({"message": "Product updated successfully"}), 200

        return jsonify({"error": "Product not found"}), 404

    return jsonify({"error": "Invalid Product data"}), 400


if __name__ == '__main__':
    app.run(debug=True)