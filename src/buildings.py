from typing import Tuple

from game import GameObject
import pygame
import jsonpickle


def load_buildings(map_data: dict) -> Tuple[dict, pygame.sprite.Group]:

    """Retrieves the buildings stored in a map data structure.\n
    Requires a buildings tuple containing each building so it can be iterated over

    Returns:
        dict: adjusted map data containing decoded buildings
        pygame.sprite.Group: contains all of the building objects
    """

    buildings_group = pygame.sprite.Group()

    # Iterate over X and Y
    for x in range(map_data["Dimentions"][0]):
        for y in range(map_data["Dimentions"][1]):

            # If there is a building
            if map_data[f"{x},{y}"][1] != None:

                # Decode the pickled building, add it to the buildings group
                building = jsonpickle.decode(map_data[f"{x},{y}"][1])
                building.add(buildings_group)
                # Place the decoded building back into the map data
                map_data[f"{x},{y}"][1] = building

    return map_data, buildings_group


class Building(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, *groups: tuple):
        super().__init__(*groups)
        self.x_coord = x
        self.y_coord = y


class SpaceElevator(Building):
    def __init__(self, x: int, y: int, *groups: tuple):
        super().__init__(x, y, *groups)

        pass
