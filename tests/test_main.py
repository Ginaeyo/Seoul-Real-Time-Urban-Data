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

    place = "강남역"
    data = types.SimpleNamespace(congestion="붐빔")
    app.location_selector.result = place
    app.api.result = data

    app.run()

    captured = capsys.readouterr()
    assert "분석: 붐빔" in captured.out
