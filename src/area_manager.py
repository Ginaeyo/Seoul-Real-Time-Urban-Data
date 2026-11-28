"""서울 지원 지역 목록과 지역 조회를 관리하는 모듈."""
import csv
from pathlib import Path
from place import Place


class AreaManager:

    def __init__(self):
        # 실행 위치와 무관하게 이 모듈 옆의 CSV를 읽습니다.
        path = Path(__file__).resolve().with_name("places.csv")
        self.areas = []
        seen = set()
        with path.open(encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)
            if not reader.fieldnames or not {"area_name", "area_code"}.issubset(reader.fieldnames):
                raise ValueError("CSV에 area_name, area_code 열이 필요합니다.")
            for row in reader:
                name = (row["area_name"] or "").strip()
                code = (row["area_code"] or "").strip() or None
                if not name or name in seen:
                    raise ValueError(f"비어 있거나 중복된 지역명: {name}")
                seen.add(name)
                self.areas.append(Place(name, code))
        if not self.areas:
            raise ValueError("CSV 지역 목록이 비어 있습니다.")

    def get_areas(self):
        """전체 지역 목록 반환"""
        return list(self.areas)

    def search_areas(self, search_keyword):
        """지역명으로 검색"""
        keyword = str(search_keyword).strip().casefold()

        if not keyword:
            return self.get_areas()

        return [
            area for area in self.areas
            if keyword in area.area_name.casefold()
        ]

    def get_area(self, area_identifier):

        if isinstance(area_identifier, int) and not isinstance(area_identifier, bool):
            if 1 <= area_identifier <= len(self.areas):
                return self.areas[area_identifier - 1]
            return None

        if isinstance(area_identifier, str):
            value = area_identifier.strip()

            for area in self.areas:
                if area.area_name == value:
                    return area

                if area.area_code is not None and str(area.area_code) == value:
                    return area

        return None
