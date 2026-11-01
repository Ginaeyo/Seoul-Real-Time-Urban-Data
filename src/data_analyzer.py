"""혼잡도 정보를 이해하기 쉬운 설명으로 바꾸는 모듈.

TODO(담당: 김효중 / main.py 연결: 민경환)
- 혼잡도 값별로 사용자에게 보여 줄 설명을 반환한다.
- None 또는 예상하지 못한 값에는 정보가 없다는 안내를 반환한다.
- 분석 결과가 MainApp 실행 흐름에서 실제로 출력되도록 연결한다.
"""
"""두 지역의 UrbanData를 항목별로 정리하고 비교하는 클래스.

UrbanData는 population, weather, traffic, transit, culture_events 속성을
제공한다고 가정합니다. 실제 API 응답 세부 필드가 확정되면 각 prepare_*에서
필요한 값들을 추출하도록 확장하면 됩니다.
"""
from datetime import datetime
from numbers import Real


class DataAnalyzer:
    def __init__(self, urban_data=None):
        self.urban_data = urban_data
        self.comparison_date = None
        self.comparison_result = None

    @staticmethod
    def _prepare(value):
        """누락값을 빈 값으로 정리하고 원본 데이터는 변경하지 않습니다."""
        if value is None:
            return {"status": "정보 없음"}
        if isinstance(value, dict):
            return dict(value)
        if isinstance(value, list):
            return list(value)
        return value

    def prepare_population(self, urban_data=None):
        data = urban_data if urban_data is not None else self.urban_data
        return self._prepare(getattr(data, "population", None))

    def prepare_weather(self, urban_data=None):
        data = urban_data if urban_data is not None else self.urban_data
        return self._prepare(getattr(data, "weather", None))

    def prepare_traffic(self, urban_data=None):
        data = urban_data if urban_data is not None else self.urban_data
        return self._prepare(getattr(data, "traffic", None))

    def prepare_transit(self, urban_data=None):
        data = urban_data if urban_data is not None else self.urban_data
        return self._prepare(getattr(data, "transit", None))

    def prepare_culture_events(self, urban_data=None):
        data = urban_data if urban_data is not None else self.urban_data
        return self._prepare(getattr(data, "culture_events", None))

    @staticmethod
    def _numeric_differences(first, second):
        """동일한 키에 담긴 숫자만 '첫 지역 - 둘째 지역' 차이 계산.

        숫자 필드의 단위와 의미가 양쪽에서 동일하다는 전제입니다.
        정성적인 혼잡도나 이벤트 목록은 억지로 숫자로 비교하지 않습니다.
        """
        if not isinstance(first, dict) or not isinstance(second, dict):
            return {}
        differences = {}
        for key in first.keys() & second.keys():
            left, right = first[key], second[key]
            if (isinstance(left, Real) and not isinstance(left, bool)
                    and isinstance(right, Real) and not isinstance(right, bool)):
                differences[key] = left - right
        return differences

    def compare_areas(self, area1_data, area2_data,
                      area1_name="지역 1", area2_name="지역 2"):
        """두 UrbanData 객체를 받아 항목별 비교 결과를 반환합니다.

        지역명을 직접 input() 받지 않습니다. Main/LocationSelector가 선택하고
        SeoulAPI/UrbanData가 제공한 객체를 매개변수로 전달해야 합니다.
        """
        if area1_data is None or area2_data is None:
            raise ValueError("비교할 두 지역의 UrbanData 객체가 모두 필요합니다.")

        self.comparison_date = datetime.now().astimezone().isoformat(timespec="seconds")
        methods = (
            ("population", self.prepare_population),
            ("weather", self.prepare_weather),
            ("traffic", self.prepare_traffic),
            ("transit", self.prepare_transit),
            ("culture_events", self.prepare_culture_events),
        )
        results = {}
        for category, prepare in methods:
            first = prepare(area1_data)
            second = prepare(area2_data)
            results[category] = {
                "area1": first,
                "area2": second,
                "numeric_differences": self._numeric_differences(first, second),
            }

        self.comparison_result = {
            "area1_name": area1_name,
            "area2_name": area2_name,
            "comparison_date": self.comparison_date,
            "results": results,
        }
        return self.comparison_result
