import pygame


class Seed(pygame.sprite.Sprite):
    def __init__(self, dna):
        self.image = pygame.Surface(20, 20)
        self.rect = self.image.get_rect()
        self.dna = dna