import random

class Board:
    def __init__(self):
        self.grid = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]

    def make_empty_board(self):
        self.grid = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]

    def other_player(self, player):
        return 'O' if player == 'X' else 'X'

    def get_winner(self):
        # Check rows
        for row in self.grid:
            if self.check_line(row):
                return row[0]

        # Check columns
        for col in range(3):
            if self.check_line([self.grid[row][col] for row in range(3)]):
                return self.grid[0][col]

        # Check diagonals
        if self.check_line([self.grid[i][i] for i in range(3)]):
            return self.grid[0][0]
        elif self.check_line([self.grid[i][2 - i] for i in range(3)]):
            return self.grid[0][2]

        return None

    def check_line(self, line):
        return all(cell == line[0] and cell is not None for cell in line)

    def get_empty_squares(self):
        return [(i, j) for i in range(3) for j in range(3) if self.grid[i][j] is None]

class RandomBot:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        available_squares = board.get_empty_squares()
        return random.choice(available_squares) if available_squares else None
