from typing import Final

from assaia_game.domain.player import Player
from assaia_game.domain.symbol import Symbol


class Lobby:
    __slots__ = (
        "_capacity",
        "_players",
        "_used_symbols",
    )

    N_PLAYERS_MIN: Final[int] = 2
    N_PLAYERS_MAX: Final[int] = 26

    def __init__(self, capacity: int) -> None:
        self._validate_capacity(capacity)
        self._capacity = capacity
        self._players: list[Player] = []
        self._used_symbols: set[Symbol] = set()

    def _validate_capacity(self, capacity: int) -> None:
        if capacity < self.N_PLAYERS_MIN or capacity > self.N_PLAYERS_MAX:
            raise ValueError(
                f"Lobby capacity out of range "
                f"[{self.N_PLAYERS_MIN}..{self.N_PLAYERS_MAX}] (got {capacity})."
            )

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def size(self) -> int:
        return len(self._players)

    def add(self, player: Player) -> None:
        if len(self._players) >= self._capacity:
            raise ValueError(f"Lobby is full (capacity {self._capacity}).")
        if player.symbol in self._used_symbols:
            taken = (
                ", ".join(str(s) for s in sorted(self._used_symbols, key=str)) or "—"
            )
            raise ValueError(
                f"Symbol already taken: {player.symbol}. Choose one not in {{{taken}}}."
            )
        self._players.append(player)
        self._used_symbols.add(player.symbol)

    def to_roster(self) -> tuple[Player, ...]:
        if len(self._players) < self.N_PLAYERS_MIN:
            raise ValueError(
                f"Need at least {self.N_PLAYERS_MIN} players "
                f"(got {len(self._players)})."
            )
        return tuple(self._players)
