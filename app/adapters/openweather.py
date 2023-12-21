from app.clients.openweather import OpenWeatherClient
from app.config import Settings


class OpenWeatherAdapter:
    def __init__(self, settings: Settings) -> None:
        self.client = OpenWeatherClient(settings)

    def get_weather_at_location(self, city: str, country_code: str) -> dict:
        response = self.client.get_weather_at_location(city, country_code)
        return response
