from kivy.graphics import Ellipse
from kivy.uix.widget import Widget


class Scrolls(Widget):
    def __init__(self, **kwargs):
        super(Scrolls, self).__init__(**kwargs)
        self.scrolls = 3
        self.orientation = 'vertical'
        self.circle1 = Ellipse(size=(50, 50))
        self.circle2 = Ellipse(size=(50, 50))
        self.circle3 = Ellipse(size=(50, 50))
        self.canvas.add(self.circle1)
        self.canvas.add(self.circle2)
        self.canvas.add(self.circle3)

    def on_size(self, *args):
        print('on size: ' + str(self.width) + ', ' + str(self.height))
        print(self.center_x, self.center_y)
        self.circle1.pos = (self.center_x - 25, self.height*1/4 - 25)
        self.circle2.pos = (self.center_x - 25, self.height*2/4 - 25)
        self.circle3.pos = (self.center_x - 25, self.height*3/4 - 25)

    def draw_scroll(self):
        self.scrolls -= 1
