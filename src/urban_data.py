"""API 또는 샘플에서 받은 도시 정보를 담는 데이터 모델.

TODO(담당: 민경환 / 필드 협의: 할리오나, 원미혜)
- 기본 필드 area_name, congestion, weather를 일관되게 저장한다.
- API에서 제공되는 것이 확인된 항목만 팀 합의 후 추가한다.
- 값이 없는 필드는 None을 허용해 화면에서 안전하게 표시할 수 있게 한다.
"""


class UrbanData:
    """지역의 도시 정보(혼잡도, 날씨)를 저장한다.

    기본 필드는 area_name, congestion, weather 이다.
    값이 없는 필드는 None 으로 둘 수 있다.
    API에서 제공되는 것이 확인된 항목만 팀 합의 후 추가한다.
    """

    def __init__(self, area_name=None, congestion=None, weather=None):
        self.area_name = area_name    # 지역 이름
        self.congestion = congestion  # 혼잡도 (없으면 None)
        self.weather = weather        # 날씨 (없으면 None)

    def display_info(self):
        """저장된 정보를 그대로 콘솔에 출력한다."""
        print(f"\n지역: {self.area_name}")
        print(f"혼잡도: {self.congestion}")
        print(f"날씨: {self.weather}")
