from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout


class Player(GridLayout):
    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.cols = 2
        size_top = (1, .2)
        owned_tokens = Button(text='owned_tokens', size_hint=size_top)
        self.add_widget(owned_tokens)
        owned_scrolls = Button(text='owned_scrolls', size_hint=size_top)
        self.add_widget(owned_scrolls)
        owned_cards = Button(text='owned_cards')
        self.add_widget(owned_cards)
        reserved_cards = Button(text='reserved_cards')
        self.add_widget(reserved_cards)
