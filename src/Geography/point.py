#!/usr/bin/env python
"""The Point representing an x, y coordinate in the environment plane.

This is the x, y coordinate of an object in the simulation environment. A point can
also be updated or changed.
"""

from math import cos, sin

__author__ = "Ellis Thompson"
__credits__ = ["Ellis Thompson"]

__license__ = "GNU GPLv3"
__maintainer__ = "Ellis Thompson"
__email__ = "thompson_e@gwu.edu"
__status__ = "Development"


class Point:
    """
    The x, y coordinate of an object in the environment space.

    Attributes
    ----------
    x: float
        The x coordinate
    
    y: float
        The y coordinate

    Methods
    -------
    update(h, d)
        Move the current point by some distance in some heading
    
    get
        Returns the coordinates of the point
    """
    def __init__(self, x: float, y: float):
        """
        Parameters
        ----------
        x: float
            The x coordinate
        
        y: float
            The y coordinate
        """
        self.x = x
        self.y = y
    
    def update(self, h:float, d:float):
        """
        Move the point in a given direction by some distance (m)

        Parameters
        ----------
        h: float
            The heading that point should be moved to
        
        d: float
            The distance the point should be moved
        """

        self.x = self.x + d*cos(h)
        self.y = self.y + d*sin(h)
    
    def get(self) -> (float, float):
        """
        Returns the coordinates of the point
        """
        return(self.x, self.y)
