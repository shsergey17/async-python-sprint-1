import os
from api_client import YandexWeatherAPI
from statistics import mean
from dataclasses import dataclass
from typing import List, Tuple, Type
from pathlib import Path
from src.entity import CityData, DateInfo
from src.file_types import IFileType
from utils import HOUR_FROM, HOUR_TO, WEATHER_CONDITION, logger


class DataFetchingTask:
    @staticmethod
    def make_request(city_name: str) -> dict:
        """
        Делает запрос к API погоды Яндекса для указанного города и возвращает ответ.

        Params:
        city_name (str): Название города

        Returns:
        list: ответ API погоды Яндекса.
        """
        ywAPI = YandexWeatherAPI()
        logger.info("Making request to Yandex Weather API for city: %s", city_name)
        resp = ywAPI.get_forecasting(city_name)
        logger.debug("API response: %s", resp)

        return resp.get("forecasts", {})


class DataCalculationTask:
    def __init__(
        self, hour_from: int, hour_to: int, weather_condition: list[str]
    ) -> None:
        """
        Params:
        hour_from (int): начальный час для расчетов.
        hour_to (int): конечный час для расчетов.
        weather_condition (list[str]): погодные условия для дней без осадков, которые следует учитывать при расчетах
        """

        self.hour_from = hour_from
        self.hour_to = hour_to
        self.weather_condition = weather_condition

    def calc(self, city_name: str, data: list) -> CityData:
        """
        Вычисляет среднюю температуру и среднее сумма часов без осадков для города

        Params:
        city_name (str): Название города
        data (list): данные по городу

        Returns:
        CityData: объект, содержащий рассчитанную статистику для города
        """
        logger.info("Calculating statistics for city: %s", city_name)

        date_info_list = self.day_calc(data)

        logger.debug("Date list: %s", date_info_list)

        avg_temp = self.average(date_info_list, "avg_temperature")
        avg_condition = self.average(date_info_list, "sum_condition")

        logger.debug("Average temperature: %s", avg_temp)
        logger.debug("Average condition: %s", avg_condition)

        return CityData(
            city_name=city_name,
            dates=date_info_list,
            average_temp=avg_temp,
            average_condition=avg_condition,
        )

    def avg(self, value, length: int) -> float:
        if length == 0:
            return 0
        return round(value / length, 1)

    def average(self, data: List[DateInfo], field: str) -> float:
        total_sum = sum([getattr(date_info, field) for date_info in data])
        count = len(data)

        return self.avg(total_sum, count)

    def day_calc(self, data: list) -> List[DateInfo]:
        """
        Рассчитывает температуру и сумму часов без осадков за каждый день

        Params:
        data (list): Данные для обработки

        Returns:
        List[DateInfo]: Список объектов DateInfo, содержащих рассчитанную статистику за каждый день.
        """

        logger.info("Calculating statistics for days")

        temperate_dict = []
        for date_item in data:

            try:
                hours_list = date_item.get("hours")
                date_str = date_item.get("date")
            except Exception as e:
                logger.error("Error extracting data from date item: %s", e)

            if not hours_list:
                continue

            temperatures, hours_sum_condition = self.hour_calc(hours_list)

            hours_average_temperature = self.avg(sum(temperatures), len(temperatures))

            temperate_dict.append(
                DateInfo(date_str, hours_average_temperature, hours_sum_condition)
            )

        return temperate_dict

    def hour_calc(self, hours_list: list) -> Tuple[List[float], int]:
        """
        Рассчитывает температуру и погодные условия за каждый час

        Средняя температура рассчитывается за промежуток времени
        self.hour_from и self.hour_to, игнорируя осадки, т.к.
        не указано в условии

        Сумма времени (часов), когда погода без осадков, рассчитывается
        за указанный промежуток времени

        see tests/test_day_calc_temp

        Params:
        hours_list (list): Список данных по часам

        Returns:
        Tuple[List[float], int]: Список температуры и сумму часов без осадков
        """

        logger.info("Calculating statistics for hours")

        temperatures = []
        day_sum_condition = 0

        for hour_item in hours_list:

            current_hour = int(hour_item.get("hour"))
            hour_temp = int(hour_item.get("temp"))
            hour_condition = str(hour_item.get("condition"))

            # Check if the current hour is within the desired range
            if self.hour_from <= current_hour <= self.hour_to:

                if current_hour and hour_temp:
                    temperatures.append(hour_temp)

                if hour_condition in self.weather_condition:
                    day_sum_condition += 1

        return temperatures, day_sum_condition


