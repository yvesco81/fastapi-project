from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models

# url = 'postgresql://postgres:Boulogne_1981@localhost:5432/fastapi_test'
url = f'postgresql://{settings.database_username}:{settings.database_password}@' \
      f'{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(url)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture()
def test_user(client):
    user_data = {"email": "yvesco@email.com", "password": "azerty"}

    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture()
def test_user_2(client):
    user_data = {"email": "amaya@email.com", "password": "qsdfg"}

    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture()
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture()
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}

    return client


@pytest.fixture()
def test_posts(session, test_user, test_user_2):
    posts_data = [{"title": "first title",
                   "content": "first content",
                   "user_id": test_user['id']},
                  {"title": "second title",
                   "content": "second content",
                   "user_id": test_user['id']},
                  {"title": "second title",
                   "content": "second content",
                   "user_id": test_user_2['id']}
                  ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)

    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                  models.Post(title="second title", content="second content", owner_id=test_user['id'])])

    session.commit()
    return session.query(models.Post).all()