def tokenize(grammar: dict, word: str):
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