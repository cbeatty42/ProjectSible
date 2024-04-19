import pygame
import time
from BoardGenerator import *
from Utils import *
pygame.font.init()

# Define color schemes
DAY_MODE_COLORS = {
    "background": (255, 255, 255),
    "grid_lines": (0, 0, 0),
    "super_text": (255,0,0),
    "text": (0, 0, 0),
    "selected": (255, 0, 0),
    "cube_text": (0, 0, 0),
    "cube_temp_text": (50, 50, 255)
}

NIGHT_MODE_COLORS = {
    "background": (0, 0, 0),
    "grid_lines": (255, 255, 255),
    "super_text": (255,0,0),
    "text": (255, 255, 255),
    "selected": (255, 0, 0),
    "cube_text": (255, 255, 255),
    "cube_temp_text": (100, 100, 255)
}

def toggle_night_mode(win, board, time, strikes, night_mode):
    global DAY_MODE_COLORS, NIGHT_MODE_COLORS
    if night_mode:
        # Switch to day mode
        colors = DAY_MODE_COLORS
    else:
        # Switch to night mode
        colors = NIGHT_MODE_COLORS

    # Update colors in the board and redraw
    win.fill(colors["background"])
    board.draw(win, colors)
    redraw_window(win, board, time, strikes, colors)
    pygame.display.update()

    return not night_mode # Return the new mode

