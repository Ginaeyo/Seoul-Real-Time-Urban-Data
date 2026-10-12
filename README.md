# Seoul Real-Time Urban Data

## 프로젝트 소개

서울 실시간 도시데이터 프로젝트는 서울시 실시간 도시데이터 API를 활용하여 사용자가 선택한 지역의 실시간 도시 정보를 확인할 수 있는 객체지향 프로그래밍(OOP) 팀 프로젝트입니다.

사용자는 서울의 특정 지역을 선택하거나 검색하여 다음 정보를 확인할 수 있습니다.

- 실시간 인구 현황 및 혼잡도
- 날씨 정보
- 교통 상황

본 프로젝트는 데이터 수집, 관리, 분석 및 출력 기능을 클래스별로 분리하여 구현합니다.

## 주요 기능

- 서울 지역 검색 및 선택
- 실시간 인구 현황 및 혼잡도 확인
- 선택한 지역의 날씨 정보 확인
- 선택한 지역의 교통 상황 확인
- API 데이터 수집 및 가공
- 객체지향 프로그래밍을 활용한 클래스별 기능 분리

## 사용 데이터

- 기본 데이터: 서울 실시간 도시데이터
- 데이터 수집: 서울시 실시간 도시데이터 API
- 주요 정보: 인구 현황, 날씨, 교통 상황

## 클래스 구조

| 클래스 | 주요 책임 |
|---|---|
| MainApp | 전체 프로그램 흐름 제어 및 클래스 연결 |
| LocationSelector | 사용자 검색어 입력 및 지역 선택 |
| AreaManager | 지역 목록 관리 및 검색 결과 조회 |
| Place | 지역명, 지역 코드 등 기본 정보 저장 |
| SeoulAPI | API 요청 및 데이터 수신 |
| UrbanData | 실시간 인구, 날씨 및 교통 데이터 저장 |
| DataAnalyzer | 수집한 데이터 가공 및 분석 |
| Dashboard | 가공된 데이터를 사용자에게 출력 |

## 프로그램 동작 흐름

1. 사용자가 지역을 검색하고 선택합니다.
2. AreaManager가 해당 지역 정보를 확인합니다.
3. Place가 지역명과 지역 코드 등 기본 정보를 제공합니다.
4. SeoulAPI가 서울시 실시간 도시데이터 API에 요청합니다.
5. UrbanData가 수신한 데이터를 저장합니다.
6. DataAnalyzer가 인구, 날씨 및 교통 데이터를 가공합니다.
7. Dashboard가 가공된 정보를 사용자에게 출력합니다.

## 프로젝트 구조

```text
Seoul-Real-Time-Urban-Data/
├── src/
│   ├── main.py
│   ├── seoul_api.py
│   ├── urban_data.py
│   ├── place.py
│   ├── area_manager.py
│   ├── location_selector.py
│   └── data_analyzer.py
├── docs/
│   └── Seoul_Real_Time_Urban_Data_Proposal.docx
├── images/
├── .gitignore
├── License
├── README.md
└── requirements.txt
```

실제 파일 구성은 개발 진행 상황에 따라 변경될 수 있습니다.

## 실행 방법

현재 콘솔 프로그램으로 구현할 예정입니다.

1. Python을 설치합니다.
2. 저장소를 다운로드하거나 복제합니다.
3. 필요한 라이브러리를 설치합니다.

```bash
pip install -r requirements.txt
```

4. `src/main.py`를 실행합니다.

```bash
python src/main.py
```

API 연결 및 프로그램 구현이 완료되면 실행 방법을 업데이트합니다.

## 팀원 역할 분담

| 팀원 | 담당 클래스 및 업무 |
|---|---|
| 에르덴자야 (Ginaeyo) | 팀장, 프로젝트 관리, 일정 조율, GitHub 관리, 문서 작성 및 최종 검토 |
| 할리오나 (Liuka0715) | SeoulAPI, API 연동 및 실시간 데이터 수집 |
| 민경환 (Kimmolang11) | Place, UrbanData, MainApp, 데이터 구조 설계 및 프로그램 흐름 통합 |
| 원미혜 (Today0505) | Dashboard, 사용자 인터페이스 및 결과 출력 |
| 김효중 (a01056405156-ctrl) | AreaManager, LocationSelector, DataAnalyzer, 지역 관리 및 데이터 분석 |

모든 팀원은 통합 테스트, 오류 수정 및 발표 준비에 참여합니다.

## 개발 환경

- Language: Python
- Data Source: Seoul Real-Time Urban Data API
- Version Control: GitHub

## License

본 프로젝트는 MIT License를 따릅니다. 자세한 내용은 License 파일을 참고하세요.
