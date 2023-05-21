from src.utils import State
from src.libs import fltk as tk
from src.engine import Dungeon


class Game(State):
    def __init__(self):
        with self.proxy as storage:
            name = storage['map']

        self.dungeon = Dungeon.from_file(f'assets/maps/{name}')
        self.dx = 720 / self.dungeon.width
        self.dy = 480 / self.dungeon.height
        self.texture_map = {
            'A': 'Knight_s.png',
            'D': 'Dragon_s.png',
            'T': 'treasure.png'
        }

    def on_enter(self):
        self.draw()

    def draw(self):
        tk.efface_tout()
        for room in self.dungeon.rooms.values():
            x = room.x * self.dx
            y = room.y * self.dy
            tk.rectangle(x, y, x + self.dx, y + self.dy, remplissage='#83769C', epaisseur=0)
            if not room.top:
                tk.rectangle(x, y, x + self.dx, y + self.dy * 0.1, remplissage='#000000', epaisseur=0)
            if not room.right:
                tk.rectangle(x + self.dx * 0.9, y, x + self.dx, y + self.dy, remplissage='#000000', epaisseur=0)
            if not room.bottom:
                tk.rectangle(x, y + self.dy * 0.9, x + self.dx, y + self.dy, remplissage='#000000', epaisseur=0)
            if not room.left:
                tk.rectangle(x, y, x + self.dx * 0.1, y + self.dy, remplissage='#000000', epaisseur=0)

        for entity in self.dungeon.entities:
            if entity.alive:
                tk.image((entity.x + 0.5) * self.dx, (entity.y + 0.5) * self.dy, f'assets/media/{self.texture_map[entity.symbol]}', self.dx * 0.8, self.dy * 0.8)
                tk.texte(entity.x * self.dx, entity.y * self.dy, entity.level)

    def on_event(self, ev: tk.FltkEvent):
        if tk.type_ev(ev) == 'Touche' and tk.touche(ev) == 'space':
            if self.dungeon.update_dungeon():
                self.over()
                return
        elif tk.type_ev(ev) == 'ClicGauche':
            self.dungeon.room(tk.abscisse(ev) // self.dx, tk.ordonnee(ev) // self.dy).rotate_right()
        elif tk.type_ev(ev) == 'ClicDroit':
            self.dungeon.room(tk.abscisse(ev) // self.dx, tk.ordonnee(ev) // self.dy).rotate_left()
        self.draw()

    def on_exit(self):
        tk.efface_tout()

    def over(self):
        with self.proxy as storage:
            storage['result'] = 'U Win' if self.dungeon.player.alive else 'U lost'

        print('here')
        from src.over import Over
        State.change_state(Over())
