import random
import sys
import os
from typing import NoReturn

from game import GameObject, Game
from load_map_file import load_map_file
import pygame


class TestObject(GameObject):

    """Class for test object"""

    def __init__(self, x_pos:int, y_pos:int,
                width:int, height:int, *groups:tuple):
        super().__init__(x_pos, y_pos, width, height, *groups)

        self.image.fill((50,50,150))
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

        self.map_data = load_map_file(os.path.join("levels", "level_0.json"))
        print(self.map_data)

        self.image, self.rect = self.render_map_image()
    
    # Currently requires the dimentions of the map to be hard coded,
    # needs a way to read the dimentions beforehand.
    def render_map_image(self) -> pygame.Surface and pygame.Rect:

        image = pygame.Surface((self.width, self.height))
        rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)

        for x in range(self.x_tiles):
            for y in range(self.y_tiles):
 
                tile_image = pygame.Surface((self.tile_width, self.tile_height))


                tile_image.fill(self.TILE_SET[self.map_data[f"{x},{y}"][0]][0])

                image.blit(tile_image,
                            (x * self.tile_width, y * self.tile_height,
                            self.tile_width, self.tile_height))

        return image, rect
            




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
        self.cam_speed = 10
        
        self.cam_pan_group = pygame.sprite.Group()

        #self.test_object_group = pygame.sprite.Group()
        #self.test_object = TestObject(50, 69, 100, 100,
        #                                self.test_object_group, self.cam_pan_group)

        self.map_group = pygame.sprite.Group()
        self.map = Map(0, 0, 24, 24, 50, 50, TILE_SET, self.map_group, self.cam_pan_group)


    def draw_object_groups(self) -> None:

        """Method to draw all object groups"""

        self.window.fill(self.COLOUR_PALETTE["Black"])

        #self.test_object_group.draw(self.window)
        self.map_group.draw(self.window)


    def update_object_groups(self) -> None:

        """Method to update all object groups"""



    def handle_inputs(self) -> None:

        """Method to handle player input"""

        keys = pygame.key.get_pressed()

        for sprite in self.cam_pan_group:
            sprite.rect.x += (keys[pygame.K_a] - keys[pygame.K_d]) * self.cam_speed
            sprite.rect.y += (keys[pygame.K_w] - keys[pygame.K_s]) * self.cam_speed

    def main_loop(self) -> None:

        """Method containing the main loop"""

        while self.running:
            
            self.clock.tick(self.frame_rate)
            self.handle_events()
            self.handle_inputs()

            self.update_object_groups()

            self.draw_object_groups()
            pygame.display.flip()


def main() -> None:

    COLOURS = {
        "Black": (0, 0, 0),
        "White": (255, 255, 255)
    }

    #(Tile image path, Can be built over?)
    #"Boundry": (os.path.join("assets", "tile_set", "boundry.png"), False),

    #(colour, Can be built over?)
    TILE_SET = {
        "Boundry": ((40, 40, 40), False),
        "Buildable": ((80, 80, 80), True)
    }

    pygame.init()

    game = AstralPrivateer("Astral Privateer", 800, 800,
                            COLOURS, 60, TILE_SET)

    game.main_loop()

if __name__ == "__main__":

    main()
