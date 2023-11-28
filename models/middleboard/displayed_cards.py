from functools import partial

from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from models import GemType


class ColorButton(Button):
    """
    A button representing a color choice for a card.
    """
    def __init__(self, color=None, caller_displayed_cards=None, card=None, **kwargs):
        super(ColorButton, self).__init__(**kwargs)
        self.text = str(color)
        self.card_color = color
        self.caller_displayed_cards = caller_displayed_cards
        self.card = card

    def on_press(self):
        """
        Triggered when the button is pressed.
        """
        self.caller_displayed_cards.draw_card_any(self.card, self.card_color)


class AnyCardPopupCard(BoxLayout):
    """
    The layout for displaying color choices in the AnyCardPopup.
    """
    def __init__(self, caller_displayed_cards=None, card=None, **kwargs):
        super(AnyCardPopupCard, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.caller_displayed_cards = caller_displayed_cards
        self.card = card
        self.build_ui()

    def build_ui(self):
        """
        Build the UI with ColorButton widgets for each available color.
        """
        color_list = self.get_non_null()
        for color in color_list:
            card_button = ColorButton(color=color, caller_displayed_cards=self.caller_displayed_cards, card=self.card)
            self.add_widget(card_button)

    def get_non_null(self):
        """
        Get a list of non-null colors from the current player's owned cards.
        """
        owned_cards = self.caller_displayed_cards.parent.parent.current_player.owned_cards
        owned_colors = []
        for color in GemType:
            if color != GemType.GOLD and color != GemType.ANY:
                color_cards = owned_cards.get_card_widget(color)
                if len(color_cards.cards) > 0:
                    owned_colors.append(color)
        return owned_colors


class AnyCardPopup(Popup):
    """
    Popup for selecting a color when drawing a card with type ANY.
    """
    def __init__(self, caller_displayed_cards=None, card=None, **kwargs):
        super(AnyCardPopup, self).__init__(**kwargs)
        self.title = f'Which color should be this card?'
        self.size_hint = (.3, .3)
        self.auto_dismiss = True
        self.caller_displayed_cards = caller_displayed_cards
        popup_card = AnyCardPopupCard(caller_displayed_cards=self.caller_displayed_cards, card=card)
        self.add_widget(popup_card)


class CardButton(Button):
    """
    A button representing a card with detailed information.
    """
    def __init__(self, card=None, disabled=True, caller_displayed_cards=None, **kwargs):
        super(CardButton, self).__init__(**kwargs)
        self.card = card
        self.disabled = disabled
        card_text = self.get_card_text()
        self.text = card_text
        self.caller_displayed_cards = caller_displayed_cards

    def on_press(self):
        """
        Triggered when the button is pressed.
        """
        self.caller_displayed_cards.draw_card(self.card)

    def get_card_text(self):
        """
        Get the detailed text representation of the card.
        """
        return (
            f'ID: {self.card.card_id}\n'
            f'Color: {self.card.value} {self.card.color}\n'
            f'Victory points: {self.card.victory_points}\n'
            f'Crowns: {self.card.crowns}\n'
            f'Special effect: {self.card.special_effect}\n\n'
            f'Cost:\n{self.display_cost()}\n'
        )

    def display_cost(self):
        """
        Display the cost of the card.
        """
        return '\n'.join([f'- {color}: {value}' for color, value in self.card.cost.items()])


class DisplayedCardPopupCard(BoxLayout):
    """
    The layout for displaying cards in the DisplayedCardPopup.
    """
    def __init__(self, cards=None, caller_displayed_cards=None, **kwargs):
        super(DisplayedCardPopupCard, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.cards = cards
        self.caller_displayed_cards = caller_displayed_cards
        self.build_ui()

    def build_ui(self):
        """
        Build the UI with CardButton widgets for each available card.
        """
        for card in self.cards:
            enough_tokens = self.compute_has_enough_tokens(card=card)
            card_button = CardButton(card=card, disabled=not enough_tokens,
                                     caller_displayed_cards=self.caller_displayed_cards)
            self.add_widget(card_button)

    def compute_has_enough_tokens(self, card):
        """
        Check if the player has enough tokens to buy the card.
        """
        owned_tokens = self.caller_displayed_cards.parent.parent.current_player.owned_tokens.tokens
        owned_cards = self.caller_displayed_cards.parent.parent.current_player.owned_cards
        color_card_in_hand = self.is_there_any_color_card_in_hand()
        jokers = owned_tokens[GemType.GOLD]
        for color, required_tokens in card.cost.items():
            num_card_color = owned_cards.get_card_widget(color).num_tokens
            available_tokens = owned_tokens[color]
            delta_token = max(0, required_tokens - available_tokens - num_card_color)
            jokers -= delta_token
            if jokers < 0:
                return False
            if card.color == GemType.ANY and not color_card_in_hand:
                return False
        return True

    def is_there_any_color_card_in_hand(self):
        """
        Check if there is any color card in the player's hand. This is used to know when card ANY can be bought
        (a color has to be already owned by the user).
        """
        owned_cards = self.caller_displayed_cards.parent.parent.current_player.owned_cards
        for color_cards in owned_cards.card_widgets.values():
            if len(color_cards.cards) > 0:
                return True
        return False


class DisplayedCardPopup(Popup):
    """
    Popup for displaying cards in the game.
    """
    def __init__(self, level=None, cards=None, caller_displayed_cards=None, **kwargs):
        super(DisplayedCardPopup, self).__init__(**kwargs)
        self.title = f'Cards level {level}'
        self.size_hint = (.8, .8)
        self.auto_dismiss = True
        popup_card = DisplayedCardPopupCard(cards=cards, caller_displayed_cards=caller_displayed_cards)
        self.add_widget(popup_card)


class DisplayedCards(ButtonBehavior, BoxLayout):
    """
    The layout for displaying a set of cards in the game, on the right of the board.
    """
    cards = None

    def __init__(self, max_cards=None, level=None, deck=None, **kwargs):
        super(DisplayedCards, self).__init__(**kwargs)
        self.popup_color = None
        self.orientation = 'vertical'
        self.max_cards = max_cards
        self.cards = [None] * self.max_cards
        self.level = level
        self.deck = deck
        self.popup = None
        self.fill_cards()
        self.show_cards()

    def on_press(self):
        """
        Triggered when the user clicks on a set of cards.
        """
        self.popup = DisplayedCardPopup(level=self.level, cards=self.cards, caller_displayed_cards=self)
        self.popup.open()

    def show_cards(self):
        """
        Display the cards on the layout.
        """
        self.clear_widgets()
        for card in self.cards:
            label_text = f'Card level {card.level} (id: {card.card_id})'
            label = Label(text=label_text)
            self.add_widget(label)

    def fill_cards(self):
        """
        Fill empty card positions with new cards from the deck.
        """
        for card_position in range(len(self.cards)):
            if self.cards[card_position] is None:
                self.cards[card_position] = self.deck.draw_card()

    def remove_card(self, card):
        """
        Remove a specific card from the layout.
        """
        self.cards = [None if x == card else x for x in self.cards]

    def draw_card(self, card):
        """
        Draw a card and update the layout accordingly.
        """
        if card.color == GemType.ANY:
            # Delay the opening of the AnyCardPopup by scheduling it after a short delay
            Clock.schedule_once(partial(self.open_any_card_popup, card), 0.1)
        else:
            # Continue with the rest of the draw_card logic for other card types
            current_player = self.parent.parent.current_player
            current_player.owned_cards.get_card_widget(card.color).add_card(card)
            current_player.owned_tokens.remove_tokens(card.cost)
            self.remove_card(card)
            self.fill_cards()
            self.show_cards()
            self.popup.dismiss()
            self.parent.parent.end_turn()

    def draw_card_any(self, card, color):
        """
        Draw a card with type ANY and update the layout accordingly.
        """
        current_player = self.parent.parent.current_player
        card.color = color
        current_player.owned_cards.get_card_widget(card.color).add_card(card)
        current_player.owned_tokens.remove_tokens(card.cost)
        self.remove_card(card)
        self.fill_cards()
        self.show_cards()
        self.popup_color.dismiss()
        self.popup.dismiss()
        self.parent.parent.end_turn()

    def open_any_card_popup(self, card, dt):
        """
        Open the AnyCardPopup after a short delay.
        """
        self.popup_color = AnyCardPopup(owned_cards=self.parent.parent.current_player.owned_cards, card=card,
                                        caller_displayed_cards=self)
        self.popup_color.open()

    def __str__(self):
        return f'{self.cards}'
