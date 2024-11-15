from cell import Cell
from component import Component
from car import Car

class Map:
    def __init__(self, cols: int, rows: int, cellsize: int, bgcolor: str):
        self.cols = cols
        self.rows = rows
        self.cellsize = cellsize
        self.bgcolor = bgcolor
        # Initialize a 2D grid where each cell is a stack (list) to hold multiple components
        self.cells = [[[] for _ in range(self.cols)] for _ in range(self.rows)]
        self.components = dict()  # Dictionary to store component-object and position pairs

    def __getitem__(self, pos: tuple):
        """
        Returns the top component at the specified grid position.
        """
        row, col = pos
        if 0 <= row < self.rows and 0 <= col < self.cols:
            if self.cells[row][col]:
                return self.cells[row][col][-1]  # Return the top component
            else:
                return None  # No component at this position
        else:
            raise ValueError("Given index exceeds map size")

    def __setitem__(self, pos: tuple, component):
        """
        Adds a new component to the stack at the specified grid position.
        """
        row, col = pos
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.cells[row][col].append(component)  # Stack component on top
        else:
            raise ValueError("Given index exceeds map size")

    def __delitem__(self, pos: tuple):
        """
        Removes the top component from the stack at the specified grid position.
        """
        row, col = pos
        if 0 <= row < self.rows and 0 <= col < self.cols:
            if self.cells[row][col]:
                self.cells[row][col].pop()  # Remove the top component
            else:
                raise ValueError("No cell to delete at the given position")
        else:
            raise ValueError("Given index exceeds map size")

    def getxy(self, y: int, x: int):
        """
        Returns the top component at the pixel position (y, x).
        Use modulo operations to map pixels to grid cells.
        """
        row = y // self.cellsize
        col = x // self.cellsize
        if 0 <= row < self.rows and 0 <= col < self.cols:
            if self.cells[row][col]:
                return self.cells[row][col][-1]  # Return the top component
            else:
                return None  # No component at this position
        else:
            raise ValueError("Pixel position exceeds map size")

    def place(self, obj, y: int, x: int):
       


        car = Car("merso", self, "messi", (y,x), 0, 100, 100, 20, 100)

        
        ## needs to be added to components list if necessary

        

    def view(self, y: int, x: int, height: int, width: int):
        
        ## todo

    def draw(self):
        
        ## todo
        
