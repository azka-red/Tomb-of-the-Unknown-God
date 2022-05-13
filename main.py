import pygame
from pygame.locals import *
import sys
import math
from settings import SETTINGS, COLOR
from utils import dist
from maps import TEST_ROOM
from player import Player


def draw_3d_rays():
    px = player.px
    py = player.py
    tile_size = SETTINGS["TILE_SIZE"]
    wx_size, wy_size = SETTINGS["RENDER_SIZE"]
    fov = SETTINGS["FOV"]
    # aux variable to calculate nearest ry value
    bit_mod = int(math.log(tile_size, 2))
    m_size_x = len(TEST_ROOM[0])
    m_size_y = len(TEST_ROOM)

    dr = math.radians(fov/wx_size)
    ra = player.pa-dr*(wx_size-tile_size*m_size_x)/2
    if (ra < 0):
        ra += 2*math.pi

    if (ra > 2*math.pi):
        ra -= 2*math.pi

    # raycasting loop for 400 vertical lines
    for r in range(400):

        # check horizontal lines
        dof = 0
        dist_h = 1000000
        hx = px
        hy = py
        if (ra > math.pi):  # looking up
            atan = float(-1/math.tan(ra))
            ry = (int(py) >> bit_mod << bit_mod)-0.0001
            rx = (py-ry)*atan+px
            yo = -tile_size
            xo = -yo*atan
        if(ra < math.pi):  # looking down
            atan = float(-1/math.tan(ra))
            ry = (int(py) >> bit_mod << bit_mod)+tile_size
            rx = (py-ry)*atan+px
            yo = tile_size
            xo = -yo*atan
        if ra == 0 or ra == math.pi:  # looking left or right
            rx = px
            ry = py
            dof = m_size_y
        while dof < m_size_y:  # check as much vertical tiles the map has
            mx = int(rx) >> bit_mod
            my = int(ry) >> bit_mod

            # make sure whe just check between possible map coordinates
            if(0 <= mx < m_size_x and 0 <= my < m_size_y) and TEST_ROOM[my][mx] == 1:
                dof = m_size_y
                hx = rx
                hy = ry
                dist_h = dist(px, py, hx, hy)

            else:
                rx += xo
                ry += yo
                dof += 1

        # check vertical lines
        dof = 0
        dist_v = 1000000
        vx = px
        vy = py

        if (ra > math.pi/2 and ra < 3*math.pi/2):  # looking left
            ntan = -float(math.tan(ra))
            rx = (int(px) >> bit_mod << bit_mod)-0.0001
            ry = (px-rx)*ntan+py
            xo = -tile_size
            yo = -xo*ntan
        if(ra < math.pi/2 or ra > 3*math.pi/2):  # looking right
            ntan = -float(math.tan(ra))
            rx = (int(px) >> bit_mod << bit_mod)+tile_size
            ry = (px-rx)*ntan+py
            xo = tile_size
            yo = -xo*ntan
        if ra == 0 or ra == math.pi:  # looking up or down
            rx = px
            ry = py
            dof = m_size_y
        while dof < m_size_y:  # check as much vertical tiles the map has
            mx = int(rx) >> bit_mod
            my = int(ry) >> bit_mod

            # make sure whe just check between possible map coordinates
            if(0 <= mx < m_size_x and 0 <= my < m_size_y) and TEST_ROOM[my][mx] == 1:
                dof = m_size_y
                vx = rx
                vy = ry
                dist_v = dist(px, py, vx, vy)

            else:
                rx += xo
                ry += yo
                dof += 1
        if (dist_h < dist_v):
            rx = hx
            ry = hy
            dist_t = dist_h
        if (dist_v < dist_h):
            rx = vx
            ry = vy
            dist_t = dist_v
        pygame.draw.line(surface=surface, color=COLOR["RED"],
                         start_pos=(player.px, player.py),
                         end_pos=(rx, ry))

        # draw 3d walls
        ca = player.pa-ra
        if ca < 0:
            ca += 2*math.pi
        if ca > 2*math.pi:
            ca -= 2*math.pi
        dist_t = dist_t*math.cos(ca)

        line_h = (tile_size*400)/dist_t
        if line_h > 270:
            line_h = 270
        line_off = 135-line_h/2

        # wall color based on distance to simulate some basic shading
        c_color = (255/dist_t*8)+5
        if c_color > 255:
            c_color = 255
        if c_color < 0:
            c_color = 0

        pygame.draw.line(surface=surface, color=(c_color, 0, 0),
                         start_pos=(r+80, line_off), end_pos=(r+80, line_h+line_off), width=1)

        ra += dr
        if (ra < 0):
            ra += 2*math.pi

        if (ra > 2*math.pi):
            ra -= 2*math.pi


def draw_player():
    # Draw Player as a square
    pygame.draw.rect(surface=surface, color=COLOR["YELLOW"],
                     rect=pygame.Rect(player.px-player.size/2,
                                      player.py-player.size/2,
                                      player.size, player.size))
    pygame.draw.line(surface=surface, color=COLOR["YELLOW"],
                     start_pos=(player.px, player.py),
                     end_pos=(player.px+math.cos(player.pa)*player.size*2,
                              player.py+math.sin(player.pa)*player.size*2), width=int(player.size/4))


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


def draw():
    # draw background
    surface.fill(COLOR["DARK_GRAY"])
    draw_2d_map()
    draw_3d_rays()
    draw_player()


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.movement = 1

            if event.key == pygame.K_s:
                player.movement = -1

            if event.key == pygame.K_a:
                player.da -= 3

            if event.key == pygame.K_d:
                player.da += 3

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player.movement = 0

            if event.key == pygame.K_a or event.key == pygame.K_d:
                player.da = 0

        elif event.type == VIDEORESIZE:
            global window
            window = pygame.display.set_mode(
                event.size, HWSURFACE | DOUBLEBUF | RESIZABLE)

# update stuff according to delta time value


def update(dt):
    player.update(dt)


#################################################################
clock = pygame.time.Clock()

px, py = SETTINGS["PLAYER_SPOS"]
player = Player(px, py, SETTINGS["PLAYER_SIZE"],
                SETTINGS["PLAYER_SPEED"],
                SETTINGS["PLAYER_SANGLE"],
                SETTINGS["PLAYER_TSPEED"])

##################################################################
pygame.init()
pygame.display.set_caption(SETTINGS["TITLE"])
pygame.display.set_icon(pygame.image.load(SETTINGS["ICON_URL"]))

# window that contains fake screen and surface
window = pygame.display.set_mode(
    SETTINGS["WINDOW_SIZE"], HWSURFACE | DOUBLEBUF | RESIZABLE)

#copy of container window for scaling purposes
#fake_screen = window.copy()
# actual drawing surface
surface=pygame.surface.Surface(SETTINGS["RENDER_SIZE"])

while True:
    dt = clock.tick(SETTINGS["FPS"]) / 1000
    handle_events()
    draw()
    update(dt)
    #fake_screen.blit(surface,(0,0))
    window.blit(pygame.transform.scale(
        surface, window.get_rect().size), (0, 0))

    pygame.display.flip()
