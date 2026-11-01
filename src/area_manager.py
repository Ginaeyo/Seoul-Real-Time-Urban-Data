"""서울 지원 지역 목록과 지역 조회를 관리하는 모듈.

TODO(담당: 김효중 / 협력: 민경환, 할리오나)
- 지역명과 확인된 API 지역 코드로 Place 목록을 구성한다.
- show_areas()에서 지역 목록을 번호와 함께 보여 준다.
- get_area(index)는 유효한 번호에 Place를 반환하고, 잘못된 번호에는 None을 반환한다.
"""
"""서울 실시간 도시데이터 지역 목록 관리.

Place 객체는 area_name, area_code 속성을 제공한다고 가정합니다.
121개 지역 목록 자체는 Place 담당 팀원으로부터 주입받습니다.
"""

class AreaManager:
    def __init__(self, Areas=None):
        self.Areas = list(Areas) if Areas is not None else []

    def get_areas(self):
        """Place 객체 전체 목록을 반환합니다."""
        return list(self.Areas)

    def search_areas(self, search_keyword):
        """검색어를 포함하는 지역을 Place 객체 리스트로 반환합니다.

        빈 검색어이면 전체 목록을 반환합니다.
        """
        keyword = str(search_keyword).strip().casefold()
        return [area for area in self.Areas
                if keyword in area.area_name.casefold()]

    def get_area(self, area_identifier):
        """선택 번호(1부터), 지역명 또는 지역코드로 Place 객체 조회.

        찾지 못하거나 잘못된 번호이면 None을 반환합니다.
        """
        if isinstance(area_identifier, int) and not isinstance(area_identifier, bool):
            if 1 <= area_identifier <= len(self.Areas):
                return self.Areas[area_identifier - 1]
            return None
        if not isinstance(area_identifier, str):
            return None
        value = area_identifier.strip()
        if not value:
            return None
        for area in self.Areas:
            if area.area_name == value or str(area.area_code) == value:
                return area
        return None

    def show_areas(self):
        """'지역코드. 지역명' 형식으로 전체 지역을 콘솔에 출력합니다."""
        for area in self.get_areas():
            print(f"{area.area_code}. {area.area_name}")
