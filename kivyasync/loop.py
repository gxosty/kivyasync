from queue import Queue
from types import ModuleType

from kivy.app import App as KivyApp

from .asynclib import *


_async_functions_queue = Queue()


# static class
class KivyAsync:
    class EventLoop:
        """Main event loop that runs kivy app

        All async events are handled in this class

        Attributes:
            app: The Kivy app
            asynclib: Async module to use
        """

        app: KivyApp
        asynclib: AsyncLibBase | None = None

        def __init__(self, app: KivyApp, module_name: str = "asyncio") -> None:
            """Run `app` and `async_module` in async event loop

            Args:
                app (KivyApp): App to run in event loop
                module_name (str): Async module name to use
            """

            self.app = app

            if module_name == "asyncio":
                from .asynclib.asynciolib import AsyncioLib

                self.asynclib = AsyncioLib()
            else:
                raise NotImplementedError(
                    f"Async module `{module_name}` is not supported yet"
                )

        def run(self) -> None:
            self.asynclib.run(self._main_async_loop())

        async def _queued_functions_loop(self):
            while True:
                while not _async_functions_queue.empty():
                    async_func = _async_functions_queue.get_nowait()
                    self.asynclib.schedule_task(async_func)

                await self.asynclib.sleep(0)

        async def _app_loop(self):
            await self.app.async_run()

        async def _main_async_loop(self):
            self.asynclib.schedule_task(self._queued_functions_loop())
            await self._app_loop()

    _event_loop: EventLoop | None = None

    @staticmethod
    def get_event_loop() -> EventLoop:
        if KivyAsync._event_loop is None:
            raise RuntimeError(
                "kivyasync loop is not running. Are you not running your app through kivyasync.run(...)?"
            )

        return KivyAsync._event_loop


def run(app: KivyApp, module_name: str = "asyncio") -> None:
    """Main entry point for running kivy app

    Args:
        app (KivyApp): The Kivy app to run
        module_name (str): The async module to use (default: `"asyncio"`)
    """
    event_loop = KivyAsync.EventLoop(app, module_name)
    KivyAsync._event_loop = event_loop
    event_loop.run()
    KivyAsync._event_loop = None


async def sleep(duration: float) -> None:
    """Call `sleep` function of async module

    Shortcut function for calling corresponding `sleep` function of
    async module that is being used by kivyasync

    Args:
        duration (float): duration to sleep in seconds
    """
    await KivyAsync.get_event_loop().asynclib.sleep(duration)
