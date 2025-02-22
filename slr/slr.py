from slr.movements import Action
from slr.table import gen_table, make_rules_dict

def run_slr(grammar, tokens, print_derivation=False):
    rules = {}

    # creates the numerated set of rules (used for reduction)
    rules = make_rules_dict(grammar)


    # generates table
    slr_table = gen_table(grammar)

    tokens.append('$')
    stack = [0]
    derivations = []

    accepted = False
    while not accepted:
        try:
            op = slr_table[int(stack[-1])][tokens[0]]
            if op == '':
                print(f'Error: No operation found for {stack[-1]} and {tokens[0]}')
                return False
        except: # nop will not be found with (stack[-1], token), but with (stack[-2], stack[-1])
            try:
                stack.append(str(slr_table[int(stack[-2])][stack[-1]][1]))
            except:
                print(f'Error: No operation found for {stack[-2]} and {stack[-1]}')
                return False
            continue

        if op[0] == Action.STACK:
            stack.append(tokens[0])
            stack.append(str(op[1]))
            tokens = tokens[1:]
        
        elif op[0] == Action.REDUCE:
            left, right = rules[op[1]]
            rstack = list(reversed(stack))
            right = list(reversed(right))
            if right == ['&']:
                stack.append(left)
                continue
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
            derivations.append((left, list(reversed(right))))

        elif op[0] == Action.ACCEPT:
            accepted = True
        
    if print_derivation:
        print("".join(derivations[-1][0]) + ' -> ' + "".join(derivations[-1][1]))
        current_derivation = derivations[-1][1]
        for i in reversed(range(len(derivations) - 1)):
            print('Rule used: ' + "".join(derivations[i][0]) + "->" + "".join(derivations[i][1]))
            print("".join(current_derivation), end=' ')
            if str(current_derivation[-1]).isupper():
                current_derivation = current_derivation[:-1]
                current_derivation += derivations[i][1]

            print('-> ' + "".join(current_derivation))

    return True