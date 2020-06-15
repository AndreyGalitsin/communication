import requests
import json

data = {
        'one': 1,
        'two': 2
        }


res = requests.post("http://localhost:9902", data=json.dumps(data))

print('res', res)