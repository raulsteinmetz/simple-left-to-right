import argparse
import ast

from lexer.grammar import read_txt, parse_yaml, nice_grammar_print
from lexer.lexer import tokenize_grammar, tokenize_word
from slr.slr import run_slr
from slr.table import gen_table

def main(grammar_path: str, words_path: str):

    if grammar_path.endswith('.yaml'):
        grammar = parse_yaml(grammar_path)
    else: # its a txt
        grammar = read_txt(grammar_path)

        # verify if its a right linear grammar
        grammar = tokenize_grammar(grammar)
        exit()

        # turn into dictionary for evaluating words
        grammar = ast.literal_eval(grammar)

    nice_grammar_print(grammar)
    gen_table(grammar)

    word = str(input('Word: '))
    _, tokens, _ = tokenize_word(grammar, word)

    print(run_slr(grammar, tokens))

    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Recognize a grammar and test words on it')
    parser.add_argument('--grammar', type=str, default='./grammars/ops.yaml', help='Path to your grammar definition')
    parser.add_argument('--words', type=str, default='TODO', help='Path to the words to be tested on your grammar')
    args = parser.parse_args()
    
    main(args.grammar, args.words)
