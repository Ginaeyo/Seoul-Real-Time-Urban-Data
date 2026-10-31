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
    """지역 선택 → 데이터 조회 → 대시보드 출력 → 혼잡도 분석 결과 출력 순서로 실행한다."""

    def __init__(self):
        self.area_manager = AreaManager()            # 지원 지역 목록 관리
        self.location_selector = LocationSelector()  # 사용자 입력으로 지역 선택
        self.api = SeoulAPI()                        # 도시 데이터 조회
        self.analyzer = DataAnalyzer()               # 혼잡도 설명 생성
        self.dashboard = Dashboard()                 # 결과 출력

    def run(self):
        """전체 흐름을 실행한다. 문제가 생기면 안내 메시지만 출력하고 끝낸다."""

        print("=================================")
        print("Seoul Real-Time Urban Data")
        print("=================================")

        # 1) 지역 선택 (잘못된 입력이면 None)
        area = self.location_selector.select_location(
            self.area_manager
        )

        if area is None:
            print("잘못된 입력입니다.")
            return

        # 2) 데이터 조회 (API 오류나 데이터 없음이면 None)
        urban_data = self.api.get_data(area)

        if urban_data is None:
            print("도시 데이터를 가져오지 못했습니다.")
            return

        # 3) 지역과 도시 정보 출력
        self.dashboard.display(area, urban_data)

        # 4) 혼잡도 분석 결과 출력
        result = self.analyzer.analyze_congestion(
            urban_data.congestion
        )

        print(result)


if __name__ == "__main__":
    app = MainApp()
    app.run()
