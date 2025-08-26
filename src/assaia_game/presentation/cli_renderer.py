from assaia_game.application.read_models import BoardReadModel
from assaia_game.domain.game_status import GameStatus


class CliRenderer:
    __slots__ = (
        "_cell_empty_symbol",
        "_cell_width",
        "_gutter",
        "_row_label_min_width",
    )

    def __init__(
        self,
        cell_width: int,
        cell_empty_symbol: str,
        row_label_min_width: int,
        gutter: int,
    ) -> None:
        self._cell_width = cell_width
        self._cell_empty_symbol = cell_empty_symbol
        self._row_label_min_width = row_label_min_width
        self._gutter = gutter

    def show_setup_intro(self) -> None:
        print("Game setup (press Enter for defaults).")

    def show_draft_created(self, *, min_players: int, max_players: int) -> None:
        print(f"Draft created. Players allowed: {min_players}..{max_players}.")

    def show_player_added(
        self,
        *,
        lobby_size: int,
        players_total: int,
        player_name: str,
        player_symbol: str,
    ) -> None:
        print(
            f"Added: {player_name} ({player_symbol}). "
            f"Lobby {lobby_size}/{players_total}."
        )

    def show_start(
        self,
        *,
        board_read_model: BoardReadModel,
        first_player_name: str,
        first_player_symbol: str,
    ) -> None:
        self._render_board_frame(board_read_model)
        print(f"{first_player_name} starts ({first_player_symbol}).")

    def show_turn_update(
        self,
        *,
        board_read_model: BoardReadModel,
        game_status: GameStatus,
        mover_name: str,
        mover_symbol: str,
        next_player_name: str | None,
        next_player_symbol: str | None,
    ) -> None:
        self._render_board_frame(board_read_model)
        if game_status == GameStatus.WIN:
            print(f"\nWinner: {mover_name} ({mover_symbol})")
        elif game_status == GameStatus.DRAW:
            print("\nDraw.")
        else:
            print(f"\n{next_player_name} to move ({next_player_symbol}).")

    def _render_board_frame(self, board_read_model: BoardReadModel) -> None:
        rows, cols = board_read_model.rows, board_read_model.cols
        cell_w = self._cell_width
        row_label_w = max(self._row_label_min_width, len(str(rows)))
        indent = " " * (row_label_w + self._gutter)
        header = (
            indent + "│" + "│".join(f"{i:^{cell_w}}" for i in range(1, cols + 1)) + "│"
        )
        top_border = indent + "┌" + "┬".join("─" * cell_w for _ in range(cols)) + "┐"
        bottom_border = indent + "└" + "┴".join("─" * cell_w for _ in range(cols)) + "┘"
        print(header)
        print(top_border)
        for r in range(rows):
            rendered_cells: list[str] = []
            for c in range(cols):
                cell = board_read_model.cells[r][c]
                text = self._cell_empty_symbol if cell is None else cell
                rendered_cells.append(f"{text:^{cell_w}}")
            left_label = f"{rows - r:>{row_label_w}}" + " " * self._gutter
            print(left_label + "│" + "│".join(rendered_cells) + "│")
        print(bottom_border)
