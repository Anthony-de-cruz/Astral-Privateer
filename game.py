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
        window_height: int,
        COLOUR_PALETTE: dict,
        frame_rate: int):

        self.COLOUR_PALETTE = COLOUR_PALETTE
        self.clock = pygame.time.Clock()
        self.frame_rate = frame_rate
        self.window_name = window_name

        self.window_width = window_width
        self.window_height = window_height

        self.objects: list[GameObject] = []
        
        self.setup_window()

        self.running = True
    
    def setup_window(self) -> None:

        """Method to setup game window"""

        self.window = pygame.display.set_mode(
            (self.window_width, self.window_height))
        pygame.display.set_caption((self.window_name))
        os.environ["SDL_VIDEO_CENTERED"] = "1"

    def add_object(self, game_object: GameObject) -> None:

        """Method to add a game object into the game object list"""

        self.objects.append(game_object)
    
    def draw_objects(self) -> None:

        """Method to draw all objects"""

        for obj in self.objects:
            obj.draw(self.window, self.COLOUR_PALETTE)

    def handle_events(self) -> None:

        """Method to handle pygame events"""

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    def main_loop(self) -> None:

        """Method containing the main loop"""

        while self.running:

            self.clock.tick(self.frame_rate)
            self.handle_events()

            self.draw_objects()
            pygame.display.flip()

