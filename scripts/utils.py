import json


def parse_json_output(json_str: str) -> dict:
    json_str = json_str.replace("`", "").replace("json", "")
    json_dict = json.loads(json_str)
    return json_dict
