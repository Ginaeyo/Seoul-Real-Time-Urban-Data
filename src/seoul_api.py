"""서울 실시간 도시데이터 API 요청과 응답 변환을 담당합니다."""
from data_provider import DataProvider
import math
import os
from urllib.parse import quote
import requests
from urban_data import UrbanData
from place import Place


class SeoulAPI(DataProvider):
    BASE_URL = "http://openapi.seoul.go.kr:8088"


    def __init__(self, api_key=None, *, fallback_provider: DataProvider):
        self.api_key = (api_key or os.getenv("SEOUL_API_KEY", "")).strip()
        self.fallback_provider = fallback_provider

    def sample_data(self, place: Place, reason=None) -> UrbanData:
        data = self.fallback_provider.get_data(place)
        if data is not None:
            data.fallback_reason = reason
        return data

    def get_data(self, place: Place) -> UrbanData:
        if not isinstance(place, Place):
            raise TypeError("place must be a Place object")
        area_name = place.area_name
        if not self.api_key:
            return self.sample_data(place, "missing_api_key")
        area_identifier = getattr(place, "area_code", None) or area_name
        key = quote(self.api_key, safe="")
        location = quote(str(area_identifier), safe="")
        url = f"{self.BASE_URL}/{key}/json/citydata/1/5/{location}"
        try:
            response = requests.get(url, timeout=(3, 5))
            response.raise_for_status()
            result = response.json()
            if not isinstance(result, dict):
                return self.sample_data(place, "invalid_response")
            if "RESULT" in result:
                status = result["RESULT"]
                if not isinstance(status, dict) or (status.get("RESULT.CODE") or status.get("CODE")) != "INFO-000":
                    return self.sample_data(place, "api_status_error")
            city_data = result.get("CITYDATA", {})
            if isinstance(city_data, list):
                city_data = city_data[0] if city_data else {}
            if not isinstance(city_data, dict) or not city_data:
                return self.sample_data(place, "missing_city_data")
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
                return self.sample_data(place, "missing_readings")
            low, high = population.get("AREA_PPLTN_MIN"), population.get("AREA_PPLTN_MAX")
            try:
                low, high = int(low), int(high)
                if not 0 <= low <= high:
                    low = high = None
            except (TypeError, ValueError, OverflowError):
                low = high = None
            try:
                weather = float(weather_data.get("TEMP"))
                if not math.isfinite(weather):
                    weather = None
            except (TypeError, ValueError, OverflowError):
                weather = None
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
                congestion=congestion or None,
                weather=weather,
                population_min=low,
                population_max=high,
                updated_at=updated_at,
                traffic=traffic,
                data_source="api",
                rain_chance=rain_chance,
                dust_status=dust_status,
            )
        except (requests.RequestException, ValueError):
            # An exception can contain the URL and its API key.
            return self.sample_data(place, "request_failed")
