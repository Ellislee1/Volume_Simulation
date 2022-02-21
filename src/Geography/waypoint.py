#!/usr/bin/env python
"""waypoint.py holds the Waypoint information.

A waypoint is an extension of a Point. It holds extra information.
"""

import string

import src.assets.colours as c
from numpy import inf
from pygame import draw as d
from pygame import font
from src.geography.point import Point
from src.utility.util import in_bound
from src.utility.util import dist_to_line

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
    
    bounds: the bounds 
    
    Methods
    -------
    draw(WINDOW)
        Draw the waypoint to the output window
    
    has_reached(apos)
        Returns if the aircraft has reached the waypoint bounds
    
    dist_from(apos)
        Returns the distance to the waypoint bounds from the aircraft's current position
    
    """
    def __init__(self, _id:string, x:float, y:float, x_pad = 25, y_pad = 50):
        """
        Parameters
        ----------
        _id: string
            The unique ID of the waypoint
        
        x: float
            The x coordinate of the waypoint
        
        y: float
            The y coordinate of the waypoint
        
        x_pad: float
            The padding to create the waypoint boundary (x)
        
        y_pad: float
            The padding to create the waypoint boundary (y)
        """
        super().__init__(x, y)  # Initilise parent

        self._id = _id              # The unique ID for the waypoint

        # tl, bl, tr, br
        self.bounds = [(self.x-x_pad,self.y-y_pad), (self.x+x_pad,self.y-y_pad), (self.x+x_pad,self.y+y_pad), (self.x-x_pad,self.y+y_pad)]
    
    def draw(self, WINDOW):
        """
        Draw the waypoint to the output window

        Parameters
        ----------
        WINDOW
            The output window
        """

        f = font.SysFont('couriernew', 15)
        d.polygon(WINDOW, c.WHITE, [(self.x-2,self.y-2), (self.x+2,self.y-2), (self.x+2,self.y+2), (self.x-2,self.y+2)])
        d.polygon(WINDOW, c.WHITE, self.bounds, width = 1)
        WINDOW.blit(f.render(f'{self._id}', True, c.WHITE), (self.x+35, self.y-55))
    
    def has_reached(self, apos: Point) -> bool:
        """
        Returns if the aircraft has reached the waypoint bounds

        Parameters
        ----------
        apos: Point
            The aircraft position
        """
        return in_bound(self.bounds, apos)
    
    def dist_from(self, apos: Point) -> float:
        """
        Returns the distance to the waypoint bounds from the aircraft's current position

        Parameters
        ----------
        apos: Point
            The aircraft position
        """

        min_dist = 9e10

        for i in range(-1, len(self.bounds)-1):
            min_dist = min(dist_to_line(Point(self.bounds[i][0],self.bounds[i][1]), Point(self.bounds[i+1][0],self.bounds[i+1][1]), apos),min_dist)
        
        return round(min_dist,3)
