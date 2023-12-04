#cli.py

import sys
import pandas as pd
from logic import Board, RandomBot
import csv
import os
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

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

def convert_position(row, col):
    """
    将位置(row, col)转换为数值表示，角落: 0, 中间: 1, 边缘: 2
    """
    if (row, col) in [(0, 0), (0, 2), (2, 0), (2, 2)]:
        return 0  # 角落
    elif (row, col) == (1, 1):
        return 1  # 中间
    else:
        return 2  # 边缘

def analyze_game_logs(board):  # 添加 board 参数
    print("Entering analyze_game_logs()...")  # 调试输出
    df = pd.DataFrame(board.game_log)
    
    # 显示描述性统计信息
    print("Descriptive Statistics:")
    print(df.describe())

    # 显示每个结果的数量
    print("\nCount of each result:")
    print(df['result'].value_counts())





def linear_regression_analysis(board):
    print("Entering linear_regression_analysis()...")  # Debug output
    df = pd.DataFrame(board.game_log)

    # Get the first player
    first_player = df['player'].iloc[0]

    # Convert position to numerical values (corner: 0, center: 1, edge: 2)
    df['position'] = df.apply(lambda row: convert_position(row['row'], row['col']), axis=1)

    # Prepare data
    X = df[['position']]
    
    # Use LabelEncoder to convert string labels to integers
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df['result'])

    # Create a decision tree classifier model
    model = DecisionTreeClassifier()
    model.fit(X, y)

    # Report model fit parameters
    print("\nDecision Tree Classifier Model Fit Parameters:")
    # The decision tree classifier does not have coefficients, so we won't print them
    # If you want to visualize the tree, you can use plot_tree function from sklearn.tree
    print("Model trained successfully.")



def play_game(board):
    print("Entering play_game()...")  # 调试输出
    player = choose_player_type()
    start_time = datetime.now()  

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
            board.record_move(player, row, col, start_time)  
            winner = board.get_winner()
            if winner:
                print_board(board)
                print(f"Player {winner} wins!")
                break
            elif all(cell is not None for row in board.grid for cell in row):
                print_board(board)
                print("It's a draw!")
                board.record_draw(start_time)
                break
            else:
                player = board.other_player(player)
        else:
            print("Invalid input! Row and column must be 0, 1, or 2.")

    write_csv(board)
    analyze_game_logs(board)  # 传递 board 参数
    linear_regression_analysis(board)

def write_csv(board):
    file_path = os.path.join('logs', 'game_log.csv')
    fieldnames = ['player', 'row', 'col', 'board', 'result', 'elapsed_time', 'step', 'first_player']

    if not os.path.exists(file_path):
        with open(file_path, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

    with open(file_path, mode='a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writerows(board.game_log)

def main():
    while True:
        board = Board()
        play_game(board)
        restart = input("Do you want to play again? (yes/no): ")
        if restart.lower() != 'yes':
            break

if __name__ == '__main__':
    main()
