from data_provider import DataProvider
from urban_data import UrbanData

class SampleDataProvider(DataProvider):
    SAMPLE_VALUES = {
        "강남역": ("약간 붐빔", "18.5°C", "서행"),
        "홍대입구역(2호선)": ("붐빔", "16.3°C", "정체"),
        "잠실역": ("보통", "17.2°C", "원활"),
        "명동 관광특구": ("약간 붐빔", "19.0°C", "서행"),
        "서울역": ("여유", "15.8°C", "원활"),
    }
    def get_data(self, place):
        area_name = getattr(place, "area_name", None) or str(place)

        print("샘플 데이터를 사용합니다.")

        congestion, weather, traffic = self.SAMPLE_VALUES.get(
            area_name, ("보통", "18.5°C", "원활")
        )

        return UrbanData(
            area_name=area_name,
            congestion=f"{congestion} (샘플)",
            weather=weather,
            traffic=traffic,
            traffic_sample=True,
            data_source="sample",
            rain_chance=10,
            dust_status="좋음"
        )