from enum import Enum
import random

from kivy.uix.boxlayout import BoxLayout

from models.middleboard.middleboard import MiddleBoard
from models.player.player import Player


class GameState(Enum):
    START = 1
    PLAYING = 2
    END = 3


class TurnState(Enum):
    START = 1
    PLAYING = 2
    END = 3


class Game(BoxLayout):

    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)

        self.orientation = 'vertical'
        self.spacing = 20

        self.player2 = Player(reserved_cards=[], name='player2')
        self.add_widget(self.player2)

        middleboard = MiddleBoard()
        self.add_widget(middleboard)

        self.player1 = Player(reserved_cards=[], name='player1')
        self.add_widget(self.player1)

        self.current_player = random.choice([self.player1, self.player2])
        self.game_state = GameState.START
        self.turn_state = None
        self.turn = None

        self.start_game()

    def start_game(self):
        self.game_state = GameState.PLAYING
        self.start_turn()

    def start_turn(self):
        print(f"{self.current_player}'s turn")

    def end_turn(self):
        self.turn_state = TurnState.END
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2
        self.start_turn()
