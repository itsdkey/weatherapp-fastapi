from typing import Annotated

from fastapi import APIRouter, Depends

from app.config import Settings, get_settings
from opeanweather.adapters import OpenWeatherAdapter
from opeanweather.clients import WeatherDBClient
from opeanweather.schemas import Temperature, WeatherMeasurement

opeanweather_router = APIRouter()


@opeanweather_router.get("/")
def get_current_temperature_at_location(
    # db: Annotated[WeatherDBClient, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)],
    city: str,
    country_code: str,
) -> WeatherMeasurement | None:
    response = None
    if city and country_code:
        adapter = OpenWeatherAdapter(settings)
        measurement = adapter.get_weather_at_location(city, country_code)
        db = WeatherDBClient(settings)
        db.save_weather_data(measurement, tags={"location": city})
        response = measurement
    return response


@opeanweather_router.get("/history")
def get_temperature_history_for_location(
    settings: Annotated[Settings, Depends(get_settings)],
    city: str,
) -> list[Temperature]:
    with WeatherDBClient(settings) as db:
        return db.get_weather_measurements(location=city)
