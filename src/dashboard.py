"""선택 지역과 실시간 도시 정보를 콘솔에 표시하는 모듈.

TODO(담당: 원미혜 / 데이터 필드 협의: 민경환)
- display(place, urban_data)에서 지역명, 혼잡도, 날씨와 사용 가능한 정보를 정리해 출력한다.
- 값이 None이거나 응답에 없는 항목은 오류 없이 '정보 없음'으로 표시한다.
- API 요청이나 데이터 분석은 이 모듈에서 수행하지 않는다.
"""

from unicodedata import east_asian_width

from congestion_chart import is_sample_congestion, parse_temperature

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
        print("       서울 실시간 도시데이터")
        self._print_line("=")

        if urban_data is None:
            print("도시 데이터를 불러오지 못했습니다.")
            print("API 인증키나 네트워크 상태를 확인하세요.")
            self._print_line("-")

        self.show_area(place, urban_data)
        self.show_population(urban_data)
        self.show_weather(urban_data)
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

        # 알려진 단계일 때만 게이지를 함께 보여준다. 예: [###-] 3/4 단계
        level_name = congestion.removesuffix(" (샘플)").strip()
        if level_name in CONGESTION_LEVELS:
            level = CONGESTION_LEVELS.index(level_name) + 1
            total = len(CONGESTION_LEVELS)
            bar = "#" * level + "-" * (total - level)
            print(f"         [{bar}] {level}/{total} 단계")

    def show_weather(self, urban_data):
        weather = getattr(urban_data, "weather", None)
        print(f"[기온]   {self._temperature(weather)}")

    def display_overview(self, rows):
        """Print the all-area overview using API fields without inventing measurements."""
        def print_row(name, population, congestion, level, weather):
            columns = []
            for value, width in zip((name, population, congestion, level), (24, 26, 16, 8)):
                cells = sum(2 if east_asian_width(char) in ("F", "W") else 1 for char in value)
                columns.append(value + " " * max(2, width - cells))
            print("".join(columns) + weather)

        print("\n실시간 대시보드")
        print_row("지역", "인구", "혼잡도", "단계", "기온")
        print("-" * 82)
        indexed = []
        temps = []
        sources = set()
        for place, data in rows:
            name = getattr(place, "area_name", str(place))
            raw = getattr(data, "congestion", None) or ""
            sample = is_sample_congestion(raw)
            sources.add(sample)
            if sample:
                name += " (시연)"
            clean = str(raw).removesuffix(" (샘플)").strip()
            level = CONGESTION_LEVELS.index(clean) + 1 if clean in CONGESTION_LEVELS else None
            index = level * 25 if level else None
            population = getattr(data, "population", None) or MISSING
            weather = self._temperature(getattr(data, "weather", None))
            temperature = parse_temperature(weather)
            if temperature is not None:
                temps.append(temperature)
            print_row(name, str(population), clean or MISSING, f"{level}/4" if level else "--", weather)
            bar = "█" * (index // 5) + "░" * (20 - index // 5) if index else "데이터 없음"
            print(f"  혼잡 단계 지수  {bar}  {f'{index}/100' if index else MISSING} (단계 기준)")
            if level:
                indexed.append((name, level))
        if len(sources) > 1:
            print("\n실시간 데이터와 시연 데이터의 혼잡도 순위 및 평균 기온은 계산하지 않습니다.")
        else:
            if indexed:
                highest = max(indexed, key=lambda item: item[1])
                lowest = min(indexed, key=lambda item: item[1])
                print("\n주요 정보")
                print(f"• 혼잡도가 가장 높은 지역: {highest[0]} (혼잡 단계 {highest[1]}/4)")
                print(f"• 혼잡도가 가장 낮은 지역: {lowest[0]} (혼잡 단계 {lowest[1]}/4)")
            if temps:
                print(f"• 평균 기온: {sum(temps) / len(temps):.1f}°C")
        print("\n인구는 API 인구 범위의 중간값입니다. 혼잡 지수는 API의 4단계를 바탕으로 계산했으며, API가 제공하는 백분율이 아닙니다.")
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
