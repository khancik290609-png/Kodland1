import random

def create_zone(rows, cols):
    grid = [[1 for _ in range(cols)] for _ in range(rows)]
    col = random.randint(0, cols-1)
    for row in range(rows - 1, -1, -1):
        grid[row][col] = 0
        move = random.choice([-1, 0, 1])
        new_col = col + move
        if 0 <= new_col < cols:
            if new_col > col:
                grid[row][col+1]=0
            elif new_col < col:
                grid[row][col-1]=0
            
            col = new_col
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 0:
                grid[r][c] = random.choice([0, 1])
    return grid

def render_area(area, pos):
    symbols = {
    0: '\u2B1C',
    1: '\u2B1B',
    2: '🙂'
    }
    view = [row[:] for row in area]

    r, c = pos
    view[r][c] = 2

    text = ""
    for row in view:
        text += "\n" + "".join(symbols[cell] for cell in row) + "\n"

    return text