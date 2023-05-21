from src.utils import State, TextButton
from src.libs import fltk as tk


class Play(TextButton):
    def on_click(self):
        from src.map import Map
        State.change_state(Map())


class Exit(TextButton):
    def on_click(self):
        State.change_state(None)


class Menu(State):
    def __init__(self):
        self.play = Play(360, 200, 120, 60, 'Play!', '#008751')
        self.exit = Exit(360, 280, 120, 60, 'Exit!', '#FF004D')

    def on_event(self, ev: tk.FltkEvent):
        super().on_event(ev)
        if tk.type_ev(ev) in ('ClicGauche', 'ClicDroit'):
            x, y = tk.abscisse(ev), tk.ordonnee(ev)
            self.play.click(x, y)
            self.exit.click(x, y)

    def on_enter(self):
        self.play.draw()
        self.exit.draw()
