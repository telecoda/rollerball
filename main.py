#!/usr/bin/env python
from game import Rollerball, DESKTOP, SENSE_HAT
import argparse

parser = argparse.ArgumentParser(description='Rollerball')
parser.add_argument('--sensehat', dest='sense_hat_display', action='store_true')
parser.add_argument('--no-sensehat', dest='sense_hat_display', action='store_false')
parser.set_defaults(sense_hat_display=True)

args = parser.parse_args()

if __name__ == "__main__":

    if args.sense_hat_display:
        game = Rollerball(platform=SENSE_HAT)
    else:
        game = Rollerball(platform=DESKTOP)
    game.run()
