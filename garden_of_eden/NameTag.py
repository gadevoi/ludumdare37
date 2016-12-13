import pygame


class NameTag(pygame.sprite.Sprite):
    def __init__(self, plant, font):
        super().__init__()

        self.image, self.rect = font.render(plant.name, fgcolor=(255, 255, 255), bgcolor=(0, 0, 0))
        self.rect = self.rect.move(plant.x+6, plant.y)