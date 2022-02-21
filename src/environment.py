#!/usr/bin/env python
"""Provides the Environment class for the simulation environment.

Environment is responsible for running the simulation at each step as well as checking
for terminal conditions and generation new aircraft. It usually runs disjointed from the
UI but when the UI is active is bound by the FPS of that UI.
"""

from time import sleep

import numpy as np

from aircraft import Aircraft

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
    objects: dict
        A dictionary containing all elements in the simulaton or that have existed
    running: bool
        If the simulation is currently running or terminated
    start_points: [point/waypoint]
            An array of starting points either as points or waypoints
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
    """
    def __init__(self, area:(int,int), visual:bool = False, fps:int =60, scale:float = 1, time_scale:float = 1, start_points: Point = [], min_spd: int = 20, max_spd: int = 20, min_alt: int = 100, max_alt: int = 100, ac_prefix:string = "AC"):
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

        """
        # Environment Parameters
        self.area = area                        # The simulation area/world size
        self.visual = visual                    # Is the UI present
        self.fps = fps                          # What fps does the simulation run at
        self.scale = scale                      # The world scale multiplier
        self.time_scale = time_scale            # How quickly should the simulation run

        # Aircraft Parameters (for generation)
        self.start_points = start_points        # All possible ac start positions
        self.min_spd = min_spd                  # Minimum aircraft speed
        self.max_spd = max_spd                  # Maximum aircraft speed
        self.min_alt = min_alt                  # Minimum aircraft altitude
        self.max_alt = max_alt                  # Maximum aircraft Altitude
        self.ac_prefix = ac_prefix              # Default string prefix

        # Objects
        self.objects = {                        # Dictionary of objects
            'aircraft':{},
            'waypoints':{},
            'corridors':{},
            'terminated':{}
        }

        # Simulation Parameters
        self.running = False                    # Is the simulation running
    
    def run(self, max_aircraft:int = 0, delay:[int] = [9,12,15]):
        """
        Running the simulation until some end condition is reached

        Parameters
        ----------
        max_aircraft: int
            The maximum number of aircraft to generate before the simulation terminates (0 for infinate)
        delay: [int]
            An array of possible time delays (seconds) between aircraft generation

        """
        aircraft = 0
        step = 0
        timer = 0
        next_ac = np.zeros(len(self.start_points))

        self.running = True

        while self.running:
            if max_aircraft > 0 and aircraft == max_aircraft:
                self.running = False
                continue
            
            # Generate the next AC if the timer is equal to the time of next aircraft generation
            for i, t in enumerate(next_ac):
                if timer == t:
                    self.generate_ac(i, f'{self.ac_prefix}{aircraft}')
                    next_ac[i] += np.random.choice(delay,1)[0]

            # Force a delay for UI operation so it doesn't run too quick
            if self.visual:
                sleep((1/self.fps)/self.time_scale)
            
            self.step()
            step = (step + 1)%self.fps

            if step == 0:
                timer += 1


    def step(self):
        """
        One step of the simulation where one step is the equivilent of 1 second * the time_scale.
        """

        # Step and update all the aircraft
        for ac in self.objects['aircraft'].keys():
            self.objects['aircraft'][ac].step()
        
        self.update_active()
    
    def update_active(self):
        """
        Update the list of active aircraft, moving terminated aircraft to the terminated list.
        """
        aircraft = self.objects['aircraft'].keys()

        for ac in aircraft:
            if self.objects['aircraft'][ac].terminated > 0:
                self.objects['terminated'][ac] = self.objects['aircraft'][ac]
                del self.self.objects['aircraft'][ac]


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
        pos = self.start_points[k]
        spd = np.random.randint(self.min_spd,self.max_spd+1)
        alt = np.random.randint(self.min_alt,self.max_alt+1)
        hdg = np.random.randint(0,360)

        ac = Aircraft(_id,pos,spd,alt,hdg, scale=self.scale)
        self.objects['aircraft'][_id] = ac
        