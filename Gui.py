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
    "selected": (255, 0, 255),
    "cube_text": (0, 0, 0),
    "cube_temp_text": (50, 50, 255),
    "cube_entry_text": (255, 0, 255)
}

NIGHT_MODE_COLORS = {
    "background": (0, 0, 0),
    "grid_lines": (255, 255, 255),
    "super_text": (255,0,0),
    "text": (255, 255, 255),
    "selected": (255, 0, 255),
    "cube_text": (255, 255, 255),
    "cube_temp_text": (100, 100, 255),
    "cube_entry_text": (255, 0, 255)
}

def toggle_night_mode(win, board, night_mode):
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
    redraw_window(win, board, colors)
    pygame.display.update()

    return not night_mode # Return the new mode

def display_message(win, colors, message):
    win.fill(colors["background"])
    font = pygame.font.SysFont("cambria", 40)
    message_text = font.render(message, True, colors["super_text"])
    win.blit(message_text, (win.get_width() // 2 - message_text.get_width() // 2, win.get_height() // 2 - message_text.get_height() // 2))
    pygame.display.update()


class Grid:
    def __init__(self, win, rows, cols, width, height, loadFile, difficulty, bestTime = -1):
        self.win = win
        self.rows = rows
        self.cols = cols
        self.loadFile = loadFile
        self.currentTime = time.time()
        self.bestTime = bestTime

        if loadFile:
            self.board, self.backupBoard, self.bestTime, self.currentTime = load("board.json")
        
        if not loadFile or self.board == None:
            self.board = generate_sudoku_board(difficulty)
            self.backupBoard = [row[:] for row in self.board]
            
            save("board.json", self.board, self.backupBoard, self.bestTime, self.currentTime)

        self.cubes = [[Cube(self.board[r][c], r, c, width, height, self.backupBoard) for c in range(cols)] for r in range(rows)]
        self.width = width
        self.height = height
        self.selected = None

    def set_time(self, time):
        self.currentTime = time

    def get_time(self):
        return self.currentTime

    def set_bestTime(self, time):
        self.bestTime = time

    def get_bestTime(self):
        return self.bestTime

    def reset(self):
        self.board = [row[:] for row in self.backupBoard]
        for row in range(len(self.cubes)):
            for column in range(len(self.board[row])):
                self.cubes[row][column].set(self.board[row][column])
                self.cubes[row][column].set_temp(0)
        save("board.json", self.board, self.backupBoard, self.currentTime, self.bestTime)
        
    def reset_cube(self,row,column):
        self.board[row][column]=self.backupBoard[row][column]
        self.cubes[row][column].set(self.board[row][column])
        save("board.json", self.board, self.backupBoard, self.currentTime, self.bestTime)
        print("reset: ["+ str(column+1)+","+str(row+1)+"]")


    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.board[row][col] = val
            print("Placement: ["+ str(col+1)+","+str(row+1)+"]")

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win, colors):
        # Calculate the size of each cube and the gap as a percentage of the window's size
        cube_size = min(win.get_width(), win.get_height()) * 0.1 
        gap = cube_size // 10 

        # Calculate the starting position to center the grid
        start_x = (win.get_width() - (9 * cube_size + 8 * gap)) // 2
        start_y = (win.get_height() - (9 * cube_size + 8 * gap)) // 2

        # Draw Grid Lines
        for i in range(self.rows + 1):
            if i % 3 != 0:
                thick = 6
                pygame.draw.line(win, colors["grid_lines"], (start_x, start_y + i * (cube_size + gap)), (start_x + 9 * (cube_size + gap), start_y + i * (cube_size + gap)), thick)
                pygame.draw.line(win, colors["grid_lines"], (start_x + i * (cube_size + gap), start_y), (start_x + i * (cube_size + gap), start_y + 9 * (cube_size + gap)), thick)
        for i in range(self.rows + 1):   
            if i % 3 == 0:
                thick = 10
                pygame.draw.line(win, colors["cube_temp_text"], (start_x, start_y + i * (cube_size + gap)), (start_x + 9 * (cube_size + gap), start_y + i * (cube_size + gap)), thick)
                pygame.draw.line(win, colors["cube_temp_text"], (start_x + i * (cube_size + gap), start_y), (start_x + i * (cube_size + gap), start_y + 9 * (cube_size + gap)), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                x = start_x + j * (cube_size + gap)
                y = start_y + i * (cube_size + gap)
                self.cubes[i][j].draw(win, colors, x, y, cube_size, gap, i, j)

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
        cube_size = min(self.win.get_width(), self.win.get_height()) * 0.1
        gap = cube_size // 10 

        # Calculate the starting position to center the grid
        start_x = (self.win.get_width() - (9 * cube_size + 8 * gap)) // 2
        start_y = (self.win.get_height() - (9 * cube_size + 8 * gap)) // 2

        if pos[0] < start_x or pos[0] > start_x + 9 * (cube_size + gap) or pos[1] < start_y or pos[1] > start_y + 9 * (cube_size + gap):
            return None

        gap = cube_size // 10 
        x = (pos[0] - start_x) // (cube_size + gap)
        y = (pos[1] - start_y) // (cube_size + gap)
        return int(y), int(x)
    
    def is_finished(self):
        #checks if there are no empty spaces
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True
    
    def is_solved(self):
        """
        Check if the Sudoku board is completely solved according to the rules of Sudoku.
        Returns True if the board is solved, False otherwise.
        """
        # Check rows
        for row in self.board:
            if len(set(row))!= 9 or 0 in row:
                return False

        # Check columns
        for col in zip(*self.board):
            if len(set(col))!= 9 or 0 in col:
                return False

        # Check 3x3 sub-grids
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                sub_grid = [self.board[x][y] for x in range(i, i + 3) for y in range(j, j + 3)]
                if len(set(sub_grid))!= 9 or 0 in sub_grid:
                    return False

        return True

class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height, backupBoard):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
        self.backupBoard=backupBoard

    def draw(self, win, colors, x, y, size, gap, i, j):
            fnt = pygame.font.SysFont("cambria", 60)
            

            if self.temp != 0 and self.value == 0:
                text = fnt.render(str(self.temp), 1, colors["cube_temp_text"])
                win.blit(text, (x + 5, y + 5))
            elif self.value!=0 and self.backupBoard[i][j]!=self.value:
               text = fnt.render(str(self.value), 1, colors["cube_entry_text"])
               win.blit(text, (x + (size / 2 - text.get_width() / 2), y + (size / 2 - text.get_height() / 2)))
            elif self.value != 0:
                text = fnt.render(str(self.value), 1, colors["cube_text"])
                win.blit(text, (x + (size / 2 - text.get_width() / 2), y + (size / 2 - text.get_height() / 2)))
            

            if self.selected:
                #this draws the red rectangle 
                pygame.draw.rect(win, colors["selected"], (x, y, size+gap, size+gap), 7)

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


def time_from_units(sec, minute, hour):
    return ((hour * 60) + (minute * 60) + sec)


def get_time_units(secs):
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60
    return sec, minute, hour


def format_time(secs):
    sec, minute, hour = get_time_units(secs)

    if sec<10 and hour>=1:
        mat = " "+ str(hour) + ":" + str(minute-(60*hour)) + ":0" + str(sec)
    elif sec<10:
        mat = " " + str(minute-(60*hour)) + ":0" + str(sec)
    elif hour>=1:
        mat=" "+ str(hour) + ":" + str(minute-(60*hour)) + ":" + str(sec)
    else:
        mat = " " + str(minute-(60*hour)) + ":" + str(sec)

    return mat


def redraw_window(win, board, colors):
    win.fill(colors["background"])
    # Draw time
    fnt = pygame.font.SysFont("cambria", 40)

    text = fnt.render("Time: " + format_time(board.get_time()), 1, colors["text"])
    text_rect = text.get_rect()
    text_rect.topright = (win.get_width() - 30, 20) # Position at the top right
    win.blit(text, text_rect)
    
    if board.get_bestTime() != -1:
        text = fnt.render("Best Time: " + format_time(board.get_bestTime()), 1, colors["text"])
        text_rect = text.get_rect()
        text_rect.topright = (win.get_width() - 30, 60) # Position at the top right
        win.blit(text, text_rect)   

    # Draw grid and board
    board.draw(win, colors)

    # Help text
    # Calculate the size of each cube and the gap as a percentage of the window's size
    cube_size = min(win.get_width(), win.get_height()) * 0.1 
    gap = cube_size // 10 

    # Calculate the starting position to center the grid
    start_x = (win.get_width() - (9 * cube_size + 8 * gap)) // 2
    start_y = (win.get_height() - (9 * cube_size + 8 * gap)) // 2

    # Calculate the rectangle position to be to the left of the grid
    rect_x = start_x - 200 
    rect_y = start_y # Position it at the same y as the grid
    rect_width = 185
    rect_height = 240

    pygame.draw.rect(win, colors["grid_lines"], pygame.Rect(rect_x, rect_y, rect_width, rect_height), 2)

    # Render and position the "n=Night Mode" text
    fnt = pygame.font.SysFont("cambria", 20)

    options = [
        ("n = Night Mode", 5),
        ("CTRL+r = Reset", 30),
        ("CTRL+c = Check", 55),
        ("--------------------",80),
        ("difficulty settings",92),
        ("--------------------",104),
        ("CTRL+v = Very Easy", 129),
        ("CTRL+e = Easy", 154),
        ("CTRL+m = Medium", 179),
        ("CTRL+h = Hard", 204)

    ]

    for option_text, offset in options:
        text = fnt.render(option_text, 1, colors["text"])
        text_rect = text.get_rect()
        text_rect.left = rect_x + 5
        text_rect.top = rect_y + offset
        win.blit(text, text_rect)

