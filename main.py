import pygame
from models import LEVEL1_CARDS, LEVEL2_CARDS, LEVEL3_CARDS, CROWN_CARDS
from models.tokenbag import TokenBag
from models.board import Board
from models.decks import Deck
from models.display_cards import DisplayCards

pygame.init()
bounds = (1024, 768)
window = pygame.display.set_mode(bounds)
pygame.display.set_caption("Splendor Duel")

tokenbag = TokenBag()
board = Board()
tokenbag.shuffle()
board.fill(tokenbag=tokenbag)

level1_deck = Deck(db_cards=LEVEL1_CARDS)
level2_deck = Deck(db_cards=LEVEL2_CARDS)
level3_deck = Deck(db_cards=LEVEL3_CARDS)
crown_deck = Deck(db_cards=CROWN_CARDS)

display1 = DisplayCards(max_cards=5, level=1, deck=level1_deck)
display2 = DisplayCards(max_cards=4, level=2, deck=level2_deck)
display3 = DisplayCards(max_cards=3, level=3, deck=level3_deck)
display_crown = DisplayCards(max_cards=4, level=4, deck=crown_deck)
