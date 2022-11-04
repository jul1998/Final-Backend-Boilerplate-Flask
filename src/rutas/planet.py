import os
from ..main import request, jsonify, app, bcrypt
from ..db import db
from ..modelos import Planets
from flask import Flask, url_for
from datetime import datetime
import json

@app.route("/planets", methods=["POST"])
def insert_planets():
    body = request.get_json()
    planet_name = body["planet_name"]
    population = body["population"]

    try:
        new_planet = Planets(planet_name=planet_name, population=population)
        db.session.add(new_planet)
        db.session.commit()
        return jsonify("Planet added correctly"),200
    except Exception as err:
        db.session.rollback()
        print(err)
        return jsonify({"mensaje": "error al registrar usuario"}), 500
