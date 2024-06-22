import os
import argparse
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

def get_firsts(grammar: dict):
    firsts = {nt: set() for nt in grammar['non_terminals']}
    productions = grammar['productions']

    for terminal in grammar['terminals']:
        firsts[terminal] = {terminal}

    changed = True
    while changed:
        changed = False
        for nt in grammar['non_terminals']:
            for production in productions.get(nt, []):
                for symbol in production:
                    if symbol in grammar['terminals']:
                        if symbol not in firsts[nt]:
                            firsts[nt].add(symbol)
                            changed = True
                        break
                    elif symbol in grammar['non_terminals']:
                        before_update = len(firsts[nt])
                        firsts[nt].update(firsts[symbol] - {'$'})
                        if '$' in firsts[symbol]:
                            continue
                        if len(firsts[nt]) != before_update:
                            changed = True
                        break
                    if symbol == '$':
                        if '$' not in firsts[nt]:
                            firsts[nt].add('$')
                            changed = True
                        break

    return {nt: list(firsts[nt]) for nt in firsts if nt in grammar['non_terminals']}

def main(grammar_path: str, words_path: str):
    grammar = parse_yaml(grammar_path)
    grammar_str = grammar_to_string(grammar)
    firsts = get_firsts(grammar)

    print(grammar_str)
    print(firsts)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Recognize a grammar and test words on it')
    parser.add_argument('--grammar_path', type=str, default='./grammars/right-linear.yaml', help='Path to your grammar definition')
    parser.add_argument('--words_path', type=str, default='TODO', help='Path to the words to be tested on your grammar')
    args = parser.parse_args()
    
    main(args.grammar_path, args.words_path)
