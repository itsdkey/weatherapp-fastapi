from typing import Annotated

from fastapi import APIRouter, Depends

from app.config import Settings, get_settings
from opeanweather.adapters import OpenWeatherAdapter

opeanweather_router = APIRouter()


@opeanweather_router.get("/")
def read_weather(
    settings: Annotated[Settings, Depends(get_settings)],
    city: str,
    country_code: str,
) -> dict:
    response = {}
    if city and country_code:
        adapter = OpenWeatherAdapter(settings)
        measurement = adapter.get_weather_at_location(city, country_code)
        response = measurement.model_dump()
    return response
