from what_to_wear.api.models.current_weather import WeatherResponse


def generate_clothes_recommendation_prompt(weather_data: WeatherResponse) -> str:
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
