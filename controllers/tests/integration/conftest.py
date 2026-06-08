import os
import pytest
from Projeto_Flask.__init__ import create_app
from ...models import Role, User, db

@pytest.fixture()
def app():
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app = create_app(
        {
            "SECRET_KEY": "dev",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///" + os.path.join(BASE_DIR, "teste_.sqlite"),
            "JWT_SECRET_KEY": "super-secret"
        }
    )
    with app.app_context():
        db.create_all()
        yield app

        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def access_token(client):
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user = User(username="Alex", password="teste", role_id=role.id)
    db.session.add(user)
    db.session.commit()

    response = client.post("/auth/login", json={"username": user.username, "password": user.password})
    return response.json["access_token"]

