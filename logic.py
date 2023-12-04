import random
from datetime import datetime

class Board:
    def __init__(self):
        self.grid = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]
        self.game_log = []  

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
        # 检查行
        for row in self.grid:
            if row[0] == row[1] == row[2] and row[0] is not None:
                return row[0]

        # 检查列
        for col in range(3):
            if self.grid[0][col] == self.grid[1][col] == self.grid[2][col] and self.grid[0][col] is not None:
                return self.grid[0][col]

        # 检查对角线
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] and self.grid[0][0] is not None:
            return self.grid[0][0]
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] and self.grid[0][2] is not None:
            return self.grid[0][2]

        return None

    def get_empty_squares(self):
        return [(i, j) for i in range(3) for j in range(3) if self.grid[i][j] is None]

    def record_move(self, player, row, col, start_time):
        end_time = datetime.now()
        elapsed_time = (end_time - start_time).total_seconds()  

        # 检查是否是第一步
        if len(self.game_log) == 0:
            first_player = player
        else:
            first_player = None

        self.game_log.append({
            'player': player,
            'row': row,
            'col': col,
            'board': [row[:] for row in self.grid],
            'result': self.get_winner(),
            'elapsed_time': elapsed_time,
            'step': len(self.game_log),
            'first_player': first_player,  # 新增字段，表示第一位玩家的移动
        })

    def record_draw(self, start_time):
        end_time = datetime.now()
        elapsed_time = (end_time - start_time).total_seconds()  
        self.game_log.append({
            'player': None,  
            'row': None,
            'col': None,
            'board': [row[:] for row in self.grid],  
            'result': None,  
            'elapsed_time': elapsed_time,
            'step': len(self.game_log),  
        })

    def convert_position(row, col):
    # 这是一个示例实现，你可以根据需要进行修改
        if (row, col) in [(0, 0), (0, 2), (2, 0), (2, 2)]:
            return 0  # 角落
        elif (row, col) == (1, 1):
            return 1  # 中间
        else:
            return 2  # 边缘

    
class RandomBot:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        available_squares = board.get_empty_squares()
        return random.choice(available_squares) if available_squares else None
