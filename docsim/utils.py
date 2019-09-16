import logging
from typing import Callable, Optional, Tuple, Type, TypeVar


T = TypeVar('T')
logger = logging.getLogger(__file__)


def ignore_exception(func: Callable[..., T],
                     exceptions: Tuple[Type[Exception]]) -> Optional[T]:
    """
    Decorator
    """
    def wrapper(*args, **kwargs):
        try:
            val: T = func(*args, **kwargs)
            return val
        except exceptions as e:
            logger.error(e, exc_info=True)
            return
    return wrapper
