import json

def trim_json_whitespace(rawJSON):
    j = json.loads(rawJSON)
    return json.dumps(j)
