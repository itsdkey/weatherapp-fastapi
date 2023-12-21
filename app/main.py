from typing import Annotated

from fastapi import Depends, FastAPI

from app.adapters.openweather import OpenWeatherAdapter
from app.config import Settings, get_settings

app = FastAPI()


@app.get("/")
def read_root() -> dict:
    return {"Hello": "World"}


@app.get("/weather")
def read_weather(
    settings: Annotated[Settings, Depends(get_settings)],
    city: str | None = None,
    country_code: str | None = None,
) -> dict:
    response = {}
    if city and country_code:
        adapter = OpenWeatherAdapter(settings)
        response = adapter.get_weather_at_location(city, country_code)
    return response
