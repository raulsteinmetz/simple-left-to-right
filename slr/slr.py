from slr.movements import Action

def run_slr(grammar, tokens):
    tokens.append('$')

    rules = {}

    itr = 1
    for symbol in grammar['productions']:
        for production in grammar['productions'][symbol]:
            rules[itr] = [symbol, production]
            itr += 1


    slr_table = {
        0: {'id': [Action.STACK, 5], '+': '', '*': '', '(': [Action.STACK, 4], ')': '', '$': '', 'E': [Action.NOP, 1], 'T': [Action.NOP, 2], 'F': [Action.NOP, 3]},
        1: {'id': '', '+': [Action.STACK, 6], '*': '', '(': '', ')': '', '$': [Action.ACCEPT], 'E': '', 'T': '', 'F': ''},
        2: {'id': '', '+': [Action.REDUCE, 2], '*': [Action.STACK, 7], '(': '', ')': [Action.REDUCE, 2], '$': [Action.REDUCE, 2], 'E': '', 'T': '', 'F': ''},
        3: {'id': '', '+': [Action.REDUCE, 4], '*': [Action.REDUCE, 4], '(': '', ')': [Action.REDUCE, 4], '$': [Action.REDUCE, 4], 'E': '', 'T': '', 'F': ''},
        4: {'id': [Action.STACK, 5], '+': '', '*': '', '(': [Action.STACK, 4], ')': '', '$': '', 'E': [Action.NOP, 8], 'T': [Action.NOP, 2], 'F': [Action.NOP, 3]},
        5: {'id': '', '+': [Action.REDUCE, 6], '*': [Action.REDUCE, 6], '(': '', ')': [Action.REDUCE, 6], '$': [Action.REDUCE, 6], 'E': '', 'T': '', 'F': ''},
        6: {'id': [Action.STACK, 5], '+': '', '*': '', '(': [Action.STACK, 4], ')': '', '$': '', 'E': '', 'T': [Action.NOP, 9], 'F': [Action.NOP, 3]},
        7: {'id': [Action.STACK, 5], '+': '', '*': '', '(': [Action.STACK, 4], ')': '', '$': '', 'E': '', 'T': '', 'F': [Action.NOP, 10]},
        8: {'id': '', '+': [Action.STACK, 6], '*': '', '(': '', ')': [Action.STACK, 11], '$': '', 'E': '', 'T': '', 'F': ''},
        9: {'id': '', '+': [Action.REDUCE, 1], '*': [Action.STACK, 7], '(': '', ')': [Action.REDUCE, 1], '$': [Action.REDUCE, 1], 'E': '', 'T': '', 'F': ''},
        10: {'id': '', '+': [Action.REDUCE, 3], '*': [Action.REDUCE, 3], '(': '', ')': [Action.REDUCE, 3], '$': [Action.REDUCE, 3], 'E': '', 'T': '', 'F': ''},
        11: {'id': '', '+': [Action.REDUCE, 5], '*': [Action.REDUCE, 5], '(': '', ')': [Action.REDUCE, 5], '$': [Action.REDUCE, 5], 'E': '', 'T': '', 'F': ''}
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

        if op[0] == Action.STACK:
            stack.append(tokens[0])
            stack.append(str(op[1]))
            tokens = tokens[1:]
        
        elif op[0] == Action.REDUCE:
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


        elif op[0] == Action.ACCEPT:
            accepted = True

    return True