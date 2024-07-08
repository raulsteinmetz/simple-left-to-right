import argparse
import ast

from lexer.grammar import read_txt, parse_yaml, nice_grammar_print
from lexer.lexer import tokenize_grammar, tokenize_word
from slr.slr import run_slr

def main(grammar_path: str, words_path: str):

    # creates dictionary for right linear grammar recognizer grammar
    grammar_recognizer = parse_yaml('./grammars/gld.yaml')

    # grammars can either be on txt or yaml
    if grammar_path.endswith('.yaml'):
        grammar_dict = parse_yaml(grammar_path)
    elif grammar_path.endswith('.txt'):
        grammar = read_txt(grammar_path)
        
        # verify if its a right linear grammar
        grammar_tokens = tokenize_grammar(grammar)
        # recognize grammar structure
        if not run_slr(grammar_recognizer, grammar_tokens):
            print('Grammar not recognized as a right-linear grammar')
            exit()
        
        print('Grammar is a correctly defined right-linear grammar.')
        # turn into dictionary for evaluating words
        grammar_dict = ast.literal_eval(grammar)


    nice_grammar_print(grammar_dict)

    word = 'dummy'
    while word != 'leave':
        word = str(input('Type your Word or "leave" enter to leave: '))
        _, tokens, _ = tokenize_word(grammar_dict, word)
        if run_slr(grammar_dict, tokens):
            print('Word Recognized by your grammar.')
        else:
            print('Word not recognized by your grammar.')

    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Recognize a grammar and test words on it')
    parser.add_argument('--grammar', type=str, default='./grammars/ops.yaml', help='Path to your grammar definition')
    parser.add_argument('--words', type=str, default='TODO', help='Path to the words to be tested on your grammar')
    args = parser.parse_args()
    
    main(args.grammar, args.words)
