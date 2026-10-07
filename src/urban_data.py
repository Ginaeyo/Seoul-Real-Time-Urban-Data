class UrbanData:
    def __init__(self, area_name, congestion, weather):
        self.area_name = area_name
        self.congestion = congestion
        self.weather = weather

    def display_info(self):
        print(f"\n지역: {self.area_name}")
        print(f"혼잡도: {self.congestion}")
        print(f"날씨: {self.weather}")