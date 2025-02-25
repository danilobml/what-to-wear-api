import pytest
import respx
import httpx
import json
from pathlib import Path

from what_to_wear.api.services.recommendation_service import get_llm_recommendation, query_llm
from what_to_wear.api.models.schemas.current_weather import CurrentWeatherResponse
from what_to_wear.api.models.schemas.forecast_weather import ForecastWeatherResponse
from what_to_wear.api.utils.constants import LLM_API_URL, HEADERS, RequestTypeEnum, ModelTypeEnum
from fastapi import HTTPException


def load_mock_data(filename: str):
    json_path = Path(__file__).parent / "mock_data" / filename
    with open(json_path, "r") as file:
        return json.load(file)


MOCK_CURRENT_WEATHER_RESPONSE = load_mock_data("mock_current_weather_response.json")
MOCK_FORECAST_WEATHER_RESPONSE = load_mock_data("mock_forecast_weather_response.json")
MOCK_LLM_RESPONSE = {"choices": [{"message": {"content": "Wear a light jacket."}}]}
MOCK_INVALID_LLM_RESPONSE = {"error": "Invalid request"}


@pytest.mark.asyncio
@respx.mock
async def test_get_llm_recommendation_current():
    weather_data = CurrentWeatherResponse(**MOCK_CURRENT_WEATHER_RESPONSE)

    respx.post(LLM_API_URL, headers=HEADERS).mock(
        return_value=httpx.Response(200, json=MOCK_LLM_RESPONSE)
    )

    response = await get_llm_recommendation(weather_data, RequestTypeEnum.CURRENT)

    assert isinstance(response, str)
    assert response == "Wear a light jacket."


@pytest.mark.asyncio
@respx.mock
async def test_get_llm_recommendation_forecast():
    weather_data = ForecastWeatherResponse(**MOCK_FORECAST_WEATHER_RESPONSE)

    respx.post(LLM_API_URL, headers=HEADERS).mock(
        return_value=httpx.Response(200, json=MOCK_LLM_RESPONSE)
    )

    response = await get_llm_recommendation(weather_data, RequestTypeEnum.FORECAST)

    assert isinstance(response, str)
    assert response == "Wear a light jacket."


@pytest.mark.asyncio
@respx.mock
async def test_query_llm_success():
    prompt = "What should I wear today?"

    respx.post(LLM_API_URL, headers=HEADERS).mock(
        return_value=httpx.Response(200, json=MOCK_LLM_RESPONSE)
    )

    response = await query_llm(prompt, ModelTypeEnum.MISTRAL)

    assert isinstance(response, str)
    assert response == "Wear a light jacket."


@pytest.mark.asyncio
@respx.mock
async def test_query_llm_http_error():
    prompt = "What should I wear today?"

    respx.post(LLM_API_URL, headers=HEADERS).mock(
        return_value=httpx.Response(400, json=MOCK_INVALID_LLM_RESPONSE)
    )

    with pytest.raises(HTTPException) as exc_info:
        await query_llm(prompt, ModelTypeEnum.MISTRAL)

    assert exc_info.value.status_code == 400
    assert "Invalid request" in exc_info.value.detail


@pytest.mark.asyncio
@respx.mock
async def test_query_llm_request_error():
    prompt = "What should I wear today?"

    respx.post(LLM_API_URL, headers=HEADERS).mock(
        side_effect=httpx.RequestError("Connection Error")
    )

    with pytest.raises(HTTPException) as exc_info:
        await query_llm(prompt, ModelTypeEnum.MISTRAL)

    assert exc_info.value.status_code == 503
    assert "Service unavailable" in exc_info.value.detail


@pytest.mark.asyncio
@respx.mock
async def test_query_llm_unexpected_error():
    prompt = "What should I wear today?"

    respx.post(LLM_API_URL, headers=HEADERS).mock(
        side_effect=Exception("Unexpected Error")
    )

    with pytest.raises(HTTPException) as exc_info:
        await query_llm(prompt, ModelTypeEnum.MISTRAL)

    assert exc_info.value.status_code == 500
    assert "Unexpected Error" in exc_info.value.detail
