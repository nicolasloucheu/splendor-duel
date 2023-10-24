from enum import Enum
import pygame


class GemType(Enum):
    BLUE = 1
    WHITE = 2
    GREEN = 3
    BLACK = 4
    RED = 5
    PEARL = 6
    GOLD = 7


class Token:
    gem_type = None
    image = None

    def __init__(self, gem_type):
        self.gem_type = gem_type
        self.image = pygame.image.load('images/' + self.gem_type.name + '.jpeg')

    def __str__(self):
        return f'{self.gem_type}'

    def __repr__(self):
        return f'{self.gem_type}'

