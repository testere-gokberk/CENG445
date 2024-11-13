from cell import Cell
import random

class CheckpointCell(Cell):

    def __init__(self, row:int, col:int, rotation:int):
    
        super().__init__()
        self.row = row
        self.col = col
        self.rotation = rotation

    def interact(self, car, y:int, x:int):
        
        # ADD CHECPOINT
