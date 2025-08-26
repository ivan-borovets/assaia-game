from dataclasses import dataclass

from assaia_game.application.gateways import SessionGateway
from assaia_game.application.read_models import BoardReadModel, board_to_read_model
from assaia_game.application.types import SessionId
from assaia_game.domain.game_status import GameStatus


@dataclass(slots=True, frozen=True)
class PlayTurnRequest:
    session_id: SessionId
    col: int


@dataclass(slots=True, frozen=True)
class PlayTurnResponse:
    board_read_model: BoardReadModel
    game_status: GameStatus
    mover_name: str
    mover_symbol: str
    next_player_name: str | None
    next_player_symbol: str | None


class PlayTurnInteractor:
    __slots__ = ("_gateway",)

    def __init__(self, gateway: SessionGateway) -> None:
        self._gateway = gateway

    def execute(self, request: PlayTurnRequest) -> PlayTurnResponse:
        session, referee = self._gateway.read(request.session_id)
        mover, last_cell = session.apply_move(request.col)
        status = referee.judge_after_move(session.board, last_cell, session.n_players)
        if status != GameStatus.ONGOING:
            session.end_with(status)

        board_read_model = board_to_read_model(session.board)
        next_player = session.current_player if status == GameStatus.ONGOING else None
        self._gateway.update(request.session_id, session)

        return PlayTurnResponse(
            board_read_model=board_read_model,
            game_status=status,
            mover_name=mover.name,
            mover_symbol=mover.symbol.value,
            next_player_name=(next_player.name if next_player else None),
            next_player_symbol=(next_player.symbol.value if next_player else None),
        )
