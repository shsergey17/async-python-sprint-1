import pytest
import sys

sys.path.append("../")
from src.entity import CityData, DateInfo
from tasks import DataAggregationTask

from typing import List
from dataclasses import dataclass


@pytest.mark.parametrize(
    "city_data_list, expected_response",
    [
        (
            [
                CityData(
                    "New York",
                    [
                        DateInfo("2022-01-01", 10, 8),
                        DateInfo("2022-01-02", 12, 6),
                        DateInfo("2022-01-03", 14, 4),
                    ],
                    12,
                    5,
                ),
                CityData(
                    "London",
                    [
                        DateInfo("2022-01-01", 9, 6),
                        DateInfo("2022-01-02", 11, 4),
                        DateInfo("2022-01-03", 13, 2),
                    ],
                    11,
                    3,
                ),
            ],
            [
                [
                    "Город/день",
                    "",
                    "2022-01-01",
                    "2022-01-02",
                    "2022-01-03",
                    "Среднее",
                    "Рейтинг",
                ],
                ["New York", "Температура, среднее", "10", "12", "14", "12", "None"],
                ["", "Без осадков, часов", "8", "6", "4", "5", ""],
                ["London", "Температура, среднее", "9", "11", "13", "11", "None"],
                ["", "Без осадков, часов", "6", "4", "2", "3", ""],
            ],
        )
    ],
)

def test_make_data_list(city_data_list, expected_response):
    task = DataAggregationTask()
    response = task.make_data_list(city_data_list)

    assert response == expected_response
