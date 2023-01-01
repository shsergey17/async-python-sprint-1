import sys
import json
import os
import csv
import openpyxl

sys.path.append("../")

from src.file_types import JsonFileType, CsvFileType, XlsxFileType


def test_json_file():
    filename = "test_json.json"

    json_type = JsonFileType(filename)

    data = [["a", "b"], ["c", "d"]]
    json_type.save(data)

    with open(filename, "r") as file:
        assert json.load(file) == data

    os.remove(filename)


def test_csv_file():
    filename = "test_csv.csv"
    json_type = CsvFileType(filename)

    data = [["a", "b"], ["c", "d"]]
    json_type.save(data)

    with open(filename, "r") as csv_file:
        reader = csv.reader(csv_file)
        data_list = list(reader)
        assert data_list == data

    os.remove(filename)


def test_xlsx_file():
    filename = "test_xlsx.xlsx"
    json_type = XlsxFileType(filename)

    data = [["a", "b"], ["c", "d"]]
    json_type.save(data)

    result_data = _read_excel(filename)

    assert result_data == data

    os.remove(filename)


def _read_excel(filename):
    wb = openpyxl.load_workbook(filename)
    sheet = wb.active
    data = []
    for row in sheet.rows:
        row_data = []
        for cell in row:
            row_data.append(cell.value)
        data.append(row_data)
    return data
