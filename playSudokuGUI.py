# GUI for playing and solving Sudoku puzzles
import pygame

from sudokuSolver import gen_rand_board, solve, print_board, is_valid, search_empty
from copy import deepcopy
import time

pygame.font.init()

# Window
WIN_WIDTH = 540
WIN_HEIGHT = 600
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# Board
BOARD_WIDTH = WIN_WIDTH
BOARD_HEIGHT = WIN_HEIGHT

# Squares
CUBE_WIDTH = CUBE_HEIGHT = 540

# Solve Button
SOLVE_X = BOARD_WIDTH/45
SOLVE_Y = BOARD_HEIGHT - CUBE_WIDTH / 11
SOLVE_WIDTH = 140
SOLVE_HEIGHT = 40

# Misc
BLACK = (0, 0, 0)
LIGHT_GRAY = (211, 211, 211)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
SELECTED_COLOR = GRAY
GAME_FONT = "timesnewroman"
GAME_FONT_SIZE = 25


class Board:
    def __init__(self):
        self.rows = self.columns = 9  # Board is always square
        self.width = BOARD_WIDTH
        self.height = BOARD_HEIGHT
        self.board = gen_rand_board()
        self.solution = deepcopy(self.board)
        solve(self.solution)
        self.squares = [[Square(self.board[i][j], i, j) for i in range(self.rows)] for j in range(self.columns)]
        self.model = None
        self.current_square = None

    def draw_squares(self, win):
        for i in range(self.rows):
            for j in range(self.columns):
                self.squares[i][j].draw(win)
        return True

    def draw_lines(self, win):
        gap = self.width / 9
        for i in range(self.rows+1):
            for j in range(self.columns):
                if i == 3 or i == 6:
                    r_line_thickness = 4
                else:
                    r_line_thickness = 1
                pygame.draw.line(win, BLACK, (0, gap * i), (BOARD_WIDTH, gap * i), r_line_thickness)

                if j % 3 == 0 and j != 0:
                    c_line_thickness = 4
                else:
                    c_line_thickness = 1
                pygame.draw.line(win, BLACK, (gap * j, 0), (gap * j, BOARD_HEIGHT - gap), c_line_thickness)

    def update_model(self):
        self.model = [[self.squares[i][j].value for i in range(self.rows) for j in range(self.columns)]]

    def set_preview(self, val):
        if self.current_square is not None:
            r, c = self.current_square
            self.squares[r][c].sketch = val

    def try_put(self, val):
        c, r = self.current_square  # row and column of selected square
        if self.board[r][c] == 0:
            self.board[r][c] = val
            self.squares[c][r].value = val

            if self.solution[r][c] == self.board[r][c]:
                return True
            else:
                self.squares[c][r].set(0)
                self.board[r][c] = 0
                self.update_model()
                return False

    def select_square(self, pos):
        r, c = pos  # pos is current square
        for i in range(self.rows):
            for j in range(self.columns):
                self.squares[i][j].is_selected = False

        self.squares[r][c].is_selected = True
        self.current_square = (r, c)

    def click(self, mouse_pos):
        width, height = mouse_pos
        if width < self.width and height < self.width:
            gap = self.width / 9
            row = width // gap
            col = height // gap
            print("Current square:  " + str(int(row)) + ", " + str(int(col)))
            return int(row), int(col)
        else:
            return False

    def solve_button_clicked(self, mouse_pos):
        x, y = mouse_pos
        return SOLVE_X <= x <= SOLVE_X + SOLVE_WIDTH and SOLVE_Y <= y <= SOLVE_Y + SOLVE_HEIGHT

    def solve_board(self, t):
        for event in pygame.event.get():
            if event == pygame.QUIT:
                exit()

        next_empty = search_empty(self.board)
        if not next_empty:
            print("Board solved!")
            print_board(self.board)
            return True

        r, c = next_empty

        for i in range(1, 10):
            if is_valid(self.board, i, (r, c)):
                self.board[r][c] = i
                self.squares[c][r].value = i
                self.update_model()
                draw_game(WIN, self, t)
                pygame.display.update()

                if self.solve_board(t):
                    return True

                self.board[r][c] = 0
                self.squares[c][r].value = 0
                self.update_model()
                draw_game(WIN, self, t)
                pygame.display.update()

    def is_complete(self):
        return not any(0 in sublist for sublist in self.board)


