from assaia_game.domain.game_status import GameStatus
from assaia_game.presentation.cli_add_player import CliAddPlayerController
from assaia_game.presentation.cli_create_draft import CliCreateDraftController
from assaia_game.presentation.cli_finalize_draft import CliFinalizeDraftController
from assaia_game.presentation.cli_play_turn import CliPlayTurnController


class CliGameEngine:
    __slots__ = (
        "_add_player_ctl",
        "_create_draft_ctl",
        "_finalize_draft_ctl",
        "_play_turn_ctl",
    )

    def __init__(
        self,
        create_draft_controller: CliCreateDraftController,
        add_player_controller: CliAddPlayerController,
        finalize_draft_controller: CliFinalizeDraftController,
        play_turn_controller: CliPlayTurnController,
    ) -> None:
        self._create_draft_ctl = create_draft_controller
        self._add_player_ctl = add_player_controller
        self._finalize_draft_ctl = finalize_draft_controller
        self._play_turn_ctl = play_turn_controller

    def run(self) -> None:
        draft_ui_result = self._create_draft_ctl.run()
        players_total = draft_ui_result.chosen_players

        taken_symbols: set[str] = set()
        for i in range(draft_ui_result.chosen_players):
            add_player_response = self._add_player_ctl.run(
                draft_id=draft_ui_result.draft_id,
                index=i,
                players_total=players_total,
                taken_symbols=taken_symbols,
            )
            taken_symbols.add(add_player_response.player_symbol)

        start = self._finalize_draft_ctl.run(draft_id=draft_ui_result.draft_id)
        session_id = start.session_id
        board_read_model = start.board_read_model
        current_player_name = start.first_player_name
        current_player_symbol = start.first_player_symbol

        while True:
            turn = self._play_turn_ctl.run(
                session_id=session_id,
                board_read_model=board_read_model,
                current_player_name=current_player_name,
                current_player_symbol=current_player_symbol,
            )
            board_read_model = turn.board_read_model
            if turn.game_status != GameStatus.ONGOING:
                break

            current_player_name = turn.next_player_name or current_player_name
            current_player_symbol = turn.next_player_symbol or current_player_symbol
