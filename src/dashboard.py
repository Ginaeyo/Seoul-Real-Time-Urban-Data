"""선택 지역과 실시간 도시 정보를 콘솔에 표시하는 모듈.

TODO(담당: 원미혜 / 데이터 필드 협의: 민경환)
- display(place, urban_data)에서 지역명, 혼잡도, 날씨와 사용 가능한 정보를 정리해 출력한다.
- 값이 None이거나 응답에 없는 항목은 오류 없이 '정보 없음'으로 표시한다.
- API 요청이나 데이터 분석은 이 모듈에서 수행하지 않는다.
"""


from congestion_chart import plot_area_dashboard, plot_congestion_comparison

from congestion_levels import FIRST_MORE, SECOND_MORE, EQUAL, MIXED_SOURCES

MISSING = "정보 없음"


class Dashboard:

    WIDTH = 44

    def show_title(self):
        self._print_line("=")
        print("서울 인구·날씨 대시보드")
        self._print_line("=")

    def show_menu(self):
        print("\n1. 지역 정보 조회")
        print("2. 두 지역 혼잡도 비교 (그래프)")
        print("3. 종료")

    def show_message(self, message):
        print(message)

    def display_analysis(self, result):
        messages = {
            1: "현재 여유로운 상태입니다.",
            2: "현재 보통 수준입니다.",
            3: "현재 다소 혼잡합니다.",
            4: "현재 매우 혼잡합니다.",
        }
        print(messages.get(result, "정보가 없습니다."))

    def display_comparison(self, first_area, first_data, second_area, second_data, result, *, first_midpoint=None, second_midpoint=None):
        first_sample = first_data.data_source == "sample"
        second_sample = second_data.data_source == "sample"
        first_source = "시연" if first_sample else "실시간"
        second_source = "시연" if second_sample else "실시간"
        print(f"\n=== 첫 번째 지역 ({first_source}) ===")
        self.display(first_area, first_data, midpoint=first_midpoint)
        print(f"\n=== 두 번째 지역 ({second_source}) ===")
        self.display(second_area, second_data, midpoint=second_midpoint)
        print("\n=== 혼잡도 비교 결과 ===")
        if result == MIXED_SOURCES:
            print("실시간 데이터와 시연 데이터의 혼잡도 순위는 비교하지 않습니다.")
        elif result == FIRST_MORE:
            print(f"{first_area.area_name}이(가) {second_area.area_name}보다 혼잡합니다.")
        elif result == SECOND_MORE:
            print(f"{second_area.area_name}이(가) {first_area.area_name}보다 혼잡합니다.")
        elif result == EQUAL:
            print("두 지역의 혼잡도는 같습니다.")
        else:
            print("혼잡도를 비교할 수 없습니다.")

    def display_area_chart(self, area, urban_data, *, midpoint=None):
        try:
            image_path = plot_area_dashboard(
                area.area_name, urban_data.congestion, getattr(urban_data, "weather", None),
                traffic=getattr(urban_data, "traffic", None),
                population=midpoint if midpoint is not None else getattr(urban_data, "population", None),
                rain_chance=getattr(urban_data, "rain_chance", None),
                dust_status=getattr(urban_data, "dust_status", None),
                data_source=urban_data.data_source,
            )
            print(f"상세 대시보드 저장 위치: {image_path}")
        except ImportError:
            print("시각화 기능을 사용하려면 matplotlib를 설치하세요: pip install matplotlib")
        except OSError:
            print("상세 대시보드 이미지를 저장할 수 없습니다.")

    def display_comparison_chart(self, first_area, first_data, second_area, second_data, *, first_midpoint=None, second_midpoint=None, average_temperature=None):
        try:
            chart_path = plot_congestion_comparison(
                first_area.area_name, first_data.congestion, second_area.area_name, second_data.congestion,
                getattr(first_data, "weather", None), getattr(second_data, "weather", None),
                first_data_source=first_data.data_source,
                second_data_source=second_data.data_source,
                average_temperature=average_temperature,
                first_traffic=getattr(first_data, "traffic", None),
                second_traffic=getattr(second_data, "traffic", None),
                first_population=first_midpoint if first_midpoint is not None else getattr(first_data, "population", None),
                second_population=second_midpoint if second_midpoint is not None else getattr(second_data, "population", None),
                first_environment=(getattr(first_data, "rain_chance", None),
                                   getattr(first_data, "dust_status", None)),
                second_environment=(getattr(second_data, "rain_chance", None),
                                    getattr(second_data, "dust_status", None)),
            )
            print(f"그래프 저장 위치: {chart_path}")
        except ImportError:
            print("그래프 기능을 사용하려면 matplotlib를 설치하세요: pip install matplotlib")
        except OSError:
            print("비교 그래프 이미지를 저장할 수 없습니다.")
        except ValueError as error:
            print(f"그래프를 표시할 수 없습니다: {error}")


    # main.py가 호출하는 팀 합의 메서드.
    def display(self, place, urban_data, *, midpoint=None):
        self.display_dashboard(place, urban_data, midpoint=midpoint)

    def display_dashboard(self, place, urban_data, *, midpoint=None):
        self._print_line("=")
        print("       서울 도시데이터")
        self._print_line("=")

        if urban_data is None:
            print("도시 데이터를 불러오지 못했습니다.")
            print("API 인증키나 네트워크 상태를 확인하세요.")
            self._print_line("-")
            return

        reason = getattr(urban_data, "fallback_reason", None)
        messages = {
            "missing_api_key": "API 키가 없어 샘플 모드로 실행합니다.",
            "invalid_response": "API 응답 형식이 올바르지 않습니다.",
            "api_status_error": "API가 도시 데이터를 반환하지 않았습니다.",
            "missing_city_data": "도시 데이터를 찾을 수 없습니다.",
            "missing_readings": "도시 데이터에 인구와 날씨 정보가 없습니다.",
            "request_failed": "API 요청에 실패했습니다. 연결 상태와 인증키를 확인하세요.",
        }
        if reason in messages:
            print(messages[reason])
        if getattr(urban_data, "data_source", None) == "sample":
            print("※ 시연 데이터입니다. 실제 API 값이 아닙니다.")

        self.show_area(place, urban_data)
        self.show_population(urban_data, midpoint=midpoint)
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

    def show_population(self, urban_data, *, midpoint=None):
        congestion = self._text(getattr(urban_data, "congestion", None))
        print(f"[혼잡도] {congestion}")
        population = getattr(urban_data, "population", None)
        if midpoint is not None:
            print(f"[인구]   {midpoint:,}명 (범위 중간값)")
        elif not self._is_missing(population):
            print(f"[인구]   {population}")
        else:
            print(f"[인구]   {MISSING}")

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
