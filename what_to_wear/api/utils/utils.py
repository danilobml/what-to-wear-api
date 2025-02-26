from what_to_wear.api.models.schemas.current_weather import CurrentWeatherResponse
from what_to_wear.api.models.schemas.forecast_weather import DayForecast, ForecastWeatherResponse


def generate_clothes_recommendation_prompt_current_weather(weather_data: CurrentWeatherResponse) -> str:
    """ Gets a llm prompt for one current weather clothes recommendation """
    return f"""
        Based on the following weather conditions, provide a direct clothing recommendation,
        without repeating the details:
        - Temperature: {weather_data.current.temp_c}°C
        - Feels Like: {weather_data.current.feelslike_c}°C
        - Pressure: {weather_data.current.pressure_mb} mbar
        - Humidity: {weather_data.current.humidity}%
        - Wind Speed: {weather_data.current.wind_kph} km/h
        - Precipitation: {weather_data.current.precip_mm} mm
        - Time of Day: {"Daytime" if weather_data.current.is_day else "Evening"}

    Only give the recommended clothing choices concisely.
    """


def generate_individual_forecast_prompt(daily_data: DayForecast) -> str:
    """ Gets a llm prompt for each day with forecasted weather """
    return f"""
        - Average Temperature: {daily_data.avgtemp_c}°C
        - Max Temperature: {daily_data.maxtemp_c}°C
        - Min Temperature: {daily_data.mintemp_c}°C
        - Average Humidity: {daily_data.avghumidity}%
        - Total Precipitation: {daily_data.totalprecip_mm} mm
        - Chance of rain: {daily_data.daily_chance_of_rain}
        - UV radiation levels: {daily_data.uv}
    """


def generate_clothes_recommendation_prompt_forecast(weather_data: ForecastWeatherResponse) -> str:
    """ Consolidates a llm prompt for all forecasted days to obtain clothes recommendation """
    final_prompt = """
            Based on the following weather conditions for each day, provide a direct clothing
            recommendation for each day, without repeating the details.
            Only give the recommended clothing choices concisely:
        """
    for day in weather_data.forecast.forecastday:
        day_prompt = generate_individual_forecast_prompt(day.day)
        final_prompt += f" .Day: {day.date}: {day_prompt}"
    return final_prompt
