# kivyasync
Run kivy apps asynchronously

<hr>

# Installation
not yet documented

# Example usage

By default, `kivyasync` uses `asyncio` module

```py
import random

from kivy.app import App
from kivy.uix.button import Button

import kivyasync


class AsyncApp(App):
    def build(self):
        self.button = Button(text="Random number", on_release=self.get_random_number)
        return self.button

    @kivyasync.async_function
    async def get_random_number(self, button):
        # some operation
        kivyasync.sleep(1)
        self.button.text = str(random.randint(1, 10))

if __name__ == '__main__':
    app = AsyncApp()
    kivyasync.run(app)
```