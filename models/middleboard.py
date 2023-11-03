from kivy.uix.boxlayout import BoxLayout

from models import CROWN_CARDS, LEVEL1_CARDS, LEVEL2_CARDS, LEVEL3_CARDS
from models.board import Board
from models.crown_cards import CrownCards
from models.decks import Deck
from models.displayed_cards import DisplayedCards
from models.scrolls import Scrolls


class MiddleBoard(BoxLayout):

    def __init__(self, **kwargs):
        super(MiddleBoard, self).__init__(**kwargs)
        self.cards_size = (.25, 1)
        crown_cards = CrownCards(deck=Deck(db_cards=CROWN_CARDS), size_hint=self.cards_size)
        self.add_widget(crown_cards)
        scrolls = Scrolls(size_hint=(.25, 1))
        self.add_widget(scrolls)
        board = Board()
        self.add_widget(board)
        displayed_cards1 = DisplayedCards(max_cards=5, level=1, deck=Deck(db_cards=LEVEL1_CARDS), size_hint=self.cards_size)
        self.add_widget(displayed_cards1)
        displayed_cards2 = DisplayedCards(max_cards=4, level=1, deck=Deck(db_cards=LEVEL2_CARDS), size_hint=self.cards_size)
        self.add_widget(displayed_cards2)
        displayed_cards3 = DisplayedCards(max_cards=3, level=1, deck=Deck(db_cards=LEVEL3_CARDS), size_hint=self.cards_size)
        self.add_widget(displayed_cards3)
