from .loop import _async_functions_queue

from typing import Callable


def async_function(func) -> Callable:
    '''Schedule async function to run in event loop

    Args:
        func (Awaitable): async function to schedule

    Returns:
        Callable: function that schedules
    '''

    def wrapper(*args, **kwargs) -> None:
        _async_functions_queue.put_nowait(func(*args, **kwargs))

    wrapper.__name__ = func.__name__

    return wrapper