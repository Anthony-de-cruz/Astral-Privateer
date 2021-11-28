from typing import Tuple

from game import GameObject
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
        self, x_coord: int, y_coord: int, width: int, height: int, *groups: tuple
    ):
        super().__init__(*groups)

        self.x_coord = x_coord
        self.y_coord = y_coord

        self.x_pos = self.x_coord * width
        self.y_pos = self.y_coord * height

        self.width = width
        self.height = height

        self.create_rect()

    def create_rect(self):
        self.image = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)

    def render(self, buildings_sheet):
        pass


class SpaceElevator(Building):
    def __init__(
        self, x_coord: int, y_coord: int, width: int, height: int, *groups: tuple
    ):
        super().__init__(x_coord, y_coord, width, height, *groups)

    def render(self, buildings_sheet):

        self.image.blit(buildings_sheet.space_elevator_sprite, (0, 0))
