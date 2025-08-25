from assaia_game.domain.board import Board, Cell
from assaia_game.domain.game_status import GameStatus
from assaia_game.domain.player import Player


class GameSession:
    __slots__ = ("_board", "_roster", "_status", "_turn_idx")

    def __init__(self, board: Board, roster: tuple[Player, ...]) -> None:
        self._board = board
        self._roster = roster
        self._turn_idx: int = 0
        self._status: GameStatus = GameStatus.ONGOING

    @property
    def board(self) -> Board:
        return self._board

    @property
    def n_players(self) -> int:
        return len(self._roster)

    @property
    def current_player(self) -> Player:
        return self._roster[self._turn_idx % len(self._roster)]

    def apply_move(self, col: int) -> tuple[Player, Cell]:
        if self._status != GameStatus.ONGOING:
            raise RuntimeError("Game is not ongoing.")
        mover = self.current_player
        cell = self._board.place_symbol(col=col, symbol=mover.symbol)
        self._turn_idx += 1
        return mover, cell

    def end_with(self, status: GameStatus) -> None:
        if status == GameStatus.ONGOING:
            return
        self._status = status
