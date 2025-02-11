from http import HTTPStatus

from fastapi.testclient import TestClient

from what_to_wear.main import app


def test_get_test_returns_test():
    client = TestClient(app)

    response = client.get('/test')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Test!'}
