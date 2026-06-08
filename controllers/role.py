from flask import Blueprint, Flask, jsonify, request
from http import HTTPStatus
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from .models import db, User
from .models import Role

app = Blueprint("role", __name__, url_prefix="/roles")

@app.route("/", methods=["POST"])
def create_role():
    data = request.json
    role = Role(name=data["name"])
    db.session.add(role)
    db.session.commit()
    return {"message": "Role created!"}, HTTPStatus.CREATED