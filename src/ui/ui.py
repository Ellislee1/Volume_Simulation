#!/usr/bin/env python
"""Provides the base class for the graphical user interface.

Defines the window and controls each frame output to it
"""

import pygame
import src.assets.colours as c
from pygame import display, time
from pygame import init as py_init
from pygame.locals import *

__author__ = "Ellis Thompson"
__credits__ = ["Ellis Thompson"]

__license__ = "GNU GPLv3"
__maintainer__ = "Ellis Thompson"
__email__ = "thompson_e@gwu.edu"
__status__ = "Development"


class Window:
    """
    The UI window for visual display and demonstration of the simulation.

    Attributes
    ----------
    env: Environment
        The environment to which is linked to the world
    
    WINDOW: pygame.display
        The output window of the UI
    
    fps: int
        The fps of the window
    
    fpsClock: pygame.time.Clock
        The simulated FPS clock

    Methods
    -------
    run
        Run loop for the UI
    
    step
        Each step of the simulaton
    
    end
        End the simulation
    """

    def __init__(self, env, size: (int, int) = (800,800), fps:int = 60):
        """
        Parameters
        ----------
        env: Environment
            The environment that the simulation runs in
        
        size: (int, int)
            The width and height of the environment
        
        fps: int
            The fps of the window
        """
        py_init()
        display.set_caption("RADAR: Simulation")

        self.env = env
        self.WINDOW = display.set_mode(size)
        self.fps = fps
        self.fpsClock = time.Clock()
    
    def run(self) -> bool:
        """
        Run loop for the UI
        """
        run = True

        while run:
            run = self.step()
        
        return False
    
    def step(self) -> bool:
        """
        Each step of the simulation is carried out here
        """

        # Check for exit states
        if self.env.get_is_finished():
            return False

        for event in pygame.event.get() :
            if event.type == QUIT :
                return self.end()

        
        # Render elements of the game
        self.WINDOW.fill(c.BACKGROUND)

        # Draw objects to the frame
        self.env.draw_objects(self.WINDOW)

        # Update frame
        pygame.display.update()
        self.fpsClock.tick(self.fps)

        return True
    
    def end(self):
        """
        End the simulation
        """
        pygame.quit()
        return False
