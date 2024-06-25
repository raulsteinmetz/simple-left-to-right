import os
import argparse
import ply.lex as lex


from tools import parse_yaml, grammar_to_string
from slr.table import get_firsts # TODO
from slr.lexer import build_lexer # TODO 

STACK = 's'
REDUCE = 'r'
NOP = 'n'
ACCEPT = 'ac'

def recognize(grammar, word):
    word = ['id', '+', '(', 'id', ')', '$']
    rules = {
        1: ['E', ['E', '+', 'T']],
        2: ['E', ['T']],
        3: ['T', ['T', '*', 'F']],
        4: ['T', ['F']],
        5: ['F', ['(', 'E', ')']],
        6: ['F', ['id']]
    }

    slr_table = {
        0: {'id': [STACK, 5], '+': '', '*': '', '(': [STACK, 4], ')': '', '$': '', 'E': [NOP, 1], 'T': [NOP, 2], 'F': [NOP, 3]},
        1: {'id': '', '+': [STACK, 6], '*': '', '(': '', ')': '', '$': [ACCEPT], 'E': '', 'T': '', 'F': ''},
        2: {'id': '', '+': [REDUCE, 2], '*': [STACK, 7], '(': '', ')': [REDUCE, 2], '$': [REDUCE, 2], 'E': '', 'T': '', 'F': ''},
        3: {'id': '', '+': [REDUCE, 4], '*': [REDUCE, 4], '(': '', ')': [REDUCE, 4], '$': [REDUCE, 4], 'E': '', 'T': '', 'F': ''},
        4: {'id': [STACK, 5], '+': '', '*': '', '(': [STACK, 4], ')': '', '$': '', 'E': [NOP, 8], 'T': [NOP, 2], 'F': [NOP, 3]},
        5: {'id': '', '+': [REDUCE, 6], '*': [REDUCE, 6], '(': '', ')': [REDUCE, 6], '$': [REDUCE, 6], 'E': '', 'T': '', 'F': ''},
        6: {'id': [STACK, 5], '+': '', '*': '', '(': [STACK, 4], ')': '', '$': '', 'E': '', 'T': [NOP, 9], 'F': [NOP, 3]},
        7: {'id': [STACK, 5], '+': '', '*': '', '(': [STACK, 4], ')': '', '$': '', 'E': '', 'T': '', 'F': [NOP, 10]},
        8: {'id': '', '+': [STACK, 6], '*': '', '(': '', ')': [STACK, 11], '$': '', 'E': '', 'T': '', 'F': ''},
        9: {'id': '', '+': [REDUCE, 1], '*': [STACK, 7], '(': '', ')': [REDUCE, 1], '$': [REDUCE, 1], 'E': '', 'T': '', 'F': ''},
        10: {'id': '', '+': [REDUCE, 3], '*': [REDUCE, 3], '(': '', ')': [REDUCE, 3], '$': [REDUCE, 3], 'E': '', 'T': '', 'F': ''},
        11: {'id': '', '+': [REDUCE, 5], '*': [REDUCE, 5], '(': '', ')': [REDUCE, 5], '$': [REDUCE, 5], 'E': '', 'T': '', 'F': ''}
    }

    stack = [0]

    accepted = False
    while not accepted:
        print('stack: ', stack)
        print('word: ', word, end='\n\n')

        try:
            op = slr_table[int(stack[-1])][word[0]]
            if op == '':
                return False
        except: # nop
            stack.append(str(slr_table[int(stack[-2])][stack[-1]][1]))
            continue

        if op[0] == STACK:
            stack.append(word[0])
            stack.append(str(op[1]))
            word = word[1:]
        
        elif op[0] == REDUCE:
            left, right = rules[op[1]]
            rstack = list(reversed(stack))
            right = list(reversed(right))
            itr = 0
            cut = 0
            for i in range(len(right)):
                print('itr: ', itr)
                print('rstack: ', rstack)
                print('i: ', i)
                print('right: ', right)
                if str(rstack[itr]).isnumeric():
                    itr += 1
                    cut -= 1
                if rstack[itr] == right[i]:
                    itr += 1
                    cut -= 1
                else:
                    return False
            
            stack = stack[:cut]
            stack.append(left)


        elif op[0] == ACCEPT:
            accepted = True

    return True


def main(grammar_path: str, words_path: str):
    grammar = parse_yaml(grammar_path)
    grammar_str = grammar_to_string(grammar)


    accpt = recognize(grammar, '')

    print(accpt)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Recognize a grammar and test words on it')
    parser.add_argument('--grammar', type=str, default='./grammars/grammar_ops.yaml', help='Path to your grammar definition')
    parser.add_argument('--words', type=str, default='TODO', help='Path to the words to be tested on your grammar')
    args = parser.parse_args()
    
    main(args.grammar, args.words)



# id + id * id