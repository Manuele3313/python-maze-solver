from tkinter import Tk, BOTH, Canvas
from graphics import Window, Point, Line, Cell
from maze import Maze
def main():

    # Create the Window
    window = Window(1020,1020)

    # Create the Maze
    maze = Maze(10,10,10,10,100,100,window,0x1da0)

    is_solvable = maze.solve()
    if not is_solvable:
        print("Maze cannot be solved!")
    else:
        print("Maze solved!")
    
    window.wait_for_close()

main()