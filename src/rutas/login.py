import os
from ..main import request, jsonify, app, bcrypt, create_access_token, get_jwt_identity, jwt_required, JWTManager
from ..db import db
from ..modelos import User
from flask import Flask, url_for
from datetime import datetime
import json

jwt = JWTManager(app)

@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("username", None)
    password = request.json.get("password", None)
 
    all_info = db.session.query(User).filter_by(email=email).first()
    


    try:
        if email != all_info.email:
            return jsonify({"msg": "Bad username or password"}), 401
        if email is None:
             return jsonify({"msg": "Email is none"}), 401
        if not bcrypt.check_password_hash(all_info.password, password):
            return jsonify({"msg":"Password does not match"}),200
        print(all_info.id)
        access_token = create_access_token(identity=all_info.email)#here we select what we want to return with token,
        #Then, generate new token
        return jsonify(access_token=access_token)
    except:
        return jsonify("user does not exist"),401
