import time
import random

from graphics import Window, Cell, Point, Line

class Maze: 
    def __init__(
      self,
      x1: int,
      y1: int,
      num_rows: int,
      num_cols: int,
      cell_size_x: float,
      cell_size_y: float,
      win: Window = None,
      seed = None
   ) -> None:
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        # 2-dim array in column-major order
        self.__cells = []

        if seed != None:
            random.seed(seed)
        

        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0,0)
        self.__reset_cells_visited()

        
    def __create_cells(self) -> None:
        # Add to list
        for i in range(self.__num_cols):
            cell_column = []
            for j in range(self.__num_rows):
                cell_column.append(Cell(self.__win,))
            self.__cells.append(cell_column)

        # Draw
        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__draw_cell(i, j)

    def __draw_cell(self,i,j):
        c_x1 = self.__x1 + self.__cell_size_x * (i)
        c_y1 = self.__y1 + self.__cell_size_y * (j)
        c_x2 = self.__x1 + self.__cell_size_x * (i + 1)
        c_y2 = self.__y1 + self.__cell_size_y * (j + 1)

        if self.__win == None:
            return

        self.__cells[i][j].draw(c_x1, c_y1, c_x2, c_y2)
        self.__animate()

    def __break_entrance_and_exit(self):
            self.__cells[0][0].has_top_wall = False
            self.__draw_cell(0,0)

            self.__cells[self.__num_cols-1][self.__num_rows-1].has_bottom_wall = False
            self.__draw_cell(self.__num_cols-1,self.__num_rows-1)

    def __animate(self):

        if self.__win == None:
            return
        self.__win.redraw()
        time.sleep(0.05)
    
    def __break_walls_r(self, i: int, j: int) -> None:
        self.__cells[i][j].visited = True
        while True:
            next_cells = []

            # determine which cell(s) to visit next
            # left
            if i > 0 and not self.__cells[i - 1][j].visited:
                next_cells.append((i - 1, j))
            # right
            if i < self.__num_cols - 1 and not self.__cells[i + 1][j].visited:
                next_cells.append((i + 1, j))
            # up
            if j > 0 and not self.__cells[i][j - 1].visited:
                next_cells.append((i, j - 1))
            # down
            if j < self.__num_rows - 1 and not self.__cells[i][j + 1].visited:
                next_cells.append((i, j + 1))

            # if there is nowhere to go from here, just break out
            if len(next_cells) == 0:
                self.__draw_cell(i, j)
                return

            # randomly choose the next direction to go
            direction_index = random.randrange(len(next_cells))
            next_index = next_cells[direction_index]

            # knock out walls between this cell and the next cell(s)
            # right
            if next_index[0] == i + 1:
                self.__cells[i][j].has_right_wall = False
                self.__cells[i + 1][j].has_left_wall = False
            # left
            if next_index[0] == i - 1:
                self.__cells[i][j].has_left_wall = False
                self.__cells[i - 1][j].has_right_wall = False
            # down
            if next_index[1] == j + 1:
                self.__cells[i][j].has_bottom_wall = False
                self.__cells[i][j + 1].has_top_wall = False
            # up
            if next_index[1] == j - 1:
                self.__cells[i][j].has_top_wall = False
                self.__cells[i][j - 1].has_bottom_wall = False

            # recursively visit the next cell
            self.__break_walls_r(next_index[0], next_index[1])

    def __reset_cells_visited(self) -> None:
        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__cells[i][j].visited = False

    # returns True if this is the end cell, OR if it leads to the end cell.
    # returns False if this is a loser cell.
    def _solve_r(self, i: int, j: int) -> bool:
        self.__animate()

        # vist the current cell
        self.__cells[i][j].visited = True

        # if we are at the end cell, we are done!
        if i == self.__num_cols - 1 and j == self.__num_rows - 1:
            return True

        # move left if there is no wall and it hasn't been visited
        if (
            i > 0
            and not self.__cells[i][j].has_left_wall
            and not self.__cells[i - 1][j].visited
        ):
            self.__cells[i][j].draw_move(self.__cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                self.__cells[i][j].draw_move(self.__cells[i - 1][j], True)

        # move right if there is no wall and it hasn't been visited
        if (
            i < self.__num_cols - 1
            and not self.__cells[i][j].has_right_wall
            and not self.__cells[i + 1][j].visited
        ):
            self.__cells[i][j].draw_move(self.__cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self.__cells[i][j].draw_move(self.__cells[i + 1][j], True)

        # move up if there is no wall and it hasn't been visited
        if (
            j > 0
            and not self.__cells[i][j].has_top_wall
            and not self.__cells[i][j - 1].visited
        ):
            self.__cells[i][j].draw_move(self.__cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self.__cells[i][j].draw_move(self.__cells[i][j - 1], True)

        # move down if there is no wall and it hasn't been visited
        if (
            j < self.__num_rows - 1
            and not self.__cells[i][j].has_bottom_wall
            and not self.__cells[i][j + 1].visited
        ):
            self.__cells[i][j].draw_move(self.__cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self.__cells[i][j].draw_move(self.__cells[i][j + 1], True)

        # we went the wrong way let the previous cell know by returning False
        return False

    def solve(self) -> bool:
        return self._solve_r(0, 0)

