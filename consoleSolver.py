from sudokuSolver import print_board, solve, gen_rand_board, gen_empty_board, testBoard


def main(self):
    print_board(self)
    print("\nSolving...\n")
    if not solve(self):
        print("This puzzle has no solution.")
    else:
        solve(self)
        print_board(self)
        print("Solved!")


if __name__ == "__main__":
    print("\n")
    main(gen_rand_board())

