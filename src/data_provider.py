from abc import ABC, abstractmethod
from urban_data import UrbanData
from place import Place


class DataProvider(ABC):
    """도시 데이터를 제공하는 추상 클래스."""

    @abstractmethod
    def get_data(self, place: Place) -> UrbanData:
        """Place를 받아 UrbanData를 반환한다. 잘못된 입력은 TypeError로 처리한다.
        data_source는 api 또는 sample, weather는 유한한 숫자 또는 None이다."""
        pass