class DataAnalyzingTask:
    def calc_rating(self, city_data: list[CityData]) -> list[CityData]:
        """
        Добавляет рейтинг городу
        Путем сортировки по средней температуре и средней сумме часов без осадков

        Params:
        city_data (list[CityData]): список объектов с данными по городам для обработки

        Returns:
        list[CityData]: список объектов с данными по городам с рассчитанными рейтингами
        """
        logger.info("Calculating ratings for cities")

        sort_city_data = self.sort_by_temp_and_condition(city_data)
        for i, city_data in enumerate(sort_city_data):
            city_data.rating = len(sort_city_data) - i

        return sort_city_data

    def sort_by_temp_and_condition(self, city_data: list[CityData]) -> list[CityData]:
        """
        Сортирует список объектов с данными по городам по средней температуре и средней сумме часов без осадков.
        Сортировка по ср. температуре и ср. сумме дней по погодным условиям
        Большая ср. температура и большая ср. сумма погоды - выше

        Пример как в sql: order by average_temp DESC, average_condition DESC

        Params:
        city_data (list[CityData]): список объектов с данными по городам для сортировки.

        Returns:
        list[CityData]: отсортированный список объектов с данными по городам

        """
        logger.info("Sorting city data by temperature and condition")
        return sorted(city_data, key=lambda x: (-x.average_temp, -x.average_condition))


class DataAggregationTask:
    def __init__(self) -> None:
        self.best_city = None

    def run(self, data_analyzing: DataAnalyzingTask, city_data: list[CityData]):
        """
        Запускает анализ данных по списку объектов городов и выбирает лучший город на основе результатов.

        Params:
        data_analyzing (DataAnalyzingTask): Используется для анализа
        city_data (list[CityData]): Список городов

        Returns: self

        """
        logger.info("Running analysis on city data")

        if not city_data:
            raise ValueError("CityData empty")

        city_with_rating_list = data_analyzing.calc_rating(city_data)
        self.best_city = city_with_rating_list[0]
        return self

    def save_to_file(self, file_type: IFileType, city_data: list[CityData]) -> bool:
        """
        Сохраняет данные по городам в файл

        params:
        file_type (IFileType): тип файла, используемый для сохранения данных
        city_data (list[CityData]): список городов с данными

        Returns:
        bool: True если успешно и файл существует, False в противном случае.
        """

        logger.info("Saving data to file")

        prepare_table = self.make_data_list(city_data)
        file_type.save(prepare_table)
        return os.path.isfile(file_type.filename)

    def make_data_list(self, city_data_list: List[CityData]) -> List[List[str]]:
        """
        Подготавливаем таблицу для сохранение

        Params:
        city_data_list (List[CityData]): Список городов с данными

        Returns:
        List[List[str]]: Подготовленный список-таблица для сохранения
        """
        logger.info("Preparing data for saving to file")

        dates = [
            date_info.date
            for city_data in city_data_list
            for date_info in city_data.dates
        ]
        dates = list(set(dates))

        data = [["Город/день", ""] + dates + ["Среднее", "Рейтинг"]]

        for city_data in city_data_list:
            temp_row = (
                [city_data.city_name, "Температура, среднее"]
                + [str(date.avg_temperature) for date in city_data.dates]
                + [str(city_data.average_temp), str(city_data.rating)]
            )
            cond_row = (
                ["", "Без осадков, часов"]
                + [str(date.sum_condition) for date in city_data.dates]
                + [str(city_data.average_condition), ""]
            )

            data.append(temp_row)
            data.append(cond_row)

        return data
