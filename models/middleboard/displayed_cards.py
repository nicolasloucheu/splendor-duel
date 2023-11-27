from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from models import GemType


class CardButton(Button):
    def __init__(self, card=None, disabled=True, caller_displayed_cards=None, **kwargs):
        super(CardButton, self).__init__(**kwargs)
        self.card = card
        self.disabled = disabled
        card_text = self.get_card_text(self.card)
        self.text = card_text
        self.caller_displayed_cards = caller_displayed_cards

    def on_press(self):
        print(f'Card pressed: {self.card}')
        print(f'Card color: {self.card.color}')
        current_player = self.caller_displayed_cards.parent.parent.current_player
        print(f'Current player: {current_player}')
        current_player.owned_cards.get_card_widget(self.card.color).add_card(self.card)

    def get_card_text(self, card):
        return (
            f'ID: {card.card_id}\n'
            f'Color: {card.value} {card.color}\n'
            f'Victory points: {card.victory_points}\n'
            f'Crowns: {card.crowns}\n'
            f'Special effect: {card.special_effect}\n\n'
            f'Cost:\n{self.display_cost(card)}\n'
        )

    @staticmethod
    def display_cost(card):
        return '\n'.join([f'- {color}: {value}' for color, value in card.cost.items()])


class DisplayedCardPopupCard(BoxLayout):
    def __init__(self, cards=None, owned_tokens=None, caller_displayed_cards=None, **kwargs):
        super(DisplayedCardPopupCard, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.build_ui(cards, owned_tokens, caller_displayed_cards)

    def build_ui(self, cards, owned_tokens, caller_displayed_cards):
        for card in cards:
            enough_tokens = self.compute_has_enough_tokens(card, owned_tokens)
            card_button = CardButton(card=card, disabled=not enough_tokens, caller_displayed_cards=caller_displayed_cards)
            self.add_widget(card_button)

    @staticmethod
    def compute_has_enough_tokens(card, owned_tokens):
        jokers = owned_tokens[GemType.GOLD]
        for color, required_tokens in card.cost.items():
            available_tokens = owned_tokens[color]
            delta_token = max(0, required_tokens - available_tokens)
            jokers -= delta_token
            if jokers < 0:
                return False
        return True


class DisplayedCardPopup(Popup):
    def __init__(self, level=None, cards=None, owned_tokens=None, caller_displayed_cards=None, **kwargs):
        super(DisplayedCardPopup, self).__init__(**kwargs)
        self.title = f'Cards level {level}'
        self.size_hint = (.8, .8)
        self.auto_dismiss = True
        popup_card = DisplayedCardPopupCard(cards=cards, owned_tokens=owned_tokens,
                                            caller_displayed_cards=caller_displayed_cards)
        self.add_widget(popup_card)


class DisplayedCards(ButtonBehavior, BoxLayout):
    cards = None

    def __init__(self, max_cards=None, level=None, deck=None, **kwargs):
        super(DisplayedCards, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.max_cards = max_cards
        self.cards = [None] * self.max_cards
        self.level = level
        self.deck = deck
        self.fill_cards()
        self.show_cards()

    def on_press(self):
        owned_tokens = self.parent.parent.current_player.owned_tokens.tokens
        popup = DisplayedCardPopup(level=self.level, cards=self.cards, owned_tokens=owned_tokens,
                                   caller_displayed_cards=self)
        popup.open()

    def show_cards(self):
        for card in self.cards:
            label_text = f'Card level {card.level} (id: {card.card_id})'
            label = Label(text=label_text)
            self.add_widget(label)

    def fill_cards(self):
        for card_position in range(len(self.cards)):
            if self.cards[card_position] is None:
                self.cards[card_position] = self.deck.draw_card()

    def draw_card(self, card_position):
        return self.cards.pop(card_position)

    def __str__(self):
        return f'{self.cards}'
