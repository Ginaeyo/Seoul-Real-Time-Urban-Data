import pytest

from data_provider import DataProvider
from sample_data_provider import SampleDataProvider
from seoul_api import SeoulAPI
from urban_data import UrbanData
from place import Place


def test_abstract_class():
    with pytest.raises(TypeError):
        DataProvider()


def test_provider_inheritance():
    assert issubclass(SeoulAPI, DataProvider)
    assert issubclass(SampleDataProvider, DataProvider)


def test_sample_provider():
    provider = SampleDataProvider()
    result = provider.get_data(Place("강남역"))

    assert isinstance(result, UrbanData)
    assert result.area_name == "강남역"
    assert result.data_source == "sample"

def test_provider_substitution():
    api = SeoulAPI(fallback_provider=SampleDataProvider())
    api.api_key = ""

    providers = [
        api,
        SampleDataProvider()
    ]

    for provider in providers:
        result = provider.get_data(Place("강남역"))

        assert isinstance(result, UrbanData)
        assert result.area_name == "강남역"
        assert result.data_source == "sample"

def test_place_contract_and_required_fallback():
    with pytest.raises(TypeError):
        SeoulAPI()
    for provider in (SampleDataProvider(), SeoulAPI(fallback_provider=SampleDataProvider())):
        with pytest.raises(TypeError):
            provider.get_data("강남역")
