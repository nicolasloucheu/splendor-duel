from kivy.app import App
from models.table import Table
from models.player import Player


class SplendorApp(App):
    def build(self):
        return Player()


if __name__ == '__main__':
    SplendorApp().run()
