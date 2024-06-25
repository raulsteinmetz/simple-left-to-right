# TODO: generalizable lexer creator given grammar

import ply.lex as lex

def build_lexer(grammar):
    terminals = grammar['terminals']

    token_name_map = {
        'id': 'ID',
        '+': 'PLUS',
        '*': 'TIMES',
        '(': 'OPB',
        ')': 'CLB',
        '$': 'DOLLAR'
    }

    tokens = [token_name_map[t] if t in token_name_map else t for t in terminals]


    t_ignore = ' \t'


    token_rules = {}
    for terminal in terminals:
        token_name = token_name_map.get(terminal, terminal)
        if terminal == 'id':
            rule = r'id'
        elif terminal in token_name_map:
            rule = fr'\{terminal}' if terminal in '()[]{}*+?$' else terminal
        token_rules[token_name] = rule


    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    lexer_attributes = {'tokens': tokens, 't_ignore': t_ignore, 't_error': t_error}
    for token, rule in token_rules.items():
        lexer_attributes[f't_{token}'] = rule

    lexer_class = type('DynamicLexer', (object,), lexer_attributes)

    return lex.lex(module=lexer_class)




# lexer = build_lexer(grammar)

# lexer.input(word)

# for tok in lexer:
#     print(tok.type, tok.value)
