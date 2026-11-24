"""서울 지원 지역 목록과 지역 조회를 관리하는 모듈.

TODO(담당: 김효중 / 협력: 민경환, 할리오나)
- 지역명과 확인된 API 지역 코드로 Place 목록을 구성한다.
- show_areas()에서 지역 목록을 번호와 함께 보여 준다.
- get_area(index)는 유효한 번호에 Place를 반환하고, 잘못된 번호에는 None을 반환한다.
"""
from place import Place


class AreaManager:

    def __init__(self):
        # 표시 이름과 API 장소명이 다른 경우 두 번째 인수로 공식 장소명을 사용합니다.
        self.areas = [
            Place("강남역"),
            Place("홍대입구역(2호선)"),
            Place("잠실역"),
            Place("명동 관광특구"),
            Place("서울역"),
            Place("건대입구역"),
            Place("성수카페거리"),
            Place("이태원 관광특구"),
            Place("고속터미널역"),
            Place("광화문·덕수궁"),
            Place("여의도한강공원"),
            Place("반포한강공원"),
            Place("서울숲공원"),
            Place("광화문광장"),
            Place("DDP(동대문디자인플라자)"),
            Place("남대문시장"),
            Place("고척돔"),
            Place("잠실종합운동장"),
            Place("노들섬"),
            Place("어린이대공원"),
            Place("왕십리역"),
        ]

    def get_areas(self):
        """전체 지역 목록 반환"""
        return list(self.areas)

    def search_areas(self, search_keyword):
        """지역명으로 검색"""
        keyword = str(search_keyword).strip().casefold()

        if not keyword:
            return self.get_areas()

        return [
            area for area in self.areas
            if keyword in area.area_name.casefold()
        ]

    def show_areas(self):
        print("\n=== 지역 목록 ===")

        for i, area in enumerate(self.areas, start=1):
            print(f"{i}. {area.area_name}")

    def get_area(self, area_identifier):

        if isinstance(area_identifier, int) and not isinstance(area_identifier, bool):
            if 1 <= area_identifier <= len(self.areas):
                return self.areas[area_identifier - 1]
            return None

        if isinstance(area_identifier, str):
            value = area_identifier.strip()

            for area in self.areas:
                if area.area_name == value:
                    return area

                if area.area_code is not None and str(area.area_code) == value:
                    return area

        return None

