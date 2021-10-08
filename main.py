import random
from typing import NoReturn

from game import GameObject, Game
import pygame


class AstralPrivateer(Game):

    """Main game class"""

    def __init__(self,
        window_name: str,
        window_width: int,
        window_height: int
        ):
        super().__init__(
            window_name,
            window_width,
            window_height)
        

def main() -> None:

    pygame.init()

    game = AstralPrivateer("Astral Privateer", 800, 800)

if __name__ == "__main__":

    main()
