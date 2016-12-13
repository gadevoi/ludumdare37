import random
import pygame
from math import cos, sin, pi, isnan
import numpy as np


class Plant(pygame.sprite.DirtySprite):
    def __init__(self, x, y, dna, width=800, height=600):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = pygame.Rect(x-10, y-20, 20, 60)

        self.dna = dna.copy()
        self.tree = dna.basis
        self.energy = 10000
        self.tree = dna.basis
        self.surface = 0
        self.size = 0
        self.lines = []
        self.polys = []
        self.fruit = []
        self.i = 0
        self.α = 0.0
        self.name = dna.name

        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def update(self):
        self.grow()
        self.build()
        self.tick()
        self.draw()

    def tick(self):
        self.energy += (self.surface*1.5 - self.size - len(self.tree)/3) / 2

    def grow(self):
        # self.tree = ''.join([self._apply_rule(c) for c in self.tree])
        if self.is_alive():
            if self.i >= len(self.tree):
                self.i = 0
            i = self.i
            newdna = self._apply_rule(self.tree[i])
            self.tree = self.tree[:i] + newdna + self.tree[i+1:]
            self.i += len(newdna)
        else:
            self.tree = self.tree[:-1]

    def build(self):
        self.lines = []
        self.polys = []
        self.fruit = []
        self.surface = 0
        self.size = 0

        stack = []
        poly = []

        w = 5
        color = [0, 100, 0]

        pos = np.array([0, 0, 0])
        head = np.array([[0, 0, -1],  # heading
                         [-1, 0, 0],  # left
                         [0, -1, 0]   # up
                         ])

        RU = lambda α :  np.transpose(
            np.array([[cos(α),  sin(α),    0],
                      [-sin(α),  cos(α),    0],
                      [0,        0,         1]]))
        RL = lambda α : np.transpose(
            np.array([[cos(α),   0,  -sin(α)],
                      [0,         1,  0],
                      [sin(α),    0,  cos(α)]]))
        RH = lambda α : np.transpose(
            np.array([[1, 0,        0],
                      [0, cos(α),    -sin(α)],
                      [0, sin(α),    cos(α)]]))

        RHδ = RH(self.dna.δ)
        RHmδ = RH(-self.dna.δ)
        RUδ = RU(self.dna.δ)
        RUmδ = RU(-self.dna.δ)
        RLδ = RL(self.dna.δ)
        RLmδ = RL(-self.dna.δ)


        #unit normal vector of plane defined by points a, b, and c
        def unit_normal(a, b, c):
            x = np.linalg.det([[1,a[1],a[2]],
                 [1,b[1],b[2]],
                 [1,c[1],c[2]]])
            y = np.linalg.det([[a[0],1,a[2]],
                 [b[0],1,b[2]],
                 [c[0],1,c[2]]])
            z = np.linalg.det([[a[0],a[1],1],
                 [b[0],b[1],1],
                 [c[0],c[1],1]])
            magnitude = (x**2 + y**2 + z**2)**.5
            return (x/magnitude, y/magnitude, z/magnitude)

        #area of polygon poly
        def poly_area(poly):
            if len(poly) < 3: # not a plane - no area
                return 0
            total = [0, 0, 0]
            N = len(poly)
            for i in range(N):
                vi1 = poly[i]
                vi2 = poly[(i+1) % N]
                prod = np.cross(vi1, vi2)
                total[0] += prod[0]
                total[1] += prod[1]
                total[2] += prod[2]
            result = np.dot(total, unit_normal(poly[0], poly[1], poly[2]))
            return abs(result/2)

        for c in self.tree:
            if c == "+":
                head = np.dot(RUδ, head)
            elif c == "-":
                head = np.dot(RUmδ, head)
            elif c == "&":
                head = np.dot(RLδ, head)
            elif c == "^":
                head = np.dot(RLmδ, head)
            elif c == '\\':
                head = np.dot(RHδ, head)
            elif c == "/":
                head = np.dot(RHmδ, head)
            elif c == "|":
                head = np.dot(RU(pi), head)
            elif c == "!":
                if w > 1:
                    w -= 1
            elif c == '\'':
                color = [(c+5)%255 for c in color]
            elif c == "[":
                stack.append((pos, head, color, w))
            elif c == "]":
                if stack:
                    pos, head, color, w = stack.pop()
            elif c == "F":
                new_pos = pos + head[0] * self.dna.d
                self.lines.append(((139, 69, 19), pos, new_pos, w))
                self.size += w*self.dna.d
                pos = new_pos
            elif c == "f":
                new_pos = pos + head[0] * 10
                poly.append(new_pos)
                pos = new_pos
            elif c == "{":
                poly = []
            elif c == "}":
                try:
                    self.polys.append((color, poly))
                    a = poly_area(poly)
                    if not isnan(a):
                        self.surface += poly_area(poly)
                except:
                    pass
            elif c == "b":
                self.fruit.append(((155, 0, 0), pos, 5))

    def _apply_rule(self, c):
        # rule a -> b with probability proba
        for a, b, proba in self.dna.rules:
            if a == c and random.random() < proba:
                return b
        # if no rule was applied, return the original char.
        return c

    def draw(self):
        α = self.α
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(self.x-10, self.y-20, 20, 60)
        rot = np.array([
            [cos(α), -sin(α), 0],
            [sin(α), cos(α), 0],
            [0,      0,      1]])

        def project(coords):
            c = np.dot(rot, np.transpose(coords))
            return int(c[0]) + self.x, int(c[2])+self.y

        for color, pos_a, pos_b, width in self.lines:
            rect = pygame.draw.line(self.image, color,
                             project(pos_a),
                             project(pos_b),
                             width)
            self.rect.union_ip(rect)
        for color, pos, size in self.fruit:
            rect = pygame.draw.circle(self.image, color, project(pos), size)
            self.rect.union_ip(rect)
        for color, poly in self.polys:
            try :
                rect = pygame.draw.polygon(self.image, color, [project(p) for p in poly])
                self.rect.union_ip(rect)
            except:
                pass

    def is_alive(self):
        return self.energy > 0 and len(self.tree) > 0

    def reset(self, dna):
        self.dna = dna.copy()
        self.tree = dna.basis
        self.surface = 0
        self.size = 0
        self.energy = 10000
        self.lines = []
        self.polys = []
        self.fruit = []
        self.i = 0
        self.α = 0.0

    def has_fruit(self):
        return len(self.fruit) > 0

