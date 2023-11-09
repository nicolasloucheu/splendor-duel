from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class OwnedCards(BoxLayout):

    def __init__(self, **kwargs):
        super(OwnedCards, self).__init__(**kwargs)
        red_cards = Button(text='red')
        self.add_widget(red_cards)
        green_cards = Button(text='green')
        self.add_widget(green_cards)
        blue_cards = Button(text='blue')
        self.add_widget(blue_cards)
        black_cards = Button(text='black')
        self.add_widget(black_cards)
        white_cards = Button(text='white')
        self.add_widget(white_cards)
        neutral_cards = Button(text='neutral')
        self.add_widget(neutral_cards)
        empty_spot = Label()
        self.add_widget(empty_spot)
