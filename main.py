import sudokuSolver
from sudokuSolver import testBoard


def main(self):
    sudokuSolver.print_board(self)
    print("\nSolving...\n")
    if not sudokuSolver.solve(self):
        print("This puzzle has no solution.")
    else:
        sudokuSolver.solve(self)
        sudokuSolver.print_board(self)


if __name__ == "__main__":
    print("\n")
    main(sudokuSolver.gen_rand_board())
    print("\nSolved!")

