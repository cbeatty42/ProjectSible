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
    # Create a 9x9 list populated with None
    board = [[None for _ in range(9)] for _ in range(9)]
    place_number(board, 0, 0)
    return board

# Accepts a board and returns a duplicate board with values missing
def remove_numbers(board):
    new_board = board

    for y in range(9):
        count = 0
        for x in range(9):
            if random.randint(-1, 1) >= 0:
                new_board[y][x] = 0
                count += 1
                x += count
            
            if count > 5:
                break

    return new_board