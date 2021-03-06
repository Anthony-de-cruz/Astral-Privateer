import random
import sys
import os

from game import GameObject, Game
from ui import MoneyCounterUI
from load_map_file import load_map_file
from sprite_sheet import TileSetSheet, BuildingSheet, EnemySheet
from buildings import Building, SpaceElevator, load_buildings
from enemies import Enemy
import pygame


class TestObject(GameObject):

    """Class for test object"""

    def __init__(self, x_pos: int, y_pos: int, width: int, height: int, *groups: tuple):
        super().__init__(x_pos, y_pos, width, height, *groups)

        self.image.fill((50, 50, 150))
        # self.image = pygame.transform.scale(self.image, ())


class Map(pygame.sprite.Sprite):

    """Class for the gridded map"""

    def __init__(
        self,
        x_pos: int,
        y_pos: int,
        tile_width: int,
        tile_height: int,
        TILE_SET: dict,
        map_data: dict,
        *groups: tuple,
    ):
        super().__init__(*groups)

        self.x_pos = x_pos
        self.y_pos = y_pos

        self.tile_width = tile_width
        self.tile_height = tile_height
        self.TILE_SET = TILE_SET

        self.map_data = map_data

        # Retrieve the dimentions of the map
        self.x_tiles = self.map_data["Dimentions"][0]
        self.y_tiles = self.map_data["Dimentions"][1]

        self.width = self.x_tiles * tile_width
        self.height = self.y_tiles * tile_height

        self.image, self.rect = self.render_map_image()

    # Currently requires the dimentions of the map to be hard coded,
    # needs a way to read the dimentions beforehand.
    def render_map_image(self) -> pygame.Surface and pygame.Rect:

        image = pygame.Surface((self.width, self.height))
        rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)

        for y in range(self.y_tiles):
            for x in range(self.x_tiles):

                # Create a new image for the tile and blit the texture onto it
                tile_image = pygame.Surface((self.tile_width, self.tile_height))
                tile_image.blit(self.TILE_SET[self.map_data[f"{x},{y}"][0]][0], (0, 0))

                # Blit this new image onto the main map surface
                image.blit(
                    tile_image,
                    (
                        x * self.tile_width,
                        y * self.tile_height,
                        self.tile_width,
                        self.tile_height,
                    ),
                )

        return image, rect

    def click(self, clicked: tuple, button: tuple) -> None:

        """Method for an action to be perfom when clicked"""

        # Converts clicked tuple into map coordinates
        clicked_x = (clicked[0] - self.rect.x) // self.tile_width
        clicked_y = (clicked[1] - self.rect.y) // self.tile_height

        print(clicked_x, ",", clicked_y, self.map_data[f"{clicked_x},{clicked_y}"])

        if button[0]:
            print("Left clicked")

    def update(self) -> None:

        """Method to execute when updating"""

        self.image, _ = self.render_map_image()


