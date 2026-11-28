import os
import sys

sys.path.insert(
    0,
    os.path.join(os.path.dirname(__file__), "..", "src")
)

from seoul_api import SeoulAPI
from sample_data_provider import SampleDataProvider
from place import Place
from urban_data import UrbanData


def test_api_without_key_returns_sample_data(monkeypatch):
    monkeypatch.delenv("SEOUL_API_KEY", raising=False)

    api = SeoulAPI(api_key=None, fallback_provider=SampleDataProvider())
    place = Place("강남역")

    result = api.get_data(place)

    assert isinstance(result, UrbanData)
    assert result.area_name == "강남역"
    assert result.congestion == "약간 붐빔"
    assert result.weather == 18.5
    assert result.traffic == "서행"
    assert result.traffic_sample is True
    second = api.get_data(Place("홍대입구역(2호선)"))
    assert second.congestion == "붐빔"
    assert second.weather == 16.3


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
                    "ROAD_TRAFFIC_STTS": {
                        "AVG_ROAD_DATA": {"ROAD_TRAFFIC_IDX": "소통원활"},
                        "ROAD_TRAFFIC_STTS": [{"IDX": "정체"}],
                    },
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

    api = SeoulAPI(fallback_provider=SampleDataProvider())
    place = Place("강남역")

    result = api.get_data(place)

    assert isinstance(result, UrbanData)
    assert result.area_name == "강남역"
    assert result.congestion == "붐빔"
    assert result.weather == 20.0
    assert result.traffic == "원활"
    assert result.traffic_sample is False


def test_api_error_returns_sample_data_without_printing_the_key(monkeypatch, capsys):
    import requests

    monkeypatch.setenv("SEOUL_API_KEY", "test-key")

    def fake_request(url, **kwargs):
        raise requests.HTTPError(f"Server error for url: {url}")

    monkeypatch.setattr("seoul_api.requests.get", fake_request)

    api = SeoulAPI(fallback_provider=SampleDataProvider())
    place = Place("홍대입구")

    result = api.get_data(place)

    assert isinstance(result, UrbanData)
    assert result.area_name == "홍대입구"
    assert result.congestion == "보통"
    assert "test-key" not in capsys.readouterr().out


def test_invalid_api_status_returns_sample_data(monkeypatch, capsys):
    from unittest.mock import Mock

    response = Mock()
    monkeypatch.setattr("seoul_api.requests.get", lambda *args, **kwargs: response)
    api = SeoulAPI(api_key="test-key", fallback_provider=SampleDataProvider())

    for status in (None, [], {"RESULT.CODE": "ERROR", "RESULT.MESSAGE": "test-key"}):
        response.json.return_value = {"RESULT": status}
        assert api.get_data(Place("강남역")).congestion == "약간 붐빔"

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

    result = SeoulAPI(api_key=" test/key ", fallback_provider=SampleDataProvider()).get_data(Place("강남역", "AREA_TEST"))

    assert request.call_args.kwargs["timeout"] == (3, 5)
    assert request.call_args.args[0].endswith("/test%2Fkey/json/citydata/1/5/AREA_TEST")
    assert result.area_name == "강남역"
    assert result.congestion == "여유"
    assert result.weather == 0.0
    assert result.population is None
    assert (result.population_min, result.population_max) == (0, 100)
    assert result.updated_at == "2026-11-22 09:00"

    response.json.return_value["CITYDATA"]["WEATHER_STTS"] = [{"TEMP": "nan"}]
    result = SeoulAPI(api_key="test-key", fallback_provider=SampleDataProvider()).get_data(Place("강남역"))
    assert result.weather is None
    assert result.congestion == "여유"


def test_injected_fallback_used_without_key_and_on_request_failure(monkeypatch):
    from data_provider import DataProvider
    import requests

    class CustomFallback(DataProvider):
        def __init__(self):
            self.calls = []

        def get_data(self, place):
            self.calls.append(place)
            assert isinstance(place, Place)
            return UrbanData(area_name=place.area_name, congestion="여유", weather=10.0, data_source="sample")

    monkeypatch.delenv("SEOUL_API_KEY", raising=False)
    fallback = CustomFallback()
    api = SeoulAPI(fallback_provider=fallback)
    assert api.get_data(Place("강남역", "TEST001")).congestion == "여유"
    api.api_key = "test-key"
    def fail(*args, **kwargs):
        raise requests.ConnectionError("offline")
    monkeypatch.setattr("seoul_api.requests.get", fail)
    assert api.get_data(Place("서울역")).data_source == "sample"
    assert [(p.area_name, p.area_code) for p in fallback.calls] == [("강남역", "TEST001"), ("서울역", None)]


def test_fallback_is_silent_and_dashboard_explains_reason(monkeypatch, capsys):
    from dashboard import Dashboard
    monkeypatch.delenv('SEOUL_API_KEY', raising=False)
    place = Place('강남역')
    data = SeoulAPI(fallback_provider=SampleDataProvider()).get_data(place)
    assert data.fallback_reason == 'missing_api_key'
    assert capsys.readouterr().out == ''
    Dashboard().display(place, data)
    output = capsys.readouterr().out
    assert 'API 키가 없어 샘플 모드' in output
    assert '18.5°C' in output
    assert '시연 데이터' in output
