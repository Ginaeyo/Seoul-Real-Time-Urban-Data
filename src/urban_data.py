"""API 또는 샘플에서 받은 도시 정보를 담는 데이터 모델.

TODO(담당: 민경환 / 필드 협의: 할리오나, 원미혜)
- 기본 필드 area_name, congestion, weather를 일관되게 저장한다.
- API에서 제공되는 것이 확인된 항목만 팀 합의 후 추가한다.
- 값이 없는 필드는 None을 허용해 화면에서 안전하게 표시할 수 있게 한다.
"""

class UrbanData:
    def __init__(self, area_name=None, congestion=None, weather=None):
        self.area_name = area_name
        self.congestion = congestion
        self.weather = weather

    def display_info(self):
        print(f"\n지역: {self.area_name or '정보 없음'}")
        print(f"혼잡도: {self.congestion or '정보 없음'}")
        print(f"날씨: {self.weather or '정보 없음'}")
