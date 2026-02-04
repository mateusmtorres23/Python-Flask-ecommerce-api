from flask_login import current_user, login_required

from models.cart_item import CartItem
from models.product import Product
from exceptions import ProductAlreadyAdded, ProductNotFound
from extensions import db

class CartService():
    
    @staticmethod
    @login_required
    def read_cart():
        user_cart = current_user.cart

        cart_itens = [{
                "id": item.product.id,
                "name": item.product.name,
                "price": f'R$ {item.product.price_in_cents/100:.2f}',
                "description": item.product.description
            } for item in user_cart]
        
        return cart_itens

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