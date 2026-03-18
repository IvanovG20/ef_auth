import pytest
from rest_framework.test import APIClient
from django.contrib.auth.hashers import make_password

from users.models import User, UserPermission, TokenBlackList


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def create_user():
    def _create_user(email="user@test.com", password="1234", is_admin=False):
        return User.objects.create(
            email=email,
            password=make_password(password),
            is_admin=is_admin
        )
    return _create_user


def login(client, email, password):
    response = client.post("/login/", {
        "email": email,
        "password": password
    })
    return response.data.get("token")


@pytest.mark.django_db
def test_register_success(client):
    response = client.post("/register/", {
        "email": "test@test.com",
        "password": "1234",
        "password_repeat": "1234"
    })

    assert response.status_code == 200
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_register_password_mismatch(client):
    response = client.post("/register/", {
        "email": "test@test.com",
        "password": "1234",
        "password_repeat": "4321"
    })

    assert response.status_code == 400


@pytest.mark.django_db
def test_user_gets_default_permission(client):
    client.post("/register/", {
        "email": "test@test.com",
        "password": "1234",
        "password_repeat": "1234"
    })

    user = User.objects.first()

    assert UserPermission.objects.filter(
        user=user,
        resource="project",
        action="view"
    ).exists()


@pytest.mark.django_db
def test_login_success(client, create_user):
    create_user()

    token = login(client, "user@test.com", "1234")

    assert token is not None


@pytest.mark.django_db
def test_login_wrong_password(client, create_user):
    create_user()

    response = client.post("/login/", {
        "email": "user@test.com",
        "password": "wrong"
    })

    assert response.status_code == 401


@pytest.mark.django_db
def test_logout_blacklist(client, create_user):
    create_user()

    token = login(client, "user@test.com", "1234")

    client.post(
        "/logout/",
        HTTP_AUTHORIZATION=f"Bearer {token}"
    )

    assert TokenBlackList.objects.filter(token=token).exists()
