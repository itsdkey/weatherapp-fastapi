from enum import Enum


class WeatherMeasurementName(str, Enum):
    TEMPARATURE = "temp"
    FEELS_LIKE = "feels_like"
    TEMPERATURE_MIN = "temp_min"
    TEMPERATURE_MAX = "temp_max"
    PRESSURE = "pressure"
    HUMIDITY = "humidity"

    def __str__(self) -> str:
        return self.value
