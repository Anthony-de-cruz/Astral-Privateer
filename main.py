import random
from typing import NoReturn

from game import GameObject, Game
import pygame


class TestObject(GameObject):

    """Class for test object"""

    def __init__(self, x_pos:int, y_pos:int,
                width:int, height:int, *groups:tuple):
        super().__init__(x_pos, y_pos, width, height, *groups)

        self.image.fill((50,50,50))
        #self.image = pygame.transform.scale(self.image, ())



class Map(pygame.sprite.Sprite):

    """Class for the gridded map"""

    def __init__(self, x_pos: int, y_pos: int,
                x_tiles: int, y_tiles: int,
                tile_width:int, tile_height:int, TILE_SET: dict,
                *groups:tuple):
        super().__init__(*groups)

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_tiles = x_tiles
        self.y_tiles = y_tiles

        self.tile_width = tile_width
        self.tile_height = tile_height
        self.TILE_SET = TILE_SET

        self.width = self.x_tiles * tile_width
        self.height = self.y_tiles * tile_height

        self.image = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x_pos, self.y_pos,
                                self.width, self.height)

        self.grid = {}
        for x in range(x_tiles):
            for y in range(y_tiles):
                # [TILE, Building object]
                self.grid[f"{x},{y}"] = ["Buildable",
                                        None]
                tile_image = pygame.Surface((self.tile_width, self.tile_height))
                tile_image.fill((random.randint(50, 255),50,50))


                self.image.blit(tile_image, (x * tile_width, y * tile_height, tile_width, tile_height))

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

        
        #self.test_object_group = pygame.sprite.Group()
        #self.test_object = TestObject(50, 50, 100, 100,
        #                                self.test_object_group)

        self.map_group = pygame.sprite.Group()
        self.map = Map(0, 0, 20, 20, 50, 50, TILE_SET, self.map_group)


    def draw_object_groups(self) -> None:

        """Method to draw all object groups"""

        self.window.fill(self.COLOUR_PALETTE["Black"])

        #self.test_object_group.draw(self.window)

        self.map_group.draw(self.window)



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
