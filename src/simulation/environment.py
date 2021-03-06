#!/usr/bin/env python
"""Provides the Environment class for the simulation environment.

Environment is responsible for running the simulation at each step as well as checking
for terminal conditions and generation new aircraft. It usually runs disjointed from the
UI but when the UI is active is bound by the FPS of that UI.
"""

import string
from collections import OrderedDict
from time import sleep

import numpy as np
from src.geography.point import Point
from src.simulation.aircraft import Aircraft
from src.utility.filehandling import load_json
from src.utility.util import get_dist

__author__ = "Ellis Thompson"
__credits__ = ["Ellis Thompson"]

__license__ = "GNU GPLv3"
__maintainer__ = "Ellis Thompson"
__email__ = "thompson_e@gwu.edu"
__status__ = "Development"


class Environment():
    """
    Enrironment, where all methods for updating positions and the current environment state go.

    Attributes
    ----------
    area: (int,int)
        x & y size for the active area size (in meters)
    
    visual: bool
        If the UI is being displayed
    
    fps: int
        The default FPS for running the UI (only considered if the UI is running)
    
    scale: float
        The scale used to apply to distance measurements
    
    time_scale: float
        The scale used to apply to the speed of the environment
    
    min_spd: int
        The minimum speed of a generated aircraft m/s
    
    max_spd: int
        The maximum speed of a generated aircraft m/s
    
    min_alt: int
        The minimum altitude of a generated aircraft m
    
    max_alt: int
        The maximum altitude of a generated aircraft m
    
    ac_prefix: string
            The prefix to assign to aircraft
    
    objects: dict
        A dictionary containing all elements in the simulaton or that have existed
    
    old_paths: [[(int,int)]]
        An array of old paths
    
    running: bool
        If the simulation is currently running or terminated
    
    ran: bool
        Has the simulation run yet
    
    Methods
    -------
    run(max_aircraft = 0)
        The maximum number of aircraft to generate before the simulation terminates (0 for infinate)
    
    step
        A single step of the simulation
    
    update_active
        Update the list of active aircraft, moving terminated aircraft to the terminated list.
    
    generate_ac(k)
        Generate an aircraft at the point correspoiding to position k

    check_collisions(dist_matrix, min_sep = 25)
        Check the aircraft in the environment for any collisions and terminate where applicible 
    
    get_is_finished
        Returns if the simulation is active
    
    draw_objects(WINDOW, max_paths = 100)
        Draws all visible elements to the window
    
    draw_old_paths(WINDOW, max_paths = 100)
        Draw a limited number of older paths
    
    get_distance_matrix:
        Generate a distance matrix of aircraft active in the environment

    """
    def __init__(self, area:(int,int), visual:bool = True, fps:int =60, scale:float = 1, time_scale:float = 1, min_spd: int = 15, max_spd: int = 40, min_alt: int = 100, max_alt: int = 100, ac_prefix:string = "AC", delay:[int] = [5,7,11], env_path:string = None):
        """
        Parameters
        ----------
        area: (int,int)
            x & y size for the active area size (in meters)
        
        visual: bool
            If the UI is being displayed
        
        fps: int
            The default FPS for running the UI (only considered if the UI is running)
        
        scale: float
            The scale used to apply to distance measurements
        
        time_scale: float
            The scale used to apply to the speed of the environment
        
        start_points: [point/waypoint]
            An array of starting points either as points or waypoints (x,y)
        
        min_spd: int
            The minimum speed of a generated aircraft m/s
        
        max_spd: int
            The maximum speed of a generated aircraft m/s
        
        min_alt: int
            The minimum altitude of a generated aircraft m
        
        max_alt: int
            The maximum altitude of a generated aircraft m
        
        ac_prefix: string
            The prefix to assign to aircraft

        delay: [int]
            Time in seconds between ac generation
        
        env_path: string
            The file path to load an environment

        """
        # Environment Parameters
        self.area = area                        # The simulation area/world size
        self.visual = visual                    # Is the UI present
        self.fps = fps                          # What fps does the simulation run at
        self.scale = scale                      # The world scale multiplier
        self.time_scale = time_scale            # How quickly should the simulation run

        # Aircraft Parameters (for generation)
        self.delay = delay * scale              # Time in seconds between ac generation
        self.min_spd = min_spd                  # Minimum aircraft speed
        self.max_spd = max_spd                  # Maximum aircraft speed
        self.min_alt = min_alt                  # Minimum aircraft altitude
        self.max_alt = max_alt                  # Maximum aircraft Altitude
        self.ac_prefix = ac_prefix              # Default string prefix

        # Objects
        self.objects = {  
            'routes':OrderedDict(),
            'terminated':OrderedDict(),
            'aircraft':OrderedDict(),    
            'waypoints':OrderedDict()                  # Dictionary of objects
        }

        if not env_path is None:
            wpts, rts = load_json(env_path)

            self.objects['waypoints'] = wpts
            self.objects['routes'] = rts

        # Simulation Parameters
        self.running = False                    # Is the simulation running
        self.ran = False                        # Has the simulation been run yet

    def run(self, max_aircraft:int = 0):
        """
        Running the simulation until some end condition is reached

        Parameters
        ----------
        max_aircraft: int
            The maximum number of aircraft to generate before the simulation terminates (0 for infinate)
        """
        aircraft = 0
        step = 0
        timer = 0
        next_ac = np.random.choice(self.delay, len(self.objects['routes'].keys()))
        _len = size = np.random.randint(1, len(self.objects['routes'].keys())+1)
        next_ac[np.random.randint(len(self.objects['routes'].keys()),
        size = _len)] = 0

        self.ran = True
        self.running = True

        while self.running:
            if max_aircraft > 0 and aircraft == max_aircraft:
                self.running = False
                continue
            
            # Generate the next AC if the timer is equal to the time of next aircraft generation
            for i, t in enumerate(next_ac):
                if timer == t:
                    self.generate_ac(i, f'{self.ac_prefix}{aircraft}')
                    next_ac[i] += np.random.choice(self.delay,1)[0]
                    aircraft += 1

            # Force a delay for UI operation so it doesn't run too quick
            if self.visual:
                sleep((1/self.fps)/self.time_scale)
            
            self.step()
            step = (step + 1) % self.fps

            if step == 0:
                timer += 1


    def step(self):
        """
        One step of the simulation where one step is the equivilent of 1 second * the time_scale.
        """

        dist_matrix = self.get_distance_matrix()

        # Step and update all the aircraft
        for i, ac in enumerate(self.objects['aircraft'].keys()):
            self.objects['aircraft'][ac].step(self.area)
        
        self.check_collisions(dist_matrix)
        
        self.update_active()

    
    def update_active(self):
        """
        Update the list of active aircraft, moving terminated aircraft to the terminated list.
        """
        aircraft = self.objects['aircraft'].keys()

        new_active = OrderedDict()

        for ac in aircraft:
            if self.objects['aircraft'][ac].terminated > 0:
                self.objects['terminated'][ac] = self.objects['aircraft'][ac]
            else:
                new_active[ac] = self.objects['aircraft'][ac]
        self.objects['aircraft'] = new_active


    def generate_ac(self, k, _id):
        """
        Generate an aircraft at the point correspoiding to position k 

        Parameters
        ----------
        k: int
            The corresponding start position in the start position array
        
        _id: string
            The aircraft ID
        """
        key = list(self.objects['routes'].keys())[k]
        pos = self.objects['routes'][key].start
        spd = np.random.randint(self.min_spd,self.max_spd+1)
        alt = np.random.randint(self.min_alt,self.max_alt+1)
        hdg = self.objects['routes'][key].init_heading

        ac = Aircraft(_id,pos,spd,alt,hdg, scale=self.scale, route=self.objects['routes'][key].copy())
        self.objects['aircraft'][_id] = ac
    

    def check_collisions(self, dist_matrix: np.array, min_sep: float = 25):
        """
        Check the aircraft in the environment for any collisions and terminate where applicible 

        Parameters
        ----------
        dist_matrix: np.array
            The matrix of distances between aircraft
        
        min_sep: float
            The min separation between aircraft in meters
        """

        for i, key in enumerate(self.objects['aircraft']):
            if self.objects['aircraft'][key].terminated > 0:
                continue
            dist_array = dist_matrix[i,:]

            for j, j_key in enumerate(self.objects['aircraft']):
                if i == j or self.objects['aircraft'][j_key].terminated > 0:
                    continue

                if dist_array[j] < min_sep:
                    self.objects['aircraft'][key].terminated = 3
                    self.objects['aircraft'][j_key].terminated = 3


    def draw_objects(self, WINDOW,  max_paths = 100):
        """
        Draws all visible elements to the window

        Parameters
        ----------
        WINDOW
            The output window to draw to
        
        max_paths: int
            The maximum number of paths to draw
        """

        # Draw fixed old paths

        for key, item in self.objects.items():
            if key == 'terminated':
                self.draw_old_paths(WINDOW, max_paths)
                continue
            for k, __o in item.items():
                __o.draw(WINDOW)
                    
    
    def draw_old_paths(self, WINDOW, max_paths = 100):
        """
        Draw a limited number of older paths

        Parameters
        ----------
        WINDOW
            The window to draw to
        
        max_paths: int
            The maximum number of paths to draw
        """

        to_draw = np.array(list(self.objects['terminated'].items()))
        if len(to_draw) > max_paths:
            to_draw = to_draw[-max_paths:]
        for ac in to_draw:
            ac[1].draw_path(WINDOW)

    
    def get_is_finished(self) -> bool:
        """
        Returns if the simulation is active
        """
        if not self.ran:
            return False
        
        if self.ran and not self.running:
            return True
        
        return False
    
    def get_distance_matrix(self) -> np.array:
        """
        Generate a distance matrix of aircraft active in the environment
        """

        no_ac = len(self.objects['aircraft'].keys())
        matrix = np.zeros((no_ac, no_ac))

        for p_i, p_val in enumerate(self.objects['aircraft'].items()):
            for o_i, o_val in enumerate(self.objects['aircraft'].items()):
                if p_i == o_i:
                    continue
                
                dist = round(get_dist(p_val[1].position, o_val[1].position),3)

                matrix[p_i,o_i] = dist
        
        return matrix
