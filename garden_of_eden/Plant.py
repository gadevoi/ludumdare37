import random
import pygame
import math


class Plant:
    def __init__(self):
        self.tree = "S"
        self.rules = [("S", "S[+S]S[-S]S", .33),  # stem evolution
                      ("S", "S[+S]S", .33),
                      ("S", "S[-S]S", .55),  # stem to leaf
                      ("S", "L", .33),  # stem to flower
                      ("F", "", .10),
                      ("L", "", .10)]  # flower fades  away
        self.alphabet = ["S"]
        self.d = 10
        self.δ = math.pi/9
        print(self.δ)
        self.image = pygame.Surface((800, 600))

    def grow(self):
        self.tree = ''.join([self._apply_rule(c) for c in self.tree])

    def _apply_rule(self, c):
        # rule a -> b with probability proba
        for a, b, proba in self.rules:
            if a == c and random.random() < proba:
                return b
        # if no rule was applied, return the original char.
        return c

    def draw(self):
        self.image = pygame.Surface((800, 600), pygame.SRCALPHA, 32)
        stack = []
        x = self.image.get_width() / 2
        y = self.image.get_height()
        pos = (x, y)
        head = -math.pi/2
        for c in self.tree:
            if c == "S":
                new_pos = (pos[0] + math.cos(head)*self.d, pos[1] + math.sin(head)*self.d)
                pygame.draw.line(self.image, (0, 140, 0), pos, new_pos)
                pos = new_pos
            elif c == "L":
                pygame.draw.circle(self.image, (0, 255, 140),
                                   (int(pos[0]), int(pos[1])), 10)
            elif c == "-":
                head -= self.δ
            elif c == "+":
                head += self.δ
            elif c == "[":
                stack.append((pos, head))
            elif c == "]":
                pos, head = stack.pop()


