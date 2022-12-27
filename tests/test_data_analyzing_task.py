import pytest
import sys
sys.path.append('../')

from tasks import DataAnalyzingTask
from src.entity import DateInfo, CityData



def getTask():
    return DataAnalyzingTask()

def test_sort_by_temp_and_condition():
    city_data = [
        CityData('London', [], 20, 20),
        CityData('Moscow', [], 30, 5),
        CityData('Berlin', [], 15, 10),
        CityData('Paris', [], 20, 10),
    ]

    result = [
        CityData('Moscow', [], 30, 5),
        CityData('London', [], 20, 20),
        CityData('Paris', [], 20, 10),
        CityData('Berlin', [], 15, 10),
    ]
    task = getTask()

    # order by average_temp DESC, average_condition DESC
    sorted_data = task.sort_by_temp_and_condition(city_data)
    assert result == sorted_data


def test_calc_rating():
    city_data = [
        CityData('London', [], 20, 20),
        CityData('Moscow', [], 30, 5),
        CityData('Berlin', [], 15, 10),
        CityData('Paris', [], 20, 10),
    ]

    result = [
        CityData('Moscow', [], 30, 5, 4),
        CityData('London', [], 20, 20, 3),
        CityData('Paris', [], 20, 10, 2),
        CityData('Berlin', [], 15, 10, 1), 
    ]
    task = getTask()

    data_with_raiting = task.calc_rating(city_data)
    assert result == data_with_raiting




