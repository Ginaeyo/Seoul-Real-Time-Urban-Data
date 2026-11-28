"""API 또는 네트워크 없이 MainApp의 흐름을 확인합니다."""

import importlib
import os
import sys
import types

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


class FakeAreaManager:
    pass


class FakeLocationSelector:
    def __init__(self):
        self.result = None

    def select_location(self, area_manager):
        return self.result


class FakeSeoulAPI:
    def __init__(self):
        self.result = None
        self.received = None

    def get_data(self, area):
        self.received = area
        return self.result


class FakeDataAnalyzer:
    def calculate_population_midpoint(self, data):
        return None

    def analyze_congestion(self, congestion):
        return 4


from dashboard import Dashboard


class FakeDashboard(Dashboard):
    def __init__(self):
        self.shown = None

    def display(self, place, urban_data, *, midpoint=None):
        self.shown = (place, urban_data)


@pytest.fixture
def app():
    from main import MainApp
    from data_analyzer import DataAnalyzer
    return MainApp(FakeSeoulAPI(), area_manager=FakeAreaManager(),
                   location_selector=FakeLocationSelector(), analyzer=DataAnalyzer(),
                   dashboard=FakeDashboard())


def test_api_failure_is_reported_without_crashing(app, capsys, monkeypatch):
    inputs = iter(["1", "3"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    app.location_selector.result = "강남역"
    app.api.result = None

    app.run()

    captured = capsys.readouterr()
    assert "도시 데이터를 가져오지 못했습니다." in captured.out


def test_invalid_location_stops_before_api_call(app, capsys, monkeypatch):
    inputs = iter(["1", "3"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    app.location_selector.result = None

    app.run()

    captured = capsys.readouterr()
    assert "잘못된 입력입니다." in captured.out


def test_successful_flow_displays_data_and_analysis(app, capsys, monkeypatch):
    inputs = iter(["1", "3"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    place = types.SimpleNamespace(area_name="강남역")
    data = types.SimpleNamespace(congestion="붐빔", data_source="api")
    app.location_selector.result = place
    app.api.result = data
    monkeypatch.setattr(
        sys.modules["dashboard"], "plot_area_dashboard", lambda *args, **kwargs: "dashboard.png"
    )

    app.run()

    captured = capsys.readouterr()
    assert "현재 매우 혼잡합니다." in captured.out


def test_compare_flow_creates_congestion_chart(app, capsys, monkeypatch, tmp_path):
    first = types.SimpleNamespace(area_name="강남역")
    second = types.SimpleNamespace(area_name="홍대입구역(2호선)")
    first_data = types.SimpleNamespace(area_name="강남역", congestion="여유", traffic="원활", data_source="api", weather=10.0)
    second_data = types.SimpleNamespace(area_name="홍대입구역(2호선)", congestion="붐빔", traffic="정체", data_source="api", weather=20.0)
    data_by_area = {
        first.area_name: first_data,
        second.area_name: second_data,
    }
    app.location_selector.select_comparison_areas = lambda _: (first, second)
    app.api.get_data = lambda area: data_by_area[area.area_name]
    app.analyzer.compare_congestion = lambda *args: "second_more"
    plot_calls = []
    monkeypatch.setattr(
        sys.modules["dashboard"],
        "plot_congestion_comparison",
        lambda *args, **kwargs: plot_calls.append((args, kwargs)) or tmp_path / "comparison.png",
        raising=False,
    )

    app.compare_areas()

    assert plot_calls == [
        (("강남역", "여유", "홍대입구역(2호선)", "붐빔", 10.0, 20.0),
         {"first_data_source": "api", "second_data_source": "api", "average_temperature": 15.0, "first_traffic": "원활", "second_traffic": "정체",
          "first_population": None, "second_population": None,
          "first_environment": (None, None), "second_environment": (None, None)})
    ]
    output = capsys.readouterr().out
    assert "그래프 저장 위치" in output
    assert "홍대입구역(2호선)이(가) 강남역보다 혼잡합니다." in output


def test_menu_three_exits(app, capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "3")
    app.run()
    assert app.api.received is None
    assert "프로그램을 종료합니다." in capsys.readouterr().out


def test_mixed_sources_display_both_areas_without_ranking(app, capsys, monkeypatch):
    first = types.SimpleNamespace(area_name="강남역")
    second = types.SimpleNamespace(area_name="서울역")
    live = types.SimpleNamespace(congestion="여유 (샘플)", data_source="api", weather=10.0)
    sample = types.SimpleNamespace(congestion="약간 붐빔", data_source="sample", weather=20.0)
    app.location_selector.select_comparison_areas = lambda _: (first, second)
    app.api.get_data = lambda area: live if area is first else sample
    app.analyzer.compare_congestion = lambda *args: pytest.fail("혼합 출처는 비교하지 않아야 함")
    monkeypatch.setattr(sys.modules["dashboard"], "plot_congestion_comparison", lambda *args, **kwargs: "comparison.png")

    app.compare_areas()

    output = capsys.readouterr().out
    assert "첫 번째 지역 (실시간)" in output
    assert "두 번째 지역 (시연)" in output
    assert "혼잡도 순위는 비교하지 않습니다" in output
    assert "comparison.png" in output


def test_population_midpoint_is_forwarded_to_dashboard_and_chart(app, monkeypatch):
    from unittest.mock import Mock
    place = types.SimpleNamespace(area_name='강남역')
    data = types.SimpleNamespace(congestion='여유', population_min=20000, population_max=24000, weather=0.0)
    app.location_selector.result = place
    app.api.result = data
    app.analyzer.calculate_population_midpoint = Mock(return_value=22000)
    app.dashboard.display = Mock()
    app.dashboard.display_area_chart = Mock()
    app.show_area_info()
    app.analyzer.calculate_population_midpoint.assert_called_once_with(data)
    app.dashboard.display.assert_called_once_with(place, data, midpoint=22000)
    app.dashboard.display_area_chart.assert_called_once_with(place, data, midpoint=22000)
