# cli.py

import csv
import os
from datetime import datetime
from logic import Board, RandomBot

def print_board(board):
    for i, row in enumerate(board.grid):
        print(f"{i} | {' | '.join(cell if cell is not None else ' ' for cell in row)} |")
    print("   0   1   2")

def choose_player_type():
    while True:
        choice = input("Choose player type (1 for Human, 2 for RandomBot): ")
        if choice == '1':
            return 'X', 'Human'
        elif choice == '2':
            return 'O', 'RandomBot'
        else:
            print("Invalid choice. Please enter 1 or 2.")

# Updated write_game_log function for better debugging
def write_game_log(player_type, player_symbol, move_count, winner):
    log_file_path = 'logs/game_log.csv'

    # If the file does not exist, create the file and write the header
    if not os.path.exists(log_file_path):
        with open(log_file_path, 'w', newline='') as csvfile:
            fieldnames = ['Timestamp', 'Player Type', 'Player Symbol', 'Move Count', 'Winner']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    # Write the current game data to the file
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Check if there is already a winner to avoid duplicate entries
    if winner and winner != "Draw":
        with open(log_file_path, 'a', newline='') as csvfile:
            fieldnames = ['Timestamp', 'Player Type', 'Player Symbol', 'Move Count', 'Winner']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({
                'Timestamp': timestamp,
                'Player Type': player_type,
                'Player Symbol': player_symbol,
                'Move Count': move_count,
                'Winner': winner
            })

def main():
    board = Board()
    player_symbol, player_type = choose_player_type()
    move_count = 0

    # Create RandomBot instance outside the loop
    bot = RandomBot(player_symbol)

    while True:
        print_board(board)
        print(f"{player_type} Player {player_symbol}'s turn.")

        if player_type == 'Human':
            row = int(input("Enter the row (0, 1, or 2): "))
            col = int(input("Enter the column (0, 1, or 2): "))
        else:
            move = bot.get_move(board)
            if player_type == 'RandomBot':
                row, col = move

        if 0 <= row < 3 and 0 <= col < 3:
            if board.grid[row][col] is not None:
                print("That cell is already occupied! Try again.")
                continue

            board.grid[row][col] = player_symbol
            move_count += 1
            winner = board.get_winner()
            if winner:
                print_board(board)
                print(f"{player_type} Player {player_symbol} wins!")
                write_game_log(player_type, player_symbol, move_count, player_symbol)
                break
            elif all(cell is not None for row in board.grid for cell in row):
                print_board(board)
                print("It's a draw!")
                write_game_log(player_type, player_symbol, move_count, "Draw")
                break
            else:
                player_symbol = board.other_player(player_symbol)
        else:
            print("Invalid input! Row and column must be 0, 1, or 2.")

        # 添加额外的输入，清除输入缓冲
        input("Press Enter to continue...")

if __name__ == '__main__':
    main()
