"""선택 지역과 실시간 도시 정보를 콘솔에 표시하는 모듈.

TODO(담당: 원미혜 / 데이터 필드 협의: 민경환)
- display(place, urban_data)에서 지역명, 혼잡도, 날씨와 사용 가능한 정보를 정리해 출력한다.
- 값이 None이거나 응답에 없는 항목은 오류 없이 '정보 없음'으로 표시한다.
- API 요청이나 데이터 분석은 이 모듈에서 수행하지 않는다.
"""

MISSING = "정보 없음"

# 서울시 실시간 도시데이터의 혼잡도 단계 (AREA_CONGEST_LVL)
CONGESTION_LEVELS = ["여유", "보통", "약간 붐빔", "붐빔"]


class Dashboard:

    WIDTH = 44

    # main.py가 호출하는 팀 합의 메서드.
    def display(self, place, urban_data):
        self.display_dashboard(place, urban_data)

    def display_dashboard(self, place, urban_data):
        self._print_line("=")
        print("       SEOUL REAL-TIME URBAN DATA")
        self._print_line("=")

        # API 키가 없거나 요청이 실패하면 urban_data가 None으로 들어온다.
        if urban_data is None:
            print("도시 데이터를 불러오지 못했습니다.")
            print("API 인증키나 네트워크 상태를 확인하세요.")
            self._print_line("-")

        self.show_area(place, urban_data)
        self.show_population(urban_data)
        self.show_weather(urban_data)

        self._print_line("=")
        print("       데이터 조회가 완료되었습니다.")
        self._print_line("=")
        print()

    def show_area(self, place, urban_data):
        # Place 객체 -> 지역명 문자열 -> UrbanData의 지역명 순서로 찾는다.
        name = getattr(place, "area_name", None)
        if name is None and isinstance(place, str):
            name = place
        if name is None:
            name = getattr(urban_data, "area_name", None)

        print(f"[지역]   {self._text(name)}")

    def show_population(self, urban_data):
        congestion = self._text(getattr(urban_data, "congestion", None))
        print(f"[혼잡도] {congestion}")

        # 알려진 단계일 때만 게이지를 함께 보여준다. 예: [###-] 3/4 단계
        if congestion in CONGESTION_LEVELS:
            level = CONGESTION_LEVELS.index(congestion) + 1
            total = len(CONGESTION_LEVELS)
            bar = "#" * level + "-" * (total - level)
            print(f"         [{bar}] {level}/{total} 단계")

    def show_weather(self, urban_data):
        weather = getattr(urban_data, "weather", None)
        print(f"[기온]   {self._temperature(weather)}")

    def _temperature(self, value):
        # 숫자로 바꿀 수 있으면 °C 단위를 붙이고, 아니면 그대로 보여준다.
        if self._is_missing(value):
            return MISSING
        try:
            return f"{float(value):.1f}°C"
        except (TypeError, ValueError):
            return str(value)

    def _text(self, value):
        return MISSING if self._is_missing(value) else str(value)

    def _is_missing(self, value):
        # None, 빈 문자열, "정보 없음"은 모두 값이 없는 것으로 본다.
        return value is None or str(value).strip() in ("", MISSING)

    def _print_line(self, char):
        print(char * self.WIDTH)