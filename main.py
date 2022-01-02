import sudokuSolver
from sudokuSolver import board


def main(self):
    sudokuSolver.solve(self)
    sudokuSolver.print_board(self)


if __name__ == "__main__":
    print("Solving...\n")
    main(board)
    print("\n")
    print("Solved!")
