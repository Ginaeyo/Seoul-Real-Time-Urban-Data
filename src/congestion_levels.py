"""분석과 시각화가 공유하는 혼잡도 기준 및 비교 상태."""
from types import MappingProxyType

LEVELS = MappingProxyType({"여유": 1, "보통": 2, "약간 붐빔": 3, "붐빔": 4})
FIRST_MORE = "first_more"
SECOND_MORE = "second_more"
EQUAL = "equal"
UNKNOWN = "unknown"
MIXED_SOURCES = "mixed_sources"


def normalize_congestion(congestion):
    clean = congestion.replace(" (샘플)", "").strip() if isinstance(congestion, str) else ""
    return LEVELS.get(clean), clean if clean in LEVELS else "정보 없음"
