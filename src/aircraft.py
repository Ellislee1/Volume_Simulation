#!/usr/bin/env python
"""Provides the Aircraft class for the simulation, the aircraft is a simple simulated entity.

Aircraft is respoinsible for the simplified implementation of an aircraft.
"""

from math import pi, radians

from pygame import draw as d
from pygame import font

import src.visual.colours as c

__author__ = "Ellis Thompson"
__credits__ = ["Ellis Thompson"]

__license__ = "GNU GPLv3"
__maintainer__ = "Ellis Thompson"
__email__ = "thompson_e@gwu.edu"
__status__ = "Development"


class Aircraft:
    """
    Defines an aircraft and its calculations to take each step

    Attributes
    ----------
    _id: string
        The given ID of the aircraft
    pos: point
        The position of the aircraft
    spd: float
        The speed of the aircraft
    tas: float
        The visual true airspeed of the aircraft
    alt: float
        The altitude of the aircraft
    heading: float
        The heading of the aircraft
    scale: float
        The distance scale of the environment
    route: Route
        The route of the aircraft
    path: [Points]
        The path the aircraft has followed
    updater: int
        The number of times the aircraft has been updated
    point_constant: int
        A constant for the frequency for adding points to the path
    terminated: int
        How has the aircraft been terminated (0: exists, 1: safe, 2: out of bounds, 3: collision)
    size: int
        Size of the visual aircraft
    boarder_size: int
        Size for the visual boarder of the aircraft
    text_boost: int
        Where the aircraft info text should start    

    Methods
    -------
    step(bounds)
        Simulates an aircraft step
    update_position
        Update the aircraft's position using speed, heading and current position
    in_bounds(bounds)
        Get if the aircraft is in all current bounds, the world and any corridors
    in_world(bounds)
        Test that the aircraft is in the world, return if it exists in the world
    in_corridor
        Test that, if the aircraft should be in a corridor, it is in that corridor
    draw(WINDOW)
        Draws the aircraft to the window
    draw_path
        Draw the path of the aircraft to the window
    def get_text_stats
        Get the text to output and its starting position

    """
    def __init__(self, _id:string, start_pos:Point, spd:float = 30, alt:float = 100, heading:float = 0, scale:float = 1, route:Route = None):
        """
        Parameters
        ----------
        _id: string
            The given ID of the aircraft
        start_pos: point
            The starting position of the aircraft
        spd: float
            The starting speed of the aircraft
        alt: float
            The altitude of the aircraft
        heading: float
            The heading of the aircraft
        scale: float
            The distance scale of the environment
        route: Route
            The route of the aircraft
        """
        self._id = _id                      # The aircraft ID
        self.position = start_pos           # The current aircraft position
        self.spd = (min(45,speed)/scale)/60 # The current aircraft speed (m/s)
        self.tas = spd                      # The visual true airspeed of the aircraft
        self.alt = alt                      # The current altitude (m)
        self.heading = (heading*-1)%360     # The current heading (deg)
        self.scale = scale                  # The world scale
        self.route = route                  # The route the aircraft is on
        self.path = []                      # Points of the traversed path of the aircraft
        self.updater = 0                    # How many times the aircraft has been updated
        self.point_constant = 18            # A constant value for adding points
        self.terminated = 0                 # How has the aircraft been terminated (0: exists, 1: safe, 2: out of bounds, 3: collision)

        # Visual constants
        self.size = min(2, int(5/self.scale))           # Size of the visual aircraft
        self.boarder_size = min(6, int(15/self.scale))  # Size for the visual boarder of the aircraft
        self.text_boost = min(16, int(25/self.scale))   # Where the text should start
    

    def step(self, bounds: (int,int)):
        """
        Simulates an aircraft step

        Parameters
        ----------
        bounds: (int,int)
            The bound of the world in meters (without scaling applied)
        """

        # Update the aircrafts position
        self.update_position()

        # Update the path drawing for the aircraft
        if (self.updater%self.point_constant)*self.scale == 0:
            self.path.append(self.position.get())
        self.updater += 1

    
    def update_position(self):
        """
        Update the aircraft's position using speed, heading and current position
        """
        hdg = (self.heading-180)%360    # Convert heading into sim heading

        hdg = pi/2 - radians(hdg)
        sim_speed = self.spd/self.scale # Change the speed to the simulated speed

        in_world, in_bounds = self.position.update(hdg, sim_speed)

        if not in_world or not in_bounds:
            self.terminated = 1
    
    def in_bounds(self, bounds: (int,int))-> (bool, bool):
        """
        Get if the aircraft is in all current bounds, the world and any corridors.
        Returns a tuple of if the aircraft is in the world and if the aircraft is in 
        it's corridor.

        Parameters
        ----------
        bounds: (int,int)
            The bound of the world in meters (without scaling applied)
        """

        return self.in_world(bounds), self.in_corridor()
    
    def in_world(self, bounds: (int,int)) -> bool:
        """
        Test that the aircraft is in the world, return if it exists in the world

        Parameters
        ----------
        bounds: (int,int)
            The bound of the world in meters (without scaling applied)
        """
        if 0 <= self.position.x <= bounds[0]:
            if 0 <= self.position.y <= bounds[1]:
                return True
        return False
    
    def in_corridor(self) -> bool():
        """
        Test that, if the aircraft should be in a corridor, it is in that corridor
        """
        if not self.route is None:
            return self.route.in_corridor(self.position)
        return True
    
    def draw(self, WINDOW):
        """
        Draws the aircraft to the window

        Parameters
        ----------
        WINDOW
            The output window to draw the aircraft to
        """
        # Draw the current path of the aircraft
        self.draw_path(WINDOW)

        # Draw the aircraft object
        d.circle(WINDOW, c.SAFE, self.position.get(), self.size)
        d.circle(WINDOW, c.SAFE, self.position.get(), self.boarder_size)

        # Draw its related stats
        text_arr, t_pos = self.get_text_stats()
        for i, t in enumerate(text_arr):
            x = t_pos[0]
            y = t_pos[1]-(12-i)

            WINDOW.blit(t, (x, y))


    def draw_path(self, WINDOW):
        """
        Draw the path of the aircraft to the window

        Parameters
        ----------
        WINDOW
            The window to output to
        """
        if len(self.points) > 1:
            pygame.draw.lines(WINDOW,c.LINE,False,self.path, width = 1)

    
    def get_text_stats(self)-> (string, (float,float)):
        """
        Get the text to output and its starting position
        """
        f = font.SysFont('couriernew', 15)
        text = []

        # Add heading
        t = f'{int((self.heading*-1)%360)}'
        text.append(font.render(t, True, c.WHITE))
        # Add Speed
        t = f'{self.tas}m/s'
        text.append(font.render(t, True, c.WHITE))
        # Add Altitude
        t = f'{self.alt}m'
        text.append(font.render(t, True, c.WHITE))

        return text,(self.x + self.text_boost,self.y-self.text_boost)

        
