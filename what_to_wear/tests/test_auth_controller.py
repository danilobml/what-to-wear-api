import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from what_to_wear.api.controllers.auth_controller import router
from what_to_wear.main import app

client = TestClient(app)
app.include_router(router, prefix="/auth")


@pytest.mark.asyncio
async def test_register_user_success():
    with patch("what_to_wear.api.controllers.auth_controller.get_user_by_username", return_value=None), \
         patch("what_to_wear.api.controllers.auth_controller.create_user", new_callable=AsyncMock):

        response = client.post("/auth/register", json={"username": "testuser", "password": "securepassword"})
        assert response.status_code == 201
        assert response.json() == "User created successfully."


@pytest.mark.asyncio
async def test_register_user_already_exists():
    with patch("what_to_wear.api.controllers.auth_controller.get_user_by_username", return_value=True):

        response = client.post("/auth/register", json={"username": "existinguser", "password": "securepassword"})
        assert response.status_code == 400
        assert response.json()["detail"] == "Username already exists"


@pytest.mark.asyncio
async def test_register_user_server_error():
    with patch("what_to_wear.api.controllers.auth_controller.get_user_by_username", side_effect=Exception("DB error")):

        response = client.post("/auth/register", json={"username": "testuser", "password": "securepassword"})
        assert response.status_code == 500
        assert "Error creating user" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_success():
    mock_user = type("User", (), {"username": "testuser"})()

    with patch("what_to_wear.api.controllers.auth_controller.authenticate_user", return_value=mock_user), \
         patch("what_to_wear.api.controllers.auth_controller.create_access_token", return_value="mock_token"):

        response = client.post("/auth/login", json={"username": "testuser", "password": "securepassword"})
        assert response.status_code == 200
        assert response.json()["access_token"] == "mock_token"
        assert response.json()["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials():
    with patch("what_to_wear.api.controllers.auth_controller.authenticate_user", return_value=None):

        response = client.post("/auth/login", json={"username": "testuser", "password": "wrongpassword"})
        assert response.status_code == 401
        assert response.json()["detail"] == "Incorrect username or password"
