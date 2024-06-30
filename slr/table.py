def _get_firsts(grammar: dict):
    '''
        if x is terminal, First(x) = {x},
        if X -> eps, eps in First(X),
        if X -> Y[...] and Y is non terminal, First(Y) in First(X)
    '''

    firsts = {}

    # rule 1, terminals
    for term in grammar['terminals']:
        firsts[term] = [term]

    # init on non_terminals first
    for non_term in grammar['non_terminals']:
        firsts[non_term] = []

    # rule two, eps
    for non_term in grammar['productions'].keys():
        for production in grammar['productions'][non_term]:
            if production == '&':
                firsts[non_term].append(production)
    

    # rule 3, first of X is a non terminal
    changed = True
    while changed:
        changed = False
        for non_term in grammar['productions'].keys():
            for production in grammar['productions'][non_term]:
                if production == '&':
                    continue
                for symbol in production:
                    if symbol in grammar['terminals']:
                        if symbol not in firsts[non_term]:
                            firsts[non_term].append(symbol)
                            changed = True
                        break
                    elif symbol in grammar['non_terminals']:
                        for sym_first in firsts[symbol]:
                            if sym_first not in firsts[non_term]:
                                firsts[non_term].append(sym_first)
                                changed = True
                        if '&' not in firsts[symbol]:
                            break
                    else:
                        break
                else:
                    if '&' not in firsts[non_term]:
                        firsts[non_term].append('&')
                        changed = True

    return firsts

def _get_follows(grammar: dict):
    '''
        $ in follow(S) if S is the initial symbol,
        if A -> [..]XB, First(B) in Follow(X) - b being terminal or not,
        if A -> [...]X or A -> [...]XB and B -> eps, Follow(A) in Follow(X) 
    '''

    firsts = _get_firsts(grammar)
    follows = {non_term: [] for non_term in grammar['non_terminals']}
    follows[grammar['initial_symbol']].append('$')

    changed = True
    while changed:
        _follows = {k: v[:] for k, v in follows.items()}
        changed = False
        for non_term in grammar['productions'].keys():
            for production in grammar['productions'][non_term]:
                follow_temp = follows[non_term][:]
                for i in range(len(production) - 1, -1, -1):
                    symbol = production[i]
                    if symbol in grammar['non_terminals']:
                        for follow in follow_temp:
                            if follow not in follows[symbol]:
                                follows[symbol].append(follow)
                                changed = True
                        if '&' in firsts[symbol]:
                            follow_temp.extend(first for first in firsts[symbol] if first != '&')
                        else:
                            follow_temp = firsts[symbol][:]
                    elif symbol in grammar['terminals']:
                        follow_temp = [symbol]

    return follows
    


class SlrNode:
    def __init__(self):
        self.prods = []
        self.cons = []

    def add_prod(self, prod: tuple):
        self.prods.append(prod)
    
    def add_con(self, symbol: str, node: 'SlrNode'):
        self.cons.append((symbol, node))

class SlrGraph:
    def __init__(self):
        self.nodes = []

    def add_node(self, node: 'SlrNode'):
        self.nodes.append(node)



def gen_table(grammar: dict):
    
    firsts = _get_firsts(grammar)
    follows = _get_follows(grammar)


    print(f'Firsts -> {firsts}', end='\n'*2)
    print(f'Follows -> {follows}', end='\n'*2)


    rules = {0: [grammar['initial_symbol'] + "'", [grammar['initial_symbol']]]}

    itr = 1
    for symbol in grammar['productions']:
        for production in grammar['productions'][symbol]:
            rules[itr] = [symbol, production]
            itr += 1


    print(f'Rules -> {rules}', end='\n'*3)

    slr_graph = SlrGraph()

    # initial node
    i0 = SlrNode()
    init_prod_l = rules[0][0]
    init_prod_r = ['.'] + rules[0][1]
    init_prod = (init_prod_l, init_prod_r)
    i0.add_prod(init_prod)
    slr_graph.add_node(i0)


    finished = False
    while not finished:
        pass

