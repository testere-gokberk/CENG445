from abc import ABC, abstractmethod
from typing import Any

class Component(ABC):

    @abstractmethod
    def desc(self):
        pass

    @abstractmethod
    def type(self):
        pass

    @abstractmethod
    def attrs(self):
        pass

    @abstractmethod
    def __getattr__(self, attr):
        pass

    @abstractmethod
    def __setattr__(self, attr, value):
        pass

    @abstractmethod
    def draw(self):
        pass


