import random
from typing import NoReturn

from game import GameObject, Game
import pygame


class AstralPrivateer(Game):

    """Main game class"""

    def __init__(self,
        window_name: str,
        window_width: int,
        window_height: int,
        COLOUR_PALETTE: dict,
        frame_rate: int
        ):
        super().__init__(
            window_name,
            window_width,
            window_height,
            COLOUR_PALETTE,
            frame_rate)

    def draw_objects(self) -> None:

        """Method to draw all objects"""

        self.window.fill(self.COLOUR_PALETTE["Black"])

        for obj in self.objects:
            obj.draw(self.window, self.COLOUR_PALETTE)
        

def main() -> None:

    COLOURS = {
        "Black": (0, 0, 0),
        "White": (255, 255, 255)
    }

    pygame.init()

    game = AstralPrivateer("Astral Privateer", 800, 800, COLOURS, 60)

    game.main_loop()

if __name__ == "__main__":

    main()
