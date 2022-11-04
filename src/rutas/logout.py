import os
from ..main import request, jsonify, app, bcrypt, create_access_token, get_jwt_identity, jwt_required, JWTManager, get_jwt
from ..db import db
from ..modelos import BlockedList
from flask import Flask, url_for
from datetime import datetime
import json
import datetime

@app.route("/logout", methods=["GET"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    print(jti)
    now = datetime.datetime.now(datetime.timezone.utc)
    print(now)

    token_blocked = BlockedList(token=jti, created_at=now)
    db.session.add(token_blocked)
    db.session.commit()

    return jsonify("Blocked Token")