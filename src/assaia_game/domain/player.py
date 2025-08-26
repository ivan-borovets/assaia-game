from dataclasses import dataclass

from assaia_game.domain.symbol import Symbol


@dataclass(slots=True, frozen=True, kw_only=True)
class Player:
    name: str
    symbol: Symbol
