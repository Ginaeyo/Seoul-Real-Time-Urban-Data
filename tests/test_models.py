import os
import sys

# tests/ 폴더에서 실행해도 src/ 안의 모듈을 import 할 수 있게 경로를 추가한다.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from place import Place
from urban_data import UrbanData


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


def test_urban_data_fields():
    """UrbanData 에 넣은 값이 그대로 저장되는지 확인한다."""
    data = UrbanData("강남역", "붐빔", "맑음")
    assert data.area_name == "강남역"
    assert data.congestion == "붐빔"
    assert data.weather == "맑음"


def test_urban_data_missing_values_are_none():
    """값을 주지 않은 필드가 None 이 되는지 확인한다."""
    data = UrbanData()
    assert data.area_name is None
    assert data.congestion is None
    assert data.weather is None
