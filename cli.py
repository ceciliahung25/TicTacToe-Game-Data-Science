#cli.py

from logic import Board, RandomBot
import csv
import os
from datetime import datetime

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

def analyze_game_logs():
    df = pd.DataFrame(board.game_log)
    
    # 显示描述性统计信息
    print("Descriptive Statistics:")
    print(df.describe())

    # 显示每个结果的数量
    print("\nCount of each result:")
    print(df['result'].value_counts())

def linear_regression_analysis():
    df = pd.DataFrame(board.game_log)

    # 将位置转换为数值（角落: 0, 中间: 1, 边缘: 2）
    df['position'] = df.apply(lambda row: convert_position(row['row'], row['col']), axis=1)

    # 准备数据
    X = df[['position']]
    y = df['result'].apply(lambda result: 1 if result == first_player else 0)  # 1 表示获胜，0 表示其他

    # 创建线性回归模型
    model = LinearRegression()
    model.fit(X, y)

    # 报告模型拟合参数
    print("\nLinear Regression Model Fit Parameters:")
    print(f"Coefficient: {model.coef_[0]:.4f}")
    print(f"Intercept: {model.intercept_:.4f}")

def play_game(board):
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

        analyze_game_logs()  # 添加这一行，确保在每场游戏结束后提取描述性统计信息
        linear_regression_analysis()  # 添加这一行，确保在每场游戏结束后构建线性回归模型

if __name__ == '__main__':
    main()
