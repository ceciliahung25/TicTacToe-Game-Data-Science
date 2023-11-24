# cli.py

import csv
import os
from logic import Board, RandomBot

def print_board(board):
    for i, row in enumerate(board.grid):
        print(f"{i} | {' | '.join(cell if cell is not None else ' ' for cell in row)} |")
    print("   0   1   2")

def choose_player_type():
    while True:
        choice = input("Choose player type (1 for Human, 2 for RandomBot): ")
        if choice == '1':
            return 'X'
        elif choice == '2':
            return 'O'
        else:
            print("Invalid choice. Please enter 1 or 2.")

# 新增的函数，用于写入游戏数据到 CSV 文件
def write_game_log(player, winner):
    log_file_path = 'logs/game_log.csv'

    # 如果文件不存在，创建文件并写入标题
    if not os.path.exists(log_file_path):
        with open(log_file_path, 'w', newline='') as csvfile:
            fieldnames = ['Player', 'Winner']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    # 将当前游戏数据写入文件
    with open(log_file_path, 'a', newline='') as csvfile:
        fieldnames = ['Player', 'Winner']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'Player': player, 'Winner': winner})

def main():
    board = Board()
    player = choose_player_type()

    while True:
        print_board(board)
        print(f"Player {player}'s turn.")

        if player == 'X':
            row = int(input("Enter the row (0, 1, or 2): "))
            col = int(input("Enter the column (0, 1, or 2): "))
        else:
            bot = RandomBot(player)
            move = bot.get_move(board)
            row, col = move

        if 0 <= row < 3 and 0 <= col < 3:
            if board.grid[row][col] is not None:
                print("That cell is already occupied! Try again.")
                continue

            board.grid[row][col] = player
            winner = board.get_winner()
            if winner:
                print_board(board)
                print(f"Player {winner} wins!")
                write_game_log(player, winner)  # 将游戏数据写入 CSV 文件
                break
            elif all(cell is not None for row in board.grid for cell in row):
                print_board(board)
                print("It's a draw!")
                write_game_log(player, "Draw")  # 将游戏数据写入 CSV 文件
                break
            else:
                player = board.other_player(player)
        else:
            print("Invalid input! Row and column must be 0, 1, or 2.")

if __name__ == '__main__':
    main()
