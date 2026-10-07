class LocationSelector:
    def select_location(self, area_manager):
        area_manager.show_areas()

        try:
            choice = int(input("\n지역 번호를 선택하세요: "))
            return area_manager.get_area(choice)

        except ValueError:
            return None