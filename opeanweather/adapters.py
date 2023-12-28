from app.config import Settings
from opeanweather.clients import OpenWeatherClient
from opeanweather.schemas import WeatherMeasurementsWrite


class OpenWeatherAdapter:
    def __init__(self, settings: Settings) -> None:
        self.client = OpenWeatherClient(settings)

    def get_weather_at_location(
        self, city: str, country_code: str
    ) -> WeatherMeasurementsWrite:
        response = self.client.get_weather_at_location(city, country_code)
        measurement = WeatherMeasurementsWrite(**response["main"])
        return measurement
