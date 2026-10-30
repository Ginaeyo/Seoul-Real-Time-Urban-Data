# 팀원용 GitHub 작업 안내

GitHub를 처음 사용하는 팀원도 아래 순서대로 따라 하면 됩니다. 모든 팀원은 자기 작업을 별도의 브랜치에서 진행하고, PR을 열어 리뷰를 받은 뒤 `main`에 반영합니다.

## 1. 준비물 확인

컴퓨터에 Git과 Python이 설치되어 있어야 합니다. VS Code를 열고 **Terminal → New Terminal**을 선택해 터미널을 엽니다.

```powershell
git --version
py --version
```

버전이 표시되지 않으면 팀장에게 알려 주세요. API 키는 필요할 때 팀에서 안내한 방법으로 설정하고, 채팅이나 코드에 붙여 넣지 마세요.

## 2. 저장소를 처음 내려받기 (clone)

저장소를 아직 컴퓨터에 받지 않은 경우에만 한 번 실행합니다. 이미 프로젝트 폴더가 있다면 다시 clone하지 말고 4단계로 가세요.

```powershell
cd $HOME\Desktop
git clone https://github.com/Ginaeyo/Seoul-Real-Time-Urban-Data.git
cd "Seoul-Real-Time-Urban-Data"
```

## 3. 실행 환경 만들기

프로젝트 폴더 안에서 아래 명령을 실행합니다. 이 방법은 가상 환경을 만들고 그 안에 필요한 라이브러리를 설치합니다.

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src\main.py
```

`src\main.py` 실행 결과가 나오면 기본 환경이 준비된 것입니다. API 키나 네트워크가 준비되지 않은 경우 팀에서 제공한 샘플 데이터로 작업합니다.

## 4. 작업 전 최신 코드 받기

이미 clone한 저장소에서 새 작업을 시작할 때 실행합니다. 다른 팀원의 작업 중인 브랜치로 바꾸지 말고, `main`에서 최신 코드를 받은 뒤 자기 브랜치를 만듭니다.

```powershell
git switch main
git pull origin main
```

## 5. 내 작업 브랜치 만들기

브랜치는 작업마다 새로 만들고, `main`에 직접 수정하거나 push하지 않습니다.

```powershell
git switch -c feature/my-task
```

예시:

| 담당자 | 브랜치 이름 예시 |
|---|---|
| 에르덴자야 (Ginaeyo) | `docs/team-guide` |
| 할리오나 (Liuka0715) | `feature/seoul-api` |
| 민경환 (Kimmolang11) | `feature/data-model-main` |
| 원미혜 (Today0505) | `feature/dashboard` |
| 김효중 (a01056405156-ctrl) | `feature/area-analysis` |

브랜치 이름에 한글이나 공백은 넣지 않습니다.

## 6. 코드 작성하고 변경 내용 확인하기

파일을 수정한 뒤 어떤 파일이 바뀌었는지 확인합니다.

```powershell
git status
```

필요한 파일만 지정해 stage합니다. 예를 들어 대시보드 담당자는 다음처럼 실행할 수 있습니다.

```powershell
git add src/dashboard.py
git status
```

개인 API 키, `.env`, 개인 정보 파일은 절대 추가하지 마세요. 실수로 민감한 파일을 추가했다면 commit하기 전에 팀장에게 알립니다.

## 7. Commit 만들기

커밋 메시지는 작업 내용을 짧게 설명합니다.

```powershell
git commit -m "feat: 대시보드 정보 출력"
```

메시지 예시:

- `feat: 지역 선택 기능 추가`
- `fix: 잘못된 입력 처리`
- `test: 혼잡도 분석 테스트 추가`
- `docs: 실행 방법 보완`

## 8. GitHub에 push하기

처음 push할 때는 현재 브랜치를 원격 저장소에 올리도록 아래 명령을 실행합니다. `feature/dashboard` 부분은 본인 브랜치 이름으로 바꿉니다.

```powershell
git push -u origin feature/dashboard
```

같은 브랜치에서 다음 commit을 올릴 때는 `git push`만 실행하면 됩니다.

## 9. Pull Request(PR) 열기

1. GitHub에서 Seoul 프로젝트 저장소를 엽니다.
2. **Compare & pull request**를 선택합니다. 버튼이 보이지 않으면 **Pull requests → New pull request**로 이동합니다.
3. 대상 브랜치가 `main`, 작업 브랜치가 본인 `feature/...`인지 확인합니다.
4. 제목과 설명을 작성합니다. 무엇을 바꿨는지, 어떻게 확인했는지, 화면 캡처가 있는지 적습니다.
5. 팀원 한 명을 reviewer로 지정하고 **Create pull request**를 누릅니다.
6. 리뷰에서 수정 요청을 받으면 같은 브랜치에서 고친 뒤 commit하고 push합니다. PR은 자동으로 갱신됩니다.
7. 승인 후 팀장이 PR을 병합합니다. 본인 PR을 승인하거나 `main`에 직접 병합하지 않습니다.

## 10. 병합된 최신 코드로 다음 작업 시작하기

PR이 병합된 뒤 새 작업을 시작할 때 `main`을 갱신하고 새 브랜치를 만듭니다.

```powershell
git switch main
git pull origin main
git switch -c feature/next-task
```

## 작업 규칙

- `main`에 직접 commit/push하지 않습니다.
- 한 브랜치에는 한 가지 작업만 담고, 담당 파일을 중심으로 수정합니다.
- 새 함수에는 가능한 한 간단한 테스트를 추가하고, API 테스트는 가짜 응답을 사용합니다.
- 서울시 API에서 실제 제공되는 것이 확인되지 않은 정보를 임의로 만들지 않습니다.
- PR이 다른 사람의 파일과 겹치거나 Git 충돌이 생기면 임의로 덮어쓰지 말고 팀장에게 먼저 알립니다.
- 오류가 나면 오류 메시지와 `git status` 결과를 함께 팀 채팅에 공유합니다.


