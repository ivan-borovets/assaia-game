from assaia_game.application.add_player import AddPlayerInteractor
from assaia_game.application.create_draft import CreateDraftInteractor
from assaia_game.application.finalize_draft import FinalizeDraftInteractor
from assaia_game.application.play_turn import PlayTurnInteractor
from assaia_game.infrastructure.in_mem_daos import InMemoryDraftDAO, InMemorySessionDAO
from assaia_game.presentation.cli_add_player import CliAddPlayerController
from assaia_game.presentation.cli_create_draft import CliCreateDraftController
from assaia_game.presentation.cli_engine import CliGameEngine
from assaia_game.presentation.cli_finalize_draft import CliFinalizeDraftController
from assaia_game.presentation.cli_inputter import CliInputter
from assaia_game.presentation.cli_play_turn import CliPlayTurnController
from assaia_game.presentation.cli_renderer import CliRenderer
from assaia_game.setup.config import GameDefaults


def build_cli_game(defaults: GameDefaults | None = None) -> CliGameEngine:
    defaults = defaults or GameDefaults()

    # Gateways / DAO
    draft_g = InMemoryDraftDAO()
    session_g = InMemorySessionDAO()

    # Interactors
    create_draft_i = CreateDraftInteractor(draft_g)
    add_player_i = AddPlayerInteractor(draft_g)
    finalize_draft_i = FinalizeDraftInteractor(draft_g, session_g)
    play_turn_i = PlayTurnInteractor(session_g)

    # IO
    inputter = CliInputter(prompt_prefix=defaults.prompt_prefix)
    renderer = CliRenderer(
        cell_width=defaults.cell_width,
        cell_empty_symbol=defaults.cell_empty_symbol,
        row_label_min_width=defaults.row_label_min_width,
        gutter=defaults.gutter,
    )

    # Controllers
    create_draft_c = CliCreateDraftController(
        inputter=inputter,
        renderer=renderer,
        interactor=create_draft_i,
        defaults=defaults,
    )
    add_player_c = CliAddPlayerController(
        inputter=inputter,
        renderer=renderer,
        interactor=add_player_i,
        defaults=defaults,
    )
    finalize_draft_c = CliFinalizeDraftController(
        interactor=finalize_draft_i, renderer=renderer
    )
    play_turn_c = CliPlayTurnController(
        inputter=inputter, renderer=renderer, interactor=play_turn_i
    )

    # Engine
    return CliGameEngine(
        create_draft_controller=create_draft_c,
        add_player_controller=add_player_c,
        finalize_draft_controller=finalize_draft_c,
        play_turn_controller=play_turn_c,
    )
