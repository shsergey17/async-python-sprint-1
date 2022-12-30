from typing import List
from dataclasses import dataclass
import dataclasses, json

from src.entity import CityData, DateInfo
from tasks import DataAggregationTask

class PersonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (DateInfo, CityData)):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
# class EnhancedJSONEncoder(json.JSONEncoder):
#         def default(self, o):
#             if dataclasses.is_dataclass(o):
#                 return dataclasses.asdict(o)
#             return super().default(o)

# @dataclass
# class ApiResponse:
#     now: int
#     geo_object: dict
#     forecasts: List


# jsondata = '''
#     {
#         "now": 1653557278,
#         "geo_object": {"locality": "Étréchy"},
#         "forecasts": [{"hello": true}]
#     }
# '''


# data = ApiResponse(jsondata)
city_data = CityData(
    city_name="London",
    dates=[DateInfo('2022-12-01', 10.0, 2)],
    average_temp=10,
    average_condition=2,
)
import shutil


# print(json.dumps(city_data, cls=PersonEncoder))
# import io
# file = io.StringIO('test')
# file.seek(0)
# with open(file, "w") as file:
#     file.write('test')

# with open(file, "r") as file:
#     file.write('test')

import io

file = io.StringIO('test')

with open(file, "w") as file:
    file.write("Hello, world!")

with open(file, "r") as file:
    contents = file.read()
    print(contents)




# import json

# city_data = CityData(
#     city_name="London",
#     dates=[DateInfo('2022-12-01', 10.0, 2)],
#     average_temp=10,
#     average_condition=2,
# )

# json_data = json.dumps(city_data.__dict__)

# assert json_data == '{"city_name": "London", "dates": [{"date": "2022-12-01", "avg_temperature": 10, "sum_condition": 2}], "average_temp": 10, "average_condition": 2}'
