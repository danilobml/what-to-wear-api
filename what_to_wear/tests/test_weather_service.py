import pytest
import respx
import httpx
import json
from pathlib import Path
from fastapi import HTTPException

from what_to_wear.api.models.schemas.forecast_weather import ForecastWeatherResponse
from what_to_wear.api.models.schemas.current_weather import CurrentWeatherResponse
from what_to_wear.api.services.weather_service import get_current_weather_data, get_forecast_weather_data
from what_to_wear.api.utils.constants import WEATHER_API_BASE_URL, WEATHER_API_KEY


def load_mock_data(filename: str):
    json_path = Path(__file__).parent / "mock_data" / filename
    with open(json_path, "r") as file:
        return json.load(file)


MOCK_CURRENT_WEATHER_RESPONSE = load_mock_data("mock_current_weather_response.json")
MOCK_FORECAST_WEATHER_RESPONSE = load_mock_data("mock_forecast_weather_response.json")


@pytest.mark.asyncio
@respx.mock
async def test_get_current_weather_data_with_lat_lon():
    lat, lon, city = "12.34", "56.78", None
    q_param = f"{lat},{lon}"
    url = f"{WEATHER_API_BASE_URL}/current.json"

    respx.get(url, params={"key": WEATHER_API_KEY, "q": q_param}).mock(
        return_value=httpx.Response(200, json=MOCK_CURRENT_WEATHER_RESPONSE)
    )

    response = await get_current_weather_data(lat, lon, city)

    assert isinstance(response, CurrentWeatherResponse)
    assert response.location.name == "Test City"
    assert response.current.temp_c == 20


@pytest.mark.asyncio
@respx.mock
async def test_get_current_weather_data_with_city():
    city = "Berlin"
    lat, lon = None, None
    q_param = city
    url = f"{WEATHER_API_BASE_URL}/current.json"

    respx.get(url, params={"key": WEATHER_API_KEY, "q": q_param}).mock(
        return_value=httpx.Response(200, json=MOCK_CURRENT_WEATHER_RESPONSE)
    )

    response = await get_current_weather_data(lat, lon, city)

    assert isinstance(response, CurrentWeatherResponse)
    assert response.location.name == "Test City"
    assert response.current.temp_c == 20


@pytest.mark.asyncio
@respx.mock
async def test_get_forecast_weather_data_with_lat_lon():
    lat, lon, city, days = "12.34", "56.78", None, 3
    q_param = f"{lat},{lon}"
    url = f"{WEATHER_API_BASE_URL}/forecast.json"

    respx.get(url, params={"key": WEATHER_API_KEY, "q": q_param, "days": days}).mock(
        return_value=httpx.Response(200, json=MOCK_FORECAST_WEATHER_RESPONSE)
    )

    response = await get_forecast_weather_data(lat, lon, city, days)

    assert isinstance(response, ForecastWeatherResponse)
    assert response.location.name == "Test City"
    assert response.current.temp_c == 20
    assert response.forecast.forecastday[0].day.maxtemp_c == 25.0


@pytest.mark.asyncio
@respx.mock
async def test_get_forecast_weather_data_with_city():
    city = "Berlin"
    lat, lon, days = None, None, 3
    q_param = city
    url = f"{WEATHER_API_BASE_URL}/forecast.json"

    respx.get(url, params={"key": WEATHER_API_KEY, "q": q_param, "days": days}).mock(
        return_value=httpx.Response(200, json=MOCK_FORECAST_WEATHER_RESPONSE)
    )

    response = await get_forecast_weather_data(lat, lon, city, days)

    assert isinstance(response, ForecastWeatherResponse)
    assert response.location.name == "Test City"
    assert response.current.temp_c == 20
    assert response.forecast.forecastday[0].day.maxtemp_c == 25.0


@pytest.mark.asyncio
@respx.mock
async def test_get_current_weather_data_missing_params():
    lat, lon, city = None, None, None

    with pytest.raises(HTTPException) as exc_info:
        await get_current_weather_data(lat, lon, city)

    assert exc_info.value.status_code == 400
    assert "Either 'city' or ('lat', 'lon') must be provided" in str(exc_info.value.detail)


@pytest.mark.asyncio
@respx.mock
async def test_get_current_weather_data_invalid_city():
    city = "InvalidCity"
    lat, lon = None, None
    q_param = city
    url = f"{WEATHER_API_BASE_URL}/current.json"

    respx.get(url, params={"key": WEATHER_API_KEY, "q": q_param}).mock(
        return_value=httpx.Response(404, json={"error": "City not found"})
    )

    with pytest.raises(HTTPException) as exc_info:
        await get_current_weather_data(lat, lon, city)

    assert exc_info.value.status_code == 404
    assert "City or coordinates not found" in str(exc_info.value.detail)


@pytest.mark.asyncio
@respx.mock
async def test_get_current_weather_data_invalid_lat_lon():
    lat, lon, city = "invalid", "invalid", None
    q_param = f"{lat},{lon}"
    url = f"{WEATHER_API_BASE_URL}/current.json"

    respx.get(url, params={"key": WEATHER_API_KEY, "q": q_param}).mock(
        return_value=httpx.Response(400, json={"error": "Invalid coordinates"})
    )

    with pytest.raises(HTTPException) as exc_info:
        await get_current_weather_data(lat, lon, city)

    assert exc_info.value.status_code == 400
    assert "Invalid city or coordinates" in str(exc_info.value.detail)


@pytest.mark.asyncio
@respx.mock
async def test_get_forecast_weather_data_missing_params():
    lat, lon, city, days = None, None, None, None

    with pytest.raises(HTTPException) as exc_info:
        await get_forecast_weather_data(lat, lon, city, days)

    assert exc_info.value.status_code == 400
    assert "Either 'city' or ('lat', 'lon') must be provided" in str(exc_info.value.detail)


@pytest.mark.asyncio
@respx.mock
async def test_get_forecast_weather_data_invalid_city():
    city = "InvalidCity"
    lat, lon, days = None, None, 3
    q_param = city
    url = f"{WEATHER_API_BASE_URL}/forecast.json"

    respx.get(url, params={"key": WEATHER_API_KEY, "q": q_param, "days": days}).mock(
        return_value=httpx.Response(404, json={"error": "City not found"})
    )

    with pytest.raises(HTTPException) as exc_info:
        await get_forecast_weather_data(lat, lon, city, days)

    assert exc_info.value.status_code == 404
    assert "City or coordinates not found" in str(exc_info.value.detail)


@pytest.mark.asyncio
@respx.mock
async def test_get_forecast_weather_data_invalid_lat_lon():
    lat, lon, city, days = "invalid", "invalid", None, 3
    q_param = f"{lat},{lon}"
    url = f"{WEATHER_API_BASE_URL}/forecast.json"

    respx.get(url, params={"key": WEATHER_API_KEY, "q": q_param, "days": days}).mock(
        return_value=httpx.Response(400, json={"error": "Invalid coordinates"})
    )

    with pytest.raises(HTTPException) as exc_info:
        await get_forecast_weather_data(lat, lon, city, days)

    assert exc_info.value.status_code == 400
    assert "Invalid city or coordinates" in str(exc_info.value.detail)
