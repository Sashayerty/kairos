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


def test_api_status_code(client):
    response = client.get("/api/")
    assert response.status_code == HTTPStatus.OK
