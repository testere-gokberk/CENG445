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
        self.components.owner = self

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
        
        cars = []

        print("DRAWING")
        print(self.components)
        for component_name, component_obj in self.components._components.items():

            print(component_obj)
            if isinstance(component_obj, components.Car):
                cars.append((component_obj, (int(component_obj.pos[0]/self.cellsize), int(component_obj.pos[1]/self.cellsize))))

        bar = "\n" +"----"*self.cols
        for i in range(self.rows):

            print(" | ", end="")
            for j in range(self.cols):

                car_printed = False

                for car in cars:
                    if car[1][0] == i and car[1][1] == j:
                        car[0].draw()
                        car_printed = True

                if car_printed:
                    print(" | ", end="")
                    continue
                
                if len(self.cells[i][j]) > 0 and isinstance(self.cells[i][j][-1], components.Cell):

                    self.cells[i][j][-1].draw()
                    print(" | ", end="")
                else:
                    print("X", end="")
                    print(" | ", end="")

            
            print(bar)

    def view(self, y, x, height, width):

        return View(self, y, x, height, width)


class View:
    def __init__(self, parent_map, start_row, start_col, height, width):
       

        self.parent_map = parent_map
        self.start_row = start_row // parent_map.cellsize
        self.start_col = start_col // parent_map.cellsize
        self.view_rows = height // parent_map.cellsize
        self.view_cols = width // parent_map.cellsize

    def __getitem__(self, pos):
        row, col = pos
        actual_row = self.start_row + row
        actual_col = self.start_col + col
        return self.parent_map[actual_row, actual_col]

    def __setitem__(self, pos, component):
        row, col = pos
        actual_row = self.start_row + row
        actual_col = self.start_col + col
        self.parent_map[actual_row, actual_col] = component

    def __delitem__(self, pos):
        row, col = pos
        actual_row = self.start_row + row
        actual_col = self.start_col + col
        del self.parent_map[actual_row, actual_col]

    def draw(self):
        
        bar = "\n" + "----" * self.view_cols
        for i in range(self.view_rows):
            print(" | ", end="")
            for j in range(self.view_cols):
                actual_row = self.start_row + i
                actual_col = self.start_col + j
                if len(self.parent_map.cells[actual_row][actual_col]) > 0 and isinstance(
                    self.parent_map.cells[actual_row][actual_col][-1], components.Cell
                ):
                    self.parent_map.cells[actual_row][actual_col][-1].draw()
                    print(" | ", end="")
                else:
                    print("X", end="")
                    print(" | ", end="")
            print(bar)