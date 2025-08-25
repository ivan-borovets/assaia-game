import string
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class GameDefaults:
    # Gameplay
    rows: int = 6
    cols: int = 7
    connect_to_win: int = 4
    players: int = 2
    # CLI
    prompt_prefix: str = "> "
    symbol_pool: tuple[str, ...] = ("X", "O", *string.ascii_uppercase)
    cell_empty_symbol: str = "·"
    cell_width: int = 3
    row_label_min_width: int = 2
    gutter: int = 1

    def __post_init__(self) -> None:
        pool_unique = tuple(dict.fromkeys(self.symbol_pool))
        pool_clean = tuple(ch for ch in pool_unique if ch != self.cell_empty_symbol)
        object.__setattr__(self, "symbol_pool", pool_clean)
