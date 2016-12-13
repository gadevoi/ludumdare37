import pygame


class ButtonSprite(pygame.sprite.Sprite):
    def __init__(self, text, font, x, y):
        super().__init__()

        self.image, self.rect = font.render(text)
        self.rect = self.rect.move(x, y)