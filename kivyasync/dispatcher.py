import inspect

from typing import Type, Awaitable

import kivy_asyncstate


class Dispatcher:
    def __init__(self, event_base_class: Type, state_base_class: Type):
        self._event_base_class = event_base_class
        self._state_base_class = state_base_class
        self._event_functions = {}

        kivy_asyncstate.register_dispatcher(self)

    def __delete__(self):
        kivy_asyncstate.unregister_dispatcher(self)

    def on(self, event_class: Type, async_function: Awaitable):
        if not issubclass(event_class, self._event_base_class):
            raise TypeError(
                f"{event_class.__name__} is not subclass of {self._event_base_class.__name__}"
            )

        if not inspect.iscoroutinefunction(async_function):
            raise TypeError(
                f"Function mapped to `{event_class.__name__}` event is not async function"
            )

        if event_class in self._event_functions:
            raise RuntimeError(
                f"`{event_class.__name__}` was already added to the dispatcher"
            )

    async def _step(self):
        pass
