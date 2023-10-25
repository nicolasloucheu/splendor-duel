class Scrolls:
    """
    Scrolls available on the table
    """
    scrolls = None

    def __init__(self):
        self.scrolls = 3

    def draw_scroll(self):
        self.scrolls -= 1
