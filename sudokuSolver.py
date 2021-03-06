# we have a board with 9x9 size
# 0, 1, 2, 3, 4, 5, 6, 7, 8
import numpy as np

rawBoard = [[0, 7, 0, 0, 2, 0, 0, 4, 6],
            [0, 6, 0, 0, 0, 0, 8, 9, 0],
            [2, 0, 0, 8, 0, 0, 7, 1, 5],

            [0, 8, 4, 0, 9, 7, 0, 0, 0],
            [7, 1, 0, 0, 0, 0, 0, 5, 9],
            [0, 0, 0, 1, 3, 0, 4, 8, 0],

            [6, 9, 7, 0, 0, 2, 0, 0, 8],
            [0, 5, 8, 0, 0, 0, 0, 6, 0],
            [4, 3, 0, 0, 8, 0, 0, 7, 0]]

testBoard = np.array(rawBoard)


def gen_empty_board():
    board = [[0] * 9 for i in range(9)]
    board = np.array(board)
    return board


# WARNING: If taking too long to load rerun the program
def gen_rand_board():
    rand_board = gen_empty_board()
    for i in range(9):
        for j in range(9):
            empty_spot = np.random.choice([0, 1], 1, True, [0.75, 0.25])
            if empty_spot[0] == 0:
                rand_board[i][j] = 0
            else:
                rand_board[i][j] = rand_valid(rand_board, (i, j))
    return rand_board


# randomly generate a num [1-9], and check if it is valid in board at pos
def rand_valid(board, pos):
    num = np.random.choice(range(1, 10), 1, True, [1/9, 1/9, 1/9, 1/9, 1/9, 1/9, 1/9, 1/9, 1/9])
    while not is_valid(board, num[0], pos):
        num = np.random.choice(range(1, 10), 1, True, [1/9, 1/9, 1/9, 1/9, 1/9, 1/9, 1/9, 1/9, 1/9])
    else:
        return num[0]


# use backtracking to solve board
def solve(board):
    emp = search_empty(board)
    if not emp:
        return True
    else:
        r, c = emp  # i,j

    for i in range(1, 10):
        if is_valid(board, i, (r, c)):
            board[r][c] = i

            if solve(board):
                return True
            board[r, c] = 0

    return False


# True if num is valid at pos on board, else False
def is_valid(board, num, pos):
    return b_valid(board, num, pos) and rc_valid(board, num, pos)


# False if number present in box, else true
def b_valid(board, num, pos):
    r, c = pos
    box_x = c // 3
    box_y = r // 3  # floor division to get to top corner of box

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False
    return True


# False if number is present in row or column, else true
def rc_valid(board, num, pos):
    r, c = pos
    for i in range(9):
        if board[i][c] == num and i != r:
            return False

    for j in range(9):
        if board[r][j] == num and j != c:
            return False

    return True


# give coordinates of an empty spot on the given board
def search_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:  # if spot is empty
                return i, j
    return False


# prints board to console in sudoku format
def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ")
        for j in range(len(board)):
            if j == 3 or j == 6:
                print("| " + str(board[i][j]) + " ", end="")
            elif j == 8:
                print(str(board[i][j]))
            else:
                print(str(board[i][j]) + " ", end="")
