import os
import sys

sys.path.insert(
    0,
    os.path.join(os.path.dirname(__file__), "..", "src")
)

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
    assert manager.get_area(6) is None


def test_area_codes_are_not_invented():
    manager = AreaManager()

    for area in manager.areas:
        assert area.area_code is None