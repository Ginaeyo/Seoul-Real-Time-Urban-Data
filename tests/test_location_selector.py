
import os
import sys

sys.path.insert(
    0,
    os.path.join(os.path.dirname(__file__), "..", "src")
)

from area_manager import AreaManager
from location_selector import LocationSelector
from place import Place


def test_select_location_returns_place(monkeypatch):
    selector = LocationSelector()
    manager = AreaManager()

    inputs = iter(["", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = selector.select_location(manager)

    assert isinstance(result, Place)
    assert result.area_name == "강남역"


def test_select_location_invalid_number(monkeypatch):
    selector = LocationSelector()
    manager = AreaManager()

    inputs = iter(["", "99"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    assert selector.select_location(manager) is None


def test_select_location_non_numeric(monkeypatch):
    selector = LocationSelector()
    manager = AreaManager()

    monkeypatch.setattr("builtins.input", lambda _: "hello")

    assert selector.select_location(manager) is None
def test_select_location_by_search(monkeypatch):
    selector = LocationSelector()
    manager = AreaManager()

    inputs = iter(["강남", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = selector.select_location(manager)

    assert isinstance(result, Place)
    assert result.area_name == "강남역"


def test_select_comparison_areas(monkeypatch):
    selector = LocationSelector()
    manager = AreaManager()

    inputs = iter(["강남", "1", "홍대", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    first, second = selector.select_comparison_areas(manager)

    assert first.area_name == "강남역"
    assert second.area_name == "홍대입구"