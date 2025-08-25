from typing import Any, Final


class Symbol:
    __slots__ = ("value",)
    EXACT_LENGTH: Final[int] = 1

    def __init__(self, value: str) -> None:
        self._validate_value(value)
        self.value: str = value

    def _validate_value(self, value: str) -> None:
        if len(value) != self.EXACT_LENGTH:
            raise ValueError(
                f"Symbol must be exactly {self.EXACT_LENGTH} character long."
            )

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"Symbol({self.value!r})"

    def __hash__(self) -> int:
        return hash(self.value)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Symbol) and self.value == other.value

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "value" and hasattr(self, "value"):
            raise AttributeError("Symbol is immutable")
        object.__setattr__(self, name, value)
