from models import LEVEL1_CARDS, LEVEL2_CARDS, LEVEL3_CARDS, CROWN_CARDS


class Deck1:
    cards = []

    def __init__(self):
        self.cards.extend(LEVEL1_CARDS)


class Deck2:
    cards = []

    def __init__(self):
        self.cards.extend(LEVEL2_CARDS)


class Deck3:
    cards = []

    def __init__(self):
        self.cards.extend(LEVEL3_CARDS)