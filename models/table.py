from kivy.uix.boxlayout import BoxLayout

from models.middleboard import MiddleBoard
from models.player import Player


class Table(BoxLayout):
    def __init__(self, **kwargs):
        super(Table, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 20
        player2 = Player()
        self.add_widget(player2)
        middleboard = MiddleBoard()
        self.add_widget(middleboard)
        player1 = Player()
        self.add_widget(player1)

