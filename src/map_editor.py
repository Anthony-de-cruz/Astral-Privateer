import os
import json
import random

from game import Game, GameObject
from sprite_sheet import SpriteSheet
from buildings import Building, load_buildings, SpaceElevator
import pygame
import jsonpickle


def generate_map(x_tiles: int, y_tiles: int, x_core: int, y_core: int) -> dict:

    """Function to create a map data structure"""

    grid = {}
    grid["Dimentions"] = [x_tiles, y_tiles]
    for y in range(y_tiles):
        for x in range(x_tiles):

            grid[f"{x},{y}"] = [f"Buildable_{random.randint(0,1)}", None]
    
    # Create and pickle
    core = SpaceElevator(x_core, y_core)
    core_pickle = jsonpickle.encode(core)
    grid[f"{core.x_coord},{core.y_coord}"][1] = core_pickle
    
    return grid


def save_map(map_data, name) -> None:
    
    """Function to create/save a map file"""

    with open(os.path.join("levels", f"{name}"), "w") as map_file:
        json.dump(map_data, map_file)


def load_map_file(file_path: str) -> dict:

    """Function to load a map file"""
    
    with open(file_path, "r") as map_file:
        map_data = json.load(map_file)


    return map_data


def generate_map_input():

    """Function for the inputs to create a map file"""

    while True:

        x_tiles = int(input("x_tiles: "))
        y_tiles = int(input("y_tiles: "))
        x_core = int(input("x_core: "))
        y_core = int(input("y_core: "))
        name = input("name: ") + ".json"

        try:
            map_data = generate_map(x_tiles, y_tiles, x_core, y_core)
            save_map(map_data, name)

        #todo Make this actually handle something
        except:
            print("Something went wrong")

        else:
            print(f"{name} created successfully")
            input()
            break


def edit_map_input():

    """Function for the inputs to edit a map file"""

    print("Map files:")
    for thingy in os.listdir("levels"):
        print(" ", thingy)

    map_name = input("Name of map: ") + ".json"

    COLOURS = {
        "Black": (0, 0, 0),
        "White": (255, 255, 255),
        "Dark Grey": (25, 25, 25)
    }

    pygame.init()

    game = AstralPrivateer("Astral Privateer", 1600, 900,
                            COLOURS, 60, map_name)

    map_data = game.main_loop()

    save_choice = input("Do you want to save your map?(Y/N)")
    if save_choice.capitalize() == "Y":
        save_map(map_data, map_name)
    else:
        print("The map will not be saved")


class Map(pygame.sprite.Sprite):

    """Class for the gridded map"""

    def __init__(self, x_pos: int, y_pos: int,
                tile_width: int, tile_height: int, TILE_SET: dict,
                name: str,
                *groups: tuple):
        super().__init__(*groups)

        self.x_pos = x_pos
        self.y_pos = y_pos

        self.tile_width = tile_width
        self.tile_height = tile_height
        self.TILE_SET = TILE_SET

        self.map_data = load_map_file(os.path.join("levels", f"{name}"))
        #//print(self.map_data)

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
                tile_image.blit(self.TILE_SET[self.map_data[f"{x},{y}"][0]][0], (0,0))

                # Blit this new image onto the main map surface      
                image.blit(tile_image,
                            (x * self.tile_width, y * self.tile_height,
                            self.tile_width, self.tile_height))

        return image, rect


    def click(self, clicked: tuple, button: tuple) -> None:

        """Method for an action to be perfom when clicked"""

        # Converts clicked tuple into map coordinates
        clicked_x = (clicked[0] - self.rect.x) // self.tile_width
        clicked_y = (clicked[1] - self.rect.y) // self.tile_height

        print(clicked_x, ",", clicked_y, self.map_data[f"{clicked_x},{clicked_y}"])

        # Left click
        if button[0]:
            self.map_data[f"{clicked_x},{clicked_y}"] = (
                ["Boundary", self.map_data[f"{clicked_x},{clicked_y}"][1]])
        
        # Right Click
        elif button[2]:
            self.map_data[f"{clicked_x},{clicked_y}"] = (
                [f"Buildable_{random.randint(0, 1)}", self.map_data[f"{clicked_x},{clicked_y}"][1]])


    def update(self) -> None:

        """Method to execute when updating"""

        self.image, _ = self.render_map_image()


