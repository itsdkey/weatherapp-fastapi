from datetime import datetime

from pydantic import BaseModel

WEATHER_MEASUREMENT_DOC_TYPE = "weather_measurement"


class WeatherMeasurementsWrite(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int


class WeatherMeasurementsRead(WeatherMeasurementsWrite):
    type: str = WEATHER_MEASUREMENT_DOC_TYPE
    time: datetime


class WeatherMeasurement(BaseModel):
    type: str
    value: float | int
    time: datetime
