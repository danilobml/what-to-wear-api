from typing import Optional

from pydantic import BaseModel, Field


class WeatherRequestParams(BaseModel):
    lat: float = Field(..., description="Latitude in decimal degrees, required.")
    lon: float = Field(..., description="Longitude in decimal degrees, required.")


class ForecastWeatherRequestParams(WeatherRequestParams):
    days: Optional[int] = Field(1, ge=1, le=10, description="Number of days for the forecast (1-10). Default is 1.")
