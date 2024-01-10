import pygame


class Cursor:
    cursor_rect = None
    cursor_img = None

    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        cursor_img = pygame.image.load("images/cursor.png")
        cursor_img = pygame.transform.scale(cursor_img, (50, 50))
        self.cursor_rect = cursor_img.get_rect()
        self.cursor_img = cursor_img

    def update_cursor(self, screen):
        self.cursor_rect.center = pygame.mouse.get_pos()
        screen.blit(self.cursor_img, self.cursor_rect)
        screen.blit(self.cursor_img, self.cursor_rect)
