import pygame
from pygame import display, draw, KEYDOWN
import time
from random import randint


xMax = 960
yMax = 710

class Drop():
    def __init__(self):
        self.center = [randint(1,xMax), randint(1, yMax)]
        self.radius = 1
        self.maxRadius = randint(20,150)
        self.color = [randint(50,250), randint(50,250), randint(50,250)]


screen = display.set_mode([xMax,yMax])
drops = []
clock = pygame.time.Clock()
drops.append(Drop())

while True:
    screen.fill([0,0,0])
    for d in drops[:]:
        draw.circle(screen, d.color, d.center, d.radius, 1)
        d.radius += 5
        if d.radius >= d.maxRadius:
            drops.remove(d)
        drops.append(Drop())
        display.flip()
        clock.tick(60)
        if(pygame.event.poll().type == KEYDOWN):
            exit()


