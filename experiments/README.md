# 혼잡도 비교 실험

선택한 각 지역의 서울시 실시간 인구 API(`citydata_ppltn`)를 XML 형식으로 호출해 혼잡도 차트를 만듭니다. API 요청에 실패하면 오류를 표시합니다.

프로젝트 폴더에서 PowerShell을 열고, 발급받은 인증키를 현재 세션에 설정한 뒤 실행합니다.

```powershell
$secureApiKey = Read-Host '서울시 API 키를 입력하세요' -AsSecureString
$env:SEOUL_API_KEY = [System.Net.NetworkCredential]::new('', $secureApiKey).Password
.\.venv\Scripts\python.exe experiments\congestion_compare.py 강남역 "홍대입구역(2호선)"
```

키는 현재 PowerShell 세션에서만 사용합니다. 공개 `sample` 키로는 광화문·덕수궁만 조회할 수 있으므로 여러 지역을 비교할 때는 발급받은 키를 사용하세요. 요청에는 공식 지역명을 사용합니다. 차트는 `experiments/congestion_comparison.png`에 저장됩니다.
