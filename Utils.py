import json
# Load file
# Accepts a path
# Returns a dictionary
def load(path):
    try:
        f = open(path, "r")
        board_json = json.load(f)
        f.close()
        return board_json["board"], board_json["backupBoard"], board_json["bestTime"], board_json["currentTime"]
    except:
        return None, None, 0, 0

# Save file
# Accepts a path and dictionary
def save(path, board, backupBoard, bestTime, currentTime):
    with open(path, "w") as file:
        save_dictionary = {"board":board, "backupBoard":backupBoard, "bestTime":bestTime, "currentTime":currentTime}
        _ = json.dump(save_dictionary, file)
        file.close()

# Is in row
# Accepts 2 dimensional array and row number
# Zero indexed
def in_row(grid, row, num):
    return num in grid[row]

# Is in column
# Accepts 2 dimensional array and column number
# Zero indexed
def in_column(grid, column, num):
    for row in grid:
        if num == row[column]:
            return True
    
    return False

def in_box(grid, row, column, num):
    # Calculate the starting column and row of the 3x3 box containing the given cell
    start_column = (column // 3) * 3  # Find the highest multiple of 3 that is less than or equal to the column of the cell
    start_row = (row // 3) * 3  # Find the highest multiple of 3 that is less than or equal to the row of the cell

    # Loop through the 3x3 box containing the cell
    for i in range(start_row, start_row + 3):
        for j in range(start_column, start_column + 3):
            # Check if the current cell contains the given number
            if grid[i][j] == num:
                return True  # Return True if the number is found in the box
    
    return False  # Return False if the number is not found in the box

# Returns if the given number is valid for the row and column in the sudoku grid
# Must not have a duplicate in a row, column, or in the 3x3 box
def is_valid_at_position(grid, row, column, num):
    return not(in_row(grid, row, num) or in_column(grid, column, num) or in_box(grid, row, column, num))
