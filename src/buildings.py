from typing import Tuple

from game import GameObject
from enemies import Enemy
import pygame
import jsonpickle

from sprite_sheet import BuildingSheet


def load_buildings(
    map_data: dict, buildings_sheet: BuildingSheet, *groups
) -> Tuple[dict, tuple]:

    """Retrieves the buildings stored in a map data structure.\n
    Requires a buildings tuple containing each building so it can be iterated over

    Returns:
        dict: adjusted map data containing decoded buildings
        tuple: contains pygame.sprite.Groups that contains all of the building objects
    """

    # Iterate over X and Y
    for x in range(map_data["Dimentions"][0]):
        for y in range(map_data["Dimentions"][1]):

            # If there is a building
            if map_data[f"{x},{y}"][1] != None:

                # Decode the pickled building, add it to the buildings group
                building = jsonpickle.decode(map_data[f"{x},{y}"][1])
                building.create_rect()
                building.render(buildings_sheet)
                # Iterate over groups, adding buildings to each one
                for group in groups:
                    building.add(group)
                # Place the decoded building back into the map data
                map_data[f"{x},{y}"][1] = building

    return map_data, groups


class Building(pygame.sprite.Sprite):
    def __init__(
        self, x_coord: int, y_coord: int, tile_width: int, tile_height: int, *groups: tuple
    ):
        super().__init__(*groups)

        self.x_coord = x_coord
        self.y_coord = y_coord

        self.x_pos = self.x_coord * tile_width
        self.y_pos = self.y_coord * tile_height

        self.width = tile_width
        self.height = tile_height

        self.create_rect()

    def create_rect(self) -> None:
        self.image = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)

    def render(self, buildings_sheet):
        pass


class SpaceElevator(Building):
    def __init__(
        self, x_coord: int, y_coord: int, tile_width: int, tile_height: int, *groups: tuple
    ):
        super().__init__(x_coord, y_coord, tile_width, tile_height, *groups)

    def render(self, buildings_sheet) -> None:

        self.image.blit(buildings_sheet.space_elevator_sprite, (0, 0))


class EnemySpawner(Building):
    def __init__(
        self, x_coord: int, y_coord: int, tile_width: int, tile_height: int, *groups: tuple
    ):
        super().__init__(x_coord, y_coord, tile_width, tile_height, *groups)

        self.timer = 0
        self.timer_difference = 0
    
    def render(self, buildings_sheet) -> None:

        self.image.blit(buildings_sheet.enemy_spawner_sprite, (0, 0))

    def update(self) -> None:

        # Timer to go off every 1 second
        self.timer = self.current_time - self.timer_difference
        if self.timer > 1000:
            #print("BRUH")
            self.timer_difference = self.current_time
            self.timer = 0

    def spawn(self):

        enemy = Enemy(self.x_coord, self.y_coord, 50, 50, )
