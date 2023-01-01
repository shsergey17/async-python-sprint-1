from typing import List
import csv, json
import openpyxl
from abc import ABC, abstractmethod


"""
Форматы сохраняемого файла - json, csv или xls/xlsx.
"""


class IFileType(ABC):
    """
    Интерфейс для форматов файлов
    """

    def __init__(self, filename: str) -> None:
        """
        Params:
        filename (str): имя файла
        ext (str): принудительно переопределяемое расширение для файла
        """
        self.filename = filename

    @abstractmethod
    def save(self, data: List[List[str]]):
        """
        Сохранение данных в файл
        Метод необходимо переопределить

        Params:
        filename (str): имя файла
        data (List[CityData]): данные

        Raises:
        NotImplementedError: Если метод не реализован в подклассе
        """
        raise NotImplementedError()


class JsonFileType(IFileType):
    """
    Сохранение данных в формате json
    """

    def save(self, data: List[List[str]]):
        json_data = json.dumps(data, ensure_ascii=False)

        with open(self.filename, "w") as file:
            file.write(json_data)


class CsvFileType(IFileType):
    """
    Сохранение данных в формате csv
    """

    def save(self, data: List[List[str]]):
        with open(self.filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for row in data:
                writer.writerow(row)


class XlsxFileType(IFileType):
    """
    Сохранение данных в формате xlsx
    """

    def save(self, data: List[List[str]]):
        wb = openpyxl.Workbook()
        sheet = wb.active
        for row in data:
            sheet.append(row)
        wb.save(self.filename)
