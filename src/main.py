"""프로그램 실행 흐름을 연결하는 진입점.

TODO(담당: 민경환 / 통합 협력: 에르덴자야)
- 지역 선택, SeoulAPI 데이터 조회, 대시보드 출력, 혼잡도 분석 흐름을 연결한다.
- Place 객체를 사용하도록 각 모듈의 입력과 반환 형식을 맞춘다.
- 잘못된 지역 선택이나 API 오류가 발생해도 사용자에게 안내한다.
"""

from area_manager import AreaManager
from location_selector import LocationSelector
from seoul_api import SeoulAPI
from data_analyzer import DataAnalyzer
from dashboard import Dashboard


class MainApp:
    def __init__(self):
        self.area_manager = AreaManager()
        self.location_selector = LocationSelector()
        self.api = SeoulAPI()
        self.analyzer = DataAnalyzer()
        self.dashboard = Dashboard()
        # 마지막으로 조회한 지역 (새로고침에 사용, 없으면 None)
        self.current_area = None

    def run(self):
        print("=================================")
        print("Seoul Real-Time Urban Data")
        print("=================================")

        while True:
            print("\n=== 메뉴 ===")
            print("1. 지역 실시간 정보 조회")
            print("2. 두 지역 혼잡도 비교")
            print("3. 종료")
            print("4. 마지막 지역 새로고침")

            choice = input("\n메뉴를 선택하세요: ").strip()

            if choice == "1":
                self.show_area_info()

            elif choice == "2":
                self.compare_areas()

            elif choice == "3":
                print("프로그램을 종료합니다.")
                break

            elif choice == "4":
                self.refresh_data()

            else:
                print("1, 2, 3, 4 중에서 선택해주세요.")

    def load_area(self):
        """지역을 선택받아 current_area에 저장하고 반환한다.

        잘못된 입력이면 안내 문구를 출력하고 None을 반환한다.
        """
        area = self.location_selector.select_location(
            self.area_manager
        )

        if area is None:
            print("잘못된 입력입니다.")
            return None

        self.current_area = area
        return area

    def refresh_data(self):
        """current_area의 데이터를 다시 조회해 대시보드와 분석 결과를 출력한다."""
        if self.current_area is None:
            print("먼저 1번 메뉴에서 지역을 조회해주세요.")
            return

        urban_data = self.api.get_data(self.current_area)

        if urban_data is None:
            print("도시 데이터를 가져오지 못했습니다.")
            return

        self.dashboard.display(self.current_area, urban_data)

        result = self.analyzer.analyze_congestion(
            urban_data.congestion
        )

        print(result)

    def show_area_info(self):
        if self.load_area() is None:
            return

        self.refresh_data()

    def compare_areas(self):
        selected_areas = self.location_selector.select_comparison_areas(
            self.area_manager
        )

        if selected_areas is None:
            return

        first_area, second_area = selected_areas

        first_data = self.api.get_data(first_area)
        second_data = self.api.get_data(second_area)

        if first_data is None or second_data is None:
            print("도시 데이터를 가져오지 못했습니다.")
            return

        print("\n=== 첫 번째 지역 ===")
        self.dashboard.display(first_area, first_data)

        print("\n=== 두 번째 지역 ===")
        self.dashboard.display(second_area, second_data)

        result = self.analyzer.compare_congestion(
            first_area.area_name,
            first_data.congestion,
            second_area.area_name,
            second_data.congestion
        )

        print("\n=== 혼잡도 비교 결과 ===")
        print(result)


if __name__ == "__main__":
    app = MainApp()
    app.run()