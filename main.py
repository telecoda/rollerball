#!/usr/bin/env python
from game import Rollerball, DESKTOP, SENSE_HAT
import argparse

parser = argparse.ArgumentParser(description='Rollerball')
parser.add_argument('desktop', nargs='?', help='Render on desktop',  default=True)
args = parser.parse_args()

if __name__ == "__main__":

    if args.desktop:
        game = Rollerball(platform=DESKTOP)
    else:
        game = Rollerball(platform=SENSE_HAT)
    game.run()
