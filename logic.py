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
        if player == 'X':
            return 'O'
        else:
            return 'X'

    def get_winner(self):
        # Check rows
        for row in self.grid:
            if row[0] == row[1] == row[2] and row[0] is not None:
                return row[0]

        # Check columns
        for col in range(3):
            if self.grid[0][col] == self.grid[1][col] == self.grid[2][col] and self.grid[0][col] is not None:
                return self.grid[0][col]

        # Check diagonals
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] and self.grid[0][0] is not None:
            return self.grid[0][0]
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] and self.grid[0][2] is not None:
            return self.grid[0][2]

        return None

    def get_empty_squares(self):
        return [(i, j) for i in range(3) for j in range(3) if self.grid[i][j] is None]

class RandomBot:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        available_squares = board.get_empty_squares()
        return random.choice(available_squares) if available_squares else None
