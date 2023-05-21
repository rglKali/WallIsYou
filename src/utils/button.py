from src.libs.fltk import rectangle, texte, taille_texte, image


__all__ = [
    'Button',
    'TextButton',
    'ImageButton'
]


class Button:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x, self.y = x, y
        self.width = width
        self.height = height
        self.ax, self.bx, self.ay, self.by = x - (width // 2), x + (width // 2), y - (height // 2), y + (height // 2)
        self.hitbox = {(w, h) for w in range(self.ax, self.bx + 1) for h in range(self.ay, self.by + 1)}

    def click(self, x: int, y: int):
        if (x, y) in self.hitbox:
            self.on_click()
            return True
        return False

    def draw(self):
        self.on_draw()

    def on_draw(self):
        raise NotImplementedError

    def on_click(self):
        raise NotImplementedError


class TextButton(Button):
    def __init__(self, x: int, y: int, width: int, height: int, text: str = str(),
                 color: str = '#FFFFFF', font_name: str = "monogramextended"):
        super().__init__(x, y, width, height)
        self.text = text
        self.color = color
        self.font_name = font_name
        self.font_size = 0

        lines = text.split('\n')
        while self.font_size < min(width, height):
            w, h = max([taille_texte(line, font_name, self.font_size) for line in lines])
            if w < width and h * len(lines) < height:
                self.font_size += 1
            else:
                self.font_size -= 1
                break

    def draw(self):
        rectangle(self.ax, self.ay, self.bx, self.by, '#000000', self.color, 5)
        texte(self.x, self.y, self.text, '#000000', "center", self.font_name, self.font_size)

    def on_click(self):
        raise NotImplementedError


class ImageButton(Button):
    def __init__(self, x: int, y: int, width: int, height: int, imagepath: str = None):
        super().__init__(x, y, width, height)
        self.image = imagepath

    def on_draw(self):
        image(self.x, self.y, self.image, self.width, self.height)
