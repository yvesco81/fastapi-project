import pytest
from app import schemas
from jose import jwt
from app.config import settings


# def test_root(client):
#     res = client.get("/")
#     # print(res.json())
#     assert res.status_code == 200
#     # assert res.json() == {"msg": "Hello World"}


def test_create_user(client):
    res = client.post("/users/",
                      json={"email": "yvesco@email.com", "password": "azerty"})

    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "yvesco@email.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post("/login",
                      data={"username": test_user['email'],
                            "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])

    id = payload.get("user_id")

    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code",
                         [('wrongemail', "azerty", 403),
                          ('yvesco@email.com', 'wrongpassword', 403),
                          ('wrongemail', 'wrongpassword', 403),
                          (None, 'azerty', 422),
                          ('yvesco@email.com', None, 422)])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login",
                      data={"username": email,
                            "password": password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'