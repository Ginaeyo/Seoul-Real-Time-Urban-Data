
import os
import sys

sys.path.insert(
    0,
    os.path.join(os.path.dirname(__file__), "..", "src")
)

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
