from kivy.uix.boxlayout import BoxLayout

from models.middleboard.middleboard import MiddleBoard
from models.player.player import Player


class Table(BoxLayout):
    def __init__(self, **kwargs):
        super(Table, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 20
        player2 = Player(reserved_cards=[])
        self.add_widget(player2)
        middleboard = MiddleBoard()
        self.add_widget(middleboard)
        player1 = Player(reserved_cards=[])
        self.add_widget(player1)

