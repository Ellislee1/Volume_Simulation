"""Util
A collection of utility functions shared between multiple classes.
"""

import numpy as np

from src.geography.point import Point

__author__ = "Ellis Thompson"
__credits__ = ["Ellis Thompson"]

__license__ = "GNU GPLv3"
__maintainer__ = "Ellis Thompson"
__email__ = "thompson_e@gwu.edu"
__status__ = "Development"

def get_dist(p1: Point, p2: Point):
    """
    Get the distance between two points

    Parameters
    ----------
    p1: Point
        The point of the first position
    
    p2: Point
        The point of the first position
    """
    return np.sqrt((p2.x-p1.x)**2+(p2.y-p1.y)**2)
