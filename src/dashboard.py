"""선택 지역과 실시간 도시 정보를 콘솔에 표시하는 모듈.

TODO(담당: 원미혜 / 데이터 필드 협의: 민경환)
- display(place, urban_data)에서 지역명, 혼잡도, 날씨와 사용 가능한 정보를 정리해 출력한다.
- 값이 None이거나 응답에 없는 항목은 오류 없이 '정보 없음'으로 표시한다.
- API 요청이나 데이터 분석은 이 모듈에서 수행하지 않는다.
"""


from congestion_chart import is_sample_congestion

MISSING = "정보 없음"


class Dashboard:

    WIDTH = 44

    # main.py가 호출하는 팀 합의 메서드.
    def display(self, place, urban_data):
        self.display_dashboard(place, urban_data)

    def display_dashboard(self, place, urban_data):
        self._print_line("=")
        print("       서울 도시데이터")
        self._print_line("=")

        if urban_data is None:
            print("도시 데이터를 불러오지 못했습니다.")
            print("API 인증키나 네트워크 상태를 확인하세요.")
            self._print_line("-")

        if is_sample_congestion(getattr(urban_data, "congestion", None)):
            print("※ 시연 데이터입니다. 실제 API 값이 아닙니다.")

        self.show_area(place, urban_data)
        self.show_population(urban_data)
        self.show_weather(urban_data)
        self.show_traffic(urban_data)
        updated_at = getattr(urban_data, "updated_at", None)
        if not self._is_missing(updated_at):
            print(f"[갱신 시각] {updated_at}")

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
        population = getattr(urban_data, "population", None)
        if not self._is_missing(population):
            print(f"[인구]   {population}")

    def show_weather(self, urban_data):
        weather = getattr(urban_data, "weather", None)
        print(f"[기온]   {self._temperature(weather)}")

    def show_traffic(self, urban_data):
        value = getattr(urban_data, "traffic", None) or MISSING
        note = " (샘플)" if getattr(urban_data, "traffic_sample", False) else ""
        print(f"[도로 교통] {value}{note}")

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
