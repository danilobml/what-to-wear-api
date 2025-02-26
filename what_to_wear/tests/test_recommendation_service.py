import json
from http import HTTPStatus
from pathlib import Path

import httpx
import pytest
import respx
from fastapi import HTTPException

from what_to_wear.api.models.schemas.current_weather import CurrentWeatherResponse
from what_to_wear.api.models.schemas.forecast_weather import ForecastWeatherResponse
from what_to_wear.api.services.recommendation_service import get_llm_recommendation, query_llm
from what_to_wear.api.utils.constants import HEADERS, LLM_API_URL, ModelTypeEnum, RequestTypeEnum


def load_mock_data(filename: str):
    json_path = Path(__file__).parent / "mock_data" / filename
    with open(json_path, "r", encoding="utf-8") as file:
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
        return_value=httpx.Response(HTTPStatus.OK, json=MOCK_LLM_RESPONSE)
    )

    response = await get_llm_recommendation(weather_data, RequestTypeEnum.CURRENT)

    assert isinstance(response, str)
    assert response == "Wear a light jacket."


@pytest.mark.asyncio
@respx.mock
async def test_get_llm_recommendation_forecast():
    weather_data = ForecastWeatherResponse(**MOCK_FORECAST_WEATHER_RESPONSE)

    respx.post(LLM_API_URL, headers=HEADERS).mock(
        return_value=httpx.Response(HTTPStatus.OK, json=MOCK_LLM_RESPONSE)
    )

    response = await get_llm_recommendation(weather_data, RequestTypeEnum.FORECAST)

    assert isinstance(response, str)
    assert response == "Wear a light jacket."


@pytest.mark.asyncio
@respx.mock
async def test_query_llm_success():
    prompt = "What should I wear today?"

    respx.post(LLM_API_URL, headers=HEADERS).mock(
        return_value=httpx.Response(HTTPStatus.OK, json=MOCK_LLM_RESPONSE)
    )

    response = await query_llm(prompt, ModelTypeEnum.MISTRAL)

    assert isinstance(response, str)
    assert response == "Wear a light jacket."


@pytest.mark.asyncio
@respx.mock
async def test_query_llm_http_error():
    prompt = "What should I wear today?"

    respx.post(LLM_API_URL, headers=HEADERS).mock(
        return_value=httpx.Response(HTTPStatus.BAD_REQUEST, json=MOCK_INVALID_LLM_RESPONSE)
    )

    with pytest.raises(HTTPException) as exc_info:
        await query_llm(prompt, ModelTypeEnum.MISTRAL)

    assert exc_info.value.status_code == HTTPStatus.BAD_REQUEST
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

    assert exc_info.value.status_code == HTTPStatus.SERVICE_UNAVAILABLE
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

    assert exc_info.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert "Unexpected Error" in exc_info.value.detail
