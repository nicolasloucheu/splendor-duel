from models import LEVEL1_CARDS, LEVEL2_CARDS, LEVEL3_CARDS
from models.card import Card, SpecialEffect
from models.token import GemType
import random


class Deck:

    def __init__(self):
        self.cards = []

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()

    def __str__(self):
        return f'{self.cards}'


class DeckLevel1(Deck):

    def __init__(self):
        super().__init__()
        self.cards.extend(LEVEL1_CARDS)


class DeckLevel2(Deck):

    def __init__(self):
        super().__init__()
        self.cards.extend(LEVEL2_CARDS)


class DeckLevel3(Deck):

    def __init__(self):
        super().__init__()
        self.cards.extend(LEVEL3_CARDS)
