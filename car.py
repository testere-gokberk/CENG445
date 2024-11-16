from components import Component
import math

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

    def breakd(self):
        self.breakFlag = True        

    def left(self):
        self.turnLeftFlag = True
    
    def right(self):
        self.turnRightFlag = True

    def tick(self):
        ## get components and interact
        
        # Iterate over each component in the stack at the calculated cell position
        
        if self.carStarted:
            row = int(self.pos[0] // self.map.cellsize)
            col = int(self.pos[1] // self.map.cellsize)
            if not self.map.cells[row][col]:
                self.speed = 5 ## set a minimum value
            else:
                for cell in self.map.cells[row][col]:
                    cell.interact(self, self.pos[0] % self.map.cellsize, self.pos[1] % self.map.cellsize)  

            ## assume tick per  0.1 second
                    
            if self.turnLeftFlag:
                self.turnLeftFlag = False   
                self.angle += 90
                if self.angle >=360:
                    self.angle -= 360
            
            if self.turnRightFlag:
                self.turnRightFlag = False
                self.angle -= 90
                if self.angle < 0:
                    self.angle += 360
            def get_acceleration(speed,  max_accel=30, decay_rate=0.015):
                    if speed >= self.topspeed:
                        return 0  # Acceleration is 0 at or beyond max_speed
                    accel = (max_accel * math.exp(-decay_rate * speed)) / 10
                    return accel  
                  
            if(self.accelFlag):
                acceleration = get_acceleration(self.speed) / 2
                self.speed += acceleration


            if(self.breakFlag):
                self.speed -= 2 

            distance = self.speed /10 ## assuming tick per 0.1 second
            if self.fuel < ((distance / 100 ) * (self.speed / 100)): ## not enough fuel, go till zero, set fuel to zero
                distance = (self.fuel / ((distance / 100 ) * (self.speed / 100))) * distance
                self.fuel = 0 
            else:
                self.fuel = self.fuel - ((distance / 100 ) * (self.speed / 100)) ## have enough fuel, reduce it

            move(distance)

            if(self.breakFlag):
                self.speed -= 10 
                self.breakFlag = False

            ## move it with average speed, then set normal speed

            if(self.accelFlag):
                self.speed += acceleration
                self.accelFlag = False


            def move(distance_to_travel):
                

                yexceeded = False
                xexceeded = False
                negativey = False
                negativex = False
                
                
                newy = self.speed * math.sin(math.radians(self.angle)) + self.pos[0]
                newx = self.speed * math.cos(math.radians(self.angle)) + self.pos[1]

                

                # Check for exceeding map boundaries and calculate remaining distance
                if newy > self.map.rows * self.map.cellsize:
                    distance_traveled = (self.map.rows * self.map.cellsize - self.pos[0]) / math.sin(math.radians(self.angle))
                    remaining_distance = distance_to_travel - distance_traveled
                    newy = self.map.rows * self.map.cellsize
                    yexceeded = True

                elif newy < 0:
                    distance_traveled = -self.pos[0] / math.sin(math.radians(self.angle))
                    remaining_distance = distance_to_travel - distance_traveled
                    newy = 0
                    negativey = True
                else:
                    remaining_distance = 0

                if newx > self.map.cols * self.map.cellsize:
                    distance_traveled = (self.map.cols * self.map.cellsize - self.pos[1]) / math.cos(math.radians(self.angle))
                    remaining_distance = distance_to_travel - distance_traveled
                    newx = self.map.cols * self.map.cellsize
                    xexceeded = True

                elif newx < 0:
                    distance_traveled = -self.pos[1] / math.cos(math.radians(self.angle))
                    remaining_distance = distance_to_travel - distance_traveled
                    newx = 0
                    negativex = True
                else:
                    remaining_distance = 0

                # Reflect the car's direction according to edge normal
                if xexceeded or negativex:
                    self.angle = 180 - self.angle
                    if self.angle < 0:
                        self.angle += 360  # Keep angle in [0, 360)

                if yexceeded or negativey:
                    self.angle = 360 - self.angle

                self.pos = (newy,newx)

                # Calculate new position after reflection using the remaining distance


                if remaining_distance > 0:
                    move(remaining_distance)

            self.accelFlag = False
            self.breakFlag = False
            self.turnLeftFlag = False
            self.turnRightFlag = False
        
