from src.engine import Dungeon
from src.fsm import State
from src.fltk import cree_fenetre, ferme_fenetre, attend_ev


def main():
    cree_fenetre(640, 640)

    attend_ev()

    ferme_fenetre()
