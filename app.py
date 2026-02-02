from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

migrate = Migrate(app, db)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price_in_cents = db.Column(db.Integer, nullable=False) # R$ 1.00 = 100
    description = db.Column(db.Text, nullable=True)


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
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200
    return jsonify({"error": "Product not found"}), 404


@app.route("/api/products/update/<int:product_id>", methods=["PUT"])
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