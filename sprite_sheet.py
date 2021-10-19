import pygame

class SpriteSheet():

    def __init__(self, sheet):

        self.sheet = sheet
    

    def get_sprite(self, x_pos: int, y_pos: int,
                    width: int, height: int,
                    frame: int, scale: float = 1) -> pygame.Surface:
        
        image = pygame.Surface((width, height))
        image.blit(self.sheet, (0, 0),
                    ((width * frame + x_pos), y_pos, width, height))

        return image
