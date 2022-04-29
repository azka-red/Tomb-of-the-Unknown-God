import pygame
import sys
from settings import SETTINGS, COLOR


def main():
    pygame.init()
    surface = pygame.display.set_mode(SETTINGS["WINDOW_SIZE"])
    pygame.display.set_caption(SETTINGS["TITLE"])
    surface.fill(COLOR["DARK_GRAY"])
    pygame.display.set_icon(pygame.image.load(SETTINGS["ICON_URL"]))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


if __name__ == "__main__":
    main()
