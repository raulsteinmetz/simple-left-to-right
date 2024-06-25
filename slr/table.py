def get_firsts(grammar: dict): # TODO: not working fully
    firsts = {nt: set() for nt in grammar['non_terminals']}
    productions = grammar['productions']

    for terminal in grammar['terminals']:
        firsts[terminal] = {terminal}

    changed = True
    while changed:
        changed = False
        for nt in grammar['non_terminals']:
            for production in productions.get(nt, []):
                for symbol in production:
                    if symbol in grammar['terminals']:
                        if symbol not in firsts[nt]:
                            firsts[nt].add(symbol)
                            changed = True
                        break
                    elif symbol in grammar['non_terminals']:
                        before_update = len(firsts[nt])
                        firsts[nt].update(firsts[symbol] - {'$'})
                        if '$' in firsts[symbol]:
                            continue
                        if len(firsts[nt]) != before_update:
                            changed = True
                        break
                    if symbol == '$':
                        if '$' not in firsts[nt]:
                            firsts[nt].add('$')
                            changed = True
                        break

    return {nt: list(firsts[nt]) for nt in firsts if nt in grammar['non_terminals']}


# firsts = get_firsts(grammar) # TODO: not working fully