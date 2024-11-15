from cell import Cell

class RefuelCell(Cell):

    def __init__(self, row:int, col:int, rotation:int):
    
        super().__init__()
        self.row = row
        self.col = col
        self.rotation = rotation

    def interact(self, car, y:int, x:int):
        
        car.fuel = car.fuel + 20
        if car.fuel>car.topfuel:
            car.fuel = car.topfuel
