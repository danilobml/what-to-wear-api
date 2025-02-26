from typing import Union

import httpx
from fastapi import HTTPException

from what_to_wear.api.models.schemas.current_weather import CurrentWeatherResponse
from what_to_wear.api.models.schemas.forecast_weather import ForecastWeatherResponse
from what_to_wear.api.utils.constants import (
    HEADERS,
    LLM_API_URL,
    MODEL_TYPE,
    ModelTypeEnum,
    RequestTypeEnum,
)
from what_to_wear.api.utils.llm_utils import get_content_from_llm_response, get_model_params
from what_to_wear.api.utils.utils import (
    generate_clothes_recommendation_prompt_current_weather,
    generate_clothes_recommendation_prompt_forecast,
)


async def get_llm_recommendation(
    weather_data: Union[CurrentWeatherResponse, ForecastWeatherResponse],
    type: RequestTypeEnum
) -> str:
    if type == RequestTypeEnum.CURRENT:
        weather_data: CurrentWeatherResponse
        prompt = generate_clothes_recommendation_prompt_current_weather(weather_data)
    else:
        weather_data: ForecastWeatherResponse
        prompt = generate_clothes_recommendation_prompt_forecast(weather_data)

    return await query_llm(prompt, MODEL_TYPE)


async def query_llm(prompt: str, model_type: ModelTypeEnum) -> str:
    data = {
        "model": f"{get_model_params(model_type)}",
        "messages": [{"role": "user", "content": prompt}]
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(LLM_API_URL, headers=HEADERS, json=data)
            response.raise_for_status()
            response_json = response.json()
            return get_content_from_llm_response(response_json, model_type)
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Service unavailable")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