class TileSetSheet(SpriteSheet):

    """Sprite sheet for the map tiles"""

    def __init__(self, sheet):
        super().__init__(sheet)

        self.boundary_sprite = self.get_sprite(0, 0, 50, 50, 0)

        self.buildable_sprite_1 = self.get_sprite(0, 50, 50, 50, 0)
        self.buildable_sprite_2 = self.get_sprite(0, 50, 50, 50, 1)


class AstralPrivateer(Game):

    """Main game class"""

    def __init__(self,
        window_name: str,
        window_width: int,
        window_height: int,
        COLOUR_PALETTE: dict,
        frame_rate: int,
        map_name: str
        ):
        super().__init__(
            window_name,
            window_width,
            window_height,
            COLOUR_PALETTE,
            frame_rate)

        ## Create sprite groups
        self.cam_speed = 10
        self.cam_pan_group = pygame.sprite.Group()
        
        self.ui_group = pygame.sprite.Group()

        self.click_group = pygame.sprite.Group()

        self.map_group = pygame.sprite.Group()

        ## Load sprite sheets
        # Load sprite sheet for the map
        tile_set_sheet = TileSetSheet(pygame.image.load(
                                    os.path.join("assets",
                                                "tile_set",
                                                "tile_set_0.png")
                                                        )
                                    )
        
        ## Create game objects
        # Create tile set table
        # (Sprite, Able to build over?)
        self.TILE_SET = {
                        "Boundary": (tile_set_sheet.boundary_sprite, False),
                        "Buildable_0": (tile_set_sheet.buildable_sprite_1, True),
                        "Buildable_1": (tile_set_sheet.buildable_sprite_2, True)
                        }

        # Create map object
        self.map = Map(0, 0, 50, 50, self.TILE_SET,
                        map_name,
                        self.map_group, self.cam_pan_group, self.click_group)


    def draw_object_groups(self) -> None:

        """Method to draw all object groups"""

        self.window.fill(self.COLOUR_PALETTE["Dark Grey"])

        self.map_group.draw(self.window)
        self.ui_group.draw(self.window)


    def update_object_groups(self) -> None:

        """Method to update all object groups"""

        self.map_group.update()

        self.ui_group.update()


    def handle_inputs(self) -> None:

        """Method to handle player input"""

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]:
            for sprite in self.cam_pan_group:
                sprite.rect.x += (keys[pygame.K_a] - keys[pygame.K_d]) * self.cam_speed
                sprite.rect.y += (keys[pygame.K_w] - keys[pygame.K_s]) * self.cam_speed
        
        for event in self.event_list:
            
            # pygame.mouse.get_pressed returns a tuple in the form
            # (leftclick, middleclick, rightclick)
            # Each is a boolean
            if True in pygame.mouse.get_pressed():
                    
                pos = pygame.mouse.get_pos()
                clicked_sprites = [s for s in self.click_group
                                        if s.rect.collidepoint(pos)]
                print("clicked at", pos, "on", clicked_sprites)

                for sprite in clicked_sprites:
                    if isinstance(sprite, Map):
                        sprite.click(pos, pygame.mouse.get_pressed())
    
    # This serves the overwrite that which is given in game.py
    # so that the script doesn't terminate once the game ends
    def handle_events(self):

        self.event_list = pygame.event.get()
        for event in self.event_list:

            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                break


    def main_loop(self) -> None:

        """Method containing the main loop"""

        while self.running:
            
            self.clock.tick(self.frame_rate)
            self.handle_events()
            if not self.running:
                continue
            self.handle_inputs()

            self.update_object_groups()

            self.draw_object_groups()
            pygame.display.flip()
        
        return self.map.map_data


def main() -> None:
    
    while True:
        
        print("""- Astral Privateer map editor -
        
        1: Create new map
        2: Edit map
        3: Exit
        """)

        menu_input = input("Enter your choice: ")

        # Create new map
        if menu_input == "1":

            generate_map_input()
            
        # Edit map
        elif menu_input == "2":

            edit_map_input()
        
        # Exit
        elif menu_input == "3":
            quit()
        
        # Invalid input
        else:
            print("Invalid input")


if __name__ == "__main__":

    main()
