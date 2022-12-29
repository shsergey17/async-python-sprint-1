from typing import List
from dataclasses import dataclass


@dataclass
class DateInfo:
    """
    Информация по дате
    """

    # Дата в формате (YYYY-MM-DD)
    date: str
    avg_temperature: float
    sum_condition: int


@dataclass
class CityData:
    """
    Данные по городу
    """

    city_name: str
    dates: List[DateInfo]
    average_temp: float
    average_condition: int
    rating: int = None
