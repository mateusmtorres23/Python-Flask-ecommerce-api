from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)


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
    

@app.route("/api/products/add", methods=["POST"])
def add_product():
    data = request.json

    product = Product(
        name=data["name"], 
        price_in_cents=data["price_in_cents"], 
        description=data.get("description", "")
    )

    db.session.add(product)
    db.session.commit()

    return "Product added successfully", 201


if __name__ == '__main__':
    app.run(debug=True)