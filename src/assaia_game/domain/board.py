from dataclasses import dataclass
from typing import Final

from assaia_game.domain.symbol import Symbol


@dataclass(slots=True, frozen=True, kw_only=True)
class Cell:
    row_idx: int
    col_idx: int


class Board:
    __slots__ = ("_grid", "cols", "rows")
    DIM_MIN: Final[int] = 3
    DIM_MAX: Final[int] = 20

    def __init__(self, *, rows: int, cols: int) -> None:
        self._validate_dims(rows, cols)
        self.rows, self.cols = rows, cols
        self._grid: list[list[Symbol | None]] = [
            [None] * self.cols for _ in range(self.rows)
        ]

    def _validate_dims(self, rows: int, cols: int) -> None:
        if not (self.DIM_MIN <= rows <= self.DIM_MAX):
            raise ValueError(f"Rows must be between {self.DIM_MIN} and {self.DIM_MAX}.")
        if not self.DIM_MIN <= cols <= self.DIM_MAX:
            raise ValueError(
                f"Columns must be between {self.DIM_MIN} and {self.DIM_MAX}."
            )

    @property
    def _top_row(self) -> list[Symbol | None]:
        return self._grid[0]

    def place_symbol(self, col: int, symbol: Symbol) -> Cell:
        if not 1 <= col <= self.cols:
            raise ValueError(f"Column {col} out of range [1..{self.cols}].")
        col_idx = col - 1
        if self._top_row[col_idx] is not None:
            raise ValueError("Column is full.")
        for row_idx in range(self.rows - 1, -1, -1):
            if self._grid[row_idx][col_idx] is None:
                self._grid[row_idx][col_idx] = symbol
                return Cell(row_idx=row_idx, col_idx=col_idx)
        raise RuntimeError(
            "Invariant violated: column had space but no empty cell found."
        )

    def get_symbol_at(self, *, row_idx: int, col_idx: int) -> Symbol | None:
        return self._grid[row_idx][col_idx]

    @property
    def available_columns(self) -> tuple[int, ...]:
        return tuple(i for i, col in enumerate(self._top_row, 1) if col is None)

    @property
    def is_full(self) -> bool:
        return None not in self._top_row
