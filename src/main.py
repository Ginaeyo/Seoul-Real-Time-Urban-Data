from area_manager import AreaManager
from location_selector import LocationSelector
from seoul_api import SeoulAPI
from data_analyzer import DataAnalyzer


class MainApp:

    def __init__(self):
        self.area_manager = AreaManager()
        self.location_selector = LocationSelector()
        self.api = SeoulAPI()
        self.analyzer = DataAnalyzer()

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

        urban_data.display_info()

        result = self.analyzer.analyze_congestion(
            urban_data.congestion
        )

        print(result)


if __name__ == "__main__":
    app = MainApp()
    app.run()