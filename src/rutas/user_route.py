import os
from ..main import request, jsonify, app, bcrypt, create_access_token, get_jwt_identity, jwt_required, get_jwt
from ..db import db
from ..modelos import User, BlockedList
from flask import Flask, url_for, redirect
from datetime import datetime, timezone, time
import json
from ..utils import APIException
from functools import wraps


def admin_only(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        try:
            if get_jwt_identity() != 1:
                return jsonify("Not a admin"), 403
        except AttributeError:
            return jsonify("Not a admin error"), 403
        else:
            return func(*args, **kwargs)
    return wrapper

@app.route('/signup', methods=['POST'])
def signup():
    body = request.get_json()
    print(body)
    try:
        if body is None:
            raise APIException(
                "Body está vacío o email no viene en el body, es inválido", status_code=400)
        if body['email'] is None or body['email'] == "":
            raise APIException("Email is not valid", status_code=400)
        if body['password'] is None or body['password'] == "":
            raise APIException("Password is not valid", status_code=400)
        if body['name'] is None or body['name'] == "":
            raise APIException("Name is not valid", status_code=400)
        

        password = bcrypt.generate_password_hash(
            body['password'], 10).decode("utf-8")

        new_user = User(email=body['email'], password=password, is_active=True, name=body['name'], img_profile=None)

        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message":"User Created"}), 200

    except Exception as err:
        db.session.rollback()
        user = User.query.filter_by(email=body['email'])
        if user:
            raise APIException("User already exists", status_code=400)
        print(err)
        raise APIException({"Error when registering new user"}, status_code=400)


@app.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    email = body['email']
    password = body['password']

    user = User.query.filter_by(email=email).first()

    if not user:
        raise APIException("User does not exist", status_code=401)

    # validate if password enter by user and password in DB matches
    if not bcrypt.check_password_hash(user.password, password):
        raise APIException("User or password does not match. Check again!", status_code=401)

    access_token = create_access_token(identity=user.id, additional_claims={"is_administrator": False}, fresh=True) # Fresh here means that token whill refresh when user is authenticated
    return jsonify({"token": access_token, "user_id":user.id , "email": user.email, "message": f"Welcome, {user.name.split(' ')[0]}"}), 200


@app.route('/user_access_protected', methods=['GET'])  
@jwt_required()  # Decorator that protects this route

def access_protected():  

    print("User Id", get_jwt_identity())

    user = User.query.get(get_jwt_identity())
    
    # get_jwt() returns an object with an important property called jti
    jti = get_jwt()["jti"]

    tokenBlocked = BlockedList.query.filter_by(token=jti).first()
    # cuando hay coincidencia tokenBloked es instancia de la clase TokenBlockedList
    # cuando No hay coincidencia tokenBlocked = None

    if isinstance(tokenBlocked, BlockedList):
        return jsonify({"message":"Access denied"})

    response_body = {
        "isToken": "token válido",
        "user_id": user.id,  # get_jwt_identity(),
        "user_email": user.email,
    }

    return jsonify(response_body), 200


    
@app.route('/logout', methods=['GET'])  
@jwt_required()
def logout():
    print(get_jwt())
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)

    tokenBlocked = BlockedList(token=jti, created_at=now)
    db.session.add(tokenBlocked)
    db.session.commit()

    return jsonify({"message": "Token was deleted"})

@app.route("/admin_only", methods=["GET"])
@jwt_required()
@admin_only
def admin_only():

    return jsonify("Welcome admin")