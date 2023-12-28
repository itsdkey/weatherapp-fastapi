from datetime import datetime

import httpx
from influxdb_client import Point

from app.config import Settings
from db.clients import InfluxDBClient
from opeanweather.schemas import (
    WEATHER_MEASUREMENT_DOC_TYPE,
    WeatherMeasurement,
    WeatherMeasurementsRead,
    WeatherMeasurementsWrite,
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
        self, measurement: WeatherMeasurementsWrite, tags: dict = None
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

    def get_weather_measurements(self, location: str) -> list[WeatherMeasurementsRead]:
        bucket = "weatherapp"
        params = {
            "_bucket": bucket,
            "_location": location.lower(),
            "_measurement": WEATHER_MEASUREMENT_DOC_TYPE,
        }
        query = (
            "from(bucket: _bucket)"
            "|> range(start: -3h)"
            "|> filter(fn:(r) => r._measurement == _measurement)"
            "|> filter(fn:(r) => r.location == _location)"
            '|> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")'
            '|> sort(columns: ["_time"], desc: true)'
        )
        queryset = self._query(query=query, params=params)
        results = []
        for table in queryset:
            for record in table.records:
                measurement = record.values | {
                    "time": record.get_time(),
                    "type": WEATHER_MEASUREMENT_DOC_TYPE,
                }
                results.append(WeatherMeasurementsRead(**measurement))
        return results

    def get_one_measurement(
        self, location: str, measurement_name: str
    ) -> list[WeatherMeasurement]:
        bucket = "weatherapp"
        measurement_name = measurement_name.lower()
        params = {
            "_bucket": bucket,
            "_field": measurement_name,
            "_location": location.lower(),
            "_measurement": WEATHER_MEASUREMENT_DOC_TYPE,
        }
        query = (
            "from(bucket: _bucket)"
            "|> range(start: -3h)"
            "|> filter(fn:(r) => r._measurement == _measurement)"
            "|> filter(fn:(r) => r.location == _location)"
            "|> filter(fn:(r) => r._field == _field)"
            '|> sort(columns: ["_time"], desc: true)'
        )
        queryset = self._query(query=query, params=params)
        results = []
        for table in queryset:
            for record in table.records:
                measurement = {
                    "time": record.get_time(),
                    "type": f"{WEATHER_MEASUREMENT_DOC_TYPE}:{measurement_name}",
                    "value": record.get_value(),
                }
                results.append(WeatherMeasurement(**measurement))
        return results
