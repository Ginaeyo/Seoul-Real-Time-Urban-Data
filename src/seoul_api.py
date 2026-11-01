
"""서울 실시간 도시데이터 API 연동 모듈."""

import os
from urllib.parse import quote

import requests

from urban_data import UrbanData


class SeoulAPI:
    BASE_URL = "http://openapi.seoul.go.kr:8088"

    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("SEOUL_API_KEY")

    def sample_data(self, area_name):
        """API 연결이 없을 때 사용하는 예시 데이터."""
        print("샘플 데이터를 사용합니다.")
        return UrbanData(
            area_name=area_name,
            congestion="보통 (샘플)",
            weather="정보 없음"
        )

    def get_data(self, place):
        """Place 객체를 받아 UrbanData 객체를 반환합니다."""
        area_name = getattr(place, "area_name", None)

        if not area_name:
            area_name = str(place)

        if not self.api_key:
            print("API 키가 없어 샘플 모드로 실행합니다.")
            return self.sample_data(area_name)

        # 실제 API에서 확인된 지역명을 사용합니다.
        area = quote(area_name, safe="")
        url = (
            f"{self.BASE_URL}/{self.api_key}/json/"
            f"citydata/1/5/{area}"
        )

        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            result = response.json()

            if not isinstance(result, dict):
                print("API 응답 형식이 올바르지 않습니다.")
                return self.sample_data(area_name)

            if "RESULT" in result and result["RESULT"].get("RESULT.CODE") != "INFO-000":
                message = result["RESULT"]
                print("API 오류:", message)
                return self.sample_data(area_name)

            city_data = result.get("CITYDATA", {})

            if isinstance(city_data, list):
                city_data = city_data[0] if city_data else {}

            if not isinstance(city_data, dict) or not city_data:
                print("도시 데이터를 찾을 수 없습니다.")
                return self.sample_data(area_name)

            population = city_data.get("LIVE_PPLTN_STTS", [])
            weather_data = city_data.get("WEATHER_STTS", [])

            if isinstance(population, list):
                population = population[0] if population else {}

            if isinstance(weather_data, list):
                weather_data = weather_data[0] if weather_data else {}

            congestion = (
                population.get("AREA_CONGEST_LVL")
                if isinstance(population, dict)
                else None
            )

            temperature = (
                weather_data.get("TEMP")
                if isinstance(weather_data, dict)
                else None
            )

            return UrbanData(
                area_name=area_name,
                congestion=congestion or "정보 없음",
                weather=(
                    f"{temperature}°C"
                    if temperature is not None
                    else "정보 없음"
                )
            )

        except (requests.RequestException, ValueError) as error:
            print(f"API 요청 실패: {error}")
            return self.sample_data(area_name)
