import os
import sys
from typing import NoReturn

import pygame


class GameObject(pygame.sprite.Sprite):

    """Base game object that all objects will inherit from"""

    def __init__(self, x: int, y:int):
        super.__init__()

        self.x = x
        self.y = y
    
    def draw(self, window: pygame.display) -> None:

        """Method to specify what is drawn to the main window"""


class Game():

    """Main game class"""

    def __init__(self,
        window_name: str,
        window_width: int,
        window_height: int):

        self.window_name = window_name

        self.window_width = window_width
        self.window_height = window_height
        
        self.setup_window()
    
    def setup_window(self) -> None:

        """Method to setup game window"""

        self.window = pygame.display.set_mode(
            (self.window_width, self.window_height))
        pygame.display.set_caption((self.window_name))
        os.environ["SDL_VIDEO_CENTERED"] = "1"
