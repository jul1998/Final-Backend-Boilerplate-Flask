from ..db import db
import os

class ShoppingCart(db.Model):
    __tablename__ = "shoppingCart"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class ShoppingCartItem(db.Model):
    __tablename__ = "shoppingCartItem"
    id = db.Column(db.Integer, primary_key=True)
    shopping_cart_id = db.Column(db.Integer, db.ForeignKey('shoppingCart.id'))
    product_price = db.Column(db.Float, nullable=False)
    product_quantity = db.Column(db.Integer, nullable=False)
    product_name= db.Column(db.String(250), nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    product_image = db.Column(db.Text, nullable=False)


    
    def __repr__(self):
        return '<shoppingCartItem %r>' % self.product_name

    def serialize(self):
        return {
            "id": self.id,
            "product_name": self.product_name,
            "user_id": self.shopping_cart_id,
            "product_price": self.product_price,
            "quantity":self.product_quantity,
            "product_image":self.product_image,
        }