class AstralPrivateer(Game):

    """Main game class, handles mainloop, inputs, updating and drawing"""

    def __init__(
        self,
        window_name: str,
        window_width: int,
        window_height: int,
        COLOUR_PALETTE: dict,
        frame_rate: int,
    ):
        super().__init__(
            window_name, window_width, window_height, COLOUR_PALETTE, frame_rate
        )

        ## Create sprite groups
        self.cam_speed = 10
        self.cam_pan_group = pygame.sprite.Group()
        self.ui_group = pygame.sprite.Group()
        self.click_group = pygame.sprite.Group()
        self.map_group = pygame.sprite.Group()
        self.buildings_group = pygame.sprite.Group()
        self.spawner_group = pygame.sprite.Group()
        self.enemies_group = pygame.sprite.Group()
        self.time_group = pygame.sprite.Group()

        ## Load sprite sheets
        # Load sprite sheet for the map
        tile_set_sheet = TileSetSheet(
            pygame.image.load(os.path.join("assets", "tile_set", "tile_set_0.png"))
        )

        # Load sprite sheet for the buildings
        buildings_sheet = BuildingSheet(
            pygame.image.load(os.path.join("assets", "buildings", "buildings.png"))
        )

         # Load sprite sheet for the enemies
        enemy_sheet = EnemySheet(
            pygame.image.load(os.path.join("assets", "enemies", "enemies.png"))
        )


        ## Create game objects
        # Create tile set table
        # (Sprite, Able to build over?)
        self.TILE_SET = {
            "Boundary": (tile_set_sheet.boundary_sprite, False),
            "Buildable_0": (tile_set_sheet.buildable_sprite_1, True),
            "Buildable_1": (tile_set_sheet.buildable_sprite_2, True),
        }

        # Create UI element
        self.money_counter_ui = MoneyCounterUI(
            10, 10, 150, 50, "verdana", 36, self.COLOUR_PALETTE, self.ui_group
        )

        # Load in map file
        map_data = load_map_file(os.path.join("levels", "level_0.json"))

        # Load in all prexisting buildings on the map file
        map_data, groups = load_buildings(
            map_data, buildings_sheet,
            self.buildings_group, self.cam_pan_group, self.time_group
        )
        self.buildings_group = groups[0]
        self.cam_pan_group = groups[1]
        self.time_group = groups[2]

        # Create map object
        self.map = Map(
            0,
            0,
            50,
            50,
            self.TILE_SET,
            map_data,
            self.map_group,
            self.cam_pan_group,
            self.click_group,
        )

        self.enemy_1 = Enemy(10, 5, 50, 50, enemy_sheet,self.enemies_group, self.cam_pan_group)
        print(self.enemies_group)
        #print(self.enemy_1.navigate(self.map.map_data))


        # Record the time when the game starts
        self.start_time = pygame.time.get_ticks()

    def draw_object_groups(self) -> None:

        """Method to draw all object groups"""

        self.window.fill(self.COLOUR_PALETTE["Dark Grey"])

        self.map_group.draw(self.window)
        self.buildings_group.draw(self.window)
        self.enemies_group.draw(self.window)
        self.ui_group.draw(self.window)

    def update_object_groups(self) -> None:

        """Method to update all object groups"""

        self.map_group.update()
        self.buildings_group.update()
        self.enemies_group.update()
        self.ui_group.update()

    def handle_inputs(self) -> None:

        """Method to handle player input"""

        # Keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]:
            for sprite in self.cam_pan_group:
                sprite.rect.x += (keys[pygame.K_a] - keys[pygame.K_d]) * self.cam_speed
                sprite.rect.y += (keys[pygame.K_w] - keys[pygame.K_s]) * self.cam_speed

        # Mouse input
        if True in pygame.mouse.get_pressed():

            pos = pygame.mouse.get_pos()
            clicked_sprites = [s for s in self.click_group if s.rect.collidepoint(pos)]
            print("Clicked at", pos, "on", clicked_sprites)

            for sprite in clicked_sprites:
                if isinstance(sprite, Map):
                    sprite.click(pos, pygame.mouse.get_pressed())

    def main_loop(self) -> None:

        """Method containing the main loop"""

        while self.running:

            self.clock.tick(self.frame_rate)
            self.current_time = pygame.time.get_ticks() - self.start_time
            # Update each sprite in time_group
            #todo need to find a more efficient way of doing this
            for sprite in self.time_group: sprite.current_time = self.current_time

            self.handle_events()
            self.handle_inputs()

            self.update_object_groups()

            self.draw_object_groups()
            pygame.display.flip()


def main() -> None:

    COLOURS = {"Black": (0, 0, 0), "White": (255, 255, 255), "Dark Grey": (25, 25, 25)}

    pygame.init()

    game = AstralPrivateer("Astral Privateer", 1600, 900, COLOURS, 60)

    game.main_loop()


if __name__ == "__main__":

    main()
