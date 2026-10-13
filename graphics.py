import time
from tkinter import BOTH, Canvas, Tk
import random


class Window:
    def __init__(self, width: int, height: int) -> None:
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self) -> None:
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self) -> None:
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")

    def close(self) -> None:
        self.__running = False

    def draw_line(self, line: Line, fill_color): 
        line.draw(self.__canvas, fill_color)

    

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1: Point, point2: Point):
        self.p1 = point1
        self.p2 = point2

    def draw(self, canvas, fill_color: str, width: int = 2):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=width)

class Cell:
    def __init__(self, win: Window = None) -> None:
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = -1.0
        self.__x2 = -1.0
        self.__y1 = -1.0
        self.__y2 = -1.0
        self.__win = win
        self.visited = False
        
    def draw(self, x1: float, y1: float, x2: float, y2: float):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

        if self.__win == None:
            return
    
        if self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self.__win.draw_line(line, "black")
        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self.__win.draw_line(line, "black")
        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self.__win.draw_line(line, "black")
        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self.__win.draw_line(line, "black")

        # Draw missing walls as lines with the same color as the background
        if not self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self.__win.draw_line(line, "white")
        if not self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self.__win.draw_line(line, "white")
        if not self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self.__win.draw_line(line, "white")
        if not self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self.__win.draw_line(line, "white")

    def draw_move(self, to_cell: Cell, undo: bool = False) -> None:
        fill_color = "gray" if undo else "red"

        mid1_x = (self.__x1 + self.__x2) // 2
        mid1_y = (self.__y1 + self.__y2) // 2

        mid2_x = (to_cell.__x1 + to_cell.__x2) // 2
        mid2_y = (to_cell.__y1 + to_cell.__y2) // 2

        line = Line(Point(mid1_x,mid1_y), Point(mid2_x,mid2_y))

        if self.__win == None:
            return
        
        self.__win.draw_line(line, fill_color=fill_color)