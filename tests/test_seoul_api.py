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
    assert result.congestion == "약간 붐빔 (샘플)"
    assert result.weather == "18.5°C"
    second = api.get_data(Place("홍대입구역(2호선)"))
    assert second.congestion == "붐빔 (샘플)"
    assert second.weather == "16.3°C"


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


def test_api_error_returns_sample_data_without_printing_the_key(monkeypatch, capsys):
    import requests

    monkeypatch.setenv("SEOUL_API_KEY", "test-key")

    def fake_request(url, **kwargs):
        raise requests.HTTPError(f"Server error for url: {url}")

    monkeypatch.setattr("seoul_api.requests.get", fake_request)

    api = SeoulAPI()
    place = Place("홍대입구")

    result = api.get_data(place)

    assert isinstance(result, UrbanData)
    assert result.area_name == "홍대입구"
    assert result.congestion == "약간 붐빔 (샘플)"
    assert "test-key" not in capsys.readouterr().out


def test_invalid_api_status_returns_sample_data(monkeypatch, capsys):
    from unittest.mock import Mock

    response = Mock()
    monkeypatch.setattr("seoul_api.requests.get", lambda *args, **kwargs: response)
    api = SeoulAPI(api_key="test-key")

    for status in (None, [], {"RESULT.CODE": "ERROR", "RESULT.MESSAGE": "test-key"}):
        response.json.return_value = {"RESULT": status}
        assert api.get_data(Place("강남역")).congestion == "약간 붐빔 (샘플)"

    assert "test-key" not in capsys.readouterr().out


def test_live_response_uses_nested_population_timestamp_and_preserves_zero(monkeypatch):
    from unittest.mock import Mock

    response = Mock()
    response.json.return_value = {
        "RESULT": {"RESULT.CODE": "INFO-000"},
        "CITYDATA": {
            "LIVE_PPLTN_STTS": [{
                "AREA_CONGEST_LVL": " 여유 ",
                "AREA_PPLTN_MIN": "0",
                "AREA_PPLTN_MAX": "100",
                "PPLTN_TIME": "2026-11-22 09:00",
            }],
            "WEATHER_STTS": [{"TEMP": 0}],
        },
    }
    request = Mock(return_value=response)
    monkeypatch.setattr("seoul_api.requests.get", request)

    result = SeoulAPI(api_key=" test/key ").get_data(Place("강남역", "AREA_TEST"))

    assert request.call_args.kwargs["timeout"] == (3, 5)
    assert request.call_args.args[0].endswith("/test%2Fkey/json/citydata/1/5/AREA_TEST")
    assert result.area_name == "강남역"
    assert result.congestion == "여유"
    assert result.weather == "0°C"
    assert result.population == "50 (범위 중간값)"
    assert result.updated_at == "2026-11-22 09:00"

    response.json.return_value["CITYDATA"]["WEATHER_STTS"] = [{"TEMP": "nan"}]
    result = SeoulAPI(api_key="test-key").get_data(Place("강남역"))
    assert result.weather == "정보 없음"
    assert result.congestion == "여유"
