from models.decks import Deck


class DisplayCards:
    max_cards = None
    level = None
    cards = []

    def __init__(self, max_cards, level, deck):
        self.max_cards = max_cards
        self.cards = [None] * self.max_cards
        self.level = level
        self.deck = deck

    def fill_cards(self):
        for card_position in range(len(self.cards)):
            if self.cards[card_position] is None:
                self.cards[card_position] = self.deck.draw_card()

    def __str__(self):
        return f'{self.cards}'


