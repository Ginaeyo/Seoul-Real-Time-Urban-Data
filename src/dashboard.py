
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
