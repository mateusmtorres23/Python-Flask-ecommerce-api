from flask import Blueprint, jsonify, request
from flask_login import login_required

from app.services.product_service import ProductService

product_bp = Blueprint("product", __name__)

@product_bp.route("", methods=["GET"])
def read_products_route():
    products = ProductService.read_products_service()

    return jsonify([{
            "id": product.id,
            "name": product.name,
            "price": f"R$ {product.price_in_cents/100:.2f}",
            "description": product.description
        }for product in products])

@product_bp.route("/<int:product_id>", methods=["GET"])
def read_product_details_route(product_id):
    product = ProductService.product_details_service(product_id)

    return jsonify({
            "id": product.id,
            "name": product.name,
            "price": f"R$ {product.price_in_cents/100:.2f}",
            "description": product.description
        })

@product_bp.route("/add", methods=["POST"])
@login_required
def add_product_route():
    data = request.json
    new_product = ProductService.create_product(data)

    return jsonify({
            "id": new_product.id,
            "name": new_product.name,
            "price": f"R$ {new_product.price_in_cents/100:.2f}",
            "description": new_product.description
        }), 201

@product_bp.route("/update/<int:product_id>", methods=["PUT"])
@login_required
def update_product_route(product_id):
    data = request.json
    updated_product = ProductService.update_product(product_id, data)

    return jsonify({
            "id": updated_product.id,
            "name": updated_product.name,
            "price": f"R$ {updated_product.price_in_cents/100:.2f}",
            "description": updated_product.description
        })

@product_bp.route("/delete/<int:product_id>", methods=["DELETE"])
@login_required
def delete_product_route(product_id):
    ProductService.delete_product(product_id)

    return jsonify({"message": "Product deleted successfully"})