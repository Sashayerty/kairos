from http import HTTPStatus

import pytest

from app import create_test_app


@pytest.fixture
def app():
    app = create_test_app()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_registration(client):
    response = client.post(
        "/reg",
        data={
            "name": "test_registration",
            "password": "123123123",
            "password_again": "123123123",
        },
        follow_redirects=True,
    )
    assert response.status_code == HTTPStatus.OK


def test_registration_registered_user(client):
    response = client.post(
        "/reg",
        data={
            "name": "test_registration",
            "password": "123123123",
            "password_again": "123123123",
        },
        follow_redirects=True,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_login(client):
    response = client.post(
        "/login",
        data={
            "name": "test_registration",
            "password": "123123123",
        },
        follow_redirects=True,
    )
    assert response.status_code == HTTPStatus.OK
