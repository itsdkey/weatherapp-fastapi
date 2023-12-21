from fastapi.testclient import TestClient
from pytest_httpx import HTTPXMock

from app.config import Settings, get_settings
from app.main import app

client = TestClient(app)


def get_settings_override() -> Settings:
    return Settings(
        OPENWEATHER_API_KEY="test1234", OPENWEATHER_DOMAIN="https://example.org"
    )


app.dependency_overrides[get_settings] = get_settings_override


def test_read_root_returns_hello_world():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_weather_returns_weather_from_third_party(httpx_mock: HTTPXMock):
    settings = get_settings_override()
    expected_response = {
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
            f"?q=Białystok,PL&appid={settings.OPENWEATHER_API_KEY}"
        ),
        method="GET",
        json=expected_response,
    )

    response = client.get(
        "/weather",
        params={"city": "Białystok", "country_code": "PL"},
    )

    assert response.status_code == 200
    assert response.json() == expected_response
