from datetime import datetime

import httpx
from influxdb_client import Point

from app.config import Settings
from db.clients import InfluxDBClient
from opeanweather.schemas import (
    WEATHER_MEASUREMENT_DOC_TYPE,
    Temperature,
    WeatherMeasurement,
)


class OpenWeatherClient:
    def __init__(self, settings: Settings) -> None:
        self.domain = settings.OPENWEATHER_DOMAIN
        self.api_key = settings.OPENWEATHER_API_KEY

    def _build_uri(self, path: str) -> str:
        return f"{self.domain}{path}"

    def _add_api_key(self, params: dict) -> dict:
        return params | {"appid": self.api_key}

    def get(self, resource: str, **kwargs) -> dict:
        if params := kwargs.get("params"):
            params = self._add_api_key(params)
            kwargs["params"] = params

        uri = self._build_uri(resource)
        response = httpx.get(uri, **kwargs)
        return response.json()

    def get_weather_at_location(self, city: str, country_code: str) -> dict:
        resource = "/data/2.5/weather"
        params = {
            "q": ",".join([city, country_code.upper()]),
            "units": "metric",
        }
        return self.get(resource, params=params)


class WeatherDBClient(InfluxDBClient):
    def save_weather_data(
        self, measurement: WeatherMeasurement, tags: dict = None
    ) -> None:
        bucket = "weatherapp"

        measurement = {
            "measurement": WEATHER_MEASUREMENT_DOC_TYPE,
            "fields": measurement.model_dump(),
            "time": datetime.now(),
        }
        if tags:
            measurement |= {"tags": tags}

        point = Point.from_dict(measurement)

        self._write_point(bucket=bucket, record=point)

    def get_weather_measurements(self, location: str) -> list[Temperature]:
        bucket = "weatherapp"
        params = {"_location": location}
        query = (
            f'from(bucket:"{bucket}")'
            f"|> range(start: -3h)"
            f'|> filter(fn:(r) => r._measurement == "{WEATHER_MEASUREMENT_DOC_TYPE}")'
            f"|> filter(fn:(r) => r.location == _location)"
            f'|> filter(fn:(r) => r._field == "temp")'
            f'|> sort(columns: ["_time"], desc: true)'
        )
        result = self._query(query=query, params=params)
        results = []
        for table in result:
            for record in table.records:
                temperature = {
                    record.get_field(): record.get_value(),
                    "time": record.get_time(),
                }
                results.append(Temperature(**temperature))
        return results
