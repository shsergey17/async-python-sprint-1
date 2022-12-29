import pytest, requests

from tasks import DataFetchingTask
from unittest import mock

# @pytest.mark.parametrize("city_name, expected_response", [
#     ("New York", ["New York", "clear", "20"])
# ])

# def test_make_request(city_name, expected_response):
#     task = DataFetchingTask()
#     response = task.make_request(city_name)
#     assert response == expected_response 

class MyGreatClass:
    def fetch_json(self, url):
        response = requests.get(url)
        return response.json()

# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'http://someurl.com/test.json':
        return MockResponse({"key1": "value1"}, 200)
    elif args[0] == 'http://someotherurl.com/anothertest.json':
        return MockResponse({"key2": "value2"}, 200)

    return MockResponse(None, 404)


