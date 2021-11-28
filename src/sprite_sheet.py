import pygame


class SpriteSheet:

    """Spritesheet object to create sprites"""

    def __init__(self, sheet):

        self.sheet = sheet

    def get_sprite(
        self,
        x_pos: int,
        y_pos: int,
        width: int,
        height: int,
        frame: int,
        scale: float = 1,
    ) -> pygame.Surface:

        """Extract sprite

        Returns:
            pygame.Surface: image containing the sprite
        """

        # Create image featuring texture
        image = pygame.Surface((width, height))
        image.blit(self.sheet, (0, 0), ((width * frame + x_pos), y_pos, width, height))

        return image


class TileSetSheet(SpriteSheet):

    """Sprite sheet for the map tiles"""

    def __init__(self, sheet):
        super().__init__(sheet)

        self.boundary_sprite = self.get_sprite(0, 0, 50, 50, 0)

        self.buildable_sprite_1 = self.get_sprite(0, 50, 50, 50, 0)
        self.buildable_sprite_2 = self.get_sprite(0, 50, 50, 50, 1)


class BuildingSheet(SpriteSheet):

    """Sprite sheet for the buildings"""

    def __init__(self, sheet):
        super().__init__(sheet)

        self.space_elevator_sprite = self.get_sprite(0, 0, 50, 50, 0)
