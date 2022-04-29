import pygame
import sys
import math
from settings import SETTINGS, COLOR
from maps import TEST_ROOM


class Player:
    def __init__(self, px: float, py: float, size, speed: float, pa: float,ts:float) -> None:
        # player coordinates
        self.px = px
        self.py = py
        self.pa = math.radians(pa/math.pi)
        self.da=0
        self.size = size
        self.speed = speed
        self.ts=ts
        self.movement = 0 # 0 is in place, 1 is moving forward, -1 is moving backwards

    def update(self, dt):
        self.px += self.movement*(self.speed*dt)*math.cos(self.pa)
        self.py += self.movement*(self.speed*dt)*math.sin(self.pa)

        self.pa+=self.da*(self.ts*dt)
        if self.pa>2*math.pi:
            self.pa=-2*math.pi
        
        elif self.pa>2*math.pi:
            self.pa=-2*math.pi
        
        

# update stuff according to delta time value


def update(dt):
    player.update(dt)


def draw_2d_map():
    tz = SETTINGS["TILE_SIZE"]
    for y in range(0, len(TEST_ROOM)):
        for x in range(0, len(TEST_ROOM[0])):
            xo = x*tz
            yo = y*tz
            if TEST_ROOM[y][x] == 1:
                _color = COLOR["WHITE"]
            else:
                _color = COLOR["BLACK"]
            pygame.draw.rect(surface=surface, color=_color,
                             rect=pygame.Rect(xo, yo, tz-1, tz-1))


def draw_player():
        # Draw Player as a square
    pygame.draw.rect(surface=surface, color=COLOR["YELLOW"],
                     rect=pygame.Rect(player.px-player.size/2,
                                      player.py-player.size/2,
                                      player.size, player.size))
    pygame.draw.line(surface=surface,color=COLOR["YELLOW"],
                        start_pos=(player.px,player.py),
                        end_pos=(player.px+math.cos(player.pa)*player.size*2,
                                 player.py+math.sin(player.pa)*player.size*2),width=int(player.size/4))


def draw():
    # draw background
    surface.fill(COLOR["DARK_GRAY"])
    draw_2d_map()
    draw_player()



def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.movement=1

            if event.key == pygame.K_s:
                player.movement=-1
                
            if event.key == pygame.K_a:
                player.da-=3

            if event.key == pygame.K_d:
                player.da+=3
                
        elif event.type == pygame.KEYUP:
            if event.key==pygame.K_w or  event.key==pygame.K_s:
                player.movement=0
            
            if event.key==pygame.K_a or event.key==pygame.K_d:
                player.da=0
            


clock = pygame.time.Clock()
surface = pygame.display.set_mode(SETTINGS["WINDOW_SIZE"],pygame.FULLSCREEN)
surface.fill(COLOR["DARK_GRAY"])
px, py = SETTINGS["PLAYER_SPOS"]
player = Player(px, py, SETTINGS["PLAYER_SIZE"],
                        SETTINGS["PLAYER_SPEED"],
                        SETTINGS["PLAYER_SANGLE"],
                        SETTINGS["PLAYER_TSPEED"])


def main():

    pygame.init()
    pygame.display.set_caption(SETTINGS["TITLE"])
    pygame.display.set_icon(pygame.image.load(SETTINGS["ICON_URL"]))

    while True:
        dt = clock.tick(SETTINGS["FPS"]) / 1000
        handle_events()
        draw()
        update(dt)
        pygame.display.update()


if __name__ == "__main__":
    main()
