import json
from src.entity import CityData, DateInfo


class PersonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (DateInfo, CityData)):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


def test_city_data():
    city_data = CityData(
        city_name="London",
        dates=[DateInfo("2022-12-01", 10.0, 2)],
        average_temp=10,
        average_condition=2,
    )
    city_data.rating = 5
    result = '{"city_name": "London", "dates": [{"date": "2022-12-01", "avg_temperature": 10.0, "sum_condition": 2}], "average_temp": 10, "average_condition": 2, "rating": 5}'
    json_data = json.dumps(city_data, cls=PersonEncoder)
    assert json_data == result
