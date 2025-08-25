from abc import abstractmethod
from typing import Protocol

from assaia_game.application.types import DraftId, SessionId
from assaia_game.domain.board import Board
from assaia_game.domain.game_session import GameSession
from assaia_game.domain.lobby import Lobby
from assaia_game.domain.referee import Referee


class DraftGateway(Protocol):
    @abstractmethod
    def create(self, board: Board, referee: Referee, lobby: Lobby) -> DraftId: ...
    @abstractmethod
    def read(self, draft_id: DraftId) -> tuple[Board, Referee, Lobby]: ...
    @abstractmethod
    def read_lobby(self, draft_id: DraftId) -> Lobby: ...
    @abstractmethod
    def update_lobby(self, draft_id: DraftId, lobby: Lobby) -> None: ...
    @abstractmethod
    def delete(self, draft_id: DraftId) -> None: ...


class SessionGateway(Protocol):
    @abstractmethod
    def create(self, session: GameSession, referee: Referee) -> SessionId: ...
    @abstractmethod
    def read(self, session_id: SessionId) -> tuple[GameSession, Referee]: ...
    @abstractmethod
    def update(self, session_id: SessionId, session: GameSession) -> None: ...
