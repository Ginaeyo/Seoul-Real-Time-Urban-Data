# 아키텍처 합의

이 문서는 현재 `src/` 구조와 Seoul Real-Time Urban Data 프로젝트를 기준으로 합니다. 첫 번째 목표는 샘플 데이터를 사용해 콘솔 프로그램을 처음부터 끝까지 실행하는 것입니다. 웹 화면은 기본 기능을 완성한 뒤 시간이 남으면 검토합니다.

## 프로그램 실행 흐름

`MainApp`이 전체 실행을 관리합니다.

1. `LocationSelector`가 `AreaManager`의 지역 목록을 보여 주고 사용자의 선택을 받습니다.
2. `AreaManager.get_area(index)`가 선택된 `Place` 객체를 반환합니다. 잘못된 입력이면 `None`을 반환합니다.
3. `SeoulAPI.get_data(place)`가 API 또는 샘플 데이터를 가져와 `UrbanData` 객체로 변환합니다.
4. `Dashboard.display(place, urban_data)`가 지역과 도시 정보를 출력합니다.
5. `DataAnalyzer.analyze_congestion(urban_data.congestion)`가 혼잡도 단계(1~4 또는 None)를 반환하고, `MainApp`이 `Dashboard.display_analysis()`에 전달하여 출력합니다.

## 클래스와 함수 규칙

- `Place`: `area_name`, `area_code`를 저장합니다. `get_info()`는 지역명과 코드를 담은 딕셔너리를 반환합니다.
- `AreaManager.show_areas() -> None`: 지역 목록을 번호와 함께 출력합니다.
- `AreaManager.get_area(index: int) -> Place | None`: 유효한 번호에 해당하는 `Place`를 반환하고, 범위를 벗어나면 `None`을 반환합니다.
- `LocationSelector.select_location(area_manager: AreaManager) -> Place | None`: 사용자 입력을 확인하고 선택된 `Place`를 반환합니다.
- `SeoulAPI.get_data(place: Place) -> UrbanData`: 지역 코드를 사용해 요청하고 결과를 `UrbanData`로 반환합니다.
- `SeoulAPI.get_data` 내부에서 실제 API 응답의 필요한 필드를 읽고 검증합니다.
- `UrbanData`: 현재 기본 필드는 `area_name`, `congestion`, `weather`입니다. 다른 필드는 API에서 실제 제공되는지 확인하고 팀이 합의한 뒤 추가합니다. 값이 없으면 `None`을 사용합니다.
- `DataAnalyzer.analyze_congestion(congestion: str | None) -> int | None`: 혼잡도 단계를 반환합니다. 값이 없거나 알 수 없으면 None을 반환합니다.
- `DataAnalyzer.compare_congestion(...)`: first_more, second_more, equal, unknown 중 하나의 비교 상태를 반환합니다. DataAnalyzer.compare_urban_data는 출처가 혼합된 경우 mixed_sources를 반환합니다. Dashboard가 문장으로 표현합니다.
- `congestion_levels.py`: 분석과 그래프가 공유하는 단계 정의 및 정규화 함수입니다.
- `SeoulAPI(api_key=None, fallback_provider=...)`: 대체 DataProvider를 생성자에서 반드시 주입합니다.
- `Dashboard.display(place: Place, urban_data: UrbanData) -> None`: 결과를 출력합니다. 값이 없거나 응답에서 빠진 항목은 오류 없이 “정보 없음”으로 표시합니다.
- `MainApp.run() -> None`: 지역 선택, 데이터 조회, 분석, 결과 출력 순서를 연결합니다.

## 데이터 공급 계약 및 의존성

- `DataProvider.get_data(place: Place) -> UrbanData`: 입력은 Place 객체, 반환은 UrbanData입니다. 잘못된 입력에는 TypeError를 발생시킵니다.
- `SeoulAPI`의 대체 공급자에게 원래 Place 객체를 그대로 전달합니다.
- `MainApp`의 협력 객체는 진입점에서 생성한 뒤 생성자에 주입합니다.
- 데이터 출처는 `UrbanData.data_source`로 판단합니다. 혼잡도 문자열의 접미사로 판단하지 않습니다.
- `DataAnalyzer.compare_urban_data`가 비교 가능 여부를 판단하고, `calculate_average_temperature`가 동일 출처의 두 유효 기온 평균을 계산합니다. Dashboard는 이를 차트에 전달합니다.
- `area_code`는 확인된 API 코드만 사용합니다.

## API 및 샘플 모드

- API 키가 필요하면 환경 변수에서 읽습니다. 실제 키를 코드, README, 테스트 파일에 넣거나 GitHub에 올리지 않습니다.
- HTTP 요청에는 timeout을 설정하고 네트워크 오류, 실패 응답, JSON 파싱 오류를 처리합니다.
- API를 사용할 수 없거나 키가 없어도 외부 네트워크 없이 샘플 데이터로 시연하고 테스트할 수 있어야 합니다.
- 샘플 데이터는 확인된 필드의 예시 값만 포함합니다. API가 제공하지 않는 정보를 실제 데이터처럼 만들어 표시하지 않습니다.
- API 연결에는 `requests`, 테스트에는 `pytest`를 사용합니다. 첫 번째 콘솔 버전에는 Streamlit, Plotly, pandas가 필요하지 않습니다.

## 변경 규칙

함수 이름, 인자, 반환 형식 또는 데이터 필드를 바꾸기 전에 관련 담당자에게 알리고 팀에서 합의합니다. 합의한 내용에 맞춰 이 문서도 함께 수정합니다. 테스트는 가짜 응답을 사용해 외부 네트워크 없이 실행합니다.

## SeoulAPI SRP 책임 재분배
SeoulAPI/SampleDataProvider → UrbanData(원본 인구 범위, 숫자 기온, 출처, 대체 사유) → MainApp이 DataAnalyzer에 계산 요청 → Dashboard에 분석값 전달 → 콘솔 및 차트 표현. JSON 파싱은 API 공급 책임에 포함하며 새 클래스는 추가하지 않는다. 혼잡도 샘플 표시와 fallback 객체 생성 규약은 아래 추가 개선을 따른다.
