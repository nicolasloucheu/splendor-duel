from collections import Counter


class Player:
    name = None
    hand = None
    reserved_cards = None
    owned_tokens = None
    owned_scrolls = None

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.reserved_cards = []
        self.owned_tokens = {}
        self.owned_scrolls = 0

    def buy_card(self, display_cards=None, card_position=None, tokenbag=None):
        new_card = display_cards.draw(card_position)
        self.hand.append(new_card)
        tokenbag.add_tokens(tokens=new_card.cost)
        self.owned_tokens = dict(Counter(self.owned_tokens) - Counter(new_card.cost))

    def reserve_card(self, display_cards=None, card_position=None, board=None, token_position=None):
        self.owned_tokens = dict(Counter(self.owned_tokens) + Counter(board.draw_tokens(token_position=token_position)))
        self.reserved_cards.append(display_cards.draw(card_position))

    def buy_reserved_card(self, card_position=None, tokenbag=None):
        new_card = self.reserved_cards.pop(card_position)
        self.hand.append(new_card)
        tokenbag.add_tokens(tokens=new_card.cost)
        self.owned_tokens = dict(Counter(self.owned_tokens) - Counter(new_card.cost))

    def take_scroll(self, scroll=None):
        scroll.draw_scroll()
        self.owned_scrolls += 1

    def draw_tokens(self, board=None, token_positions=None):
        drawn_tokens = board.draw_tokens(token_position=token_positions)
        self.owned_tokens = dict(Counter(self.owned_tokens) + Counter(drawn_tokens))

    def draw_royal_card(self, crown_deck=None, card_position=None):
        new_card = crown_deck.draw(card_position)
        self.hand.append(new_card)

    def play_scroll(self):
        self.owned_scrolls -= 1
