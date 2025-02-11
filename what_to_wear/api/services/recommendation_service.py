from fastapi import HTTPException
import httpx

from what_to_wear.api.models.current_weather import WeatherResponse
from what_to_wear.utils.utils import generate_clothes_recommendation_prompt
from what_to_wear.utils.constants import LLM_API_URL, HEADERS


async def get_llm_recommendation(weather_data: WeatherResponse):
    prompt = generate_clothes_recommendation_prompt(weather_data)
    print("get_llm_recommendation: ", prompt)
    llm_response = await query_llm(prompt)
    return llm_response


async def query_llm(prompt: str):
    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(LLM_API_URL, headers=HEADERS, json=data)
        if response.status_code == 200:
            response_json = response.json()
            content = response_json["choices"][0]["message"]["content"]
            return content
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
