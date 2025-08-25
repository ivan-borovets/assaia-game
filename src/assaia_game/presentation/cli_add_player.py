from collections.abc import Collection

from assaia_game.application.add_player import (
    AddPlayerInteractor,
    AddPlayerRequest,
    AddPlayerResponse,
)
from assaia_game.application.types import DraftId
from assaia_game.presentation.cli_inputter import CliInputter
from assaia_game.presentation.cli_presenter import CliPresenter
from assaia_game.setup.config import GameDefaults


class CliAddPlayerController:
    __slots__ = ("_defaults", "_inputter", "_interactor", "_presenter")

    def __init__(
        self,
        inputter: CliInputter,
        presenter: CliPresenter,
        interactor: AddPlayerInteractor,
        defaults: GameDefaults,
    ) -> None:
        self._inputter = inputter
        self._presenter = presenter
        self._interactor = interactor
        self._defaults = defaults

    def run(
        self,
        draft_id: DraftId,
        index: int,
        players_total: int,
        taken_symbols: Collection[str],
    ) -> AddPlayerResponse:
        pool = self._defaults.symbol_pool
        if not pool:
            raise ValueError("symbol_pool is empty. Provide at least one symbol.")
        sym_default = next(
            (ch for ch in pool if ch not in taken_symbols),
            pool[0],
        )
        player_input = self._inputter.ask_player(
            index=index,
            total=players_total,
            name_default=f"Player {index + 1}",
            symbol_default=sym_default,
            taken_symbols=taken_symbols,
            empty_cell_marker=self._defaults.cell_empty_symbol,
        )

        response = self._interactor.execute(
            AddPlayerRequest(
                draft_id=draft_id,
                name=player_input.name,
                symbol=player_input.symbol,
            )
        )
        self._presenter.show_player_added(
            lobby_size=response.lobby_size,
            players_total=players_total,
            player_name=response.player_name,
            player_symbol=response.player_symbol,
        )
        return response
