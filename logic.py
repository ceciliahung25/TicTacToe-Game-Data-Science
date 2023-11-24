# logic.py

import random

class Board:
    def __init__(self):
        self.grid = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]

    def other_player(self, player):
        return 'O' if player == 'X' else 'X'

    def make_move(self, player, row, col):
        if self.grid[row][col] is not None:
            raise ValueError("Selected spot is already occupied")
        self.grid[row][col] = player

    def get_winner(self):
        # Check rows
        for row in self.grid:
            if row.count('X') == 3:
                return 'X'
            elif row.count('O') == 3:
                return 'O'

        # Check columns
        for col in range(3):
            column = [self.grid[row][col] for row in range(3)]
            if column.count('X') == 3:
                return 'X'
            elif column.count('O') == 3:
                return 'O'

        # Check diagonals
        diagonal1 = [self.grid[i][i] for i in range(3)]
        diagonal2 = [self.grid[i][2 - i] for i in range(3)]

        if diagonal1.count('X') == 3:
            return 'X'
        elif diagonal1.count('O') == 3:
            return 'O'

        if diagonal2.count('X') == 3:
            return 'X'
        elif diagonal2.count('O') == 3:
            return 'O'

        return None

class RandomBot:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        available_squares = [(i, j) for i in range(3) for j in range(3) if board.grid[i][j] is None]
        return random.choice(available_squares) if available_squares else None
