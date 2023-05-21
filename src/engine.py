from collections import deque
from typing import Optional, List, Dict


__all__ = [
    'Dungeon',
    'Room',
    'Entity'
]


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
            top = self.dungeon.room(self.x, self.y - 1)
            neighbors.add(top) if top is not None and top.bottom else None
        if self.right:
            right = self.dungeon.room(self.x + 1, self.y)
            neighbors.add(right) if right is not None and right.left else None
        if self.bottom:
            bottom = self.dungeon.room(self.x, self.y + 1)
            neighbors.add(bottom) if bottom is not None and bottom.top else None
        if self.left:
            left = self.dungeon.room(self.x - 1, self.y)
            neighbors.add(left) if left is not None and left.right else None
        return neighbors

    @property
    def symbol(self):
        return Room.repr_map[self.value]

    def __repr__(self):
        return f'<Room(x={self.x}, y={self.y}, symbol=\'{self.symbol}\')>'


class Entity:
    def __init__(self, dungeon: 'Dungeon', value: str, x: str, y: str, level: str = None):
        self.dungeon = dungeon
        self.symbol = value
        self.x = int(x)
        self.y = int(y)
        self.level = int(level) if level is not None else 1
        self.alive = True

    def move(self, room: Room):
        """
        Moves the entity to the given room
        """
        self.x, self.y = room.x, room.y

    @property
    def room(self):
        """
        Returns the room, where the Entity is located
        """
        return self.dungeon.room(self.x, self.y)

    def __repr__(self):
        return f'<Entity(x={self.x}, y={self.y}, symbol=\'{self.symbol}\', level={self.level}, alive={self.alive})>'


class Dungeon:
    def __init__(self):
        self.rooms: Dict[tuple[int, int]: Room] = {}
        self.entities: List[Entity] = []
        self.width = 0
        self.height = 0

    @classmethod
    def from_file(cls, filename: str):
        self = cls()

        # Decode the file
        with open(filename) as f:
            lines = f.read().split('\n')
            for y, line in enumerate(lines):
                if any([line.startswith(symbol) for symbol in Room.char_map.keys()]):
                    for x, value in enumerate(line):
                        self.rooms[(x, y)] = Room(self, value, x, y)
                        self.width, self.height = x + 1, y + 1
                else:
                    self.entities += [Entity(self, *line.split())]

        self.entities.sort(key=lambda ent: (ent.symbol, ent.level))

        return self

    def room(self, x: int, y: int) -> Room:
        """
        Returns the room in the x, y coords, if exists
        """
        return self.rooms.get((x, y))

    def bfs(self) -> Optional[List[Room]]:
        """
        Returns the sortest path to the highest priority target from the available, if any
        """
        player = self.entities[0]
        targets = [e for e in self.entities if e.symbol != 'A' and e.alive]
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

        if len(paths):
            paths.sort(key=lambda tup: (tup[0].symbol, tup[0].level))
            return paths[-1][1]
        return

    def update_dungeon(self) -> bool:
        """
        Updates the dungeon. Returns False, if the game is over, otherwise True
        """
        path = self.bfs()
        player = self.entities[0]

        if path is not None:
            player.move(path[1])

            for entity in [e for e in self.entities if e.symbol != 'A' and e.alive]:
                if entity.room == player.room:
                    if entity.level > player.level:
                        player.alive = False
                    else:
                        entity.alive = False
                        player.level += 1

        return not player.alive or not len([d for d in self.dragons if d.alive])

    @property
    def player(self):
        return self.entities[0]

    @property
    def dragons(self):
        return [ent for ent in self.entities if ent.symbol == 'D']

    @property
    def treasure(self):
        return self.entities[-1]


if __name__ == '__main__':
    print(Dungeon.from_file('../assets/maps/map_test.txt'))
