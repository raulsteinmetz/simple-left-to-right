import yaml
import json


def parse_yaml(fpath: str):
    with open(fpath, 'r') as file:
        data = yaml.safe_load(file)
    return {
        "initial_symbol": data.get("start-symbol"),
        "terminals": data.get("terminals"),
        "non_terminals": data.get("non-terminals"),
        "productions": data.get("productions")
    }



def grammar_to_string(grammar: dict):
    return json.dumps(grammar, separators=(',', ': '))