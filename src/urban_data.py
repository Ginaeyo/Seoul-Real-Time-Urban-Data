"""API 또는 샘플에서 받은 도시 정보를 담는 데이터 모델."""

class UrbanData:
    def __init__(self, area_name=None, congestion=None, weather=None, population=None, updated_at=None, traffic=None, traffic_sample=False, data_source="api"):
        self.area_name = area_name
        self.congestion = congestion
        self.weather = weather
        self.population = population
        self.updated_at = updated_at
        self.traffic = traffic
        self.traffic_sample = traffic_sample
        self.data_source = data_source

    def display_info(self):
        print(f"\n지역: {self.area_name or '정보 없음'}")
        print(f"혼잡도: {self.congestion or '정보 없음'}")
        print(f"날씨: {self.weather or '정보 없음'}")
        print(f"교통상황: {self.traffic or '정보 없음'}")
