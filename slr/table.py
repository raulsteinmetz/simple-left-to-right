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

    # rule two
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

    def nice_print(self):
        for i in range(len(self.nodes)):
            print(f'Node {i}: \n')
            for prod in self.nodes[i].prods:
                print(prod)
            print('\n' * 3)

def make_rules_dict(grammar: dict):
    rules = {0: [grammar['initial_symbol'] + "'", [grammar['initial_symbol']]]}

    itr = 1
    for symbol in grammar['productions']:
        for production in grammar['productions'][symbol]:
            rules[itr] = [symbol, production]
            itr += 1

    return rules


def gen_table(grammar: dict):
    
    firsts = _get_firsts(grammar)
    follows = _get_follows(grammar)
    rules = make_rules_dict(grammar)


    # print(f'Firsts -> {firsts}', end='\n'*2)
    # print(f'Follows -> {follows}', end='\n'*2)
    # print(f'Rules -> {rules}', end='\n'*3)

    slr_graph = SlrGraph()


    def append_prods(node: SlrNode, non_term: str):
        # adds productions of a non terminal to a node in the graph
        for rule in rules.keys():
            if rules[rule][0] == non_term:
                to_append = (rules[rule][0], ['.'] + rules[rule][1])
                if to_append not in node.prods:
                    node.add_prod(to_append)

    # initial node
    i0 = SlrNode()
    init_prod = (rules[0][0], ['.'] + rules[0][1])
    i0.add_prod(init_prod)
    slr_graph.add_node(i0)

    itr = 0
    while len(slr_graph.nodes) > itr:
        current_node = slr_graph.nodes[itr]
        # adding all prods to current node
        for prod in current_node.prods:
            for i in range(len(prod[1])):
                if prod[1][i] == '.' and i == len(prod[1]) - 1:
                        break
                elif prod[1][i] == '.' and prod[1][i+1] in grammar['non_terminals']:
                    append_prods(current_node, prod[1][i+1])
        

        def check_for_existing_con(node: SlrNode, con_symbol: str):
            for symb, nd in node.cons:
                if symb == con_symbol:
                    return nd
            return None
            
        def check_for_existing_prod(prod):
            # not sure if this works yet
            for node in slr_graph.nodes:
                if prod in node.prods:
                    return node
            return None
        

        for prod in current_node.prods:
            new_prod_r = prod[1].copy()
            production_end = False
            for i in range(len(new_prod_r)):
                if i == len(new_prod_r) - 1:
                    production_end = True
                    break
                if new_prod_r[i] == '.':
                    new_prod_r[i] = new_prod_r[i+1]
                    new_prod_r[i+1] = '.'
                    con_symbol = new_prod_r[i]
                    break
        

            if production_end:
                continue

            new_prod = (prod[0], new_prod_r)

            nd = check_for_existing_con(current_node, con_symbol)
            nd2 = check_for_existing_prod(new_prod)

            if nd:
                # might have to check if prod already in node
                nd.add_prod(new_prod)
            elif nd2:
                # not sure if it works (untested)
                current_node.add_con(con_symbol, nd2)
            else:
                new_node = SlrNode()
                new_node.add_prod(new_prod)
                current_node.add_con(con_symbol, new_node) 
                slr_graph.add_node(new_node)


        slr_graph.nice_print()
        print('-' * 15)
        itr += 1
