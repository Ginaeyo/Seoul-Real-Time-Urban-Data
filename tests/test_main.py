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
    def analyze_congestion(self, congestion):
        return f"분석: {congestion}"


class FakeDashboard:
    def __init__(self):
        self.shown = None

    def display(self, place, urban_data):
        self.shown = (place, urban_data)


@pytest.fixture
def app(monkeypatch):
    fakes = {
        "area_manager": ("AreaManager", FakeAreaManager),
        "location_selector": ("LocationSelector", FakeLocationSelector),
        "seoul_api": ("SeoulAPI", FakeSeoulAPI),
        "data_analyzer": ("DataAnalyzer", FakeDataAnalyzer),
        "dashboard": ("Dashboard", FakeDashboard),
    }
    for module_name, (class_name, fake_class) in fakes.items():
        fake_module = types.ModuleType(module_name)
        setattr(fake_module, class_name, fake_class)
        monkeypatch.setitem(sys.modules, module_name, fake_module)

    sys.modules.pop("main", None)
    main = importlib.import_module("main")
    yield main.MainApp()
    sys.modules.pop("main", None)


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
    data = types.SimpleNamespace(congestion="붐빔")
    app.location_selector.result = place
    app.api.result = data
    monkeypatch.setattr(
        sys.modules["main"], "plot_area_dashboard", lambda *args, **kwargs: "dashboard.png"
    )

    app.run()

    captured = capsys.readouterr()
    assert "분석: 붐빔" in captured.out


def test_compare_flow_creates_congestion_chart(app, capsys, monkeypatch, tmp_path):
    first = types.SimpleNamespace(area_name="강남역")
    second = types.SimpleNamespace(area_name="홍대입구역(2호선)")
    first_data = types.SimpleNamespace(congestion="여유", traffic="원활")
    second_data = types.SimpleNamespace(congestion="붐빔", traffic="정체")
    data_by_area = {
        first.area_name: first_data,
        second.area_name: second_data,
    }
    app.location_selector.select_comparison_areas = lambda _: (first, second)
    app.api.get_data = lambda area: data_by_area[area.area_name]
    app.analyzer.compare_congestion = lambda *args: "comparison summary"
    plot_calls = []
    monkeypatch.setattr(
        sys.modules["main"],
        "plot_congestion_comparison",
        lambda *args, **kwargs: plot_calls.append((args, kwargs)) or tmp_path / "comparison.png",
        raising=False,
    )

    app.compare_areas()

    assert plot_calls == [
        (("강남역", "여유", "홍대입구역(2호선)", "붐빔", None, None),
         {"first_traffic": "원활", "second_traffic": "정체",
          "first_population": None, "second_population": None,
          "first_environment": (None, None), "second_environment": (None, None)})
    ]
    assert "그래프 저장 위치" in capsys.readouterr().out


def test_menu_three_exits(app, capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "3")
    app.run()
    assert app.api.received is None
    assert "프로그램을 종료합니다." in capsys.readouterr().out


def test_mixed_sources_display_both_areas_without_ranking(app, capsys, monkeypatch):
    first = types.SimpleNamespace(area_name="강남역")
    second = types.SimpleNamespace(area_name="서울역")
    live = types.SimpleNamespace(congestion="여유")
    sample = types.SimpleNamespace(congestion="약간 붐빔 (샘플)")
    app.location_selector.select_comparison_areas = lambda _: (first, second)
    app.api.get_data = lambda area: live if area is first else sample
    monkeypatch.setattr(sys.modules["main"], "plot_congestion_comparison", lambda *args, **kwargs: "comparison.png")

    app.compare_areas()

    output = capsys.readouterr().out
    assert "첫 번째 지역 (실시간)" in output
    assert "두 번째 지역 (시연)" in output
    assert "혼잡도 순위는 비교하지 않습니다" in output
    assert "comparison.png" in output
