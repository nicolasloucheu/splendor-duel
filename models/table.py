from kivy.uix.boxlayout import BoxLayout

from models import CROWN_CARDS, LEVEL1_CARDS, LEVEL2_CARDS, LEVEL3_CARDS
from models.board import Board
from models.crown_cards import CrownCards
from models.decks import Deck
from models.displayed_cards import DisplayedCards
from models.scrolls import Scrolls


class Table(BoxLayout):

    def __init__(self, **kwargs):
        super(Table, self).__init__(**kwargs)
        crown_cards = CrownCards(deck=Deck(db_cards=CROWN_CARDS))
        self.add_widget(crown_cards)
        scrolls = Scrolls()
        self.add_widget(scrolls)
        board = Board()
        self.add_widget(board)
        displayed_cards1 = DisplayedCards(max_cards=5, level=1, deck=Deck(db_cards=LEVEL1_CARDS))
        self.add_widget(displayed_cards1)
        displayed_cards2 = DisplayedCards(max_cards=4, level=1, deck=Deck(db_cards=LEVEL2_CARDS))
        self.add_widget(displayed_cards2)
        displayed_cards3 = DisplayedCards(max_cards=3, level=1, deck=Deck(db_cards=LEVEL3_CARDS))
        self.add_widget(displayed_cards3)
