"""선택 지역과 실시간 도시 정보를 콘솔에 표시하는 모듈.

TODO(담당: 원미혜 / 데이터 필드 협의: 민경환)
- display(place, urban_data)에서 지역명, 혼잡도, 날씨와 사용 가능한 정보를 정리해 출력한다.
- 값이 None이거나 응답에 없는 항목은 오류 없이 '정보 없음'으로 표시한다.
- API 요청이나 데이터 분석은 이 모듈에서 수행하지 않는다.
"""

class Dashboard:
    """Display Seoul real-time urban data."""

    def display(self, place, urban_data):
        print("\n" + "=" * 44)
        print("       SEOUL REAL-TIME URBAN DATA")
        print("=" * 44)

        area_name = getattr(place, "area_name", "정보 없음")
        congestion = getattr(urban_data, "congestion", "정보 없음")
        weather = getattr(urban_data, "weather", "정보 없음")

        print(f"\n[지역 정보]")
        print(f"지역 이름 : {area_name}")

        print("\n[실시간 도시 정보]")
        print(f"혼잡도    : {congestion}")
        print(f"날씨      : {weather}")

        print("\n" + "=" * 44)
        print("       데이터 조회가 완료되었습니다.")
        print("=" * 44 + "\n")
