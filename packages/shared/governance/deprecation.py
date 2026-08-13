import warnings
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

"""Deprecation & Sunset Policy Engine for EAOS Governance."""


F = TypeVar("F", bound=Callable[..., Any])


def deprecated_api(
    since: str = "3.0.0",
    remove_in: str = "4.0.0",
    replacement: str = "",
) -> Callable[[F], F]:
    """Decorator issuing structured deprecation warning for legacy APIs."""

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            msg = f"API '{func.__name__}' is deprecated since v{since} and will be removed in v{remove_in}."
            if replacement:
                msg += f" Use '{replacement}' instead."
            warnings.warn(msg, DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator
