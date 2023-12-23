from datetime import datetime

from pydantic import BaseModel

WEATHER_MEASUREMENT_DOC_TYPE = "weather_measurement"


class WeatherMeasurement(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int


class Temperature(BaseModel):
    type: str = "weather_measurement:temperature"
    temp: float
    time: datetime
