"""서울 지원 지역 목록과 지역 조회를 관리하는 모듈.

TODO(담당: 김효중 / 협력: 민경환, 할리오나)
- 지역명과 확인된 API 지역 코드로 Place 목록을 구성한다.
- show_areas()에서 지역 목록을 번호와 함께 보여 준다.
- get_area(index)는 유효한 번호에 Place를 반환하고, 잘못된 번호에는 None을 반환한다.
"""
class AreaManager:
    def __init__(self):
        self.areas = [
            "강남역",
            "홍대입구",
            "잠실",
            "명동",
            "서울역"
        ]

    def show_areas(self):
        print("\n=== 지역 목록 ===")

        for i, area in enumerate(self.areas, start=1):
            print(f"{i}. {area}")

    def get_area(self, index):
        if 1 <= index <= len(self.areas):
            return self.areas[index - 1]

        return None