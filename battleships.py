import pygame

from cursor import Cursor
from start_page import StartPage, GamePage


def main():
    pygame.init()
    pygame.display.set_caption("Battleships")
    default_size = 1280, 720
    fullscreen_size = pygame.display.list_modes(0, 0, 0)[0]
    if pygame.display.mode_ok(default_size):
        screen = pygame.display.set_mode(default_size, pygame.RESIZABLE)
    else:
        screen = pygame.display.set_mode(fullscreen_size, pygame.RESIZABLE)

    cursor_instance = Cursor()
    start_page = StartPage()
    game_page = GamePage()

    current_page = start_page

    running = True

    while running:
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.WINDOWRESIZED:
                current_page.scale(screen.get_width(), screen.get_height())
            elif event.type == pygame.VIDEOEXPOSE:
                screen.fill((0, 0, 0))
                current_page.scale(screen.get_width(), screen.get_height())
                pygame.display.flip()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                match current_page.check_event(pygame.mouse.get_pos()):
                    case "StartPlayer":
                        current_page = game_page
                        current_page.set_enemy("P2")
                        current_page.scale(screen.get_width(), screen.get_height())
                    case "StartPC":
                        current_page = game_page
                        current_page.set_enemy("pc")
                        current_page.scale(screen.get_width(), screen.get_height())
                    case "Continue":
                        current_page.set_text("")
                    case "Finish":
                        current_page.finish()
        current_page.update(screen)
        cursor_instance.update_cursor(screen)
        pygame.display.flip()
        pygame.time.delay(20)

    pygame.quit()


if __name__ == "__main__":
    main()
