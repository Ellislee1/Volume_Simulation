#!/usr/bin/env python
"""Util
A collection of utility functions shared between multiple classes.
"""

from math import atan2, degrees

import numpy as np
from shapely.geometry import Point as pte
from shapely.geometry.polygon import Polygon
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

def get_heading(p1: Point, p2: Point):
    """
    Get the heading from point 1 to point 2

    Parameters
    ----------
    p1: Point
        The point of the first position
    
    p2: Point
        The point of the first position
    """

    x = p2.x - p1.x
    y = p2.y - p1.y

    return int(((degrees(atan2(x,y))+180)*-1)%360)

def in_bound(bounds: [(int,int)] , pos: Point) -> bool:
        """
        Find out if a point is in some polygon

        Parameters
        ----------
        bounds: [(int,int)]
            The polygon area as an array of points

        pos: Point
            The point to check
        """

        poly = Polygon(bounds)
        return poly.contains(pte(pos.get()))

def dist_to_line(p1: Point, p2: Point, p3: Point) -> float:
    """
    For a given line, get the distance to the closest point on that line

    Parameters
    ----------
    p1: Point
        The first point on that line
    
    p1: Point
        The second point on that line
    
    p3: Point
        The point ot measure to
    """
    x1, y1 = p1.get()
    x2, y2 = p2.get()
    x3, y3 = p3.get()

    dx, dy = x2-x1, y2-y1
    det = (dx*dx) + (dy*dy)
    a = (dy*(y3-y1)+dx*(x3-x1))/det

    cx, cy = x1+a*dx,y1+a*dy

    min_x, min_y = min(x1,x2), min(y1,y2)
    max_x, max_y = max(x1,x2), max(y1,y2)

    if not(min_x <= cx <= max_x) or not(min_y <= cy <= max_y):
        return 9e10 # line extends past the reach so value is not valid


    return get_dist(Point(cx,cy), p3)


