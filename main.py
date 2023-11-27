from kivy.app import App
from kivy.core.window import Window

from models.game import Game

Window.size = (1920, 720)


class SplendorApp(App):
    def build(self):
        return Game()


if __name__ == '__main__':
    SplendorApp().run()
