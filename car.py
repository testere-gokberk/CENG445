from component import Component
from abc import ABC, abstractmethod


class Car(Component):

    def __init__(self, model:str, map, driver, pos:tuple, angle:int, topspeed:int, topfuel:int, speed:float, fuel:float):

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

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def accel(self):
        pass    

    @abstractmethod
    def break(self):
        pass        

    @abstractmethod
    def left(self):
        pass
    
    @abstractmethod
    def right(self):
        pass

    @abstractmethod
    def tick(self):
        pass
