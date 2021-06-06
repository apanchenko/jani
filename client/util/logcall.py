from functools import wraps
from typing import TypeVar, Callable, Any, cast
import logging

F = TypeVar("F", bound=Callable[..., Any])

info = logging.getLogger('📜').info


def logcall(f: F) -> F:

    def log(value:Any) -> str:
        return f'{type(value).__name__}'

    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logargs = [f'{log(a)}' for a in args]
        logkwargs = [f'{k}={log(v)}' for k, v in kwargs.items()]

        res = f(*args, **kwargs)

        info(f'{f.__name__}({logargs}, {logkwargs}) -> {log(res)}')

        return res

    return cast(F, wrapper)
