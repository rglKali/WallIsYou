from typing import Optional


class State:
    current: Optional['State'] = None

    @classmethod
    def change_state(cls, state: 'State'):
        cls.current.on_exit()
        cls.current = state
        cls.current.on_enter()

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def on_update(self):
        pass

    def on_draw(self):
        pass
