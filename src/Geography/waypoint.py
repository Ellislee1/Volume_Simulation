#!/usr/bin/env python
"""waypoint.py holds the Waypoint information.

A waypoint is an extension of a Point. It holds extra information.
"""

import string

import src.assets.colours as c
from pygame import draw as d
from pygame import font
from src.geography.point import Point

__author__ = "Ellis Thompson"
__credits__ = ["Ellis Thompson"]

__license__ = "GNU GPLv3"
__maintainer__ = "Ellis Thompson"
__email__ = "thompson_e@gwu.edu"
__status__ = "Development"

class Waypoint(Point):
    """
    A waypoint for an aircraft to use as a navigation aid. A Waypoint is an extension of a Point.

    Attributes
    ----------
    _id: string
        The unique ID of the waypoint
    
    Methods
    -------
    draw(WINDOW)
        Draw the waypoint to the output window
    
    """
    def __init__(self, _id:string, x:float, y:float):
        """
        Parameters
        ----------
        _id: string
            The unique ID of the waypoint
        
        x: float
            The x coordinate of the waypoint
        
        y: float
            The y coordinate of the waypoint
        """
        super().__init__(x, y)  # Initilise parent

        self._id = _id              # The unique ID for the waypoint
    
    def draw(self, WINDOW):
        """
        Draw the waypoint to the output window

        Parameters
        ----------
        WINDOW
            The output window
        """

        f = font.SysFont('couriernew', 15)
        d.polygon(WINDOW, c.WHITE, [(self.x-5,self.y-5), (self.x+5,self.y-5), (self.x+5,self.y+5), (self.x-5,self.y+5)])
        WINDOW.blit(f.render(f'{self._id}', True, c.WHITE), (self.x+15, self.y-5))
