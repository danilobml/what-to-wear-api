from http import HTTPStatus

from fastapi.testclient import TestClient

from what_to_wear.main import app


def test_root_should_return_ok():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.content == b'"Welcome to WhatToWear, your weather and clothes recommendation APP, powered by AI!"'
