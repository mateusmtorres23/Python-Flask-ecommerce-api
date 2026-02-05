from flask_login import current_user, login_required

from app.models.cart_item import CartItem
from app.models.product import Product
from app.exceptions import ProductAlreadyAdded, ProductNotFound
from app.extensions import db

class CartService():
    
    @staticmethod
    def read_cart():
        user_cart = current_user.cart
        return user_cart

    @staticmethod
    def add_to_cart(product_id):
        product = Product.query.get(product_id)
    
        if product:
            user_id = current_user.id
            user_cart = current_user.cart

            if CartItem.query.filter_by(user_id=user_id, product_id=product.id).first():
                raise ProductAlreadyAdded()

            user_cart.append(CartItem(user_id=user_id, product_id=product.id))

            db.session.commit()

            return
        
        raise ProductNotFound()
    
    @staticmethod
    def remove_from_cart(product_id):
        user_id = current_user.id

        cart_item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()

        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
            return

        raise ProductNotFound()
    
    @staticmethod
    def cart_checkout():
        user_cart = current_user.cart

        for item in user_cart:
            db.session.delete(item)
        
        db.session.commit()
        return