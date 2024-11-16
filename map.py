import components

class Map:

    def __init__(self, cols:int, rows:int, cellsize:int, bgcolor:str):
        
        self.cols = cols
        self.rows = rows
        self.cellsize = cellsize
        self.bgcolor = bgcolor

        self.cells = [self.cols*[None] for _ in range(self.rows)]

        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j] = []

        self.components = components.ComponentFactory()# component, pos pairs

    def __getitem__(self, pos:tuple):

        row, col = pos
        
        try:
            return self.cells[row][col][-1]
        except IndexError:
            raise "Given index exceeds map size"

    def __setitem__(self, pos:tuple, component):

        row, col = pos
        self.cells[row][col].append(component)

    def __del__(self, pos:tuple):

        row, col = pos
        self.cells[row][col] = []

    def getxy(self, y:int, x:int):

        return self.cells[x%self.cellsize][y%self.cellsize][-1]

    def place(self, obj, y:int, x:int):

        self.components[obj] = (x, y)

    def view(self, y:int, x:int, height:int, width:int):

        pass

    def draw(self):
        
        bar = "\n" +"----"*self.cols
        for i in range(self.rows):

            print(" | ", end="")
            for j in range(self.cols):
                
                if len(self.cells[i][j]) > 0 and isinstance(self.cells[i][j][-1], components.Cell):

                    self.cells[i][j][-1].draw()
                    print(" | ", end="")
                else:
                    print("X", end="")
                    print(" | ", end="")

            
            print(bar)

    def view(self, y, x, height, width):

        temp = View(y=y/self.cellsize, x=x/self.cellsize ,cols=self.cols-y/self.cellsize, rows=self.rows-x/self.cellsize, cellsize=height/(self.cols-y/self.cellsize), bgcolor=self.bgcolor)
        temp.components = self.components

        return temp

class View:

    def __init__(self, y:int, x:int, cols:int, rows:int, cellsize:int, bgcolor:str):
        
        self.y = int(y)
        self.x = int(x)
        self.cols = int(cols)
        self.rows = int(rows)
        self.cellsize = cellsize
        self.bgcolor = bgcolor

        self.components = components.ComponentFactory()# component, pos pairs

    def __getitem__(self, pos:tuple):

        row, col = pos
        
        try:
            return self.cells[row][col][-1]
        except IndexError:
            raise "Given index exceeds map size"

    def __setitem__(self, pos:tuple, component):

        row, col = pos
        self.cells[row][col].append(component)

    def __del__(self, pos:tuple):

        row, col = pos
        self.cells[row][col] = []

    def getxy(self, y:int, x:int):

        return self.cells[x%self.cellsize][y%self.cellsize][-1]

    def place(self, obj, y:int, x:int):

        self.components[obj] = (x, y)

    def view(self, y:int, x:int, height:int, width:int):

        pass

    def draw(self):
        
        bar = "\n" +"----"*self.cols
        for i in range(self.x, self.rows):

            print(" | ", end="")
            for j in range(self.x, self.cols):
                
                if len(self.cells[i][j]) > 0 and isinstance(self.cells[i][j][-1], components.Cell):

                    self.cells[i][j][-1].draw()
                    print(" | ", end="")
                else:
                    print("X", end="")
                    print(" | ", end="")

            
            print(bar)
    