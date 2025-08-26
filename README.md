# Overview

Connect-N for Assaia (hotseat).  
Inspired by https://connect4.gamesolver.org/

# Features:

* Connect-N on configurable grid (3–20 × 3–20), connect ≥3
* Hotseat multiplayer: 2–26 players
* Guided setup with sensible defaults; strict input validation
* Interdependent limits: grid bounds connect; size+connect bounds players
* Turn flow: pick column 1..N; full/out-of-range rejected with clear message
* Win detection in 4 directions; draw on full board or early-draw
* Winnability pre-check; impossible configurations rejected
* Early-draw detection to stop unwinnable games mid-way (always on)
* CLI board renderer: clean ASCII grid, column numbers, row labels
* Player symbols: single char, unique; safe against empty-cell marker
* UI tuning via config: cell width, gutter, empty-cell marker, prompt prefix
* Clean Architecture; easy to swap/extend UI or rules later

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
uv pip install -e .
# uv pip install -e '.[dev]'  # For development
# Don't forget to tell your IDE where the interpreter is located.
```

## Launch

```shell
assaia
```
