import os
from ..main import request, jsonify, app, bcrypt, create_access_token, get_jwt_identity, jwt_required, get_jwt
from ..db import db
from ..modelos import User, BlockedList, ShoppingCartItem, ShoppingCart
from flask import Flask, url_for, redirect
from datetime import datetime, timezone, time
import json
from ..utils import APIException


@app.route("/user/<int:user_id>/add_shopping_cart", methods=["POST"])
@jwt_required()
def add_item_to_shopping_cart(user_id):
    if not request.is_json:
        return jsonify({"message": "Request must be in JSON format"}), 400

    data = request.get_json()
    product_quantity = data.get("product_quantity")
    product_price = data.get("product_price")
    product_name = data.get("product_name")
    product_image = data.get("product_image")

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    cart_entry = ShoppingCart.query.filter_by(user_id=user_id).first() 
    if not cart_entry:
        try:
            shopping_cart = ShoppingCart(user_id=user_id)
            db.session.add(shopping_cart)
            db.session.commit()
            return jsonify({"message": "Shopping cart created"}), 201
        except Exception as error:
            db.session.rollback()
            raise APIException(f"Failed to create shopping cart: {error}", status_code=500)

    cart_item = ShoppingCartItem.query.filter_by(shopping_cart_id=cart_entry.id, product_name=product_name).first()
    if cart_item:
        return jsonify({"message": "Product already added to shopping cart"}), 403

    try:
        shopping_cart_item = ShoppingCartItem(
            shopping_cart_id=cart_entry.id,
            product_price=product_price,
            product_quantity=product_quantity,
            product_name=product_name,
            product_image=product_image
        )
        db.session.add(shopping_cart_item)
        db.session.commit()
        return jsonify({"message": "Product added to shopping cart"}), 201
    except Exception as error:
        db.session.rollback()
        raise APIException(f"Failed to add product to shopping cart: {error}", status_code=500)

@app.route("/user/<int:user_id>/shopping_cart", methods=["GET"])
@jwt_required()
def get_shopping_cart(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    cart_entry = ShoppingCart.query.filter_by(user_id=user_id).first() 
    print(cart_entry.user_id)
    if not cart_entry:
        return jsonify({"message": "Shopping cart not found"}), 404

    cart_items = ShoppingCartItem.query.filter_by(shopping_cart_id=cart_entry.id).all()
    if not cart_items:
        return jsonify({"message": "Shopping cart is empty"}), 404

    return jsonify([cart_item.serialize() for cart_item in cart_items]), 200