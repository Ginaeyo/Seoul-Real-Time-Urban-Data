# 아키텍처 합의

이 문서는 현재 `src/` 구조와 Seoul Real-Time Urban Data 프로젝트를 기준으로 합니다. 첫 번째 목표는 샘플 데이터를 사용해 콘솔 프로그램을 처음부터 끝까지 실행하는 것입니다. 웹 화면은 기본 기능을 완성한 뒤 시간이 남으면 검토합니다.

## 프로그램 실행 흐름

`MainApp`이 전체 실행을 관리합니다.

1. `LocationSelector`가 `AreaManager`의 지역 목록을 보여 주고 사용자의 선택을 받습니다.
2. `AreaManager.get_area(index)`가 선택된 `Place` 객체를 반환합니다. 잘못된 입력이면 `None`을 반환합니다.
3. `SeoulAPI.get_data(place)`가 API 또는 샘플 데이터를 가져와 `UrbanData` 객체로 변환합니다.
4. `Dashboard.display(place, urban_data)`가 지역과 도시 정보를 출력합니다.
5. `DataAnalyzer.analyze_congestion(urban_data.congestion)`가 혼잡도 설명을 반환하고, `MainApp`이 그 결과를 출력합니다.

## 클래스와 함수 규칙

- `Place`: `area_name`, `area_code`를 저장합니다. `get_info()`는 지역명과 코드를 담은 딕셔너리를 반환합니다.
- `AreaManager.show_areas() -> None`: 지역 목록을 번호와 함께 출력합니다.
- `AreaManager.get_area(index: int) -> Place | None`: 유효한 번호에 해당하는 `Place`를 반환하고, 범위를 벗어나면 `None`을 반환합니다.
- `LocationSelector.select_location(area_manager: AreaManager) -> Place | None`: 사용자 입력을 확인하고 선택된 `Place`를 반환합니다.
- `SeoulAPI.get_data(place: Place) -> UrbanData`: 지역 코드를 사용해 요청하고 결과를 `UrbanData`로 반환합니다.
- `SeoulAPI.parse_response(payload: dict, place: Place) -> UrbanData`: 실제 API 응답에서 필요한 필드를 읽습니다.
- `UrbanData`: 현재 기본 필드는 `area_name`, `congestion`, `weather`입니다. 다른 필드는 API에서 실제 제공되는지 확인하고 팀이 합의한 뒤 추가합니다. 값이 없으면 `None`을 사용합니다.
- `DataAnalyzer.analyze_congestion(congestion: str | None) -> str`: 혼잡도 설명을 반환합니다. 값이 없거나 알 수 없으면 안내 문구를 반환합니다.
- `Dashboard.display(place: Place, urban_data: UrbanData) -> None`: 결과를 출력합니다. 값이 없거나 응답에서 빠진 항목은 오류 없이 “정보 없음”으로 표시합니다.
- `MainApp.run() -> None`: 지역 선택, 데이터 조회, 분석, 결과 출력 순서를 연결합니다.

## 현재 코드에서 통일할 부분

현재 `AreaManager.get_area()`는 지역명을 문자열로 반환하지만 `Dashboard.display()`는 `place.area_name`을 사용합니다. 첫 버전부터 `Place` 객체를 사용하는 방식으로 통일합니다.

- 김효중은 `AreaManager.get_area()`가 `Place`를 반환하도록 수정합니다.
- 할리오나는 `SeoulAPI.get_data()`가 문자열 대신 `Place`를 받도록 수정합니다. 실제 API 요청에는 `place.area_code`를 사용하고, 샘플 조회에는 `place.area_name`을 사용합니다.
- 민경환은 `Place`, `UrbanData`, `MainApp`을 이 인터페이스에 맞춥니다.
- 원미혜는 `Dashboard`에서 `Place`와 `UrbanData`의 합의된 필드를 사용합니다.

`area_code`는 Seoul API에서 확인된 코드여야 합니다. 코드 목록을 확인하기 전에는 실제 API 요청에 사용하지 않습니다. 샘플 모드에서는 테스트용 코드를 사용할 수 있습니다.

## API 및 샘플 모드

- API 키가 필요하면 환경 변수에서 읽습니다. 실제 키를 코드, README, 테스트 파일에 넣거나 GitHub에 올리지 않습니다.
- HTTP 요청에는 timeout을 설정하고 네트워크 오류, 실패 응답, JSON 파싱 오류를 처리합니다.
- API를 사용할 수 없거나 키가 없어도 외부 네트워크 없이 샘플 데이터로 시연하고 테스트할 수 있어야 합니다.
- 샘플 데이터는 확인된 필드의 예시 값만 포함합니다. API가 제공하지 않는 정보를 실제 데이터처럼 만들어 표시하지 않습니다.
- API 연결에는 `requests`, 테스트에는 `pytest`를 사용합니다. 첫 번째 콘솔 버전에는 Streamlit, Plotly, pandas가 필요하지 않습니다.

## 변경 규칙

함수 이름, 인자, 반환 형식 또는 데이터 필드를 바꾸기 전에 관련 담당자에게 알리고 팀에서 합의합니다. 합의한 내용에 맞춰 이 문서도 함께 수정합니다. 테스트는 가짜 응답을 사용해 외부 네트워크 없이 실행합니다.
