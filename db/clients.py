from typing import Annotated, Any, Type

import influxdb_client
from fastapi import Depends
from influxdb_client import WritePrecision
from influxdb_client.client.flux_table import TableList
from influxdb_client.client.write.point import DEFAULT_WRITE_PRECISION, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from app.config import Settings, get_settings


class InfluxDBClient:
    """A wrapper around the InfluxDB client."""

    def __init__(self, settings: Annotated[Settings, Depends(get_settings)]) -> None:
        self.client = influxdb_client.InfluxDBClient(
            url=settings.INFLUXDB_URL,
            token=settings.INFLUXDB_TOKEN,
            org=settings.INFLUXDB_ORG,
        )

    def __enter__(self) -> "InfluxDBClient":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    def close(self) -> None:
        self.client.close()

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

    def _query(self, query: str, params: dict = None) -> TableList:
        query_api = self.client.query_api()
        return query_api.query(query=query, params=params)


def get_db(
    db_client: Type[InfluxDBClient],
    settings: Annotated[Settings, Depends(get_settings)],
) -> Any:
    return db_client(settings)
