from kivy.uix.boxlayout import BoxLayout

from models import CROWN_CARDS
from models.board import Board
from models.crown_cards import CrownCards
from models.decks import Deck
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
