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


def test_registration_form_small_password(client):
    response = client.post(
        "/reg",
        data={
            "name": "test",
            "password": "123",
            "password_again": "123",
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_empty_registration_form(client):
    response = client.post(
        "/reg",
        data={
            "name": "",
            "password": "",
            "password_again": "",
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_different_passwords(client):
    response = client.post(
        "/reg",
        data={
            "name": "test",
            "password": "password1",
            "password_again": "password2",
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_course_form(client):
    response = client.post(
        "/create-course",
        data={
            "users_theme": "",
            "users_desires": "test",
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
