from kivy.uix.label import Label


class OwnedScrolls(Label):
    scrolls = 0

    def __init__(self, **kwargs):
        super(OwnedScrolls, self).__init__(**kwargs)
        self.text = str(self.scrolls) + ' scrolls'
