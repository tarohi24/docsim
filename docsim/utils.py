import logging
from typing import Callable, Hashable, List, Optional, Tuple, Type, TypeVar


T = TypeVar('T')
logger = logging.getLogger(__file__)
T_has = TypeVar('T_has', bound=Hashable)


def ignore_exception(func: Callable[..., T],
                     exceptions: Tuple[Type[Exception]]) -> Callable[..., Optional[T]]:
    """
    Decorator
    """
    def wrapper(*args, **kwargs) -> Optional[T]:
        try:
            val: T = func(*args, **kwargs)
            return val
        except exceptions as e:
            logger.error(e, exc_info=True)
            return None
    return wrapper


def uniq(orig: List[T_has],
         n_top: int,
         lst: Optional[List[T_has]] = None) -> List[T_has]:
    if lst is None:
        return uniq(orig, n_top, [])
    elif len(lst) == n_top or len(orig) == 0:
        return lst
    else:
        head, *tail = orig
        if head in lst:
            return uniq(orig=tail, n_top=n_top, lst=lst)
        else:
            return uniq(orig=tail, n_top=n_top, lst=[head] + lst)
