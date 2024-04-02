import json
# Load file
# Accepts a path
# Returns a dictionary
def load(path):
    f = open(path, "r")
    data = json.load(f)
    f.close()
    return json.loads(data)

# Save file
# Accepts a path and dictionary
def save(path, data):
    json_object = json.dumps(data, indent=4)
    f = open(path, "w")
    f.write(json_object)
    f.close()

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


if __name__ == "__main__":
    import random

    # Create a 9x9 list populated with random numbers between 1 and 100
    nine_by_nine_list = [[random.randint(1, 100) for _ in range(9)] for _ in range(9)]
    for row in nine_by_nine_list:
        for value in row:
            print(f"{value:3d}", end=" ")
        print()
    while True:
        row = int(input("Enter a row: "))
        column = int(input("Enter a column: "))
        num = int(input("Enter a number: "))
        print("Is in row:", in_row(nine_by_nine_list, row, num))
        print("Is in box:", in_column(nine_by_nine_list, column, num))
        print("Is in box:", in_box(nine_by_nine_list, row, column, num))
