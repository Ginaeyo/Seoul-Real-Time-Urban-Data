class Place:
    def __init__(self, area_name, area_code):
        self.area_name = area_name
        self.area_code = area_code

    def get_info(self):
        return {
            "name": self.area_name,
            "code": self.area_code
        }

    def __str__(self):
        return f"{self.area_name} ({self.area_code})"