from abc import ABC, abstractmethod
from urban_data import UrbanData


class DataProvider(ABC):
    """도시 데이터를 제공하는 추상 클래스."""

    @abstractmethod
    def get_data(self, place) -> UrbanData:
        """지정된 지역의 도시 데이터를 반환한다."""
        pass