import os, time
import pygame
from pygame.locals import *
import renderer


DESKTOP = 1
SENSE_HAT = 2

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')


def load_image(file):
    "loads an image"
    file = os.path.join(main_dir, 'data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' %
                         (file, pygame.get_error()))
    # return surface.convert_alpha()
    return surface.convert()


class Rollerball(object):

    def __init__(self, platform=DESKTOP):

        # init correct display renderer
        if platform == SENSE_HAT:
            self.renderer = renderer.get_sensehat_renderer()
            self.sensors
        else:
            self.renderer = renderer.get_pygame_renderer()

        self.init_assets()

        self.maze = Maze('maze_01.png')
        self.maze_width = self.maze.width
        self.maze_height = self.maze.height
        self.board = Board()
        self.ball = Ball(2, 4)
        self.set_viewport(0, 0)

    def handle_input_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return True
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return True
            elif event.type == KEYDOWN and (event.key == K_LEFT):
                self.move_left()
            elif event.type == KEYDOWN and (event.key == K_RIGHT):
                self.move_right()
            elif event.type == KEYDOWN and (event.key == K_UP):
                self.move_up()
            elif event.type == KEYDOWN and (event.key == K_DOWN):
                self.move_down()

    def init_assets(self):
        # this is where we load all the game assets
        self.ball_image = load_image('ball.png')

    def move_down(self):
        if self.ball.y < renderer.ROWS-1:
            self.ball.y += 1
        if self.view_y < self.maze_height - renderer.ROWS:
            self.view_y += 1

    def move_left(self):
        if self.ball.x > 0:
            self.ball.x -= 1
        if self.view_x > 0:
            self.view_x -= 1

    def move_right(self):
        if self.ball.x < renderer.COLS-1:
            self.ball.x += 1
        if self.view_x < self.maze_width - renderer.COLS:
            self.view_x += 1

    def move_up(self):
        if self.ball.y > 0:
            self.ball.y -= 1
        if self.view_y > 0:
            self.view_y -= 1

    def render_board(self):
        '''
        render_board creates an 8x8 board that can be passed to a renderer
        '''

        # init board
        #self.board.init_board()

        self.board.cells = self.maze.get_cells(self.view_x, self.view_y)
        # overlay ball position
        self.board.cells[self.ball.x][self.ball.y].set_colour(renderer.BLUE)
        self.renderer.render(self.board.cells)

    def run(self):
        '''
        Run forever
        '''

        quit = False

        while not quit:
            # handle input events
            quit = self.handle_input_events()
            self.render_board()
            time.sleep(0.1)

    def set_viewport(self, x, y):
        self.view_x = x
        self.view_y = y


class Board(object):

    def __init__(self):
        self.init_board()

    def init_board(self):
        self.cells = [
            [Cell(renderer.WHITE) for y in range(renderer.ROWS)]
            for x in range(renderer.COLS)]

        for y in range(0, renderer.ROWS):
            self.cells[4][y].set_colour(renderer.RED)
        for x in range(0, renderer.COLS):
            self.cells[x][4].set_colour(renderer.RED)


class Cell(object):

    def __init__(self, colour):
        self.colour = colour

    def set_colour(self, colour):
        self.colour = colour


class Ball(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Maze(object):

    def __init__(self, filename):
        self.image = load_image('maze_01.png')
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def get_cells(self, view_x, view_y):
        cells = [
            [Cell(self.image.get_at((view_x + x,view_y + y))) for y in range(renderer.ROWS)]
            for x in range(renderer.COLS)]

        return cells


