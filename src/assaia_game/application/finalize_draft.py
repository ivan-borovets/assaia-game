from dataclasses import dataclass

from assaia_game.application.gateways import DraftGateway, SessionGateway
from assaia_game.application.read_models import BoardReadModel, board_to_read_model
from assaia_game.application.types import DraftId, SessionId
from assaia_game.domain.game_session import GameSession


@dataclass(slots=True, frozen=True)
class FinalizeDraftRequest:
    draft_id: DraftId


@dataclass(slots=True, frozen=True)
class FinalizeDraftResponse:
    session_id: SessionId
    board_read_model: BoardReadModel
    first_player_name: str
    first_player_symbol: str


class FinalizeDraftInteractor:
    __slots__ = ("_draft_gateway", "_session_gateway")

    def __init__(
        self,
        draft_gateway: DraftGateway,
        session_gateway: SessionGateway,
    ) -> None:
        self._draft_gateway = draft_gateway
        self._session_gateway = session_gateway

    def execute(self, request: FinalizeDraftRequest) -> FinalizeDraftResponse:
        board, referee, lobby = self._draft_gateway.read(request.draft_id)
        roster = lobby.to_roster()
        session = GameSession(board=board, roster=roster)
        session_id = self._session_gateway.create(session=session, referee=referee)
        self._draft_gateway.delete(request.draft_id)

        board_read_model = board_to_read_model(session.board)
        first_player = session.current_player
        return FinalizeDraftResponse(
            session_id=session_id,
            board_read_model=board_read_model,
            first_player_name=first_player.name,
            first_player_symbol=first_player.symbol.value,
        )
