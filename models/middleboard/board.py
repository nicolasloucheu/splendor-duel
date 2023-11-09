from collections import Counter

from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label

from models.unit.token import Token
from models.unit.tokenbag import TokenBag


def find_index(target_value, matrix):
    for row_index, row in enumerate(matrix):
        try:
            column_index = row.index(target_value)
        except ValueError:
            continue
        yield row_index, column_index


class Board(GridLayout):
    board_gems = None

    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        self.cols = 5
        self.tokenbag = TokenBag()
        self.index_board = [
            [21, 22, 23, 24, 25],
            [20, 7, 8, 9, 10],
            [19, 6, 1, 2, 11],
            [18, 5, 4, 3, 12],
            [17, 16, 15, 14, 13]
        ]
        self.board_gems = [[None] * 5 for _ in range(5)]
        self.fill(self.tokenbag)

        # Create and add buttons to represent tokens on the board

    def fill(self, tokenbag=None):
        for current_position in range(1, 26):
            if tokenbag.get_number_of_tokens_in_bag() > 0:
                matches = [match for match in find_index(current_position, self.index_board)]
                double_index = list(matches[0])
                if self.board_gems[double_index[0]][double_index[1]] is None:
                    token = tokenbag.tokens.pop(0)
                    self.board_gems[double_index[0]][double_index[1]] = token
        for i in range(len(self.board_gems)):
            for j in range(len(self.board_gems[i])):
                if isinstance(self.board_gems[i][j], Token):
                    image = Image(source=self.board_gems[i][j].image, fit_mode='cover')
                    self.add_widget(image)
                else:
                    label = Label()
                    self.add_widget(label)

    def draw_tokens(self, indices=None):
        """
        Remove from the board the tokens corresponding to the indices given
        """
        drawn_tokens = {}
        for token_index in indices:
            drawn_tokens = dict(Counter(drawn_tokens) + Counter({self.board_gems[token_index[0]][token_index[1]]: 1}))
            self.board_gems[token_index[0]][token_index[1]] = None

        return drawn_tokens

    def __str__(self):
        return f'{self.board_gems}'
