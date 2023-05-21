import os
from src.utils import State, TextButton
from src.libs import fltk as tk


class MapHandler(TextButton):
    def on_click(self):
        from src.game import Game
        with State.proxy as storage:
            storage['map'] = self.text
        State.change_state(Game())


class Map(State):
    def __init__(self):
        names = [name.split('.')[0] for name in os.listdir('assets/maps')]
        self.dy = 440 // len(names)
        self.maps = [MapHandler(120, int((index + 0.5) * self.dy), 200, int(self.dy * 0.8), name) for index, name in enumerate(names)]

    def on_enter(self):
        for button in self.maps:
            button.draw()

    def on_event(self, ev: tk.FltkEvent):
        super().on_event(ev)
        if tk.type_ev(ev) in ('ClicGauche', 'ClicDroit'):
            x, y = tk.abscisse(ev), tk.ordonnee(ev)
            for button in self.maps:
                button.click(x, y)
