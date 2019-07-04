import json


def load_json_from_file(path):
    with open(path, 'r') as file:
        return json.load(file)