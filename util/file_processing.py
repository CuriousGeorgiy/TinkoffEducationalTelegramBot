import json


def load_json_from_file(path: str):
    with open(path, 'r') as file:
        return json.load(file)


def load_json_string_from_file(path: str):
    return json.dumps(load_json_from_file(path))


def dump_json_string_to_file(json_string: str, path: str):
    with open(path, 'w') as file:
        json.dump(json.loads(json_string), file)
