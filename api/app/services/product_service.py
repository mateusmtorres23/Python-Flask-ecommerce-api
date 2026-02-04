from extensions import db

from models.product import Product
from exceptions import BadRequest, ProductNotFound

class ProductService():
    
    @staticmethod
    def read_products_service():
        products = Product.query.all()

        return products
    
    @staticmethod
    def product_details_service(product_id):
        product = Product.query.get(product_id)

        if product:
            return product
        raise ProductNotFound()
    
    @staticmethod
    def create_product(request):
        if "name" in request and "price_in_cents" in request:
            new_product = Product(
                name=request["name"],
                price_in_cents=request["price_in_cents"],
                description=request["description"]
            )

            db.session.add(new_product)
            db.session.commit()

            return new_product
        raise BadRequest(message="Invalid product data")
    
    @staticmethod
    def update_product(product_id,request):
        if "name" in request and "price_in_cents" in request:
            product = Product.query.get(product_id)

            if product:
                product.name = request["name"]
                product.price_in_cents = request["price_in_cents"]
                product.description = request["description"]

                db.session.commit()

                return product
            raise ProductNotFound()
        raise BadRequest(message="Invalid product data")

    @staticmethod
    def delete_product(product_id):
        product = Product.query.get(product_id)

        if product:
            db.session.delete(product)
            db.session.commit()
            return
        raise ProductNotFound()