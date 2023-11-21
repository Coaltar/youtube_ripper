import random
import os

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def initialize_board(size=4):
    board = [[0] * size for _ in range(size)]
    add_new_tile(board)
    add_new_tile(board)
    return board

def add_new_tile(board):
    empty_cells = [(i, j) for i in range(len(board)) for j in range(len(board[0])) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = 2 if random.random() < 0.9 else 4

def print_board(board):
    for row in board:
        print(' '.join(map(str, row)))

def slide(row):
    new_row = [0] * len(row)
    index = 0
    for value in row:
        if value != 0:
            new_row[index] = value
            index += 1
    return new_row

def merge(row):
    for i in range(len(row) - 1):
        if row[i] == row[i + 1] and row[i] != 0:
            row[i] *= 2
            row[i + 1] = 0
    return row

def move_left(board):
    new_board = []
    for row in board:
        new_row = slide(row)
        new_row = merge(new_row)
        new_row = slide(new_row)
        new_board.append(new_row)
    return new_board

def move_right(board):
    reversed_board = [row[::-1] for row in board]
    new_board = move_left(reversed_board)
    return [row[::-1] for row in new_board]

def move_up(board):
    transposed_board = [list(x) for x in zip(*board)]
    new_board = move_left(transposed_board)
    return [list(x) for x in zip(*new_board)]

def move_down(board):
    transposed_board = [list(x) for x in zip(*board)]
    new_board = move_right(transposed_board)
    return [list(x) for x in zip(*new_board)]

def is_game_over(board):
    for row in board:
        if 0 in row:
            return False
    for col in zip(*board):
        if 0 in col:
            return False
    return True

def main():
    size = 4
    board = initialize_board(size)

    while True:
        clear_screen()
        print_board(board)

        if is_game_over(board):
            print("Game Over!")
            break

        move = input("Enter move (W/A/S/D): ").upper()

        if move == 'W':
            board = move_up(board)
        elif move == 'A':
            board = move_left(board)
        elif move == 'S':
            board = move_down(board)
        elif move == 'D':
            board = move_right(board)
        else:
            print("Invalid move. Please use W/A/S/D.")

        add_new_tile(board)

if __name__ == "__main__":
    main()
