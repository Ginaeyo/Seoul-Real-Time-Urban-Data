import os
import sys

sys.path.insert(
    0,
    os.path.join(os.path.dirname(__file__), "..", "src")
)

from seoul_api import SeoulAPI
from place import Place
from urban_data import UrbanData


def test_api_without_key_returns_sample_data(monkeypatch):
    monkeypatch.delenv("SEOUL_API_KEY", raising=False)

    api = SeoulAPI(api_key=None)
    place = Place("강남역")

    result = api.get_data(place)

    assert isinstance(result, UrbanData)
    assert result.area_name == "강남역"
    assert result.congestion == "보통 (샘플)"


def test_api_success_returns_real_data(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "CITYDATA": {
                    "LIVE_PPLTN_STTS": [
                        {"AREA_CONGEST_LVL": "붐빔"}
                    ],
                    "WEATHER_STTS": [
                        {"TEMP": "20"}
                    ]
                }
            }

    monkeypatch.setenv("SEOUL_API_KEY", "test-key")
    monkeypatch.setattr(
        "seoul_api.requests.get",
        lambda *args, **kwargs: FakeResponse()
    )

    api = SeoulAPI()
    place = Place("강남역")

    result = api.get_data(place)

    assert isinstance(result, UrbanData)
    assert result.area_name == "강남역"
    assert result.congestion == "붐빔"
    assert result.weather == "20°C"


def test_api_error_returns_sample_data(monkeypatch):
    import requests

    monkeypatch.setenv("SEOUL_API_KEY", "test-key")

    def fake_request(*args, **kwargs):
        raise requests.RequestException("Connection error")

    monkeypatch.setattr("seoul_api.requests.get", fake_request)

    api = SeoulAPI()
    place = Place("홍대입구")

    result = api.get_data(place)

    assert isinstance(result, UrbanData)
    assert result.area_name == "홍대입구"
    assert result.congestion == "보통 (샘플)"