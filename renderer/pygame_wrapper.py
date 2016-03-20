from abstract import AbstractRenderer
from constants import *
import pygame
from pygame.locals import *

TILE_WIDTH = 32

SPACING = 2

SCREEN_WIDTH = TILE_WIDTH * COLS + SPACING * (COLS+1)
SCREEN_HEIGHT = TILE_WIDTH * ROWS + SPACING * (ROWS+1)

KEY_REPEAT = 50  # Key repeat in milliseconds


class DesktopRenderer(AbstractRenderer):
    def __init__(self):
        super(AbstractRenderer, self).__init__()

        # init screen
        pygame.init()

        pygame.display.set_caption("Rollerball")
        pygame.key.set_repeat(KEY_REPEAT)

        flags = DOUBLEBUF | HWSURFACE
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT), flags)

        self.cx = SCREEN_WIDTH/2
        self.cy = SCREEN_HEIGHT/2

    def render(self, cells):
        self.screen.fill((0, 0, 0))

        for x in range(0, COLS):
            for y in range(0, ROWS):
                cell = cells[x][y]
                cell_x = ((x + 1) * SPACING) + (x * TILE_WIDTH)
                cell_y = ((y + 1) * SPACING) + (y * TILE_WIDTH)
                rect = pygame.Rect(cell_x, cell_y, TILE_WIDTH, TILE_WIDTH)
                self.screen.fill(color=cell.colour, rect=rect)
        pygame.display.flip()
