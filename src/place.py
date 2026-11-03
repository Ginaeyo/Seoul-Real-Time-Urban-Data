"""서울 내 조회 지역의 이름과 API 코드를 담는 데이터 모델.

TODO(담당: 민경환 / 지역 목록 협의: 김효중, 할리오나)
- Place에 area_name과 확인된 area_code를 저장한다.
- get_info()가 지역명과 코드를 일관된 형식으로 반환하게 한다.
- 확인되지 않은 API 코드를 임의로 만들지 않는다.
"""
class Place:
    def __init__(self, area_name, area_code=None):
        self.area_name = area_name
        self.area_code = area_code

    def get_info(self):
        return {
            "name": self.area_name,
            "code": self.area_code
        }

    def __str__(self):
        return f"{self.area_name} ({self.area_code or '코드 없음'})"