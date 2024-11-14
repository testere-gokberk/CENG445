from cell import Cell

class Map:

    def __init__(self, cols:int, rows:int, cellsize:int, bgcolor:str):
        
        self.cols = cols
        self.rows = rows
        self.cellsize = cellsize
        self.bgcolor = bgcolor

        self.cells = [self.cols*[None] for _ in range(self.rows)]

        self.components = dict() # component, pos pairs

    def __getitem__(self, pos:tuple):

        row, col = pos
        
        try:
            return self.cells[row][col]
        except IndexError:
            raise "Given index exceeds map size"

    def __setitem__(self, pos:tuple, component):

        row, col = pos
        self.cells[row][col] = component

    def __del__(self, pos:tuple):

        row, col = pos
        self.cells[row][col] = None

    def getxy(self, y:int, x:int):

        return self.cells[x%self.cellsize][y%self.cellsize]

    def place(self, obj, y:int, x:int):

        self.components[obj] = (x, y)

    def view(self, y:int, x:int, height:int, width:int):

        pass

    def draw():

        pass

    