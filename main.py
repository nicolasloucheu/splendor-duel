import pygame
from models.tokenbag import TokenBag
from models.board import Board

pygame.init()
bounds = (1024, 768)
window = pygame.display.set_mode(bounds)
pygame.display.set_caption("Splendor Duel")

tokenbag = TokenBag()
board = Board()
tokenbag.shuffle()
board.fill(tokenbag)