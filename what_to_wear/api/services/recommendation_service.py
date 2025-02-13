from typing import Union
from fastapi import HTTPException
import httpx

from what_to_wear.api.models.schemas.current_weather import CurrentWeatherResponse
from what_to_wear.api.models.schemas.forecast_weather import ForecastWeatherResponse
from what_to_wear.api.utils.utils import (
    generate_clothes_recommendation_prompt_current_weather,
    generate_clothes_recommendation_prompt_forecast,
    get_content_from_llm_response,
    get_model_url
)
from what_to_wear.api.utils.constants import LLM_API_URL, HEADERS, MODEL_TYPE, ModelTypeEnum, RequestTypeEnum


async def get_llm_recommendation(
        weather_data: Union[CurrentWeatherResponse | ForecastWeatherResponse],
        type: RequestTypeEnum
        ):
    if type == RequestTypeEnum.CURRENT:
        weather_data: CurrentWeatherResponse
        prompt = generate_clothes_recommendation_prompt_current_weather(weather_data)
    else:
        weather_data: ForecastWeatherResponse
        prompt = generate_clothes_recommendation_prompt_forecast(weather_data)
    llm_response = await query_llm(prompt, MODEL_TYPE)
    return llm_response


async def query_llm(prompt: str, model_type: ModelTypeEnum):

    data = {
        "model": f"{get_model_url(model_type)}",
        "messages": [{"role": "user", "content": prompt}]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(LLM_API_URL, headers=HEADERS, json=data)
        if response.status_code == 200:
            response_json = response.json()
            content = get_content_from_llm_response(response_json, model_type)
            return content
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
