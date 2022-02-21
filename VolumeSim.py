#!/usr/bin/env python
"""VolumeSim.py is the main enterance into the volume simulation and runs the basic simulation.

The main method for default running with no addons, used for testing and evaluating the environments behaviour.

Constants
---------
AREA
    The default world area
FPS
    The default simulation frame per second
SCALE
    The default world scale
"""

import argparse
import sys
import threading

from src.simulation.environment import Environment
from src.ui.ui import Window
from src.geography.point import Point

__author__ = "Ellis Thompson"
__credits__ = ["Ellis Thompson"]

__license__ = "GNU GPLv3"
__maintainer__ = "Ellis Thompson"
__email__ = "thompson_e@gwu.edu"
__status__ = "Development"


AREA = (800,800)
FPS = (60)
SCALE = 1
TEST_FILE = 'files/cohesive_env/env1.json'

def main(area: int, scale: float, fps: int):
    """
    The main method for running the simulation

    Parameters
    ----------
    area: int
        The area of the world
    
    scale: float
        The scale of the world
    
    fps: int
        The fps to run the simulation in
    """
    env = Environment(area=area, scale=scale, fps=fps, start_points=[Point(50, 100), Point(400, 227), Point(650,526)], env_path=TEST_FILE)
    window = Window(env, area, fps)

    t = threading.Thread(target=env.run)
    t.daemon = True

    t.start()
    window.run()
    env.running = False
    t.join()

    sys.exit()

if __name__ == "__main__":
    main(AREA,SCALE,FPS)
