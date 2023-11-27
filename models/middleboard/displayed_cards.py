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
        card_text = self.get_card_text()
        self.text = card_text
        self.caller_displayed_cards = caller_displayed_cards

    def on_press(self):
        # current_player = self.caller_displayed_cards.parent.parent.current_player
        if self.card.color == GemType.ANY:
            pass
        else:
            # current_player.owned_cards.get_card_widget(self.card.color).add_card(self.card)
            self.caller_displayed_cards.draw_card(self.card)

    def get_card_text(self):
        return (
            f'ID: {self.card.card_id}\n'
            f'Color: {self.card.value} {self.card.color}\n'
            f'Victory points: {self.card.victory_points}\n'
            f'Crowns: {self.card.crowns}\n'
            f'Special effect: {self.card.special_effect}\n\n'
            f'Cost:\n{self.display_cost()}\n'
        )

    def display_cost(self):
        return '\n'.join([f'- {color}: {value}' for color, value in self.card.cost.items()])


class DisplayedCardPopupCard(BoxLayout):
    def __init__(self, cards=None, owned_tokens=None, caller_displayed_cards=None, **kwargs):
        super(DisplayedCardPopupCard, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.cards = cards
        self.owned_tokens = owned_tokens
        self.caller_displayed_cards = caller_displayed_cards
        self.build_ui()

    def build_ui(self):
        for card in self.cards:
            enough_tokens = self.compute_has_enough_tokens(card=card)
            card_button = CardButton(card=card, disabled=not enough_tokens,
                                     caller_displayed_cards=self.caller_displayed_cards)
            self.add_widget(card_button)

    def compute_has_enough_tokens(self, card):
        color_card_in_hand = self.is_there_any_color_card_in_hand()
        jokers = self.owned_tokens[GemType.GOLD]
        for color, required_tokens in card.cost.items():
            available_tokens = self.owned_tokens[color]
            delta_token = max(0, required_tokens - available_tokens)
            jokers -= delta_token
            if jokers < 0:
                return False
            if card.color == GemType.ANY and not color_card_in_hand:
                return False
        return True

    def is_there_any_color_card_in_hand(self):
        owned_cards = self.caller_displayed_cards.parent.parent.current_player.owned_cards
        for color_cards in owned_cards.card_widgets.values():
            if len(color_cards.cards) > 0:
                return True
        return False


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
        self.popup = None
        self.fill_cards()
        self.show_cards()

    def on_press(self):
        owned_tokens = self.parent.parent.current_player.owned_tokens.tokens
        self.popup = DisplayedCardPopup(level=self.level, cards=self.cards, owned_tokens=owned_tokens,
                                        caller_displayed_cards=self)
        self.popup.open()

    def show_cards(self):
        self.clear_widgets()
        for card in self.cards:
            label_text = f'Card level {card.level} (id: {card.card_id})'
            label = Label(text=label_text)
            self.add_widget(label)

    def fill_cards(self):
        for card_position in range(len(self.cards)):
            if self.cards[card_position] is None:
                self.cards[card_position] = self.deck.draw_card()

    def remove_card(self, card):
        self.cards = [None if x == card else x for x in self.cards]

    def draw_card(self, card):
        current_player = self.parent.parent.current_player
        # card = self.cards.pop(selected_card)
        current_player.owned_cards.get_card_widget(card.color).add_card(card)
        current_player.owned_tokens.remove_tokens(card.cost)
        self.remove_card(card)
        self.fill_cards()
        self.show_cards()
        self.popup.dismiss()
        self.parent.parent.end_turn()

    def __str__(self):
        return f'{self.cards}'
