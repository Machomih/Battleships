from abc import ABC, abstractmethod

import pygame

from buttons import Buttons
from table import Table

BACKGROUND = "images/background.jpg"
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
P1 = "Player1"
P2 = "Player2"


class Page(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def update(self, screen):
        pass

    @abstractmethod
    def scale(self, width, height):
        pass


def create_button(screen, start_x, start_y, width, height, text, color):
    my_button = Buttons(screen, color, start_x, start_y, width, height, 0, 10)
    my_button.draw()
    my_button.add_text(text, 40, WHITE)
    return my_button


class StartPage(Page):
    start_buttons = []
    button_pos = None

    def __init__(self):
        super().__init__()
        self.background_img = pygame.image.load(BACKGROUND)

    def update(self, screen):
        screen.blit(self.background_img, (0, 0))
        self.buttons(screen, [(200, 60), (200, 60)], ["Play vs Player", "Play vs PC"], [BLUE, RED])

    def scale(self, width, height):
        self.background_img = pygame.image.load(BACKGROUND)
        self.background_img = pygame.transform.scale(self.background_img, (width, height))

    def buttons(self, screen, buttons_sizes, texts, colors):
        self.start_buttons = []
        button_positions = (
            (screen.get_width() - buttons_sizes[0][0]) / 2, (screen.get_height() + buttons_sizes[0][1]) / 2 + 100)
        start_button = create_button(screen, button_positions[0], button_positions[1], buttons_sizes[0][0],
                                     buttons_sizes[0][1], texts[0], colors[0])
        exit_button = create_button(screen, button_positions[0], button_positions[1] + 100, buttons_sizes[1][0],
                                    buttons_sizes[1][1], texts[1], colors[1])

        self.start_buttons.append(start_button)
        self.start_buttons.append(exit_button)

    def check_event(self, pos):
        if self.start_buttons[0].left() <= pos[0] <= self.start_buttons[0].right():
            if self.start_buttons[0].top() <= pos[1] <= self.start_buttons[0].bottom():
                return "StartPlayer"
        if self.start_buttons[1].left() <= pos[0] <= self.start_buttons[1].right():
            if self.start_buttons[1].top() <= pos[1] <= self.start_buttons[1].bottom():
                return "StartPC"
        return None


def draw_line(screen):
    pygame.draw.line(screen, BLACK, (screen.get_width() / 2, 0 + screen.get_height() / 5),
                     (screen.get_width() / 2, screen.get_height()), 10)


def draw_text(screen, text):
    commentator_btn = Buttons(screen, WHITE, screen.get_width() / 2 - 100, screen.get_height() / 8 - 50, 200, 50, -1, 0)
    commentator_btn.draw()
    commentator_btn.add_text(text, 40, WHITE)


class GamePage(Page):
    def __init__(self):
        super().__init__()
        self.background_img = pygame.image.load("images/water.jpeg")
        self.text = "PREPARE"
        self.start_game = None
        self.current_turn = P2
        self.enemy = None
        self.my_table = Table()
        self.enemy_table = Table()
        self.state = "preparing"

    def update(self, screen):
        screen.blit(self.background_img, (0, 0))
        self.my_table.draw(screen, 100, screen.get_height() / 4)
        draw_line(screen)
        self.enemy_table.draw(screen, 100 + screen.get_width() / 2, screen.get_height() / 4)
        draw_text(screen, self.text)
        if self.state == "preparing":
            self.draw_start_game(screen)
        if self.enemy == "pc" and self.current_turn == P2 and self.state == "started":
            self.bot_moves()

    def scale(self, width, height):
        self.background_img = pygame.image.load("images/water.jpeg")
        self.background_img = pygame.transform.scale(self.background_img, (width, height))

    def draw_start_game(self, screen):
        self.start_game = Buttons(screen, BLUE, screen.get_width() - screen.get_width() / 4,
                                  screen.get_height() / 8 - 50, 150, 50, 0, 10)
        self.start_game.draw()
        self.start_game.add_text("Start Game", 30, WHITE)

    def check_event(self, pos):
        if self.start_game.left() <= pos[0] <= self.start_game.right():
            if self.start_game.top() <= pos[1] <= self.start_game.bottom():
                self.state = "started"
                self.set_text("")
        if self.current_turn == P1:
            current_table = self.enemy_table
        else:
            current_table = self.my_table

        if (self.state == "started"
                and current_table.left() <= pos[0] <= current_table.right()
                and current_table.top() <= pos[1] <= current_table.bottom()):
            state = current_table.shot_fired(pos[0], pos[1], "player")
            return state

        return None

    def bot_moves(self):
        if self.state != "won":
            if self.enemy == "pc" and self.current_turn == P2:
                self.my_table.shot_fired(0, 0, "bot")
                self.set_text("")

    def set_enemy(self, enemy):
        self.enemy = enemy

    def set_text(self, text):
        if self.state == "won":
            return
        if text == "":
            if self.current_turn == P1:
                self.text = "P2 Turn"
                self.current_turn = P2
            elif self.current_turn == P2:
                self.text = "P1 Turn"
                self.current_turn = P1
        else:
            self.text = text

    def finish(self):
        if self.current_turn == P1:
            self.text = "P1 WON"
        elif self.current_turn == P2:
            self.text = "P2 WON"
        self.state = "won"
