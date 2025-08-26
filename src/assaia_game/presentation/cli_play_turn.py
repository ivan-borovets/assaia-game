from assaia_game.application.play_turn import (
    PlayTurnInteractor,
    PlayTurnRequest,
    PlayTurnResponse,
)
from assaia_game.application.read_models import BoardReadModel
from assaia_game.application.types import SessionId
from assaia_game.presentation.cli_inputter import CliInputter
from assaia_game.presentation.cli_renderer import CliRenderer


class CliPlayTurnController:
    __slots__ = ("_inputter", "_interactor", "_renderer")

    def __init__(
        self,
        inputter: CliInputter,
        renderer: CliRenderer,
        interactor: PlayTurnInteractor,
    ) -> None:
        self._inputter = inputter
        self._renderer = renderer
        self._interactor = interactor

    def run(
        self,
        session_id: SessionId,
        board_read_model: BoardReadModel,
        current_player_name: str,
        current_player_symbol: str,
    ) -> PlayTurnResponse:
        available = board_read_model.available_columns
        hint = f"available: {{{', '.join(str(c) for c in available)}}}"
        col = self._inputter.ask_int(
            label=f"{current_player_name} ({current_player_symbol}) column",
            default=(available[0] if available else None),
            min_value=1,
            max_value=board_read_model.cols,
            hint=hint,
            allowed=available,
            allowed_error_msg="Column is full or not available. Choose another.",
        )
        response = self._interactor.execute(
            PlayTurnRequest(session_id=session_id, col=col)
        )
        self._renderer.show_turn_update(
            board_read_model=response.board_read_model,
            game_status=response.game_status,
            mover_name=response.mover_name,
            mover_symbol=response.mover_symbol,
            next_player_name=response.next_player_name,
            next_player_symbol=response.next_player_symbol,
        )
        return response
