class DataAnalyzer:

    def analyze_congestion(self, congestion):

        if congestion == "붐빔":
            return "현재 매우 혼잡합니다."

        elif congestion == "약간 붐빔":
            return "현재 다소 혼잡합니다."

        elif congestion == "보통":
            return "현재 보통 수준입니다."

        return "정보가 없습니다."