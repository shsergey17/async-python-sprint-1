import pytest
from unittest.mock import Mock, patch
import sys
sys.path.append("..")
from api_client import YandexWeatherAPI
from src.entity import DateInfo, CityData
from tasks import DataFetchingTask


@patch("api_client.YandexWeatherAPI")
def test_make_request(mock_yandex_weather_api):

    mock_api = Mock(YandexWeatherAPI)
    mock_yandex_weather_api.return_value = mock_api
    mock_api.get_forecasting.return_value = {"forecasts": {"some": "data"}}

    task = DataFetchingTask(mock_api)
    result = task.make_request("Moscow")
    mock_api.get_forecasting.assert_called_once_with("Moscow")
    assert result == {"some": "data"}
