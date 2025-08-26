from dataclasses import dataclass

from assaia_game.application.gateways import DraftGateway
from assaia_game.application.types import DraftId
from assaia_game.domain.board import Board
from assaia_game.domain.lobby import Lobby
from assaia_game.domain.referee import Referee


@dataclass(slots=True, frozen=True)
class CreateDraftRequest:
    rows: int
    cols: int
    connect_to_win: int


@dataclass(slots=True, frozen=True)
class CreateDraftResponse:
    draft_id: DraftId
    min_players: int
    max_players: int


class CreateDraftInteractor:
    __slots__ = ("_gateway",)

    def __init__(self, gateway: DraftGateway) -> None:
        self._gateway = gateway

    def execute(self, request: CreateDraftRequest) -> CreateDraftResponse:
        board = Board(rows=request.rows, cols=request.cols)
        referee = Referee(connect_to_win=request.connect_to_win)
        if not referee.is_winnable_on(board):
            raise ValueError(
                "With chosen sizes, nobody can win. "
                "Increase rows/cols or decrease 'connect_to_win'."
            )
        capacity = min(Lobby.N_PLAYERS_MAX, referee.max_players_for_board(board))
        lobby = Lobby(capacity)
        draft_id = self._gateway.create(board, referee, lobby)
        return CreateDraftResponse(
            draft_id=draft_id,
            min_players=Lobby.N_PLAYERS_MIN,
            max_players=capacity,
        )
