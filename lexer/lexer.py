def tokenize_word(grammar: dict, word: str):
    ''' returns success, token list, token not recognized (if it happened)'''

    # takes out spaces, tabs and line breaks
    word = word.replace(' ', '').replace('\t', '').replace('\n', '')

    tokens = []
    token = ''
    longest_match = ''
    while word: # only one iteration over the world
        token += word[0]
        word = word[1:]

        # list of terminals that start with the same characters as our current token
        matching_terminals = [i for i in grammar['terminals'] if i.startswith(token)]

        if matching_terminals: # if the list contains a terminal
            if token in matching_terminals: # is our token equal to one of the terminals?
                longest_match = token

            # in case the word has ended (all characters have been read) or 
            # we do not have any terminal that starts with our token + the next character to be read
            # check if we have already found a match (longest_match) and recognize the token
            # else error
            if not word or not any(i.startswith(token + word[0]) for i in matching_terminals):
                if longest_match and longest_match in grammar['terminals']:
                    tokens.append(longest_match)
                    token = ''
                    longest_match = ''
                else:
                    print(f"Unrecognized token: {token}")
                    print(tokens)
                    return False, tokens, token
        else: # no terminal starts with our token, not recognized
            print(f"Unrecognized token: {token}")
            return False, tokens, token

    if longest_match: # in case the word has ended and we still have a token to be recognized
        tokens.append(longest_match)

    return True, tokens, ''

def tokenize_grammar(grammar: str):
    ''' returns a list of tokens from the grammar string '''

    tokens = []

    # takes out spaces, tabs and line breaks
    grammar = grammar.replace(' ', '').replace('\t', '').replace('\n', '')

    # define reserved words and symbols used in the grammar definition
    reserved_words = ['initial_symbol', 'terminals', 'non_terminals', 'productions']
    reserved_symbs = ['{', '}', "'", ':', ',', '[', ']']

    i = 0
    while i < len(grammar):
        if grammar[i] in reserved_symbs: # if the character is a reserved symbol
            tokens.append(grammar[i])
            i += 1
        elif any(grammar.startswith(word, i) for word in reserved_words): # if the character starts a reserved word
            for word in reserved_words:
                if grammar.startswith(word, i):
                    tokens.append(word)
                    i += len(word)
                    break
        elif grammar[i].isupper(): # upper letters are recognized as non-terminals
            tokens.append('non_term')
            i += 1
        else:
            # extract terminals until we find a reserved symbol, reserved word, or non-terminal
            j = i
            while j < len(grammar) and not grammar[j].isupper() \
                and grammar[j] not in reserved_symbs \
                and not any(grammar.startswith(word, j) \
                for word in reserved_words):
                j += 1
            tokens.append('term')
            i = j

    return tokens