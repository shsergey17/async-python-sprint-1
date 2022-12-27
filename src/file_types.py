from typing import List
from pathlib import Path
import csv
from abc import ABC, abstractmethod
from src.entity import CityData

# Формат сохраняемого файла - json, csv или xls/xlsx.

class IFileType(ABC):
    def __init__(self, filename: Path) -> None:
        self.filename = filename
    
    @abstractmethod
    def save(self, filename: str, data: List[CityData]):
        raise NotImplementedError()

class JsonFileType(IFileType):

    def save(self, data: List[CityData]):
        pass

class CsvFileType(IFileType):

    # Path("data.csv")
    def save(self, data: List[List[str]]):
        with open(self.filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in data:
                writer.writerow(row)

class XlsxFileType(IFileType):

    def save(self, data: List[CityData]):
        pass
