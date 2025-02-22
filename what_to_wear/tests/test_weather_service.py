import pytest
import respx
import httpx
import json
from pathlib import Path

from what_to_wear.api.models.schemas.forecast_weather import ForecastWeatherResponse
from what_to_wear.api.services.weather_service import get_current_weather_data, get_forecast_weather_data
from what_to_wear.api.models.schemas.current_weather import CurrentWeatherResponse
from what_to_wear.api.utils.constants import WEATHER_API_BASE_URL, WEATHER_API_KEY
from fastapi import HTTPException


json_path = Path(__file__).parent / "mock_data/mock_current_weather_response.json"
with open(json_path, "r") as file:
    MOCK_CURRENT_WEATHER_RESPONSE = json.load(file)


json_path = Path(__file__).parent / "mock_data" / "mock_forecast_weather_response.json"
with open(json_path, "r") as file:
    MOCK_FORECAST_WEATHER_RESPONSE = json.load(file)


@pytest.mark.asyncio
@respx.mock
async def test_get_current_weather_data_success():
    lat, lon = "12.34", "56.78"
    q_param = f"{lat},{lon}"
    url = f"{WEATHER_API_BASE_URL}/current.json"

    respx.get(url, params={"key": WEATHER_API_KEY, "q": q_param}).mock(
        return_value=httpx.Response(200, json=MOCK_CURRENT_WEATHER_RESPONSE)
    )

    response = await get_current_weather_data(lat, lon)

    assert isinstance(response, CurrentWeatherResponse)
    assert response.location.name == "Test City"
    assert response.current.temp_c == 20


@pytest.mark.asyncio
@respx.mock
async def test_get_current_weather_data_http_error():
    lat, lon = "12.34", "56.78"
    q_param = f"{lat},{lon}"
    url = f"{WEATHER_API_BASE_URL}/current.json"

    respx.get(url, params={"key": WEATHER_API_KEY, "q": q_param}).mock(
        return_value=httpx.Response(500, json={"error": "Internal Server Error"})
    )

    with pytest.raises(HTTPException) as exc_info:
        await get_current_weather_data(lat, lon)

    assert exc_info.value.status_code == 500
    assert "Weather API error" in str(exc_info.value.detail)


@pytest.mark.asyncio
@respx.mock
async def test_get_current_weather_data_request_error():
    lat, lon = "12.34", "56.78"
    q_param = f"{lat},{lon}"
    url = f"{WEATHER_API_BASE_URL}/current.json"

    respx.get(url, params={"key": WEATHER_API_KEY, "q": q_param}).mock(
        side_effect=httpx.RequestError("Connection Error"))

    with pytest.raises(HTTPException) as exc_info:
        await get_current_weather_data(lat, lon)

    assert exc_info.value.status_code == 503
    assert "Service unavailable" in str(exc_info.value.detail)


@pytest.mark.asyncio
@respx.mock
async def test_get_current_weather_data_unexpected_error():
    lat, lon = "12.34", "56.78"
    q_param = f"{lat},{lon}"
    url = f"{WEATHER_API_BASE_URL}/current.json"

    respx.get(url, params={"key": WEATHER_API_KEY, "q": q_param}).mock(side_effect=Exception("Unexpected Error"))

    with pytest.raises(HTTPException) as exc_info:
        await get_current_weather_data(lat, lon)

    assert exc_info.value.status_code == 500
    assert "Unexpected Error" in str(exc_info.value.detail)


@pytest.mark.asyncio
@respx.mock
async def test_get_forecast_weather_data_success():
    lat, lon, days = "12.34", "56.78", 3
    q_param = f"{lat},{lon}"
    url = f"{WEATHER_API_BASE_URL}/forecast.json"

    respx.get(url, params={"key": WEATHER_API_KEY, "q": q_param, "days": days}).mock(
        return_value=httpx.Response(200, json=MOCK_FORECAST_WEATHER_RESPONSE)
    )

    response = await get_forecast_weather_data(lat, lon, days)

    assert isinstance(response, ForecastWeatherResponse)
    assert response.location.name == "Test City"
    assert response.current.temp_c == 20
    assert response.forecast.forecastday[0].day.maxtemp_c == 25.0


@pytest.mark.asyncio
@respx.mock
async def test_get_forecast_weather_data_http_error():
    lat, lon, days = "12.34", "56.78", 3
    q_param = f"{lat},{lon}"
    url = f"{WEATHER_API_BASE_URL}/forecast.json"

    respx.get(url, params={"key": WEATHER_API_KEY, "q": q_param, "days": days}).mock(
        return_value=httpx.Response(500, json={"error": "Internal Server Error"})
    )

    with pytest.raises(HTTPException) as exc_info:
        await get_forecast_weather_data(lat, lon, days)

    assert exc_info.value.status_code == 500
    assert "Weather API error" in str(exc_info.value.detail)


@pytest.mark.asyncio
@respx.mock
async def test_get_forecast_weather_data_request_error():
    lat, lon, days = "12.34", "56.78", 3
    q_param = f"{lat},{lon}"
    url = f"{WEATHER_API_BASE_URL}/forecast.json"

    respx.get(url, params={"key": WEATHER_API_KEY, "q": q_param, "days": days}).mock(
        side_effect=httpx.RequestError("Connection Error")
    )

    with pytest.raises(HTTPException) as exc_info:
        await get_forecast_weather_data(lat, lon, days)

    assert exc_info.value.status_code == 503
    assert "Service unavailable" in str(exc_info.value.detail)


@pytest.mark.asyncio
@respx.mock
async def test_get_forecast_weather_data_unexpected_error():
    lat, lon, days = "12.34", "56.78", 3
    q_param = f"{lat},{lon}"
    url = f"{WEATHER_API_BASE_URL}/forecast.json"

    respx.get(url, params={"key": WEATHER_API_KEY, "q": q_param, "days": days}).mock(
        side_effect=Exception("Unexpected Error")
    )

    with pytest.raises(HTTPException) as exc_info:
        await get_forecast_weather_data(lat, lon, days)

    assert exc_info.value.status_code == 500
    assert "Unexpected Error" in str(exc_info.value.detail)
