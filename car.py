from component import Component


class Car(Component):

    def __init__(self, model:str, map, driver:str, pos:tuple, angle:int, topspeed:int, topfuel:int, speed:float, fuel:float):

        super().__init__()
        self.model = model
        self.map = map
        self.driver = driver 
        self.pos = pos
        self.angle = angle
        self.topspeed = topspeed
        self.topfuel = topfuel
        self.speed = speed
        self.fuel = fuel

        self.carStarted = False
        self.accelFlag = False
        self.breakFlag = False
        self.turnLeftFlag = False
        self.turnRightFlag = False

    def start(self):
        self.carStarted = True

    def stop(self):
        self.carStarted = False

    
    def accel(self):
        self.accelFlag = True    

    def break(self):
        self.breakFlag = True        

    def left(self):
        self.turnLeftFlag = True
    
    def right(self):
        self.turnRightFlag = True

    def tick(self):

        if self.carStarted:

            
    


        self.accelFlag = False
        self.breakFlag = False
        self.turnLeftFlag = False
        self.turnRightFlag = False
        
