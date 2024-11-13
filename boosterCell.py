from cell import Cell

class BoosterCell(Cell):

    def __init__(self, row:int, col:int, rotation:int):
    
        super().__init__()
        self.row = row
        self.col = col
        self.rotation = rotation

    def interact(self, car, y:int, x:int):
        
        car.speed *= 1.1
