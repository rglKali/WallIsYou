from src.libs.fltk import efface_tout, FltkEvent
from typing import Optional


class Storage(dict):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class State:
    current: Optional['State'] = None
    proxy: Storage = Storage()

    @classmethod
    def change_state(cls, state: Optional['State'] = None):
        if cls.current is not None:
            cls.current.on_exit()
        cls.current = state
        if cls.current is not None:
            cls.current.on_enter()
        return cls.current

    def on_enter(self):
        """
        Code to be executed on state enter
        """

    def on_event(self, ev: FltkEvent):
        """
        Event logic
        """

    def on_exit(self):
        """
        Code to be executed on state exit
        """
        efface_tout()
