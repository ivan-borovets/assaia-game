from dataclasses import dataclass, field
from typing import Final

CONNECT_TO_WIN: Final[int] = 4
DEFAULT_ROWS: Final[int] = 6
DEFAULT_COLS: Final[int] = 7
MIN_PLAYERS: Final[int] = 2
DEFAULT_PLAYER_COUNT: Final[int] = 2
MAX_ROWS: Final[int] = 20
MAX_COLS: Final[int] = 20
EMPTY_CELL: Final[str] = "·"
CELL_WIDTH: Final[int] = 3


@dataclass(slots=True, kw_only=True)
class Player:
    name: str
    symbol: str


@dataclass(slots=True, kw_only=True)
class Move:
    row: int
    col: int
    symbol: str


@dataclass(slots=True, kw_only=True)
class Board:
    rows: int = DEFAULT_ROWS
    cols: int = DEFAULT_COLS
    last_move: Move | None = None
    _grid: list[list[str | None]] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if not (CONNECT_TO_WIN <= self.rows <= MAX_ROWS):
            raise ValueError(f"Rows must be between {CONNECT_TO_WIN} and {MAX_ROWS}.")
        if not (CONNECT_TO_WIN <= self.cols <= MAX_COLS):
            raise ValueError(
                f"Columns must be between {CONNECT_TO_WIN} and {MAX_COLS}."
            )
        self._grid = [[None] * self.cols for _ in range(self.rows)]

    def place_symbol(self, col: int, symbol: str) -> Move:
        if not (0 <= col < self.cols):
            raise ValueError("Column out of range.")
        for row in range(self.rows - 1, -1, -1):
            if self._grid[row][col] is None:
                self._grid[row][col] = symbol
                self.last_move = Move(row=row, col=col, symbol=symbol)
                return self.last_move
        raise ValueError("Column is full.")

    def symbol_at(self, row: int, col: int) -> str | None:
        return self._grid[row][col]

    def available_columns(self) -> list[int]:
        first_row = self._grid[0]
        return [col for col, cell in enumerate(first_row) if cell is None]

    @property
    def is_full(self) -> bool:
        return None not in self._grid[0]


@dataclass(slots=True, kw_only=True)
class Referee:
    connect_to_win: int = CONNECT_TO_WIN

    def is_winning(self, board: Board, last: Move) -> bool:
        row, col, symbol = last.row, last.col, last.symbol

        def line_len(delta_row: int, delta_col: int) -> int:
            total = 1
            r, c = row + delta_row, col + delta_col
            while (
                0 <= r < board.rows
                and 0 <= c < board.cols
                and board.symbol_at(r, c) == symbol
            ):
                total += 1
                r += delta_row
                c += delta_col
            r, c = row - delta_row, col - delta_col
            while (
                0 <= r < board.rows
                and 0 <= c < board.cols
                and board.symbol_at(r, c) == symbol
            ):
                total += 1
                r -= delta_row
                c -= delta_col
            return total

        for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
            if line_len(dr, dc) >= self.connect_to_win:
                return True
        return False


