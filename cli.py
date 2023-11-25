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
            writer
