from app.config import Settings
from opeanweather.clients import OpenWeatherClient
from opeanweather.schemas import WeatherMeasurement


class OpenWeatherAdapter:
    def __init__(self, settings: Settings) -> None:
        self.client = OpenWeatherClient(settings)

    def get_weather_at_location(
        self, city: str, country_code: str
    ) -> WeatherMeasurement:
        response = self.client.get_weather_at_location(city, country_code)
        measurement = WeatherMeasurement(**response)
        return measurement
