from abc import abstractmethod

from typing import Any, Coroutine, List
from types import ModuleType

from . import AsyncLibBase

import asyncio


class AsyncioLib(AsyncLibBase):
    def __init__(self):
        AsyncLibBase.__init__(self, asyncio)

    # override
    async def sleep(self, duration: float) -> None:
        return await self.get_module().sleep(duration)

    # override
    def run(self, coro: Coroutine) -> List[Any]:
        return self.get_module().run(coro)

    # override
    def schedule_task(self, coro: Coroutine) -> asyncio.Task:
        return asyncio.create_task(coro)

    # override
    async def merge(self, *coros: List[Coroutine]) -> asyncio.Task:
        return await self.get_module().gather(*coros)