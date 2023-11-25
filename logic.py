# logic.py

import csv
import os

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

    def record_move(self, player, row, col, result=None):
        move_info = {
            'player': player,
            'row': row,
            'col': col,
            'board': [row[:] for row in self.grid],
            'result': result
        }
        self.game_log.append(move_info)
        return move_info

    def write_csv(self):
        file_path = os.path.join('logs', 'game_log.csv')
        fieldnames = ['player', 'row', 'col', 'board', 'result']

        # 检查文件是否存在，如果不存在则写入表头
        if not os.path.exists(file_path):
            with open(file_path, mode='w', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()

        # 写入所有游戏日志数据
        with open(file_path, mode='a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerows(self.game_log)
