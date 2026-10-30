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

    def run(self):

        print("=================================")
        print("Seoul Real-Time Urban Data")
        print("=================================")

        area = self.location_selector.select_location(
            self.area_manager
        )

        if area is None:
            print("잘못된 입력입니다.")
            return

        urban_data = self.api.get_data(area)

        self.dashboard.display(area, urban_data)

        result = self.analyzer.analyze_congestion(
            urban_data.congestion
        )

        print(result)


if __name__ == "__main__":
    app = MainApp()
    app.run()
