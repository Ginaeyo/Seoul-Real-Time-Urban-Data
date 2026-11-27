"""서울 실시간 도시데이터 API 요청과 응답 변환을 담당합니다."""
from data_provider import DataProvider
import math
import os
from urllib.parse import quote
import requests
from urban_data import UrbanData
from sample_data_provider import SampleDataProvider


class SeoulAPI(DataProvider):
    BASE_URL = "http://openapi.seoul.go.kr:8088"


    def __init__(self, api_key=None):
        self.api_key = (api_key or os.getenv("SEOUL_API_KEY", "")).strip()

    def sample_data(self, area_name):
        return SampleDataProvider().get_data(area_name)

    def get_data(self, place):
        area_name = getattr(place, "area_name", None) or str(place)
        if not self.api_key:
            print("API 키가 없어 샘플 모드로 실행합니다.")
            return self.sample_data(area_name)
        area_identifier = getattr(place, "area_code", None) or area_name
        key = quote(self.api_key, safe="")
        location = quote(str(area_identifier), safe="")
        url = f"{self.BASE_URL}/{key}/json/citydata/1/5/{location}"
        try:
            response = requests.get(url, timeout=(3, 5))
            response.raise_for_status()
            result = response.json()
            if not isinstance(result, dict):
                print("API 응답 형식이 올바르지 않습니다.")
                return self.sample_data(area_name)
            if "RESULT" in result:
                status = result["RESULT"]
                if not isinstance(status, dict) or (status.get("RESULT.CODE") or status.get("CODE")) != "INFO-000":
                    print("API가 도시 데이터를 반환하지 않았습니다.")
                    return self.sample_data(area_name)
            city_data = result.get("CITYDATA", {})
            if isinstance(city_data, list):
                city_data = city_data[0] if city_data else {}
            if not isinstance(city_data, dict) or not city_data:
                print("도시 데이터를 찾을 수 없습니다.")
                return self.sample_data(area_name)
            traffic_section = city_data.get("ROAD_TRAFFIC_STTS", {})
            # 전체도로소통평균현황: 일부 응답에서는 dict, 일부는 list 형태
            if isinstance(traffic_section, list):
                traffic_section = traffic_section[0] if traffic_section else {}
            if not isinstance(traffic_section, dict):
                traffic_section = {}
            average_road_data = traffic_section.get("AVG_ROAD_DATA")
            if isinstance(average_road_data, list):
                average_road_data = average_road_data[0] if average_road_data else None
            if not isinstance(average_road_data, dict):
                average_road_data = traffic_section
            traffic = average_road_data.get("ROAD_TRAFFIC_IDX")
            if isinstance(traffic, dict):
                traffic = traffic.get("ROAD_TRAFFIC_IDX")
            if isinstance(traffic, list):
                traffic = traffic[0] if traffic else None
            # 전체 도로소통 분류만 사용. 도로 링크별 상태를 평균인 것처럼 대체하지 않음.
            traffic = str(traffic).strip() if traffic is not None else None
            traffic = {"소통원활":"원활", "원활":"원활", "서행":"서행", "정체":"정체"}.get(traffic)
            population = city_data.get("LIVE_PPLTN_STTS", [])
            weather_data = city_data.get("WEATHER_STTS", [])
            population = population[0] if isinstance(population, list) and population else population
            weather_data = weather_data[0] if isinstance(weather_data, list) and weather_data else weather_data
            population = population if isinstance(population, dict) else {}
            weather_data = weather_data if isinstance(weather_data, dict) else {}
            if not population and not weather_data:
                print("도시 데이터에 인구와 날씨 정보가 없습니다.")
                return self.sample_data(area_name)
            people = None
            low, high = population.get("AREA_PPLTN_MIN"), population.get("AREA_PPLTN_MAX")
            if low is not None and high is not None:
                try:
                    low, high = int(low), int(high)
                    if 0 <= low <= high:
                        people = f"{(low + high) // 2:,} (범위 중간값)"
                except (TypeError, ValueError, OverflowError):
                    pass
            temperature = weather_data.get("TEMP")
            try:
                weather = f"{temperature}°C" if math.isfinite(float(temperature)) else "정보 없음"
            except (TypeError, ValueError, OverflowError):
                weather = "정보 없음"
            forecast = weather_data.get("FCST24HOURS")
            if isinstance(forecast, list):
                forecast = forecast[0] if forecast else None
            rain_chance = None
            if isinstance(forecast, dict):
                try:
                    probability = float(str(forecast.get("RAIN_CHANCE")).strip().removesuffix("%"))
                    if 0 <= probability <= 100:
                        rain_chance = probability
                except ValueError:
                    pass
            dust_status = str(weather_data.get("PM10_INDEX") or "").strip()
            if dust_status not in ("좋음", "보통", "나쁨", "매우나쁨", "매우 나쁨"):
                dust_status = None
            congestion = population.get("AREA_CONGEST_LVL")
            if isinstance(congestion, str):
                congestion = congestion.strip()
            else:
                congestion = None
            updated_at = (
                population.get("PPLTN_TIME")
                or city_data.get("PPLTN_TIME")
                or weather_data.get("WEATHER_TIME")
            )
            return UrbanData(
                area_name=area_name,
                congestion=congestion or "정보 없음",
                weather=weather,
                population=people,
                updated_at=updated_at,
                traffic=traffic,
                data_source="api",
                rain_chance=rain_chance,
                dust_status=dust_status,
            )
        except (requests.RequestException, ValueError):
            # An exception can contain the URL and its API key.
            print("API 요청에 실패했습니다. 연결 상태와 인증키를 확인하세요.")
            return self.sample_data(area_name)
