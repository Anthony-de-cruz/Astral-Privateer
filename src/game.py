import os
import sys

import pygame


class GameObject(pygame.sprite.Sprite):

    """Base game object that all objects will inherit from"""

    def __init__(self, x_pos: int, y_pos: int, 
                width: int, height: int, transparent: bool = True, *groups: tuple):
        super().__init__(*groups)

        self.x_pos = x_pos
        self.y_pos = y_pos

        self.width = width
        self.height = height

        self.transparent = transparent
        if not self.transparent:
            self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        else:
            self.image = pygame.Surface((self.width, self.height))

        self.rect = pygame.Rect(self.x_pos, self.y_pos,
                                self.width, self.height)


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

        self.setup_window()

        self.running = True
    
    def setup_window(self) -> None:

        """Method to setup game window"""

        self.window = pygame.display.set_mode(
            (self.window_width, self.window_height))
        pygame.display.set_caption((self.window_name))
        os.environ["SDL_VIDEO_CENTERED"] = "1"

    def handle_events(self) -> None:

        """Method to handle pygame events"""

        self.event_list = pygame.event.get()
        for event in self.event_list:

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    def main_loop(self) -> None:

        """Method containing the main loop"""

        while self.running:

            self.clock.tick(self.frame_rate)
            self.handle_events()

            self.draw_object_groups()
            pygame.display.flip()

