from abc import ABC, abstractmethod
import random
import math

class Component(ABC):

    _registry = {"friction": "Friction cell slows the car down",
                 "Booster": "Booster cell increases speed.",
                 "Rock": "Stops the car",
                 "Slippery": "Changes the angle",
                 "turn90": "Rotates the car",
                 "straight": "Goes straight",
                 "fuel": "Fuel cell to refuel the cars",
                 "Ferrari": "A sports car"
                 }

    @abstractmethod
    def desc(self):
        pass

    @abstractmethod
    def type(self):
        pass

    @abstractmethod
    def attrs(self):
        pass

    """    @abstractmethod
    def __getattr__(self, attr):
        pass

    @abstractmethod
    def __setattr__(self, attr, value):
        pass
    """
    @abstractmethod
    def draw(self):
        pass

    @classmethod
    def list(self):

        print(list(self._registry.items()))

    @classmethod
    def create(self, type):

        if type == "slippery":
            pass
        elif type == "booster":
            return BoosterCell()
        elif type == "checkpoint":
            return CheckpointCell()
        elif type == "friction":
            return FrictionCell()
        elif type == "rock":
            return ObstacleCell()
        elif type == "slippery":
            return SlipperyCell()
        elif type == "turn90":
            return Turn90Cell()
        elif type == "straight":
            return StraightCell()
        elif type == "fuel":
            return FuelCell()
        elif type == "Ferrari":
            return Ferrari()
        else:
            raise "Unknown cell type"

    @classmethod
    def register(type, cls):
        cls._registry[type] = cls

    @classmethod
    def unregister(type, cls):
        del cls._registry[type]

class ComponentFactory(Component):

    def __init__(self):
        self._components = {}
        self.owner = None # the map that owns the obj

    def __getattr__(self, attr):
        return super().__getattr__(attr)
    def __setattr__(self, attr, value):
        return super().__setattr__(attr, value)
    def attrs(self):
        return super().attrs()
    def desc(self):
        print("Interface class of Component for the Repo")
    def draw(self):
        return super().draw()
    def type(self):
        return super().type()
    def create(self, type):
        obj = super().create(type=type)

        if isinstance(obj, Car):
            obj.map = self.owner

        self._components[type] =  obj
        return obj


class Cell(Component):

    def __init__(self,): #(self, row:int, col:int, rotation:int):
    
        super().__init__()
        self.row = 0
        self.col = 0
        self.rotation = 0 # 0, 1, 2, 3

    def __getattr__(self, attr):
        
        raise f"{attr} is not supported"

        """        if attr == "row":
            return self.row
        elif attr == "col":
            return self.col
        elif attr == "rotation":
            return self.rotation
        else:
            raise "Unsupported attribute."
        """

    def __setattr__(self, attr, value):
        
        if attr == "row":
            object.__setattr__(self, attr, value)#self.row = value
        elif attr == "col":
            object.__setattr__(self, attr, value)#self.col = value
        elif attr == "rotation":
            object.__setattr__(self, attr, value)#self.rotation = value
        else:
            raise "Unsupported attribute."

    def attrs(self):
                
        return([("row",int), ("col", int), ("rotation", int)])

    def desc(self):
        return "Cell base class"

    def draw(self):
        pass

    def interact(self, car, y:int, x:int):
        pass

class BoosterCell(Cell):

    def __init__(self):
    
        super().__init__()

    def interact(self, car, y:int, x:int):
        
        car.speed *= 1.1

    def desc(self):
        return "Booster cell to increase speed"
    
    def type(self):
        return "road"
    
    def draw(self):
        print("🚀" , end="")

class CheckpointCell(Cell):

    def __init__(self):
    
        super().__init__()

    def interact(self, car, y:int, x:int):
        
        # ADD CHECPOINT
        pass

    def desc(self):
        return "Checkpoint cell to create a checkpoint."

    def type(self):
        return "checkpoint"
    
    def draw(self):
        print("🏁" , end="")

