import os
from ..main import request, jsonify, app, bcrypt
from ..db import db
from ..modelos import User
from flask import Flask, url_for
from datetime import datetime
import json

@app.route('/signup' , methods=['POST'])
def signup():
    body = request.get_json()
    #print(body['username'])     
    try:
        if body is None:
            raise APIException("Body está vacío o email no viene en el body, es inválido" , status_code=400)
        if body['email'] is None or body['email']=="":
            raise APIException("email es inválido" , status_code=400)
        if body['password'] is None or body['password']=="":
            raise APIException("password es inválido" , status_code=400)      
      

        password = bcrypt.generate_password_hash(body['password'], 10).decode("utf-8")

        new_user = User(email=body['email'], password=password, is_active=True)
        users = User.query.all()
        users = list(map( lambda user: user.serialize(), users))

        for i in range(len(users)):
            if(users[i]['email']==new_user.serialize()['email']):
                raise APIException("El usuario ya existe" , status_code=400)
                
        print(new_user)
        #print(new_user.serialize())
        db.session.add(new_user) 
        db.session.commit()
        return jsonify({"mensaje": "Usuario creado exitosamente"}), 201

    except Exception as err:
        db.session.rollback()
        print(err)
        return jsonify({"mensaje": "error al registrar usuario"}), 500