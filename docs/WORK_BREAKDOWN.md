# 파일별 업무 분담

이 문서는 현재 `src/` 코드와 Seoul Real-Time Urban Data 프로젝트 목표에 맞춘 팀 업무 계획입니다. 팀원은 담당 파일을 중심으로 작업하고, 다른 사람의 파일을 수정해야 하면 먼저 공유해 주세요.

## 팀 공통 인터페이스

첫 버전은 OOP 구조로 통일합니다.

- `AreaManager.get_area(index) -> Place | None`: 유효한 번호면 `Place` 객체를, 잘못된 번호면 `None`을 반환합니다.
- `LocationSelector.select_location(area_manager) -> Place | None`: 사용자가 선택한 `Place` 객체를 반환합니다.
- `SeoulAPI.get_data(place) -> UrbanData`: 선택한 `Place`의 실제 API 또는 샘플 데이터를 `UrbanData`로 반환합니다.
- `DataAnalyzer.analyze_congestion(congestion) -> str`: 혼잡도 설명을 반환합니다.
- `Dashboard.display(place, urban_data) -> None`: 지역과 도시 정보를 출력합니다.

`Place`의 `area_name`, `area_code`와 `UrbanData`의 필드명은 `docs/architecture.md`에 적힌 규칙을 따릅니다. 이 형식을 바꾸려면 관련 담당자에게 먼저 알리고 연결된 코드를 함께 수정합니다.

## 담당자별 업무

### 에르덴자야 (Ginaeyo) — 팀장·프로젝트 관리·문서·최종 검토

- `README.md`: 프로젝트 소개, 설치 및 실행 방법, 샘플 데이터 사용법, 테스트 방법을 정리합니다.
- `.gitignore`: `.env`, `__pycache__/`, `*.py[cod]`, `.venv/` 등 개인 환경 파일을 제외합니다.
- `.github/workflows/tests.yml`: PR마다 pytest가 실행되도록 GitHub Actions를 설정합니다.
- `docs/architecture.md`: 팀에서 합의한 클래스·함수·데이터 규칙을 관리합니다.
- PR을 확인하고 리뷰어를 지정해 11/1에 병합을 진행합니다. 팀원별 화면 캡처와 수행 내용을 모아 보고서를 최종 확인하고 11/2 제출을 준비합니다.
- 민경환이 통합한 `src/main.py`를 샘플 데이터로 실행해 전체 흐름을 확인합니다.

### 할리오나 (Liuka0715) — `SeoulAPI`, API 연동 및 실시간 데이터 수집

- `src/seoul_api.py`: `get_data(place)`에서 서울 실시간 도시데이터 API를 호출하고, 응답을 `UrbanData` 객체로 변환합니다.
- `place.area_code`를 API 요청에 사용하고 `place.area_name`을 결과 데이터에 포함합니다.
- 요청 timeout, HTTP 오류, JSON 파싱 오류와 필수 값 누락을 처리합니다.
- API 키가 필요한 경우 환경 변수에서 읽습니다. 실제 키를 코드, README, 테스트 파일에 넣지 않습니다.
- API 연결이 안 되어도 가짜 샘플 데이터로 기능을 확인할 수 있게 합니다.
- `requirements.txt`에서 `requests`를 확인하고, 없을 때만 추가합니다.
- `tests/test_seoul_api.py`에 샘플 응답 파싱과 오류 처리 테스트를 작성합니다. 테스트는 인터넷에 접속하지 않습니다.

### 민경환 (Kimmolang11) — `Place`, `UrbanData`, `MainApp`; 데이터 구조와 실행 흐름 통합

- `src/place.py`: 지역명과 API 지역 코드를 저장하는 `Place` 클래스를 정리합니다. `get_info()`의 반환 형식을 일관되게 합니다.
- `src/urban_data.py`: 현재 필요한 `area_name`, `congestion`, `weather`를 저장하고, API가 실제 제공하는 경우에만 추가 필드를 팀과 합의해 넣습니다.
- `src/main.py`: 지역 선택 → 데이터 조회 → 대시보드 출력 → 혼잡도 분석 결과 출력 순서를 연결합니다.
- `AreaManager`와 `SeoulAPI`가 `Place` 객체를 주고받도록 김효중, 할리오나와 인터페이스를 맞춥니다.
- `tests/test_models.py`가 필요하면 `Place`와 `UrbanData` 생성 및 필드 테스트를 추가합니다.

### 원미혜 (Today0505) — `Dashboard`; 사용자 인터페이스와 결과 출력

