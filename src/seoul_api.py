from urban_data import UrbanData


class SeoulAPI:
    def get_data(self, area_name):

        sample_data = {
            "강남역": ("붐빔", "맑음"),
            "홍대입구": ("보통", "흐림"),
            "잠실": ("약간 붐빔", "맑음"),
            "명동": ("붐빔", "비"),
            "서울역": ("보통", "흐림")
        }

        congestion, weather = sample_data.get(
            area_name,
            ("정보 없음", "정보 없음")
        )

        return UrbanData(
            area_name,
            congestion,
            weather
        )