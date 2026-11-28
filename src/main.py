"""프로그램 실행 흐름과 콘솔 기반 시각화를 연결합니다."""

import sys
from data_provider import DataProvider

from area_manager import AreaManager
from location_selector import LocationSelector
from seoul_api import SeoulAPI
from data_analyzer import DataAnalyzer
from dashboard import Dashboard
from sample_data_provider import SampleDataProvider

class MainApp:
    def __init__(self, api: DataProvider, *, area_manager, location_selector, analyzer, dashboard):
        self.area_manager = area_manager
        self.location_selector = location_selector
        self.api = api
        self.analyzer = analyzer
        self.dashboard = dashboard

    def run(self):
        self.dashboard.show_title()
        while True:
            self.dashboard.show_menu()
            choice = input("\n메뉴를 선택하세요: ").strip()
            if choice == "1":
                self.show_area_info()
            elif choice == "2":
                self.compare_areas()
            elif choice == "3":
                self.dashboard.show_message("프로그램을 종료합니다.")
                break
            else:
                self.dashboard.show_message("1, 2, 3 중에서 선택해주세요.")

    def show_area_info(self):
        area = self.location_selector.select_location(self.area_manager)
        if area is None:
            self.dashboard.show_message("잘못된 입력입니다.")
            return
        urban_data = self.api.get_data(area)
        if urban_data is None:
            self.dashboard.show_message("도시 데이터를 가져오지 못했습니다.")
            return
        midpoint = self.analyzer.calculate_population_midpoint(urban_data)
        self.dashboard.display(area, urban_data, midpoint=midpoint)
        result = self.analyzer.analyze_congestion(urban_data.congestion)
        self.dashboard.display_analysis(result)
        self.dashboard.display_area_chart(area, urban_data, midpoint=midpoint)

    def compare_areas(self):
        selected_areas = self.location_selector.select_comparison_areas(self.area_manager)
        if selected_areas is None:
            return
        first_area, second_area = selected_areas
        first_data, second_data = self.api.get_data(first_area), self.api.get_data(second_area)
        if first_data is None or second_data is None:
            self.dashboard.show_message("도시 데이터를 가져오지 못했습니다.")
            return
        result = self.analyzer.compare_urban_data(first_data, second_data)
        average = self.analyzer.calculate_average_temperature(first_data, second_data)
        midpoints = {
            "first_midpoint": self.analyzer.calculate_population_midpoint(first_data),
            "second_midpoint": self.analyzer.calculate_population_midpoint(second_data),
        }
        self.dashboard.display_comparison(first_area, first_data, second_area, second_data, result, **midpoints)
        self.dashboard.display_comparison_chart(first_area, first_data, second_area, second_data, average_temperature=average, **midpoints)


if __name__ == "__main__":
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure") and not stream.isatty():
            stream.reconfigure(encoding="utf-8")
    dashboard = Dashboard()
    try:
        MainApp(SeoulAPI(fallback_provider=SampleDataProvider()),
                area_manager=AreaManager(), location_selector=LocationSelector(),
                analyzer=DataAnalyzer(), dashboard=dashboard).run()
    except (EOFError, KeyboardInterrupt):
        dashboard.show_message("\n프로그램을 종료합니다.")
