# import logging
# import threading
# import subprocess
# import multiprocessing
import concurrent.futures
import queue, json
import threading
from concurrent.futures import as_completed
from concurrent.futures import ThreadPoolExecutor
from api_client import YandexWeatherAPI
from src.file_types import CsvFileType, IFileType, XlsxFileType, JsonFileType
from tasks import (
    DataFetchingTask,
    DataCalculationTask,
    DataAggregationTask,
    DataAnalyzingTask,
)
import logging
from utils import HOUR_FROM, HOUR_TO, WEATHER_CONDITION, CITIES, logger
from multiprocessing import Queue
from src.entity import CityData


def result(city_name: str) -> CityData:
    """
    Получает и обрабатывает данные о погоде для города.

    params:
    city_name (str): Имя города

    Returns:
    CityData: Объект города с данными
    """
    response = DataFetchingTask.make_request(city_name)
    threadId = threading.get_native_id()
    logger.debug('Thread: %s City: %s', threadId, city_name)

    task = DataCalculationTask(HOUR_FROM, HOUR_TO, WEATHER_CONDITION)
    if response is None or 'forecasts' not in response:
        logger.error(f"Bad response for city: {city_name}")
        raise ValueError(f"Bad response for city: {city_name}")

    return task.calc(city_name, response.get('forecasts'))


def forecast_weather(file: IFileType):
    logger.info("Starting weather forecast")
    with ThreadPoolExecutor() as pool:
        fetching_pool_outputs = pool.map(result, CITIES)

    city_data_list = []
    for item in fetching_pool_outputs:
        if item:
            city_data_list.append(item)

    aggregate = DataAggregationTask()
    aggregate.run(DataAnalyzingTask(), city_data_list)

    if aggregate.save_to_file(file, city_data_list):
        logger.info(f"Saved weather data to file: {file.filename}")
    else:
        logger.error(f"Failed to save weather data to file: {file.filename}")

    print(f"Best city: {aggregate.best_city.city_name}\nSave to file: {file.filename}")


# Run test: python -m pytest tests -v
if __name__ == "__main__":
    """ JsonFileType, CsvFileType, XlsxFileType"""

    file = XlsxFileType(filename = 'city')
    forecast_weather(file)

    # import resource
    # memory_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # print('Memory use: ' + str(round(memory_usage / 1024, 1)) + ' Mb')

