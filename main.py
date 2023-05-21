from src.libs.fltk import cree_fenetre, attend_ev, ferme_fenetre
from src.utils import State
from src.menu import Menu


def main():
    cree_fenetre(720, 480)

    State.change_state(Menu())

    while State.current is not None:
        State.current.on_event(attend_ev())

    ferme_fenetre()


if __name__ == '__main__':
    main()
