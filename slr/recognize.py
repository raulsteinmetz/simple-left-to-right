STACK = 's'
REDUCE = 'r'
NOP = 'n'
ACCEPT = 'ac'

def run_slr(grammar, tokens):
    tokens.append('$')

    rules = {}

    itr = 1
    for symbol in grammar['productions']:
        for production in grammar['productions'][symbol]:
            rules[itr] = [symbol, production]
            itr += 1


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

        try:
            op = slr_table[int(stack[-1])][tokens[0]]
            if op == '':
                return False
        except: # nop
            stack.append(str(slr_table[int(stack[-2])][stack[-1]][1]))
            continue

        if op[0] == STACK:
            stack.append(tokens[0])
            stack.append(str(op[1]))
            tokens = tokens[1:]
        
        elif op[0] == REDUCE:
            left, right = rules[op[1]]
            rstack = list(reversed(stack))
            right = list(reversed(right))
            itr = 0
            cut = 0
            for i in range(len(right)):
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