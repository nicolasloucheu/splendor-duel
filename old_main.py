from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from enum import Enum
from models import LEVEL1_CARDS, LEVEL2_CARDS, LEVEL3_CARDS, CROWN_CARDS
from models.board import Board
from models.decks import Deck
from models.display_cards import DisplayCards
from models.player import Player
from models.tokenbag import TokenBag
import random


class GameEngine:
    tokenbag = None
    level1_deck = None
    level2_deck = None
    level3_deck = None
    crown_deck = None
    board = None
    display1 = None
    display2 = None
    display3 = None
    display_crown = None
    player1 = None
    player2 = None
    state = None
    current_player = None
    result = None

    def __init__(self, **kwargs):
        self.tokenbag = TokenBag()
        self.level1_deck = Deck(db_cards=LEVEL1_CARDS)
        self.level2_deck = Deck(db_cards=LEVEL2_CARDS)
        self.level3_deck = Deck(db_cards=LEVEL3_CARDS)
        self.crown_deck = Deck(db_cards=CROWN_CARDS)
        self.board = Board()
        self.board.fill(tokenbag=self.tokenbag)

        self.display1 = DisplayCards(max_cards=5, level=1, deck=self.level1_deck)
        self.display2 = DisplayCards(max_cards=4, level=2, deck=self.level2_deck)
        self.display3 = DisplayCards(max_cards=3, level=3, deck=self.level3_deck)
        self.display_crown = DisplayCards(max_cards=4, level=4, deck=self.crown_deck)

        self.player1 = Player(name='Player 1')
        self.player2 = Player(name='Player 2')
        self.player1.opponent = self.player2
        self.player2.opponent = self.player1

        self.current_player = random.choice([self.player1, self.player2])
        self.state = GameState.PLAYING

    def play(self, key):
        if key is None:
            return

        if self.state == GameState.ENDED:
            return


class GameState(Enum):
    PLAYING = 0
    ENDED = 1


class TableLayout(BoxLayout):
    pass


class RoyalCards(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.royal_cards = game.crown_deck

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print(touch)
            print('pressed')


class SplendorApp(App):
    pass


SplendorApp().run()
game = GameEngine()
