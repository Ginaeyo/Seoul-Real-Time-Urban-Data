import os
import sys

sys.path.insert(
    0,
    os.path.join(os.path.dirname(__file__), "..", "src")
)

from data_analyzer import DataAnalyzer
from congestion_levels import FIRST_MORE, SECOND_MORE, EQUAL, UNKNOWN


def test_compare_different_congestion():
    analyzer = DataAnalyzer()

    result = analyzer.compare_congestion(
        "강남역", "붐빔",
        "홍대입구", "보통"
    )

    assert result == FIRST_MORE


def test_compare_same_congestion():
    analyzer = DataAnalyzer()

    result = analyzer.compare_congestion(
        "강남역", "보통",
        "홍대입구", "보통"
    )

    assert result == EQUAL


def test_compare_unknown_congestion():
    analyzer = DataAnalyzer()

    result = analyzer.compare_congestion(
        "강남역", "정보 없음",
        "홍대입구", "보통"
    )

    assert result == UNKNOWN

def test_analysis_levels_and_missing():
    analyzer = DataAnalyzer()
    for label, level in [("여유", 1), ("보통", 2), ("약간 붐빔 (샘플)", 3), ("붐빔", 4), (None, None), ("정보 없음", None), (42, None)]:
        assert analyzer.analyze_congestion(label) == level


def test_second_area_more_congested():
    assert DataAnalyzer().compare_congestion("A", "여유", "B", "붐빔") == SECOND_MORE


def test_shared_chart_and_analysis_levels():
    from congestion_chart import _normalize, LEVELS as chart_levels
    from congestion_levels import LEVELS
    assert chart_levels is LEVELS
    for label, level in LEVELS.items():
        assert _normalize(label + " (샘플)")[0] == DataAnalyzer().analyze_congestion(label) == level


def test_population_midpoint_and_missing_values():
    from urban_data import UrbanData
    analyzer = DataAnalyzer()
    for low, high, expected in [(20000, 24000, 22000), (0, 0, 0), (1, 2, 1), (None, 100, None), (20, 10, None), (-1, 10, None)]:
        assert analyzer.calculate_population_midpoint(UrbanData(population_min=low, population_max=high)) == expected


def test_compare_sources_uses_metadata_not_label():
    from urban_data import UrbanData
    from congestion_levels import MIXED_SOURCES
    a = UrbanData("A", "붐빔 (샘플)", 0, data_source="api")
    b = UrbanData("B", "여유", 20, data_source="sample")
    analyzer = DataAnalyzer()
    assert analyzer.compare_urban_data(a, b) == MIXED_SOURCES
    assert analyzer.calculate_average_temperature(a, b) is None
    b.data_source = "api"
    assert analyzer.compare_urban_data(a, b) == FIRST_MORE
    assert analyzer.calculate_average_temperature(a, b) == 10
    b.weather = float("nan")
    assert analyzer.calculate_average_temperature(a, b) is None
    b.weather = None
    assert analyzer.calculate_average_temperature(a, b) is None
