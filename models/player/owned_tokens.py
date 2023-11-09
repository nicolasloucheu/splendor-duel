from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from models.unit.token import GemType


class OwnedTokens(BoxLayout):
    tokens = {GemType.RED: 0, GemType.GREEN: 0, GemType.BLUE: 0, GemType.BLACK: 0, GemType.WHITE: 0, GemType.PEARL: 0,
              GemType.GOLD: 0}

    def __init__(self, **kwargs):
        super(OwnedTokens, self).__init__(**kwargs)
        red_tokens = Label(text=str(self.tokens[GemType.RED]) + ' red')
        self.add_widget(red_tokens)
        green_tokens = Label(text=str(self.tokens[GemType.GREEN]) + ' green')
        self.add_widget(green_tokens)
        blue_tokens = Label(text=str(self.tokens[GemType.BLUE]) + ' blue')
        self.add_widget(blue_tokens)
        black_tokens = Label(text=str(self.tokens[GemType.BLACK]) + ' black')
        self.add_widget(black_tokens)
        white_tokens = Label(text=str(self.tokens[GemType.WHITE]) + ' white')
        self.add_widget(white_tokens)
        pearl_tokens = Label(text=str(self.tokens[GemType.PEARL]) + ' pearl')
        self.add_widget(pearl_tokens)
        gold_tokens = Label(text=str(self.tokens[GemType.GOLD]) + ' gold')
        self.add_widget(gold_tokens)

