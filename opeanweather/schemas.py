from pydantic import BaseModel


class WeatherMeasurement(BaseModel):
    base: str
    clouds: dict
    cod: int
    coord: dict
    dt: int
    id: int
    main: dict
    name: str
    sys: dict
    timezone: int
    visibility: int
    weather: list
    wind: dict
