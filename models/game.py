from enum import Enum
import random

from kivy.uix.boxlayout import BoxLayout

from models.middleboard.middleboard import MiddleBoard
from models.player.player import Player


class GameState(Enum):
    START = 1
    PLAYING = 2
    END = 3


class Game(BoxLayout):
    first_player = None
    player1 = None
    player2 = None
    game_state = GameState.START
    turn = None

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
        self.start_game()

    def start_game(self):
        first_player = random.choice([self.player1, self.player2])
        print(first_player)
        self.turn = Turn(first_player, self.game_state)
        self.turn.start_turn()


class Turn:
    def __init__(self, player, game_state):
        self.player = player
        self.game_state = game_state

    def start_turn(self):
        print('start turn')