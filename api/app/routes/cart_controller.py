from flask import Blueprint

cart_bp = Blueprint("cart", __name__)

@cart_bp.route("/", methods=["GET"])
def read_cart_route():
    ...

@cart_bp.route("/add/<int:product_id>", methods=["POST"])
def add_cart_route():
    ...

@cart_bp.route("/remove/<int:product_id>", methods=["DELETE"])
def remove_cart_route():
    ...

@cart_bp.route("/checkout", methods=["POST"])
def checkout_cart_route():
    ...