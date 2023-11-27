from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from models.unit.token import GemType


class OwnedTokens(BoxLayout):

    def __init__(self, **kwargs):
        super(OwnedTokens, self).__init__(**kwargs)
        self.tokens = {GemType.RED: 0, GemType.GREEN: 0, GemType.BLUE: 0, GemType.BLACK: 0, GemType.WHITE: 0,
                       GemType.PEARL: 0, GemType.GOLD: 0}
        self.update_widgets()

    def add_tokens(self, tokens_list):
        for token in tokens_list:
            self.tokens[token.gem_type] += 1
        self.clear_widgets()
        self.update_widgets()

    def remove_tokens(self, tokens_dict_to_pay=None):
        for key in self.tokens:
            if key in tokens_dict_to_pay:
                if self.tokens[key] < tokens_dict_to_pay[key]:
                    self.tokens[GemType.GOLD] -= tokens_dict_to_pay[key] - self.tokens[key]
                    self.tokens[key] = 0
                else:
                    self.tokens[key] -= tokens_dict_to_pay[key]
        self.update_widgets()

    def update_widgets(self):
        self.clear_widgets()
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
