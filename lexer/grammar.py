import yaml
import json

def read_txt(fpath: str) -> str: # reads txt, returns string
    with open(fpath, 'r', encoding='utf-8') as file:
        return file.read()


def parse_yaml(fpath: str): # creates grammar dictionary from yaml definition
    with open(fpath, 'r') as file:
        data = yaml.safe_load(file)
    return {
        "initial_symbol": data.get("start-symbol"),
        "terminals": data.get("terminals"),
        "non_terminals": data.get("non-terminals"),
        "productions": data.get("productions")
    }


def grammar_to_string(grammar: dict): # turns dictionary into a string, exactly as the dict would be printed
    return json.dumps(grammar, separators=(',', ': '))


def nice_grammar_print(grammar: dict):
    print("====== Grammar ======")
    print("\nInitial Symbol:")
    print(f"  {grammar['initial_symbol']}")
    print("\nTerminals:")
    print(f"  {', '.join(grammar['terminals'])}")
    print("\nNon-Terminals:")
    print(f"  {', '.join(grammar['non_terminals'])}")
    print("\nProductions:")
    for non_term, productions in grammar['productions'].items():
        for production in productions:
            production_str = " ".join(production)
            print(f"  {non_term} -> {production_str}")
    print("=====================", end='\n'*3)