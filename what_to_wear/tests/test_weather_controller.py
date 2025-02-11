import json
import os
from http import HTTPStatus

import pytest
from dotenv import load_dotenv
from httpx import AsyncClient


load_dotenv()

weather_api_base_url = os.getenv("WEATHER_API_BASE_URL")
weather_api_key = os.getenv("WEATHER_API_KEY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(BASE_DIR, "mock_data",
                         "mock_current_weather_data.json")

with open(json_path, encoding="utf-8") as f:
    mock_current_weather_data = json.load(f)


@pytest.mark.asyncio
async def test_get_current_weather(httpx_mock):
    httpx_mock.add_response(
        method="GET",
        url=f"{weather_api_base_url}/current.json/?key={weather_api_key}&q=-23.538497,-46.683642",
        json=mock_current_weather_data,
        status_code=HTTPStatus.OK,
    )

    async with AsyncClient(base_url=weather_api_base_url) as client:
        response = await client.get("/weather/current/-23.538497/-46.683642")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == mock_current_weather_data
