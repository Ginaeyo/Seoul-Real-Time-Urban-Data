
import os
import requests
from urllib.parse import quote

from urban_data import UrbanData


class SeoulAPI:
    BASE_URL = "http://openapi.seoul.go.kr:8088"

    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("SEOUL_API_KEY")

    def get_data(self, area_name):
        if not self.api_key:
            print("API 인증키가 없습니다.")
            return None

        area = quote(area_name, safe="")
        url = (
            f"{self.BASE_URL}/{self.api_key}/json/"
            f"citydata/1/5/{area}"
        )

        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            result = response.json()

            if "RESULT" in result:
                print("API 오류:", result["RESULT"].get("MESSAGE"))
                return None

            city_data = result.get("CITYDATA", {})
            if not city_data:
                print("도시 데이터를 찾을 수 없습니다.")
                return None

            population = city_data.get("LIVE_PPLTN_STTS", [])
            weather = city_data.get("WEATHER_STTS", [])

            if isinstance(population, list):
                population = population[0] if population else {}

            if isinstance(weather, list):
                weather = weather[0] if weather else {}

            congestion = (
                population.get("AREA_CONGEST_LVL", "정보 없음")
                if isinstance(population, dict)
                else "정보 없음"
            )

            temperature = (
                weather.get("TEMP", "정보 없음")
                if isinstance(weather, dict)
                else "정보 없음"
            )

            return UrbanData(
                area_name,
                congestion,
                temperature
            )

        except (requests.RequestException, ValueError) as error:
            print(f"API 요청 실패: {error}")
            return None