def display_game_over(win, colors):
    win.fill(colors["background"])
    font = pygame.font.SysFont("timesnewroman", 40)
    game_over_text = font.render('GAME OVER', True, colors["super_text"])
    win.blit(game_over_text, (win.get_width() // 2 - game_over_text.get_width() // 2, win.get_height() // 2 - game_over_text.get_height() // 2))
    pygame.display.update()



class Grid:
    #default board
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    def __init__(self, win, rows, cols, width, height, loadFile, difficulty):
        self.win=win
        self.rows = rows
        self.cols = cols
        self.loadFile=loadFile 

        if loadFile:
            self.board = load("board.json")
        else:
            self.board = generate_sudoku_board(difficulty)
            save("board.json", self.board)

        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row, col)) and solve(self.model):
                self.board[row][col] = val
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win, colors):
        # Calculate the size of each cube and the gap as a percentage of the window's size
        cube_size = min(win.get_width(), win.get_height()) * 0.1 # Adjust the 0.1 value to change the size of the grid
        gap = cube_size // 10 # Adjust the gap as needed

        # Calculate the starting position to center the grid
        start_x = (win.get_width() - (9 * cube_size + 8 * gap)) // 2
        start_y = (win.get_height() - (9 * cube_size + 8 * gap)) // 2

        # Draw Grid Lines
        for i in range(self.rows + 1):
            if i % 3== 0: #and i != 0:
                thick = 5
            else:
                thick = 3
            pygame.draw.line(win, colors["grid_lines"], (start_x, start_y + i * (cube_size + gap)), (start_x + 9 * (cube_size + gap), start_y + i * (cube_size + gap)), thick)
            pygame.draw.line(win, colors["grid_lines"], (start_x + i * (cube_size + gap), start_y), (start_x + i * (cube_size + gap), start_y + 9 * (cube_size + gap)), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                x = start_x + j * (cube_size + gap)
                y = start_y + i * (cube_size + gap)
                self.cubes[i][j].draw(win, colors, x, y, cube_size)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        # Calculate the size of each cube and the gap as a percentage of the window's size
        cube_size = min(self.win.get_width(), self.win.get_height()) * 0.1 # Adjust the 0.1 value to change the size of the grid
        gap = cube_size // 10 # Adjust the gap as needed

        # Calculate the starting position to center the grid
        start_x = (self.win.get_width() - (9 * cube_size + 8 * gap)) // 2
        start_y = (self.win.get_height() - (9 * cube_size + 8 * gap)) // 2

        if pos[0] < start_x or pos[0] > start_x + 9 * (cube_size + gap) or pos[1] < start_y or pos[1] > start_y + 9 * (cube_size + gap):
            return None

        gap = cube_size // 10 # Adjust the gap as needed
        x = (pos[0] - start_x) // (cube_size + gap)
        y = (pos[1] - start_y) // (cube_size + gap)
        return int(y), int(x)
    
    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win, colors, x, y, size):
            fnt = pygame.font.SysFont("timesnewroman", 40)

            if self.temp != 0 and self.value == 0:
                text = fnt.render(str(self.temp), 1, colors["cube_temp_text"])
                win.blit(text, (x + 5, y + 5))
            elif self.value != 0:
                text = fnt.render(str(self.value), 1, colors["cube_text"])
                win.blit(text, (x + (size / 2 - text.get_width() / 2), y + (size / 2 - text.get_height() / 2)))

            if self.selected:
                pygame.draw.rect(win, colors["selected"], (x, y, size, size), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def valid(board, number, position):
    # checking row
    for i in range(len(board[0])):
        if board[position[0]][i] == number and position[1] != i:
            return False

    # checking column
    for i in range(len(board)):
        if board[i][position[1]] == number and position[0] != i:
            return False

    # check which box  we are in
    box_x = position[1] // 3  # integer division
    box_y = position[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == number and (i, j) != position:
                return False

    return True


def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return i, j

    return None


def solve(board):
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    # filling values in empty spaces
    for i in range(1, 10):
        if valid(board, i, (row, col)):
            board[row][col] = i

            if solve(board):
                return True

            # backtrack the solution if the solution found doesn't satisfy condition later
            board[row][col] = 0

    return False


def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60

    mat = " " + str(minute) + ":" + str(sec)
    return mat


def redraw_window(win, board, time, strikes, colors):
    win.fill(colors["background"])
    # Draw time
    fnt = pygame.font.SysFont("timesnewroman", 40)
    text = fnt.render("Time: " + format_time(time), 1, colors["text"])
    text_rect = text.get_rect()
    text_rect.topright = (win.get_width() - 30, 20) # Position at the top right, adjust as needed
    win.blit(text, text_rect)
    # Draw Strikes (Code may not be used)

    text = fnt.render("X " * strikes, 1, colors["text"])
    text_rect = text.get_rect()
    text_rect.left = 20 # Adjust as needed
    text_rect.bottom = win.get_height() - 20 # Position at the bottom, adjust as needed
    win.blit(text, text_rect)
    # Draw grid and board
    board.draw(win, colors)

    # Help text
    # Calculate the size of each cube and the gap as a percentage of the window's size
    cube_size = min(win.get_width(), win.get_height()) * 0.1 # Adjust the 0.1 value to change the size of the grid
    gap = cube_size // 10 # Adjust the gap as needed

    # Calculate the starting position to center the grid
    start_x = (win.get_width() - (9 * cube_size + 8 * gap)) // 2
    start_y = (win.get_height() - (9 * cube_size + 8 * gap)) // 2

    # Calculate the rectangle position to be to the left of the grid
    rect_x = start_x - 200 # Adjust as needed to ensure it's to the left of the grid
    rect_y = start_y # Position it at the same y as the grid
    rect_width = 160
    rect_height = 240

    pygame.draw.rect(win, colors["grid_lines"], pygame.Rect(rect_x, rect_y, rect_width, rect_height), 2)

    # Render and position the "n=Night Mode" text
    fnt = pygame.font.SysFont("timesnewroman", 20)
    
    options = [
        ("n = Night Mode", 5),
        ("r = Refresh Board", 30),
        ("--------------------",42),
        ("difficulty settings",55),
        ("--------------------",67),
        ("v = very easy", 80),
        ("e = easy", 105),
        ("m = medium", 130),
        ("h = hard", 155)

    ]

    for option_text, offset in options:
        text = fnt.render(option_text, 1, colors["text"])
        text_rect = text.get_rect()
        text_rect.left = rect_x + 5
        text_rect.top = rect_y + offset
        win.blit(text, text_rect)



def main():
    colors = DAY_MODE_COLORS
    win = pygame.display.set_mode((0, 0),pygame.RESIZABLE)
    pygame.display.set_caption("Project Sible")
    difficulty=3
    board = Grid(win,9, 9, 540, 540, True, difficulty)
    key = None
    run = True
    
    start = time.time()
    strikes = 0
    night_mode=False

    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
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
                if event.key == pygame.K_BACKSPACE:
                    key=0
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            #strikes += 1
                        key = None

                        if board.is_finished():
                            print("Game over")
                            run = False
                            display_game_over(win, colors)
                            time.sleep(3) # Pause for 3 seconds before closing the window
                #use n key to set night mode
                if event.key == pygame.K_n:
                    night_mode = toggle_night_mode(win, board, play_time, strikes, night_mode)
                    if night_mode:
                        colors = NIGHT_MODE_COLORS
                    else:
                        colors = DAY_MODE_COLORS
                    redraw_window(win, board, play_time, strikes, colors)
                #use r key to reset board and time.
                if event.key==pygame.K_r:
                    board = Grid(win,9, 9, 540, 540, False, difficulty)
                    key = None
                    start = time.time()
                    strikes = 0
                #various keys are used to set the difficulty
                if event.key==pygame.K_h:
                    difficulty=2
                if event.key==pygame.K_m:
                    difficulty=3
                if event.key==pygame.K_e:
                    difficulty=4
                if event.key==pygame.K_v:
                    difficulty=5
                #arrow keys used to move around
                if event.key == pygame.K_LEFT:
                    if board.selected:
                        row, col = board.selected
                        key=None
                        if col > 0:
                            board.select(row, col - 1)
                    else:
                        board.select(4,3)
                if event.key == pygame.K_RIGHT:
                    if board.selected:
                        row, col = board.selected
                        key=None
                        if col < 8:
                            board.select(row, col + 1)
                    else:
                        board.select(4,5)
                if event.key == pygame.K_UP:
                    if board.selected:
                        row, col = board.selected
                        key=None
                        if row > 0:
                            board.select(row - 1, col)
                    else:
                        board.select(3,4)
                if event.key == pygame.K_DOWN:
                    if board.selected:
                        row, col = board.selected
                        key=None
                        if row < 8:
                            board.select(row + 1, col)
                    else:
                        board.select(5,4)
                #use esc key to force quit game
                if event.key==pygame.K_ESCAPE:
                    run=False


            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)

                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key is not None:
            board.sketch(key)
  

        redraw_window(win, board, play_time, strikes, colors)

        pygame.display.update()

    save("board.json", board.board)

main()
pygame.quit()