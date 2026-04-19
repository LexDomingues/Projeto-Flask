from flask import Blueprint, Flask, request
from http import HTTPStatus
from ..models import db, User

app = Blueprint("user", __name__, url_prefix="/users")

def _create_user():
    data = request.json

    if not data:
        return {"error": "JSON inválido"}, 400

    if "username" not in data:
        return {"error": "username é obrigatório"}, 400

    user = User(
        username=data["username"],
        email=data.get("email")  # evita erro
    )

    db.session.add(user)
    db.session.commit()
    return None

def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    return [{"id": user.id, "username": user.username, "email": user.email} for user in users]

@app.route("/", methods=["GET", "POST"])
def handle_user():
    if request.method == "POST":
        error = _create_user()
        if error:
            return error
        return {"message": "User created successfully"}, HTTPStatus.CREATED
    else:
        return {"users": _list_users()}
    
@app.route("/<int:user_id>")
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return {"id": user.id, "username":user.username, "email": user.email}
