# cli.py

from logic import Board, RandomBot
import csv
import os

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

def play_game(board):
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
                break
            elif all(cell is not None for row in board.grid for cell in row):
                print_board(board)
                print("It's a draw!")
                break
            else:
                player = board.other_player(player)
        else:
            print("Invalid input! Row and column must be 0, 1, or 2.")

    # 游戏结束后写入CSV文件
    write_csv(board.game_log)

def write_csv(game_log):
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
        writer.writerows(game_log)

def main():
    while True:
        board = Board()
        play_game(board)
        restart = input("Do you want to play again? (yes/no): ")
        if restart.lower() != 'yes':
            break

if __name__ == '__main__':
    main()
