import copy
import uuid

from assaia_game.application.gateways import DraftGateway, SessionGateway
from assaia_game.application.types import DraftId, SessionId
from assaia_game.domain.board import Board
from assaia_game.domain.game_session import GameSession
from assaia_game.domain.lobby import Lobby
from assaia_game.domain.referee import Referee


class InMemoryDraftDAO(DraftGateway):
    def __init__(self) -> None:
        self._store: dict[DraftId, tuple[Board, Referee, Lobby]] = {}

    def create(self, board: Board, referee: Referee, lobby: Lobby) -> DraftId:
        draft_id = DraftId(uuid.uuid4().hex)
        self._store[draft_id] = (
            copy.deepcopy(board),
            copy.deepcopy(referee),
            copy.deepcopy(lobby),
        )
        return draft_id

    def read(self, draft_id: DraftId) -> tuple[Board, Referee, Lobby]:
        board, referee, lobby = self._store[draft_id]
        return copy.deepcopy(board), copy.deepcopy(referee), copy.deepcopy(lobby)

    def read_lobby(self, draft_id: DraftId) -> Lobby:
        lobby = self._store[draft_id][2]
        return copy.deepcopy(lobby)

    def update_lobby(self, draft_id: DraftId, lobby: Lobby) -> None:
        board, referee, _ = self._store[draft_id]
        self._store[draft_id] = (board, referee, copy.deepcopy(lobby))

    def delete(self, draft_id: DraftId) -> None:
        self._store.pop(draft_id, None)


class InMemorySessionDAO(SessionGateway):
    def __init__(self) -> None:
        self._store: dict[SessionId, tuple[GameSession, Referee]] = {}

    def create(self, session: GameSession, referee: Referee) -> SessionId:
        session_id = SessionId(uuid.uuid4().hex)
        self._store[session_id] = (copy.deepcopy(session), copy.deepcopy(referee))
        return session_id

    def read(self, session_id: SessionId) -> tuple[GameSession, Referee]:
        session, referee = self._store[session_id]
        return copy.deepcopy(session), copy.deepcopy(referee)

    def update(self, session_id: SessionId, session: GameSession) -> None:
        _, referee = self._store[session_id]
        self._store[session_id] = (copy.deepcopy(session), referee)
