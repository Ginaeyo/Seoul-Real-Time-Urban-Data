import os
import sys

sys.path.insert(
    0,
    os.path.join(os.path.dirname(__file__), "..", "src")
)

from data_analyzer import DataAnalyzer


def test_compare_different_congestion():
    analyzer = DataAnalyzer()

    result = analyzer.compare_congestion(
        "강남역", "붐빔",
        "홍대입구", "보통"
    )

    assert result == "강남역이(가) 홍대입구보다 혼잡합니다."


def test_compare_same_congestion():
    analyzer = DataAnalyzer()

    result = analyzer.compare_congestion(
        "강남역", "보통",
        "홍대입구", "보통"
    )

    assert result == "두 지역의 혼잡도는 같습니다."


def test_compare_unknown_congestion():
    analyzer = DataAnalyzer()

    result = analyzer.compare_congestion(
        "강남역", "정보 없음",
        "홍대입구", "보통"
    )

    assert result == "혼잡도를 비교할 수 없습니다."