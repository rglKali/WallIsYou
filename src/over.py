from src.utils import State, TextButton
from src.libs import fltk as tk


class Handler(TextButton):
    def on_click(self):
        from src.menu import Menu
        State.change_state(Menu())


class Over(State):
    def __init__(self):
        with self.proxy as storage:
            result = storage['result']

        self.handler = Handler(360, 240, 180, 120, result)

    def on_enter(self):
        self.handler.draw()

    def on_event(self, ev: tk.FltkEvent):
        self.handler.click(self.handler.x, self.handler.y)
