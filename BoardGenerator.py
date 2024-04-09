import random
from Utils import is_valid_at_position


def place_number(grid, row, column):
    # If we have made it to the first out of bounds position then we've filled the board
    if row > 8 or column > 8:
        print("r", row, "c", column)
        return True
    
    # Get list of numbers that are not already placed in the same row, column, and/or box as the new coordinates
    valid_list = [num for num in range(1,10) if is_valid_at_position(grid, row, column, num)]
    
    # Randomize the order of the list so that we get a different sudoku board each time
    random.shuffle(valid_list)

    # Set the next indicies for the next row and column
    if column < 8:
        next_row = row
        next_column = column + 1
    else:
        next_row = row + 1
        next_column = 0
    
    for num in valid_list:
        grid[row][column] = num # place a number
        isGood = place_number(grid, next_row, next_column) # call place number for the next position
        if isGood:
            return True # If it returned true return true
        else:
            grid[row][column] = None # Otherwise set the current position to None
    return False # If we could not place any number, return false

def generate_completed_sudoku_board():
    # Create a 9x9 list populated with 0
    board = [[0 for _ in range(9)] for _ in range(9)]
    place_number(board, 0, 0)
    return board

# Needs changed to go through every box (remove a roughly even amount from every box equal to avg_hint_count)
def leave_hints(grid, avg_hints_per_box):
    avg_hints_per_box = min(max(0, avg_hints_per_box), 9) # keep within range of # of cells in a grid
    # Calculate the starting column and row of the 3x3 box containing the given cell
    for start_row in range(0, 9, 3):
        for start_column in range(0, 9, 3):
            # Loop through the 3x3 box containing the cell
            for i in range(start_row, start_row + 3):
                for j in range(start_column, start_column + 3):
                    n = random.randint(0, 9)
                    should_clear =  n > avg_hints_per_box
                    if should_clear:
                       grid[i][j] = 0

def generate_sudoku_board(avg_hints_per_box):
    board = generate_completed_sudoku_board()
    leave_hints(board, avg_hints_per_box)
    return board
