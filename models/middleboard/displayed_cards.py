from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class DisplayedCards(BoxLayout):
    max_cards = None
    level = None
    deck = None
    cards = []

    def __init__(self, max_cards=None, level=None, deck=None, **kwargs):
        super(DisplayedCards, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.max_cards = max_cards
        self.cards = [None] * self.max_cards
        self.level = level
        self.deck = deck
        self.fill_cards()
        self.show_cards()

    def show_cards(self):
        for card in self.cards:
            # str_label = f'{card.victory_points} victory points\nCost: {card.cost}\nLevel: {card.level}'
            # if card.special_effect:
            #     special_effect = card.special_effect.name.lower()
            #     str_label += f' - {special_effect}'
            # else:
            #     str_label += ' - no effect'
            str_label = f'Card level {card.level} (id: {card.card_id})'
            label = Label(text=str_label)
            self.add_widget(label)

    def fill_cards(self):
        for card_position in range(len(self.cards)):
            if self.cards[card_position] is None:
                self.cards[card_position] = self.deck.draw_card()

    def draw_card(self, card_position):
        return self.cards.pop(card_position)

    def __str__(self):
        return f'{self.cards}'


