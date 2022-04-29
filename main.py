from pydoc import plain
import pygame
import sys
from settings import SETTINGS, COLOR

class Player:
    def __init__(self, px: float, py: float, size, speed: float) -> None:
        # player coordinates
        self.px = px
        self.py = py
        self.size = size
        self.speed = speed
        self.velocity = [0, 0]


    def update(self,dt):
        self.px += self.velocity[0]*(self.speed*dt)
        self.py += self.velocity[1]*(self.speed*dt)

# update stuff according to delta time value
def update(dt):
    player.update(dt)


def draw():
    surface.fill(COLOR["DARK_GRAY"])

    # Draw Player as a square    
    pygame.draw.rect(surface=surface, color=COLOR["YELLOW"],
                     rect=pygame.Rect(player.px-player.size/2,
                                      player.py-player.size/2,
                                      player.size, player.size))


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.velocity[1] = -1

            if event.key == pygame.K_a:
                player.velocity[0] = -1

            if event.key == pygame.K_s:
                player.velocity[1] = 1

            if event.key == pygame.K_d:
                player.velocity[0] = 1

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player.velocity[1] = 0

            if event.key == pygame.K_a or event.key == pygame.K_d:
                player.velocity[0] = 0    


clock = pygame.time.Clock()
surface = pygame.display.set_mode(SETTINGS["WINDOW_SIZE"])
surface.fill(COLOR["DARK_GRAY"])
px, py = SETTINGS["PLAYER_SPOS"]
player = Player(px, py, SETTINGS["PLAYER_SIZE"], SETTINGS["PLAYER_SPEED"])

def main():

    pygame.init()
    pygame.display.set_caption(SETTINGS["TITLE"])
    pygame.display.set_icon(pygame.image.load(SETTINGS["ICON_URL"]))

    while True:
        pygame.display.update()
        dt=clock.tick(SETTINGS["FPS"]) / 1000
        handle_events()
        draw()
        update(dt)


if __name__ == "__main__":
    main()
