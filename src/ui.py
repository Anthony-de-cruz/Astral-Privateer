from game import GameObject
import pygame


class MoneyCounterUI(GameObject):

    """Class for the money counter object"""

    def __init__(
        self,
        x_pos: int,
        y_pos: int,
        width: int,
        height: int,
        font: str,
        font_size: int,
        COLOUR_PALETTE: dict,
        *groups: tuple,
    ):
        super().__init__(x_pos, y_pos, width, height, False, *groups)

        self.COLOUR_PALETTE = COLOUR_PALETTE
        self.font = font
        self.font_size = font_size
        self.ui_font = pygame.font.SysFont(self.font, self.font_size)

        self.money = str(0)

    def update(self) -> None:

        ui_text = self.ui_font.render(
            str(self.money), True, (self.COLOUR_PALETTE["White"])
        )

        # This fill exists to wipe the image before reblitting every frame
        # this allows for the image to refreshed
        self.image.fill((0, 0, 0, 0))
        self.image.blit(ui_text, (0, 0))
