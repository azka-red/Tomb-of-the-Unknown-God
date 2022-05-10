from math import sqrt
# returns distance between 2 points
def dist(ax: float, ay: float, bx: float, by: float):
    return (sqrt((bx-ax)**2+(by-ay)**2))