from abc import abstractmethod

from typing import Any, Coroutine, List
from types import ModuleType


AsyncTask = Any


class AsyncLibBase:
    """Abstract wrapper class for modules like asyncio, trio

    Class that defines common functions of async libs
    """

    def __init__(self, async_module: ModuleType):
        self._async_module = async_module

    def get_module(self) -> ModuleType:
        """Get underlying async module

        Returns:
            ModuleType: async module
        """

        return self._async_module

    @abstractmethod
    async def sleep(self, duration: float) -> None:
        """Call module's `sleep` method

        Args:
            duration (float): seconds to sleep
        """

    @abstractmethod
    def run(self, coro: Coroutine) -> List[Any]:
        """Wrapper method for running module's event loop

        Examples:
          Calls `asyncio.run(coro)` for asyncio
          Calls `trio.run(coro)` for trio

        Args:
            coro (Coroutine): Coroutine object to run
        """

    @abstractmethod
    def schedule_task(self, coro: Coroutine) -> AsyncTask:
        ...

    @abstractmethod
    async def merge(self, *coros: List[Coroutine]) -> AsyncTask:
        ...