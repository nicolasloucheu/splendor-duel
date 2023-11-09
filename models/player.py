from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from models.owned_cards import OwnedCards
from models.owned_scrolls import OwnedScrolls
from models.owned_tokens import OwnedTokens


class Player(GridLayout):

    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.cols = 2
        self.size_hint = (.75, .5)
        self.pos_hint = {'center_x': .5}
        size_top = (1, .33)
        owned_tokens = OwnedTokens(size_hint=size_top)
        self.add_widget(owned_tokens)
        owned_scrolls = OwnedScrolls(size_hint=size_top)
        self.add_widget(owned_scrolls)
        owned_cards = OwnedCards()
        self.add_widget(owned_cards)
        reserved_cards = Button(text='reserved_cards')
        self.add_widget(reserved_cards)
