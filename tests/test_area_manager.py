import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from area_manager import AreaManager
from place import Place


def test_get_area_returns_place():
    manager = AreaManager()
    area = manager.get_area(1)
    assert isinstance(area, Place)
    assert area.area_name == "강남역"


def test_get_area_invalid_index():
    manager = AreaManager()
    assert manager.get_area(0) is None
    assert manager.get_area(len(manager.get_areas()) + 1) is None


def test_area_codes_are_not_invented():
    manager = AreaManager()
    for area in manager.areas:
        assert area.area_code is None


def test_get_areas_returns_all_places():
    manager = AreaManager()
    result = manager.get_areas()
    assert len(result) == 121
    assert len({area.area_name for area in result}) == 121
    assert all(isinstance(area, Place) for area in result)


def test_search_areas_by_name():
    manager = AreaManager()
    result = manager.search_areas("강남")
    assert {area.area_name for area in result} == {"강남역", "강남 MICE 관광특구"}
    assert result[0].area_name == "강남역"


def test_get_area_by_name():
    manager = AreaManager()
    result = manager.get_area("홍대입구역(2호선)")
    assert isinstance(result, Place)
    assert result.area_name == "홍대입구역(2호선)"


def test_wangsimni_uses_official_area_name():
    manager = AreaManager()
    area = manager.get_area("왕십리역")
    assert isinstance(area, Place)
    assert area.area_name == "왕십리역"


def test_csv_loads_from_other_working_directory(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    manager = AreaManager()
    assert len(manager.get_areas()) == 121
    assert manager.get_area("숭례문").area_name == "숭례문"
