from flask import Blueprint, jsonify
from flask_login import login_required

from app.services.cart_service import CartService

cart_bp = Blueprint("cart", __name__)

@cart_bp.route("", methods=["GET"])
@login_required
def read_cart_route():
    cart_items = CartService.read_cart()

    return jsonify([{
                "id": item.product.id,
                "name": item.product.name,
                "price": f'R$ {item.product.price_in_cents/100:.2f}',
                "description": item.product.description
            } for item in cart_items])

@cart_bp.route("/add/<int:product_id>", methods=["POST"])
@login_required
def add_cart_route(product_id):
    new_item = CartService.add_to_cart(product_id)

    return jsonify({"message": "Product added to cart successfully"})

@cart_bp.route("/remove/<int:product_id>", methods=["DELETE"])
@login_required
def remove_cart_route(product_id):
    CartService.remove_from_cart(product_id)

    return jsonify({"message": "Product removed from cart successfully"}) 

@cart_bp.route("/checkout", methods=["POST"])
@login_required
def checkout_cart_route():
    CartService.cart_checkout()

    return jsonify({"message":"Checkout successfull"})