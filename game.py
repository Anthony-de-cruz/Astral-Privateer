import os
import sys
from typing import NoReturn

import pygame



class GameObject(pygame.sprite.Sprite):

    def __init__(self, x: int, y:int):
        super.__init__()

        self.x = x
        self.y = y
    
    def draw(self):

        """Method to specify what is drawn to the main window"""