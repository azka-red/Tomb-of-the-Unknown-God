from math import radians,cos,sin,pi

class Player:
    def __init__(self, px: float, py: float, size, speed: float, pa: float, ts: float) -> None:
        # player coordinates
        self.px = px
        self.py = py
        self.pa = radians(pa)
        self.da = 0
        self.size = size
        self.speed = speed
        self.ts = ts
        self.movement = 0  # 0 is in place, 1 is moving forward, -1 is moving backwards

    def update(self, dt):
        self.px += self.movement*(self.speed*dt)*cos(self.pa)
        self.py += self.movement*(self.speed*dt)*sin(self.pa)

        self.pa += self.da*(self.ts*dt)
        if self.pa > 2*pi:
            self.pa -= 2*pi

        elif self.pa < 0:
            self.pa += 2*pi

