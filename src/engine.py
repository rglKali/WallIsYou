from typing import Optional, List


class Room:
    char_map = {
        '╨': 1, '╞': 2, '╥': 4, '╡': 8,
        '╚': 3, '╔': 6, '╗': 12, '╝': 9,
        '║': 5, '═': 10,
        '╠': 7, '╦': 14, '╣': 13, '╩': 11,
        '╬': 15,
    }
    repr_map = {
        1: '╨', 2: '╞', 4: '╥', 8: '╡',
        3: '╚', 6: '╔', 12: '╗', 9: '╝',
        5: '║', 10: '═',
        7: '╠', 14: '╦', 13: '╣', 11: '╩',
        15: '╬',
    }

    def __init__(self, value: str, x: int, y: int):
        self.value = Room.char_map[value]
        self.x = x
        self.y = y
        self.neighbors = {side: None for side in ('left', 'right', 'top', 'bottom')}

    def rotate_right(self) -> None:
        """
        Rotates the room right
        """
        self.value = (self.value << 1) & 0xF | (self.value >> 3)

    def rotate_left(self) -> None:
        """
        Rotates the room left
        """
        self.value = (self.value >> 1) | (self.value << 3) & 0xF

    @property
    def top(self):
        """
        Returns True, if the door to the top room is opened, else False
        """
        return bool(self.value & 1)

    @property
    def right(self):
        """
        Returns True, if the door to the right room is opened, else False
        """
        return bool(self.value & 2)

    @property
    def bottom(self):
        """
        Returns True, if the door to the bottom room is opened, else False
        """
        return bool(self.value & 4)

    @property
    def left(self):
        """
        Returns True, if the door to the left room is opened, else False
        """
        return bool(self.value & 8)

    def __repr__(self):
        return f'<Room(x={self.x}, y={self.y}, symbol=\'{Room.repr_map[self.value]}\')>'


class Entity:
    char_map = {'A': 0, 'D': 1, 'T': 2}
    repr_map = {0: 'A', 1: 'D', 2: 'T'}

    def __init__(self, value: str, x: int, y: int, level: int = None):
        self.value = Entity.char_map[value]
        self.x = x
        self.y = y
        self.level = level or 1

    def __repr__(self):
        return f'<Room(x={self.x}, y={self.y}, symbol=\'{Room.repr_map[self.value]}\')>'


class Dungeon:
    def __init__(self):
        self.rooms: List[Room] = []
        self.entities: List[Entity] = []

    def read_file(self, filename: str):
        # Decode the file
        with open(filename) as f:
            lines = f.readlines()
            for y, line in enumerate(lines):
                if any([line.startswith(symbol) for symbol in Room.char_map.keys()]):
                    for x, value in enumerate(line):
                        self.rooms += [Room(value, x, y)]
                elif any([line.startswith(symbol) for symbol in Entity.char_map.keys()]):
                    self.entities += [Entity(*line.split())]

        # Set up relations between rooms
        """
        todo
        """