class FuelCell(Cell):

    def __init__(self):
    
        super().__init__()

    def interact(self, car, y:int, x:int):
        
        car.fuel = 1.0

    def desc(self):
        return "Fuel cell to refuel the cars."

    def type(self):
        return "fuel"
    
    def draw(self):
        print("⛽" , end="")

class FrictionCell(Cell):

    def __init__(self):
    
        super().__init__()

    def interact(self, car, y:int, x:int):
        
        car.speed *= 0.9

    def desc(self):
        return "Friction cell to slow the car down."

    def type(self):
        return "road"

    def draw(self):
        print("F" , end="")

class ObstacleCell(Cell):

    def __init__(self):
    
        super().__init__()

    def interact(self, car, y:int, x:int):
        
        car.speed = 0

    def desc(self):
        return "Obstacke cell to stop the car."

    def type(self):
        return "obstacle"

    def draw(self):
        print("🪨" , end="")

class SlipperyCell(Cell):

    def interact(self, car, y: int, x: int):
        car.rotation += 1
        car.rotation = random.choice([0, 1, 2, 3])

    def desc(self):
        return "Slippery cell to change the direction"

    def type(self):
        return "road"

    def draw(self):
        print("❄️" , end="")

class Turn90Cell(Cell):

    def __init__(self):
    
        super().__init__()

    def interact(self, car, y:int, x:int):
        
        car.angle += 90
        car.angle = car.angle%360

    def desc(self):
        return "Change the direction of the car"        

    def type(self):
        return "road"

    def draw(self):

        if self.rotation == 0:
            print("┏" , end="")
        elif self.rotation == 1:
            print("┓" , end="")
        elif self.rotation == 2:
            print("┛" , end="")                        
        elif self.rotation == 3:
            print("┗" , end="")                        

class StraightCell(Cell):

    def __init__(self):
    
        super().__init__()

    def interact(self, car, y:int, x:int):
        
        pass

    def desc(self):
        return "Straight cell, go straight ahead"     
    
    def type(self):
        return "road"

    def draw(self):

        if self.rotation % 2 == 0:
            print("-" , end="")
        else:
            print("|" , end="")

class Car(Component):

    def __init__(self, model:str, map, driver:str, pos:tuple = (0,0), angle:int=0, topspeed:int=100, topfuel:int=100, speed:float=0.0, fuel:float=100.0):

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

    def attrs(self):

        attr_list = [(attr, type(value)) for attr, value in vars(self).items()]
        return attr_list
    
    def desc(self):
        return "Default car."

    def type(self):
        return type(self)

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
                if self.speed > self.topspeed:
                    self.speed = self.topspeed


            if(self.breakFlag):
                self.speed -= 2 

            distance = self.speed /10 ## assuming tick per 0.1 second
            if self.fuel < ((distance / 100 ) * (self.speed / 100)): ## not enough fuel, go till zero, set fuel to zero
                distance = (self.fuel / ((distance / 100 ) * (self.speed / 100))) * distance
                self.fuel = 0 
            else:
                self.fuel = self.fuel - ((distance / 100 ) * (self.speed / 100)) ## have enough fuel, reduce it

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


            move(distance)

            if(self.breakFlag):
                self.speed -= 10 
                self.breakFlag = False

            ## move it with average speed, then set normal speed

            if(self.accelFlag):
                self.speed += acceleration
                self.accelFlag = False


            self.accelFlag = False
            self.breakFlag = False
            self.turnLeftFlag = False
            self.turnRightFlag = False       

class Ferrari(Car):

    def __init__(self, model="Ferrari", map=None, driver=None, pos=(0,0), angle=0, topspeed=250, topfuel=100, speed=0.0, fuel=100):
        super().__init__(model, map, driver, pos, angle, topspeed, topfuel, speed, fuel)

    def draw(self):

        print("🏎️", end="")

    def desc(self):
        return "Ferrari, sports car."