- `src/dashboard.py`: `Place`와 `UrbanData`를 받아 지역명, 혼잡도, 날씨와 사용 가능한 도시 정보를 읽기 쉽게 출력합니다.
- 일부 데이터가 `None`이거나 누락되어도 프로그램이 중단되지 않도록 하고, 해당 항목에는 “정보 없음”을 표시합니다.
- `UrbanData`의 필드명과 출력 내용을 민경환과 먼저 맞춥니다.
- `tests/test_dashboard.py`에서 출력 결과와 누락 정보 표시를 확인합니다. API나 네트워크를 호출하지 않습니다.
- 샘플 데이터 실행 화면을 캡처해 11/1까지 공유합니다.

### 김효중 (a01056405156-ctrl) — `AreaManager`, `LocationSelector`, `DataAnalyzer`; 지역 관리·선택·분석

- `src/area_manager.py`: 지원 지역 목록을 관리하고, 번호로 조회하면 `Place` 객체를 반환하며 잘못된 번호에는 `None`을 반환합니다.
- `src/location_selector.py`: 지역 목록을 보여 주고 번호 선택을 받습니다. 숫자가 아닌 입력과 범위를 벗어난 번호를 안전하게 처리합니다.
- `src/data_analyzer.py`: 혼잡도 값별로 이해하기 쉬운 설명을 반환하고, 알 수 없는 값에는 안내 문구를 반환합니다.
- `tests/test_area_manager.py`와 `tests/test_data_analyzer.py`에 정상 입력, 잘못된 입력, 알 수 없는 혼잡도 테스트를 작성합니다.
- `Place`의 지역명과 지역 코드 목록을 민경환, 할리오나와 맞춥니다. 확인되지 않은 API 코드를 임의로 만들지 않습니다.

## 테스트·문서·이미지 파일

- `tests/test_area_manager.py`, `tests/test_data_analyzer.py`: 김효중 담당.
- `tests/test_seoul_api.py`: 할리오나 담당.
- `tests/test_dashboard.py`: 원미혜 담당.
- `tests/test_models.py`와 `src/main.py` 통합: 민경환 담당.
- `.github/workflows/tests.yml`, README, 전체 PR·보고서 관리: 에르덴자야 담당.
- `images/`: 각자 작업 화면 또는 실행 결과 캡처 1~2장을 11/1까지 에르덴자야에게 전달합니다.

## 완료 기준

- API 키가 없어도 샘플 데이터로 `python src/main.py`를 실행할 수 있습니다.
- 지역 선택, 데이터 조회, 결과 출력까지 한 흐름으로 동작합니다.
- 잘못된 지역 입력에도 프로그램이 갑자기 종료되지 않고 안내 메시지를 보여 줍니다.
- API에서 제공하지 않는 값은 임의로 만들지 않고 “정보 없음”으로 표시합니다.
- 담당 기능에 대한 테스트 또는 재현 가능한 수동 확인 방법이 있습니다.
- PR에는 변경 내용, 실행/테스트 방법, 필요한 화면 캡처가 포함되고 팀원 한 명의 리뷰를 받습니다.
- API 키와 개인정보가 커밋되지 않았습니다.

## 일정

- **10/30(금):** `Place` 반환 방식, 데이터 필드와 함수 규칙을 확정하고 각자 `feature/작업명` 브랜치를 만듭니다.
- **10/31(토):** 각자 담당 기능과 간단한 테스트를 완료해 PR을 올립니다. API 연결을 기다리지 말고 샘플 데이터로 개발합니다.
- **11/1(일):** 서로 PR을 검토하고 승인 후 병합합니다. 통합 실행, 화면 캡처, 보고서용 수행 내용 2~3문장을 모읍니다.
- **11/2(월) 오전:** 보고서를 마무리합니다. 팀장은 18:00 전에 PDF를 제출합니다.

## 모든 팀원이 지킬 규칙

- `main` 브랜치에 직접 push하지 않고 `feature/작업명` 브랜치에서 작업합니다.
- 커밋 메시지는 `feat: 기능 설명`, `fix: 수정 내용`, `docs: 문서 내용`, `test: 테스트 내용` 형식으로 작성합니다.
- PR을 올리고 팀원 한 명의 리뷰와 승인을 받은 뒤 병합합니다.
- 테스트와 시연에는 가짜 데이터만 사용합니다. 실제 API 키나 개인정보를 GitHub에 올리지 않습니다.
