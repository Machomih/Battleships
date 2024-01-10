import random
import string

import numpy as np
import pygame

HORIZONTAL = "horizontal"
VERTICAL = "vertical"


def get_random():
    return random.randint(0, 10)


def get_random_orientation():
    i = random.randint(0, 1)
    if i == 0:
        return HORIZONTAL
    if i == 1:
        return VERTICAL


class Table:
    def __init__(self, ):
        self.screen = None
        self.start_x = None
        self.start_y = None
        self.cell_size = None

        self.matrix = np.zeros((11, 11), int)
        self.battleship = []
        self.battleship_length = 4

        self.place_random()
        self.clicked_cells = set()

    def draw(self, screen, start_x, start_y):
        font = pygame.font.Font(None, 36)
        col_labels = [str(i) for i in range(1, 11)]
        row_labels = list(string.ascii_uppercase[:10])
        cell_size = screen.get_height() // 20

        for i, label in enumerate(row_labels):
            text_surface = font.render(label, True, (255, 255, 255))
            screen.blit(text_surface, (start_x, start_y + (i + 1) * cell_size))

        for i, label in enumerate(col_labels):
            text_surface = font.render(label, True, (255, 255, 255))
            screen.blit(text_surface, (start_x + (i + 1) * cell_size, start_y))

        for i, row_label in enumerate(row_labels):
            for j, col_label in enumerate(col_labels):
                pygame.draw.rect(screen, (0, 0, 0),
                                 (start_x + (j + 1) * cell_size, start_y + (i + 1) * cell_size, cell_size, cell_size),
                                 2)
        self.cell_size = cell_size
        self.screen = screen
        self.start_x = start_x
        self.start_y = start_y

        for grid_x, grid_y, cell_value in self.clicked_cells:
            # calculate the pixel center of the cell
            center_x = self.start_x + (grid_y * self.cell_size + self.cell_size / 2)
            center_y = self.start_y + (grid_x * self.cell_size + self.cell_size / 2)
            # radius for the circle
            radius = self.cell_size // 3

            # draw the circle for 0
            if cell_value == 0:
                pygame.draw.circle(self.screen, (255, 0, 0), (int(center_x), int(center_y)), radius)
            # draw the 'X' for 1
            elif cell_value == 1:
                pygame.draw.line(self.screen, (255, 0, 0), (center_x - radius, center_y - radius),
                                 (center_x + radius, center_y + radius), 5)
                pygame.draw.line(self.screen, (255, 0, 0), (center_x - radius, center_y + radius),
                                 (center_x + radius, center_y - radius), 5)

    def place_random(self):
        x = get_random() + 1
        while x + self.battleship_length > 10:
            x = get_random() + 1
        y = get_random() + 1
        while y + self.battleship_length > 10:
            y = get_random() + 1
        orientation = get_random_orientation()

        if orientation == HORIZONTAL:
            for i in range(self.battleship_length):
                self.matrix[y][x + i] = 1

        if orientation == VERTICAL:
            for i in range(self.battleship_length):
                self.matrix[y + i][x] = 1

        print("Battleship at:", x, y)

    def get_cell_size(self):
        return self.cell_size

    def shot_fired(self, mouse_x, mouse_y, player_or_bot):
        if player_or_bot == "player":
            if (self.start_x + self.cell_size <= mouse_x <= self.right()) and (
                    self.start_y / 4 + self.cell_size <= mouse_y <= self.bottom()):
                grid_y = int((mouse_x - self.start_x) // self.cell_size)
                grid_x = int((mouse_y - self.start_y) // self.cell_size)
                print((grid_x, grid_y) in self.clicked_cells)
                if any((grid_x, grid_y) == (x, y) for x, y, v in self.clicked_cells):
                    return "Already clicked"

                cell_value = self.matrix[grid_x][grid_y]
                self.clicked_cells.add((grid_x, grid_y, cell_value))

                if cell_value == 1:
                    self.matrix[grid_x][grid_y] = 0

                if all(cell == 0 for row in self.matrix for cell in row):
                    return "Finish"
                else:
                    return "Continue"

        if player_or_bot == "bot":
            grid_x = random.randint(1, 10)
            grid_y = random.randint(1, 10)
            if any((grid_x, grid_y) == (x, y) for x, y, v in self.clicked_cells):
                grid_x = random.randint(1, 10)
                grid_y = random.randint(1, 10)
            cell_value = self.matrix[grid_x][grid_y]
            self.clicked_cells.add((grid_x, grid_y, cell_value))

            if cell_value == 1:
                self.matrix[grid_x][grid_y] = 0

            if all(cell == 0 for row in self.matrix for cell in row):
                return "Finish"
            else:
                return "Continue"

    def left(self):
        return self.start_x

    def right(self):
        return self.start_x + 11 * self.cell_size

    def top(self):
        return self.start_y

    def bottom(self):
        return self.start_y + 11 * self.cell_size
