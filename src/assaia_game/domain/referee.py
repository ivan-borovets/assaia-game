from typing import Final

from assaia_game.domain.board import Board, Cell
from assaia_game.domain.game_status import GameStatus


class Referee:
    __slots__ = ("connect_to_win",)
    CONNECT_TO_WIN_MIN: Final[int] = 3

    def __init__(self, *, connect_to_win: int) -> None:
        self._validate_connect_to_win(connect_to_win)
        self.connect_to_win = connect_to_win

    def _validate_connect_to_win(self, connect_to_win: int) -> None:
        if connect_to_win < self.CONNECT_TO_WIN_MIN:
            raise ValueError(f"Connect to win must be >= {self.CONNECT_TO_WIN_MIN}.")

    def max_players_for_board(self, board: Board) -> int:
        cells = board.rows * board.cols
        return (cells - 1) // (self.connect_to_win - 1)

    def is_winnable_on(self, board: Board) -> bool:
        return self.connect_to_win <= max(board.rows, board.cols)

    def judge_after_move(
        self,
        board: Board,
        last_move_cell: Cell,
        n_players: int,
    ) -> GameStatus:
        if self._is_move_winning(board, last_move_cell):
            return GameStatus.WIN
        if board.is_full:
            return GameStatus.DRAW
        if not self._is_win_still_possible(board, n_players):
            return GameStatus.DRAW
        return GameStatus.ONGOING

    def _is_move_winning(self, board: Board, last: Cell) -> bool:
        get_symbol_at = board.get_symbol_at
        symbol = get_symbol_at(row_idx=last.row_idx, col_idx=last.col_idx)
        if symbol is None:
            return False

        rows, cols = board.rows, board.cols
        directions = ((0, 1), (1, 0), (1, 1), (1, -1))

        for dr, dc in directions:
            total = 1

            r, c = last.row_idx + dr, last.col_idx + dc
            while (
                0 <= r < rows
                and 0 <= c < cols
                and get_symbol_at(row_idx=r, col_idx=c) == symbol
            ):
                total += 1
                r += dr
                c += dc

            r, c = last.row_idx - dr, last.col_idx - dc
            while (
                0 <= r < rows
                and 0 <= c < cols
                and get_symbol_at(row_idx=r, col_idx=c) == symbol
            ):
                total += 1
                r -= dr
                c -= dc

            if total >= self.connect_to_win:
                return True
        return False

    def _is_win_still_possible(self, board: Board, players_count: int) -> bool:
        """heuristic"""
        rows, cols = board.rows, board.cols
        get_symbol_at = board.get_symbol_at

        empties_total = sum(
            sum(get_symbol_at(row_idx=row, col_idx=col) is None for col in range(cols))
            for row in range(rows)
        )
        if empties_total == 0:
            return False

        k = self.connect_to_win
        limit = (empties_total + players_count - 1) // players_count
        directions = ((0, 1), (1, 0), (1, 1), (1, -1))

        for d_row, d_col in directions:
            r_stop = rows if d_row == 0 else rows - k + 1
            c_start = 0 if d_col >= 0 else k - 1
            c_stop = cols if d_col == 0 else (cols - k + 1 if d_col > 0 else cols)

            for row0 in range(0, r_stop):
                for col0 in range(c_start, c_stop):
                    first = None
                    empties = 0
                    row, col = row0, col0

                    for _ in range(k):
                        s = get_symbol_at(row_idx=row, col_idx=col)
                        if s is None:
                            empties += 1
                            if empties > limit:
                                break
                        elif first is None:
                            first = s
                        elif s != first:
                            break
                        row += d_row
                        col += d_col
                    else:
                        return True
        return False
