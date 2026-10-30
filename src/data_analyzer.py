"""혼잡도 정보를 이해하기 쉬운 설명으로 바꾸는 모듈.

TODO(담당: 김효중 / main.py 연결: 민경환)
- 혼잡도 값별로 사용자에게 보여 줄 설명을 반환한다.
- None 또는 예상하지 못한 값에는 정보가 없다는 안내를 반환한다.
- 분석 결과가 MainApp 실행 흐름에서 실제로 출력되도록 연결한다.
"""
class DataAnalyzer:

    def analyze_congestion(self, congestion):

        if congestion == "붐빔":
            return "현재 매우 혼잡합니다."

        elif congestion == "약간 붐빔":
            return "현재 다소 혼잡합니다."

        elif congestion == "보통":
            return "현재 보통 수준입니다."

        return "정보가 없습니다."