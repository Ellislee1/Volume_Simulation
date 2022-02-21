#!/usr/bin/env python
"""route.py defines the class for handling routes flown by an aircraft.
"""

import string
from queue import Queue

import src.assets.colours as c
from pygame import draw as d
from src.geography.point import Point
from src.geography.waypoint import Waypoint
from src.utility.util import dist_to_line, get_dist, get_heading

__author__ = "Ellis Thompson"
__credits__ = ["Ellis Thompson"]

__license__ = "GNU GPLv3"
__maintainer__ = "Ellis Thompson"
__email__ = "thompson_e@gwu.edu"
__status__ = "Development"


class Route:
    """
    Defines a route of either corridors or waypoints.

    Attributes
    ----------
    _id: string
        The unique ID of the route
    
    origional_route: [Point/Waypoint]
        The origional unformatted route

    route: [Point/Waypoint]
        A queue of each waypoint on the route
    
    start: Point/Waypoint
        The start point of the route, used for generating aircraft
    
    next_waypoint: Point/Waypoint
        The next point the aircraft is to visit
    
    previous_waypoint: Point/Waypoint
        The aircrafts previous waypoint
    
    init_heading: int
        The initial route heading

    Methods
    -------
    init_route(route)
        Initilise the route and prepare the next waypoints
    
    update(ac_pos, wpt_dist = 10, max_dist = 25, acc = 3)
        Run an update and all checks on the aircraft position

    get_in_bound(pos, max_dist = 25, acc = 3)
        Returns if the a point is too far from the path between the next waypoint and previous waypoint

    dist_to_next(pos)
        Returns the distance from one point to the next waypoint

    copy
        Copy the route to a new class

    draw(WINDOW)
        Place holder for handling the draw function of the route

    """
    def __init__(self, _id: string, route):
        """
        Parameters
        ----------
        _id: string
            The unique ID of the route
        
        route: [Point/Waypoint]
            The waypoints in order on the route

        Raises
        ------
        Exception
            Route must have at least 2 points, a start and end
        """

        if len(route) < 2:
            raise Exception("Route must have a start and end waypoint")

        self._id = _id                  # Unique ID of the route
        self.origional_route = route    # The unedited route

        self.init_route(route)
    
    def init_route(self, route):
        """
        Initilise the route and prepare the next waypoints

        Parameters
        ----------
        route: [Point/Waypoint]
            The waypoints in order on the route
        """

        self.route = Queue()

        for point in route:
            self.route.put(point)
        
        self.start = self.route.get()                                   # The start point of the route
        self.next_waypoint = self.route.get()                           # The next waypoint after start
        self.previous_waypoint = self.start                             # The waypoint the aircraft is leaving

        self.init_heading = get_heading(self.start, self.next_waypoint) # The initial heading for the route
    
    def update(self, ac_pos: Point, wpt_dist:float = 10, max_dist:int = 25, acc:int = 3) -> int:
        """
        Run an update and all checks on the aircraft position

        Parameters
        ----------
        ac_pos: Point
            The current aircraft postion

        wpt_dist: float
            The waypoint threashold distance for arrival

        max_dist: float
            The maximum deviation distance where -1 is infinate

        acc: int
            The accuracy to be considered
        """

        d_next = self.dist_to_next(ac_pos)
        in_bound = self.get_in_bound(ac_pos, max_dist, acc)

        # Has the aircraft reached it's goal
        if self.next_waypoint.has_reached(ac_pos):
            if self.route.qsize() <= 0:
                return 1
            self.next_waypoint = self.route.get()
        
        # 
        if not in_bound[0]:
            return 2
        
        return 0
    
    def get_in_bound(self, pos: Point, max_dist: float = 25, acc:int = 3) -> (bool, float):
        """
        Returns if the a point is too far from the path between the next waypoint and previous waypoint

        Parameters
        ----------
        pos: Point
            The point of the position to get the distance of
        
        max_dist: float
            The maximum deviation distance where -1 is infinate

        acc: int
            The accuracy to be considered
        """

        if max_dist == -1:
            return True
        
       

        distance = round(dist_to_line(self.previous_waypoint, self.next_waypoint, pos), acc)

        if distance < max_dist:
            return True, distance
        
        return False, distance
    
    def dist_to_next(self, pos: Point) -> float:
        """
        Returns the distance from one point to the next waypoint

        Parameters
        ----------
        pos: Point
            The point to measure distance to next waypoint
        """

        return round(get_dist(self.next_waypoint, pos),5)

    def copy(self):
        """
        Copy the route to a new class
        """
        return Route(self._id, self.origional_route)
    
    def draw(self, WINDOW):
        """
        Place holder for handling the draw function of the route

        Parameters
        ----------
        WINDOW
            The output window
        """
        path = []

        for point in self.origional_route:
            path.append(point.get())

        d.lines(WINDOW,c.WHITE,False,path, width = 1)
