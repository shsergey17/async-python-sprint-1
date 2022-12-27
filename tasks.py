import os
from api_client import YandexWeatherAPI
from statistics import mean
from dataclasses import dataclass
from typing import List, Tuple
from pathlib import Path
from src.entity import CityData, DateInfo
from src.file_types import IFileType
import json
from utils import HOUR_FROM, HOUR_TO, WEATHER_CONDITION

class DataFetchingTask:

    @staticmethod
    def make_request(city_name: str) -> list:
        # Code to make the API request goes here
        ywAPI = YandexWeatherAPI()
        resp = ywAPI.get_forecasting(city_name)
        return resp


class DataCalculationTask():
    def __init__(self, hour_from, hour_to, weather_condition) -> None:
        self.hour_from = hour_from
        self.hour_to = hour_to
        self.weather_condition = weather_condition

    def calc(self, city_name, data) -> CityData:

        date_info_list = self.day_calc(data)

        return CityData(
            city_name = city_name, 
            dates = date_info_list, 
            average_temp = self.average(date_info_list, 'avg_temperature'), 
            average_condition = self.average(date_info_list, 'sum_condition')
        )

    def avg(self, value, length: int) -> float:
        if length == 0: return 0
        return round(value / length, 1)

    def average(self, data: List[DateInfo], field: str) -> float:
        total_sum = sum([getattr(date_info, field) for date_info in data])
        count = len(data)

        return self.avg(total_sum, count)

    def day_calc(self, data: list) -> List[DateInfo]:
        temperate_dict = []
        for date_item in data:

            try:
                hours_list = date_item.get('hours')
                date_str = date_item.get('date')
            except Exception as e:
                print(date_item)
                exit()


            if not hours_list:
                continue

            temperatures, hours_sum_condition = self.hour_calc(hours_list)

            hours_average_temperature = self.avg(sum(temperatures), len(temperatures))
            temperate_dict.append(
                DateInfo(date_str, hours_average_temperature, hours_sum_condition)
            )

        return temperate_dict

    def hour_calc(self, hours_list: list) -> Tuple[List[float], int]:
        '''
            Средняя температура рассчитывается за промежуток времени 
            self.hour_from и self.hour_to, игнорируя осадки, т.к.
            не указано в условии

            Сумма времени (часов), когда погода без осадков, рассчитывается 
            за указанный промежуток времени

            see tests/test_day_calc_temp
        '''
        temperatures = []
        day_sum_condition = 0
        
        for hour_item in hours_list:

            current_hour = int(hour_item.get('hour'))
            hour_temp = int(hour_item.get('temp'))
            hour_condition = str(hour_item.get('condition'))

            # print([self.hour_from,current_hour, self.hour_to, self.hour_from <= current_hour  <= self.hour_to])
            if self.hour_from <= current_hour  <= self.hour_to:

                if current_hour and hour_temp:
                    temperatures.append(hour_temp)

                if hour_condition in self.weather_condition:
                    day_sum_condition += 1

        return temperatures, day_sum_condition


class DataAnalyzingTask:

    def calc_rating(self, city_data: list[CityData]) -> list[CityData]:

        sort_city_data = self.sort_by_temp_and_condition(city_data)
        for i, city_data in enumerate(sort_city_data):
            city_data.rating = len(sort_city_data) - i

        return sort_city_data

    def sort_by_temp_and_condition(self, city_data: list[CityData]) -> list[CityData]:
        '''
            order by average_temp DESC, average_condition DESC
        '''
        return sorted(city_data, key=lambda x: (-x.average_temp, -x.average_condition))

class DataAggregationTask:
    def __init__(self) -> None:
        self.best_city = None
        
    def run(self, data_analyzing: DataAnalyzingTask, city_data: list[CityData]) -> CityData:
        if not city_data:
            raise ValueError('CityData empty')

        city_with_rating_list = data_analyzing.calc_rating(city_data)
        self.best_city = city_with_rating_list[0]
        return self

    def save_to_file(self, file_type: IFileType, city_data: list[CityData]) -> bool:

        prepare_table = self.make_data_list(city_data)
        file_type.save(prepare_table)
        return os.path.isfile(file_type.filename)

    def make_data_list(self, city_data_list: List[CityData]) -> List[List[str]]:
        dates = [date_info.date for city_data in city_data_list for date_info in city_data.dates]
        dates = list(set(dates))

        data = [['City', ''] + dates + ['Average', 'Rating']]

        for city_data in city_data_list:
            temp_row = [city_data.city_name, 'Temperature'] + [str(date.avg_temperature) for date in city_data.dates] + [str(city_data.average_temp), str(city_data.rating)]
            cond_row = ['', 'condition'] + [str(date.sum_condition) for date in city_data.dates] + [str(city_data.average_condition), '']

            data.append(temp_row)
            data.append(cond_row)

        return data
