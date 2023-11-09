from kivy.app import App
from models.table import Table


class SplendorApp(App):
    def build(self):
        return Table()


if __name__ == '__main__':
    SplendorApp().run()
