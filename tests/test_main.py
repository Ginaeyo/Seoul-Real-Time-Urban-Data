import importlib
import os
import sys
import types

import pytest

# tests/ 폴더에서 실행해도 src/ 안의 모듈을 import 할 수 있게 경로를 추가한다.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from place import Place
from urban_data import UrbanData


# ---- 가짜(Fake) 클래스: 다른 팀원 코드와 상관없이 MainApp 흐름만 확인하기 위한 대역 ----

class FakeAreaManager:
    """지역 목록 관리 대역 (MainApp 은 이 객체를 그대로 전달만 한다)."""


class FakeLocationSelector:
    """미리 정해 둔 result 를 돌려주는 가짜 지역 선택기."""
    result = None

    def select_location(self, area_manager):
        return self.result


class FakeSeoulAPI:
    """미리 정해 둔 result 를 돌려주는 가짜 API. 전달받은 지역을 received 에 기록한다."""
    result = None
    received = None

    def get_data(self, area):
        self.received = area
        return self.result


class FakeDataAnalyzer:
    """혼잡도 값을 '분석:값' 형태로 돌려주는 가짜 분석기."""

    def analyze_congestion(self, congestion):
        return f"분석:{congestion}"


class FakeDashboard:
    """display() 에 전달된 값을 기록만 하는 가짜 대시보드."""
    shown = None

    def display(self, place, urban_data):
        self.shown = (place, urban_data)


@pytest.fixture
def app(monkeypatch):
    """가짜 모듈로 대체한 상태에서 MainApp 객체를 만들어 돌려준다.

    main.py 가 import 하는 5개 모듈을 가짜로 바꾸므로, seoul_api.py 등
    다른 팀원 파일이 아직 완성되지 않았거나 오류가 있어도 이 테스트는 실행된다.
    monkeypatch 가 테스트가 끝나면 원래 모듈 상태로 되돌려 준다.
    """
    fakes = {
        "area_manager": ("AreaManager", FakeAreaManager),
        "location_selector": ("LocationSelector", FakeLocationSelector),
        "seoul_api": ("SeoulAPI", FakeSeoulAPI),
        "data_analyzer": ("DataAnalyzer", FakeDataAnalyzer),
        "dashboard": ("Dashboard", FakeDashboard),
    }
    for module_name, (class_name, fake_class) in fakes.items():
        fake_module = types.ModuleType(module_name)
        setattr(fake_module, class_name, fake_class)
        monkeypatch.setitem(sys.modules, module_name, fake_module)

    # 가짜 모듈이 적용된 상태로 main 을 새로 import 한다.
    sys.modules.pop("main", None)
    main = importlib.import_module("main")

    yield main.MainApp()

    sys.modules.pop("main", None)


# ---- 테스트 ----

def test_full_flow(app, capsys):
    """지역 선택 → 조회 → 대시보드 → 분석 출력이 한 흐름으로 동작하는지 확인한다."""
    place = Place("강남역", "TEST001")
    data = UrbanData("강남역", "붐빔", "맑음")
    app.location_selector.result = place
    app.api.result = data

    app.run()

    assert app.api.received is place                 # 선택한 Place 가 API 로 전달됨
    assert app.dashboard.shown == (place, data)      # 대시보드가 같은 값을 받음
    assert "분석:붐빔" in capsys.readouterr().out     # 혼잡도 분석 결과가 출력됨


def test_invalid_selection_shows_message(app, capsys):
    """잘못된 지역 선택(None)이면 안내 후 조회 없이 끝나는지 확인한다."""
    app.location_selector.result = None

    app.run()

    assert "잘못된 입력입니다." in capsys.readouterr().out
    assert app.api.received is None      # API 를 호출하지 않음
    assert app.dashboard.shown is None   # 출력하지 않음


def test_api_returns_none_does_not_crash(app, capsys):
    """API 결과가 None 이어도 오류 없이 안내만 하고 끝나는지 확인한다."""
    app.location_selector.result = Place("강남역", "TEST001")
    app.api.result = None

    app.run()

    assert "도시 데이터를 가져오지 못했습니다." in capsys.readouterr().out
    assert app.dashboard.shown is None   # 대시보드 출력까지 가지 않음


def test_missing_congestion_still_runs(app, capsys):
    """혼잡도 값이 None 이어도 흐름이 끝까지 진행되는지 확인한다."""
    place = Place("강남역", "TEST001")
    data = UrbanData("강남역", None, None)
    app.location_selector.result = place
    app.api.result = data

    app.run()

    assert app.dashboard.shown == (place, data)
    assert "분석:None" in capsys.readouterr().out
