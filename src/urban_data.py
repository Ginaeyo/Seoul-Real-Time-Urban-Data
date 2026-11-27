"""API 또는 샘플에서 받은 도시 정보를 담는 데이터 모델."""

class UrbanData:
    def __init__(self, area_name=None, congestion=None, weather=None, population=None,
                 updated_at=None, traffic=None, traffic_sample=False, data_source="api",
                 rain_chance=None, dust_status=None):
        self.area_name = area_name
        self.congestion = congestion
        self.weather = weather
        self.population = population
        self.updated_at = updated_at
        self.traffic = traffic
        self.traffic_sample = traffic_sample
        self.data_source = data_source
        self.rain_chance = rain_chance
        self.dust_status = dust_status

   
