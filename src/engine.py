from collections import deque
from typing import Optional, List, Dict


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

    def __init__(self, dungeon: 'Dungeon', value: str, x: int, y: int):
        self.dungeon = dungeon
        self.value = Room.char_map[value]
        self.x = x
        self.y = y

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

    @property
    def neighbors(self):
        """
        Returns all the active neighbors of the current room
        """
        neighbors = set()
        if self.top:
            top = self.dungeon.rooms.get((self.x, self.y - 1))
            neighbors.add(top) if top is not None and top.bottom else None
        if self.right:
            right = self.dungeon.rooms.get((self.x + 1, self.y))
            neighbors.add(right) if right is not None and right.left else None
        if self.bottom:
            bottom = self.dungeon.rooms.get((self.x, self.y + 1))
            neighbors.add(bottom) if bottom is not None and bottom.top else None
        if self.left:
            left = self.dungeon.rooms.get((self.x - 1, self.y))
            neighbors.add(left) if left is not None and left.right else None
        return neighbors

    def __repr__(self):
        return f'<Room(x={self.x}, y={self.y}, symbol=\'{Room.repr_map[self.value]}\')>'


class Entity:
    char_map = {'A': 0, 'D': 1, 'T': 2}
    repr_map = {0: 'A', 1: 'D', 2: 'T'}

    def __init__(self, dungeon: 'Dungeon', value: str, x: int, y: int, level: int = None):
        self.dungeon = dungeon
        self.value = Entity.char_map[value]
        self.x = x
        self.y = y
        self.level = level or 1

    @property
    def room(self):
        """
        Returns the room, where the Entity is located
        """
        return self.dungeon.rooms.get((self.x, self.y))

    def __repr__(self):
        return f'<Entity(x={self.x}, y={self.y}, symbol=\'{Room.repr_map[self.value]}\')>'


class Dungeon:
    def __init__(self):
        self.rooms: Dict[tuple[int, int]: Room] = {}
        self.entities: List[Entity] = []

    def read_file(self, filename: str):
        # Decode the file
        with open(filename) as f:
            lines = f.readlines()
            for y, line in enumerate(lines):
                if any([line.startswith(symbol) for symbol in Room.char_map.keys()]):
                    for x, value in enumerate(line):
                        self.rooms[(x, y)] = Room(self, value, x, y)
                elif any([line.startswith(symbol) for symbol in Entity.char_map.keys()]):
                    self.entities += [Entity(self, *line.split())]

        self.entities.sort(key=lambda ent: (ent.value, ent.level))

    def bfs(self):
        # Get the shortest path to the most-priority target
        player = self.entities[0]
        targets = self.entities[1:].copy()
        paths = []

        visited = set()
        queue = deque([(player.room, [player.room])])

        while queue:
            room, path = queue.popleft()

            for target in targets:
                if room == target.room:
                    paths += [(target, path)]
                    targets.remove(target)
                    break

            if room not in visited:
                visited.add(room)

                for neighbor in room.neighbors:
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor]))

        paths.sort(key=lambda tup: (tup[0].value, tup[0].level))
        return paths[-1]
