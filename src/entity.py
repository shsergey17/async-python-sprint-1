from typing import List
from dataclasses import dataclass

@dataclass
class DateInfo:
    date: str
    avg_temperature: float
    sum_condition: int

@dataclass
class CityData:
    city_name: str
    dates: List[DateInfo]
    average_temp: float
    average_condition: int
    rating: int = None

@dataclass
class CityDataRaiting:
    city_data: CityData
    raiting: int


if __name__ == "__main__":
    city = CityData('LONDON', [], 11.0, 11)

    print(city)