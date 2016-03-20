from abstract import AbstractRenderer
import os
import pygame
from constants import *
from sense_hat import SenseHat

class SenseHATRenderer(AbstractRenderer):
    def __init__(self):
        super(AbstractRenderer,self).__init__()

        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()
        pygame.display.set_mode((1,1))
        self.sense = SenseHat()

    def render(self, cells):
        print "Rendering cells"
        for x in range(0, COLS):
            for y in range(0, ROWS):
                colour = cells[x][y].colour
                r = colour[0]
                g = colour[1]
                b = colour[2]
                self.sense.set_pixel(x, y, (r, g, b))


