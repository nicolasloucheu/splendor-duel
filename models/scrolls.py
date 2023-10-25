from models.scroll import Scroll


class Scrolls:
    """
    Scrolls available on the table
    """
    scrolls = []

    def __init__(self):
        self.scrolls = [Scroll(1), Scroll(2), Scroll(3)]

    def draw_scroll(self):
        return self.scrolls.pop(0)
