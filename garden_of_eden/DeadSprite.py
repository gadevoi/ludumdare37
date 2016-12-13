import pygame


class DeadSprite(pygame.sprite.Sprite):
    def __init__(self, dead_icon, plant):
        super().__init__()

        self.image = dead_icon
        self.rect = (plant.x-10, plant.y+10, 20, 20)
        self.plant = plant

    def update(self):
        if not self.plant.is_alive() and len(self.plant.tree) > 0:
            self.rect = (self.plant.x-10, self.plant.y+10, 20, 20)
        else:
            self.rect = (-100, -100, 20, 20)

import pygame


class RadSprite(pygame.sprite.Sprite):
    def __init__(self, dead_icon, plant):
        super().__init__()

        self.image = dead_icon
        self.rect = (plant.x-30, plant.y+10, 20, 20)
        self.plant = plant

    def update(self):
        if self.plant.is_alive() and len(self.plant.tree) > 0 and self.plant.y < 200:
            self.rect = (self.plant.x-30, self.plant.y+10, 20, 20)
        else:
            self.rect = (-100, -100, 20, 20)