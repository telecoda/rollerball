import os
import time
import pygame
from pygame.locals import *
import renderer
from stick import SenseStick

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

    def __init__(self, platform=SENSE_HAT):

        # init correct display renderer
        if platform == SENSE_HAT:
            print 'Using SenseHAT display'
            self.renderer = renderer.get_sensehat_renderer()
            self.stick = SenseStick()
        else:
            print 'Using desktop display'
            self.renderer = renderer.get_pygame_renderer()

        self.platform = platform

        self.init_assets()

        self.maze = Maze('maze_01.png')
        self.maze_width = self.maze.width
        self.maze_height = self.maze.height
        self.board = Board()
        self.ball = Ball(3, 3)
        self.set_viewport(7, 15)

    def handle_keyboard_events(self):
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

    def handle_stick_events(self):
        event = self.stick.read()
        print event
        if event.key == SenseStick.KEY_UP and event.state == SenseStick.STATE_PRESS:
            print 'Move up'
            self.move_up()
        elif event.key == SenseStick.KEY_DOWN and event.state == SenseStick.STATE_PRESS:
            self.move_down()
        elif event.key == SenseStick.KEY_RIGHT and event.state == SenseStick.STATE_PRESS:
            self.move_right()
        elif event.key == SenseStick.KEY_LEFT and event.state == SenseStick.STATE_PRESS:
            self.move_left()

    def init_assets(self):
        # this is where we load all the game assets
        self.ball_image = load_image('ball.png')

    def move_down(self):
        if self.view_y < self.maze_height - renderer.ROWS:
            cell_1 = self.board.cells[self.ball.x][self.ball.y+2]
            cell_2 = self.board.cells[self.ball.x+1][self.ball.y+2]
            if cell_1.colour != renderer.BLACK and cell_2.colour != renderer.BLACK:
                self.view_y += 1

    def move_left(self):
        if self.view_x > 0:
            # check maze is clear to move right
            cell_1 = self.board.cells[self.ball.x-1][self.ball.y]
            cell_2 = self.board.cells[self.ball.x-1][self.ball.y+1]
            if cell_1.colour != renderer.BLACK and cell_2.colour != renderer.BLACK:
                self.view_x -= 1

    def move_right(self):
        if self.view_x < self.maze_width - renderer.COLS:
            # check maze is clear to move right
            cell_1 = self.board.cells[self.ball.x+2][self.ball.y]
            cell_2 = self.board.cells[self.ball.x+2][self.ball.y+1]
            if cell_1.colour != renderer.BLACK and cell_2.colour != renderer.BLACK:
                self.view_x += 1

    def move_up(self):
        if self.view_y > 0:
            cell_1 = self.board.cells[self.ball.x][self.ball.y-1]
            cell_2 = self.board.cells[self.ball.x+1][self.ball.y-1]
            if cell_1.colour != renderer.BLACK and cell_2.colour != renderer.BLACK:
                self.view_y -= 1

    def render_board(self):
        '''
        render_board creates an 8x8 board that can be passed to a renderer
        '''

        self.board.cells = self.maze.get_cells(self.view_x, self.view_y)
        # overlay ball position
        ball_cells = self.ball.get_cells()
        self.board.cells[3][3].set_colour(ball_cells[0][0].colour)
        self.board.cells[4][3].set_colour(ball_cells[1][0].colour)
        self.board.cells[3][4].set_colour(ball_cells[0][1].colour)
        self.board.cells[4][4].set_colour(ball_cells[1][1].colour)

        self.renderer.render(self.board.cells)

    def run(self):
        '''
        Run forever
        '''

        quit = False

        while not quit:
            if self.platform == SENSE_HAT:
                self.handle_stick_events()
            else:
                quit = self.handle_keyboard_events()

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
        self.image = load_image('ball.png')
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = x
        self.y = y

    def get_cells(self):
        cells = [
            [Cell(self.image.get_at((x, y))) for y in range(self.height)]
            for x in range(self.width)]

        return cells


class Maze(object):

    def __init__(self, filename):
        self.image = load_image('maze_01.png')
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def get_cells(self, view_x, view_y):
        cells = [
            [Cell(self.image.get_at((view_x + x, view_y + y))) for y in range(renderer.ROWS)]
            for x in range(renderer.COLS)]

        return cells
