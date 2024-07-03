from slr.movements import Action

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

def gen_graph(grammar: dict, rules: dict):
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

    for current_node in slr_graph.nodes:
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
                nd.add_prod(new_prod)
            elif nd2:
                current_node.add_con(con_symbol, nd2)
            else:
                new_node = SlrNode()
                new_node.add_prod(new_prod)
                current_node.add_con(con_symbol, new_node) 
                slr_graph.add_node(new_node)


    return slr_graph


def nice_table_print(table: dict):
    for key in table.keys():
        print(key, table[key])
        print()


def gen_table(grammar: dict):
    
    firsts = _get_firsts(grammar)
    follows = _get_follows(grammar)
    rules = make_rules_dict(grammar)


    print(f'Firsts -> {firsts}', end='\n'*2)
    print(f'Follows -> {follows}', end='\n'*2)
    print(f'Rules -> {rules}', end='\n'*3)
    print('=====================', end='\n\n')

    graph = gen_graph(grammar, rules)    
    graph.nice_print()
    print('=====================', end='\n\n')


    '''
        1. if there is a production A -> [...].terminal, verify the connection for a, which node goes to
        table[i, a] = stack connected node

        2. if there is a production A -> [...]., for each a in follow of A, table[i, a] = reduce the rule A -> [...]

        3. if S' -> S. is in node, table[node, $] = accept

        4. if there a connection with a non_terminal in the node, table[i, non_terminal] = connected node
    '''

    # initialize the table with empty values

    table = {}
    for i in range(len(graph.nodes)):
        table[i] = {}

    for i in range(len(graph.nodes)):
        for j in grammar['terminals'] + ['$'] + grammar['non_terminals']:
            table[i][j] = ''


    # rule 1 and 4
    for node in graph.nodes:
        index = graph.nodes.index(node)
        for symbol, node_ in node.cons:
            index_ = graph.nodes.index(node_)
            if symbol in grammar['terminals']:
                table[index][symbol] = [Action.STACK, index_]
            else:
                table[index][symbol] = [Action.NOP, index_]

    # rule 2
    def get_key_from_value(target_value):
        for key, value in rules.items():
            if value == target_value:
                return key
        return None
    
    for node in graph.nodes:
        index = graph.nodes.index(node)
        for prod_l, prod_r in node.prods:
            if prod_r[-1] == '.':
                rule_index = get_key_from_value([prod_l, prod_r[:-1]])
                if prod_l == grammar['initial_symbol'] + "'":
                    continue
                for symbol in follows[prod_l]:
                    table[index][symbol] = [Action.REDUCE, rule_index] if not table[index][symbol] else table[index][symbol] # ambiguity favors stack

            
    # rule 3
    for node in graph.nodes:
        first_rule = (grammar['initial_symbol'] + "'", [grammar['initial_symbol'], '.'])
        if first_rule in node.prods:
            index = graph.nodes.index(node)
            table[index]['$'] = [Action.ACCEPT]

    




    nice_table_print(table)
    print('=====================', end='\n\n')


