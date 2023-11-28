from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from models import GemType


class TotalPointsCrowns(BoxLayout):
    def __init__(self, **kwargs):
        super(TotalPointsCrowns, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.total_points = 0
        self.total_crowns = 0
        self.build_ui()

    def update_points_crowns(self):
        for color in GemType:
            if color != GemType.GOLD and color != GemType.ANY:
                color_card = self.parent.get_card_widget(color)
                self.total_points += color_card.victory_points
                self.total_crowns += color_card.crowns
        self.clear_widgets()
        self.build_ui()

    def build_ui(self):
        self.add_widget(Label(text=f'total points={self.total_points}'))
        self.add_widget(Label(text=f'crowns={self.total_crowns}'))


class OwnedCardBox(BoxLayout):
    def __init__(self, color=None, **kwargs):
        super(OwnedCardBox, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.color = color
        self.num_tokens = 0
        self.victory_points = 0
        self.crowns = 0
        self.cards = []
        self.build_ui()

    def add_card(self, card):
        self.cards.append(card)
        self.update_cards(self.cards)

    def update_cards(self, cards):
        self.cards = cards
        self.num_tokens = sum([card.value for card in cards])
        self.victory_points = sum([card.victory_points for card in cards])
        self.crowns = sum([card.crowns for card in cards])
        self.clear_widgets()
        self.build_ui()
        self.parent.points_crowns.update_points_crowns()

    def build_ui(self):
        self.add_widget(Label(text=f'{self.color}'))
        self.add_widget(Label(text=f'tokens: {self.num_tokens}'))
        self.add_widget(Label(text=f'points: {self.victory_points}'))


class OwnedCards(BoxLayout):
    def __init__(self, **kwargs):
        super(OwnedCards, self).__init__(**kwargs)
        self.card_widgets = {}
        for color in GemType:
            if color != GemType.GOLD and color != GemType.ANY:
                card = OwnedCardBox(orientation='vertical', color=color)
                self.card_widgets[color] = card
                self.add_widget(card)

        card = OwnedCardBox(orientation='vertical', color='neutral')
        self.card_widgets['neutral'] = card
        self.add_widget(card)

        self.points_crowns = TotalPointsCrowns()
        self.add_widget(self.points_crowns)

    def get_card_widget(self, color):
        return self.card_widgets.get(color)
