import pytest
import json

from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from pathlib import Path

from what_to_wear.api.controllers.recommendation_controller import router
from what_to_wear.api.services.auth_service import get_current_user
from what_to_wear.api.models.schemas.current_weather import CurrentWeatherResponse
from what_to_wear.api.models.schemas.forecast_weather import ForecastWeatherResponse
from what_to_wear.main import app

client = TestClient(app)
app.include_router(router, prefix="/recommendation")


def load_mock_data(filename: str):
    json_path = Path(__file__).parent / "mock_data" / filename
    with open(json_path, "r") as file:
        return json.load(file)


MOCK_CURRENT_WEATHER_RESPONSE = load_mock_data("mock_current_weather_response.json")
MOCK_FORECAST_WEATHER_RESPONSE = load_mock_data("mock_forecast_weather_response.json")
MOCK_LLM_RECOMMENDATION = "Wear a light jacket and sunglasses."


@pytest.fixture
def override_auth():
    app.dependency_overrides[get_current_user] = lambda: {"username": "testuser"}
    yield
    app.dependency_overrides.pop(get_current_user, None)


@pytest.mark.asyncio
async def test_get_current_recommendation(override_auth):
    with patch("what_to_wear.api.controllers.recommendation_controller.get_current_weather_data",
               new_callable=AsyncMock) as mock_weather, \
         patch("what_to_wear.api.controllers.recommendation_controller.get_llm_recommendation",
               new_callable=AsyncMock) as mock_recommendation:

        mock_weather.return_value = CurrentWeatherResponse.model_validate(MOCK_CURRENT_WEATHER_RESPONSE)
        mock_recommendation.return_value = MOCK_LLM_RECOMMENDATION

        headers = {"Authorization": "Bearer fake_token"}
        response = client.get(
            "/recommendation/current",
            params={"lat": 12.34, "lon": 56.78},
            headers=headers
        )

        assert response.status_code == 200
        assert response.json() == MOCK_LLM_RECOMMENDATION


@pytest.mark.asyncio
async def test_get_forecast_recommendation(override_auth):
    with patch("what_to_wear.api.controllers.recommendation_controller.get_forecast_weather_data",
               new_callable=AsyncMock) as mock_weather, \
         patch("what_to_wear.api.controllers.recommendation_controller.get_llm_recommendation",
               new_callable=AsyncMock) as mock_recommendation:

        mock_weather.return_value = ForecastWeatherResponse.model_validate(MOCK_FORECAST_WEATHER_RESPONSE)
        mock_recommendation.return_value = MOCK_LLM_RECOMMENDATION

        headers = {"Authorization": "Bearer fake_token"}
        response = client.get(
            "/recommendation/forecast",
            params={"city": "Test City", "days": 3},
            headers=headers
        )

        assert response.status_code == 200
        assert response.json() == MOCK_LLM_RECOMMENDATION


@pytest.mark.asyncio
async def test_get_current_recommendation_unauthorized():
    response = client.get("/recommendation/current", params={"lat": 12.34, "lon": 56.78})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_forecast_recommendation_unauthorized():
    response = client.get("/recommendation/forecast", params={"lat": 12.34, "lon": 56.78, "days": 3})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_current_recommendation_missing_params():
    headers = {"Authorization": "Bearer fake_token"}

    response = client.get("/recommendation/current", params={}, headers=headers)
    assert response.status_code == 422

    response = client.get("/recommendation/current", params={"lat": 12.34}, headers=headers)
    assert response.status_code == 422

    response = client.get("/recommendation/current", params={"lon": 56.78}, headers=headers)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_current_recommendation_too_many_params():
    headers = {"Authorization": "Bearer fake_token"}

    response = client.get("/recommendation/current", params={
        "lat": 12.34, "lon": 56.78, "city": "Test City"}, headers=headers)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_forecast_recommendation_invalid_days(override_auth):
    headers = {"Authorization": "Bearer fake_token"}
    response = client.get(
        "/recommendation/forecast",
        params={"lat": 12.34, "lon": 56.78, "days": "three"},
        headers=headers
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_forecast_recommendation_too_many_params():
    headers = {"Authorization": "Bearer fake_token"}

    response = client.get("/recommendation/forecast", params={
        "lat": 12.34, "lon": 56.78, "city": "Test City", "days": 3}, headers=headers)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_current_recommendation_server_error(override_auth):
    with patch("what_to_wear.api.controllers.recommendation_controller.get_current_weather_data",
               new_callable=AsyncMock) as mock_weather:

        mock_weather.side_effect = Exception("Internal Server Error")

        headers = {"Authorization": "Bearer fake_token"}
        response = client.get(
            "/recommendation/current",
            params={"lat": 12.34, "lon": 56.78},
            headers=headers
        )

        assert response.status_code == 500
