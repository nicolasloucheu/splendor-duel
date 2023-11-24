from kivy.clock import Clock
from kivy.graphics import Rectangle, Color
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout

from models.unit.token import Token, GemType
from models.unit.tokenbag import TokenBag


def find_index(target_value, matrix):
    for row_index, row in enumerate(matrix):
        try:
            column_index = row.index(target_value)
        except ValueError:
            continue
        yield row_index, column_index


def find_common_elements(*lists_with_board):
    lists = lists_with_board[1:]
    if not lists:
        return []

    # Convert each list to a set
    sets = [set(lst) for lst in lists]

    # Find the intersection of all sets
    common_elements = set.intersection(*sets)

    return list(common_elements)


def get_opposite_diagonal(cell1, cell2):
    row1, col1 = cell1
    row2, col2 = cell2

    opposite1 = (row1 - (row2 - row1), col1 - (col2 - col1))
    opposite2 = (row2 + (row2 - row1), col2 + (col2 - col1))

    return opposite1, opposite2


class ImageButton(ButtonBehavior, Image):
    def __init__(self, row, col, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        self.current_size = self.size
        self.row = row
        self.col = col

    def on_press(self):
        current_cell = (self.row, self.col)
        current_gemtype = self.parent.board_gems[self.row][self.col].gem_type

        if current_cell in self.parent.clicked_cells:
            if len(self.parent.clicked_cells) == 3:
                cells = zip(*self.parent.clicked_cells)
                middle_cell = tuple(sum(coord) // 3 for coord in cells)

                if current_cell != middle_cell:
                    click_index = self.parent.clicked_cells.index(current_cell)
                    del self.parent.clicked_cells[click_index]
                    del self.parent.clicked_cells_gemtype[click_index]
            else:
                click_index = self.parent.clicked_cells.index(current_cell)
                del self.parent.clicked_cells[click_index]
                del self.parent.clicked_cells_gemtype[click_index]

        elif current_cell in self.parent.not_clickable_cells_index or current_gemtype == GemType.ANY:
            pass
        else:
            self.parent.clicked_cells.append(current_cell)
            self.parent.cell_size = self.size
            self.parent.width_confirm_cell = self.parent.cell_size[0] * .4
            self.parent.height_confirm_cell = self.parent.cell_size[1] * .4
            self.parent.clicked_cells_gemtype.append(self.parent.board_gems[self.row][self.col])

        self.parent.update_board()


class Board(RelativeLayout):
    board_gems = None
    clicked_cells = []
    clicked_cells_gemtype = []
    cell_size = (0, 0)
    not_clickable_cells_pos = []
    not_clickable_cells_index = []

    width_confirm_cell = .4 * cell_size[0]
    height_confirm_cell = .4 * cell_size[1]

    confirm_pos = None

    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        self.bind(size=self.on_window_resize)
        self.cols = 5
        self.rows = 5
        self.tokenbag = TokenBag()
        self.index_board = [
            [21, 22, 23, 24, 25],
            [20, 7, 8, 9, 10],
            [19, 6, 1, 2, 11],
            [18, 5, 4, 3, 12],
            [17, 16, 15, 14, 13]
        ]
        self.board_gems = [[Token(gem_type=GemType.ANY)] * 5 for _ in range(5)]
        self.fill(self.tokenbag)

        self.cell_size = (self.width / self.cols, self.height / self.rows)

    def fill(self, tokenbag=None):
        for current_position in range(1, 26):
            if tokenbag.get_number_of_tokens_in_bag() > 0:
                matches = [match for match in find_index(current_position, self.index_board)]
                double_index = list(matches[0])
                if self.board_gems[double_index[0]][double_index[1]].gem_type == GemType.ANY:
                    token = tokenbag.tokens.pop(0)
                    self.board_gems[double_index[0]][double_index[1]] = token
        self.update_board()

    def update_board(self, *args):
        self.clear_widgets()
        self.draw_board()
        self.color_clicked_cells()
        self.generate_not_clickable_cells()
        self.color_not_clickable_cells()
        if len(self.clicked_cells) > 0:
            self.get_confirmation_index()
            self.add_confirmation_to_pick()

    def draw_board(self):
        for row in range(len(self.board_gems)):
            for col in range(len(self.board_gems[row])):
                if isinstance(self.board_gems[row][col], Token):
                    image = ImageButton(
                        row=row,
                        col=col,
                        source=Token(self.board_gems[row][col].gem_type).image,
                        fit_mode='cover'
                    )
                    image.size_hint = (None, None)
                    image.size = (self.width / self.cols, self.height / self.rows)
                    image.pos = (col * image.width, (self.rows - 1 - row) * image.height)
                    self.add_widget(image)

    def color_clicked_cells(self):
        for clicked_cell in self.clicked_cells:
            cell_pos_x = clicked_cell[1] * self.cell_size[0]
            cell_pos_y = (4 - clicked_cell[0]) * self.cell_size[1]
            with self.canvas:
                Color(0, 1, 0, .5, mode='rgba')
                Rectangle(pos=(cell_pos_x, cell_pos_y), size=self.cell_size)

    def color_not_clickable_cells(self):
        for coord_to_darken in self.not_clickable_cells_pos:
            with self.canvas:
                Color(0, 0, 0, .5, mode='rgba')
                Rectangle(pos=coord_to_darken, size=self.cell_size)

    def generate_not_clickable_cells(self):
        self.not_clickable_cells_pos = []
        self.not_clickable_cells_index = []
        if len(self.clicked_cells) == 1:
            if self.clicked_cells_gemtype[0].gem_type == GemType.GOLD:
                self.generate_not_clickable_cells_one_selected_gold()
            else:
                self.generate_not_clickable_cells_one_selected()
        elif len(self.clicked_cells) == 2:
            self.generate_not_clickable_cells_two_selected()
        elif len(self.clicked_cells) == 3:
            self.generate_not_clickable_cells_three_selected()

    def generate_not_clickable_cells_one_selected(self):
        clicked_cell = self.clicked_cells[0]
        for possible_row in range(5):
            for possible_col in range(5):
                # If the cell it at more than one cell than the clicked one
                # Or the cell is a Gold token
                # Or the cell is empty
                if (
                        abs(clicked_cell[0] - possible_row) > 1 or abs(clicked_cell[1] - possible_col) > 1 or
                        self.board_gems[possible_row][possible_col].gem_type == GemType.GOLD or
                        self.board_gems[possible_row][possible_col].gem_type == GemType.ANY
                ):
                    cell_pos_x = possible_col * self.cell_size[0]
                    cell_pos_y = (4 - possible_row) * self.cell_size[1]

                    self.not_clickable_cells_pos.append((cell_pos_x, cell_pos_y))
                    self.not_clickable_cells_index.append((possible_row, possible_col))

    def generate_not_clickable_cells_one_selected_gold(self):
        clicked_cell = self.clicked_cells[0]
        for possible_row in range(5):
            for possible_col in range(5):
                if possible_row != clicked_cell[0] or possible_col != clicked_cell[1]:
                    cell_pos_x = possible_col * self.cell_size[0]
                    cell_pos_y = (4 - possible_row) * self.cell_size[1]

                    self.not_clickable_cells_pos.append((cell_pos_x, cell_pos_y))
                    self.not_clickable_cells_index.append((possible_row, possible_col))

    def generate_not_clickable_cells_two_selected(self):
        clicked_one = self.clicked_cells[0]
        clicked_two = self.clicked_cells[1]
        possible_clicks = []

        # If the two clicks are in a vertical line
        if clicked_one[1] == clicked_two[1]:
            possible_clicks.append((min(clicked_one[0], clicked_two[0]) - 1, clicked_one[1]))
            possible_clicks.append((max(clicked_one[0], clicked_two[0]) + 1, clicked_one[1]))
        # If the two clicks are in a horizontal line
        if clicked_one[0] == clicked_two[0]:
            possible_clicks.append((clicked_one[0], min(clicked_one[1], clicked_two[1]) - 1))
            possible_clicks.append((clicked_one[0], max(clicked_one[1], clicked_two[1]) + 1))
        else:
            opposites = get_opposite_diagonal(clicked_one, clicked_two)
            for cell in opposites:
                possible_clicks.append(cell)

        for possible_row in range(5):
            for possible_col in range(5):
                cell_position = (possible_col * self.cell_size[0], (4 - possible_row) * self.cell_size[1])
                cell_index = (possible_row, possible_col)

                # If the cell is not in the clicks that are authorized or that the Token is not a gold one
                # And if the cell is not clicked
                if ((
                        cell_index not in possible_clicks or
                        self.board_gems[possible_row][possible_col].gem_type == GemType.GOLD or
                        self.board_gems[possible_row][possible_col].gem_type == GemType.ANY
                ) and
                        cell_index not in self.clicked_cells):

                    self.not_clickable_cells_pos.append(cell_position)
                    self.not_clickable_cells_index.append(cell_index)

    def generate_not_clickable_cells_three_selected(self):
        for possible_row in range(5):
            for possible_col in range(5):
                if (possible_row, possible_col) not in self.clicked_cells:
                    cell_pos_x = possible_col * self.cell_size[0]
                    cell_pos_y = (4 - possible_row) * self.cell_size[1]
                    self.not_clickable_cells_pos.append((cell_pos_x, cell_pos_y))
                    self.not_clickable_cells_index.append((possible_row, possible_col))

    def get_confirmation_index(self):
        righteous_cell = [0, 0]
        for cell in self.clicked_cells:
            if cell[1] >= righteous_cell[1]:
                righteous_cell = cell
        if righteous_cell[1] == 4:
            still_going_left = True
            y_index_empty = 0
            while still_going_left:
                if (righteous_cell[0], righteous_cell[1] - y_index_empty) in self.clicked_cells:
                    y_index_empty += 1
                else:
                    still_going_left = False
            confirm_x = (righteous_cell[1] - y_index_empty + 1) * self.cell_size[0] - self.width_confirm_cell
            confirm_y = (4 - righteous_cell[0]) * self.cell_size[1]
            self.confirm_pos = (confirm_x, confirm_y)
        else:
            confirm_x = (righteous_cell[1] * self.cell_size[0]) + self.cell_size[0]
            confirm_y = (4 - righteous_cell[0]) * self.cell_size[1]
            self.confirm_pos = (confirm_x, confirm_y)

    def add_confirmation_to_pick(self):
        with self.canvas:
            Color(1, 0, 0, 1, mode='rgba')
            confirmation_button = Button(
                pos=(self.confirm_pos[0], self.confirm_pos[1]),
                size_hint=(None, None),
                size=(self.width_confirm_cell, self.height_confirm_cell)
            )
            confirmation_button.bind(on_press=self.confirmation_button_pressed)
            self.add_widget(confirmation_button)

    def confirmation_button_pressed(self, instance):
        for position in self.clicked_cells:
            self.board_gems[position[0]][position[1]].gem_type = GemType.ANY

        self.not_clickable_cells_pos = []
        self.not_clickable_cells_index = []
        self.clicked_cells = []
        self.clicked_cells_gemtype = []
        self.confirm_pos = None
        self.update_board()

    def on_window_resize(self, instance, value):
        Clock.schedule_once(self.update_board, 0)

    def __str__(self):
        return f'{self.board_gems}'
