from collections.abc import Collection
from dataclasses import dataclass

from assaia_game.domain.symbol import Symbol
from assaia_game.presentation.cli_messages import show_error, show_warning


@dataclass(slots=True, frozen=True, kw_only=True)
class PlayerInput:
    name: str
    symbol: str


class CliInputter:
    __slots__ = ("_prompt_prefix",)

    def __init__(self, prompt_prefix: str) -> None:
        self._prompt_prefix = prompt_prefix

    def ask_int(
        self,
        *,
        label: str | None = None,
        default: int | None = None,
        min_value: int | None = None,
        max_value: int | None = None,
        hint: str | None = None,
        allowed: Collection[int] | None = None,
        allowed_error_msg: str | None = None,
    ) -> int:
        label = f"{self._prompt_prefix}{label or ''}"
        default_hint = f" [{default}]" if default is not None else ""
        bounds_hint = ""
        if min_value is not None and max_value is not None:
            bounds_hint = f" ({min_value}..{max_value})"
        elif min_value is not None:
            bounds_hint = f" (≥{min_value})"
        elif max_value is not None:
            bounds_hint = f" (≤{max_value})"
        hint_part = f" {hint}" if hint else ""

        while True:
            raw = input(f"{label}{bounds_hint}{default_hint}{hint_part}: ").strip()

            if not raw:
                if default is None:
                    show_error("Enter an integer.")
                    continue
                value = default
            else:
                try:
                    value = int(raw)
                except ValueError:
                    show_error("Enter an integer.")
                    continue

            if (min_value is not None and value < min_value) or (
                max_value is not None and value > max_value
            ):
                if min_value is not None and max_value is not None:
                    show_error(
                        f"Value must be between {min_value} and {max_value} inclusive."
                    )
                elif min_value is not None:
                    show_error(f"Value must be ≥ {min_value}.")
                else:
                    show_error(f"Value must be ≤ {max_value}.")
                continue

            if allowed is not None and value not in allowed:
                show_error(
                    allowed_error_msg
                    or "Column is full or not available. Choose another."
                )
                continue

            return value

    def ask_player(
        self,
        *,
        index: int,
        total: int,
        name_default: str,
        symbol_default: str,
        taken_symbols: Collection[str],
        empty_cell_marker: str,
    ) -> PlayerInput:
        i = index + 1
        name = (
            input(
                f"{self._prompt_prefix}Player {i}/{total} name [{name_default}]: "
            ).strip()
            or name_default
        )
        taken_hint = f"; taken: {{{', '.join(taken_symbols)}}}" if taken_symbols else ""
        prompt = (
            f"{self._prompt_prefix}{name} [{i}/{total}] symbol "
            f"(single character{taken_hint}) [{symbol_default}]: "
        )

        while True:
            raw = input(prompt).strip() or symbol_default
            if raw == empty_cell_marker:
                show_error(
                    f"Symbol cannot be the empty-cell marker '{empty_cell_marker}'."
                )
                continue
            if len(raw) != Symbol.EXACT_LENGTH:
                show_error(
                    f"Symbol must be exactly {Symbol.EXACT_LENGTH} character long."
                )
                continue
            if raw in taken_symbols:
                show_warning(f"Symbol already taken: {raw}. Choose another.")
                continue

            return PlayerInput(name=name, symbol=raw)
