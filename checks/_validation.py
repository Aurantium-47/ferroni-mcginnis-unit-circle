"""Input validation shared by the two otherwise independent constructions."""

from collections.abc import Iterable
from operator import index


def integer(value: object, name: str) -> int:
    """Accept exact integer objects, but never bool, floats, or numeric strings."""
    if isinstance(value, bool):
        raise TypeError(f"{name} must be an integer, not bool")
    try:
        return index(value)
    except TypeError as exc:
        raise TypeError(f"{name} must be an exact integer") from exc


def capacities(values: Iterable[int]) -> tuple[int, ...]:
    """Return a nonempty tuple of strictly positive integer capacities."""
    if isinstance(values, (str, bytes)):
        raise TypeError("capacities must be an iterable of positive integers")
    try:
        result = tuple(integer(value, "capacity") for value in values)
    except TypeError as exc:
        raise TypeError("capacities must be an iterable of positive integers") from exc
    if not result:
        raise ValueError("at least one capacity is required")
    if any(value <= 0 for value in result):
        raise ValueError("every capacity must be strictly positive")
    return result


def parameters(values: Iterable[int], k: int) -> tuple[tuple[int, ...], int]:
    """Validate the conjecture's domain: n >= 1 and 1 <= k <= n."""
    result = capacities(values)
    count = integer(k, "k")
    if not 1 <= count <= len(result):
        raise ValueError("k must satisfy 1 <= k <= number of capacities")
    return result, count


def require(condition: bool, message: str) -> None:
    """A check that remains active under python -O."""
    if not condition:
        raise AssertionError(message)
