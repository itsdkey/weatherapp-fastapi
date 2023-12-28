from typing import Annotated

from fastapi import APIRouter, Depends

from app.config import Settings, get_settings
from opeanweather.adapters import OpenWeatherAdapter
from opeanweather.clients import WeatherDBClient
from opeanweather.enums import WeatherMeasurementName
from opeanweather.schemas import (
    WeatherMeasurement,
    WeatherMeasurementsRead,
    WeatherMeasurementsWrite,
)

opeanweather_router = APIRouter()


@opeanweather_router.get("")
def get_current_temperature_at_location(
    settings: Annotated[Settings, Depends(get_settings)],
    city: str,
    country_code: str,
) -> WeatherMeasurementsWrite | None:
    response = None
    if city and country_code:
        adapter = OpenWeatherAdapter(settings)
        measurement = adapter.get_weather_at_location(city, country_code)
        with WeatherDBClient(settings) as db:
            db.save_weather_data(measurement, tags={"location": city.lower()})
        response = measurement
    return response


@opeanweather_router.get("/history")
def get_historical_measurements_for_location(
    settings: Annotated[Settings, Depends(get_settings)],
    city: str,
) -> list[WeatherMeasurementsRead]:
    with WeatherDBClient(settings) as db:
        return db.get_weather_measurements(location=city)


@opeanweather_router.get("/history/{measurement_name}")
def get_one_historical_measurement_for_location(
    settings: Annotated[Settings, Depends(get_settings)],
    city: str,
    measurement_name: WeatherMeasurementName,
) -> list[WeatherMeasurement]:
    with WeatherDBClient(settings) as db:
        return db.get_one_measurement(location=city, measurement_name=measurement_name)
