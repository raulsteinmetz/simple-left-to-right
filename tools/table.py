# firsts = get_firsts(grammar) # TODO: not working fully

def get_firsts(grammar: dict):
    '''
        if x is terminal, First(x) = {x},
        if X -> eps, eps in First(X),
        if X -> Y[...] and Y is non terminal, First(Y) in First(X)
    '''
    pass


def get_follows(grammar:dict):
    '''
        $ in follow(S) if S is the initial symbol,
        if A -> [..]XB, First(B) in Follow(X) - b being terminal or not,
        if A -> [...]X or A -> [...]XB and B -> eps, Follow(A) in Follow(X) 
    '''
    pass


def gen_table(grammar: dict):
    pass