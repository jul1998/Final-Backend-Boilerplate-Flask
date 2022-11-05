import os
from ..main import request, jsonify, app, bcrypt
from ..db import db
from ..modelos import User
from flask import Flask, url_for
from datetime import datetime
import json
from ..utils import APIException

@app.route('/signup' , methods=['POST'])
def signup():
    body = request.get_json()
    print(body)
    #print(body['username'])     
    try:
        if body is None:
           return jsonify("Body está vacío o email no viene en el body, es inválido")
        if body['email'] is None or body['email']=="":
           return jsonify("email es inválido")
        if body['password'] is None or body['password']=="":
           return jsonify("password es inválido")      
      

        password = bcrypt.generate_password_hash(body['password'], 10).decode("utf-8")
        new_user = User(email=body['email'], password=password, is_active=True)

        user = db.session.query(User).filter_by(email=body['email']).first()
        if user:
            return jsonify("El usuario ya existe")
                
        print(body['email'])
        #print(new_user.serialize())
        db.session.add(new_user) 
        db.session.commit()
        return jsonify("Usuario creado exitosamente"), 201

    except Exception as err:
        db.session.rollback()
        print(err)
        return jsonify({"mensaje": "error al registrar usuario"}), 500



