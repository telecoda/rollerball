class AbstractRenderer(object):
    def __init__(self):
    	pass

    def render(self, board):	
    	pass


def get_pygame_renderer():
	from pygame_wrapper import *
	return DesktopRenderer()

def get_sensehat_renderer():
	from sensehat_wrapper import SenseHATRenderer
	return SenseHATRenderer()
