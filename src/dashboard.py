class Dashboard:
    def display(self, place, urban_data):
        print("\n===== Seoul Real-Time Urban Data =====")
        print(f"지역: {place.area_name}")
        print(f"혼잡도: {urban_data.congestion}")
        print(f"날씨: {urban_data.weather}")
        print("=====================================\n")