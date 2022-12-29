from typing import List
from dataclasses import dataclass
import dataclasses, json

class EnhancedJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            return super().default(o)

@dataclass
class ApiResponse:
    now: int
    geo_object: dict
    forecasts: List


jsondata = '''
    {
        "now": 1653557278,
        "geo_object": {"locality": "Étréchy"},
        "forecasts": [{"hello": true}]
    }
'''


data = ApiResponse(jsondata)
print(data)


