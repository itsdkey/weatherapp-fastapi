from datetime import datetime
from unittest.mock import ANY

from dateutil.tz import tzlocal
from fastapi.testclient import TestClient
from freezegun import freeze_time
from pytest import fixture
from pytest_httpx import HTTPXMock

from app.config import Settings, get_settings
from app.main import app
from opeanweather.clients import WeatherDBClient
from opeanweather.schemas import (
    WEATHER_MEASUREMENT_DOC_TYPE,
    Temperature,
    WeatherMeasurement,
)

client = TestClient(app)


def get_settings_override() -> Settings:
    return Settings(
        OPENWEATHER_API_KEY="test1234", OPENWEATHER_DOMAIN="https://example.org"
    )


app.dependency_overrides[get_settings] = get_settings_override


@fixture(autouse=True)
def run_around_tests():
    settings = get_settings_override()
    db = WeatherDBClient(settings)
    delete_api = db.client.delete_api()

    yield

    delete_api.delete(
        start="1970-01-01T00:00:00Z",
        stop=datetime.now(),
        predicate=f'_measurement="{WEATHER_MEASUREMENT_DOC_TYPE}"',
        bucket="weatherapp",
    )


def test_read_root_returns_hello_world():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_weather_returns_weather_from_third_party(httpx_mock: HTTPXMock):
    settings = get_settings_override()
    openweather_response = {
        "coord": {"lon": 23.15, "lat": 53.1333},
        "weather": [
            {
                "id": 804,
                "main": "Clouds",
                "description": "overcast clouds",
                "icon": "04d",
            }
        ],
        "base": "stations",
        "main": {
            "temp": 273.91,
            "feels_like": 271.3,
            "temp_min": 272.6,
            "temp_max": 274.61,
            "pressure": 998,
            "humidity": 93,
        },
        "visibility": 10000,
        "wind": {"speed": 2.24, "deg": 185, "gust": 4.47},
        "clouds": {"all": 100},
        "dt": 1703142429,
        "sys": {
            "type": 2,
            "id": 2077278,
            "country": "PL",
            "sunrise": 1703140750,
            "sunset": 1703167877,
        },
        "timezone": 3600,
        "id": 776069,
        "name": "Białystok",
        "cod": 200,
    }
    httpx_mock.add_response(
        url=(
            f"{settings.OPENWEATHER_DOMAIN}/data/2.5/weather"
            f"?q=Białystok,PL&units=metric"
            f"&appid={settings.OPENWEATHER_API_KEY}"
        ),
        method="GET",
        json=openweather_response,
    )
    expected_response = openweather_response["main"]

    response = client.get(
        "/weather",
        params={"city": "Białystok", "country_code": "PL"},
    )

    assert response.status_code == 200
    assert response.json() == expected_response


def test_weather_returns_error_when_country_code_missing():
    expected_response = {
        "detail": [
            {
                "input": None,
                "loc": ["query", "country_code"],
                "msg": "Field required",
                "type": "missing",
                "url": "https://errors.pydantic.dev/2.5/v/missing",
            },
        ],
    }

    response = client.get(
        "/weather",
        params={"city": "Białystok"},
    )

    assert response.status_code == 422
    assert response.json() == expected_response


def test_weather_returns_error_when_city_missing():
    expected_response = {
        "detail": [
            {
                "input": None,
                "loc": ["query", "city"],
                "msg": "Field required",
                "type": "missing",
                "url": "https://errors.pydantic.dev/2.5/v/missing",
            }
        ],
    }

    response = client.get(
        "/weather",
        params={"country_code": "PL"},
    )

    assert response.status_code == 422
    assert response.json() == expected_response


def test_weather_returns_error_when_both_params_missing():
    expected_response = {
        "detail": [
            {
                "input": None,
                "loc": ["query", "city"],
                "msg": "Field required",
                "type": "missing",
                "url": "https://errors.pydantic.dev/2.5/v/missing",
            },
            {
                "input": None,
                "loc": ["query", "country_code"],
                "msg": "Field required",
                "type": "missing",
                "url": "https://errors.pydantic.dev/2.5/v/missing",
            },
        ],
    }

    response = client.get("/weather")

    assert response.status_code == 422
    assert response.json() == expected_response


def test_weather_from_third_party_is_saved_in_db(httpx_mock: HTTPXMock):
    settings = get_settings_override()
    city = "Białystok"
    openweather_response = {
        "coord": {"lon": 23.15, "lat": 53.1333},
        "weather": [
            {
                "id": 804,
                "main": "Clouds",
                "description": "overcast clouds",
                "icon": "04d",
            }
        ],
        "base": "stations",
        "main": {
            "temp": 273.91,
            "feels_like": 271.3,
            "temp_min": 272.6,
            "temp_max": 274.61,
            "pressure": 998,
            "humidity": 93,
        },
        "visibility": 10000,
        "wind": {"speed": 2.24, "deg": 185, "gust": 4.47},
        "clouds": {"all": 100},
        "dt": 1703142429,
        "sys": {
            "type": 2,
            "id": 2077278,
            "country": "PL",
            "sunrise": 1703140750,
            "sunset": 1703167877,
        },
        "timezone": 3600,
        "id": 776069,
        "name": "Białystok",
        "cod": 200,
    }
    httpx_mock.add_response(
        url=(
            f"{settings.OPENWEATHER_DOMAIN}/data/2.5/weather"
            f"?q={city},PL&units=metric"
            f"&appid={settings.OPENWEATHER_API_KEY}"
        ),
        method="GET",
        json=openweather_response,
    )
    frozen_time = datetime.now(tz=tzlocal())
    expected_response = [
        Temperature(
            type="weather_measurement:temperature",
            temp=openweather_response["main"]["temp"],
            time=frozen_time,
        ),
    ]

    with freeze_time(frozen_time):
        client.get(
            "/weather",
            params={"city": "Białystok", "country_code": "PL"},
        )

    with WeatherDBClient(settings) as db:
        response = db.get_weather_measurements(location=city)
    assert response == expected_response


def test_history_returns_weather_from_the_past():
    settings = get_settings_override()
    city = "Białystok"
    data = {
        "temp": 273.91,
        "feels_like": 271.3,
        "temp_min": 272.6,
        "temp_max": 274.61,
        "pressure": 998,
        "humidity": 93,
    }
    with WeatherDBClient(settings) as db:
        db.save_weather_data(WeatherMeasurement(**data), tags={"location": city})
    expected_response = [
        {
            "temp": data["temp"],
            "time": ANY,
            "type": f"{WEATHER_MEASUREMENT_DOC_TYPE}:temperature",
        },
    ]

    response = client.get("/weather/history", params={"city": city})

    assert response.status_code == 200
    assert response.json() == expected_response
