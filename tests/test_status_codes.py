from http import HTTPStatus

import pytest

from app import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config["SECRET_KEY"] = "testing"
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_status_code(client):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK


def test_login_status_code(client):
    response = client.get("/login")
    assert response.status_code == HTTPStatus.OK


def test_register_status_code(client):
    response = client.get("/reg")
    assert response.status_code == HTTPStatus.OK


def test_logout_status_code(client):
    response = client.get("/logout")
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_profile_status_code(client):
    response = client.get("/profile")
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_courses_status_code(client):
    response = client.get("/courses")
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_terms_of_using_kairos_status_code(client):
    response = client.get("/terms")
    assert response.status_code == HTTPStatus.OK


def test_delete_course_status_code(client):
    response = client.get("/delete-course/1")
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_favorites_status_code(client):
    response = client.get("/favorites/1")
    assert response.status_code == HTTPStatus.UNAUTHORIZED
