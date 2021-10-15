import random
from typing import NoReturn

from game import GameObject, Game
import pygame

class TestObject(GameObject):

    """Class for test object"""

    def __init__(self, x_pos:int, y_pos:int,
                width:int, height:int, *groups:tuple):
        super().__init__(x_pos, y_pos, width, height, *groups)



class Map(GameObject):

    """Class for the gridded map"""

    def __init__(self, x_pos: int, y_pos: int,
                width: int, height: int, TILE_SET: dict):
        super().__init__(x_pos, y_pos, width, height)

        print(self.rect)

        self.grid = {}
        for x in range(20):
            for y in range(20):
                # [TILE, Building]
                self.grid[f"{x},{y}"] = [TILE_SET["Buildable"], None]

        print(self.grid)


class AstralPrivateer(Game):

    """Main game class"""

    def __init__(self,
        window_name: str,
        window_width: int,
        window_height: int,
        COLOUR_PALETTE: dict,
        frame_rate: int,
        TILE_SET: dict
        ):
        super().__init__(
            window_name,
            window_width,
            window_height,
            COLOUR_PALETTE,
            frame_rate)
        
        self.TILE_SET = TILE_SET

        
        self.test_object_group = pygame.sprite.Group()
        self.test_object = TestObject(50, 50, 100, 100,
                                        self.test_object_group)

        self.test_object_group.draw(self.window)
        

    def draw_object_groups(self) -> None:

        """Method to draw all object groups"""

        self.window.fill(self.COLOUR_PALETTE["Black"])



    def update_object_groups(self) -> None:

        """Method to update all object groups"""



    def main_loop(self) -> None:

        """Method containing the main loop"""

        while self.running:
            
            self.clock.tick(self.frame_rate)
            self.handle_events()

            self.update_object_groups()

            self.draw_object_groups()
            pygame.display.flip()


def main() -> None:

    COLOURS = {
        "Black": (0, 0, 0),
        "White": (255, 255, 255)
    }

    #(can be built over?)
    TILE_SET = {
        "Boundry": (False),
        "Buildable": (True)
    }

    pygame.init()

    game = AstralPrivateer("Astral Privateer", 800, 800,
                            COLOURS, 60, TILE_SET)

    game.main_loop()

if __name__ == "__main__":

    main()
