import os
from ..main import request,get_jwt, jsonify, app, bcrypt, create_access_token, get_jwt_identity, jwt_required, JWTManager
from ..db import db
from ..modelos import User, BlockedList
from flask import Flask, url_for
from datetime import datetime
import json

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    user = User.query.get(get_jwt_identity())
    print(user)
    jti = get_jwt()["jti"]
    tocken_blocked = BlockedList.query.filter_by(token=jti).first()
    if isinstance(tocken_blocked, BlockedList):
        return jsonify({"msg":"Access denied"})

    return jsonify(logged_in_as=current_user), 200