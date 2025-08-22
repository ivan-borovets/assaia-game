# Overview

Connect game for Assaia

See the original:
https://connect4.gamesolver.org/

## Installation

```shell
# sudo apt update
# sudo apt install pipx
# pipx ensurepath
# pipx install uv
# uv python install 3.12
uv v
source .venv/bin/activate
# .venv\Scripts\activate  # Windows
# https://docs.astral.sh/uv/getting-started/installation/#shell-autocompletion
uv pip install -e '.[dev]'
```

Don't forget to tell your IDE where the interpreter is located.

## Launch

```shell
assaia
```
