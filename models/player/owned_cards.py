from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from models import GemType


class OwnedCardBox(BoxLayout):
    def __init__(self, color=None, **kwargs):
        super(OwnedCardBox, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.color = color
        self.num_tokens = 0
        self.victory_points = 0
        self.cards = []
        self.build_ui()

    def add_card(self, card):
        self.cards.append(card)
        self.update_cards(self.cards)

    def update_cards(self, cards):
        self.cards = cards
        self.num_tokens = sum([card.value for card in cards])
        self.victory_points = sum([card.victory_points for card in cards])
        self.clear_widgets()
        self.build_ui()

    def build_ui(self):
        self.add_widget(Label(text=f'{self.color}'))
        self.add_widget(Label(text=f'tokens: {self.num_tokens}'))
        self.add_widget(Label(text=f'points: {self.victory_points}'))


class OwnedCards(BoxLayout):

    def __init__(self, **kwargs):
        super(OwnedCards, self).__init__(**kwargs)
        self.card_widgets = {}
        for color in GemType:
            if color != GemType.GOLD:
                card = OwnedCardBox(orientation='vertical', color=color)
                self.card_widgets[color] = card
                self.add_widget(card)

        neutral_cards = BoxLayout(orientation='vertical')
        neutral_label = Label(text='neutral')
        neutral_points = Label(text='points=0')
        neutral_cards.add_widget(neutral_label)
        neutral_cards.add_widget(Label())
        neutral_cards.add_widget(neutral_points)
        self.add_widget(neutral_cards)
        points_crowns = BoxLayout(orientation='vertical')
        total_points = Label(text='total points=0')
        total_crowns = Label(text='crowns=0')
        points_crowns.add_widget(total_points)
        points_crowns.add_widget(total_crowns)
        self.add_widget(points_crowns)

    def get_card_widget(self, color):
        return self.card_widgets.get(color)
