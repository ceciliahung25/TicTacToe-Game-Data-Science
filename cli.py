# logic.py

import random
from datetime import datetime

class Board:
    def __init__(self):
        self.grid = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]
        self.game_log = []  # 新增的属性，用于记录游戏数据

    def reset_board(self):
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

    def record_move(self, player, row, col, start_time):
        # 在每一步完成后记录游戏数据
        end_time = datetime.now()
        elapsed_time = (end_time - start_time).total_seconds()  # 游戏用时（秒）

        # 获取游戏结果
        winner = self.get_winner()
        result = winner if winner is not None else 'Draw'  # 如果有赢家，使用赢家；否则，使用 'Draw'

        self.game_log.append({
            'player': player,
            'row': row,
            'col': col,
            'board': [row[:] for row in self.grid],  # 创建一个副本以防止引用问题
            'result': result,
            'elapsed_time': elapsed_time,
            'step': len(self.game_log),  # 步数即已记录的数据数量
        })

class RandomBot:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        available_squares = board.get_empty_squares()
        return random.choice(available_squares) if available_squares else None
