from typing import Any

import influxdb_client
from influxdb_client import WritePrecision
from influxdb_client.client.write.point import DEFAULT_WRITE_PRECISION, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from app.config import Settings


class InfluxDBClient:
    """A wrapper around the InfluxDB client."""

    def __init__(self, settings: Settings) -> None:
        self.domain = settings.OPENWEATHER_DOMAIN
        self.api_key = settings.OPENWEATHER_API_KEY
        self.client = influxdb_client.InfluxDBClient(
            url=settings.INFLUXDB_URL,
            token=settings.INFLUXDB_INIT_ADMIN_TOKEN,
            org=settings.INFLUXDB_INIT_ORG,
        )

    def _write_point(
        self,
        bucket: str,
        record: Point,
        write_precision: WritePrecision = DEFAULT_WRITE_PRECISION,
        **kwargs
    ) -> Any:
        write_api = self.client.write_api(write_options=SYNCHRONOUS)
        return write_api.write(
            bucket=bucket, record=record, write_precision=write_precision, **kwargs
        )
