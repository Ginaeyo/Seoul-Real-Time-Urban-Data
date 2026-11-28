from data_provider import DataProvider
from urban_data import UrbanData
from place import Place

class SampleDataProvider(DataProvider):
    SAMPLE_VALUES = {
        "강남역": ("약간 붐빔", 18.5, "서행"),
        "홍대입구역(2호선)": ("붐빔", 16.3, "정체"),
        "잠실역": ("보통", 17.2, "원활"),
        "명동 관광특구": ("약간 붐빔", 19.0, "서행"),
        "서울역": ("여유", 15.8, "원활"),
    }
    def get_data(self, place: Place) -> UrbanData:
        if not isinstance(place, Place):
            raise TypeError("place must be a Place object")
        area_name = place.area_name

        congestion, weather, traffic = self.SAMPLE_VALUES.get(
            area_name, ("보통", 18.5, "원활")
        )

        return UrbanData(
            area_name=area_name,
            congestion=congestion,
            weather=weather,
            traffic=traffic,
            traffic_sample=True,
            data_source="sample",
            rain_chance=10,
            dust_status="좋음"
        )
