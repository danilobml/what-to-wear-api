from typing import Optional
from pydantic import BaseModel, Field, model_validator


class WeatherRequestParams(BaseModel):
    lat: Optional[float] = Field(None, description="Latitude in decimal degrees.")
    lon: Optional[float] = Field(None, description="Longitude in decimal degrees.")
    city: Optional[str] = Field(None, description="City name.")

    @model_validator(mode="before")
    @classmethod
    def check_required_params(cls, values):
        if not values.get("lat") or not values.get("lon"):
            if not values.get("city"):
                raise ValueError("Either 'city' or ('lat', 'lon') must be provided.")
        return values


class ForecastWeatherRequestParams(WeatherRequestParams):
    days: Optional[int] = Field(1, ge=1, le=10, description="Number of days for the forecast (1-10). Default is 1.")
