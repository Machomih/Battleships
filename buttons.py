import pygame


class Buttons:
    def __init__(self, screen, color, start_x, start_y, width, height, border, border_radius):
        self.screen = screen
        self.color = color
        self.start_x = start_x
        self.start_y = start_y
        self.width = width
        self.height = height
        self.border = border
        self.border_radius = border_radius
        self.text_object = None

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.start_x, self.start_y, self.width, self.height), self.border,
                         self.border_radius)

    def add_text(self, text, size, color):
        font = pygame.font.Font(None, size)
        text_obj = font.render(text, True, color)
        self.screen.blit(text_obj, (self.start_x + self.width / 2 - text_obj.get_width() / 2,
                                    self.start_y + self.height / 2 - text_obj.get_height() / 2))

    def left(self):
        return self.start_x

    def top(self):
        return self.start_y

    def right(self):
        return self.start_x + self.width

    def bottom(self):
        return self.start_y + self.height

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_text_object(self):
        return self.text_object
