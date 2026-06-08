from http import HTTPStatus
from ...models import Role
from ...models import db, User
from sqlalchemy import func

def test_create_user(client, access_token):
    role_id = db.session.execute(db.select(Role.id).where(Role.name == "admin")).scalar()
    payload = {"username": "testuser", "password": "testpass", "role_id": role_id}

    response = client.post("/users/", json=payload, headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {"message": "User created successfully"}
    assert db.session.execute(db.select(func.count(User.id))).scalar() == 2

def test_list_users(client, access_token):
    user = db.session.execute(db.select(User).where(User.username == "Alex")).scalar()
    response = client.post("/auth/login", json={"username": user.username, "password": user.password})
    access_token = response.json["access_token"]

    response = client.get("/users/", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "users": [
            {
                "id": user.id,
                "username": user.username,
                "role": {
                    "id": user.role.id,
                    "name": user.role.name
                },
            }
        ]
    }