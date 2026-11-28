"""혼잡도를 분석하고 표현 형식과 독립적인 결과를 반환합니다."""
import math
from congestion_levels import MIXED_SOURCES, normalize_congestion, FIRST_MORE, SECOND_MORE, EQUAL, UNKNOWN


class DataAnalyzer:
    def analyze_congestion(self, congestion):
        """혼잡도 단계(1~4) 또는 알 수 없는 경우 None을 반환합니다."""
        return normalize_congestion(congestion)[0]

    def compare_congestion(self, area1, congestion1, area2, congestion2):
        """두 지역의 비교 상태를 반환합니다. 지역명 인자는 기존 호출 호환성을 위해 유지합니다."""
        level1 = self.analyze_congestion(congestion1)
        level2 = self.analyze_congestion(congestion2)
        if level1 is None or level2 is None:
            return UNKNOWN
        if level1 > level2:
            return FIRST_MORE
        if level1 < level2:
            return SECOND_MORE
        return EQUAL

    def calculate_population_midpoint(self, urban_data):
        """유효한 인구 범위의 정수 중간값을 반환합니다."""
        low = getattr(urban_data, "population_min", None)
        high = getattr(urban_data, "population_max", None)
        if type(low) is int and type(high) is int and 0 <= low <= high:
            return (low + high) // 2
        return None

    def compare_urban_data(self, first_data, second_data):
        """출처가 일치하는 경우에만 혼잡도를 비교합니다."""
        if first_data.data_source != second_data.data_source:
            return MIXED_SOURCES
        if first_data.data_source not in ("api", "sample"):
            return UNKNOWN
        return self.compare_congestion(first_data.area_name, first_data.congestion,
                                       second_data.area_name, second_data.congestion)

    def calculate_average_temperature(self, first_data, second_data):
        """동일한 출처의 유효한 숫자형 기온 두 개의 산술평균을 반환합니다."""
        if first_data.data_source != second_data.data_source or first_data.data_source not in ("api", "sample"):
            return None
        temps = (first_data.weather, second_data.weather)
        if not all(type(t) in (int, float) and math.isfinite(t) for t in temps):
            return None
        return sum(temps) / 2
