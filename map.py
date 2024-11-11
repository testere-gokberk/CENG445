
class Map:

    def __init__(self, cols:int, rows:int, cellsize:int, bgcolor:str):
        
        self.cols = cols
        self.rows = rows
        self.cellsize = cellsize
        self.bgcolor = bgcolor

    def __getitem__(self, pos:tuple):

        row, col = pos


    def __setitem__(self, pos:tuple, component):

        pass

    def __del__(self, pos:tuple):

        pass

    def getxy(self, y:int, x:int):

        pass

    def place(self, obj, y:int, x:int):

        pass

    def view(self, y:int, x:int, height:int, width:int):

        pass

    def draw():

        pass

    