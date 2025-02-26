import json
from http import HTTPStatus
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from what_to_wear.api.controllers.weather_controller import router
from what_to_wear.api.models.schemas.current_weather import CurrentWeatherResponse
from what_to_wear.api.models.schemas.forecast_weather import ForecastWeatherResponse
from what_to_wear.api.services.auth_service import get_current_user
from what_to_wear.main import app

client = TestClient(app)
app.include_router(router, prefix="/weather")


def load_mock_data(filename: str):
    json_path = Path(__file__).parent / "mock_data" / filename
    with open(json_path, "r", encoding="utf-8") as file:
        return json.load(file)


MOCK_CURRENT_WEATHER_RESPONSE = load_mock_data("mock_current_weather_response.json")
MOCK_FORECAST_WEATHER_RESPONSE = load_mock_data("mock_forecast_weather_response.json")


@pytest.fixture
def override_auth():
    app.dependency_overrides[get_current_user] = lambda: {"username": "testuser"}
    yield
    app.dependency_overrides.pop(get_current_user, None)


@pytest.mark.asyncio
async def test_get_current_weather(override_auth):
    with patch("what_to_wear.api.controllers.weather_controller.get_current_weather_data",
               new_callable=AsyncMock) as mock_weather:
        mock_weather.return_value = CurrentWeatherResponse.model_validate(MOCK_CURRENT_WEATHER_RESPONSE)

        headers = {"Authorization": "Bearer fake_token"}
        response = client.get(
            "/weather/current",
            params={"city": "Test City"},
            headers=headers
        )

        expected_temp = 20.0
        assert response.status_code == HTTPStatus.OK
        assert response.json()["location"]["name"] == "Test City"
        assert response.json()["current"]["temp_c"] == expected_temp


@pytest.mark.asyncio
async def test_get_forecast_weather(override_auth):
    with patch("what_to_wear.api.controllers.weather_controller.get_forecast_weather_data",
               new_callable=AsyncMock) as mock_weather:
        mock_weather.return_value = ForecastWeatherResponse.model_validate(MOCK_FORECAST_WEATHER_RESPONSE)

        headers = {"Authorization": "Bearer fake_token"}
        response = client.get(
            "/weather/forecast",
            params={"lat": 12.34, "lon": 56.78, "days": 3},
            headers=headers
        )

        expected_maxtemp = 25.0
        assert response.status_code == HTTPStatus.OK
        assert response.json()["location"]["name"] == "Test City"
        assert response.json()["forecast"]["forecastday"][0]["day"]["maxtemp_c"] == expected_maxtemp


@pytest.mark.asyncio
async def test_get_current_weather_unauthorized():
    response = client.get("/weather/current", params={"lat": 12.34, "lon": 56.78})
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_forecast_weather_unauthorized():
    response = client.get("/weather/forecast", params={"city": "Test City", "days": 3})
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_current_weather_missing_params():
    headers = {"Authorization": "Bearer fake_token"}

    response = client.get("/weather/current", params={}, headers=headers)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    response = client.get("/weather/current", params={"lat": 12.34}, headers=headers)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    response = client.get("/weather/current", params={"lon": 56.78}, headers=headers)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_get_current_weather_too_many_params():
    headers = {"Authorization": "Bearer fake_token"}

    response = client.get("/weather/current", params={"lat": 12.34, "lon": 56.78, "city": "Test City"}, headers=headers)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_get_forecast_weather_invalid_days(override_auth):
    headers = {"Authorization": "Bearer fake_token"}
    response = client.get(
        "/weather/forecast",
        params={"city": "Test City", "days": "three"},
        headers=headers
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_get_current_weather_server_error(override_auth):
    with patch("what_to_wear.api.controllers.weather_controller.get_current_weather_data",
               new_callable=AsyncMock) as mock_weather:
        mock_weather.side_effect = Exception("Internal Server Error")

        headers = {"Authorization": "Bearer fake_token"}
        response = client.get(
            "/weather/current",
            params={"lat": 12.34, "lon": 56.78},
            headers=headers
        )

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
