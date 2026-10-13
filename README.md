# Python Maze Solver
A simple python program that generates a maze and solves it.
Uses `tkinter` to display the maze.

## Usage
Edit `main.py` to modify the window size and the displayed maze.

The `Maze` class takes the following parameters:
- `x1` - x-coordinate of the top-left corner of the maze
- `y1` - y-coordinate of the top-left corner of the maze
- `num_rows` - number of rows in the maze
- `num_cols` - number of columns in the maze
- `cell_size_x` - width of each cell in pixels
- `cell_size_y` - height of each cell in pixels
- `win` - the window to display the maze in
- `seed` - the seed for the random number generator

The `Window` class takes the following parameters:
- `width` - width of the window in pixels
- `height` - height of the window in pixels

Then, run `main.py`.
```
python3 main.py
```
