# cli.py
import pandas as pd
from sklearn.linear_model import LinearRegression
from logic import Board, RandomBot
import csv
import os
from datetime import datetime
from sklearn.preprocessing import OneHotEncoder

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
    if (row, col) in [(0, 0), (0, 2), (2, 0), (2, 2)]:
        return 0  # Corner
    elif (row, col) == (1, 1):
        return 1  # Center
    else:
        return 2  # Edge

# 导入独热编码函数

def linear_regression_analysis(board):
    print("Entering linear_regression_analysis()...")
    df = pd.DataFrame(board.game_log)

    # Get the first player
    first_player = df['player'].iloc[0]

    # Convert position to numerical values (corner: 0, center: 1, edge: 2)
    df['position'] = df.apply(lambda row: convert_position(row['row'], row['col']), axis=1)

    # 使用独热编码
    encoder = OneHotEncoder(sparse=False, drop='first')  # drop='first' 用于避免共线性
    encoded_positions = encoder.fit_transform(df[['position']])
    encoded_positions_df = pd.DataFrame(encoded_positions, columns=['position_center', 'position_edge'])

    # 合并独热编码后的位置列到原始 DataFrame
    df = pd.concat([df, encoded_positions_df], axis=1)

    # Prepare data
    X = df[['position_center', 'position_edge']]
    y = df['result'].apply(lambda result: 1 if result == first_player else 0)

    # 创建线性回归模型
    model = LinearRegression()

    # 拟合模型
    model.fit(X, y)

    # 报告模型拟合参数
    print("\nLinear Regression Model Fit Parameters:")
    for feature, coef in zip(X.columns, model.coef_):
        print(f"{feature}: {coef:.4f}")
    print(f"Intercept: {model.intercept_:.4f}")

    # 预测每个位置的结果
    positions = [[0, 1], [1, 0], [0, 0]]  # 分别对应 center, edge, corner
    predictions = model.predict(positions)

    # 报告预测结果
    print("\nPredicted Outcomes for Each Position:")
    for pos, pred in zip(positions, predictions):
        print(f"Position (Center, Edge, Corner): {pos} - {pred:.4f}")

def play_game(board):
    print("Entering play_game()...")
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

