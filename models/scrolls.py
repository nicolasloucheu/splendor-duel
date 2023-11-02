from kivy.graphics import Ellipse
from kivy.metrics import dp
from kivy.uix.widget import Widget


class Scrolls(Widget):
    def __init__(self, **kwargs):
        super(Scrolls, self).__init__(**kwargs)
        self.scrolls = 3
        self.orientation = 'vertical'
        self.circe_size = dp(20)
        self.circle1 = Ellipse(size=(self.circe_size, self.circe_size))
        self.circle2 = Ellipse(size=(self.circe_size, self.circe_size))
        self.circle3 = Ellipse(size=(self.circe_size, self.circe_size))
        self.circles = [self.circle1, self.circle2, self.circle3]
        self.canvas.add(self.circle1)
        self.canvas.add(self.circle2)
        self.canvas.add(self.circle3)

    def on_size(self, *args):
        circle_positions = [(self.center_x - 25, self.height * i / 10 - 25) for i in range(4, 4 + self.scrolls)]
        for circle, position in zip(self.circles, circle_positions):
            circle.pos = position

    def draw_scroll(self):
        self.scrolls -= 1