class Square:
    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.column = col
        self.width = CUBE_WIDTH
        self.height = CUBE_HEIGHT
        self.is_selected = False
        self.sketch = 0

    def draw(self, win):
        fnt = pygame.font.SysFont(GAME_FONT, GAME_FONT_SIZE)

        gap_size = self.width / 9
        x = self.column * gap_size
        y = self.row * gap_size

        if self.value != 0:
            displayed_val = fnt.render(str(self.value), True, BLACK)
            win.blit(displayed_val, (x + (gap_size / 2 - displayed_val.get_width() / 2),
                                     y + (gap_size / 2 - displayed_val.get_height() / 2)))

        if self.sketch != 0 and self.value == 0:
            displayed_val = fnt.render(str(self.sketch), True, GRAY)
            win.blit(displayed_val, (x + (gap_size / 2 - displayed_val.get_width() / 2),
                                     y + (gap_size / 2 - displayed_val.get_height() / 2)))

        if self.is_selected:
            pygame.draw.rect(win, SELECTED_COLOR, (x, y, gap_size, gap_size), 3)

    def set(self, val):
        self.value = val


def draw_game(win, board, t):
    win.fill(WHITE)

    time_font = pygame.font.SysFont(GAME_FONT, GAME_FONT_SIZE)
    time_text = time_font.render(display_time(t), True, BLACK)
    win.blit(time_text, (0.81 * BOARD_WIDTH, BOARD_HEIGHT - CUBE_WIDTH / 12))

    board.draw_lines(win)
    board.draw_squares(win)


def display_time(t):
    return time.strftime("%H:%M:%S", time.gmtime(t))


def create_solve_button(win):
    x, y = pygame.mouse.get_pos()
    properties = pygame.font.SysFont(GAME_FONT, GAME_FONT_SIZE)
    solve_text = properties.render("Solve", True, BLACK)

    if SOLVE_X <= x <= SOLVE_X + SOLVE_WIDTH and SOLVE_Y <= y <= SOLVE_Y + SOLVE_HEIGHT:  # if mouse hovers button
        button_color = GRAY
    else:
        button_color = LIGHT_GRAY
    pygame.draw.rect(win, button_color, [SOLVE_X, SOLVE_Y, SOLVE_WIDTH, SOLVE_HEIGHT])
    win.blit(solve_text, (SOLVE_X + 0.25 * SOLVE_WIDTH, SOLVE_Y + SOLVE_HEIGHT/8))
    pygame.display.update()


def main():
    pygame.display.set_caption("Sudoku")
    game_board = Board()
    if any(0 in sublist for sublist in game_board.solution):
        print("Error: Unsolvable board generated. Please rerun program.")
        exit()

    key = None
    run = True  # game over when false
    start = time.time()

    while run:
        current = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if game_board.solve_button_clicked(mouse_pos):
                    game_board.solve_board(current)
                clicked = game_board.click(mouse_pos)
                if clicked:
                    game_board.select_square(clicked)
                    key = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9

                if event.key == pygame.K_RETURN:
                    if key is not None and 1 <= key <= 9:
                        if game_board.try_put(key):
                            print("Correct!")
                        else:
                            print("Wrong!")
                        key = None

                        if game_board.is_complete():
                            print("Puzzle completed! Time: " + display_time(current))
                            run = False

        if game_board.current_square is not None and key is not None:
            game_board.set_preview(key)

        draw_game(WIN, game_board, current)
        create_solve_button(WIN)
        pygame.display.update()


if __name__ == "__main__":
    main()
    pygame.quit()
