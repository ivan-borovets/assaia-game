from dataclasses import dataclass

from assaia_game.domain.board import Board


@dataclass(slots=True, frozen=True)
class BoardReadModel:
    rows: int
    cols: int
    cells: tuple[tuple[str | None, ...], ...]
    available_columns: tuple[int, ...]


def board_to_read_model(board: Board) -> BoardReadModel:
    rows, cols = board.rows, board.cols
    cells = tuple(
        tuple(
            (sym.value if sym is not None else None)
            for sym in (board.get_symbol_at(row_idx=r, col_idx=c) for c in range(cols))
        )
        for r in range(rows)
    )
    return BoardReadModel(
        rows=rows,
        cols=cols,
        cells=cells,
        available_columns=board.available_columns,
    )
