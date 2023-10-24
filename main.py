import pygame
from models.tokenbag import TokenBag
from models.board import Board
from models.decks import DeckLevel1, DeckLevel2, DeckLevel3
from models.display_cards import DisplayCards

pygame.init()
bounds = (1024, 768)
window = pygame.display.set_mode(bounds)
pygame.display.set_caption("Splendor Duel")

tokenbag = TokenBag()
board = Board()
tokenbag.shuffle()
board.fill(tokenbag)

level1_deck = DeckLevel1()
level2_deck = DeckLevel2()
level3_deck = DeckLevel3()

display1 = DisplayCards(max_cards=5, level=1, deck=level1_deck)
display1.fill_cards()
print(display1)