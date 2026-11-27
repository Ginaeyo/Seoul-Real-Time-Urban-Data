
# 팀원용 GitHub 작업 안내

모든 팀원은 각자의 브랜치에서 작업하고, PR(Pull Request)을 통해 리뷰를 받은 뒤 main 브랜치에 반영합니다.

## 1. 준비물 확인

VS Code에서 터미널을 열고 Git과 Python이 설치되어 있는지 확인합니다.

```powershell
git --version
py --version
```

API 키는 환경 변수로 설정하고 소스 코드나 GitHub에 직접 저장하지 않습니다.

## 2. 저장소 처음 내려받기

프로젝트를 처음 내려받는 경우에만 실행합니다.

```powershell
cd $HOME\Desktop
git clone https://github.com/Ginaeyo/Seoul-Real-Time-Urban-Data.git
cd "Seoul-Real-Time-Urban-Data"
```

이미 프로젝트 폴더가 있다면 다시 clone할 필요는 없습니다.

## 3. 실행 환경 설정

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src\main.py
```

API 키가 없거나 요청에 실패하면 SampleDataProvider를 통해 샘플 데이터를 제공합니다.

## 4. 작업 전 최신 코드 받기

작업 중인 변경 사항이 있는지 먼저 확인합니다.

```powershell
git status
```

커밋하지 않은 변경 사항이 있다면 먼저 본인 브랜치에 저장합니다.

새로운 작업을 시작하는 경우 다음 명령을 실행합니다.

```powershell
git switch main
git pull --ff-only origin main
```

### 기존 작업 브랜치에 최신 main 반영하기

이미 본인의 브랜치에서 작업 중이라면 새로운 브랜치를 만들 필요가 없습니다.

현재 작업 브랜치에서 변경 사항을 커밋한 뒤 다음 명령을 실행합니다.

```powershell
git fetch origin
git merge origin/main
```

추상 클래스 구현 및 SOLID 원칙 적용으로 기존 클래스의 구조와 의존 관계가 일부 변경되었습니다.

따라서 이후 작업은 최신 main 브랜치의 변경 사항을 반영한 상태에서 진행해 주세요.

충돌이 발생하면 임의로 코드를 삭제하거나 덮어쓰지 말고 팀장에게 알려 주세요.

## 5. 작업 브랜치 만들기

새로운 작업을 시작할 때는 최신 main을 기준으로 브랜치를 만듭니다.

```powershell
git switch -c feature/my-task
```

| 담당자 | 브랜치 이름 예시 |
|---|---|
| 에르덴자야 (Ginaeyo) | feature/abstract-class |
| 할리오나 (Liuka0715) | feature/seoul-api |
| 민경환 (Kimmolang11) | feature/data-model-main |
| 원미혜 (Today0505) | feature/dashboard |
| 김효중 (a01056405156-ctrl) | feature/area-analysis |

브랜치 이름은 작업 내용에 맞게 작성하며 한글이나 공백은 사용하지 않습니다.

## 6. 클래스 구조 및 개발 시 주의 사항

현재 프로젝트에는 다음과 같은 추상 클래스 구조가 적용되어 있습니다.

- DataProvider: 데이터 제공 방식의 공통 규칙 정의
- SeoulAPI: 실시간 데이터 수집 및 처리
- SampleDataProvider: 샘플 데이터 생성 및 제공
- MainApp: 데이터 제공 객체를 외부에서 전달받아 실행 흐름 관리

SeoulAPI와 SampleDataProvider는 DataProvider를 상속하며 get_data() 메서드를 구현합니다.

새로운 기능을 추가하거나 기존 클래스를 수정할 때는 클래스별 책임과 SOLID 원칙을 고려해 주세요.

MainApp의 기존 의존성 주입 구조를 유지합니다.

```python
MainApp(SeoulAPI()).run()
```

웹사이트 구현 시에도 기존 데이터 수집, 지역 관리 및 분석 클래스를 최대한 재사용합니다.

공통 클래스의 구조를 변경해야 하는 경우 팀원들과 먼저 공유합니다.

## 7. 코드 수정 및 테스트

변경된 파일을 확인합니다.

```powershell
git status
git diff
```

테스트에 필요한 라이브러리를 설치합니다.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

전체 테스트를 실행합니다.

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

추상 클래스 및 SOLID 원칙 적용 작업 완료 시점의 테스트 결과는 36 passed입니다.

새로운 기능을 추가한 경우 관련 테스트도 추가하거나 수정합니다.

## 8. 커밋 만들기

필요한 파일만 선택하여 추가합니다.

```powershell
git add src/dashboard.py
git diff --cached
git status
```

API 키, .env, 개인 정보, 불필요한 파일이 포함되지 않았는지 확인한 뒤 커밋합니다.

```powershell
git commit -m "feat: 대시보드 기능 개선"
```

커밋 메시지 예시:

- feat: 웹사이트 지역 선택 기능 구현
- refactor: 추상 클래스 구현 및 SOLID 원칙 적용
- fix: API 응답 오류 처리
- test: 데이터 제공 객체 검증 테스트 추가
- docs: README 및 클래스 다이어그램 수정

## 9. GitHub에 올리기

처음 올리는 브랜치는 다음과 같이 실행합니다.

```powershell
git push -u origin feature/my-task
```

feature/my-task 부분은 본인의 브랜치 이름으로 변경합니다.

이후 같은 브랜치에서는 다음 명령만 실행하면 됩니다.

```powershell
git push
```

## 10. 병합 요청(PR) 만들기

1. GitHub에서 프로젝트 저장소에 접속합니다.
2. Compare & pull request를 선택합니다.
3. base 브랜치가 main인지 확인합니다.
4. compare 브랜치가 본인의 작업 브랜치인지 확인합니다.
5. 변경 내용과 테스트 결과를 작성합니다.
6. 팀원 한 명을 리뷰 담당자로 지정합니다.
7. Create pull request를 선택합니다.
8. 리뷰 및 승인 후 팀장이 병합합니다.

### PR 설명 작성 예시

변경 내용:
- 구현하거나 수정한 기능
- 변경된 클래스 및 파일

테스트:
- 실행한 테스트
- 테스트 성공 및 실패 여부

참고 사항:
- 다른 팀원이 확인해야 할 내용
- 추가 수정이 필요한 부분

## 11. 병합 후 최신 코드 반영

본인의 PR이 병합된 뒤 새로운 작업을 시작할 때는 다음 명령을 실행합니다.

```powershell
git switch main
git pull --ff-only origin main
git switch -c feature/next-task
```

기존 작업 브랜치를 계속 사용하는 경우에는 해당 브랜치에서 다음 명령을 실행합니다.

```powershell
git fetch origin
git merge origin/main
```

## 12. 최종 발표 및 문서 준비

각자 맡은 기능과 클래스에 대해 다음 내용을 정리합니다.

- 클래스의 역할과 구현 목적
- 주요 메서드와 실행 흐름
- 다른 클래스와의 관계
- 적용한 객체지향 프로그래밍 개념 및 SOLID 원칙
- 코드 및 실행 화면 캡처
- 테스트 결과

정리한 설명문은 최종 발표 자료 제작에 활용할 수 있도록 발표자에게 전달합니다.

PPT는 교수님이 제공하신 예시와 양식을 참고하여 제작합니다.

## 작업 규칙

- main 브랜치에 직접 커밋하거나 push하지 않습니다.
- 각자의 브랜치에서 작업한 뒤 PR을 통해 병합합니다.
- 작업 전 최신 main의 변경 사항을 확인합니다.
- 다른 팀원의 코드를 임의로 삭제하거나 덮어쓰지 않습니다.
- 클래스별 책임과 SOLID 원칙을 고려하여 개발합니다.
- API 키와 개인 정보는 GitHub에 올리지 않습니다.
- 샘플 데이터와 실시간 데이터를 명확하게 구분합니다.
- 변경 후 테스트를 실행합니다.
- 충돌이나 오류가 발생하면 팀 채팅에 공유합니다. API 키 등 민감한 정보는 제거한 후 공유합니다.
- 각자 담당한 부분의 설명문을 작성합니다.
