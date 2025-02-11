from http import HTTPStatus

from fastapi.testclient import TestClient

from what_to_wear.main import app


def test_root_should_return_hello():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Welcome to WhatToWear!'}
