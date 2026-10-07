class AreaManager:
    def __init__(self):
        self.areas = [
            "강남역",
            "홍대입구",
            "잠실",
            "명동",
            "서울역"
        ]

    def show_areas(self):
        print("\n=== 지역 목록 ===")

        for i, area in enumerate(self.areas, start=1):
            print(f"{i}. {area}")

    def get_area(self, index):
        if 1 <= index <= len(self.areas):
            return self.areas[index - 1]

        return None