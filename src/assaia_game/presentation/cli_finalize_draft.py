from assaia_game.application.finalize_draft import (
    FinalizeDraftInteractor,
    FinalizeDraftRequest,
    FinalizeDraftResponse,
)
from assaia_game.application.types import DraftId
from assaia_game.presentation.cli_renderer import CliRenderer


class CliFinalizeDraftController:
    __slots__ = ("_interactor", "_renderer")

    def __init__(
        self,
        interactor: FinalizeDraftInteractor,
        renderer: CliRenderer,
    ) -> None:
        self._interactor = interactor
        self._renderer = renderer

    def run(self, draft_id: DraftId) -> FinalizeDraftResponse:
        response = self._interactor.execute(FinalizeDraftRequest(draft_id=draft_id))
        self._renderer.show_start(
            board_read_model=response.board_read_model,
            first_player_name=response.first_player_name,
            first_player_symbol=response.first_player_symbol,
        )
        return response
