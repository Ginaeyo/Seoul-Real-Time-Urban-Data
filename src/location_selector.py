"""콘솔에서 사용자가 조회할 지역을 선택하는 모듈.

TODO(담당: 김효중)
- AreaManager의 지역 목록을 보여 주고 번호 입력을 받는다.
- 숫자가 아닌 입력과 범위를 벗어난 번호를 안전하게 처리한다.
- select_location()은 선택된 Place 또는 실패 시 None을 반환한다.
"""

class LocationSelector:

    def select_location(self, area_manager):
        print("\n=== 지역 검색 ===")
        keyword = input("지역명을 입력하세요 (전체 목록은 Enter): ").strip()

        areas = area_manager.search_areas(keyword)

        if not areas:
            print("검색 결과가 없습니다.")
            return None

        print("\n=== 검색 결과 ===")

        for i, area in enumerate(areas, start=1):
            print(f"{i}. {area.area_name}")

        try:
            choice = int(input("\n지역 번호를 선택하세요: "))

            if 1 <= choice <= len(areas):
                return areas[choice - 1]

            print("잘못된 번호입니다.")
            return None

        except ValueError:
            print("숫자를 입력해주세요.")
            return None

    def select_comparison_areas(self, area_manager):
        print("\n=== 첫 번째 지역 선택 ===")
        first = self.select_location(area_manager)

        if first is None:
            return None

        while True:
            print("\n=== 두 번째 지역 선택 ===")
            second = self.select_location(area_manager)

            if second is None:
                return None

            if first.area_name == second.area_name:
                print("서로 다른 두 지역을 선택해주세요.")
                continue

            return first, second