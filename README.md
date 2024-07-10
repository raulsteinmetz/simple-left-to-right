# Simple Left-to-Right (SLR) Analyzer in Python

This repository hosts an automatic SLR analyzer. It takes in a grammar, creates the SLR graph and SLR table, and analyzes words inputted by the user.

The `main.py` script receives the following arguments:

- `--grammar`: Path to the grammar file, which can be in YAML or TXT format. Refer to the examples in `./grammars` to see how to define a grammar file.
- `--checkrl`: When passed, the grammar in `./grammars/rl.yaml` will be used to check if the specified grammar is right linear (using the SLR algorithm).

After processing these arguments, the main script will build your grammar inside the program and analyze any word you provide.

## Repository Structure

- `./grammars`: Contains grammar examples.
- `./lexer/grammar.py`: Contains utility code for parsing files and transforming grammars.
- `./lexer/lexer.py`: Contains functions for tokenizing words and grammars (the latter for the right linear check).
- `./slr/table.py`: Contains code for generating the SLR table.
- `./slr/slr.py`: Contains the main analyzer code.
