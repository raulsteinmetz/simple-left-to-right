from slr.movements import Action
from slr.table import gen_table

def run_slr(grammar, tokens):
    tokens.append('$')

    rules = {}

    itr = 1
    for symbol in grammar['productions']:
        for production in grammar['productions'][symbol]:
            rules[itr] = [symbol, production]
            itr += 1


    slr_table = gen_table(grammar)

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