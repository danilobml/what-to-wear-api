from typing import Optional

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, model_validator


class WeatherRequestParams(BaseModel):
    lat: Optional[float] = Field(None, description="Latitude in decimal degrees.")
    lon: Optional[float] = Field(None, description="Longitude in decimal degrees.")
    city: Optional[str] = Field(None, description="City name.")

    @model_validator(mode="before")
    @classmethod
    def check_required_params(cls, values):
        lat, lon, city = values.get("lat"), values.get("lon"), values.get("city")

        if (lat is None or lon is None) and not city:
            raise RequestValidationError("Either 'city' or ('lat', 'lon') must be provided.")

        if city and lat is not None and lon is not None:
            raise RequestValidationError("Provide either 'city' or ('lat', 'lon'), but not all three.")

        return values


class ForecastWeatherRequestParams(WeatherRequestParams):
    days: Optional[int] = Field(1, ge=1, le=10, description="Number of days for the forecast (1-10). Default is 1.")
