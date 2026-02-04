from flask import Blueprint

product_bp = Blueprint("product", __name__)

@product_bp.route("/", methods=["GET"])
def read_products_route():
    ...

@product_bp.route("/<int:product_id>", methods=["GET"])
def read_product_details_route(product_id):
    ...

@product_bp.route("/add", methods=["POST"])
def add_product_route():
    ...

@product_bp.route("/update", methods=["PUT"])
def update_product_route():
    ...

@product_bp.route("/delete", methods=["DELETE"])
def delete_product_route():
    ...