@dataclass(slots=True, kw_only=True)
class ConsoleUI:
    empty_cell: str = EMPTY_CELL
    cell_width: int = CELL_WIDTH

    def render_board(self, board: Board) -> None:
        col_w = self.cell_width
        row_w = max(2, len(str(board.rows)))
        indent = " " * (row_w + 1)

        header = (
            indent
            + "│"
            + "│".join(f"{i:^{col_w}}" for i in range(1, board.cols + 1))
            + "│"
        )
        top = indent + "┌" + "┬".join("─" * col_w for _ in range(board.cols)) + "┐"
        bottom = indent + "└" + "┴".join("─" * col_w for _ in range(board.cols)) + "┘"

        print(header)
        print(top)
        for row in range(board.rows):
            cells = [
                f"{(board.symbol_at(row, col) or self.empty_cell):^{col_w}}"
                for col in range(board.cols)
            ]
            line = f"{board.rows - row:>{row_w}} " + "│" + "│".join(cells) + "│"
            print(line)
        print(bottom)

    def prompt_number(
        self,
        prompt: str,
        default: int | None = None,
        *,
        min_value: int = 0,
        max_value: int | None = None,
    ) -> int:
        hint = f" [{default}]" if default is not None else ""
        while True:
            raw = input(f"{prompt}{hint}: ").strip()
            value_str = raw or (str(default) if default is not None else "")
            try:
                value = int(value_str)
            except ValueError:
                print("Enter a valid integer.")
                continue
            if value < min_value or (max_value is not None and value > max_value):
                hi = f" and ≤ {max_value}" if max_value is not None else ""
                print(f"Value must be ≥ {min_value}{hi}.")
                continue
            return value

    def prompt_players(self, default_count: int = DEFAULT_PLAYER_COUNT) -> list[Player]:
        def suggest_symbol(index: int) -> str:
            return (
                "X"
                if index == 0
                else ("O" if index == 1 else chr(65 + (index - 2) % 26))
            )

        count = self.prompt_number(
            "Number of players (≥2)", default=default_count, min_value=MIN_PLAYERS
        )
        players: list[Player] = []
        used: set[str] = set()
        for index in range(count):
            name_default = f"Player {index + 1}"
            name = (
                input(f"Player {index + 1} name [{name_default}]: ").strip()
                or name_default
            )
            while True:
                symbol = input(
                    f"{name} symbol (single character) [{suggest_symbol(index)}]: "
                ).strip() or suggest_symbol(index)
                if len(symbol) != 1:
                    print("Symbol must be exactly one character.")
                    continue
                if symbol in used:
                    print("Symbol already taken. Choose another.")
                    continue
                used.add(symbol)
                players.append(Player(name=name, symbol=symbol))
                break
        return players

    def prompt_board_setup(self) -> tuple[int, int, int]:
        rows = self.prompt_number(
            "Rows", default=DEFAULT_ROWS, min_value=CONNECT_TO_WIN, max_value=MAX_ROWS
        )
        cols = self.prompt_number(
            "Columns",
            default=DEFAULT_COLS,
            min_value=CONNECT_TO_WIN,
            max_value=MAX_COLS,
        )
        connect = self.prompt_number(
            "In-a-row to win",
            default=CONNECT_TO_WIN,
            min_value=3,
            max_value=max(rows, cols),
        )
        return rows, cols, connect

    def prompt_column(self, player: Player, board: Board) -> int:
        print(
            f"{player.name} to move ({player.symbol}). Choose a column 1..{board.cols}."
        )
        while True:
            raw = input("> ").strip()
            if not raw.isdigit():
                print(f"Enter a number 1..{board.cols}.")
                continue
            col = int(raw) - 1
            if col in board.available_columns():
                return col
            if 0 <= col < board.cols:
                print("That column is full. Try another.")
            else:
                print(f"Column must be 1..{board.cols}.")


@dataclass(slots=True, kw_only=True)
class Game:
    board: Board
    players: list[Player]
    ui: ConsoleUI
    referee: Referee | None = None

    def __post_init__(self) -> None:
        if len(self.players) < MIN_PLAYERS:
            raise ValueError(f"Need at least {MIN_PLAYERS} players.")
        symbols = [p.symbol for p in self.players]
        if any(len(s) != 1 for s in symbols):
            raise ValueError("Each player symbol must be a single character.")
        if len(set(symbols)) != len(symbols):
            raise ValueError("Player symbols must be unique.")
        if self.referee is None:
            self.referee = Referee(connect_to_win=CONNECT_TO_WIN)

    def run(self) -> None:
        print("CONNECT 4 — hotseat")
        self.ui.render_board(self.board)
        print(f"{self.players[0].name} starts ({self.players[0].symbol}).")
        turn = 0
        while True:
            current = self.players[turn % len(self.players)]
            col = self.ui.prompt_column(current, self.board)
            last = self.board.place_symbol(col, current.symbol)
            print()
            self.ui.render_board(self.board)
            if self.referee and self.referee.is_winning(self.board, last):
                print(f"\nWinner: {current.name} ({current.symbol})")
                return
            if self.board.is_full:
                print("\nDraw.")
                return
            turn += 1


def setup() -> Game:
    ui = ConsoleUI()
    print("Game setup (press Enter for defaults).")
    rows, cols, connect_to_win = ui.prompt_board_setup()
    players = ui.prompt_players(default_count=DEFAULT_PLAYER_COUNT)
    board = Board(rows=rows, cols=cols)
    referee = Referee(connect_to_win=connect_to_win)
    return Game(board=board, players=players, ui=ui, referee=referee)


def main() -> None:
    game = setup()
    game.run()


if __name__ == "__main__":
    main()
