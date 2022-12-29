import sys

sys.path.append("..")

from tasks import DataCalculationTask
from src.entity import DateInfo, CityData


def getTask():
    return DataCalculationTask(
        hour_from=9,
        hour_to=19,
        weather_condition=["clear", "partly", "cloudy", "overcast"],
    )


def test_hour_calc():
    task = getTask()

    hours_list = [
        {"hour": "8", "temp": 24, "condition": "clear"},
        {"hour": "9", "temp": 24, "condition": "clear"},
        {"hour": "10", "temp": 25, "condition": "clear"},
        {"hour": "12", "temp": 21, "condition": "cloudy"},
        {"hour": "13", "temp": 23, "condition": "rain"},
    ]

    temperatures, day_sum_condition = task.hour_calc(hours_list)

    assert temperatures == [24, 25, 21, 23]
    assert day_sum_condition == 3


def test_hour_calc_none():
    task = getTask()

    hours_list = [
        {"hour": "1", "temp": 24, "condition": "clear"},
        {"hour": "2", "temp": 24, "condition": "clear"},
    ]

    temperatures, day_sum_condition = task.hour_calc(hours_list)

    assert temperatures == []
    assert day_sum_condition == 0


def test_average():
    data = [
        DateInfo(date="2022-01-01", avg_temperature=24, sum_condition=8),
        DateInfo(date="2022-01-02", avg_temperature=25, sum_condition=4),
        DateInfo(date="2022-01-03", avg_temperature=21, sum_condition=7),
    ]

    task = getTask()

    result_avg_temperature = task.average(data, "avg_temperature")
    result_sum_condition = task.average(data, "sum_condition")

    assert result_avg_temperature == 23.3
    assert result_sum_condition == 6.3


def test_avg():
    task = getTask()

    assert task.avg(sum([5, 6, 7]), 3) == 6
    assert task.avg(0, 0) == 0


def test_day_calc():
    task = getTask()
    data = [
        {
            "date": "2022-01-25",
            "hours": [
                {"hour": 1, "temp": 19, "condition": "clear"},
                {"hour": 9, "temp": 20, "condition": "clear"},
                {"hour": 10, "temp": 19, "condition": "clear"},
                {"hour": 11, "temp": 10, "condition": "not_clear"},
            ],
        }
    ]
    result_avg_temperature = task.day_calc(data)

    result = [DateInfo(date="2022-01-25", avg_temperature=16.3, sum_condition=2)]

    assert result == result_avg_temperature


def test_day_calc_temp():
    task = getTask()
    data = [
        {
            "date": "2022-01-25",
            "hours": [
                {"hour": 10, "temp": 20, "condition": "clear"},
                {"hour": 11, "temp": 10, "condition": "not_clear"},
            ],
        }
    ]
    average_temp = 15.0
    result_avg_temperature = task.day_calc(data)

    result = [
        DateInfo(date="2022-01-25", avg_temperature=average_temp, sum_condition=1)
    ]

    assert result == result_avg_temperature


def test_calc():
    task = getTask()

    data = [
        {
            "date": "2022-01-25",
            "hours": [
                {"hour": 10, "temp": 20, "condition": "clear"},
                {"hour": 11, "temp": 10, "condition": "clear"},
            ],
        }
    ]

    result = CityData(
        city_name="London",
        dates=[DateInfo(date="2022-01-25", avg_temperature=15.0, sum_condition=2)],
        average_temp=15.0,
        average_condition=2,
    )

    assert result == task.calc("London", data)
