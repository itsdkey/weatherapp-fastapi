import httpx

from app.config import Settings


class OpenWeatherClient:
    def __init__(self, settings: Settings) -> None:
        self.domain = settings.OPENWEATHER_DOMAIN
        self.api_key = settings.OPENWEATHER_API_KEY

    def _build_uri(self, path: str) -> str:
        return f"{self.domain}{path}"

    def _add_api_key(self, params: dict) -> dict:
        return params | {"appid": self.api_key}

    def get(self, resource: str, **kwargs):
        if params := kwargs.get("params"):
            params = self._add_api_key(params)
            kwargs["params"] = params

        uri = self._build_uri(resource)
        response = httpx.get(uri, **kwargs)
        return response.json()

    def get_weather_at_location(self, city: str, country_code: str):
        resource = "/data/2.5/weather"
        params = {"q": ",".join([city, country_code.upper()])}
        return self.get(resource, params=params)
