"""프로그램 실행 흐름과 콘솔 기반 시각화를 연결합니다."""

import sys

from area_manager import AreaManager
from location_selector import LocationSelector
from seoul_api import SeoulAPI
from data_analyzer import DataAnalyzer
from dashboard import Dashboard
from congestion_chart import (
    is_sample_congestion,
    plot_area_dashboard,
    plot_congestion_comparison,
)


class MainApp:
    def __init__(self):
        self.area_manager = AreaManager()
        self.location_selector = LocationSelector()
        self.api = SeoulAPI()
        self.analyzer = DataAnalyzer()
        self.dashboard = Dashboard()

    def run(self):
        print("=" * 44)
        print("서울 인구·날씨 대시보드")
        print("=" * 44)
        while True:
            print("\n1. 지역 정보 조회")
            print("2. 두 지역 혼잡도 비교 (그래프)")
            print("3. 종료")
            choice = input("\n메뉴를 선택하세요: ").strip()
            if choice == "1":
                self.show_area_info()
            elif choice == "2":
                self.compare_areas()
            elif choice == "3":
                print("프로그램을 종료합니다.")
                break
            else:
                print("1, 2, 3 중에서 선택해주세요.")

    def show_area_info(self):
        area = self.location_selector.select_location(self.area_manager)
        if area is None:
            print("잘못된 입력입니다.")
            return
        urban_data = self.api.get_data(area)
        if urban_data is None:
            print("도시 데이터를 가져오지 못했습니다.")
            return
        self.dashboard.display(area, urban_data)
        print(self.analyzer.analyze_congestion(urban_data.congestion))
        try:
            image_path = plot_area_dashboard(
                area.area_name, urban_data.congestion, getattr(urban_data, "weather", None),
                traffic=getattr(urban_data, "traffic", None),
                population=getattr(urban_data, "population", None),
                rain_chance=getattr(urban_data, "rain_chance", None),
                dust_status=getattr(urban_data, "dust_status", None),
            )
            print(f"상세 대시보드 저장 위치: {image_path}")
        except ImportError:
            print("시각화 기능을 사용하려면 matplotlib를 설치하세요: pip install matplotlib")
        except OSError:
            print("상세 대시보드 이미지를 저장할 수 없습니다.")

    def compare_areas(self):
        selected_areas = self.location_selector.select_comparison_areas(self.area_manager)
        if selected_areas is None:
            return
        first_area, second_area = selected_areas
        first_data, second_data = self.api.get_data(first_area), self.api.get_data(second_area)
        if first_data is None or second_data is None:
            print("도시 데이터를 가져오지 못했습니다.")
            return
        first_sample = is_sample_congestion(first_data.congestion)
        second_sample = is_sample_congestion(second_data.congestion)
        first_source = "시연" if first_sample else "실시간"
        second_source = "시연" if second_sample else "실시간"
        print(f"\n=== 첫 번째 지역 ({first_source}) ===")
        self.dashboard.display(first_area, first_data)
        print(f"\n=== 두 번째 지역 ({second_source}) ===")
        self.dashboard.display(second_area, second_data)
        print("\n=== 혼잡도 비교 결과 ===")
        if first_sample != second_sample:
            print("실시간 데이터와 시연 데이터의 혼잡도 순위는 비교하지 않습니다.")
        else:
            print(self.analyzer.compare_congestion(
                first_area.area_name, first_data.congestion,
                second_area.area_name, second_data.congestion,
            ))
        try:
            chart_path = plot_congestion_comparison(
                first_area.area_name, first_data.congestion, second_area.area_name, second_data.congestion,
                getattr(first_data, "weather", None), getattr(second_data, "weather", None),
                first_traffic=getattr(first_data, "traffic", None),
                second_traffic=getattr(second_data, "traffic", None),
                first_population=getattr(first_data, "population", None),
                second_population=getattr(second_data, "population", None),
                first_environment=(getattr(first_data, "rain_chance", None),
                                   getattr(first_data, "dust_status", None)),
                second_environment=(getattr(second_data, "rain_chance", None),
                                    getattr(second_data, "dust_status", None)),
            )
            print(f"그래프 저장 위치: {chart_path}")
        except ImportError:
            print("그래프 기능을 사용하려면 matplotlib를 설치하세요: pip install matplotlib")
        except OSError:
            print("비교 그래프 이미지를 저장할 수 없습니다.")
        except ValueError as error:
            print(f"그래프를 표시할 수 없습니다: {error}")


if __name__ == "__main__":
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure") and not stream.isatty():
            stream.reconfigure(encoding="utf-8")
    try:
        MainApp().run()
    except (EOFError, KeyboardInterrupt):
        print("\n프로그램을 종료합니다.")
