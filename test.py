import pygame
 
class Ticker:
    def __init__(self, length):
        self.next_tick = length
        self.length = length
 
    def elapse(self, ticks):
        if ticks > self.next_tick:
            self.next_tick += self.length
            return True
        return False
 
class Screen:
    WIDTH = 1280
    HEIGHT = 720
 
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Scanlines")
        self.screen = pygame.display.set_mode(self.get_size())
        self.clock = pygame.time.Clock()
        self.running = False
        font = pygame.font.Font(None, 24)
        color = pygame.Color('forestgreen')
        self.text = font.render("testing scanlines", 1, color)
        self.text2 = font.render("line two", 1, color)
 
        self.create_scanline()
        self.lines_position = list(range(0, Screen.HEIGHT + 1, 200))
        self.scanline_ticker = Ticker(2)
        self.scanline_speed = 10
 
    def create_scanline(self):
        self.scanline = pygame.Surface((1, 200))
        self.scanline = self.scanline.convert_alpha()
        color = pygame.Color(0, 180, 0)
        color.a = 15
        for a in range(100):
            color.g -= 1
            self.scanline.set_at((0, a), color)
            self.scanline.set_at((0, 199 - a), color)
 
        self.scanline = pygame.transform.scale(self.scanline, (Screen.WIDTH, 200))
 
    def draw(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.text, (80, 100))
        self.screen.blit(self.text2, (80, 150))
 
        ticks = pygame.time.get_ticks()
        if self.scanline_ticker.elapse(ticks):
            for i in range(len(self.lines_position)):
                self.lines_position[i] -= self.scanline_speed
                if self.lines_position[i] < -199:
                    self.lines_position[i] = Screen.HEIGHT
 
        for line in self.lines_position:
            self.screen.blit(self.scanline, (0, line), None, pygame.BLEND_RGBA_MULT)
            self.screen.blit(self.scanline, (0, line), None)
 
    def get_size(self):
        return Screen.WIDTH, Screen.HEIGHT
 
    def get_rect(self):
        return pygame.Rect(0,0,Screen.WIDTH,Screen.HEIGHT)
 
    def loop(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
 
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
 
        pygame.quit()
 
if __name__ == '__main__':
    screen = Screen()
    screen.loop()