"""프로그램 실행 흐름을 연결하는 진입점.

TODO(담당: 민경환 / 통합 협력: 에르덴자야)
- 지역 선택, SeoulAPI 데이터 조회, 대시보드 출력, 혼잡도 분석 흐름을 연결한다.
- Place 객체를 사용하도록 각 모듈의 입력과 반환 형식을 맞춘다.
- 잘못된 지역 선택이나 API 오류가 발생해도 사용자에게 안내한다.
"""

"""AreaManager, LocationSelector, DataAnalyzer 연동 테스트용 Main.
실제 SeoulAPI를 호출하지 않으며, 예시용 가짜 Place/UrbanData만 사용합니다.
"""
import json
import tkinter as tk
from tkinter import ttk, messagebox

from AreaManager import AreaManager
from LocationSelector import LocationSelector
from DataAnalyzer import DataAnalyzer


class Place:
    """Place 담당 팀원의 클래스가 없는 동안 사용하는 테스트용 대체 클래스."""
    def __init__(self, area_name, area_code):
        self.area_name = area_name
        self.area_code = area_code

    def get_info(self):
        return {"area_name": self.area_name, "area_code": self.area_code}


class UrbanData:
    """UrbanData 담당 팀원의 클래스가 없는 동안 사용하는 테스트용 대체 클래스."""
    def __init__(self, population, weather, traffic, transit, culture_events):
        self.population = population
        self.weather = weather
        self.traffic = traffic
        self.transit = transit
        self.culture_events = culture_events


def make_fake_urban_data(area_code):
    """같은 지역 코드는 언제나 같은 가짜 데이터를 반환합니다 (API 요청 없음)."""
    sample_no = int(area_code.replace('TEST', ''))
    congestion = ('여유', '보통', '붐빔')[sample_no % 3]
    traffic_level = ('원활', '서행', '정체')[sample_no % 3]
    return UrbanData(
        population={"estimated_people": 8500 + sample_no * 900,
                    "congestion_level": congestion},
        weather={"temperature_c": 12.5 + sample_no,
                 "humidity_percent": 45 + sample_no * 3,
                 "condition": ('맑음', '흐림')[sample_no % 2]},
        traffic={"average_speed_kmh": 28 - sample_no,
                 "traffic_level": traffic_level},
        transit={"bus_arrival_minutes": 3 + sample_no,
                 "bike_available": 7 + sample_no * 2},
        culture_events={"event_count": sample_no % 4,
                        "events": [f"가상 문화행사 {sample_no}"] if sample_no % 4 else []},
    )


class Main:
    def __init__(self):
        # Tk 루트 창은 Main에서 단 한 번 생성합니다.
        self.root = tk.Tk()
        self.root.title('서울 실시간 도시데이터 - 클래스 연동 테스트')
        self.root.geometry('760x650')

        # TEST 코드는 공식 서울시 지역 코드가 아닙니다.
        areas = [
            Place('강남역', 'TEST001'),
            Place('홍대 관광특구', 'TEST002'),
            Place('명동 관광특구', 'TEST003'),
            Place('광화문광장', 'TEST004'),
            Place('여의도', 'TEST005'),
            Place('잠실 관광특구', 'TEST006'),
            Place('성수카페거리', 'TEST007'),
            Place('서울역', 'TEST008'),
        ]
        self.area_manager = AreaManager(areas)
        self.selector = LocationSelector(self.area_manager)
        self.analyzer = DataAnalyzer()
        self._build_ui()

    def _build_ui(self):
        frame = ttk.Frame(self.root, padding=18)
        frame.pack(fill='both', expand=True)
        ttk.Label(frame, text='서울 실시간 도시데이터 - 기능 테스트',
                  font=('맑은 고딕', 16, 'bold')).pack(anchor='w', pady=(0, 8))
        ttk.Label(frame, text='실제 API 미사용 · 예시 지역 8개 · 모든 수치는 가짜 데이터',
                  foreground='firebrick').pack(anchor='w', pady=(0, 14))

        buttons = ttk.Frame(frame)
        buttons.pack(fill='x', pady=(0, 12))
        ttk.Button(buttons, text='지역 하나 조회', command=self.load_area).pack(side='left', padx=(0, 8))
        ttk.Button(buttons, text='두 지역 비교', command=self.compare_selected_areas).pack(side='left', padx=(0, 8))
        ttk.Button(buttons, text='전체 지역 목록 출력', command=self.show_all_areas).pack(side='left')

        self.output = tk.Text(frame, font=('맑은 고딕', 10), wrap='word', state='disabled')
        self.output.pack(fill='both', expand=True)
        self._write('버튼을 눌러 세 클래스의 동작을 테스트하세요.\n'
                    '지역 선택 창에서 목록 클릭 또는 검색어 필터링을 사용할 수 있습니다.')

    def _write(self, text):
        self.output.config(state='normal')
        self.output.delete('1.0', tk.END)
        self.output.insert(tk.END, text)
        self.output.config(state='disabled')

    def show_all_areas(self):
        # AreaManager.show_areas()는 콘솔 출력용이므로 GUI에는 get_areas()를 사용합니다.
        areas = self.area_manager.get_areas()
        self._write('테스트 지역 목록\n\n' + '\n'.join(
            f'{p.area_code}. {p.area_name}' for p in areas))
        self.area_manager.show_areas()  # 터미널에서도 확인 가능

    def load_area(self):
        # LocationSelector가 Main의 root를 부모로 하는 선택 창을 띄웁니다.
        area_name = self.selector.search_location(parent=self.root)
        if area_name is None:
            self._write('지역 선택이 취소되었습니다.')
            return
        place = self.area_manager.get_area(area_name)
        if place is None:
            messagebox.showerror('조회 오류', '선택한 지역을 찾지 못했습니다.', parent=self.root)
            return
        data = make_fake_urban_data(place.area_code)
        details = {
            'place': place.get_info(),
            'population': self.analyzer.prepare_population(data),
            'weather': self.analyzer.prepare_weather(data),
            'traffic': self.analyzer.prepare_traffic(data),
            'transit': self.analyzer.prepare_transit(data),
            'culture_events': self.analyzer.prepare_culture_events(data),
        }
        self._write('지역 단일 조회 결과 (가짜 데이터)\n\n' + json.dumps(
            details, ensure_ascii=False, indent=2))

    def compare_selected_areas(self):
        # 기존 LocationSelector의 지역 선택 UI를 두 번 재사용합니다.
        names = self.selector.select_comparison_areas(parent=self.root)
        if names is None:
            self._write('지역 비교가 취소되었습니다.')
            return
        first, second = (self.area_manager.get_area(name) for name in names)
        if first is None or second is None:
            messagebox.showerror('비교 오류', '선택한 지역을 찾지 못했습니다.', parent=self.root)
            return
        first_data = make_fake_urban_data(first.area_code)
        second_data = make_fake_urban_data(second.area_code)
        try:
            result = self.analyzer.compare_areas(
                first_data, second_data, first.area_name, second.area_name)
        except ValueError as exc:
            messagebox.showerror('비교 오류', str(exc), parent=self.root)
            return
        self._write('두 지역 비교 결과 (가짜 데이터)\n'
                    'numeric_differences = 첫 번째 지역 - 두 번째 지역\n\n'
                    + json.dumps(result, ensure_ascii=False, indent=2))

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    Main().run()
