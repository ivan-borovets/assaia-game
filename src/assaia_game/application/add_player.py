from dataclasses import dataclass

from assaia_game.application.gateways import DraftGateway
from assaia_game.application.types import DraftId
from assaia_game.domain.player import Player
from assaia_game.domain.symbol import Symbol


@dataclass(slots=True, frozen=True)
class AddPlayerRequest:
    draft_id: DraftId
    name: str
    symbol: str


@dataclass(slots=True, frozen=True)
class AddPlayerResponse:
    lobby_size: int
    player_name: str
    player_symbol: str


class AddPlayerInteractor:
    __slots__ = ("_gateway",)

    def __init__(self, gateway: DraftGateway) -> None:
        self._gateway = gateway

    def execute(self, request: AddPlayerRequest) -> AddPlayerResponse:
        lobby = self._gateway.read_lobby(request.draft_id)
        player = Player(name=request.name, symbol=Symbol(request.symbol))
        lobby.add(player)
        self._gateway.update_lobby(request.draft_id, lobby)
        return AddPlayerResponse(
            lobby_size=lobby.size,
            player_name=player.name,
            player_symbol=player.symbol.value,
        )
