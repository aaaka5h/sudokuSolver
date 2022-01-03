import sudokuSolver
import numpy as np


# testing solve() on impossible board
rawImpossibleBoard = \
            [[0, 7, 0, 0, 2, 0, 0, 4, 6],
             [0, 6, 1, 0, 0, 0, 8, 9, 0],
             [2, 0, 0, 8, 0, 0, 7, 1, 5],

             [0, 8, 4, 0, 9, 7, 0, 0, 0],
             [7, 1, 0, 0, 0, 0, 0, 5, 9],
             [0, 0, 0, 1, 3, 0, 4, 8, 2],

             [6, 9, 7, 0, 0, 2, 0, 0, 8],
             [0, 5, 8, 0, 0, 0, 0, 6, 0],
             [4, 3, 0, 0, 8, 0, 0, 7, 0]]

impossibleBoard = np.array(rawImpossibleBoard)

# for testing validity of random board
exRandBoard = sudokuSolver.gen_rand_board()
sudokuSolver.print_board(exRandBoard)


def test_b_valid():
    assert(sudokuSolver.b_valid(sudokuSolver.testBoard, 5, (0, 5))), "Error: Should be valid"
    assert(sudokuSolver.b_valid(sudokuSolver.testBoard, 6, (0, 5))), "Error: Should be valid"
    assert not (sudokuSolver.b_valid(sudokuSolver.testBoard, 7, (2, 2))), "Error: Should not be valid"


def test_solve():
    assert(sudokuSolver.solve(sudokuSolver.testBoard)), "Error: Should be solvable"
    assert not (sudokuSolver.solve(impossibleBoard)), "Error: should not be solvable"


if __name__ == "__main__":
    test_b_valid()
    test_solve()
    print("All tests pass!")


