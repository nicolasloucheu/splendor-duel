from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from models import GemType, SpecialEffect


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

        self.apply_special_effect(card)
        self.update_cards()

    def update_cards(self):
        self.cards = self.cards
        self.num_tokens = sum([card.value for card in self.cards])
        self.victory_points = sum([card.victory_points for card in self.cards])
        self.crowns = sum([card.crowns for card in self.cards])
        self.clear_widgets()
        self.build_ui()
        self.parent.points_crowns.update_points_crowns()

    def apply_special_effect(self, card):
        if card.special_effect == SpecialEffect.PLAY_AGAIN:
            current_player = self.parent.parent.parent.current_player
            player1 = self.parent.parent.parent.player1
            player2 = self.parent.parent.parent.player2
            self.parent.parent.parent.current_player = player1 if current_player == player2 else player2
        elif card.special_effect == SpecialEffect.TAKE_SAME_COLOR:
            print('take same color')
            pass
        elif card.special_effect == SpecialEffect.TAKE_SCROLL:
            if self.parent.parent.parent.middleboard.scrolls.scrolls > 0:
                self.parent.parent.parent.middleboard.scrolls.take_scroll()
                self.parent.parent.parent.current_player.owned_scrolls.take_scroll()
            elif self.parent.parent.parent.opponent.owned_scrolls.scrolls > 0:
                self.parent.parent.parent.opponent.owned_scrolls.use_scroll()
                self.parent.parent.parent.current_player.owned_scrolls.scrolls.take_scroll()
        elif card.special_effect == SpecialEffect.TAKE_OPPONENT_TOKEN:
            print('take opponent token')
            pass

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
