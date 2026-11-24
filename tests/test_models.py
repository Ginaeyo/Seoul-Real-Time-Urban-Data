
import os
import sys

sys.path.insert(
    0,
    os.path.join(os.path.dirname(__file__), "..", "src")
)

from place import Place
from urban_data import UrbanData


def test_urban_data_stores_values():
    data = UrbanData("Gangnam", "Busy", "Sunny")

    assert data.area_name == "Gangnam"
    assert data.congestion == "Busy"
    assert data.weather == "Sunny"


def test_urban_data_default_values():
    data = UrbanData()

    assert data.area_name is None
    assert data.congestion is None
    assert data.weather is None


def test_urban_data_partial_values():
    data = UrbanData("Hongdae", congestion="Normal")

    assert data.area_name == "Hongdae"
    assert data.congestion == "Normal"
    assert data.weather is None


def test_place_fields():
    """Place 에 넣은 지역명과 코드가 그대로 저장되는지 확인한다."""
    place = Place("강남역", "TEST001")
    assert place.area_name == "강남역"
    assert place.area_code == "TEST001"


def test_place_get_info():
    """get_info() 가 항상 name, code 키를 가진 딕셔너리를 반환하는지 확인한다."""
    place = Place("강남역", "TEST001")
    assert place.get_info() == {"name": "강남역", "code": "TEST001"}


def test_place_str():
    """str(place) 가 '지역명 (코드)' 형식인지 확인한다."""
    assert str(Place("강남역", "TEST001")) == "강남역 (TEST001)"
