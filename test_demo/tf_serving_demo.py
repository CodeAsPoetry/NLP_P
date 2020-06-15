import requests
import json

url_path = "http://localhost:8503/v1/models/sa_triple_classification:predict"
data = {
    "instances": [
        {
            "input_ids_ph": [
                [101, 872, 703, 4696, 4281, 6873, 8013, 102, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "input_mask_ph": [
                [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0]
            ],
            "segment_ids_ph": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0]
            ]
        }
    ]
}

r = requests.post(url_path, data=json.dumps(data))

print(r.text)
