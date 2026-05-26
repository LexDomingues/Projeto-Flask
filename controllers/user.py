from ..controllers .utils import requires_role
from flask import Blueprint, Flask, request
from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import column, inspect
from ..models import db, User

app = Blueprint("user", __name__, url_prefix="/users")

#CREATE
def _create_user():
    data = request.json

    if not data:
        return {"error": "JSON inválido"}, 400

    if "username" not in data:
        return {"error": "username é obrigatório"}, 400

    user = User(
        username=data["username"],
        password=data["password"],
        role_id=data["role_id"], 
    )

    db.session.add(user)
    db.session.commit()
    return None

#READ
def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    return [
        {
            "id": user.id,
            "username": user.username,
            "role":{
                "id": user.role.id,
                "name": user.role.name,
            },
        }
          for user in users
          ]

@app.route("/", methods=["GET", "POST"])
@jwt_required()
@requires_role("admin") 
def list_or_create_user():
    requires_role("admin")
    if request.method == "POST":
         _create_user()
         return {"message": "User created successfully"}, HTTPStatus.CREATED
    else:
        return {"users": _list_users()}

# READ
@app.route("/<int:user_id>")
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return {"id": user.id, "username":user.username}


@app.route("/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json

    mapper = inspect(User)
    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])
    db.session.commit()

    return {"id": user.id, "username":user.username, "password": user.password}

#DELETE
@app.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT