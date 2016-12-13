import pygame


class TextBox:
    def __init__(self, font):
        self.font = font
        self.rect = pygame.Rect(10, 500, 680, 100)
        self.surface = None
        self._reset_surface()
        self.lines = []

    def say(self, text):
        print(text)
        self._reset_surface()
        self.lines.append(text)
        self.lines = self.lines[-4:]
        for i in range(len(self.lines)):
            t, r = self.font.render(self.lines[i])
            self.surface.blit(t, r.move(0, 10 + 16*i))

    def _reset_surface(self):
        self.surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA, 32)