"""혼잡도 정보를 이해하기 쉬운 설명으로 바꾸는 모듈.

TODO(담당: 김효중 / main.py 연결: 민경환)
- 혼잡도 값별로 사용자에게 보여 줄 설명을 반환한다.
- None 또는 예상하지 못한 값에는 정보가 없다는 안내를 반환한다.
- 분석 결과가 MainApp 실행 흐름에서 실제로 출력되도록 연결한다.
"""


class DataAnalyzer:

    def analyze_congestion(self, congestion):
        if not congestion:
            return "정보가 없습니다."

        congestion = congestion.replace(" (샘플)", "").strip()

        if congestion == "붐빔":
            return "현재 매우 혼잡합니다."
        elif congestion == "약간 붐빔":
            return "현재 다소 혼잡합니다."
        elif congestion == "보통":
            return "현재 보통 수준입니다."
        elif congestion == "여유":
            return "현재 여유로운 상태입니다."

        return "정보가 없습니다."

    def compare_congestion(self, area1, congestion1, area2, congestion2):
        levels = {
            "여유": 1,
            "보통": 2,
            "약간 붐빔": 3,
            "붐빔": 4
        }

        if isinstance(congestion1, str):
            congestion1 = congestion1.replace(" (샘플)", "").strip()

        if isinstance(congestion2, str):
            congestion2 = congestion2.replace(" (샘플)", "").strip()

        level1 = levels.get(congestion1)
        level2 = levels.get(congestion2)

        if level1 is None or level2 is None:
            return "혼잡도를 비교할 수 없습니다."

        if level1 > level2:
            return f"{area1}이(가) {area2}보다 혼잡합니다."

        elif level1 < level2:
            return f"{area2}이(가) {area1}보다 혼잡합니다."

        return "두 지역의 혼잡도는 같습니다."
