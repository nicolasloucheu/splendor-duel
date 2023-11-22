from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from models.player.owned_cards import OwnedCards
from models.player.owned_scrolls import OwnedScrolls
from models.player.owned_tokens import OwnedTokens
from models.player.reserved import Reserved


class Player(GridLayout):

    def __init__(self, reserved_cards, **kwargs):
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
        reserved_cards = Reserved(reserved_cards=reserved_cards)
        self.add_widget(reserved_cards)
