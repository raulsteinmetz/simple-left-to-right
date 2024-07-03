import argparse

from lexer.grammar import parse_yaml, grammar_to_string, nice_grammar_print
from lexer.lexer import tokenize
from slr.slr import run_slr
from slr.table import gen_table

def main(grammar_path: str, words_path: str):
    grammar = parse_yaml(grammar_path)
    nice_grammar_print(grammar)
    gen_table(grammar)

    word = 'id + id * (id) * id'
    _, tokens, _ = tokenize(grammar, word)

    print(run_slr(grammar, tokens))

    

    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Recognize a grammar and test words on it')
    parser.add_argument('--grammar', type=str, default='./grammars/grammar_ops.yaml', help='Path to your grammar definition')
    parser.add_argument('--words', type=str, default='TODO', help='Path to the words to be tested on your grammar')
    args = parser.parse_args()
    
    main(args.grammar, args.words)
