from flask import Blueprint, Flask, jsonify, request
from http import HTTPStatus
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from ..models import db, User

app = Blueprint("auth", __name__, url_prefix="/auth")

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = db.session.execute(db.select(User).where(User.username == username)).scalar()
    if not user or user.password != password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify(access_token=access_token)