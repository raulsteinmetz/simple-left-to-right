def tokenize_word(grammar: dict, word: str):
    ''' returns success, token list, token not recognized (if it happened)'''
    word = word.replace(' ', '').replace('\t', '').replace('\n', '')

    tokens = []
    token = ''
    longest_match = ''
    while word:
        token += word[0]
        word = word[1:]

        matching_terminals = [i for i in grammar['terminals'] if i.startswith(token)]

        if matching_terminals:
            if token in matching_terminals:
                longest_match = token

            if not word or not any(i.startswith(token + word[0]) for i in matching_terminals):
                if longest_match and longest_match in grammar['terminals']:
                    tokens.append(longest_match)
                    token = ''
                    longest_match = ''
                else:
                    print(f"Unrecognized token: {token}")
                    print(tokens)
                    return False, tokens, token
        else:
            print(f"Unrecognized token: {token}")
            return False, tokens, token

    if longest_match:
        tokens.append(longest_match)

    return True, tokens, ''

def tokenize_grammar(grammar: str):
    tokens = []
    grammar = grammar.replace(' ', '').replace('\t', '').replace('\n', '')
    reserved_words = ['initial_symbol', 'terminals', 'non_terminals', 'productions']
    reserved_symbs = ['{', '}', "'", ':', ',', '[', ']']
    

    i = 0
    while i < len(grammar):
        if grammar[i] in reserved_symbs:
            tokens.append(grammar[i])
            i += 1
        elif any(grammar.startswith(word, i) for word in reserved_words):
            for word in reserved_words:
                if grammar.startswith(word, i):
                    tokens.append(word)
                    i += len(word)
                    break
        elif grammar[i].isupper():
            tokens.append('non_term')
            i += 1
        else:
            j = i
            while j < len(grammar) and not grammar[j].isupper() \
                and grammar[j] not in reserved_symbs \
                and not any(grammar.startswith(word, j) \
                for word in reserved_words):
                j += 1
            tokens.append('term')
            i = j

    return tokens
