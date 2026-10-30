"""콘솔에서 사용자가 조회할 지역을 선택하는 모듈.

TODO(담당: 김효중)
- AreaManager의 지역 목록을 보여 주고 번호 입력을 받는다.
- 숫자가 아닌 입력과 범위를 벗어난 번호를 안전하게 처리한다.
- select_location()은 선택된 Place 또는 실패 시 None을 반환한다.
"""
class LocationSelector:
    def select_location(self, area_manager):
        area_manager.show_areas()

        try:
            choice = int(input("\n지역 번호를 선택하세요: "))
            return area_manager.get_area(choice)

        except ValueError:
            return None