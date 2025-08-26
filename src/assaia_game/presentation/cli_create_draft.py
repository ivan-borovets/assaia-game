from dataclasses import dataclass

from assaia_game.application.create_draft import (
    CreateDraftInteractor,
    CreateDraftRequest,
)
from assaia_game.application.types import DraftId
from assaia_game.domain.board import Board
from assaia_game.domain.referee import Referee
from assaia_game.presentation.cli_inputter import CliInputter
from assaia_game.presentation.cli_renderer import CliRenderer
from assaia_game.setup.config import GameDefaults


@dataclass(slots=True, frozen=True)
class CreateDraftUIResult:
    draft_id: DraftId
    chosen_players: int


class CliCreateDraftController:
    __slots__ = ("_defaults", "_inputter", "_interactor", "_renderer")

    def __init__(
        self,
        inputter: CliInputter,
        renderer: CliRenderer,
        interactor: CreateDraftInteractor,
        defaults: GameDefaults,
    ) -> None:
        self._inputter = inputter
        self._renderer = renderer
        self._interactor = interactor
        self._defaults = defaults

    def run(self) -> CreateDraftUIResult:
        self._renderer.show_setup_intro()
        rows = self._inputter.ask_int(
            label="Rows",
            default=self._defaults.rows,
            min_value=max(Board.DIM_MIN, Referee.CONNECT_TO_WIN_MIN),
            max_value=Board.DIM_MAX,
        )
        cols = self._inputter.ask_int(
            label="Columns",
            default=self._defaults.cols,
            min_value=max(Board.DIM_MIN, Referee.CONNECT_TO_WIN_MIN),
            max_value=Board.DIM_MAX,
        )
        connect_max = max(rows, cols)
        connect = self._inputter.ask_int(
            label="In-a-row to win",
            default=min(self._defaults.connect_to_win, connect_max),
            min_value=Referee.CONNECT_TO_WIN_MIN,
            max_value=connect_max,
        )
        response = self._interactor.execute(
            CreateDraftRequest(rows=rows, cols=cols, connect_to_win=connect)
        )
        self._renderer.show_draft_created(
            min_players=response.min_players, max_players=response.max_players
        )

        players_default = max(self._defaults.players, response.min_players)
        players_default = min(players_default, response.max_players)
        chosen = self._inputter.ask_int(
            label="Players",
            default=players_default,
            min_value=response.min_players,
            max_value=response.max_players,
        )

        return CreateDraftUIResult(draft_id=response.draft_id, chosen_players=chosen)
